"""
fix_ig_handle_batch.py — One-shot batched fix for the broken @sleepwisereviews
handle in the IG QUEUE Caption column (should be @sleepwise.reviews, the real
account). sheets_db.py's push() writes one API call per column per row, which
blew the Sheets write-quota on 59 rows x 18 cols. This does it in a single
batch_update call instead.

Run from repo root:
    python automation/scripts/fix_ig_handle_batch.py
"""

import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "automation"))

from sheets_db import get_worksheet, DB_PATH, COLUMNS

CAPTION_COL_LETTER = "E"  # matches COLUMNS["caption"] = 4 (0-based) -> E (1-based)
assert COLUMNS["caption"] == 4


def main():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT post_id, sheet_row, caption FROM ig_queue WHERE dirty = 1"
    ).fetchall()

    if not rows:
        print("Nothing dirty — nothing to push.")
        return

    print(f"{len(rows)} dirty rows to push (caption column only)")

    ws = get_worksheet()
    data = [
        {"range": f"{CAPTION_COL_LETTER}{r['sheet_row']}", "values": [[r["caption"]]]}
        for r in rows
        if r["sheet_row"]
    ]

    ws.batch_update(data)
    print(f"[batch push] wrote {len(data)} caption cells in 1 API call")

    ids = [r["post_id"] for r in rows]
    conn.execute(
        f"UPDATE ig_queue SET dirty = 0 WHERE post_id IN ({','.join('?' * len(ids))})",
        ids,
    )
    conn.commit()
    conn.close()
    print("Local DB marked clean.")


if __name__ == "__main__":
    main()
