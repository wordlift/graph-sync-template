# Graph Sync DOs and DONTs

Merged reusable guidance gathered from WordLift GitHub repositories tagged
`graph-sync`. Keep project-specific exceptions in generated project `AGENTS.md`
files or in the Graph Sync Agent Kit.

## DOs

- Assign explicit, stable, deterministic IRIs to all entities.
- Start with static entities for `WebSite`, `Organization`, and core vertical entities; then prefer YARRRML mappings; use postprocessors only when mappings cannot express the behavior cleanly.
- Ground implementation decisions in repository evidence and observed source behavior.
- Use `http://schema.org` as the default vocabulary unless a project explicitly requires `https://schema.org`.
- Use relative XPath selectors in YARRRML.
- Use the runtime current-page URL value, such as `__URL__` in mappings, for page-level `schema:url`.
- Ensure each page has exactly one clear main page-like entity IRI and that entity includes `schema:url`.
- Prefer the most specific grounded Schema.org type for each page or entity, such as `Article`, `NewsArticle`, `AboutPage`, `ProfilePage`, `CollectionPage`, `SearchResultsPage`, `FAQPage`, `Service`, `Organization`, `ContactPoint`, `ItemList`, `Place`, `Event`, or `DigitalDocument`.
- Use specific `WebPage` subtypes when they are the best grounded semantic fit; discourage generic `WebPage`.
- Connect child entities through explicit hierarchy such as `mainEntity`, `itemListElement`, `hasPart`, `about` / `subjectOf`, or another grounded Schema.org relationship.
- Use static rooted identity entities as the source of truth for organizations and businesses; page-level mappings and postprocessors should link to them instead of re-emitting partial duplicate nodes.
- For geographic entities, try to provide `schema:sameAs` links to Wikidata, GeoNames, and DBpedia.
- Scout for question/answer pairs and create `FAQPage` markup connected to the main entity, unless `FAQPage` is the main entity itself.
- When `FAQPage` is not the page main entity, link it with `schema:about` from FAQ to main entity and `schema:subjectOf` from main entity to FAQ.
- Look for ratings and connect them to `Organization` or supported output markup.
- Add authorship markup on creative works where source evidence supports it.
- Write URL-valued schema properties as absolute plain literals, not IRIs and not `xsd:anyURI`, including `schema:url`, `schema:contentUrl`, and similar URL fields.
- Emit numeric properties such as `schema:position` as plain numeric literals from source values when possible.
- Add `schema:potentialAction` with `ShareAction` when social sharing links are present.
- Prefer lightweight link structures for related content already modeled elsewhere, instead of recreating full page entities.
- Add collection/list markup when pages expose related URLs or item lists.
- Keep `ItemList` entities inside the hierarchy of the owning page or entity.
- Inspect XHR/network traffic before finalizing extraction; if a stable upstream structured source exists, prefer it over fragile HTML parsing.
- Treat `worai.toml` as the authoritative runtime configuration.
- Store graph exports, production graph snapshots, validation/audit artifacts, KPI reports, and other local investigation artifacts under `.private/`.
- Keep docs, indexes, examples, changelogs, and TODOs in sync when behavior contracts change.
- Validate structured data changes before graph sync runs.
- Run relevant tests or validation before considering work complete.
- Follow an OOP and KISS approach for code changes.

## DONTs

- Do not use blank nodes.
- Do not create duplicate mappings.
- Do not create multiple primary entities for the same canonical URL within a profile.
- Do not hardcode dataset URIs; use placeholders or runtime context.
- Do not point `schema:url` to a dataset URI.
- Do not write schema URL properties as IRIs.
- Do not type URL-valued schema properties as `xsd:anyURI`.
- Do not emit image URLs as IRIs; keep URL-valued image properties as literals.
- Do not emit relative IRIs or relative URL literals where absolute IRIs or URLs are required.
- Do not ingest image or static asset URLs as source pages, including uploads, images, PDFs, and similar assets.
- Do not create duplicate `WebPage` entities for collection or related-link sections; link related pages by URL literals.
- Do not assign `schema:url` to `FAQPage` entities that are not the page main entity.
- Do not attach `Question` nodes directly to `WebPage`; model `FAQPage` + `Question` + `Answer`.
- Do not publish `Question` or `Answer` nodes when content is empty or equals `None`.
- Do not derive page-level `schema:url` from canonical tags or Open Graph meta tags when a runtime URL value is available.
- Do not relate entities directly to the web page canonical URL as a substitute for proper entity relationships.
- Do not use generic `WebPage` markup when a more specific grounded type is available.
- Do not use `CreativeWork` when a more specific grounded Schema.org type applies.
- Do not invent Schema.org types or properties.
- Do not model schema.org enum values as IRI objects.
- Do not use absolute XPath selectors in YARRRML.
- Do not use JSON-LD or other existing structured data markup as the extraction source; use it only as semantic/type evidence.
- Do not hardcode constants from sample pages used during development.
- Do not add hard-coded fallbacks unless explicitly authorized.
- Do not introduce unverified values for policy, pricing, availability, shipping, return, tax, or corporate identifier data.
- Do not widen mapping scope with catch-all rules when a cluster-specific rule is possible.
- Do not process pages already fully defined by static templates; route them to a null mapping that emits no graph.
- Do not change mapping or postprocessor semantics without explicit approval.
- Do not implement custom IRI canonicalization in project mappings or postprocessors when `worai` / `wordlift-sdk` owns canonicalization.
- Do not treat ad-hoc local config files as project defaults.
- Do not run bulk graph property deletes or account-level resets without explicit user approval and scoped confirmation.
- Do not delegate final semantic modeling or integration decisions to subagents.
- Do not ship mapping or postprocessor changes without validation evidence.
- Do not mark work complete without tests or equivalent validation.
