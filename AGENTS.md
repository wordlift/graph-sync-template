## Rules

**Mandatory Verification (Tests):**
- **Never** consider a code change complete without running tests.
- If a change modifies logic, **new tests must be added** or existing ones updated.

**Documentation & Status Sync:**
- **Proactive Updates:** Every task must conclude with a review of the documentation. If the logic, architecture, or setup changed, update `README.md`, `specs/`, and `AGENTS.md` accordingly.
- **TODO Sync:** Always update `TODO.md` to mark completed items or add newly identified technical debt/tasks.

## Current Architecture Notes

- Repository scope is a Copier template for `worai graph sync` projects.
- Template question contract is in `copier.yml`.
- Copier post-generation tasks create `.env` from sensitive answers and scaffold per-profile runtime directories.
- Copier post-generation tasks remove `.copier-answers.yml`, and generated output excludes `copier.yml`, to detach generated projects from Copier update tracking.
- Copier can validate API keys via WordLift `/accounts/me` during generation.
- Copier derives runtime package name from `dataset_uri` and renames local runtime package from `acme_kg` accordingly.
- Copier sets generated `pyproject.toml` `[project].name` from the destination directory, normalized to a valid Python project name.
- Workflow contract is profile-based (no country input), in `.github/workflows/graph-sync.yml`.
- Runtime config template is `worai.toml.jinja` (rendered output: `worai.toml`).
- Runtime template follows SDK v8 cloud-flow contract (`ingest_source`, `ingest_loader`, `ingest_timeout_ms`; no `web_page_import_*` fallback keys).
- Runtime template sets `materialization_backend = "worph"` in `[profiles._base]`.
- Template render smoke verification is in `scripts/smoke_render_template.sh` and CI workflow `.github/workflows/template-smoke.yml` (excluded from generated output).
- Template-maintenance tests (`tests/test_runtime_assets.py`, `tests/test_template_smoke.py`, `tests/test_youtube_runtime.py`) are excluded from generated output.
- Postprocessor example contract is in `profiles/_base/postprocessors.example.toml`.
- Local Python example runtime code is in:
  - `src/acme_kg/postprocessors/youtube.py`
  - `src/acme_kg/enrichment/youtube.py`

## Maintainer Macros

- `deploy release [major|minor|patch]` (default: `patch`)
  - Script: `scripts/deploy_release.sh [major|minor|patch]`
  - Steps:
    - bump release version
    - refresh dependencies and lockfile (`uv sync --dev`, `uv lock`)
    - update `AGENTS.md`, `README.md`, `specs/`, and `docs/`
    - commit all changes, create tag, push branch and tags

- `upgrade project`
  - Script: `scripts/upgrade_project.sh`
  - Steps:
    - update to latest `wordlift-sdk` in `pyproject.toml` and lockfile
    - update `.github/workflows/graph-sync.yml` to latest `wordlift/graph-sync` tag
    - run `deploy release patch` macro
