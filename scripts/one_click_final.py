#!/usr/bin/env python3
"""One command to prepare the hackathon-ready bundle.

This script is intentionally conservative: it does not deploy contracts and it does
not require secrets. It runs local checks, refreshes the submission bundle, and
optionally tries the Playwright/ffmpeg recording pipeline.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], *, optional: bool = False) -> int:
    print("\n$", " ".join(cmd))
    proc = subprocess.run(cmd, cwd=ROOT)
    if proc.returncode and not optional:
        raise SystemExit(proc.returncode)
    if proc.returncode and optional:
        print(f"[warn] optional command failed with code {proc.returncode}")
    return proc.returncode


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-video", action="store_true", help="Do not run Playwright/ffmpeg recording")
    args = parser.parse_args()

    print("Scratch Wallet finalizer — no Codex credits needed")
    run([sys.executable, "scripts/preflight.py"])
    run([sys.executable, "-m", "pytest", "-q", "tests_py"])
    run([sys.executable, "scripts/prepare_submission_bundle.py"])

    if not args.skip_video:
        if shutil.which("ffmpeg") is None:
            print("[warn] ffmpeg not found. The Playwright recorder may still save webm/screenshots.")
        if sys.platform.startswith("win"):
            run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "scripts/record_demo.ps1"], optional=True)
        else:
            run(["bash", "scripts/record_demo.sh"], optional=True)

    print("\nDONE. Use SUBMISSION_READY/ and scratch-wallet-submission-bundle.zip for the hackathon.")


if __name__ == "__main__":
    main()
