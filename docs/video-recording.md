# Automated video recording

This repo includes a no-edit video pipeline so you do not need to manually record a demo.

## Install local video tools

### Windows PowerShell

```powershell
cd scratch-wallet-streamlit
scripts\record_demo.ps1
```

### macOS / Linux / WSL

```bash
cd scratch-wallet-streamlit
./scripts/record_demo.sh
```

The script will:

1. install Python dependencies;
2. install Playwright Chromium;
3. launch Streamlit locally;
4. click through the demo automatically;
5. save screenshots;
6. record a browser video;
7. convert it to MP4 using `ffmpeg` if available.

## Output

The video assets are written to:

```text
demo_recordings/scratch-wallet-demo-YYYYMMDD-HHMMSS/
```

Main file to upload:

```text
scratch_wallet_demo.mp4
```

Fallback if MP4 is not created:

```text
scratch_wallet_demo.webm
```

## ffmpeg install

If MP4 conversion fails, install ffmpeg.

Windows with Chocolatey:

```powershell
choco install ffmpeg -y
```

Windows with winget:

```powershell
winget install Gyan.FFmpeg
```

Ubuntu / WSL:

```bash
sudo apt-get update && sudo apt-get install -y ffmpeg
```

macOS:

```bash
brew install ffmpeg
```

## Manual fallback

If browser recording fails but screenshots are created:

```bash
python scripts/make_video_from_screenshots.py --screenshots demo_recordings/<run>/screenshots --out demo_recordings/fallback.mp4
```

## Suggested 90-second script

Use `SUBMISSION_READY/VIDEO_SCRIPT_90_SECONDS.md`.
The generated `video_assets/demo_narration.srt` can also be used as a subtitle/narration guide.
