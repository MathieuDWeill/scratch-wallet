$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")
python -m pip install -r requirements.txt
python -m pip install -r requirements-video.txt
python -m playwright install chromium
python scripts/record_demo_playwright.py --start-app
