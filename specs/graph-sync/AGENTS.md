# Graph Sync AGENTS Template (Dispatcher)

Use this file as the root `AGENTS.md` in vanilla graph-sync template projects.

## Start Here
- Read `specs/graph-sync/INDEX.md` first.
- Then read `specs/graph-sync/developer-agent-workflow.md`.
- Then read `specs/graph-sync/dos-and-donts.md`.
- For role-based reviews, read `specs/roles/INDEX.md`.
- Then open only the section files needed for the task.

## File Routing
- Agent execution protocol:
  - `specs/graph-sync/developer-agent-workflow.md`
- Practical DOs and DONTs for implementation:
  - `specs/graph-sync/dos-and-donts.md`
- Role guides for specialized reviews:
  - `specs/roles/INDEX.md`
- SEO/GEO markup quality review:
  - `specs/roles/seo-geo-expert.md`
- YARRRML/RML and Morph-KGC mapping review:
  - `specs/roles/yarrrml-rml-expert.md`
- Code quality and architecture review:
  - `specs/roles/senior-engineer.md`
- GitHub workflow and integration optimization:
  - `specs/roles/github-advisor.md`
- Core workflow and high-level contract:
  - `specs/graph-sync/overview.md`
- Mapping behavior and config:
  - `specs/graph-sync/mappings.md`
- Static templates and exports behavior:
  - `specs/graph-sync/static-templates.md`
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
- Do not violate rules in `specs/graph-sync/dos-and-donts.md`.
- Prefer `GPT-5.3-Codex-Spark` subagents for parallel, bounded QA/review tasks (mapping checks, TTL spot checks, log triage); keep final semantic modeling decisions in the main agent.
- Keep docs/examples/changelog in sync when behavior contracts change.
- Prefer minimal-context loading by reading only relevant files from the index.
- Do not mark work complete without running tests.
