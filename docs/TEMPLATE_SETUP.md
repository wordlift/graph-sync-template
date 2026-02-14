# Template Setup (Copier)

## Generate

From local template repository:

```bash
copier copy . ../my-graph-project
```

From remote template repository:

```bash
copier copy gh:wordlift/graph-build-template my-graph-project
```

## Required Answers

- `project_slug`
- `customer_name`
- `api_key`
- `source_type` (`urls`, `sitemap`, `google_sheets`)
- `profiles`
- `default_profile` (must be in `profiles`)

## Source-Specific Answers

- `source_type=urls`: provide `urls`
- `source_type=sitemap`: provide `sitemap_url` and optional `sitemap_url_pattern`
- `source_type=google_sheets`: provide `sheets_url`, `sheets_name`, `sheets_service_account`

## Optional Runtime Answers

- `overwrite`
- `concurrency`
- `web_page_import_mode`
- `web_page_import_timeout`
- `google_search_console`

## What Copier Creates

- Moves `specs/graph-sync/AGENTS.md` to root `AGENTS.md`.
- Generates local `.env` with:
  - `WORDLIFT_API_KEY`
  - `SHEETS_SERVICE_ACCOUNT`
  - `YOUTUBE_API_KEY` (empty by default)
- Ensures each selected profile has:
  - `profiles/<profile>/mappings/`
  - `profiles/<profile>/templates/`
  - `profiles/<profile>/postprocessors/`

## GitHub Secrets

Set in generated repository:

- `WORDLIFT_API_KEY`
- `SHEETS_SERVICE_ACCOUNT` (required only for Google Sheets source type)
