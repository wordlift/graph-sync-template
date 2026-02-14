# Graph Build Template (Copier)

Copier template for bootstrapping a `worai graph sync` project.

This repository provides:
- template configuration (`copier.yml`)
- runtime config template (`worai.toml`)
- profile assets (`profiles/*`)
- optional local postprocessor example (`src/acme_kg/postprocessors/youtube.py`)
- GitHub Actions workflow for graph sync (`.github/workflows/graph-sync.yml`)

## Use This Template

```bash
copier copy . ../my-graph-project
```

Or from a remote repository:

```bash
copier copy gh:wordlift/graph-build-template my-graph-project
```

## Required Copier Inputs

- `project_slug`
- `customer_name`
- `api_key`
- `source_type` (`urls`, `sitemap`, `google_sheets`)
- `profiles`
- `default_profile`

`default_profile` must be one of `profiles`.

## Source-Specific Inputs

- `urls`: `urls`
- `sitemap`: `sitemap_url`, optional `sitemap_url_pattern`
- `google_sheets`: `sheets_url`, `sheets_name`, `sheets_service_account`

## Runtime Knobs

- `overwrite`
- `concurrency`
- `web_page_import_mode`
- `web_page_import_timeout`
- `google_search_console`

## Generated Workflow
- `.github/workflows/graph-sync.yml`
- Manual input uses `profile` (or `all`)
- Matrix runs selected `profiles`
## Generation Notes

- Copier generates `.env` with:
  - `WORDLIFT_API_KEY`
  - `SHEETS_SERVICE_ACCOUNT`
  - `YOUTUBE_API_KEY` (empty by default)
- Copier scaffolds `profiles/<profile>/mappings` and `profiles/<profile>/templates` for all selected profiles.

## Docs

- `docs/INDEX.md`
- `docs/QUICKSTART.md`
- `docs/TEMPLATE_SETUP.md`
- `docs/STATE_OF_ART.md`
- `docs/WORAI_TOML_EXAMPLES.md`
- `specs/INDEX.md`
