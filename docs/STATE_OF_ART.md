# State of the Art (February 24, 2026)

## Current Capability

- Repository acts as a Copier template for `worai graph sync` projects.
- Template config is defined in `copier.yml`.
- Runtime config is generated from `worai.toml.jinja` with source-type-dependent fields.
- Runtime template is aligned with SDK `6.5.1` canonical cloud workflow contract (`ingest_source`, `ingest_loader`, `ingest_timeout_ms`).
- Workflow is profile-based (`.github/workflows/graph-sync.yml`) and does not use country-specific inputs.
- Graph sync workflow uses `wordlift/graph-sync@v6`.
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
