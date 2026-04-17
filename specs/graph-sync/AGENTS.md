# Graph Sync AGENTS Template (Dispatcher)

Use this file as the root `AGENTS.md` in vanilla graph-sync template projects.

## Start Here
- Read `specs/graph-sync/INDEX.md` first.
- Then read `specs/graph-sync/developer-agent-workflow.md`.
- Then read `specs/graph-sync/dos-and-donts.md`.
- For role-based reviews, read `specs/graph-sync/roles/INDEX.md`.
- Then open only the section files needed for the task.

## File Routing
- Agent execution protocol:
  - `specs/graph-sync/developer-agent-workflow.md`
- Practical DOs and DONTs for implementation:
  - `specs/graph-sync/dos-and-donts.md`
- Role guides for specialized reviews:
  - `specs/graph-sync/roles/INDEX.md`
- SEO/GEO markup quality review:
  - `specs/graph-sync/roles/seo-geo-expert.md`
- YARRRML/RML and Morph-KGC mapping review:
  - `specs/graph-sync/roles/yarrrml-rml-expert.md`
- Code quality and architecture review:
  - `specs/graph-sync/roles/senior-engineer.md`
- GitHub workflow and integration optimization:
  - `specs/graph-sync/roles/github-advisor.md`
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
- Policy source of truth: `specs/graph-sync/dos-and-donts.md`.
- Prefer `GPT-5.3-Codex-Spark` subagents for parallel, bounded QA/review tasks (mapping checks, TTL spot checks, log triage); keep final semantic modeling decisions in the main agent.
- Keep docs/examples/changelog in sync when behavior contracts change.
- Prefer minimal-context loading by reading only relevant files from the index.

## Maintainer Macros
- `deploy release [major|minor|patch]` (default: `patch`)
  - Script: `scripts/deploy_release.sh [major|minor|patch]`
  - Steps:
    - bump release version
    - refresh dependencies and lockfile (`uv sync --dev`, `uv lock`)
    - update `AGENTS.md`, `README.md`, `specs/`, and `docs/`
    - commit all changes, create tag, push branch and tags

- `upgrade project`
  - Script: `scripts/upgrade_project.sh`
  - Steps:
    - update to latest `wordlift-sdk` in `pyproject.toml` and lockfile
    - update `worai` to the latest version in GH workflow
    - run `deploy release patch` macro
