# TODO

## Copier Template Migration

- [x] Rename workflow to `.github/workflows/graph-sync.yml`.
- [x] Replace country-based workflow dispatch with profile-based dispatch.
- [x] Add Copier question contract in `copier.yml`.
- [x] Add source-type conditional inputs (`urls`, `sitemap`, `google_sheets`).
- [x] Template `worai.toml` for source-specific settings.
- [x] Add example postprocessor contract file.
- [x] Keep only YouTube postprocessor example runtime code.
- [x] Configure Copier to replace root `AGENTS.md` with `specs/graph-sync/AGENTS.md`.
- [x] Generate local `.env` from Copier answers for sensitive values.
- [x] Scaffold per-profile `mappings`/`templates`/`postprocessors` directories at generation time.
- [x] Improve YouTube missing-key warning with actionable guidance and non-fatal behavior.
- [x] Align `README.md`, `docs/`, `specs/`, and `AGENTS.md` with template scope.
- [x] Add practical `worai.toml` examples with fake data in docs.
- [x] Ensure secret Copier inputs define defaults for Copier v9 compatibility.
- [x] Enforce non-empty `api_key` input with a Copier validator.
- [x] Ensure runtime/workflow templates are rendered via Copier (`worai.toml.jinja`, `graph-sync.yml.jinja`).
- [x] Fix `.env` generation to use real newline separators.
- [x] Add missing source-specific validators for `urls`, `sitemap_url`, `sheets_url`, and `sheets_name`.
- [x] Add template smoke render validation script and CI workflow.
- [x] Remove unused `project_slug` prompt from Copier contract.
- [x] Remove unused `customer_name` prompt from Copier contract.
- [x] Tune Copier prompts/defaults and hide selected advanced options from interactive prompts.
- [x] Raise `wordlift-sdk` minimum version to `>=3.9.0,<4.0.0`.
- [x] Validate WordLift API key during generation via `/accounts/me` (with network-failure warning fallback).
- [x] Derive runtime package name from `dataset_uri` path (`_graph_sync` suffix) and rename generated `acme_kg` package accordingly.
- [x] Exclude Copier/template-maintenance tests from generated projects to prevent reified-project test failures.
- [x] Enforce static-entity scaffold standards: one-node-per-file, no blank nodes, depth-prefixed filenames, URL literals for `schema:url`/`schema:sameAs`, and stable unhashed exported root IRIs.

## Next Steps

- [ ] Add `worai graph project new` command to render this template directly.
- [ ] Define template versioning/update policy for generated projects.
- [ ] Publish a scripted migration helper for already-generated projects using pre-standard static templates.
