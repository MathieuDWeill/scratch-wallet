#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ -x ".venv/bin/python" ]]; then
  PYTHON_BIN=".venv/bin/python"
else
  PYTHON_BIN="${PYTHON:-$(command -v python3 || command -v python)}"
fi
"$PYTHON_BIN" -m pip install -r requirements.txt
"$PYTHON_BIN" -m pip install -r requirements-video.txt
"$PYTHON_BIN" -m playwright install chromium
"$PYTHON_BIN" scripts/record_demo_playwright.py --start-app
