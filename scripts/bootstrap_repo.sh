#!/usr/bin/env bash
set -euo pipefail

if [ ! -d .git ]; then
  git init
fi

git add .
git commit -m "Initial scaffold for AI Awards Judge" || true

echo "Repository initialized. Add a remote next:"
echo "  git remote add origin <YOUR_GITHUB_REPO_URL>"
echo "  git push -u origin main"
