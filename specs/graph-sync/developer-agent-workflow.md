# Graph Sync Developer Agent Workflow

## Purpose
- Provide a strict execution protocol for coding agents working on graph-sync template projects.
- Ensure behavior, docs, and validation stay aligned after every change.

## Required First Actions
1. Read `specs/graph-sync/INDEX.md`.
2. Read `specs/graph-sync/overview.md`.
3. Classify the task before editing any file.

## Task Classification
- Mapping selection/config behavior:
  - Read `specs/graph-sync/mappings.md`.
- Static template/export behavior:
  - Read `specs/graph-sync/static-templates.md`.
- Postprocessor loading/runtime behavior:
  - Read `specs/graph-sync/postprocessors.md`.
- Authoring or changing custom postprocessors:
  - Read `specs/graph-sync/postprocessors-authoring.md`.
- Runtime failures and regressions:
  - Read `specs/graph-sync/troubleshooting.md`.
- CI/smoke contract changes:
  - Read `specs/graph-sync/ci-checklist.md`.

## Change Protocol
1. Confirm current behavior from relevant spec files.
2. Propose minimal change set and expected impact.
3. Edit code and tests together; do not leave behavior changes untested.
4. Update all impacted docs/specs in the same change:
   - template-level context files under `specs/graph-sync/`
   - repo-level contract docs (`specs/graph_sync.md`, `README.md`) when user-visible or contract behavior changed
5. Update task tracking in `TODO.md`.

## Verification Protocol
- Always run tests before considering the task complete.
- Default command:
  - `uv run pytest`
- If failures appear unrelated, report them explicitly and separate them from your change impact.
- For graph-sync-specific updates, verify at least these behaviors through tests:
  - mapping route resolution and fallback
  - static template one-time patching per run
  - postprocessor load order and execution
  - CLI contract for `graph sync run` and `graph sync create`

## Guardrails
- Do not change runtime semantics without explicit approval.
- Do not update only one layer of documentation when contract behavior changed.
- Prefer focused context loading; avoid scanning unrelated specs.
- When uncertain, stop and ask for clarification instead of inferring behavior changes.

## Handoff Checklist
- Code updated.
- Tests added/updated.
- `uv run pytest` executed.
- `specs/`, `README.md`, and `TODO.md` synced as needed.
- Summary includes what changed, why, and any residual risks.
