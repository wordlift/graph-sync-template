#!/usr/bin/env bash
set -euo pipefail

release_type="${1:-patch}"

case "$release_type" in
  major|minor|patch) ;;
  *)
    echo "Invalid release type: $release_type"
    echo "Usage: scripts/deploy_release.sh [major|minor|patch]"
    exit 1
    ;;
esac

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "This macro must run inside a git repository."
  exit 1
fi

current_branch="$(git rev-parse --abbrev-ref HEAD)"
if [ "$current_branch" = "HEAD" ]; then
  echo "Detached HEAD is not supported for release deploys."
  exit 1
fi

uv version --bump "$release_type"
new_version="$(uv version --short)"

echo "Refresh dependencies and lockfile"
uv sync --dev
uv lock

echo "Required documentation checkpoint before release"
echo "- Update AGENTS.md"
echo "- Update README.md"
echo "- Update docs/"

git add -A
git commit -m "chore(release): v${new_version}"

tag="v${new_version}"
if git rev-parse "$tag" >/dev/null 2>&1; then
  echo "Tag already exists: $tag"
  exit 1
fi

git tag "$tag"
git push origin "$current_branch"
git push origin --tags

echo "Release deployed: ${tag}"
