"""
fix_s1_banner.py
----------------
Strips the solid-black text banner from the TOP of s1.png,
saves the clean photo as s1_bg.png so build_carousel.py
can re-apply the hook overlay correctly.

Usage:
    python automation/fix_s1_banner.py
"""

from pathlib import Path
from PIL import Image
import numpy as np

BASE = Path(__file__).parent.parent / "images" / "instagram"
TARGETS = ["ig-002", "ig-010"]


def find_banner_end(img: Image.Image) -> int:
    """
    Find where the solid-black top banner ends.
    Strategy: a row is 'banner' when > 55% of its pixels are very dark
    (R+G+B < 60). Scan from top; return the y where we exit the last
    consecutive run of banner rows, plus a small buffer.
    Minimum scan starts at y=100 to skip any thin black strip at the top.
    """
    arr = np.array(img.convert("RGB"))
    height = arr.shape[0]
    last_banner_y = 0
    for y in range(height):
        dark_fraction = (arr[y].sum(axis=1) < 60).mean()
        if dark_fraction > 0.55:
            last_banner_y = y
        elif last_banner_y > 100:
            # We've exited a substantial banner — add 10px buffer
            return last_banner_y + 10
    return 0


def fix_folder(name: str) -> None:
    folder  = BASE / name
    s1      = folder / "s1.png"
    bg      = folder / "s1_bg.png"

    if not s1.exists():
        print(f"[{name}] s1.png not found — skipping")
        return

    if bg.exists():
        print(f"[{name}] s1_bg.png already exists — skipping")
        return

    img = Image.open(s1).convert("RGB")
    banner_end = find_banner_end(img)

    if banner_end < 20:
        print(f"[{name}] No banner detected (first bright row at y={banner_end}) — saving s1.png as-is")
        img.save(bg)
        return

    print(f"[{name}] Banner ends at y={banner_end} — cropping…")
    cropped = img.crop((0, banner_end, img.width, img.height))
    clean   = cropped.resize((1080, 1080), Image.LANCZOS)
    clean.save(bg)
    print(f"[{name}] OK s1_bg.png saved  ({img.width}x{img.height - banner_end} -> 1080x1080)")


if __name__ == "__main__":
    for t in TARGETS:
        fix_folder(t)
    print("\nDone. Now run:  python automation/build_carousel.py")
