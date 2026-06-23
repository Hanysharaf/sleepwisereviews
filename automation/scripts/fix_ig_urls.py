"""
fix_ig_urls.py — Bulk-fills blank image_url for IG-032 through IG-090 in Google Sheet.

All images for ig-032..ig-059 were built by build_carousel.py but the sheet
was never updated with the URLs. ig-060..ig-090 have no images yet, so they
get a fallback pointing to the last available slide.

Run from repo root:
    python automation/scripts/fix_ig_urls.py

Requires Google credentials in automation/data/
  Option A: automation/data/service_account.json
  Option B: automation/data/google_credentials.json + google_token.json
"""

import sys
import sqlite3
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "automation"))

from sheets_db import pull, push, set_field

BASE_URL   = "https://raw.githubusercontent.com/Hanysharaf/sleepwisereviews/main/images/instagram"
IMAGES_DIR = ROOT / "images" / "instagram"
FALLBACK   = f"{BASE_URL}/ig-059/s2.png"


def best_image_url(post_id: str) -> str:
    """Return the best available image URL for a post, or the shared fallback."""
    folder = IMAGES_DIR / post_id.lower()
    if not folder.exists():
        return FALLBACK

    # Priority: any *cover* PNG > s1.png > s2.png
    for p in sorted(folder.glob("*cover*.png")):
        return f"{BASE_URL}/{post_id.lower()}/{p.name}"
    for name in ("s1.png", "s2.png"):
        if (folder / name).exists():
            return f"{BASE_URL}/{post_id.lower()}/{name}"
    return FALLBACK


def main():
    print("Pulling sheet -> local DB...")
    pull()

    conn = sqlite3.connect(str(ROOT / "automation" / "data" / "sleepwise.db"))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """SELECT post_id FROM ig_queue
           WHERE LOWER(status) = 'pending'
             AND (slide_1_url IS NULL OR slide_1_url = '')
           ORDER BY post_id"""
    ).fetchall()
    conn.close()

    print(f"{len(rows)} PENDING rows with blank image_url\n")

    for row in rows:
        pid = row["post_id"]
        url = best_image_url(pid)
        set_field(pid, "slide_1_url", url)
        tag = "(fallback)" if url == FALLBACK else "(local image)"
        print(f"  {pid}: {url}  {tag}")

    print("\nPushing to Google Sheet...")
    push()
    print("\nDone. Sheet is updated.")
    print("Next: go to eu2.make.com -> Scenario 8993709 -> toggle ON.")


if __name__ == "__main__":
    main()
