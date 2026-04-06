"""
sync_prompts_to_sheet.py
Parse ig_image_prompts.txt -> extract PROMPT per post_id -> push photo prompts
to sheet column G.

Overwrites if col G is empty OR contains a video/reel script (detected by
signature patterns like "30-sec", "0-3s:", "b-roll", "vertical").

Also reports whether s1.png already exists for each post so you know which
images still need to be generated.

Usage:
    python sync_prompts_to_sheet.py          # dry-run, print diff table
    python sync_prompts_to_sheet.py --apply  # write to sheet
"""

import argparse
import re
import sys
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

SHEET_ID = "1KeWK1xO5eiD2YbFe63Fx8sV9Vf6jUwi57h71fc8zb5o"
SHEET_NAME = "IG QUEUE"
SERVICE_ACCOUNT_PATH = (
    r"C:\Users\Hany\OneDrive - Petroleum Air Services"
    r"\Projects\SleepReviewes\automation\data\service_account.json"
)
PROMPTS_PATH = (
    r"C:\Users\Hany\OneDrive - Petroleum Air Services"
    r"\Projects\SleepReviewes\automation\data\ig_image_prompts.txt"
)
IMAGES_DIR = Path(
    r"O:\MyFiles\Projects\SleepReviewes\images\instagram"
)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

COL_POST_ID = 0
COL_VISUAL_PROMPT = 6  # column G

# Patterns that identify a video/reel script rather than a photo prompt
VIDEO_SCRIPT_PATTERNS = [
    r"\b30-sec\b",
    r"\b0-3s\b",
    r"\bb-roll\b",
    r"\bvertical\b",
    r"\bCTA card\b",
    r"\bhook text overlay\b",
]
_video_re = re.compile("|".join(VIDEO_SCRIPT_PATTERNS), re.IGNORECASE)


def is_video_script(text: str) -> bool:
    return bool(_video_re.search(text))


def s1_exists(post_id: str) -> bool:
    return (IMAGES_DIR / post_id.lower() / "s1.png").exists()


def get_sheet():
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_PATH, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)


def parse_prompts(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        content = f.read()

    blocks = re.split(r"-{20,}", content)
    prompts = {}
    post_id_re = re.compile(r"^(IG-\d+)\s*\|", re.MULTILINE)
    prompt_re = re.compile(r"^PROMPT:\s*(.+)", re.MULTILINE)

    for block in blocks:
        block = block.strip()
        if not block:
            continue
        id_match = post_id_re.search(block)
        prompt_match = prompt_re.search(block)
        if id_match and prompt_match:
            post_id = id_match.group(1).upper()
            prompts[post_id] = prompt_match.group(1).strip()

    return prompts


def main(apply: bool) -> None:
    sys.stdout.reconfigure(encoding="utf-8")

    file_prompts = parse_prompts(PROMPTS_PATH)
    print(f"Parsed {len(file_prompts)} entries from prompts file.\n")

    sheet = get_sheet()
    all_values = sheet.get_all_values()
    data_rows = all_values[1:]

    sheet_map = {}
    for i, row in enumerate(data_rows):
        post_id = row[COL_POST_ID].strip().upper() if len(row) > COL_POST_ID else ""
        visual_prompt = row[COL_VISUAL_PROMPT].strip() if len(row) > COL_VISUAL_PROMPT else ""
        if post_id:
            sheet_map[post_id] = (i + 2, visual_prompt)

    updates = []

    col_w = [10, 10, 13, 12, 12, 22]
    header = (
        f"{'POST_ID':<{col_w[0]}} "
        f"{'S1_EXISTS':<{col_w[1]}} "
        f"{'FILE_PROMPT':<{col_w[2]}} "
        f"{'SHEET_PROMPT':<{col_w[3]}} "
        f"{'VIDEO_SCRIPT':<{col_w[4]}} "
        f"ACTION"
    )
    print(header)
    print("-" * len(header))

    needs_generation = []

    for post_id in sorted(file_prompts.keys()):
        photo_built = s1_exists(post_id)
        file_has = True

        if post_id not in sheet_map:
            print(
                f"{post_id:<{col_w[0]}} "
                f"{str(photo_built):<{col_w[1]}} "
                f"{str(file_has):<{col_w[2]}} "
                f"{'False':<{col_w[3]}} "
                f"{'?':<{col_w[4]}} "
                f"skip (not in sheet)"
            )
            continue

        sheet_row, current = sheet_map[post_id]
        sheet_has = bool(current)
        video = is_video_script(current) if sheet_has else False

        needs_update = (not sheet_has) or video

        if needs_update:
            action = "WILL UPDATE" if apply else "NEEDS UPDATE"
            updates.append((sheet_row, file_prompts[post_id]))
        else:
            action = "skip (photo prompt ok)"

        if not photo_built:
            needs_generation.append(post_id)

        print(
            f"{post_id:<{col_w[0]}} "
            f"{str(photo_built):<{col_w[1]}} "
            f"{str(file_has):<{col_w[2]}} "
            f"{str(sheet_has):<{col_w[3]}} "
            f"{str(video):<{col_w[4]}} "
            f"{action}"
        )

    print(f"\nPrompts needing update : {len(updates)}")
    print(f"Posts needing s1 gen   : {len(needs_generation)}")
    if needs_generation:
        print("  -> " + ", ".join(needs_generation))

    if not updates:
        print("\nNothing to update in sheet.")
    elif apply:
        batch = [
            {"range": f"G{row}", "values": [[prompt]]}
            for row, prompt in updates
        ]
        sheet.batch_update(batch)
        print(f"\nAPPLIED: {len(updates)} prompts written to column G.")
    else:
        print("\nDRY RUN: pass --apply to write changes.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync photo prompts from text file to sheet")
    parser.add_argument("--apply", action="store_true", help="Write changes to sheet")
    args = parser.parse_args()
    main(apply=args.apply)
