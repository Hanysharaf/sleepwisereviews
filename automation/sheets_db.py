"""
sheets_db.py
------------
Google Sheets <-> Local SQLite sync for SleepWise Reviews.
Google Sheet is the MASTER — conflicts always resolve in favour of the sheet.

Auth order (first match wins):
  1. automation/data/service_account.json  — service account, zero browser prompts
  2. automation/data/google_credentials.json + google_token.json — OAuth (token cached after first run)

Usage (CLI):
  python automation/sheets_db.py pull          # Sheet -> local DB (full sync)
  python automation/sheets_db.py push          # local DB -> Sheet (dirty rows only)
  python automation/sheets_db.py status        # show pending/dirty rows
  python automation/sheets_db.py set IG-002 status POSTED
  python automation/sheets_db.py set IG-010 slide_1_url https://...
  python automation/sheets_db.py get IG-002
  python automation/sheets_db.py list --status PENDING
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE            = Path(__file__).parent.parent
DATA_DIR        = BASE / "automation" / "data"
DB_PATH         = BASE / "automation" / "data" / "sleepwise.db"
SERVICE_ACCT    = DATA_DIR / "service_account.json"
OAUTH_CREDS     = DATA_DIR / "google_credentials.json"
OAUTH_TOKEN     = DATA_DIR / "google_token.json"

SPREADSHEET_ID  = "1KeWK1xO5eiD2YbFe63Fx8sV9Vf6jUwi57h71fc8zb5o"
SHEET_NAME      = "IG QUEUE"

# ── Column map: DB field -> sheet column index (0-based) ──────────────────────
COLUMNS = {
    "post_id":        0,   # A
    "scheduled_date": 1,   # B
    "content_type":   2,   # C
    "hook_title":     3,   # D
    "caption":        4,   # E
    "hashtags":       5,   # F
    "visual_prompt":  6,   # G
    "slide_1_url":    7,   # H
    "affiliate_link": 8,   # I
    "status":         9,   # J
    "posted_at":      10,  # K
    "post_url":       11,  # L
    "notes":          12,  # M
    "platform":       13,  # N
    "qa":             14,  # O
    "slide_2_url":    15,  # P
    "slide_3_url":    16,  # Q
    "slide_4_url":    17,  # R
    "slide_5_url":    18,  # S
}
MAX_COL = max(COLUMNS.values()) + 1   # columns needed per row


# ── DB setup ──────────────────────────────────────────────────────────────────
def get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db(conn: sqlite3.Connection):
    fields = ",\n    ".join(
        f"{col} TEXT" if col != "post_id" else f"{col} TEXT PRIMARY KEY"
        for col in COLUMNS
    )
    conn.executescript(f"""
        CREATE TABLE IF NOT EXISTS ig_queue (
            {fields},
            sheet_row   INTEGER,
            dirty       INTEGER DEFAULT 0,
            last_synced TEXT
        );
        CREATE TABLE IF NOT EXISTS sync_log (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            direction   TEXT,
            rows_affected INTEGER,
            ts          TEXT
        );
    """)
    conn.commit()


# ── Google Sheets auth ────────────────────────────────────────────────────────
def get_worksheet():
    import gspread

    if SERVICE_ACCT.exists():
        gc = gspread.service_account(filename=str(SERVICE_ACCT))
        print("[auth] service account")
    elif OAUTH_CREDS.exists():
        gc = gspread.oauth(
            credentials_filename=str(OAUTH_CREDS),
            authorized_user_filename=str(OAUTH_TOKEN),
        )
        print("[auth] OAuth token")
    else:
        sys.exit(
            "ERROR: No credentials found.\n"
            f"  Option A (recommended): place a service account JSON at:\n"
            f"    {SERVICE_ACCT}\n"
            f"  Option B: place OAuth desktop credentials at:\n"
            f"    {OAUTH_CREDS}\n"
            "  See README or the ig-sheets-db skill for setup instructions."
        )

    ws = gc.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    return ws


# ── Pull: Sheet -> DB ─────────────────────────────────────────────────────────
def pull(ws=None, verbose=True) -> int:
    if ws is None:
        ws = get_worksheet()

    all_values = ws.get_all_values()
    if not all_values:
        print("Sheet is empty.")
        return 0

    # Skip header row (row index 0 = row 1 in sheets)
    data_rows = all_values[1:]

    conn = get_conn()
    init_db(conn)

    upserted = 0
    col_keys = list(COLUMNS.keys())

    for sheet_row_idx, row in enumerate(data_rows, start=2):  # 2 = first data row
        # Pad row to at least MAX_COL columns
        while len(row) < MAX_COL:
            row.append("")

        post_id = row[COLUMNS["post_id"]].strip()
        if not post_id:
            continue

        values = {col: row[idx] for col, idx in COLUMNS.items()}
        values["sheet_row"]   = sheet_row_idx
        values["dirty"]       = 0
        values["last_synced"] = datetime.utcnow().isoformat()

        placeholders = ", ".join(f":{k}" for k in values)
        cols_sql     = ", ".join(values.keys())
        updates      = ", ".join(
            f"{k} = excluded.{k}"
            for k in values
            if k not in ("post_id", "dirty")  # don't overwrite dirty flag on pull
        )

        conn.execute(
            f"""INSERT INTO ig_queue ({cols_sql})
                VALUES ({placeholders})
                ON CONFLICT(post_id) DO UPDATE SET {updates}""",
            values,
        )
        upserted += 1

    conn.execute(
        "INSERT INTO sync_log (direction, rows_affected, ts) VALUES (?,?,?)",
        ("pull", upserted, datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()

    if verbose:
        print(f"[pull] {upserted} rows synced from sheet -> local DB")
    return upserted


# ── Push: DB -> Sheet (dirty rows only) ───────────────────────────────────────
def push(ws=None, verbose=True) -> int:
    conn = get_conn()
    init_db(conn)
    dirty = conn.execute(
        "SELECT * FROM ig_queue WHERE dirty = 1"
    ).fetchall()

    if not dirty:
        if verbose:
            print("[push] nothing to push (no dirty rows)")
        conn.close()
        return 0

    if ws is None:
        ws = get_worksheet()

    pushed = 0
    for row in dirty:
        sheet_row = row["sheet_row"]
        if not sheet_row:
            print(f"  WARN {row['post_id']} has no sheet_row — skipping")
            continue

        for col, idx in COLUMNS.items():
            if col == "post_id":
                continue
            val = row[col] or ""
            ws.update_cell(sheet_row, idx + 1, val)  # gspread is 1-based

        conn.execute(
            "UPDATE ig_queue SET dirty=0, last_synced=? WHERE post_id=?",
            (datetime.utcnow().isoformat(), row["post_id"]),
        )
        pushed += 1
        if verbose:
            print(f"  pushed {row['post_id']} (row {sheet_row})")

    conn.execute(
        "INSERT INTO sync_log (direction, rows_affected, ts) VALUES (?,?,?)",
        ("push", pushed, datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()
    if verbose:
        print(f"[push] {pushed} rows pushed to sheet")
    return pushed


# ── Local helpers ─────────────────────────────────────────────────────────────
def set_field(post_id: str, field: str, value: str):
    """Update a field locally and mark the row dirty for next push."""
    if field not in COLUMNS and field not in ("sheet_row", "dirty"):
        valid = list(COLUMNS.keys())
        sys.exit(f"Unknown field '{field}'. Valid: {valid}")

    conn = get_conn()
    init_db(conn)
    rows = conn.execute(
        "SELECT post_id FROM ig_queue WHERE LOWER(post_id)=LOWER(?)",
        (post_id,)
    ).fetchall()

    if not rows:
        sys.exit(f"Post '{post_id}' not found in local DB. Run `pull` first.")

    conn.execute(
        f"UPDATE ig_queue SET {field}=?, dirty=1 WHERE LOWER(post_id)=LOWER(?)",
        (value, post_id),
    )
    conn.commit()
    conn.close()
    print(f"[set] {post_id}.{field} = {value!r}  (dirty — run push to sync)")


def get_post(post_id: str):
    conn = get_conn()
    init_db(conn)
    row = conn.execute(
        "SELECT * FROM ig_queue WHERE LOWER(post_id)=LOWER(?)", (post_id,)
    ).fetchone()
    conn.close()
    if not row:
        sys.exit(f"Post '{post_id}' not found. Run `pull` first.")
    for key in row.keys():
        print(f"  {key:<20} {row[key]}")


def list_posts(status: str = None, content_type: str = None, dirty_only: bool = False):
    conn = get_conn()
    init_db(conn)
    clauses, params = [], []
    if status:
        clauses.append("LOWER(status)=LOWER(?)")
        params.append(status)
    if content_type:
        clauses.append("LOWER(content_type)=LOWER(?)")
        params.append(content_type)
    if dirty_only:
        clauses.append("dirty=1")
    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    rows = conn.execute(
        f"SELECT post_id, scheduled_date, content_type, status, dirty FROM ig_queue {where} ORDER BY post_id",
        params,
    ).fetchall()
    conn.close()

    if not rows:
        print("No rows match.")
        return

    print(f"{'ID':<10} {'Date':<12} {'Type':<14} {'Status':<10} {'Dirty'}")
    print("-" * 60)
    for r in rows:
        dirty_flag = "*" if r["dirty"] else ""
        print(f"{r['post_id']:<10} {r['scheduled_date'] or '':<12} {r['content_type'] or '':<14} {r['status'] or '':<10} {dirty_flag}")


def status_report():
    conn = get_conn()
    init_db(conn)
    total   = conn.execute("SELECT COUNT(*) FROM ig_queue").fetchone()[0]
    pending = conn.execute("SELECT COUNT(*) FROM ig_queue WHERE LOWER(status)='pending'").fetchone()[0]
    posted  = conn.execute("SELECT COUNT(*) FROM ig_queue WHERE LOWER(status)='posted'").fetchone()[0]
    dirty   = conn.execute("SELECT COUNT(*) FROM ig_queue WHERE dirty=1").fetchone()[0]
    last    = conn.execute("SELECT ts FROM sync_log ORDER BY id DESC LIMIT 1").fetchone()
    conn.close()

    print(f"DB: {DB_PATH}")
    print(f"  Total rows : {total}")
    print(f"  PENDING    : {pending}")
    print(f"  POSTED     : {posted}")
    print(f"  Dirty (pending push): {dirty}")
    print(f"  Last sync  : {last['ts'] if last else 'never'}")


# ── CLI ───────────────────────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser(description="SleepWise Reviews — Sheet <-> DB sync")
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("pull", help="Sync sheet -> local DB (master wins)")
    sub.add_parser("push", help="Push dirty local rows -> sheet")
    sub.add_parser("status", help="Show DB stats and dirty rows")

    sp_set = sub.add_parser("set", help="Update a field locally (marks dirty)")
    sp_set.add_argument("post_id")
    sp_set.add_argument("field")
    sp_set.add_argument("value")

    sp_get = sub.add_parser("get", help="Show all fields for a post")
    sp_get.add_argument("post_id")

    sp_list = sub.add_parser("list", help="List posts with optional filters")
    sp_list.add_argument("--status",       default=None)
    sp_list.add_argument("--type",         default=None, dest="content_type")
    sp_list.add_argument("--dirty",        action="store_true")

    args = p.parse_args()

    if args.cmd == "pull":
        pull()
    elif args.cmd == "push":
        push()
    elif args.cmd == "status":
        status_report()
    elif args.cmd == "set":
        set_field(args.post_id, args.field, args.value)
    elif args.cmd == "get":
        get_post(args.post_id)
    elif args.cmd == "list":
        list_posts(status=args.status, content_type=args.content_type, dirty_only=args.dirty)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
