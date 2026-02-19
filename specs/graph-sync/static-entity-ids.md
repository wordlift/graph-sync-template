# Static Entity ID Policy

## Scope
- This policy defines deterministic IRI generation for static entities in `profiles/<profile>/templates/*` and `profiles/<profile>/exports.toml(.j2|.liquid)`.

## Normative Rules
- Static entities MUST use dataset-root IRIs: `<dataset_uri>/<container>/<slug>[/*]`.
- Type containers MUST use lowercase-dashed plural names.
- Examples:
  - `WebPage` -> `web-pages`
  - `WebSite` -> `web-sites`
  - `Organization` -> `organizations`
  - `PostalAddress` -> `postal-addresses`
- Slugs MUST be lowercase-dashed and deterministic.
- Static entities MUST NOT use blank nodes.

## Dependent vs Independent Nodes
- Dependent nodes MUST be nested under their parent IRI path.
- Independent nodes MUST be placed under dataset root.
- Examples:
  - Parent organization: `<dataset_uri>/organizations/acme`
  - Dependent postal address: `<dataset_uri>/organizations/acme/postal-addresses/main`
  - Independent website: `<dataset_uri>/web-sites/acme`

## URL Normalization and Hashing
- Runtime canonical ID generation may normalize URL-based identifiers and append hashes where needed to avoid collisions.
- Exception: exported top-level root IRIs in `exports.toml(.j2|.liquid)` MUST remain stable and human-readable.
- Exported root IRIs MUST NOT include URL-hash suffixes.

## GTIN Override
- Product entities keyed by GTIN MUST use `/01/<gtin>` path strategy.
- Example: `<dataset_uri>/products/01/08012345678906`
