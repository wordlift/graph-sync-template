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

## Next Steps

- [ ] Add `worai graph project new` command to render this template directly.
- [ ] Define template versioning/update policy for generated projects.
