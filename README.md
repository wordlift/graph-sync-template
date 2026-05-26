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

Agent-driven graph-sync workflows are handled through `wordlift/graph-sync-agent-kit`, not by reusable specs copied into generated projects.

Recommended installs:

```bash
claude plugin marketplace add wordlift/agent-marketplace
claude plugin install graph-sync-agent-kit@wordlift

codex plugin marketplace add wordlift/agent-marketplace --ref main
codex plugin add graph-sync-agent-kit@wordlift
```

Generated projects receive a small `AGENTS.md` pointer to the skill kit and may add project-specific notes there.

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

Required inputs:

- `api_key`
- `source_type` with one of `urls`, `sitemap`, or `google_sheets`

Source-specific inputs:

- `urls`: `urls`
- `sitemap`: `sitemap_url`, optional `sitemap_url_pattern`
- `google_sheets`: `sheets_url`, `sheets_name`, `sheets_service_account`

Runtime defaults are rendered into generated `worai.toml`. Keep reusable modeling, mapping, validation, and review strategy in the installed graph-sync skills.

## What Generation Does

During `copier copy`, the template:

- validates the WordLift API key against `/accounts/me` by default
- derives the runtime package name from the returned `dataset_uri`
- renames the local runtime package from `acme_kg` to `<dataset>_graph_sync`
- writes secrets to local `.env` instead of tracked config
- sets generated `pyproject.toml` `[project].name` from the destination directory name
- scaffolds `profiles/<profile>/mappings`, `templates`, and `postprocessors`
- renders `AGENTS.md.jinja` as the generated project's `AGENTS.md`
- removes `.copier-answers.yml` and excludes `copier.yml` from generated output

If validation is skipped or the API is unreachable, the fallback package name is `acme_graph_sync`.

## Generated Project Shape

Generated projects include:

- `AGENTS.md`
- `README.md`
- `docs/QUICKSTART.md`
- `worai.toml`
- `.github/workflows/graph-sync.yml`
- `.env`
- `profiles/<profile>/mappings`
- `profiles/<profile>/templates`
- `profiles/<profile>/postprocessors`

Generated projects do not include template-maintenance assets such as:

- `copier.yml`
- `.github/workflows/template-smoke.yml`
- `scripts/smoke_render_template.sh`
- `tests/`
- `specs/`

## Runtime Compatibility

Supported runtime settings depend on the `wordlift-sdk` version resolved by the generated project's `pyproject.toml` and `uv.lock`. The pinned `worai` version in the generated GitHub workflow acts as the CLI/action executor for that SDK contract.

For `worai` CLI configuration, profile selection, and command usage, see the official `worai` documentation. Graph-sync runtime settings are interpreted by the resolved `wordlift-sdk` version.

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

- `deploy release [major|minor|patch]` (default: `patch`)
  - `scripts/deploy_release.sh [major|minor|patch]`
  - bumps version, refreshes dependencies and lockfile, requires docs updates, then commits, tags, and pushes

- `upgrade project`
  - `scripts/upgrade_project.sh`
  - updates `wordlift-sdk` to latest, updates `.github/workflows/graph-sync.yml` to latest `worai_version`, then runs `deploy release patch`

## CI

The template-maintenance workflow lives in `.github/workflows/template-smoke.yml`. It installs dependencies, runs tests, and renders a sample project.

Generated projects receive `.github/workflows/graph-sync.yml`, which exposes profile-based manual dispatch and reusable workflow inputs.
