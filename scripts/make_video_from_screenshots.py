#!/usr/bin/env python3
"""Fallback video maker: create an MP4 from screenshots with ffmpeg.

Use this if browser recording fails but screenshots exist:
  python scripts/make_video_from_screenshots.py --screenshots demo_recordings/<run>/screenshots --out demo_recordings/fallback.mp4
"""
from __future__ import annotations
import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--screenshots", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--seconds-per-slide", type=float, default=6.0)
    args = ap.parse_args()
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("ffmpeg not found. Install ffmpeg first.")
    shots = sorted(Path(args.screenshots).glob("*.png"))
    if not shots:
        raise SystemExit("No PNG screenshots found.")
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        for i, src in enumerate(shots, start=1):
            # Duplicate frames to create a pause per slide.
            dst = td_path / f"frame_{i:04d}.png"
            shutil.copy2(src, dst)
        cmd = [
            ffmpeg, "-y", "-framerate", str(1 / args.seconds_per_slide),
            "-i", str(td_path / "frame_%04d.png"),
            "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2",
            "-c:v", "libx264", "-r", "30", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)
        ]
        subprocess.run(cmd, check=True)
    print(f"Wrote {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
