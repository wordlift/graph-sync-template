# Graph Build Template (Copier)

Copier template for bootstrapping a `worai graph sync` project.

This repository provides:
- template configuration (`copier.yml`)
- runtime config template (`worai.toml.jinja`, rendered as `worai.toml`)
- profile assets (`profiles/*`)
- optional local postprocessor example (`src/acme_kg/postprocessors/youtube.py`)
- GitHub Actions workflow template (`.github/workflows/graph-sync.yml.jinja`, rendered as `.github/workflows/graph-sync.yml`)

## Use This Template

```bash
copier copy . ../my-graph-project
```

Or from a remote repository:

```bash
copier copy gh:wordlift/graph-build-template my-graph-project
```

## Required Copier Inputs

- `api_key`
- `source_type` (`urls`, `sitemap`, `google_sheets`)

## Source-Specific Inputs

- `urls`: `urls`
- `sitemap`: `sitemap_url`, optional `sitemap_url_pattern`
- `google_sheets`: `sheets_url`, `sheets_name`, `sheets_service_account`

## Runtime Knobs (Template Defaults)

- `overwrite`
- `concurrency` (default `4`, hidden prompt)
- `web_page_import_mode` (default `""`, hidden prompt)
- `web_page_import_timeout` (default `120`, hidden prompt)
- `google_search_console` (default `false`, hidden prompt)
- `profiles` (default `["default"]`, hidden prompt)
- `default_profile` (default `"default"`, hidden prompt; must be one of `profiles`)
- `validate_api_key` (default `true`, hidden prompt; checks key via WordLift API during generation)

## Generated Workflow
- `.github/workflows/graph-sync.yml`
- Manual input uses `profile` (or `all`)
- Matrix runs selected `profiles`
## Generation Notes

- Copier generates `.env` with:
  - `WORDLIFT_API_KEY`
  - `SHEETS_SERVICE_ACCOUNT`
  - `YOUTUBE_API_KEY` (empty by default)
- Copier validates `api_key` against `https://api.wordlift.io/accounts/me` by default.
- Copier derives local runtime package name from `dataset_uri` returned by `/accounts/me`: path is normalized and `_graph_sync` is appended.
- Example: `https://data.wordlift.io/wl123/customer-x` -> `wl123_customer_x_graph_sync`.
- If validation is skipped or API is unreachable, fallback package is `acme_graph_sync`.
- To skip validation in automation/offline mode, pass `--data validate_api_key=false`.
- Copier scaffolds `profiles/<profile>/mappings` and `profiles/<profile>/templates` for all selected profiles.

## Docs

- `docs/INDEX.md`
- `docs/QUICKSTART.md`
- `docs/TEMPLATE_SETUP.md`
- `docs/STATE_OF_ART.md`
- `docs/WORAI_TOML_EXAMPLES.md`
- `specs/INDEX.md`

## Verification

- `pytest -q`
- `scripts/smoke_render_template.sh` (renders template and validates `worai.toml`/`.env` output)
