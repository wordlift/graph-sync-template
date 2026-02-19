#!/usr/bin/env bash
set -euo pipefail

tmpbase="$(mktemp -d)"
src="$tmpbase/template"
out="$tmpbase/out"

cleanup() {
  rm -rf "$tmpbase"
}
trap cleanup EXIT

rsync -a \
  --exclude '.git' \
  --exclude '.venv' \
  --exclude '.pytest_cache' \
  --exclude '.ruff_cache' \
  --exclude '.idea' \
  --exclude '__pycache__' \
  ./ "$src"/

(
  cd "$src"
  git init -q
  git config user.email "template-smoke@example.com"
  git config user.name "Template Smoke"
  git add .
  git -c commit.gpgsign=false commit -qm "template snapshot"
)

(
  cd "$src"
  copier copy . "$out" --trust --defaults \
    --data api_key='abc123' \
    --data validate_api_key=false \
    --data source_type='sitemap' \
    --data sitemap_url='https://example.com/sitemap.xml' \
    --data sitemap_url_pattern='' \
    --data profiles='["default","eu"]' \
    --data default_profile='default'
)

test -f "$out/worai.toml"
test -f "$out/.github/workflows/graph-sync.yml"
test -f "$out/.env"
test -d "$out/src/acme_graph_sync"
test ! -d "$out/src/acme_kg"
test ! -f "$out/.github/workflows/template-smoke.yml"
test ! -d "$out/.git"

if rg -n '\{\{|\{%' "$out/worai.toml" >/dev/null; then
  echo "Unrendered template syntax found in generated worai.toml"
  exit 1
fi

rg -n 'sitemap_url = "https://example.com/sitemap.xml"' "$out/worai.toml" >/dev/null
rg -n 'api_key = "\$\{WORDLIFT_API_KEY\}"' "$out/worai.toml" >/dev/null
rg -n 'default: "default"' "$out/.github/workflows/graph-sync.yml" >/dev/null
test ! -f "$out/tests/test_runtime_assets.py"
test ! -f "$out/tests/test_template_smoke.py"
rg -n 'class = "acme_graph_sync\.postprocessors\.youtube:YouTubePostprocessor"' "$out/profiles/_base/postprocessors.example.toml" >/dev/null

if rg -n '\\n' "$out/.env" >/dev/null; then
  echo "Generated .env contains literal \\\\n sequences"
  exit 1
fi

env_lines="$(wc -l < "$out/.env" | tr -d '[:space:]')"
if [ "$env_lines" -ne 3 ]; then
  echo "Generated .env has unexpected line count: $env_lines"
  exit 1
fi

echo "Template smoke render passed."
