# State of the Art (May 18, 2026)

## Current Capability

- Repository acts as a Copier template for `worai graph sync` projects.
- Template config is defined in `copier.yml`.
- Runtime config is generated from `worai.toml.jinja` with source-type-dependent fields.
- Runtime template is aligned with SDK `8.2.1` canonical cloud workflow contract (`ingest_source`, `ingest_loader`, `ingest_timeout_ms`).
- Default `ingest_loader` is `crawler`; `ingest_timeout_ms` is rendered as a comment (opt-in override); default is 600000 ms (10 min) for `crawler`, 30000 ms (30 s) for all other loaders.
- `crawler` loader supports `crawler_js_render_mode` (disabled | auto | enabled) and `crawler_proxy_mode` (disabled | simple | standard | premium | auto).
- Workflow is profile-based (`.github/workflows/graph-sync.yml`) and does not use country-specific inputs.
- Graph sync workflow uses `wordlift/graph-sync@v6` with `worai_version` pinned to `6.17.19`.
- API key can be validated against WordLift `/accounts/me` during generation.
- Local runtime Python package is derived from `dataset_uri` path and normalized with `_graph_sync` suffix.
- Generated `pyproject.toml` `[project].name` is derived from the Copier destination directory name and normalized to a valid project name.
- Static scaffold follows one-node-per-file templates with explicit IRIs and no blank nodes.
- Static template filenames use depth prefixes (`20_*`, `40_*`, ...).
- Exported root IRIs in `exports.toml.j2` are stable/human-readable and not URL-hashed.

## Runtime Entry Point

- `worai --config worai.toml graph sync --profile <name>`

## Verification Snapshot

- `uv run pytest -q`: passing in template repository.

## Known Gaps

- Template update/versioning and downstream migration strategy are not automated yet.
