#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$repo_root"

latest_sdk="$(python - <<'PY'
from urllib.request import urlopen
import json

with urlopen("https://pypi.org/pypi/wordlift-sdk/json", timeout=10) as response:
    payload = json.load(response)

print(payload["info"]["version"])
PY
)"

python - <<'PY' "$latest_sdk"
from pathlib import Path
import re
import sys

latest = sys.argv[1]
major = int(latest.split(".", 1)[0])
upper = major + 1
new_constraint = f"wordlift-sdk>={latest},<{upper}.0.0"

path = Path("pyproject.toml")
text = path.read_text(encoding="utf-8")
updated, count = re.subn(r"wordlift-sdk>=[^\",]+,<[^\",]+", new_constraint, text, count=1)
if count != 1:
    raise SystemExit("Failed to update wordlift-sdk dependency constraint in pyproject.toml")
path.write_text(updated, encoding="utf-8")
PY

echo "Updated SDK baseline to wordlift-sdk>=${latest_sdk}"
uv lock --upgrade-package wordlift-sdk

latest_graph_sync_tag="$(git ls-remote --tags --refs https://github.com/wordlift/graph-sync.git 'v*' | awk '{print $2}' | sed 's#refs/tags/##' | sort -V | tail -n 1)"
if [ -z "$latest_graph_sync_tag" ]; then
  echo "Failed to resolve latest wordlift/graph-sync tag"
  exit 1
fi

python - <<'PY' "$latest_graph_sync_tag"
from pathlib import Path
import re
import sys

tag = sys.argv[1]
path = Path(".github/workflows/graph-sync.yml")
text = path.read_text(encoding="utf-8")
updated, count = re.subn(r"wordlift/graph-sync@v[0-9][^\s]*", f"wordlift/graph-sync@{tag}", text, count=1)
if count != 1:
    raise SystemExit("Failed to update wordlift/graph-sync action version in workflow")
path.write_text(updated, encoding="utf-8")
PY

echo "Updated workflow action to wordlift/graph-sync@${latest_graph_sync_tag}"

"$repo_root/scripts/deploy_release.sh" patch
