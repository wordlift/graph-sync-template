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

search() {
  local pattern="$1"
  local file="$2"
  if command -v rg >/dev/null 2>&1; then
    rg -n "$pattern" "$file" >/dev/null
  else
    grep -nE "$pattern" "$file" >/dev/null
  fi
}

if search '\{\{|\{%' "$out/worai.toml"; then
  echo "Unrendered template syntax found in generated worai.toml"
  exit 1
fi

search 'sitemap_url = "https://example.com/sitemap.xml"' "$out/worai.toml"
search 'api_key = "\$\{WORDLIFT_API_KEY\}"' "$out/worai.toml"
test ! -f "$out/tests/test_runtime_assets.py"
test ! -f "$out/tests/test_template_smoke.py"
search 'class = "acme_graph_sync\.postprocessors\.youtube:YouTubePostprocessor"' "$out/profiles/_base/postprocessors.example.toml"

if search '\\n' "$out/.env"; then
  echo "Generated .env contains literal \\\\n sequences"
  exit 1
fi

env_lines="$(wc -l < "$out/.env" | tr -d '[:space:]')"
if [ "$env_lines" -ne 3 ]; then
  echo "Generated .env has unexpected line count: $env_lines"
  exit 1
fi

echo "Template smoke render passed."
