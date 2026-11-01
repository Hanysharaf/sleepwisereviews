# How to run (from the sleepwisereviews repo root; GOOGLE_AI_API_KEY must be set in automation\.env):
#   git fetch origin claude/stoic-hopper-76rxhh
#   git checkout claude/stoic-hopper-76rxhh ; git pull
#   python scripts/make_covers_106_119.py   (Hany's PC: C:\Users\Hany\venvs\swr\Scripts\python.exe)
"""
Make the 14 IG-106..119 cover images (slide 1) for PR #61 and push them to the PR branch.

For each post: generate a lifestyle photo with Gemini from the batch file's G prompt
(content/ig-batch-106-119.md in swr-hub), put the amber hook on it with
automation/build_carousel.py add_hook_overlay (unchanged), save it as
images/instagram/ig-<id>/ig-<id>-cover.png, and delete the temporary s1/s1_bg files so each
folder matches ig-105 (cover + s2-s5). Existing covers are skipped, so re-running is safe.

The key is read from automation/.env (GOOGLE_AI_API_KEY) and is never printed.
Nothing is pushed until you check the 14 covers and confirm at the prompt.
"""
import base64
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

REPO = Path(__file__).resolve().parent.parent
BRANCH = "claude/stoic-hopper-76rxhh"  # PR #61 branch
assert (REPO / "automation" / "build_carousel.py").exists(), "script must live in <repo>/scripts/"

load_dotenv(REPO / "automation" / ".env")
KEY = os.getenv("GOOGLE_AI_API_KEY", "")
if not KEY:
    sys.exit("GOOGLE_AI_API_KEY missing in automation/.env")
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent"

sys.path.insert(0, str(REPO / "automation"))
from build_carousel import add_hook_overlay, IMAGES_DIR  # noqa: E402

POSTS = {
    "ig-106": ("Pick one wake-up time and keep it every day", "Bedside table with an analog alarm clock showing early morning, soft sunrise light through sheer curtains, neatly made bed with white linen, calm minimalist bedroom, no people, no text"),
    "ig-107": ("Think a nightcap helps you sleep? Rethink it", "Empty wine glass beside a glass of water on a wooden nightstand, dim warm lamp, white linen bed in soft focus, calm evening still life, no people, no brand labels, no text"),
    "ig-108": ("Loud snoring and gasping for air? It could be sleep apnea", "Dark calm bedroom at night, empty bed with rumpled white linen, a soft blue night light on the nightstand, quiet moody atmosphere, no people, no text"),
    "ig-109": ("An urge to move your legs at night? Meet restless legs syndrome", "Cozy armchair with a knitted throw and a footstool in a softly lit living room at night, warm lamp, calm mood, no people, no text"),
    "ig-110": ("Three bedroom fixes for better sleep: quiet, calm, cool", "Minimalist bedroom at night with a small white noise machine on the nightstand, cool blue-grey tones, white linen bed, window slightly open, no people, no brand logos, no text"),
    "ig-111": ("Try a 30-minute screen-free buffer before bed", "Smartphone face down on a wooden nightstand beside an open paperback and a warm lamp, cozy bed with linen bedding, evening glow, no people, no screen content, no text"),
    "ig-112": ("Napping? Keep it short and early", "Sunny living room in early afternoon, a sofa with a soft cushion and a light blanket, a cup of tea on a side table, airy calm light, no people, no text"),
    "ig-113": ("Your melatonin label may not match what's inside", "Small amber supplement bottle without a label and a few soft gummies on a white saucer, nightstand, soft evening light, no brand names, no text"),
    "ig-114": ("Drowsy driving is more common than you think", "Empty car interior at dusk seen from the passenger side, steering wheel and dashboard in soft evening light, road ahead blurred, no people, no brand logos, no text"),
    "ig-115": ("Sleeping in the day after a night shift? Make it very dark", "Bedroom in daytime with heavy room-darkening curtains drawn, thin line of sunlight at the edge, dim calm interior, made bed with grey linen, no people, no text"),
    "ig-116": ("Heartburn at night? Two changes to ask about", "Bed with a white foam wedge pillow under linen pillows, soft morning light, minimalist bedroom, side view, no people, no brand logos, no text"),
    "ig-117": ("When does insomnia count as chronic?", "Open notebook with a simple hand-drawn weekly grid and a pen on a nightstand, warm lamp, calm bedroom background, no people, no readable text"),
    "ig-118": ("Can you catch up on sleep at the weekend? One study says no", "Weekend morning bedroom with sunlight through curtains, rumpled white bed, a calendar on the wall with no readable text, calm mood, no people"),
    "ig-119": ("Thinking of melatonin for your child? Ask first", "Child's bedroom at night with a small star-shaped night light, stuffed toy on a neatly made bed, soft warm glow, no people, no text"),
}


def gemini(prompt: str) -> bytes:
    r = requests.post(URL, params={"key": KEY}, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=120)
    if r.status_code != 200:
        # report status only; the request URL (which carries the key) is never printed
        raise RuntimeError(f"Gemini HTTP {r.status_code}")
    for part in r.json()["candidates"][0]["content"]["parts"]:
        inline = part.get("inlineData") or part.get("inline_data")
        if inline:
            return base64.b64decode(inline["data"])
    raise RuntimeError("no image in Gemini response")


def git(*args):
    subprocess.run(["git", *args], cwd=REPO, check=True)


def main():
    current = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=REPO,
                             capture_output=True, text=True, check=True).stdout.strip()
    if current != BRANCH:
        sys.exit(f"Checked out branch is '{current}'. Run: git checkout {BRANCH}")

    done = []
    for pid, (hook, prompt) in POSTS.items():
        folder = IMAGES_DIR / pid
        cover = folder / f"{pid}-cover.png"
        if cover.exists():
            print(f"{pid}: cover exists, skip")
            done.append(cover)
            continue
        print(f"{pid}: generating photo...")
        try:
            (folder / "s1_bg.png").write_bytes(gemini(prompt))
        except Exception as e:
            print(f"{pid}: FAILED ({type(e).__name__}: {str(e).replace(KEY, '***')})")
            continue
        add_hook_overlay(pid, hook)                       # writes s1.png from s1_bg.png
        shutil.move(str(folder / "s1.png"), str(cover))   # ig-105 layout: cover + s2-s5 only
        (folder / "s1_bg.png").unlink()
        done.append(cover)
        time.sleep(4)

    print(f"\n{len(done)}/14 covers ready in images/instagram/ig-106..ig-119/.")
    if len(done) != 14:
        sys.exit("Not all covers were made. Re-run the script (existing covers are skipped). Nothing pushed.")

    print("Open the 14 covers and check: no faces, no brand logos, no stray text, hook readable.")
    input(f"Press Enter to commit and push the 14 covers to {BRANCH} (PR #61), or Ctrl+C to stop... ")

    paths = [p.relative_to(REPO).as_posix() for p in done]
    git("add", *paths)
    git("commit", "-m", "IG-106..119 covers (hook overlay via automation/build_carousel.py)")
    git("push", "origin", f"HEAD:{BRANCH}")
    print("Pushed. PR #61 now has all 70 files; ask the reviewer to check it.")


if __name__ == "__main__":
    main()
