# State of the Art (February 13, 2026)

## Current Capability

- Repository acts as a Copier template for `worai graph sync` projects.
- Template config is defined in `copier.yml`.
- Runtime config is generated from `worai.toml.jinja` with source-type-dependent fields.
- Workflow is profile-based (`.github/workflows/graph-sync.yml.jinja`) and does not use country-specific inputs.
- API key can be validated against WordLift `/accounts/me` during generation.
- Local runtime Python package is derived from `dataset_uri` path and normalized with `_graph_sync` suffix.

## Runtime Entry Point

- `worai --config worai.toml graph sync --profile <name>`

## Verification Snapshot

- `uv run pytest -q`: passing in template repository.

## Known Gaps

- Template update/versioning and downstream migration strategy are not automated yet.
