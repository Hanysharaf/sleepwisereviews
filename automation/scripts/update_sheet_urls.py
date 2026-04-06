"""
update_sheet_urls.py
Push GitHub slide URLs + QA=PASS to the Google Sheet for built posts.

For each post: sets col H (Image URL/s1), P-S (s2-s5), and col O (QA=PASS).

Usage:
    python update_sheet_urls.py              # dry-run
    python update_sheet_urls.py --apply      # write to sheet
    python update_sheet_urls.py --post IG-005 --apply  # single post
"""

import argparse
import sys
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

SHEET_ID    = "1KeWK1xO5eiD2YbFe63Fx8sV9Vf6jUwi57h71fc8zb5o"
SHEET_NAME  = "IG QUEUE"
SERVICE_ACCOUNT_PATH = (
    r"C:\Users\Hany\OneDrive - Petroleum Air Services"
    r"\Projects\SleepReviewes\automation\data\service_account.json"
)

GITHUB_RAW = "https://raw.githubusercontent.com/Hanysharaf/sleepwisereviews/main/images/instagram"

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Column indices (0-based)
COL_POST_ID   = 0   # A
COL_IMAGE_URL = 7   # H  — slide 1 (MUST stay "Image URL" for Make.com)
COL_QA        = 14  # O
COL_SLIDE2    = 15  # P
COL_SLIDE3    = 16  # Q
COL_SLIDE4    = 17  # R
COL_SLIDE5    = 18  # S

# Posts that are already done — skip
SKIP_POSTS = {"IG-001", "IG-002", "IG-010"}


def get_sheet():
    creds  = Credentials.from_service_account_file(SERVICE_ACCOUNT_PATH, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)


def github_url(post_id: str, slide: int) -> str:
    pid_lower = post_id.lower()
    return f"{GITHUB_RAW}/{pid_lower}/s{slide}.png"


def main(apply: bool, post_filter: str = None):
    sys.stdout.reconfigure(encoding="utf-8")

    sheet      = get_sheet()
    all_values = sheet.get_all_values()
    data_rows  = all_values[1:]   # skip header

    # Build post_id → sheet row number (1-based including header)
    sheet_map = {}
    for i, row in enumerate(data_rows):
        pid = row[COL_POST_ID].strip().upper() if len(row) > COL_POST_ID else ""
        if pid:
            sheet_map[pid] = i + 2   # +1 for header, +1 for 1-based

    updates = []   # list of {"range": "XN", "values": [[v]]}

    print(f"{'POST_ID':<10} {'ROW':<5} {'ACTION'}")
    print("-" * 40)

    for pid, sheet_row in sorted(sheet_map.items()):
        if pid in SKIP_POSTS:
            continue
        if post_filter and pid != post_filter.upper():
            continue
        # Only update posts we have slides for (IG-003 to IG-031)
        try:
            num = int(pid.split("-")[1])
        except (IndexError, ValueError):
            continue
        if num < 3 or num > 31:
            continue

        action = "WILL UPDATE" if apply else "NEEDS UPDATE"
        print(f"{pid:<10} {sheet_row:<5} {action}")

        updates.append({"range": f"H{sheet_row}", "values": [[github_url(pid, 1)]]})
        updates.append({"range": f"P{sheet_row}", "values": [[github_url(pid, 2)]]})
        updates.append({"range": f"Q{sheet_row}", "values": [[github_url(pid, 3)]]})
        updates.append({"range": f"R{sheet_row}", "values": [[github_url(pid, 4)]]})
        updates.append({"range": f"S{sheet_row}", "values": [[github_url(pid, 5)]]})
        updates.append({"range": f"O{sheet_row}", "values": [["PASS"]]})

    print(f"\n{len(updates) // 6} posts to update ({len(updates)} cells)")

    if not updates:
        print("Nothing to update.")
        return

    if apply:
        sheet.batch_update(updates)
        print("APPLIED.")
    else:
        print("DRY RUN — pass --apply to write.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--post", help="Single post only, e.g. IG-005")
    args = parser.parse_args()
    main(apply=args.apply, post_filter=args.post)
