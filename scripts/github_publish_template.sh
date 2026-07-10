#!/usr/bin/env bash
set -euo pipefail

REPO_URL=${1:-"https://github.com/mathieuweill/scratch-wallet.git"}

if [ ! -d .git ]; then
  git init
fi

git add .
git commit -m "Submit Scratch Wallet" || true
git branch -M main
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"
git push -u origin main
