#!/usr/bin/env bash
# Publish content changes: commit everything under content/ and push.
# GitHub Actions builds and deploys the site automatically (~2 min).
set -euo pipefail
cd "$(dirname "$0")"

if [ -z "$(git status --porcelain content)" ]; then
  echo "No content changes to publish."
  exit 0
fi

git add -A content
git commit -m "content: update $(date '+%Y-%m-%d %H:%M')"
git push
echo "Pushed. Site will be live at https://yggphh.github.io in about 2 minutes."
