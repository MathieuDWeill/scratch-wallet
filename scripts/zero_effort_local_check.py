#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def run(cmd):
    print(f"\n$ {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=ROOT)

steps = [
    [sys.executable, "scripts/preflight.py"],
    [sys.executable, "-m", "pytest", "-q", "tests_py"],
    [sys.executable, "scripts/prepare_submission_bundle.py"],
]

failed = False
for cmd in steps:
    res = run(cmd)
    if res.returncode != 0:
        failed = True
        print(f"FAILED: {' '.join(cmd)}")

if failed:
    sys.exit(1)

print("\nOK — local checks passed.")
print("Next: streamlit run app.py")
print("Submission fields: SUBMISSION_READY/DORAHACKS_FORM_FIELDS.md")
