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

latest_worai="$(python - <<'PY'
from urllib.request import urlopen
import json

with urlopen("https://pypi.org/pypi/worai/json", timeout=10) as response:
    payload = json.load(response)

print(payload["info"]["version"])
PY
)"

python - <<'PY' "$latest_worai"
from pathlib import Path
import re
import sys

version = sys.argv[1]
path = Path(".github/workflows/graph-sync.yml")
text = path.read_text(encoding="utf-8")
updated, count = re.subn(r'worai_version: "[^"]+"', f'worai_version: "{version}"', text, count=1)
if count != 1:
    raise SystemExit("Failed to update worai_version in workflow")
path.write_text(updated, encoding="utf-8")
PY

echo "Updated workflow worai_version to ${latest_worai}"

"$repo_root/scripts/deploy_release.sh" patch
