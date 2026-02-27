# Graph Sync Agent Context Index

This folder contains modular agent context for vanilla `worai graph sync` projects.

## Read Order
1. `specs/graph-sync/developer-agent-workflow.md`
2. `specs/graph-sync/agent-working-agreement.md`
3. `specs/graph-sync/overview.md`
4. Open only the focused docs needed for the current task.

## Task-to-File Map
- Agent execution protocol (required):
  - `specs/graph-sync/developer-agent-workflow.md`
- Practical collaboration defaults (DOs/DONTs/code-of-conduct style rules):
  - `specs/graph-sync/agent-working-agreement.md`
- Mapping behavior and `worai.toml` mapping config:
  - `specs/graph-sync/mappings.md`
- Static templates and exports behavior:
  - `specs/graph-sync/static-templates.md`
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
- Tasks are not complete until tests run and docs/specs/todo are synced.
- CLI entrypoints in worai:
  - `worai graph sync run --profile <name> [--debug]`
  - `worai graph sync create <destination> ...`
