# Graph Sync Mappings

## Mapping Configuration Contract
- Fallback mapping key:
  - `mapping` (default: `default.yarrrml`)
- Mapping base directory:
  - `mappings_dir` (default: `profiles/<profile_name>/mappings`)
- Route table:
  - `[[profiles.<name>.mappings]]`
  - required keys per route: `pattern`, `mapping`

## Mapping Selection Rules
- Callback mapping selection is profile-driven using `ProfileDefinition.resolve_mapping(url)`.
- Route matching target is URL path only (`urlparse(url).path`), not full URL/query/fragment.
- Route scan is ordered; first match wins.
- In YARRRML XPath selectors, use relative XPath expressions only; do not use absolute XPath paths.
- Mapping logic must not hardcode constants from sample pages used during development; patterns and transforms must generalize to other pages in the same source.
- Do not introduce hard-coded fallback values or fallback branches unless explicitly authorized by the user.
- Fallback behavior:
  - if no routes are defined, runtime behaves as implicit `pattern = ".*"` with `mapping`
  - if routes exist without `pattern = ".*"`, runtime appends that fallback

## Mapping Path And Template Resolution
- Selected mapping path:
  - absolute paths are used as-is
  - relative paths resolve under `mappings_dir`
- Template variant resolution order:
  1. existing `.j2`/`.liquid` path as selected
  2. sibling `<file>.j2`
  3. sibling `<file>.liquid`
  4. plain file
