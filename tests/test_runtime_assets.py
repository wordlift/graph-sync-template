from pathlib import Path
import importlib.util
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


def _load_post_copy_helper():
    helper_path = Path(".copier-tasks/post_copy.py")
    spec = importlib.util.spec_from_file_location("post_copy", helper_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_runtime_assets_present() -> None:
    root = Path.cwd()
    assert (root / "copier.yml").exists()
    assert (root / ".copier-tasks" / "context.json.jinja").exists()
    assert (root / ".copier-tasks" / "post_copy.py").exists()
    assert (root / "AGENTS.md").exists()
    assert (root / "AGENTS.md.jinja").exists()
    assert (root / "README.md").exists()
    assert (root / "README.md.jinja").exists()
    assert (root / "docs" / "QUICKSTART.md").exists()
    assert ".private/" in (root / ".gitignore").read_text(encoding="utf-8")
    assert not (root / "specs").exists()
    assert not (root / "TODO.md").exists()
    assert (root / "worai.toml.jinja").exists()
    jinja = (root / "worai.toml.jinja").read_text(encoding="utf-8")
    assert "log_level = {{ log_level | tojson }}" in jinja
    assert "graph_write_strategy = {{ graph_write_strategy | tojson }}" in jinja
    assert 'materialization_backend = "worph"' in jinja
    assert "canonical_id_strategy = {{ canonical_id_strategy | tojson }}" in jinja
    assert "concurrency = {{ concurrency }}" in jinja
    assert "postprocessor_pool_size = {{ postprocessor_pool_size }}" in jinja
    assert "postprocessor_runtime = {{ postprocessor_runtime | tojson }}" in jinja
    assert "shacl_pool_size = {{ shacl_pool_size }}" in jinja
    assert "shacl_exclude_builtin_shapes = {{ shacl_exclude_builtin_shapes | tojson }}" in jinja
    assert "mapping_pool_size = {{ mapping_pool_size }}" in jinja
    assert "ingest_loader = {{ ingest_loader | tojson }}" in jinja
    assert "playwright_wait_until = {{ playwright_wait_until | tojson }}" in jinja
    assert "playwright_headless = {{ playwright_headless | lower }}" in jinja
    assert "ingest_timeout_ms = {{ ingest_timeout_ms }}" in jinja
    assert "crawler_js_render_mode = {{ crawler_js_render_mode | tojson }}" in jinja
    assert "crawler_proxy_mode = {{ crawler_proxy_mode | tojson }}" in jinja
    assert "ingest_retry_attempts = {{ ingest_retry_attempts }}" in jinja
    assert "ingest_retry_backoff_ms = {{ ingest_retry_backoff_ms }}" in jinja
    assert "google_search_console = {{ google_search_console | lower }}" in jinja
    assert not (root / "profiles" / "_base" / "postprocessors.toml").exists()
    assert (root / "profiles" / "_base" / "postprocessors.example.toml").exists()
    assert (root / "profiles" / "default" / "mappings" / "default.yarrrml.j2").exists()
    assert (root / "profiles" / "default" / "templates" / "20_organization.ttl.j2").exists()
    assert (root / "profiles" / "default" / "templates" / "20_website.ttl.j2").exists()
    assert (root / "profiles" / "default" / "templates" / "40_organization_postal_address.ttl.j2").exists()
    assert (root / ".github" / "workflows" / "graph-sync.yml").exists()
    assert (root / "scripts" / "deploy_release.sh").exists()
    assert (root / "scripts" / "upgrade_project.sh").exists()
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
    lockfile = Path("uv.lock").read_text(encoding="utf-8")
    assert 'wordlift-sdk>=8.4.1,<9.0.0' in pyproject
    assert re.search(r'(?ms)^name = "wordlift-sdk"\nversion = "8\.4\.1"$', lockfile)


def test_profile_based_workflow_contract() -> None:
    workflow = Path(".github/workflows/graph-sync.yml").read_text(encoding="utf-8")
    assert "workflow_dispatch" in workflow
    assert "profile:" in workflow
    assert "country:" not in workflow
    assert "wordlift/graph-sync@v6" in workflow
    assert 'worai_version: "6.20.10"' in workflow
    assert "graph_kpis_enabled: true" in workflow
    assert "python-version: '3.12'" in workflow
    assert "enable-cache: true" in workflow
    assert "cache-dependency-glob:" in workflow
    assert "uv sync --locked --no-dev" in workflow
    assert "cache-python:" not in workflow


def test_template_smoke_workflow_uses_uv() -> None:
    workflow = Path(".github/workflows/template-smoke.yml").read_text(encoding="utf-8")
    assert "astral-sh/setup-uv@v6" in workflow
    assert "actions/setup-python" not in workflow
    assert "python-version: '3.12'" in workflow
    assert "enable-cache: true" in workflow
    assert "cache-dependency-glob:" in workflow
    assert "uv sync --all-extras --dev" in workflow
    assert "uv run pytest -q" in workflow
    assert "uv run scripts/smoke_render_template.sh" in workflow


def test_upgrade_project_updates_sdk_without_pinning_worai() -> None:
    script = Path("scripts/upgrade_project.sh").read_text(encoding="utf-8")
    assert "https://pypi.org/pypi/wordlift-sdk/json" in script
    assert "uv lock --upgrade-package wordlift-sdk" in script
    assert "https://pypi.org/pypi/worai/json" not in script
    assert "worai_version" not in script
    assert "wordlift/graph-sync@" not in script


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
    assert "help: Source of your page list" in copier
    assert '"Manual URL list": urls' in copier
    assert '"Sitemap XML": sitemap' in copier
    assert '"Google Sheets": google_sheets' in copier
    assert "help: Sitemap URL" in copier
    assert "concurrency:\n  type: int\n  default: 4" in copier
    assert 'concurrency:\n  type: int\n  default: 4\n  help: Parallel import workers\n  when: "{{ false }}"' in copier
    assert 'log_level:\n  type: str\n  default: warning' in copier
    assert 'graph_write_strategy:\n  type: str\n  default: put' in copier
    assert 'canonical_id_strategy:\n  type: str\n  default: dependency_graph' in copier
    assert 'postprocessor_pool_size:\n  type: int\n  default: 2' in copier
    assert 'postprocessor_runtime:\n  type: str\n  default: persistent' in copier
    assert 'shacl_pool_size:\n  type: int\n  default: 1' in copier
    assert '- google-course\n    - google-recipe' in copier
    assert 'mapping_pool_size:\n  type: int\n  default: 1' in copier
    assert 'playwright_wait_until:\n  type: str\n  default: domcontentloaded' in copier
    assert 'playwright_headless:\n  type: bool\n  default: true' in copier
    assert 'ingest_retry_attempts:\n  type: int\n  default: 2' in copier
    assert 'ingest_retry_backoff_ms:\n  type: int\n  default: 3000' in copier
    assert 'ingest_loader:\n  type: str\n  default: crawler\n  help: Ingestion loader' in copier
    assert "    - crawler\n" in copier
    assert "ingest_timeout_ms:\n  type: int\n  default: 600000" in copier
    assert 'crawler_js_render_mode:\n  type: str\n  default: disabled' in copier
    assert 'crawler_proxy_mode:\n  type: str\n  default: disabled' in copier
    assert 'google_search_console:\n  type: bool\n  default: false\n  help: Enable Google Search Console enrichment\n  when: "{{ false }}"' in copier
    assert 'profiles:\n  type: yaml' in copier
    assert 'validator: "{% if not profiles or profiles|length == 0 %}profiles must include at least one profile{% endif %}"\n  when: "{{ false }}"' in copier
    assert 'default_profile:\n  type: str\n  default: default' in copier
    assert 'validator: "{% if default_profile not in profiles %}default_profile must be one of the selected profiles{% endif %}"\n  when: "{{ false }}"' in copier
    assert '- ".git"' in copier
    assert '- "copier.yml"' in copier
    assert '- ".github/workflows/template-smoke.yml"' in copier
    assert '- "scripts/smoke_render_template.sh"' in copier
    assert '- "tests/test_runtime_assets.py"' in copier
    assert '- "tests/test_template_smoke.py"' in copier
    assert '- "tests/test_youtube_runtime.py"' in copier
    assert "_tasks:\n  - python .copier-tasks/post_copy.py .copier-tasks/context.json" in copier
    assert "python - <<'PY'" not in copier
    assert "https://api.wordlift.io/accounts/me" not in copier
    assert "Authorization" not in copier
    assert "{{ api_key | tojson }}" not in copier
    assert "mv AGENTS" not in copier
    assert 'Path(".env").write_text' not in copier


def test_copier_post_copy_helper_contains_generation_steps() -> None:
    context_template = Path(".copier-tasks/context.json.jinja").read_text(encoding="utf-8")
    post_copy = Path(".copier-tasks/post_copy.py").read_text(encoding="utf-8")

    assert '"api_key": {{ api_key | tojson }}' in context_template
    assert '"profiles": {{ profiles | tojson }}' in context_template
    assert '"validate_api_key": {{ validate_api_key | tojson }}' in context_template
    assert 'source_type == "google_sheets"' in context_template

    assert "context_path.unlink(missing_ok=True)" in post_copy
    assert "shutil.rmtree(helper_dir, ignore_errors=True)" in post_copy
    assert "https://api.wordlift.io/accounts/me" in post_copy
    assert '"Authorization": f"Key {api_key}"' in post_copy
    assert "def clean_api_key(raw_api_key: str) -> str:" in post_copy
    assert "api_key = clean_api_key(context_string(context, \"api_key\"))" in post_copy
    assert "except ValueError as exc:" in post_copy
    assert "class ProjectNames:" in post_copy
    assert "def slug_from_account_url(account_url: str) -> str:" in post_copy
    assert "def slug_from_dataset_uri(dataset_uri: str) -> str:" in post_copy
    assert "def runtime_package_from_distribution_name(distribution_name: str) -> str:" in post_copy
    assert "def project_names_from_account_payload(" in post_copy
    assert 'GENERATED_PROJECT_VERSION = "0.1.0"' in post_copy
    assert "Generated by graph-sync-template" in post_copy
    assert "def update_project_metadata(project_names: ProjectNames) -> None:" in post_copy
    assert "def display_value_from_uri(uri: str) -> str:" in post_copy
    assert "domainUri" in post_copy
    assert "description = {json.dumps(project_names.description)}" in post_copy
    assert "datasetUri" in post_copy
    assert "OLD_PACKAGE = \"acme_kg\"" in post_copy
    assert "def normalize_slug(raw: str) -> str:" in post_copy
    assert 'normalized = re.sub(r"[^a-z0-9._-]+", "-", raw.lower())' in post_copy
    assert 'Path(".env").write_text("\\n".join(content), encoding="utf-8")' in post_copy
    assert "(profile_dir / \"mappings\").mkdir" in post_copy
    assert "(profile_dir / \"templates\").mkdir" in post_copy
    assert "templates/20_organization.ttl.j2" in post_copy
    assert "templates/20_website.ttl.j2" in post_copy
    assert "templates/40_organization_postal_address.ttl.j2" in post_copy
    assert '"__GRAPH_SYNC_PROJECT_PACKAGE__": project_names.distribution_name' in post_copy
    assert "shutil.move(str(old_dir), str(new_dir))" in post_copy
    assert 'Path(".copier-answers.yml").unlink(missing_ok=True)' in post_copy
    assert "def initialize_git_repository() -> bool:" in post_copy
    assert 'shutil.which("git")' in post_copy
    assert '["check-ignore", "-q", ".env"]' in post_copy
    assert '"initial commit"' in post_copy
    assert "Graph Sync project post-copy setup completed." in post_copy
    assert 'print(f"Project package: {project_names.distribution_name}")' in post_copy
    assert 'print(f"Runtime module: {project_names.runtime_package}")' in post_copy


def test_copier_post_copy_derives_names_from_account_url() -> None:
    post_copy = _load_post_copy_helper()

    names = post_copy.project_names_from_account_payload(
        {"url": "https://zurich.ca", "datasetUri": "https://data.wordlift.io/wl1506345/"},
        "fallback-project",
    )

    assert names.distribution_name == "graph-sync-zurich-ca"
    assert names.runtime_package == "graph_sync_zurich_ca"
    assert names.description == "Graph Sync project for zurich.ca"


def test_copier_post_copy_derives_names_from_domain_uri() -> None:
    post_copy = _load_post_copy_helper()

    names = post_copy.project_names_from_account_payload(
        {
            "url": "",
            "domainUri": "https://www.zurich.ca/insurance",
            "datasetUri": "https://data.wordlift.io/wl1506345/",
        },
        "fallback-project",
    )

    assert names.distribution_name == "graph-sync-zurich-ca-insurance"
    assert names.runtime_package == "graph_sync_zurich_ca_insurance"
    assert names.description == "Graph Sync project for zurich.ca/insurance"


def test_copier_post_copy_falls_back_to_dataset_uri_for_names() -> None:
    post_copy = _load_post_copy_helper()

    names = post_copy.project_names_from_account_payload(
        {"url": "", "datasetUri": "https://data.wordlift.io/wl1506345/"},
        "fallback-project",
    )

    assert names.distribution_name == "graph-sync-wl1506345"
    assert names.runtime_package == "graph_sync_wl1506345"
    assert names.description == "Graph Sync project for data.wordlift.io/wl1506345"


def test_copier_post_copy_falls_back_to_project_dir_for_names() -> None:
    post_copy = _load_post_copy_helper()

    names = post_copy.derive_project_names("abc123", False, "My-Graph_Project.demo")

    assert names.distribution_name == "graph-sync-my-graph-project-demo"
    assert names.runtime_package == "graph_sync_my_graph_project_demo"


def test_copier_post_copy_cleans_api_key_before_validation() -> None:
    post_copy = _load_post_copy_helper()

    assert post_copy.clean_api_key(" abc123\n") == "abc123"

    try:
        post_copy.clean_api_key("abc\nxyz")
    except SystemExit as exc:
        assert "single line" in str(exc)
    else:
        raise AssertionError("Expected multiline API key to stop generation")


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


def test_template_docs_do_not_reference_removed_specs() -> None:
    docs = [
        Path("README.md"),
        Path("README.md.jinja"),
        Path("AGENTS.md"),
        Path("AGENTS.md.jinja"),
        Path("docs/QUICKSTART.md"),
        Path("scripts/deploy_release.sh"),
    ]
    for path in docs:
        text = path.read_text(encoding="utf-8")
        assert "specs/graph-sync" not in text
        assert "TODO.md" not in text
