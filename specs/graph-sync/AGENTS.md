# Graph Sync AGENTS Template (Dispatcher)

Use this file as the root `AGENTS.md` in vanilla graph-sync template projects.

## Start Here
- Read `specs/graph-sync/INDEX.md` first.
- Then open only the section files needed for the task.

## File Routing
- Core workflow and high-level contract:
  - `specs/graph-sync/overview.md`
- Mapping behavior and config:
  - `specs/graph-sync/mappings.md`
- Static templates and exports behavior:
  - `specs/graph-sync/static-templates.md`
- Static entity ID conventions:
  - `specs/graph-sync/static-entity-ids.md`
- Postprocessor runtime loading/execution:
  - `specs/graph-sync/postprocessors.md`
- Writing custom postprocessors:
  - `specs/graph-sync/postprocessors-authoring.md`
- Failure diagnosis:
  - `specs/graph-sync/troubleshooting.md`
- CI smoke expectations:
  - `specs/graph-sync/ci-checklist.md`

## Agent Guardrails
- Do not change mapping/postprocessor semantics without explicit approval.
- Keep docs/examples/changelog in sync when behavior contracts change.
- Prefer minimal-context loading by reading only relevant files from the index.
