"""
generate_photos_batch.py
Generate lifestyle photos for ig-032 to ig-090 using Google Imagen 3.
Reads prompts from photo_queue.txt, saves each as ig-NNN/s1.png.
Free tier: 15 images/day via Google AI Studio.

Usage:
    python automation/scripts/generate_photos_batch.py --start 32 --end 45
    python automation/scripts/generate_photos_batch.py --id 32
    python automation/scripts/generate_photos_batch.py --start 32 --end 41 --dry-run
"""

import os
import re
import sys
import time
import base64
import argparse
import requests
from pathlib import Path

BASE_DIR   = Path(__file__).resolve().parent.parent.parent
AUTO_DIR   = BASE_DIR / "automation"
IMAGES_DIR = BASE_DIR / "images" / "instagram"
QUEUE_FILE = AUTO_DIR / "data" / "photo_queue.txt"

from dotenv import load_dotenv
load_dotenv(AUTO_DIR / ".env")

GEMINI_IMAGEN_URL = (
    "https://generativelanguage.googleapis.com/v1beta"
    "/models/imagen-3.0-generate-002:predict"
)


def parse_queue(path: Path) -> dict:
    entries = {}
    current_id = None
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        m = re.match(r"^IG-(\d+)$", line)
        if m:
            current_id = int(m.group(1))
            entries[current_id] = {}
        elif current_id and line.startswith("SAVE TO:"):
            entries[current_id]["save_to"] = line.split(":", 1)[1].strip()
        elif current_id and line.startswith("PROMPT:"):
            entries[current_id]["prompt"] = line.split(":", 1)[1].strip()
    return entries


def generate_imagen(api_key: str, prompt: str) -> bytes:
    resp = requests.post(
        GEMINI_IMAGEN_URL,
        params={"key": api_key},
        json={
            "instances": [{"prompt": prompt}],
            "parameters": {"sampleCount": 1, "aspectRatio": "1:1"},
        },
        timeout=90,
    )
    resp.raise_for_status()
    predictions = resp.json().get("predictions", [])
    if not predictions:
        raise ValueError("Imagen returned no predictions")
    return base64.b64decode(predictions[0]["bytesBase64Encoded"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=32)
    parser.add_argument("--end",   type=int, default=45)
    parser.add_argument("--id",    type=int, help="Single post number")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    api_key = os.getenv("GOOGLE_AI_API_KEY", "").strip()
    if not api_key and not args.dry_run:
        print("GOOGLE_AI_API_KEY not set in automation/.env")
        sys.exit(1)

    queue = parse_queue(QUEUE_FILE)

    if args.id:
        ids = [args.id]
    else:
        ids = list(range(args.start, args.end + 1))

    to_do = [(n, queue[n]) for n in ids if n in queue]
    print(f"Posts to generate: {len(to_do)}")
    print(f"Free tier: 15/day via Google Imagen 3\n")

    done = 0
    for i, (num, entry) in enumerate(to_do):
        pid = f"ig-{num:03d}"
        save_rel = entry.get("save_to", f"images/instagram/{pid}/s1.png")
        out_path  = BASE_DIR / save_rel
        prompt    = entry.get("prompt", "")

        out_path.parent.mkdir(parents=True, exist_ok=True)

        if out_path.exists():
            print(f"  SKIP {pid}/s1.png — already exists")
            continue

        print(f"  [{i+1}/{len(to_do)}] {pid} — generating...")
        if args.dry_run:
            print(f"    Prompt: {prompt[:80]}...")
            continue

        try:
            img_bytes = generate_imagen(api_key, prompt)
            out_path.write_bytes(img_bytes)
            print(f"    Saved -> {out_path}")
            done += 1
        except Exception as e:
            print(f"    FAILED: {e}")

        if i < len(to_do) - 1:
            time.sleep(4)

    print(f"\nDone: {done} photos generated")
    if done:
        print("Next step: run build_carousels_batch.py to build full carousels")


if __name__ == "__main__":
    main()
