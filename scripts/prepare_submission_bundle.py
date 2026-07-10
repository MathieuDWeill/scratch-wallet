#!/usr/bin/env python3
from __future__ import annotations

import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "submission_bundle"
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
for rel in [
    "SUBMISSION_READY",
    "docs",
    "demo_assets",
    "video_assets",
    "README.md",
    "RUN_ME_FIRST.md",
    "contracts/ScratchWalletRegistry.sol",
]:
    src = ROOT / rel
    dst = OUT / rel
    if src.is_dir():
        shutil.copytree(src, dst)
    elif src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
(OUT / "BUILD_INFO.txt").write_text(f"Scratch Wallet submission bundle generated {datetime.now(timezone.utc).isoformat()}\n")
zip_path = ROOT / "scratch-wallet-submission-bundle.zip"
if zip_path.exists():
    zip_path.unlink()
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for p in OUT.rglob("*"):
        if p.is_file():
            z.write(p, p.relative_to(OUT))
print(zip_path)
