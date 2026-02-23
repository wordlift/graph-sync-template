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

- `api_key`
- `source_type` (`urls`, `sitemap`, `google_sheets`)

## Source-Specific Answers

- `source_type=urls`: provide `urls`
- `source_type=sitemap`: provide `sitemap_url` and optional `sitemap_url_pattern`
- `source_type=google_sheets`: provide `sheets_url`, `sheets_name`, `sheets_service_account`

## Runtime Defaults (Not Prompted)

- `overwrite=true`
- `concurrency=4`
- `web_page_import_mode=""`
- `web_page_import_timeout=120`
- `google_search_console=false`
- `profiles=["default"]`
- `default_profile="default"` (must be one of `profiles`)
- `validate_api_key=true` (validates key via `https://api.wordlift.io/accounts/me`)

## What Copier Creates

- Renders `worai.toml` from `worai.toml.jinja`.
- Renders `.github/workflows/graph-sync.yml`.
- Moves `specs/graph-sync/AGENTS.md` to root `AGENTS.md`.
- Generates local `.env` with:
  - `WORDLIFT_API_KEY`
  - `SHEETS_SERVICE_ACCOUNT`
  - `YOUTUBE_API_KEY` (empty by default)
- Validates `api_key` against the WordLift API (`/accounts/me`) by default.
- Derives package name from response `dataset_uri` path, normalized and suffixed with `_graph_sync`.
- Example: `https://data.wordlift.io/wl123/customer-x` -> `wl123_customer_x_graph_sync`.
- If validation is skipped (`--data validate_api_key=false`) or API is unreachable, fallback package is `acme_graph_sync`.
- Set `--data validate_api_key=false` to skip this check in offline/CI scenarios.
- Renames local runtime package from `acme_kg` to the derived package name.
- Excludes template-only maintenance tests from generated projects:
  - `tests/test_runtime_assets.py`
  - `tests/test_template_smoke.py`
- Ensures each selected profile has:
  - `profiles/<profile>/mappings/`
  - `profiles/<profile>/templates/`
  - `profiles/<profile>/postprocessors/`

## Static Entity Rules (Generated Scaffold)

- One static template file per subject node.
- No blank nodes in static templates.
- `schema:url` and `schema:sameAs` are URL literals in static templates.
- Depth-prefixed template filenames by IRI depth (`20_*`, `40_*`, ...).
- Deterministic IDs in `exports.toml(.j2)` with lowercase-dashed containers and slugs.
- Exported top-level root IRIs remain stable/unhashed.

Default static templates:
- `profiles/default/templates/20_organization.ttl.j2`
- `profiles/default/templates/20_website.ttl.j2`
- `profiles/default/templates/40_organization_postal_address.ttl.j2`

## Migration Notes

For projects generated before this standard:
- Split any multi-node static file into one node per file.
- Rename each file to depth-prefixed format based on the subject IRI.
- Replace `schema:url` and `schema:sameAs` IRI objects with URL string literals.
- Replace blank nodes with exported explicit dependent IRIs.
- Preserve existing exported root IRIs as stable/human-readable (no URL hash suffix).

## GitHub Secrets

Set in generated repository:

- `WORDLIFT_API_KEY`
- `SHEETS_SERVICE_ACCOUNT` (required only for Google Sheets source type)
