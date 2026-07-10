#!/usr/bin/env python3
"""Automated demo recorder for Scratch Wallet.

What it does:
1. Optionally starts `streamlit run app.py` locally.
2. Opens the app with Playwright/Chromium.
3. Clicks through the key hackathon demo flow.
4. Records a browser video as WEBM.
5. Converts it to MP4 with ffmpeg when available.
6. Saves screenshots for DoraHacks / README assets.

Install once:
  pip install -r requirements.txt
  pip install -r requirements-video.txt
  python -m playwright install chromium

Run:
  python scripts/record_demo_playwright.py --start-app
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen


def wait_for_http(url: str, timeout: int = 60) -> None:
    start = time.time()
    last_error: Exception | None = None
    while time.time() - start < timeout:
        try:
            with urlopen(url, timeout=2) as resp:  # nosec - local demo utility
                if resp.status < 500:
                    return
        except Exception as exc:  # noqa: BLE001
            last_error = exc
        time.sleep(1)
    raise RuntimeError(f"Timed out waiting for {url}. Last error: {last_error}")


def safe_click(page, text: str, timeout: int = 3500) -> bool:
    candidates = [
        lambda: page.get_by_role("button", name=text),
        lambda: page.get_by_text(text, exact=True),
        lambda: page.get_by_text(text),
    ]
    for make_locator in candidates:
        try:
            loc = make_locator()
            loc.first.click(timeout=timeout)
            return True
        except Exception:
            continue
    print(f"[WARN] Could not click: {text}")
    return False


def screenshot(page, out_dir: Path, name: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{name}.png"
    try:
        page.screenshot(path=str(path), full_page=True)
        print(f"[OK] screenshot {path}")
    except Exception as exc:  # noqa: BLE001
        print(f"[WARN] screenshot failed for {name}: {exc}")


def run_ffmpeg_convert(webm: Path, mp4: Path) -> bool:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        print("[WARN] ffmpeg not found. WEBM kept; MP4 not generated.")
        return False
    cmd = [
        ffmpeg,
        "-y",
        "-i",
        str(webm),
        "-vf",
        "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2",
        "-r",
        "30",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "24",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        str(mp4),
    ]
    print("[RUN]", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print(f"[OK] MP4 written to {mp4}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:8501")
    parser.add_argument("--port", type=int, default=8501)
    parser.add_argument("--start-app", action="store_true", help="Start Streamlit automatically before recording")
    parser.add_argument("--headed", action="store_true", help="Show Chromium window while recording")
    parser.add_argument("--out", default="demo_recordings", help="Output directory")
    parser.add_argument("--keep-webm", action="store_true", help="Keep Playwright WEBM after MP4 conversion")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    out_root = root / args.out
    stamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    run_dir = out_root / f"scratch-wallet-demo-{stamp}"
    video_dir = run_dir / "playwright-video"
    shots_dir = run_dir / "screenshots"
    video_dir.mkdir(parents=True, exist_ok=True)
    shots_dir.mkdir(parents=True, exist_ok=True)

    proc: subprocess.Popen | None = None
    if args.start_app:
        cmd = [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app.py",
            "--server.port",
            str(args.port),
            "--server.headless",
            "true",
            "--browser.gatherUsageStats",
            "false",
        ]
        print("[RUN]", " ".join(cmd))
        proc = subprocess.Popen(cmd, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        args.url = f"http://localhost:{args.port}"

    try:
        wait_for_http(args.url, timeout=75)
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=not args.headed)
            context = browser.new_context(
                viewport={"width": 1280, "height": 720},
                record_video_dir=str(video_dir),
                record_video_size={"width": 1280, "height": 720},
            )
            page = context.new_page()
            page.goto(args.url, wait_until="networkidle", timeout=90000)
            page.wait_for_timeout(2500)
            screenshot(page, shots_dir, "01_landing")

            safe_click(page, "🎫 Scratch Today") or safe_click(page, "Scratch Today")
            page.wait_for_timeout(4500)
            screenshot(page, shots_dir, "02_daily_scratch_result")

            safe_click(page, "Mock Anchor")
            page.wait_for_timeout(2500)
            screenshot(page, shots_dir, "03_mock_anchor")

            # Sidebar navigation items. Streamlit radio labels are text nodes/buttons depending on version.
            nav = [
                "Scratch Card",
                "Control Room",
                "Claim Shield",
                "Opportunities",
                "Anchor / Deploy",
                "Video / Submit",
                "Submission",
            ]
            for idx, label in enumerate(nav, start=4):
                safe_click(page, label)
                page.wait_for_timeout(2600)
                clean = label.lower().replace(" ", "_").replace("/", "")
                screenshot(page, shots_dir, f"{idx:02d}_{clean}")

            # Return to Demo at end for a clean closing frame.
            safe_click(page, "Demo")
            page.wait_for_timeout(2500)
            screenshot(page, shots_dir, "11_closing_demo")

            context.close()
            browser.close()

        webms = sorted(video_dir.glob("*.webm"), key=lambda x: x.stat().st_mtime, reverse=True)
        if not webms:
            raise RuntimeError("No Playwright video file was produced.")
        webm = webms[0]
        final_webm = run_dir / "scratch_wallet_demo.webm"
        webm.rename(final_webm)
        print(f"[OK] WEBM written to {final_webm}")

        mp4 = run_dir / "scratch_wallet_demo.mp4"
        converted = run_ffmpeg_convert(final_webm, mp4)
        if converted and not args.keep_webm:
            # Keep the named WEBM anyway because it is often useful for debugging if mp4 is rejected.
            pass

        # Copy narration/subtitle helper into the recording folder.
        srt_src = root / "video_assets" / "demo_narration.srt"
        if srt_src.exists():
            shutil.copy2(srt_src, run_dir / "demo_narration.srt")

        (run_dir / "README_VIDEO_OUTPUT.md").write_text(
            f"""# Scratch Wallet video output\n\nGenerated at: {stamp} UTC\n\nFiles:\n- `scratch_wallet_demo.mp4` — preferred upload if present.\n- `scratch_wallet_demo.webm` — browser recording fallback.\n- `screenshots/` — screenshots for README/DoraHacks.\n- `demo_narration.srt` — optional subtitle/narration guide.\n\nSuggested DoraHacks caption:\n\n> Scratch Wallet is a risk-capped autonomous DeFi micro-wallet: a lottery ticket that knows when not to play.\n""",
            encoding="utf-8",
        )
        print(f"[DONE] Demo assets are in: {run_dir}")
        return 0
    finally:
        if proc:
            proc.terminate()
            try:
                proc.wait(timeout=8)
            except subprocess.TimeoutExpired:
                proc.kill()


if __name__ == "__main__":
    raise SystemExit(main())
