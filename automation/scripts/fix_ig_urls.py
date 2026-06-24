"""
fix_ig_urls.py — Fills slide URLs for IG-032..IG-059 in Google Sheet.

Fills columns:
  H  = Image URL      (slide 1 / main image)
  P  = Slide 2 URL
  Q  = Slide 3 URL
  R  = Slide 4 URL
  S  = Slide 5 URL

IG-032..IG-059: images exist in repo (s2-s5 built; ig-032 also has cover photo).
IG-060..IG-090: no images yet — skipped (build them first, then re-run).

Run from repo root:
    python automation/scripts/fix_ig_urls.py

Requires Google credentials in automation/data/:
  Option A: service_account.json
  Option B: google_credentials.json + google_token.json
"""

import sys
import sqlite3
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "automation"))

from sheets_db import pull, push, set_field

BASE       = "https://raw.githubusercontent.com/Hanysharaf/sleepwisereviews/main/images/instagram"
IMG_DIR    = ROOT / "images" / "instagram"


def slide_urls(post_id: str):
    """Return (s1, s2, s3, s4, s5) URLs. None if folder missing."""
    folder = IMG_DIR / post_id.lower()
    if not folder.exists():
        return None

    base = f"{BASE}/{post_id.lower()}"

    # Slide 1: prefer any *cover* PNG, then s1.png, then s2.png
    s1_file = None
    for p in sorted(folder.glob("*cover*.png")):
        s1_file = p.name
        break
    if not s1_file:
        for name in ("s1.png", "s2.png"):
            if (folder / name).exists():
                s1_file = name
                break
    if not s1_file:
        return None

    return (
        f"{base}/{s1_file}",
        f"{base}/s2.png" if (folder / "s2.png").exists() else None,
        f"{base}/s3.png" if (folder / "s3.png").exists() else None,
        f"{base}/s4.png" if (folder / "s4.png").exists() else None,
        f"{base}/s5.png" if (folder / "s5.png").exists() else None,
    )


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

    print(f"{len(rows)} PENDING rows with blank image URL\n")

    updated = 0
    skipped = 0

    for row in rows:
        pid = row["post_id"]
        urls = slide_urls(pid)

        if urls is None:
            print(f"  {pid}: no local images — skipped (generate images first)")
            skipped += 1
            continue

        s1, s2, s3, s4, s5 = urls
        set_field(pid, "slide_1_url", s1 or "")
        set_field(pid, "slide_2_url", s2 or "")
        set_field(pid, "slide_3_url", s3 or "")
        set_field(pid, "slide_4_url", s4 or "")
        set_field(pid, "slide_5_url", s5 or "")
        print(f"  {pid}: {s1}")
        updated += 1

    print(f"\nPushing {updated} rows to Google Sheet...")
    push()
    print(f"Done. {updated} updated, {skipped} skipped.")
    print("\nNext: reactivate Make.com scenario 8993709 on eu2.make.com")


if __name__ == "__main__":
    main()
