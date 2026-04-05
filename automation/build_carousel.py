"""
SleepWise Reviews — Carousel Builder
Reads ig_image_prompts.txt and builds slides s1-s5 for every Carousel entry.
Run: python automation/build_carousel.py
"""

import os
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent.parent
IMAGES_DIR = BASE_DIR / "images" / "instagram"
PROMPTS    = BASE_DIR / "automation" / "data" / "ig_image_prompts.txt"

# ── Brand colours (Nocturnal Serenity palette) ─────────────────────────────────
DEEP_INDIGO    = (26,  26,  64)
MIDNIGHT       = (15,  15,  35)
WARM_AMBER     = (255, 191, 128)
CREAM          = (250, 248, 245)
MUTED_LAVENDER = (100,  90, 130)

SIZE = (1080, 1080)


# ── Background ─────────────────────────────────────────────────────────────────
def make_gradient_bg():
    """Deep indigo -> midnight vertical gradient."""
    img  = Image.new("RGB", SIZE, MIDNIGHT)
    draw = ImageDraw.Draw(img)
    for y in range(SIZE[1]):
        ratio = y / SIZE[1]
        r = int(DEEP_INDIGO[0] * (1 - ratio) + MIDNIGHT[0] * ratio)
        g = int(DEEP_INDIGO[1] * (1 - ratio) + MIDNIGHT[1] * ratio)
        b = int(DEEP_INDIGO[2] * (1 - ratio) + MIDNIGHT[2] * ratio)
        draw.line([(0, y), (SIZE[0], y)], fill=(r, g, b))
    return img


# ── Font helpers ───────────────────────────────────────────────────────────────
def get_font(size, bold=False):
    windows_fonts = "C:/Windows/Fonts"
    if bold:
        candidates = ["georgiab.ttf", "timesbd.ttf", "arialbd.ttf"]
    else:
        candidates = ["georgia.ttf",  "times.ttf",   "arial.ttf"]
    for f in candidates:
        path = os.path.join(windows_fonts, f)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines, line = [], ""
    for word in words:
        test = f"{line} {word}".strip()
        if draw.textlength(test, font=font) <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_centred_text(draw, lines, font, y_start, colour, line_gap=12):
    for line in lines:
        w  = draw.textlength(line, font=font)
        x  = (SIZE[0] - w) / 2
        draw.text((x, y_start), line, font=font, fill=colour)
        bb = font.getbbox(line)
        y_start += (bb[3] - bb[1]) + line_gap
    return y_start


# ── Brand mark ─────────────────────────────────────────────────────────────────
def draw_mini_crescent(img, x, y, radius=24):
    """Small crescent brand signature — composited via RGBA."""
    size    = radius * 6
    moon    = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    mdraw   = ImageDraw.Draw(moon)
    cx = cy = size // 2

    mdraw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                  fill=(*WARM_AMBER, 190))
    so = int(radius * 0.42)
    sr = int(radius * 0.88)
    mdraw.ellipse([cx + so - sr, cy - sr, cx + so + sr, cy + sr],
                  fill=(*MIDNIGHT, 255))

    base = img.convert("RGBA")
    px   = int(x - size // 2)
    py   = int(y - size // 2)
    base.paste(moon, (px, py), moon)
    return base.convert("RGB")


# ── Slide builders ─────────────────────────────────────────────────────────────
def add_hook_overlay(post_id, hook):
    """Overlay amber hook text on s1.png.
    Reads s1_bg.png (clean photo) if it exists, so repeated runs never stack overlays.
    Text strip is positioned on the mattress / subject area (middle band, not top).
    """
    folder   = IMAGES_DIR / post_id
    bg_path  = folder / "s1_bg.png"
    out_path = folder / "s1.png"

    src = bg_path if bg_path.exists() else out_path
    if not src.exists():
        print(f"  WARN no source photo for {post_id}, skipping hook overlay")
        return

    base = Image.open(src).convert("RGBA").resize(SIZE)

    # Semi-transparent strip over the mattress / mid area (y 540-900)
    # Fades in over 100px at top, stays solid, fades out over 80px at bottom
    overlay   = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    odraw     = ImageDraw.Draw(overlay)
    MAX_ALPHA = 168
    TOP       = 540
    FADE_IN   = 100   # y 540-640
    SOLID_BOT = 820   # y 640-820 solid
    FADE_OUT  = 80    # y 820-900

    for y in range(TOP, TOP + FADE_IN):
        a = int(MAX_ALPHA * (y - TOP) / FADE_IN)
        odraw.rectangle([(0, y), (SIZE[0], y + 1)], fill=(0, 0, 0, a))
    for y in range(TOP + FADE_IN, SOLID_BOT):
        odraw.rectangle([(0, y), (SIZE[0], y + 1)], fill=(0, 0, 0, MAX_ALPHA))
    for y in range(SOLID_BOT, SOLID_BOT + FADE_OUT):
        a = int(MAX_ALPHA * (1 - (y - SOLID_BOT) / FADE_OUT))
        odraw.rectangle([(0, y), (SIZE[0], y + 1)], fill=(0, 0, 0, a))

    img  = Image.alpha_composite(base, overlay)
    draw = ImageDraw.Draw(img)

    font_lg = get_font(54, bold=True)
    lines   = wrap_text(hook, font_lg, SIZE[0] - 140, draw)

    # Centre text block inside the solid band (y 640-820 → 180px usable)
    total_h = 0
    for ln in lines:
        bb       = font_lg.getbbox(ln)
        total_h += (bb[3] - bb[1]) + 14
    y_start = (TOP + FADE_IN) + ((SOLID_BOT - (TOP + FADE_IN)) - total_h) // 2

    draw_centred_text(draw, lines, font_lg, y_start, WARM_AMBER, line_gap=14)

    img.convert("RGB").save(out_path)
    print(f"  OK s1 hook overlay -> {post_id}/s1.png")


def make_point_slide(post_id, slide_num, point_raw):
    """Build s2/s3/s4 — gradient bg + Georgia serif + amber headline + cream body."""
    parts    = point_raw.split("|", 1)
    headline = parts[0].strip()
    benefit  = parts[1].strip() if len(parts) > 1 else ""

    img  = make_gradient_bg()
    draw = ImageDraw.Draw(img)

    pad   = 90
    max_w = SIZE[0] - pad * 2

    font_head    = get_font(56, bold=True)
    font_benefit = get_font(38, bold=False)
    font_num     = get_font(26, bold=False)

    # Slide number top-right, subtle
    draw.text((SIZE[0] - 70, 40), str(slide_num), font=font_num, fill=MUTED_LAVENDER)

    # Headline — strip ALL leading non-ASCII chars (emoji + variation selectors)
    head_text = headline
    while head_text and ord(head_text[0]) > 127:
        head_text = head_text[1:]
    head_text = head_text.strip()

    h_lines = wrap_text(head_text, font_head, max_w, draw)
    b_lines = wrap_text(benefit, font_benefit, max_w, draw)

    def block_height(lines, font, gap):
        h = 0
        for ln in lines:
            bb = font.getbbox(ln)
            h += (bb[3] - bb[1]) + gap
        return h

    GAP_HEAD   = 14
    GAP_BODY   = 14
    ACCENT_H   = 3    # amber line height
    ACCENT_GAP = 28   # space between amber line and headline
    SEP_SPACE  = 52   # lavender separator + spacing above/below

    total_h = (ACCENT_H + ACCENT_GAP
               + block_height(h_lines, font_head, GAP_HEAD)
               + SEP_SPACE
               + block_height(b_lines, font_benefit, GAP_BODY))

    # Vertically centre the whole block between slide number row and bottom margin
    y_block = 80 + ((980 - 80) - total_h) // 2

    # Amber accent line — anchored to the block, not the slide top
    draw.rectangle([(pad, y_block), (SIZE[0] - pad, y_block + ACCENT_H)], fill=WARM_AMBER)
    y = y_block + ACCENT_H + ACCENT_GAP

    # Headline
    y = draw_centred_text(draw, h_lines, font_head, y, WARM_AMBER, line_gap=GAP_HEAD)

    # Lavender separator
    y += 18
    draw.rectangle([(pad + 60, y), (SIZE[0] - pad - 60, y + 1)], fill=MUTED_LAVENDER)
    y += 34

    # Benefit
    draw_centred_text(draw, b_lines, font_benefit, y, CREAM, line_gap=GAP_BODY)

    out = IMAGES_DIR / post_id / f"s{slide_num}.png"
    img.save(out)
    print(f"  OK s{slide_num} -> {post_id}/s{slide_num}.png")


def make_cta_slide(post_id, cta_raw):
    """Build s5 — gradient + amber CTA text + orange pill URL + crescent brand mark."""
    img  = make_gradient_bg()
    draw = ImageDraw.Draw(img)

    pad   = 90
    max_w = SIZE[0] - pad * 2

    font_cta   = get_font(54, bold=True)
    font_url   = get_font(36, bold=True)
    font_brand = get_font(24, bold=False)

    # Split CTA from URL (supports both -> and arrow char)
    parts = cta_raw.split("->", 1)
    if len(parts) == 1:
        parts = cta_raw.split("\u2192", 1)
    cta_text = parts[0].strip()
    url      = parts[1].strip() if len(parts) > 1 else ""

    # Amber accent line
    draw.rectangle([(pad, 370), (SIZE[0] - pad, 373)], fill=WARM_AMBER)

    # CTA text
    y = 410
    cta_lines = wrap_text(cta_text, font_cta, max_w, draw)
    y = draw_centred_text(draw, cta_lines, font_cta, y, WARM_AMBER, line_gap=12)
    y += 44

    # Orange pill for URL
    if url:
        bb         = draw.textbbox((0, 0), url, font=font_url)
        url_w      = bb[2] - bb[0]
        url_h      = bb[3] - bb[1]
        pill_pad   = 36
        pill_left  = (SIZE[0] - url_w) // 2 - pill_pad
        pill_right = (SIZE[0] + url_w) // 2 + pill_pad
        draw.rounded_rectangle([pill_left, y - 8, pill_right, y + url_h + 16],
                                radius=40, fill=WARM_AMBER)
        draw.text(((SIZE[0] - url_w) // 2, y), url, font=font_url, fill=MIDNIGHT)

    # Small crescent — bottom-right, brand signature
    img = draw_mini_crescent(img, SIZE[0] - 80, SIZE[1] - 80, radius=24)
    draw = ImageDraw.Draw(img)

    # Brand handle — bottom centre
    brand = "@sleepwisereviews"
    bw    = draw.textlength(brand, font=font_brand)
    draw.text(((SIZE[0] - bw) // 2, SIZE[1] - 52), brand,
              font=font_brand, fill=MUTED_LAVENDER)

    out = IMAGES_DIR / post_id / "s5.png"
    img.save(out)
    print(f"  OK s5 (CTA) -> {post_id}/s5.png")


# ── Parser ─────────────────────────────────────────────────────────────────────
def parse_prompts(path):
    posts   = []
    current = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if re.match(r"^IG-\d+\s*\|", line):
            if current:
                posts.append(current)
            parts   = line.split("|", 1)
            current = {
                "id":   parts[0].strip().lower(),
                "type": parts[1].strip() if len(parts) > 1 else "",
            }
        elif line.startswith("PHOTO:"):
            current["photo"] = line[6:].strip()
        elif line.startswith("HOOK:"):
            current["hook"] = line[5:].strip()
        elif re.match(r"^POINT-\d:", line):
            pts = current.setdefault("points", [])
            pts.append(line.split(":", 1)[1].strip())
        elif line.startswith("CTA:"):
            current["cta"] = line[4:].strip()
    if current:
        posts.append(current)
    return posts


# ── Main ───────────────────────────────────────────────────────────────────────
def build():
    posts   = parse_prompts(PROMPTS)
    built   = 0
    skipped = 0

    for post in posts:
        pid   = post["id"].lower()
        ptype = post.get("type", "")

        if "Carousel" not in ptype:
            skipped += 1
            continue

        folder = IMAGES_DIR / pid
        folder.mkdir(exist_ok=True)

        print(f"\n>> {pid.upper()} - {ptype}")

        if "hook" in post:
            add_hook_overlay(pid, post["hook"])

        points = post.get("points", [])
        for i, pt in enumerate(points[:3], start=2):
            make_point_slide(pid, i, pt)

        if "cta" in post:
            make_cta_slide(pid, post["cta"])

        built += 1

    print(f"\nDone - {built} carousels built, {skipped} non-carousel skipped.")


if __name__ == "__main__":
    build()
