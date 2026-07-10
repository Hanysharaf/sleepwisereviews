"""
sync_covers_to_sheet.py
=======================
Reads sheet_pending_updates.json from GitHub (written by the cloud routine)
and fills the Google Sheet with cover (col H) and slide (cols P-S) URLs.

Also backfills any posts where slides exist in GitHub but sheet is empty.

Usage:
    python automation/scripts/sync_covers_to_sheet.py           # dry-run
    python automation/scripts/sync_covers_to_sheet.py --apply   # write to sheet
"""

import argparse
import json
import os
import sys
from pathlib import Path

import requests
import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

BASE_DIR  = Path(__file__).resolve().parent.parent.parent
AUTO_DIR  = BASE_DIR / "automation"
SA_FILE   = r"C:\Users\Hany\OneDrive - Petroleum Air Services\Projects\SleepReviewes\automation\data\service_account.json"
SHEET_ID  = "1KeWK1xO5eiD2YbFe63Fx8sV9Vf6jUwi57h71fc8zb5o"
SHEET_NAME = "IG QUEUE"

GITHUB_RAW  = "https://raw.githubusercontent.com/Hanysharaf/sleepwisereviews/main/images/instagram"
GITHUB_API  = "https://api.github.com/repos/Hanysharaf/sleepwisereviews/contents/images/instagram"
MANIFEST_URL = "https://raw.githubusercontent.com/Hanysharaf/sleepwisereviews/main/automation/data/sheet_pending_updates.json"

load_dotenv(AUTO_DIR / ".env")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")


def get_sheet():
    creds = Credentials.from_service_account_file(SA_FILE, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    gc = gspread.authorize(creds)
    return gc.open_by_key(SHEET_ID).worksheet(SHEET_NAME)


def check_github_file_exists(pid_lower, filename):
    url = f"{GITHUB_API}/{pid_lower}/{filename}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    r = requests.get(url, headers=headers, timeout=15)
    return r.status_code == 200


def build_updates_from_github(sheet_rows):
    """For ig-046 to ig-091: check GitHub for existing files and build URL map."""
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    updates = {}

    for pid, h_val, p_val in sheet_rows:
        num = int(pid.split("-")[1])
        if num < 46:
            continue
        pid_lower = pid.lower()

        entry = {}

        # Check cover
        if not h_val:
            cover_url = f"{GITHUB_API}/{pid_lower}/{pid_lower}-cover.png"
            r = requests.get(cover_url, headers=headers, timeout=15)
            if r.status_code == 200:
                entry["cover"] = f"{GITHUB_RAW}/{pid_lower}/{pid_lower}-cover.png"

        # Check slides
        if not p_val:
            slides_found = {}
            for sn in range(2, 6):
                slide_url = f"{GITHUB_API}/{pid_lower}/s{sn}.png"
                r = requests.get(slide_url, headers=headers, timeout=15)
                if r.status_code == 200:
                    slides_found[f"s{sn}"] = f"{GITHUB_RAW}/{pid_lower}/s{sn}.png"
            if slides_found:
                entry.update(slides_found)

        if entry:
            updates[pid] = entry

    return updates


def apply_to_sheet(ws, updates, dry_run):
    all_rows = ws.get_all_values()
    batch = []
    applied = []

    for i, row in enumerate(all_rows[1:], start=2):
        if not row:
            continue
        pid = row[0].strip().upper()
        if pid not in updates:
            continue

        entry = updates[pid]
        if "cover" in entry:
            batch.append({"range": f"H{i}", "values": [[entry["cover"]]]})
        if "s2" in entry:
            batch.append({"range": f"P{i}", "values": [[entry["s2"]]]})
        if "s3" in entry:
            batch.append({"range": f"Q{i}", "values": [[entry["s3"]]]})
        if "s4" in entry:
            batch.append({"range": f"R{i}", "values": [[entry["s4"]]]})
        if "s5" in entry:
            batch.append({"range": f"S{i}", "values": [[entry["s5"]]]})
        applied.append(pid)

    if dry_run:
        print(f"DRY-RUN: would update {len(applied)} rows: {applied}")
        for pid, entry in updates.items():
            print(f"  {pid}: {list(entry.keys())}")
    else:
        if batch:
            ws.batch_update(batch)
            print(f"Applied {len(applied)} rows to sheet: {applied}")
        else:
            print("Nothing to apply.")

    return applied


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--manifest-only", action="store_true", help="Only apply manifest from GitHub, skip full scan")
    args = parser.parse_args()

    dry_run = not args.apply

    ws = get_sheet()
    all_rows = ws.get_all_values()
    sheet_rows = []
    for row in all_rows[1:]:
        if row and row[0].strip().upper().startswith("IG-"):
            pid = row[0].strip().upper()
            h   = row[7]  if len(row) > 7  else ""
            p   = row[15] if len(row) > 15 else ""
            sheet_rows.append((pid, h, p))

    updates = {}

    # Phase 1: load manifest from GitHub (if exists)
    print("Checking for sheet_pending_updates.json manifest...")
    r = requests.get(MANIFEST_URL, timeout=15)
    if r.status_code == 200:
        manifest = r.json()
        print(f"Manifest found: {len(manifest)} posts")
        for pid, entry in manifest.items():
            updates[pid] = {}
            if "cover" in entry:
                updates[pid]["cover"] = entry["cover"]
            for sn in range(2, 6):
                key = f"s{sn}"
                if key in entry:
                    updates[pid][key] = entry[key]
    else:
        print("No manifest found — doing full GitHub scan")

    if not args.manifest_only:
        # Phase 2: full scan for any missing URLs not in manifest
        print("Scanning GitHub for missing covers/slides...")
        scan_updates = build_updates_from_github(sheet_rows)
        for pid, entry in scan_updates.items():
            if pid not in updates:
                updates[pid] = entry
            else:
                # merge — manifest takes priority for cover
                for k, v in entry.items():
                    if k not in updates[pid]:
                        updates[pid][k] = v

    print(f"\nTotal updates to apply: {len(updates)} posts")
    apply_to_sheet(ws, updates, dry_run)

    if dry_run:
        print("\nRun with --apply to write to sheet.")


if __name__ == "__main__":
    main()
