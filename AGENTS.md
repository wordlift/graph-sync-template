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
- Workflow contract is profile-based (no country input), in `.github/workflows/graph-sync.yml`.
- Runtime config template is generated from `worai.toml`.
- Postprocessor example contract is in `profiles/_base/postprocessors.example.toml`.
- Local Python example runtime code is in:
  - `src/acme_kg/postprocessors/youtube.py`
  - `src/acme_kg/enrichment/youtube.py`
