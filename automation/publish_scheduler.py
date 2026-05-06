import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import gspread
import requests

# ── Constants ─────────────────────────────────────────────────────────────────
SPREADSHEET_ID = "1KeWK1xO5eiD2YbFe63Fx8sV9Vf6jUwi57h71fc8zb5o"
SHEET_NAME = "Content Calendar"
DATE_FORMAT = "%d-%m-%Y"
BASE_URL = "https://sleepwisereviews.com"

PROJECT_ROOT = Path(__file__).parent.parent
SCHEDULED_DIR = PROJECT_ROOT / "scheduled"
POSTS_DIR = PROJECT_ROOT / "posts"
SITEMAP_PATH = PROJECT_ROOT / "sitemap.xml"
INDEX_PATH = PROJECT_ROOT / "posts" / "INDEX.md"

# Column indices (0-based) matching sheet column order:
# publish_date | article_filename | article_title | category | status | published_at
COL_PUBLISH_DATE = 0
COL_FILENAME = 1
COL_TITLE = 2
COL_CATEGORY = 3
COL_STATUS = 4
COL_PUBLISHED_AT = 5


# ── Google Sheets auth ────────────────────────────────────────────────────────
def get_worksheet():
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not sa_json:
        print("ERROR: GOOGLE_SERVICE_ACCOUNT_JSON env var not set.")
        sys.exit(1)

    sa_dict = json.loads(sa_json)
    gc = gspread.service_account_from_dict(sa_dict)
    return gc.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)


# ── Sitemap update (string-based to preserve formatting) ─────────────────────
def append_to_sitemap(filename: str, today_str: str):
    if not SITEMAP_PATH.exists():
        print(f"  WARN: sitemap.xml not found at {SITEMAP_PATH}, skipping sitemap update.")
        return

    url = f"{BASE_URL}/posts/{filename}"
    new_entry = (
        f"\n  <url>\n"
        f"    <loc>{url}</loc>\n"
        f"    <lastmod>{today_str}</lastmod>\n"
        f"    <changefreq>monthly</changefreq>\n"
        f"    <priority>0.8</priority>\n"
        f"  </url>"
    )

    content = SITEMAP_PATH.read_text(encoding="utf-8")

    if url in content:
        print(f"  sitemap already contains {url}, skipping.")
        return

    updated = content.replace("</urlset>", new_entry + "\n</urlset>")
    SITEMAP_PATH.write_text(updated, encoding="utf-8")
    print(f"  sitemap.xml updated with {url}")


# ── INDEX.md append ───────────────────────────────────────────────────────────
def append_to_index(filename: str, title: str, category: str, pub_date_display: str):
    if not INDEX_PATH.exists():
        print(f"  WARN: posts/INDEX.md not found, skipping index update.")
        return

    content = INDEX_PATH.read_text(encoding="utf-8")

    # Find last row number to increment
    last_num = 0
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and not stripped.startswith("| #") and not stripped.startswith("|---"):
            parts = [p.strip() for p in stripped.split("|")]
            if len(parts) >= 2:
                try:
                    last_num = max(last_num, int(parts[1]))
                except ValueError:
                    pass

    next_num = last_num + 1
    new_row = f"| {next_num} | {filename} | {title} | {category} | {pub_date_display} |"

    updated = content.rstrip() + "\n" + new_row + "\n"
    INDEX_PATH.write_text(updated, encoding="utf-8")
    print(f"  INDEX.md updated (row {next_num}): {filename}")


# ── Telegram notification ─────────────────────────────────────────────────────
def send_telegram(title: str, filename: str, today_str: str):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")

    if not bot_token or not chat_id:
        print("  WARN: Telegram env vars not set, skipping notification.")
        return

    url_link = f"{BASE_URL}/posts/{filename}"
    text = (
        f"Published: <b>{title}</b>\n\n"
        f"URL: {url_link}\n"
        f"Date: {today_str}"
    )
    resp = requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
        timeout=15,
    )
    if resp.ok:
        print(f"  Telegram notification sent for: {title}")
    else:
        print(f"  WARN: Telegram notification failed: {resp.text}")


# ── Mark row as PUBLISHED in sheet ───────────────────────────────────────────
def mark_published(ws, sheet_row: int, today_str: str):
    # gspread rows are 1-based; row 1 is the header
    ws.update_cell(sheet_row, COL_STATUS + 1, "PUBLISHED")
    ws.update_cell(sheet_row, COL_PUBLISHED_AT + 1, today_str)


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    today = datetime.now(timezone.utc)
    today_sheet = today.strftime(DATE_FORMAT)       # DD-MM-YYYY for sheet matching
    today_iso = today.strftime("%Y-%m-%d")           # YYYY-MM-DD for sitemap/display
    today_display = today.strftime("%b %Y")          # e.g. "Apr 2026" for INDEX.md

    ws = get_worksheet()
    all_rows = ws.get_all_values()

    if not all_rows:
        print("No articles scheduled for today.")
        return

    # Row 0 is header; data starts at row 1 (sheet_row index 2 in gspread 1-based)
    header = all_rows[0]
    data_rows = all_rows[1:]

    published_count = 0

    for row_offset, row in enumerate(data_rows):
        # Pad row to ensure all columns exist
        while len(row) <= COL_PUBLISHED_AT:
            row.append("")

        publish_date = row[COL_PUBLISH_DATE].strip()
        status = row[COL_STATUS].strip().upper()
        filename = row[COL_FILENAME].strip()
        title = row[COL_TITLE].strip()
        category = row[COL_CATEGORY].strip()

        if publish_date != today_sheet or status != "PENDING":
            continue

        if not filename:
            print(f"  ERROR: row {row_offset + 2} has empty filename, skipping.")
            continue

        source = SCHEDULED_DIR / filename
        dest = POSTS_DIR / filename

        if not source.exists():
            print(f"  ERROR: /scheduled/{filename} not found, skipping.")
            continue

        print(f"Publishing: {filename}")

        # 1. Copy file with canonical tag injection
        POSTS_DIR.mkdir(parents=True, exist_ok=True)
        html = source.read_text(encoding="utf-8")
        canonical_url = f"{BASE_URL}/posts/{filename}"
        canonical_tag = f'<link rel="canonical" href="{canonical_url}" />'
        if 'rel="canonical"' not in html:
            # inject after <title> close tag if present, otherwise before </head>
            if "</title>" in html:
                html = html.replace("</title>", f"</title>\n  {canonical_tag}", 1)
            else:
                html = html.replace("</head>", f"  {canonical_tag}\n</head>", 1)
            print(f"  Injected canonical: {canonical_url}")
        dest.write_text(html, encoding="utf-8")
        print(f"  Copied to /posts/{filename}")

        # 2. Append to INDEX.md
        append_to_index(filename, title, category, today_display)

        # 3. Append to sitemap.xml
        append_to_sitemap(filename, today_iso)

        # 4. Mark PUBLISHED in sheet
        sheet_row = row_offset + 2  # +1 for header, +1 for 1-based gspread
        mark_published(ws, sheet_row, today_iso)
        print(f"  Marked PUBLISHED in sheet (row {sheet_row})")

        # 5. Send Telegram notification
        send_telegram(title, filename, today_iso)

        published_count += 1

    if published_count == 0:
        print("No articles scheduled for today.")
    else:
        print(f"Done. Published {published_count} article(s).")


if __name__ == "__main__":
    main()
