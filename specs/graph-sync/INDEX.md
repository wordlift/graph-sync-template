# Graph Sync Agent Context Index

This folder contains modular agent context for vanilla `worai graph sync` projects.

## Read Order
1. `specs/graph-sync/overview.md`
2. Open only the focused docs needed for the current task.

## Task-to-File Map
- Mapping behavior and `worai.toml` mapping config:
  - `specs/graph-sync/mappings.md`
- Static templates and exports behavior:
  - `specs/graph-sync/static-templates.md`
- Deterministic static entity IDs and path conventions:
  - `specs/graph-sync/static-entity-ids.md`
- Postprocessor runtime loading/execution:
  - `specs/graph-sync/postprocessors.md`
- Building custom postprocessors:
  - `specs/graph-sync/postprocessors-authoring.md`
- Common failures and fixes:
  - `specs/graph-sync/troubleshooting.md`
- CI smoke checks:
  - `specs/graph-sync/ci-checklist.md`

## Scope
- This index is for agent context in template projects.
- Runtime behavior must match current SDK implementation.
