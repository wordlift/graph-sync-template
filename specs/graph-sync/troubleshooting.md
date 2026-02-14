# Graph Sync Troubleshooting

## Mapping Routes Do Not Match
- Symptom:
  - URL-specific mapping is never selected.
- Check:
  - patterns match URL path, not full URL.
  - route order is correct (first match wins).

## Unexpected Fallback Mapping
- Symptom:
  - unmatched URLs still resolve to a mapping.
- Cause:
  - runtime ensures fallback `.* -> mapping`.
- Check:
  - intended fallback `mapping` file and location.

## Mapping File Not Found
- Symptom:
  - mapping read/render failure.
- Check:
  - relative paths are resolved under `mappings_dir`.
  - absolute path usage is intentional and valid.

## Template Variable Errors
- Symptom:
  - `.j2` or `.liquid` rendering fails.
- Check:
  - required context keys exist (`dataset_uri`, `account`, `exports`).
  - template references valid variable names.

## Postprocessor Class Import Failure
- Symptom:
  - subprocess exits with import/class error.
- Check:
  - `class` uses `package.module:ClassName`.
  - `python` points to env where your package is installed/importable.

## Postprocessor Timeout
- Symptom:
  - callback fails after timeout.
- Check:
  - increase `timeout_seconds` in manifest.
  - optimize expensive graph operations.

## Missing Postprocessor Output Graph
- Symptom:
  - runtime reports no output graph produced.
- Check:
  - processor does not crash.
  - runner writes output and processor returns `Graph` or `None`.

## Debug Artifacts
- Static template debug:
  - `output/debug_cloud/<profile>/static_templates.ttl`
- Per-page callback debug:
  - `output/debug_cloud/<profile>/cloud_<sha256(url)>.ttl`
- Postprocessor temp artifacts on failure:
  - `output/postprocessor_debug/<class_path_sanitized>/`
