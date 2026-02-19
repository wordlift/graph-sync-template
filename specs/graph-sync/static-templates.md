# Graph Sync Static Templates

## Templates Directory
- Static template source directory is `templates_dir`.
- Default `templates_dir`: `profiles/<profile_name>/templates`.

## Exports Loading
- Runtime loads profile exports from profile directory in this order:
  1. `exports.toml`
  2. `exports.toml.j2`
  3. `exports.toml.liquid`
- If no exports manifest exists, `exports` is `{}`.

## Static RDF Reification
- Runtime scans files in `templates_dir` and reifies files whose RDF format can be inferred.
- Supported forms include:
  - plain RDF files (for example `.ttl`, `.jsonld`)
  - templated RDF files (for example `.ttl.j2`, `.ttl.liquid`)
- Render/reify context includes:
  - `account`
  - `dataset_uri`
  - `exports`

## Static Template Authoring Rules (Normative)
- Each static template file MUST define exactly one subject node.
- Static templates MUST NOT emit blank nodes.
- Every node MUST use an explicit IRI.
- `schema:url` and `schema:sameAs` in static templates MUST be URL literals (string objects), not IRI objects.
- Example:

```ttl
<{{ exports.website_root_iri }}>
  a schema:WebSite ;
  schema:url "https://www.example.com/" ;
  schema:sameAs "https://www.wikidata.org/wiki/Q1" .
```

## Depth-Prefixed Template Filenames (Normative)
- Static template filenames MUST start with a depth prefix: `10_`, `20_`, `30_`, ...
- Depth is the number of path segments after dataset root in the subject IRI.
- Examples:
  - `<dataset_uri>/organizations/acme` -> depth `2` -> `20_*.ttl.j2`
  - `<dataset_uri>/organizations/acme/postal-addresses/main` -> depth `4` -> `40_*.ttl.j2`

## Static Exports Structure (Normative)
- `exports.toml(.j2|.liquid)` MUST define root canonical IRIs used by static templates.
- `exports.toml(.j2|.liquid)` SHOULD define dependent node IRIs referenced by static templates.
- Exported root IRIs MUST be stable (human-readable, unhashed).

## ID Policy Reference
- Use deterministic ID rules from `specs/graph-sync/static-entity-ids.md`.

## Patch Timing
- Static template graph is patched once per protocol lifecycle, before page mappings.
- First callback triggers static template patching.
- Subsequent callbacks in the same run skip static template patching.

## Debug Output
- In `--debug`, static templates graph is written to:
  - `output/debug_cloud/<profile>/static_templates.ttl`

## Exports vs Mapping Variables
- Use `exports.toml` (or templated exports) for reusable profile-level constants and computed values.
- Use mapping template variables (`account`, `dataset_uri`, `exports`) for mapping-local rendering.
- Prefer `exports` when multiple mappings or postprocessors need the same derived values.
