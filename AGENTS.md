# Graph Sync Template Agent Instructions

This repository is the Copier template used to generate graph-sync projects.
Reusable graph-sync agent behavior lives outside this repository in the installed
`wordlift/graph-sync-agent-kit` skills.
The merged reusable review draft is in `docs/GRAPH_SYNC_DOS_AND_DONTS.md`.
Durable graph-sync DOs/DONTs should move to the skill kit after review.

## Verification

- Run tests before considering code or template behavior changes complete.
- If template generation behavior changes, update smoke coverage or tests in the
  same change.
- Keep `README.md`, `docs/QUICKSTART.md`, and `AGENTS.md.jinja` aligned with
  template behavior.

## Current Architecture Notes

- Repository scope is a Copier template for graph-sync projects.
- Template question contract is in `copier.yml`.
- Copier post-generation behavior is implemented in `.copier-tasks/post_copy.py`.
- The generated `.copier-tasks/context.json` carries sensitive answers only long enough for `post_copy.py` to read it, then the helper removes it.
- Copier post-generation tasks create `.env` from sensitive answers and scaffold per-profile runtime directories.
- Copier post-generation tasks remove `.copier-answers.yml`, and generated output excludes `copier.yml`, to detach generated projects from Copier update tracking.
- Copier excludes this maintainer `AGENTS.md` and renders `AGENTS.md.jinja` as the generated project's `AGENTS.md`.
- Copier renders `README.md.jinja` as the generated project's `README.md`.
- Copier initializes generated projects as git repositories and creates an `initial commit` when `git` is available.
- Copier can validate API keys via WordLift `/accounts/me` during generation.
- Copier derives generated project package names from the WordLift account `url`, falling back to `datasetUri`, then to the destination directory when validation is skipped or unavailable.
- Copier sets generated `pyproject.toml` `[project].name` to the dashed `graph-sync-*` distribution name, sets `[project].description` from account/domain metadata, resets generated `[project].version` to `0.1.0`, adds a template-version comment, and renames local runtime code from `acme_kg` to the underscore-safe module name.
- Workflow contract is profile-based (no country input), in `.github/workflows/graph-sync.yml`.
- Runtime config template is `worai.toml.jinja` (rendered output: `worai.toml`).
- Runtime template follows SDK v8.2.1 cloud-flow contract (`ingest_source`, `ingest_loader`, `ingest_timeout_ms`; no `web_page_import_*` fallback keys).
- Default loader is `crawler`; `ingest_timeout_ms` is emitted as a comment in `worai.toml` (opt-in override); default is 600000 ms (10 min) for `crawler`, 30000 ms (30 s) for all other loaders.
- `crawler` loader supports `crawler_js_render_mode` (disabled | auto | enabled) and `crawler_proxy_mode` (disabled | simple | standard | premium | auto).
- Runtime template sets `materialization_backend = "worph"` in `[profiles._base]`.
- Template render smoke verification is in `scripts/smoke_render_template.sh` and CI workflow `.github/workflows/template-smoke.yml` (excluded from generated output).
- Template-maintenance tests (`tests/test_runtime_assets.py`, `tests/test_template_smoke.py`, `tests/test_youtube_runtime.py`) are excluded from generated output.
- Postprocessor example contract is in `profiles/_base/postprocessors.example.toml`.
- Local Python example runtime code is in:
  - `src/acme_kg/postprocessors/youtube.py`
  - `src/acme_kg/enrichment/youtube.py`
- Bundled YouTube postprocessor example depends on `lxml` (template `pyproject.toml`).
