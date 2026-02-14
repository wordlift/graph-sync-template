from pathlib import Path
import sys


def test_runtime_assets_present() -> None:
    root = Path.cwd()
    assert (root / "copier.yml").exists()
    assert (root / "worai.toml").exists()
    assert not (root / "profiles" / "_base" / "postprocessors.toml").exists()
    assert (root / "profiles" / "_base" / "postprocessors.example.toml").exists()
    assert (root / "profiles" / "default" / "mappings" / "default.yarrrml.j2").exists()
    assert (root / "profiles" / "default" / "templates" / "1_organization.ttl.j2").exists()
    assert (root / ".github" / "workflows" / "graph-sync.yml").exists()
    assert not (root / ".github" / "workflows" / "update-kg.yml").exists()
    assert (root / "src" / "acme_kg" / "postprocessors" / "youtube.py").exists()
    assert not (root / "src" / "acme_kg" / "postprocessors" / "pricing.py").exists()


def test_runtime_imports() -> None:
    sys.path.insert(0, str((Path.cwd() / "src").resolve()))
    from acme_kg.postprocessors import YouTubePostprocessor  # noqa: F401


def test_profile_based_workflow_contract() -> None:
    workflow = Path(".github/workflows/graph-sync.yml").read_text(encoding="utf-8")
    assert "workflow_dispatch" in workflow
    assert "profile:" in workflow
    assert "country:" not in workflow


def test_copier_contract_contains_required_questions() -> None:
    copier = Path("copier.yml").read_text(encoding="utf-8")
    for key in (
        "project_slug:",
        "customer_name:",
        "api_key:",
        "source_type:",
        "profiles:",
        "default_profile:",
    ):
        assert key in copier

    assert "urls is required when source_type=urls" in copier
    assert "sitemap_url is required when source_type=sitemap" in copier
    assert "sheets_url is required when source_type=google_sheets" in copier
