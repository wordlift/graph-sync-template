# WordLift Graph-Sync Org DOs and DONTs Inventory

Snapshot date: 2026-04-11

## Scope and Method

- Inventory target: all GitHub repositories in `wordlift` with topic `graph-sync`.
- Discovery command: `gh api '/search/repositories?q=org:wordlift+topic:graph-sync&per_page=100'`.
- Rule extraction source priority per repo:
- `specs/graph-sync/dos-and-donts.md` (if present)
- otherwise `AGENTS.md` (`## Agent Guardrails`)

## Inventory (15 Repositories)

| Repository | Rule Source | Notes |
| --- | --- | --- |
| `wordlift/graph-sync-avalara-com` | `specs/graph-sync/dos-and-donts.md` | Includes explicit absolute-URL requirement. |
| `wordlift/graph-sync-homezonefurniture-com` | `AGENTS.md` guardrails | No project DO/DONT spec file. |
| `wordlift/graph-sync-r5living-com` | `specs/graph-sync/dos-and-donts.md` | Core DO/DONT profile. |
| `wordlift/graph-sync-zurich-at` | `specs/graph-sync/dos-and-donts.md` | FAQ/main-entity URL constraints. |
| `wordlift/graph-sync-bennettlegal-com` | `AGENTS.md` guardrails | No project DO/DONT spec file. |
| `wordlift/graph-sync-smallpdf-com` | `AGENTS.md` guardrails | Runtime migration/attic constraints. |
| `wordlift/graph-sync-weebora-com` | `specs/graph-sync/dos-and-donts.md` | `__URL__`-driven page URL constraint. |
| `wordlift/graph-sync-freedomdebtrelief-com` | `AGENTS.md` guardrails | LocalBusiness/state-service constraints. |
| `wordlift/graph-sync-zurich-ch` | `specs/graph-sync/dos-and-donts.md` | Canonical URL uniqueness constraint. |
| `wordlift/graph-sync-busesforsale-com` | `specs/graph-sync/dos-and-donts.md` | Core DO/DONT profile. |
| `wordlift/graph-sync-lendingtree-com` | `AGENTS.md` guardrails | FAQ postprocessor + article IRI contract. |
| `wordlift/graph-sync-zycus-com` | `specs/graph-sync/dos-and-donts.md` | Core DO/DONT profile. |
| `wordlift/graph-sync-cloudkitchens-com` | `AGENTS.md` guardrails | No project DO/DONT spec file. |
| `wordlift/graph-sync-zurich-us` | `specs/graph-sync/dos-and-donts.md` | Core DO/DONT profile. |
| `wordlift/graph-sync-closesimple-com` | `specs/graph-sync/dos-and-donts.md` | FAQ content non-empty constraint. |

## Per-Project DOs and DONTs

- `wordlift/graph-sync-avalara-com`
- DO: URL-valued schema fields must be absolute full URLs.
- DONT: follow core DONT profile (no blank nodes, no absolute XPath, no dataset hardcoding, no JSON-LD extraction source).
- `wordlift/graph-sync-homezonefurniture-com`
- DO: keep docs/examples/changelog synced on contract changes; keep context loading minimal.
- DONT: do not change mapping/postprocessor semantics without explicit approval; do not complete without tests.
- `wordlift/graph-sync-r5living-com`
- DO: core profile (explicit IRIs, static-entities-first, relative XPath, FAQ/rating/authorship/social/link-graph coverage).
- DONT: core profile (no blank nodes/duplicates/absolute XPath/JSON-LD extraction/canonical URL relations).
- `wordlift/graph-sync-zurich-at`
- DO: one main page-like entity per page with canonical `schema:url`; FAQ linkage via `about`/`subjectOf`.
- DONT: no `schema:url` on non-main `FAQPage`.
- `wordlift/graph-sync-bennettlegal-com`
- DO: keep docs/examples/changelog synced on contract changes; keep context loading minimal.
- DONT: do not change mapping/postprocessor semantics without explicit approval; do not complete without tests.
- `wordlift/graph-sync-smallpdf-com`
- DO: use active postprocessor runtime (`profiles/_base/postprocessors.toml`); keep canonical ID normalization via `EntityIdCanonicalizerPostprocessor`.
- DONT: do not use archived `.attic/` extraction/enrichment runtime as active flow.
- `wordlift/graph-sync-weebora-com`
- DO: use `__URL__` for page-level `schema:url`.
- DONT: do not derive page URL from canonical/OG tags; do not allow empty main-entity `schema:url`.
- `wordlift/graph-sync-freedomdebtrelief-com`
- DO: keep `worai.toml` as authoritative runtime config.
- DONT: do not switch `state_service` provider from `LocalBusiness` to `Organization`; do not add `schema:Organization` type to that `LocalBusiness`.
- `wordlift/graph-sync-zurich-ch`
- DO: core profile.
- DONT: one canonical URL maps to one primary entity (no duplicates by canonical URL).
- `wordlift/graph-sync-busesforsale-com`
- DO: core profile.
- DONT: core profile.
- `wordlift/graph-sync-lendingtree-com`
- DO: read postprocessor settings/auth from `context.profile["settings"]` and `context.account_key`; keep article IRI contract `.../articles/<slug>-<sha256(url)>`; enforce FAQ postprocessor contract.
- DONT: do not attach `Question` directly to `WebPage`; do not emit `FAQPage.url`.
- `wordlift/graph-sync-zycus-com`
- DO: core profile.
- DONT: core profile.
- `wordlift/graph-sync-cloudkitchens-com`
- DO: keep docs/examples/changelog synced on contract changes; keep context loading minimal.
- DONT: do not change mapping/postprocessor semantics without explicit approval; do not complete without tests.
- `wordlift/graph-sync-zurich-us`
- DO: core profile.
- DONT: core profile.
- `wordlift/graph-sync-closesimple-com`
- DO: core profile.
- DONT: do not emit `Question`/`Answer` nodes when content is empty or `None`.

## Merged Unique DO List (Across All 15 Repositories)

- Active postprocessor runtime is configured via `profiles/_base/postprocessors.toml`.
- Always assign an explicit IRI to entities.
- Always emit URL-valued schema properties as full absolute URLs (including protocol and host), not relative paths.
- Always ensure each page has exactly one main page-like entity IRI and that entity includes `schema:url` with the page canonical URL.
- Always scout for FAQs on web pages to create rich, connected `FAQPage` markup.
- Always scout for question/answer pairs to create `FAQPage` markup connected to the main entity, unless `FAQPage` is the main entity itself.
- Always try to add authorship markup on creative works (`Article`, blog posts, and related content) with an E-E-A-T mindset.
- Always use the provided `__URL__` value for page-level `schema:url` (main entity URL), never inferred canonical/meta URL fields.
- Always write URL-valued schema properties as plain literals (not IRIs and not `xsd:anyURI`), including `schema:url`, `schema:contentUrl`, and similar URL fields.
- Canonical Article/Product ID normalization is enforced by `EntityIdCanonicalizerPostprocessor` before downstream enrichers.
- FAQ extraction currently runs in postprocessing (`FAQExtractionPostprocessor`) due mapper XPath compatibility constraints.
- Follow an OOP and KISS approach.
- For `wordlift-sdk>=5.1.1`, postprocessors should read settings from `context.profile["settings"]` and auth from `context.account_key` (legacy `context.settings` / `context.account.key` may exist only for backward compatibility).
- For FAQ modeling, when `FAQPage` is not the page main entity, link it with `schema:about` (FAQ -> main entity) and inverse `schema:subjectOf` (main entity -> FAQ).
- For geographic entities, always try to provide `schema:sameAs` links to Wikidata, GeoNames, and DBpedia.
- For parallel, bounded QA/review delegations, prefer subagents on `GPT-5.3-Codex-Spark`.
- Ground all implementation decisions in observed repository behavior and source evidence; do not invent assumptions.
- In YARRRML files, use relative XPath selectors.
- Keep `Article` IRI generation consistent across review fallback and default article flows: `.../articles/<slug>-<sha256(url)>` (no `-article-` suffix), so one URL maps to one canonical `Article` node.
- Keep docs and indexes in sync with runtime scope changes.
- Keep docs/examples/changelog in sync when behavior contracts change.
- Look for ratings and connect them to `Organization` or emit output markup where supported.
- Prefer minimal-context loading by reading only relevant files from the index.
- Review fallback behavior can be enforced with `review_requires_editorial_rating=true` (default is legacy behavior deriving reviewRating from rating URL when editorial rating is missing).
- Start with static entities for `WebSite`, `Organization`, and other vertical entities; then prefer YARRRML mappings; use postprocessors only after that.
- When linking content already modeled in other clusters, prefer lightweight link structures (for example collection items with URL literals) instead of re-creating full page entities.
- When possible, add collection page markup with list items that link to related URLs.
- When social sharing links are present, add `schema:potentialAction` using `ShareAction` and connect it to the page entity.

## Merged Unique DONT List (Across All 15 Repositories)

- Do not add `schema:Organization` type to the `LocalBusiness` entity.
- Do not allow empty `schema:url` on the main entity.
- Do not assign `schema:url` to `FAQPage` entities that are not the web page main entity.
- Do not change mapping/postprocessor semantics without explicit approval.
- Do not create duplicate `WebPage` entities in collection/related-link sections when those pages are already defined elsewhere; link them by URL literals in item nodes.
- Do not create duplicate mappings.
- Do not create multiple entities for the same canonical URL within a profile; one URL must map to one primary entity.
- Do not delegate final semantic modeling or integration decisions to subagents; keep those in the main agent.
- Do not derive page-level `schema:url` from canonical tags or OG meta tags; use `__URL__`.
- Do not emit image URLs as IRIs (for example `schema:image` / `schema:contentUrl` when URL-valued); keep them as plain literals.
- DO NOT hardcode the dataset URI; use provided placeholders or runtime context.
- Do not ingest image or static asset URLs as source pages (for example `/wp-content/uploads/*`, `.webp`, `.png`, `.jpg`, `.pdf`) even if they appear in sitemaps.
- Do not mark work complete without running tests.
- Do not publish `Question` or `Answer` nodes when content is empty or equals `None`.
- Do not relate entities to the web page canonical URL.
- Do not type URL-valued schema properties as `xsd:anyURI`; keep them as plain literals.
- Do not use `WebPage` markup when a more specific entity type is available.
- Do not use blank nodes.
- Do not use JSON-LD or any other structured data markup as a data source for extraction, because it may be removed in the future.
- Do not write schema URL properties as IRIs; use plain literals.
- FAQ graph model contract: emit `FAQPage` + `Question` + `Answer`; never attach `Question` directly to `WebPage`; link FAQ pages to main entities via `about` / `subjectOf`; do not emit `FAQPage.url`.
- In YARRRML files, do not use absolute XPath selectors.
- Keep `state_service` provider linked to `LocalBusiness`; do not switch it to `Organization`.
- Legacy extraction/enrichment runtime is archived under `.attic/` and is not active.
- Treat `worai.toml` as the authoritative runtime configuration; do not treat ad-hoc `/tmp/*.toml` files as project defaults.
- You may still use JSON-LD/structured data only to infer the best semantic type when creating configurations.
