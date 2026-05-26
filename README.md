# Graph Sync Template

<p align="center">
  <img src="assets/graph-sync-logo.png" alt="Graph Sync Template logo" width="220">
</p>

<p align="center">
  <a href="https://github.com/wordlift/graph-sync-template/actions/workflows/template-smoke.yml"><img src="https://github.com/wordlift/graph-sync-template/actions/workflows/template-smoke.yml/badge.svg" alt="Template Smoke"></a>
  <img src="https://img.shields.io/badge/python-3.12-blue" alt="Python 3.12">
  <img src="https://img.shields.io/badge/copier-9.x-ffb000" alt="Copier 9">
  <img src="https://img.shields.io/badge/package%20manager-uv-5f5cff" alt="uv">
</p>

Copier template for bootstrapping graph-sync projects with the current WordLift SDK v8 cloud-flow contract.

## Agent Skill Kit

Agent-driven graph-sync workflows are handled through [wordlift/graph-sync-agent-kit](https://github.com/wordlift/graph-sync-agent-kit).

Generated projects receive a small `AGENTS.md` pointer to the skill kit and may add project-specific notes there. Install and update commands live in the Graph Sync Agent Kit documentation.

## Why This Template

Use this repository when you need a new graph-sync project with the WordLift runtime contract, GitHub Actions workflow, profile scaffolding, and local examples already aligned.

This template provides:

- generated runtime configuration from `worai.toml.jinja`
- profile scaffolding under `profiles/`
- a generated GitHub Actions workflow from `.github/workflows/graph-sync.yml`
- example local runtime code under `src/acme_kg/`
- template smoke coverage for generated project shape

## Quick Start

Generate from the local checkout:

```bash
pipx run copier copy . ../my-graph-project
```

Generate from GitHub:

```bash
pipx run copier copy gh:wordlift/graph-sync-template my-graph-project
```

For offline or automation-friendly generation, skip API-key validation explicitly:

```bash
pipx run copier copy --data validate_api_key=false gh:wordlift/graph-sync-template my-graph-project
```

If `copier` is already installed, use the same commands without `pipx run`.

See `docs/QUICKSTART.md` for the generated-project quick start.

## Template Contract

The full question contract is defined in `copier.yml`. At a high level, generated projects start from a WordLift API key and one source type: manual URLs, sitemap, or Google Sheets.

Runtime defaults are rendered into generated `worai.toml`. Keep reusable modeling, mapping, validation, and review strategy in the installed graph-sync skills.

## What Generation Does

During `copier copy`, the template:

- validates the WordLift API key against `/accounts/me` by default
- derives the generated project package name from the WordLift account URL, falling back to `datasetUri`
- renames the local runtime module from `acme_kg` to the underscore-safe project package name
- writes secrets to local `.env` instead of tracked config
- sets generated `pyproject.toml` `[project].name` from the derived `graph-sync-*` project package name
- sets generated `pyproject.toml` `[project].description` from the account URL, domain URI, dataset URI, or destination directory
- resets generated `pyproject.toml` `[project].version` to `0.1.0` and adds a comment with the template version used
- scaffolds `profiles/<profile>/mappings`, `templates`, and `postprocessors`
- renders `AGENTS.md.jinja` as the generated project's `AGENTS.md`
- removes `.copier-answers.yml` and excludes `copier.yml` from generated output
- initializes a git repository and creates an `initial commit` when `git` is available

Post-generation work runs through `.copier-tasks/post_copy.py`. Copier renders a temporary `.copier-tasks/context.json` for answers, and the helper removes it immediately after reading it so secrets are not left in generated output.

If validation is skipped or the API is unreachable, package names fall back to the destination directory with a `graph-sync-` prefix.

## Generated Project Scope

Generated projects include the runtime files needed to run graph-sync: runtime configuration, the graph-sync GitHub workflow, profile folders, local runtime code, docs, and a small `AGENTS.md` pointer to the Graph Sync Agent Kit.

Generated projects intentionally exclude template-maintenance assets such as `copier.yml`, `.github/workflows/template-smoke.yml`, `scripts/smoke_render_template.sh`, `tests/`, and `specs/`.

## Runtime Compatibility

Supported runtime settings depend on the `wordlift-sdk` version resolved by the generated project's `pyproject.toml` and `uv.lock`. The pinned `worai` version in the generated GitHub workflow acts as the CLI/action executor for that SDK contract.

For `worai` CLI configuration, profile selection, and command usage, see the official `worai` documentation. Graph-sync runtime settings are interpreted by the resolved `wordlift-sdk` version.

## Source Of Truth

- Copier questions: `copier.yml`
- Copier post-generation behavior: `.copier-tasks/post_copy.py`
- Runtime dependency constraints: `pyproject.toml`
- Resolved dependency versions: `uv.lock`
- Graph-sync workflow executor version: `.github/workflows/graph-sync.yml`
- Generated project agent pointer: `AGENTS.md.jinja`
- Generated project README: `README.md.jinja`
- Reusable agent workflows: [wordlift/graph-sync-agent-kit](https://github.com/wordlift/graph-sync-agent-kit)

## Development

Install dependencies:

```bash
uv sync --dev
```

Run the template-maintenance test suite:

```bash
uv run pytest -q
```

Run the render smoke check:

```bash
uv run scripts/smoke_render_template.sh
```

## Maintainer Macros

- `deploy release [major|minor|patch]`: run `scripts/deploy_release.sh [major|minor|patch]`.
- `upgrade project`: run `scripts/upgrade_project.sh`.

## CI

The template-maintenance workflow lives in `.github/workflows/template-smoke.yml`. It installs dependencies, runs tests, and renders a sample project.

Generated projects receive `.github/workflows/graph-sync.yml`, which exposes profile-based manual dispatch and reusable workflow inputs.
