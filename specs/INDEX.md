# Specs Index

Technical specifications for implementation and maintenance.

## Available Specs

- Template contract is defined by `copier.yml`.
- Template generation tasks include API key validation, runtime package rename, and destination-derived `pyproject.toml` project naming.
- Workflow contract template is defined in `.github/workflows/graph-sync.yml`.
- Runtime import contract template is defined in `worai.toml.jinja` (rendered output: `worai.toml`).
- Graph sync runtime behavior docs are under `specs/graph-sync/`:
  - `specs/graph-sync/INDEX.md`
  - `specs/graph-sync/agent-working-agreement.md`
  - `specs/graph-sync/implementation-playbook.md`
  - `specs/graph-sync/static-entity-ids.md`

## Scope

`specs/` is for internal implementation details.
For user-facing setup and usage, see:

- `README.md`
- `docs/QUICKSTART.md`
- `docs/TEMPLATE_SETUP.md`
- `docs/INDEX.md`
