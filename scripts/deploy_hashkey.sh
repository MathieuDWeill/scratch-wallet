#!/usr/bin/env bash
set -euo pipefail
if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env. Edit DEPLOYER_PRIVATE_KEY, then rerun this script."
  exit 1
fi
npm install
npm run compile
npm run test
npm run deploy:hashkey
python scripts/write_streamlit_secrets_from_env.py || true
