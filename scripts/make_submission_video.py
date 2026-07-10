#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from pathlib import Path
from textwrap import wrap

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "demo_recordings" / "scratch-wallet-dorahacks-submission"
FRAMES_DIR = OUT_DIR / "frames"
OUT_MP4 = OUT_DIR / "scratch_wallet_dorahacks_submission.mp4"
WIDTH = 1280
HEIGHT = 720


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        p = Path(candidate)
        if p.exists():
            return ImageFont.truetype(str(p), size=size)
    return ImageFont.load_default()


F_HERO = font(58, True)
F_TITLE = font(44, True)
F_SUB = font(29, False)
F_BODY = font(25, False)
F_SMALL = font(19, False)
F_MONO = font(20, False)
F_BADGE = font(18, True)


def draw_bg(draw: ImageDraw.ImageDraw) -> None:
    top = (9, 15, 28)
    bottom = (19, 35, 49)
    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)
        color = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        draw.line([(0, y), (WIDTH, y)], fill=color)
    draw.rectangle((0, 0, WIDTH, 8), fill=(38, 166, 154))
    draw.rectangle((0, HEIGHT - 8, WIDTH, HEIGHT), fill=(242, 201, 76))


def draw_logo(img: Image.Image, x: int = 72, y: int = 52, size: int = 86) -> None:
    logo_path = ROOT / "assets" / "scratch-wallet-logo-480.png"
    if logo_path.exists():
        logo = Image.open(logo_path).convert("RGBA").resize((size, size), Image.LANCZOS)
        img.alpha_composite(logo, (x, y))


def draw_wrapped(draw: ImageDraw.ImageDraw, text: str, xy: tuple[int, int], font_obj, fill, width_chars: int, line_gap: int = 8) -> int:
    x, y = xy
    for para in text.split("\n"):
        lines = wrap(para, width=width_chars) or [""]
        for line in lines:
            draw.text((x, y), line, font=font_obj, fill=fill)
            y += font_obj.size + line_gap
        y += 4
    return y


def badge(draw: ImageDraw.ImageDraw, x: int, y: int, text: str, fill=(38, 166, 154)) -> int:
    pad_x = 16
    pad_y = 8
    box = draw.textbbox((0, 0), text, font=F_BADGE)
    w = box[2] - box[0] + pad_x * 2
    h = box[3] - box[1] + pad_y * 2
    draw.rounded_rectangle((x, y, x + w, y + h), radius=8, fill=fill)
    draw.text((x + pad_x, y + pad_y - 1), text, font=F_BADGE, fill=(5, 12, 20))
    return x + w + 12


def slide(title: str, body: str, *, eyebrow: str = "Scratch Wallet", bullets: list[str] | None = None, footer: str = "") -> Image.Image:
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    draw_bg(draw)
    draw_logo(img)
    draw.text((180, 64), eyebrow, font=F_SMALL, fill=(148, 163, 184))
    draw.text((72, 166), title, font=F_TITLE, fill=(248, 250, 252))
    y = draw_wrapped(draw, body, (76, 244), F_SUB, (203, 213, 225), 58, 10)
    if bullets:
        y += 10
        for item in bullets:
            draw.ellipse((84, y + 10, 96, y + 22), fill=(242, 201, 76))
            y = draw_wrapped(draw, item, (112, y), F_BODY, (226, 232, 240), 70, 8)
            y += 4
    if footer:
        draw.text((76, 650), footer, font=F_SMALL, fill=(148, 163, 184))
    return img


def proof_slide() -> Image.Image:
    img = slide(
        "HashKey mainnet proof",
        "ScratchWalletRegistry is deployed on HashKey Chain mainnet and a real demo decision was anchored.",
        bullets=[
            "Contract: 0x33145C082811c5E88ce055DAD816aE540a89da94",
            "Anchor tx: 0x1bdbeac34080908bad17a491b76f212d455102195d2ff985cdd0384775329de6",
            "Funding tx: 0x88262d336419b7592cf0582fb2aed823ce9c15033aab8a286c70f7195a2f96d4",
        ],
        footer="Explorer: hashkey.blockscout.com",
    )
    return img


def hero_slide() -> Image.Image:
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    draw_bg(draw)
    draw_logo(img, 92, 70, 116)
    draw.text((230, 88), "Scratch Wallet", font=F_HERO, fill=(248, 250, 252))
    draw.text((232, 158), "by Mathieu D. WEILL", font=F_SMALL, fill=(148, 163, 184))
    draw.text((92, 270), "A lottery ticket that knows when not to play.", font=F_TITLE, fill=(242, 201, 76))
    draw_wrapped(
        draw,
        "A risk-capped autonomous DeFi micro-wallet for HashKey Chain. Users fund a tiny isolated wallet, choose a risk mode, and let the agent refuse unsafe trades, approvals, and claims.",
        (96, 352),
        F_SUB,
        (203, 213, 225),
        64,
        10,
    )
    x = 96
    for text in ["bounded downside", "autonomous micro-wallet", "Claim Shield", "HashKey audit trail"]:
        x = badge(draw, x, 578, text)
    return img


def closing_slide() -> Image.Image:
    img = slide(
        "Ready for DoraHacks",
        "Scratch Wallet is submitted as a consumer-facing autonomous finance prototype with bounded downside, auditability, and real HashKey mainnet anchoring.",
        bullets=[
            "GitHub: github.com/MathieuDWeill/scratch-wallet",
            "Core message: Autonomous finance should start with bounded downside.",
            "No main wallet. No unlimited approvals. No promised yield.",
        ],
        footer="Scratch Wallet - HashKey Chain On-Chain Horizon Hackathon",
    )
    return img


def app_screenshot(name: str) -> Image.Image:
    path = ROOT / "demo_recordings" / "scratch-wallet-app-captures" / "screenshots" / name
    img = Image.open(path).convert("RGB")
    return img.resize((WIDTH, HEIGHT), Image.LANCZOS)


def main() -> None:
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    slides = [
        hero_slide(),
        app_screenshot("01_demo_intro.png"),
        app_screenshot("02_demo_scratch_today.png"),
        app_screenshot("04_scratch_card.png"),
        app_screenshot("05_control_room.png"),
        app_screenshot("06_claim_shield.png"),
        app_screenshot("07_anchor_deploy.png"),
        proof_slide(),
        app_screenshot("09_submission.png"),
        slide(
            "What is on-chain",
            "The contract does not custody funds and does not execute trades. It anchors decision evidence for review.",
            bullets=["Opportunity hash and report hash.", "Played or skipped decision.", "Risk mode, bankroll, trade size, edge, and risk score."],
        ),
        closing_slide(),
    ]
    for idx, frame in enumerate(slides, start=1):
        frame.convert("RGB").save(FRAMES_DIR / f"frame_{idx:04d}.png", quality=95)

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    OUT_MP4.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        ffmpeg,
        "-y",
        "-framerate",
        "1/7",
        "-i",
        str(FRAMES_DIR / "frame_%04d.png"),
        "-vf",
        "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2",
        "-c:v",
        "libx264",
        "-r",
        "30",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        str(OUT_MP4),
    ]
    subprocess.run(cmd, check=True)
    (OUT_DIR / "README_VIDEO_OUTPUT.md").write_text(
        "# Scratch Wallet DoraHacks submission video\n\n"
        f"MP4: `{OUT_MP4.name}`\n"
        "Format: 1280x720 H.264 MP4\n"
        "Use this file for the DoraHacks demo video upload, or upload it to YouTube and paste the URL in the BUIDL form.\n",
        encoding="utf-8",
    )
    print(OUT_MP4)


if __name__ == "__main__":
    main()
