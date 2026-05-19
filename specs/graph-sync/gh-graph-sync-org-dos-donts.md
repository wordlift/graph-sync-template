# Graph-Sync DOs and DONTs Inventory

Generic reusable rules consolidated from graph-sync project experience.

## Scope and Method

- Keep only cross-project rules that are appropriate for this template.
- Exclude account names, account domains, project repository names, sample URLs, run IDs, and implementation reports.
- Treat `specs/graph-sync/dos-and-donts.md` as the canonical policy source for active template guidance.

## Reusable DO List

- Always assign an explicit IRI to entities.
- Always emit URL-valued schema properties as full absolute URLs when source data contains relative paths.
- Always ensure each page has exactly one main page-like entity IRI and that entity includes `schema:url`.
- Always scout for question/answer pairs to create `FAQPage` markup connected to the main entity, unless `FAQPage` is the main entity itself.
- Always try to add authorship markup on creative works (`Article`, blog posts, and related content) with an E-E-A-T mindset.
- Always write URL-valued schema properties as plain literals, not IRIs or `xsd:anyURI` values.
- For FAQ modeling, when `FAQPage` is not the page main entity, link it with `schema:about` from FAQ to main entity and `schema:subjectOf` from main entity to FAQ.
- For geographic entities, always try to provide `schema:sameAs` links to Wikidata, GeoNames, and DBpedia.
- Ground all implementation decisions in observed repository behavior and source evidence; do not invent assumptions.
- In YARRRML files, use relative XPath selectors.
- Keep docs and indexes in sync with runtime scope changes.
- Look for ratings and connect them to `Organization` or emit output markup where supported.
- Prefer minimal-context loading by reading only relevant files from the index.
- Start with static entities for `WebSite`, `Organization`, and other vertical entities; then prefer YARRRML mappings; use postprocessors only after that.
- When linking content already modeled in other clusters, prefer lightweight link structures, such as collection items with URL literals, instead of re-creating full page entities.
- When possible, add collection page markup with list items that link to related URLs.
- When social sharing links are present, add `schema:potentialAction` using `ShareAction` and connect it to the page entity.

## Reusable DONT List

- Do not allow empty `schema:url` on the main entity.
- Do not assign `schema:url` to `FAQPage` entities that are not the web page main entity.
- Do not change mapping or postprocessor semantics without explicit approval.
- Do not create duplicate mappings.
- Do not create duplicate `WebPage` entities in collection or related-link sections when those pages are already defined elsewhere; link them by URL literals in item nodes.
- Do not create multiple entities for the same canonical URL within a profile; one URL must map to one primary entity.
- Do not delegate final semantic modeling or integration decisions to subagents; keep those in the main agent.
- Do not derive page-level `schema:url` from canonical tags or OG meta tags when a runtime URL value is available.
- Do not emit image URLs as IRIs; keep URL-valued image properties as plain literals.
- Do not hardcode the dataset URI; use provided placeholders or runtime context.
- Do not ingest image or static asset URLs as source pages.
- Do not mark work complete without running tests.
- Do not publish `Question` or `Answer` nodes when content is empty or equals `None`.
- Do not relate entities to the web page canonical URL.
- Do not type URL-valued schema properties as `xsd:anyURI`; keep them as plain literals.
- Do not use `WebPage` markup when a more specific entity type is available.
- Do not use blank nodes.
- Do not use JSON-LD or any other structured data markup as a data source for extraction.
- Do not write schema URL properties as IRIs; use plain literals.
- In YARRRML files, do not use absolute XPath selectors.
- Treat `worai.toml` as the authoritative runtime configuration; do not treat ad-hoc local config files as project defaults.
