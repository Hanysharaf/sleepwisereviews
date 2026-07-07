"""
fix_and_generate_covers.py
==========================
Phase 1 (--range 46 59): Generate missing s1.png + build ig-NNN-cover.png + upload to GitHub + update sheet col H
Phase 2 (--range 60 74): Full pipeline for new posts (s1 + cover + s2-s5 + upload + update sheet)

Usage:
    python automation/scripts/fix_and_generate_covers.py --range 46 59
    python automation/scripts/fix_and_generate_covers.py --range 60 74
    python automation/scripts/fix_and_generate_covers.py --range 46 59 --dry-run
"""

import argparse
import base64
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR     = Path(__file__).resolve().parent.parent.parent
AUTO_DIR     = BASE_DIR / "automation"
IMAGES_DIR   = BASE_DIR / "images" / "instagram"
QUEUE_FILE   = AUTO_DIR / "data" / "photo_queue.txt"
CONTENT_JSON = AUTO_DIR / "data" / "slide_content.json"
SA_FILE      = r"C:\Users\Hany\OneDrive - Petroleum Air Services\Projects\SleepReviewes\automation\data\service_account.json"

load_dotenv(AUTO_DIR / ".env")

GITHUB_TOKEN  = os.getenv("GITHUB_TOKEN", "")
GEMINI_KEY    = os.getenv("GOOGLE_AI_API_KEY", "")
GITHUB_REPO   = "Hanysharaf/sleepwisereviews"
GITHUB_RAW    = "https://raw.githubusercontent.com/Hanysharaf/sleepwisereviews/main/images/instagram"
GITHUB_API    = "https://api.github.com"
GEMINI_URL    = "https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-fast-generate-001:predict"
SHEET_ID      = "1KeWK1xO5eiD2YbFe63Fx8sV9Vf6jUwi57h71fc8zb5o"
SHEET_NAME    = "IG QUEUE"

sys.path.insert(0, str(AUTO_DIR))
from build_carousel import add_hook_overlay, make_point_slide, make_cta_slide, IMAGES_DIR as _


# ── Helpers ────────────────────────────────────────────────────────────────────

def parse_queue(path: Path) -> dict:
    entries = {}
    current_id = None
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        m = re.match(r"^IG-(\d+)$", line)
        if m:
            current_id = int(m.group(1))
            entries[current_id] = {}
        elif current_id and line.startswith("PROMPT:"):
            entries[current_id]["prompt"] = line.split(":", 1)[1].strip()
    return entries


def generate_imagen(prompt: str) -> bytes:
    resp = requests.post(
        GEMINI_URL,
        params={"key": GEMINI_KEY},
        json={"instances": [{"prompt": prompt}], "parameters": {"sampleCount": 1, "aspectRatio": "1:1"}},
        timeout=90,
    )
    resp.raise_for_status()
    predictions = resp.json().get("predictions", [])
    if not predictions:
        raise ValueError("Imagen returned no predictions")
    return base64.b64decode(predictions[0]["bytesBase64Encoded"])


def github_upload(rel_path: str, image_bytes: bytes) -> str:
    api_url = f"{GITHUB_API}/repos/{GITHUB_REPO}/contents/{rel_path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    sha = None
    check = requests.get(api_url, headers=headers, timeout=30)
    if check.status_code == 200:
        sha = check.json().get("sha")
    payload = {
        "message": f"feat: add cover {rel_path.split('/')[-1]}",
        "content": base64.b64encode(image_bytes).decode("utf-8"),
    }
    if sha:
        payload["sha"] = sha
    r = requests.put(api_url, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    return f"{GITHUB_RAW}/{'/'.join(rel_path.split('/')[2:])}"


def get_sheet():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(SA_FILE, scopes=scopes)
    gc = gspread.authorize(creds)
    return gc.open_by_key(SHEET_ID).worksheet(SHEET_NAME)


def update_sheet_row(ws, post_id: str, h_url: str, p_url: str = None, q_url: str = None, r_url: str = None, s_url: str = None):
    all_rows = ws.get_all_values()
    for i, row in enumerate(all_rows[1:], start=2):
        if row and row[0].strip().upper() == post_id.upper():
            updates = [{"range": f"H{i}", "values": [[h_url]]}]
            if p_url:
                updates.append({"range": f"P{i}", "values": [[p_url]]})
            if q_url:
                updates.append({"range": f"Q{i}", "values": [[q_url]]})
            if r_url:
                updates.append({"range": f"R{i}", "values": [[r_url]]})
            if s_url:
                updates.append({"range": f"S{i}", "values": [[s_url]]})
            ws.batch_update(updates)
            print(f"  Sheet updated: {post_id} row {i}")
            return
    print(f"  WARNING: {post_id} not found in sheet")


# ── Core pipeline ──────────────────────────────────────────────────────────────

def process_post(num: int, queue: dict, content: dict, ws, dry_run: bool, build_slides: bool) -> bool:
    pid = f"IG-{num:03d}"
    pid_lower = pid.lower()
    folder = IMAGES_DIR / pid_lower
    folder.mkdir(parents=True, exist_ok=True)

    s1_path   = folder / "s1.png"
    s1_bg     = folder / "s1_bg.png"
    cover_path = folder / f"{pid_lower}-cover.png"

    print(f"\n>> {pid}")

    # Step 1: Generate lifestyle photo if needed
    if not s1_bg.exists() and not s1_path.exists():
        if num not in queue:
            print(f"  SKIP — no prompt in photo_queue.txt")
            return False
        prompt = queue[num].get("prompt", "")
        if dry_run:
            print(f"  DRY-RUN: would generate s1.png")
            print(f"  Prompt: {prompt[:80]}...")
            return True
        print(f"  Generating s1.png via Imagen 3...")
        try:
            img_bytes = generate_imagen(prompt)
            s1_path.write_bytes(img_bytes)
            print(f"  s1.png saved ({len(img_bytes)//1024}KB)")
            time.sleep(4)
        except Exception as e:
            print(f"  FAILED: {e}")
            return False
    else:
        print(f"  s1.png already exists — skip generation")

    # Step 2: Preserve clean copy then apply hook overlay
    if not s1_bg.exists() and s1_path.exists():
        shutil.copy2(s1_path, s1_bg)
        print(f"  Saved s1_bg.png (clean copy)")

    if pid_lower not in content:
        print(f"  SKIP — no content in slide_content.json")
        return False

    entry = content[pid_lower.upper()]
    hook   = entry["hook"]
    points = entry["points"]
    cta    = entry.get("cta", "Full review -> sleepwisereviews.com")

    print(f"  Applying hook overlay...")
    add_hook_overlay(pid_lower, hook)

    # Step 3: Save as cover file (copy s1.png -> ig-NNN-cover.png)
    if s1_path.exists():
        shutil.copy2(s1_path, cover_path)
        print(f"  Cover saved: {cover_path.name}")

    # Step 4: Build slides s2-s5 if requested
    if build_slides:
        for i, pt in enumerate(points, start=2):
            make_point_slide(pid_lower, i, pt)
            print(f"  s{i}: built")
        make_cta_slide(pid_lower, cta)
        print(f"  s5: CTA built")

    if dry_run:
        print(f"  DRY-RUN: would upload cover + slides to GitHub")
        return True

    # Step 5: Upload cover to GitHub
    cover_bytes = cover_path.read_bytes()
    cover_rel   = f"images/instagram/{pid_lower}/{pid_lower}-cover.png"
    print(f"  Uploading cover to GitHub...")
    cover_url = github_upload(cover_rel, cover_bytes)
    print(f"  -> {cover_url}")

    # Step 6: Upload slides if built
    p_url = q_url = r_url = s_url = None
    if build_slides:
        for slide_n, attr in [(2, 'p'), (3, 'q'), (4, 'r'), (5, 's')]:
            slide_path = folder / f"s{slide_n}.png"
            if slide_path.exists():
                slide_rel = f"images/instagram/{pid_lower}/s{slide_n}.png"
                print(f"  Uploading s{slide_n}.png...")
                slide_url = github_upload(slide_rel, slide_path.read_bytes())
                if attr == 'p': p_url = slide_url
                elif attr == 'q': q_url = slide_url
                elif attr == 'r': r_url = slide_url
                elif attr == 's': s_url = slide_url
                time.sleep(1)

    # Step 7: Update sheet
    update_sheet_row(ws, pid, cover_url, p_url, q_url, r_url, s_url)
    return True


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser()
    parser.add_argument("--range", nargs=2, type=int, metavar=("START", "END"), default=[46, 59])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    start, end = args.range
    build_slides = (start >= 60)  # ig-046..059 already have slides; ig-060+ need them built

    print(f"Processing ig-{start:03d} to ig-{end:03d} | build_slides={build_slides} | dry_run={args.dry_run}")

    queue   = parse_queue(QUEUE_FILE)
    content = json.loads(CONTENT_JSON.read_text(encoding="utf-8"))
    ws      = get_sheet()

    done = 0
    failed = []
    for num in range(start, end + 1):
        ok = process_post(num, queue, content, ws, args.dry_run, build_slides)
        if ok:
            done += 1
        else:
            failed.append(f"ig-{num:03d}")

    print(f"\n{'='*50}")
    print(f"Done: {done} | Failed: {len(failed)}")
    if failed:
        print(f"Failed: {failed}")


if __name__ == "__main__":
    main()
