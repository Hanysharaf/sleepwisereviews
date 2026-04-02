#!/usr/bin/env python3
"""
generate_ig_images.py — DALL-E 3 image generator for the Instagram queue.

Fully automated pipeline:
  1. Reads IG QUEUE from Google Sheets
  2. Generates a DALL-E 3 advertising lifestyle photo per post
  3. Uploads each image directly to GitHub (no manual git push needed)
  4. Writes the live GitHub Pages URL back to column H in the sheet
  5. n8n workflow then picks up the URL and posts to Instagram

SETUP (one-time, ~5 minutes):
  ① Install dependencies:
       pip install -r requirements.txt

  ② Image generation key is already set (Google AI Studio GOOGLE_AI_API_KEY in .env).
     Optional: add OPENAI_API_KEY for faster batch (all 90 in 20 min vs 6 days).

  ③ Google Sheets access — 3 clicks to get a credentials file:
       a. Go to: console.cloud.google.com/apis/credentials
          (use the same Google account that owns the Sheet)
       b. Click "+ CREATE CREDENTIALS" → "OAuth client ID"
          → Application type: Desktop app → Name: SleepWise → CREATE
       c. Click "DOWNLOAD JSON" on the popup → save the file as:
             automation/data/google_credentials.json
       d. Enable the Sheets API:
          console.cloud.google.com/apis/library → search "Google Sheets API" → Enable

     First run: a browser tab opens for Google login — approve once.
     After that: fully automatic, no browser needed.

USAGE:
  Run from the SleepReviewes root folder:

    # Generate ALL missing images, upload to GitHub, update sheet (full run)
    python automation/scripts/generators/generate_ig_images.py

    # Preview prompts without calling any API
    python automation/scripts/generators/generate_ig_images.py --dry-run

    # Regenerate one specific post
    python automation/scripts/generators/generate_ig_images.py --id IG-005

    # Limit to first N images (good for testing)
    python automation/scripts/generators/generate_ig_images.py --limit 3
"""

import os
import sys
import json
import time
import base64
import argparse
from pathlib import Path
from datetime import datetime

# ── Path setup ─────────────────────────────────────────────────────────────────
SCRIPT_DIR  = Path(__file__).resolve().parent
AUTO_DIR    = SCRIPT_DIR.parent.parent            # automation/
PROJECT_DIR = AUTO_DIR.parent                     # SleepReviewes/
IMAGES_DIR  = PROJECT_DIR / "images" / "instagram"
DATA_DIR    = AUTO_DIR / "data"
PROGRESS_FILE       = DATA_DIR / "ig_image_progress.json"
GOOGLE_CREDS_FILE = DATA_DIR / "google_credentials.json"
GOOGLE_TOKEN_FILE = DATA_DIR / "google_token.json"

# ── Load .env ──────────────────────────────────────────────────────────────────
from dotenv import load_dotenv
load_dotenv(AUTO_DIR / ".env")

# ── Dependency checks ──────────────────────────────────────────────────────────
MISSING = []

try:
    import requests
except ImportError:
    MISSING.append("requests")

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    MISSING.append("openai>=1.30.0")

try:
    import gspread
except ImportError:
    MISSING.append("gspread google-auth google-auth-oauthlib")

if MISSING:
    print("❌  Missing dependencies. Run:")
    print(f"      pip install {' '.join(MISSING)}")
    sys.exit(1)

# ── Image generation providers ─────────────────────────────────────────────────
GEMINI_IMAGEN_URL = (
    "https://generativelanguage.googleapis.com/v1beta"
    "/models/imagen-3.0-generate-002:predict"
)

# ── Config ─────────────────────────────────────────────────────────────────────
SPREADSHEET_ID    = "1KeWK1xO5eiD2YbFe63Fx8sV9Vf6jUwi57h71fc8zb5o"
SHEET_NAME        = "IG QUEUE"
GITHUB_REPO       = "Hanysharaf/sleepwisereviews"
GITHUB_PAGES_BASE = "https://hanysharaf.github.io/sleepwisereviews/images/instagram"
GITHUB_API_BASE   = "https://api.github.com"

# Columns (0-based)
COL_ID      = 0   # A
COL_TYPE    = 2   # C — Carousel / Reel / Single Image
COL_HOOK    = 3   # D — Hook / Title
COL_IMG_URL = 7   # H — Image URL  ← we fill this

# ── DALL-E 3 prompt system ─────────────────────────────────────────────────────

TOPIC_SCENES = {
    "weighted blanket": "wrapped in a luxurious weighted blanket on a plush sofa, serene smile, soft evening candlelight",
    "weighted":          "wrapped in a luxurious weighted blanket on the bed, deeply relaxed, bedroom evening scene",
    "mattress":          "stretching blissfully on a brand-new premium mattress, soft morning light through sheer curtains",
    "pillow":            "resting her cheek on a silky, plump pillow, dawn light, peaceful expression",
    "white noise":       "sleeping soundly with a soft-glowing white noise machine on the bedside table",
    "ear plug":          "gently placing foam sleep earplugs in before bedtime, cozy warm bedroom",
    "earplug":           "gently placing foam sleep earplugs in before bedtime, cozy warm bedroom",
    "eye mask":          "sliding on a luxurious silk sleep mask, gentle bedside lamp glow",
    "sleep mask":        "sliding on a luxurious silk sleep mask, gentle bedside lamp glow",
    "sleep tracker":     "glancing at her wrist sleep tracker with a satisfied morning smile, sitting up in bed",
    "tracker":           "glancing at her wrist sleep tracker, golden morning light",
    "melatonin":         "holding a small supplement bottle at her nightstand with a glass of water, calming bedtime ritual",
    "supplement":        "holding a small wellness supplement bottle at her nightstand, serene bedtime scene",
    "caffeine":          "choosing chamomile herbal tea over coffee, warm kitchen table in the early evening",
    "blue light":        "gently closing her laptop at her desk, warm lamp glow, transitioning to screen-free evening",
    "screen":            "putting her phone away on the nightstand, calm bedtime transition, soft lamp light",
    "exercise":          "doing a slow, joyful morning yoga stretch after waking refreshed, golden bedroom light",
    "temperature":       "sleeping comfortably under breathable linen bedding, cool and serene atmosphere",
    "cooling":           "resting on cooling gel pillows, light breathable sheets, cool morning blue-white tones",
    "back pain":         "waking up completely pain-free, doing a happy gentle back stretch in bed, morning light",
    "neck pain":         "smiling and pain-free in the morning, gently tilting her neck side to side",
    "side sleep":        "sleeping on her side with a supportive pillow tucked between her knees, peaceful setting",
    "snoring":           "couple sleeping peacefully side-by-side, minimalist bedroom, gentle morning light",
    "routine":           "following a soothing bedtime ritual — warm tea, dim lamp, journal on the nightstand",
    "bedroom":           "relaxing in a beautifully arranged sleep sanctuary — neutral linen tones, candle glow",
    "stress":            "practicing a slow breathing exercise in bed, hands on chest, serene expression",
    "anxiety":           "meditative and calm, seated on bed, warm bedside lamp, hands in her lap",
    "sleep tips":        "reading a wellness book propped on plush white pillows, cozy bedside scene",
    "sleep quality":     "waking up glowing and refreshed, stretching arms above her head, golden morning light",
    "insomnia":          "finally drifting peacefully into sleep, soft moonlit bedroom, expression of relief",
    "magnesium":         "holding a magnesium supplement bottle, nightstand with water glass and flickering candle",
    "deep sleep":        "in a deep, serene slumber, soft white bedding, moonlit window behind her",
    "headphone":         "wearing wireless sleep headphones, eyes closed, slight smile, cozy bedroom night",
    "music":             "wearing wireless sleep headphones in bed, calm expression, soft night lamp glow",
    "alarm":             "waking naturally to sunlight, stretching in bed, joyful expression — no alarm needed",
    "sunlight":          "opening sheer curtains to warm morning sunlight, feeling energized and refreshed",
    "default":           "waking up radiant and refreshed, soft morning light, white linen bedding, peaceful smile"
}

STYLE_MAP = {
    "Carousel":     "editorial lifestyle photography, clean swiping aesthetic",
    "Reel":         "dynamic editorial frame, crisp depth of field, lifestyle magazine quality",
    "Single Image": "premium hero advertising photograph, clean composition, brand campaign style"
}


def build_dalle_prompt(hook: str, content_type: str) -> str:
    hook_lower = hook.lower()
    scene = TOPIC_SCENES["default"]
    for keyword, scene_text in TOPIC_SCENES.items():
        if keyword in hook_lower:
            scene = scene_text
            break
    style = STYLE_MAP.get(content_type, STYLE_MAP["Single Image"])
    return (
        "Premium lifestyle advertising photography for a luxury sleep wellness brand. "
        f"Beautiful, radiant woman in her late 20s, {scene}. "
        "Elegant minimalist bedroom — natural white linen, warm neutral palette, "
        "soft directional light. "
        f"{style}. "
        "Commercial photography quality, sharp focus, shallow depth of field. "
        "Aspirational, calm, sophisticated. No text, no logos, no watermarks. "
        "Square 1:1 crop, Instagram-ready."
    )


# ── Google Sheets ──────────────────────────────────────────────────────────────

def connect_sheet():
    if not GOOGLE_CREDS_FILE.exists():
        print(f"\n❌  Google credentials file not found: {GOOGLE_CREDS_FILE}")
        print()
        print("    3-step setup:")
        print("    1. Go to: console.cloud.google.com/apis/credentials")
        print("    2. + CREATE CREDENTIALS → OAuth client ID → Desktop app → CREATE → Download JSON")
        print(f"    3. Save the file as: {GOOGLE_CREDS_FILE}")
        print()
        print("    Also enable Google Sheets API:")
        print("    console.cloud.google.com/apis/library → search 'Google Sheets API' → Enable")
        print()
        print("    First run opens browser once for login — automatic after that.")
        sys.exit(1)

    gc = gspread.oauth(
        credentials_filename=str(GOOGLE_CREDS_FILE),
        authorized_user_filename=str(GOOGLE_TOKEN_FILE),
    )
    ws = gc.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    return ws


def read_queue(ws) -> list:
    all_rows = ws.get_all_values()
    result = []
    for i, row in enumerate(all_rows[1:], start=0):
        while len(row) <= COL_IMG_URL:
            row.append("")
        pid = row[COL_ID].strip()
        if not pid:
            continue
        result.append({
            "row_index":  i,
            "sheet_row":  i + 2,       # gspread 1-based, header = row 1
            "id":          pid,
            "type":        row[COL_TYPE].strip() or "Single Image",
            "hook":        row[COL_HOOK].strip(),
            "image_url":   row[COL_IMG_URL].strip(),
        })
    return result


def write_image_url(ws, sheet_row: int, url: str):
    ws.update_cell(sheet_row, COL_IMG_URL + 1, url)   # gspread uses 1-based cols


# ── GitHub image upload ────────────────────────────────────────────────────────

def upload_to_github(filename: str, image_bytes: bytes, token: str) -> str:
    """
    Upload image bytes to GitHub repo and return the GitHub Pages URL.
    If the file already exists in the repo, it will be updated (requires SHA).
    """
    path    = f"images/instagram/{filename}"
    api_url = f"{GITHUB_API_BASE}/repos/{GITHUB_REPO}/contents/{path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept":        "application/vnd.github.v3+json",
    }

    # Check if file already exists (needed for update)
    sha = None
    check = requests.get(api_url, headers=headers)
    if check.status_code == 200:
        sha = check.json().get("sha")

    payload = {
        "message": f"feat: add Instagram image {filename.replace('.png', '')}",
        "content": base64.b64encode(image_bytes).decode("utf-8"),
    }
    if sha:
        payload["sha"] = sha

    resp = requests.put(api_url, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()

    return f"{GITHUB_PAGES_BASE}/{filename}"


# ── Progress tracking ──────────────────────────────────────────────────────────

def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_progress(progress: dict):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2)


# ── Core: generate one image end-to-end ───────────────────────────────────────

def generate_via_openai(client, prompt: str) -> bytes:
    """Generate image with DALL-E 3, return PNG bytes."""
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    temp_url = response.data[0].url
    img_resp = requests.get(temp_url, timeout=60)
    img_resp.raise_for_status()
    return img_resp.content


def generate_via_gemini(api_key: str, prompt: str) -> bytes:
    """Generate image with Google Imagen 3, return PNG bytes."""
    response = requests.post(
        GEMINI_IMAGEN_URL,
        params={"key": api_key},
        json={
            "instances": [{"prompt": prompt}],
            "parameters": {"sampleCount": 1, "aspectRatio": "1:1"},
        },
        timeout=60,
    )
    response.raise_for_status()
    predictions = response.json().get("predictions", [])
    if not predictions:
        raise ValueError("Gemini returned no image predictions")
    return base64.b64decode(predictions[0]["bytesBase64Encoded"])


def process_post(openai_client, gemini_key: str, post: dict, github_token: str, ws) -> bool:
    """
    Generate image → upload to GitHub → update sheet column H.
    Uses OpenAI if available, falls back to Gemini.
    """
    filename = f"{post['id'].lower()}.png"
    prompt   = build_dalle_prompt(post["hook"], post["type"])

    if openai_client:
        provider = "DALL-E 3"
        print(f"  🎨  {post['id']} [{post['type']}]  via OpenAI")
        image_bytes = generate_via_openai(openai_client, prompt)
    elif gemini_key:
        provider = "Imagen 3"
        print(f"  🎨  {post['id']} [{post['type']}]  via Google Imagen")
        image_bytes = generate_via_gemini(gemini_key, prompt)
    else:
        raise RuntimeError("No image generation API key found")

    # Save locally (backup / inspection)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    with open(IMAGES_DIR / filename, "wb") as f:
        f.write(image_bytes)

    # Upload to GitHub → get permanent URL
    pages_url = upload_to_github(filename, image_bytes, github_token)
    print(f"       → {pages_url}")

    # Update column H in Google Sheets
    write_image_url(ws, post["sheet_row"], pages_url)

    return True


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate DALL-E 3 Instagram images, upload to GitHub, update sheet"
    )
    parser.add_argument(
        "--id", type=str, metavar="IG-XXX",
        help="Process only this post (e.g. --id IG-005)"
    )
    parser.add_argument(
        "--limit", type=int, default=0, metavar="N",
        help="Process at most N posts (0 = all)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print prompts without calling any API"
    )
    parser.add_argument(
        "--overwrite", action="store_true",
        help="Regenerate even posts that already have an image URL"
    )
    args = parser.parse_args()

    print("=" * 64)
    print("  SleepWise IG Image Generator  —  DALL-E 3 + GitHub Auto-Upload")
    print("=" * 64)

    # ── Credentials ────────────────────────────────────────────────
    openai_key   = os.getenv("OPENAI_API_KEY", "").strip()
    gemini_key   = os.getenv("GOOGLE_AI_API_KEY", "").strip()
    github_token = os.getenv("GITHUB_TOKEN", "").strip()

    if not args.dry_run:
        if not openai_key and not gemini_key:
            print("\n❌  No image generation API key found.")
            print("    Add ONE of these to automation/.env:")
            print("      OPENAI_API_KEY=sk-proj-...    (OpenAI DALL-E 3, $5 one-time)")
            print("      GOOGLE_AI_API_KEY=AIza...     (Google Imagen 3, free — aistudio.google.com)")
            sys.exit(1)
        if not github_token:
            print("\n❌  GITHUB_TOKEN not set in automation/.env")
            sys.exit(1)

    openai_client = OpenAI(api_key=openai_key) if openai_key else None

    if openai_client:
        print("  Provider: OpenAI DALL-E 3")
    elif gemini_key:
        print("  Provider: Google Imagen 3 (free tier — 15 images/day)")
    else:
        openai_client = None

    # ── Google Sheets ───────────────────────────────────────────────
    print("\n📊  Reading IG QUEUE from Google Sheets…")
    ws   = connect_sheet()
    rows = read_queue(ws)
    print(f"    {len(rows)} posts loaded")

    # ── Filter posts to process ─────────────────────────────────────
    to_do = []
    for post in rows:
        if args.id and post["id"] != args.id:
            continue
        if post["image_url"] and not args.overwrite and not args.id:
            continue    # already has URL, skip
        to_do.append(post)

    if args.limit > 0:
        to_do = to_do[:args.limit]

    if not to_do:
        print("\n✅  All posts already have image URLs — nothing to generate.")
        print("    Use --overwrite to regenerate, or --id IG-XXX for a specific post.")
        return

    print(f"\n🎨  Posts queued: {len(to_do)}")
    if not args.dry_run:
        print(f"    Cost estimate:  ${len(to_do) * 0.04:.2f}  (DALL-E 3 standard)")
        print(f"    Time estimate:  ~{(len(to_do) * 14) // 60}m {(len(to_do) * 14) % 60}s")
    print()

    # ── Dry run — just show prompts ─────────────────────────────────
    if args.dry_run:
        for post in to_do:
            print(f"  {post['id']}  [{post['type']}]")
            print(f"    Hook:   {post['hook'][:72]}")
            print(f"    Prompt: {build_dalle_prompt(post['hook'], post['type'])[:120]}…")
            print()
        return

    # ── Generate ────────────────────────────────────────────────────
    progress  = load_progress()
    generated = 0
    failed    = 0

    for idx, post in enumerate(to_do):
        try:
            process_post(openai_client, gemini_key, post, github_token, ws)
            progress[post["id"]] = {
                "status": "done",
                "ts":     datetime.now().isoformat(),
            }
            save_progress(progress)
            generated += 1

        except Exception as exc:
            print(f"  ❌  {post['id']} — FAILED: {exc}")
            progress[post["id"]] = {
                "status": "failed",
                "error":  str(exc),
                "ts":     datetime.now().isoformat(),
            }
            save_progress(progress)
            failed += 1

        # Rate limits: DALL-E 3 = 5/min (12s gap), Imagen 3 = 15/day (no rush)
        if idx < len(to_do) - 1:
            time.sleep(12)

    print()
    print("=" * 64)
    print(f"  ✅  Generated: {generated}   ❌  Failed: {failed}")
    if generated:
        print()
        print("  Images are live on GitHub Pages.")
        print("  Column H in the sheet has been updated.")
        print("  Your n8n workflow will post them on their scheduled date.")
    print("=" * 64)


if __name__ == "__main__":
    main()
