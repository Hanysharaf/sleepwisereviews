"""
build_storefront_batch2.py
===========================
Rebuilds the 6 Amazon Storefront "Weeks 3-13" cover images from their clean
lifestyle-photo bases (*_bg.png) with a fixed hook-text overlay.

Fix (2026-09-05, per Hany's feedback: "the hook too long and small letters
the photo is nice but load of word writin on it"):
  - Added a real solid scrim panel behind the text (darker, and running to
    the bottom edge) instead of relying on the photo's natural shadow -- the
    old version had text sitting almost directly on a busy photo.
  - Split each hook into two tiers at its natural sentence break: a larger
    bold amber "lead" sentence, then a smaller cream "support" sentence,
    separated by a thin amber divider -- same visual language as the
    carousel point slides in build_carousel.py. This breaks the paragraph
    into a hierarchy instead of one wall of same-size text.
  - Minimum font sizes raised well above whatever the old auto-shrink
    allowed: lead never drops below 38px, support never below 30px.

The hook text itself is never altered -- word-for-word identical to Dina's
copy, since the same text is reused as the Amazon post caption.

Does NOT regenerate the base lifestyle photos (*_bg.png) -- only rebuilds
the overlay on top of them.

Usage:
    python automation/scripts/build_storefront_batch2.py
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw

BASE_DIR   = Path(__file__).resolve().parent.parent.parent
AUTO_DIR   = BASE_DIR / "automation"
COVERS_DIR = AUTO_DIR / "data" / "storefront_covers_batch2"

sys.path.insert(0, str(AUTO_DIR))
from build_carousel import (  # noqa: E402
    get_font, wrap_text, draw_centred_text,
    WARM_AMBER, CREAM, MUTED_LAVENDER, SIZE,
)

# ── Dina's exact hook copy -- do not edit, must match the Amazon caption ──────
HOOKS = {
    "anti-snoring": (
        "Snoring has more than one cause, and the fix only works if it "
        "matches the cause - a chin strap helps mouth-breathers but does "
        "nothing for tongue-based obstruction. A mandibular advancement "
        "device physically shifts the lower jaw forward to open the "
        "airway, which is why it's the most evidence-backed over-the-"
        "counter option."
    ),
    "mattress-topper": (
        "A topper changes surface feel and pressure distribution without "
        "replacing a mattress that's still structurally sound underneath. "
        "Density matters more than thickness - denser foam holds its "
        "support and contour longer before body impressions start to form."
    ),
    "bamboo-sheets": (
        "Bamboo fabric is naturally moisture-wicking and thermoregulating, "
        "which is why it sleeps noticeably cooler than standard cotton "
        "sateen. Look for lyocell over viscose - it's processed more "
        "sustainably and holds up better wash after wash."
    ),
    "cooling-pillow": (
        "Cooling pillows work through a few different mechanisms, not just "
        "a cold-to-the-touch cover. Gel conducts heat away from your head "
        "while phase-change material absorbs it as it shifts from solid to "
        "liquid - open-cell foam or latex fill keeps that effect going "
        "longer than dense memory foam."
    ),
    "earplugs": (
        "An earplug's real-world noise reduction runs roughly half its "
        "stated NRR rating, so a 32 NRR plug is cutting closer to 16 dB in "
        "practice. Low-profile flanged silicone holds a better seal than "
        "foam once you're on your side, which matters more for blocking a "
        "snoring partner than the NRR number alone."
    ),
    "sleep-mask": (
        "Even a small gap of light leaking in around the nose bridge "
        "defeats the point of wearing a mask at all. Contoured designs "
        "that hover over the eyes seal out light without pressing on the "
        "eyelids, avoiding the eye pressure flat masks can cause for "
        "sensitive sleepers."
    ),
}

# ── Layout constants ──────────────────────────────────────────────────────────
PAD           = 84
MIN_TOP       = 430   # never darken above this line -- keeps the subject visible
PANEL_BOTTOM  = 1000   # leave room below for the @handle
PAD_TOP       = 46
PAD_BOTTOM    = 30
DIV_ABOVE     = 22
DIV_BELOW     = 26
GAP_LEAD      = 10
GAP_SUPPORT   = 10
MAX_ALPHA     = 210
FADE_IN       = 90

LEAD_SIZES    = [50, 46, 42, 38]
SUPPORT_SIZES = [38, 35, 32, 30]


def split_hook(hook: str):
    """Split at the first '. ' -- every batch-2 hook is exactly two sentences."""
    idx = hook.find(". ")
    if idx == -1:
        return hook, ""
    return hook[:idx + 1], hook[idx + 2:]


def block_height(lines, font, gap):
    h = 0
    for ln in lines:
        bb = font.getbbox(ln)
        h += (bb[3] - bb[1]) + gap
    return h


def add_long_hook_overlay(post_id: str, hook: str):
    bg_path  = COVERS_DIR / f"{post_id}_bg.png"
    out_path = COVERS_DIR / f"{post_id}.png"
    if not bg_path.exists():
        print(f"  WARN no bg photo for {post_id}, skipping")
        return

    base = Image.open(bg_path).convert("RGBA").resize(SIZE)
    lead, support = split_hook(hook)

    max_w = SIZE[0] - PAD * 2
    dummy = ImageDraw.Draw(Image.new("RGB", (10, 10)))

    chosen = None
    for lsize, ssize in zip(LEAD_SIZES, SUPPORT_SIZES):
        font_lead    = get_font(lsize, bold=True)
        font_support = get_font(ssize, bold=False)
        lead_lines    = wrap_text(lead, font_lead, max_w, dummy)
        support_lines = wrap_text(support, font_support, max_w, dummy) if support else []

        total_h = block_height(lead_lines, font_lead, GAP_LEAD)
        if support_lines:
            total_h += DIV_ABOVE + 3 + DIV_BELOW
            total_h += block_height(support_lines, font_support, GAP_SUPPORT)

        available = PANEL_BOTTOM - MIN_TOP - PAD_TOP - PAD_BOTTOM
        is_last = (lsize, ssize) == (LEAD_SIZES[-1], SUPPORT_SIZES[-1])
        if total_h <= available or is_last:
            chosen = (font_lead, font_support, lead_lines, support_lines, total_h)
            break

    font_lead, font_support, lead_lines, support_lines, total_h = chosen
    top = max(MIN_TOP, PANEL_BOTTOM - PAD_TOP - PAD_BOTTOM - total_h)

    # Scrim: fades in over FADE_IN px, then solid straight to the bottom edge.
    overlay = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    odraw   = ImageDraw.Draw(overlay)
    for y in range(top, top + FADE_IN):
        a = int(MAX_ALPHA * (y - top) / FADE_IN)
        odraw.rectangle([(0, y), (SIZE[0], y + 1)], fill=(0, 0, 0, a))
    odraw.rectangle([(0, top + FADE_IN), (SIZE[0], SIZE[1])], fill=(0, 0, 0, MAX_ALPHA))

    img  = Image.alpha_composite(base, overlay)
    draw = ImageDraw.Draw(img)

    y = top + PAD_TOP
    y = draw_centred_text(draw, lead_lines, font_lead, y, WARM_AMBER, line_gap=GAP_LEAD)

    if support_lines:
        y += DIV_ABOVE
        draw.rectangle([(PAD + 60, y), (SIZE[0] - PAD - 60, y + 3)], fill=WARM_AMBER)
        y += DIV_BELOW
        draw_centred_text(draw, support_lines, font_support, y, CREAM, line_gap=GAP_SUPPORT)

    font_brand = get_font(24, bold=False)
    brand = "@sleepwisereviews"
    bw = draw.textlength(brand, font=font_brand)
    draw.text(((SIZE[0] - bw) / 2, SIZE[1] - 52), brand, font=font_brand, fill=MUTED_LAVENDER)

    img.convert("RGB").save(out_path)
    print(
        f"  OK {post_id}: lead {font_lead.size}px x{len(lead_lines)} lines / "
        f"support {font_support.size if support_lines else '-'}px x{len(support_lines)} lines "
        f"-> {out_path.name}"
    )


def main():
    for pid, hook in HOOKS.items():
        print(f">> {pid}")
        add_long_hook_overlay(pid, hook)


if __name__ == "__main__":
    main()
