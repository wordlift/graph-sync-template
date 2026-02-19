from pathlib import Path
import re
import sys


def _parse_exports_manifest(text: str) -> dict[str, str]:
    entries: dict[str, str] = {}
    for key, value in re.findall(r"^([a-zA-Z0-9_]+)\s*=\s*\"([^\"]+)\"\s*$", text, flags=re.MULTILINE):
        entries[key] = value
    return entries


def _iri_depth_from_dataset_root(value: str) -> int:
    match = re.match(r"^\{\{\s*dataset_uri\s*\}\}(/.*)$", value)
    assert match is not None, f"Expected dataset-root IRI template, got: {value}"
    suffix = match.group(1)
    return len([segment for segment in suffix.split("/") if segment])


def test_runtime_assets_present() -> None:
    root = Path.cwd()
    assert (root / "copier.yml").exists()
    assert (root / "worai.toml.jinja").exists()
    assert not (root / "profiles" / "_base" / "postprocessors.toml").exists()
    assert (root / "profiles" / "_base" / "postprocessors.example.toml").exists()
    assert (root / "profiles" / "default" / "mappings" / "default.yarrrml.j2").exists()
    assert (root / "profiles" / "default" / "templates" / "20_organization.ttl.j2").exists()
    assert (root / "profiles" / "default" / "templates" / "20_website.ttl.j2").exists()
    assert (root / "profiles" / "default" / "templates" / "40_organization_postal_address.ttl.j2").exists()
    assert (root / ".github" / "workflows" / "graph-sync.yml.jinja").exists()
    assert not (root / ".github" / "workflows" / "update-kg.yml").exists()
    assert (root / "src" / "acme_kg" / "postprocessors" / "youtube.py").exists()
    assert not (root / "src" / "acme_kg" / "postprocessors" / "pricing.py").exists()


def test_static_template_conventions() -> None:
    templates_dir = Path("profiles/default/templates")
    exports_manifest = _parse_exports_manifest(
        Path("profiles/default/exports.toml.j2").read_text(encoding="utf-8")
    )

    for template_path in sorted(templates_dir.glob("*.ttl.j2")):
        text = template_path.read_text(encoding="utf-8")

        assert "_:" not in text
        assert "[]" not in text

        subjects = re.findall(
            r"^\s*<\{\{\s*exports\.([a-zA-Z0-9_]+)\s*\}\}>\s*$",
            text,
            flags=re.MULTILINE,
        )
        assert len(subjects) == 1, f"{template_path} must define exactly one subject"

        subject_export_key = subjects[0]
        assert subject_export_key in exports_manifest, (
            f"{template_path} references unknown exports key: {subject_export_key}"
        )

        depth = _iri_depth_from_dataset_root(exports_manifest[subject_export_key])
        expected_prefix = depth * 10
        prefix_match = re.match(r"^(\d+)_", template_path.name)
        assert prefix_match is not None, f"{template_path} must be prefixed with depth*10"
        assert int(prefix_match.group(1)) == expected_prefix, (
            f"{template_path} prefix must match depth {depth} ({expected_prefix})"
        )

        for predicate, obj in re.findall(r"schema:(url|sameAs)\s+([^;.]*)[;.]", text):
            assert obj.strip().startswith('"'), (
                f"{template_path} uses schema:{predicate} with non-literal object: {obj.strip()}"
            )


def test_static_exports_policy() -> None:
    exports = _parse_exports_manifest(Path("profiles/default/exports.toml.j2").read_text(encoding="utf-8"))

    root_keys = [key for key in exports if key.endswith("_root_iri")]
    assert root_keys, "Expected at least one exported root IRI"

    for key, value in exports.items():
        depth = _iri_depth_from_dataset_root(value)
        assert depth >= 2, f"{key} should include container and slug segments"
        assert "_:" not in value

    for key in root_keys:
        value = exports[key]
        assert re.search(r"-[0-9a-f]{8,}(?:/|$)", value) is None, (
            f"{key} should remain stable/unhashed in exports: {value}"
        )

    organization_root = exports["organization_root_iri"]
    address = exports["organization_postal_address_iri"]
    assert address.startswith(f"{organization_root}/postal-addresses/")


def test_runtime_imports() -> None:
    sys.path.insert(0, str((Path.cwd() / "src").resolve()))
    from acme_kg.postprocessors import YouTubePostprocessor  # noqa: F401


def test_sdk_version_constraint() -> None:
    pyproject = Path("pyproject.toml").read_text(encoding="utf-8")
    assert 'wordlift-sdk>=3.9.0,<4.0.0' in pyproject


def test_profile_based_workflow_contract() -> None:
    workflow = Path(".github/workflows/graph-sync.yml.jinja").read_text(encoding="utf-8")
    assert "workflow_dispatch" in workflow
    assert "profile:" in workflow
    assert "country:" not in workflow


def test_copier_contract_contains_required_questions() -> None:
    copier = Path("copier.yml").read_text(encoding="utf-8")
    for key in (
        "api_key:",
        "source_type:",
        "profiles:",
        "default_profile:",
    ):
        assert key in copier

    assert "urls is required when source_type=urls" in copier
    assert "sitemap_url is required when source_type=sitemap" in copier
    assert "sheets_url is required when source_type=google_sheets" in copier
    assert "sheets_name is required when source_type=google_sheets" in copier
    assert "help: WordLift API key (required)" in copier
    assert "validate_api_key:" in copier
    assert "Validate API key against WordLift API during project generation" in copier
    assert "https://api.wordlift.io/accounts/me" in copier
    assert "Authorization" in copier
    assert "dataset_uri" in copier
    assert "acme_graph_sync" in copier
    assert "package_from_dataset_uri" in copier
    assert 'package_name_file = Path(".package_name")' in copier
    assert "old_package = \"acme_kg\"" in copier
    assert "shutil.move(str(old_dir), str(new_dir))" in copier
    assert "help: Source of your page list" in copier
    assert '"Manual URL list": urls' in copier
    assert '"Sitemap XML": sitemap' in copier
    assert '"Google Sheets": google_sheets' in copier
    assert "help: Sitemap URL" in copier
    assert "concurrency:\n  type: int\n  default: 4" in copier
    assert 'concurrency:\n  type: int\n  default: 4\n  help: Parallel import workers\n  when: "{{ false }}"' in copier
    assert 'web_page_import_mode:\n  type: str\n  default: ""\n  help: Import mode override (optional)\n  when: "{{ false }}"' in copier
    assert "web_page_import_timeout:\n  type: int\n  default: 120" in copier
    assert 'google_search_console:\n  type: bool\n  default: false\n  help: Enable Google Search Console enrichment\n  when: "{{ false }}"' in copier
    assert 'profiles:\n  type: yaml' in copier
    assert 'validator: "{% if not profiles or profiles|length == 0 %}profiles must include at least one profile{% endif %}"\n  when: "{{ false }}"' in copier
    assert 'default_profile:\n  type: str\n  default: default' in copier
    assert 'validator: "{% if default_profile not in profiles %}default_profile must be one of the selected profiles{% endif %}"\n  when: "{{ false }}"' in copier
    assert '- ".git"' in copier
    assert '- ".github/workflows/template-smoke.yml"' in copier
    assert '- "tests/test_runtime_assets.py"' in copier
    assert '- "tests/test_template_smoke.py"' in copier
    assert "mv specs/graph-sync/AGENTS.md AGENTS.md" in copier
    assert 'Path(".env").write_text(chr(10).join(content), encoding="utf-8")' in copier
    assert "(profile_dir / \"mappings\").mkdir" in copier
    assert "(profile_dir / \"templates\").mkdir" in copier
    assert "templates/20_organization.ttl.j2" in copier
    assert "templates/20_website.ttl.j2" in copier
    assert "templates/40_organization_postal_address.ttl.j2" in copier


def test_copier_secret_questions_have_defaults() -> None:
    copier = Path("copier.yml").read_text(encoding="utf-8")
    api_key_block = re.search(r"^api_key:\n(?:(?:  ).*\n)+", copier, flags=re.MULTILINE)
    assert api_key_block is not None
    assert '  secret: true\n  default: ""\n' in api_key_block.group(0)
    assert "api_key is required" in api_key_block.group(0)


def test_youtube_missing_key_warning_message() -> None:
    enricher = Path("src/acme_kg/enrichment/youtube.py").read_text(encoding="utf-8")
    assert "YOUTUBE_API_KEY is not configured" in enricher
    assert "graph sync will continue" in enricher
