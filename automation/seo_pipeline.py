import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

# Load .env
ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(ENV_PATH)

# Resolve project root and add automation dir to path
AUTOMATION_DIR = Path(__file__).parent
PROJECT_ROOT = AUTOMATION_DIR.parent
sys.path.insert(0, str(AUTOMATION_DIR))

import gspread
import anthropic

from config import ANTHROPIC_API_KEY
from modules.content_generator import ContentGenerator
from modules.website_manager import WebsiteManager

# ── Constants ──────────────────────────────────────────────────────────────────
SPREADSHEET_ID = "1KeWK1xO5eiD2YbFe63Fx8sV9Vf6jUwi57h71fc8zb5o"
SHEET_NAME = "Content Calendar"
BASE_URL = "https://sleepwisereviews.com"
DATE_FORMAT = "%d-%m-%Y"

KEYWORD_RESEARCH_SCRIPT = AUTOMATION_DIR / "scripts" / "keyword_research.py"

# Column indices (0-based)
COL_PUBLISH_DATE = 0
COL_FILENAME     = 1
COL_TITLE        = 2
COL_CATEGORY     = 3
COL_STATUS       = 4
COL_PUBLISHED_AT = 5
COL_IG_POST      = 6
COL_FB_POST      = 7

DISCLOSURE_HTML = (
    '<p class="disclosure">'
    "<em>Disclosure: We earn a small commission from qualifying Amazon purchases "
    "at no extra cost to you.</em>"
    "</p>"
)

FB_POST_PROMPT = """\
Write a Facebook post about: {keyword}
URL to include: {article_url}
Requirements:
- 100-150 words
- Conversational tone
- End with the article URL
- No affiliate links
- Mention 1-2 specific sleep tips from the topic
Return plain text only, no JSON."""


# ── Google Sheets auth ─────────────────────────────────────────────────────────
def get_worksheet():
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not sa_json:
        print("ERROR: GOOGLE_SERVICE_ACCOUNT_JSON env var not set.")
        sys.exit(1)
    sa_dict = json.loads(sa_json)
    gc = gspread.service_account_from_dict(sa_dict)
    return gc.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)


# ── Category inference ─────────────────────────────────────────────────────────
_PRODUCT_SIGNALS = {
    "best", "review", "buy", "buying", "guide", "top", "vs",
    "compare", "comparison", "cheap", "affordable", "budget",
    "ear plug", "earplug", "pillow", "mattress", "mask", "blanket",
    "machine", "tracker", "glasses", "curtain", "supplement"
}

def infer_category(keyword: str) -> str:
    lower = keyword.lower()
    for signal in _PRODUCT_SIGNALS:
        if signal in lower:
            return "Product Reviews"
    return "Sleep Science"


# ── research subcommand ────────────────────────────────────────────────────────
def cmd_research(seed: str) -> list[dict]:
    print(f"Running keyword research for: {seed}")

    result = subprocess.run(
        [sys.executable, str(KEYWORD_RESEARCH_SCRIPT), "--seed", seed],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("ERROR: keyword_research.py failed.")
        print(result.stderr)
        sys.exit(1)

    # The script prints JSON to stdout and a "Results saved to..." line to stderr
    raw_stdout = result.stdout.strip()

    # Strip the trailing "Results saved to:" line if it leaked into stdout
    lines = raw_stdout.splitlines()
    json_lines = [l for l in lines if not l.startswith("Results saved to:")]
    raw_json = "\n".join(json_lines)

    try:
        keywords = json.loads(raw_json)
    except json.JSONDecodeError:
        print("ERROR: Could not parse keyword_research.py output.")
        print(raw_stdout)
        sys.exit(1)

    # Print readable table
    col_w = 48
    print(f"\n{'#':<3}  {'Keyword':<{col_w}}  {'Intent':>6}  {'Type':<18}  {'Difficulty'}")
    print("-" * (col_w + 40))
    for i, kw in enumerate(keywords, 1):
        print(
            f"{i:<3}  {kw['keyword']:<{col_w}}  "
            f"{kw['intent_score']:>6}  "
            f"{kw['content_type']:<18}  "
            f"{kw.get('estimated_difficulty', '')}"
        )
    print()

    # Write to Google Sheets
    try:
        ws = get_worksheet()
        today_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        rows_to_append = []
        for kw in keywords:
            category = infer_category(kw["keyword"])
            row = [""] * 8
            row[COL_PUBLISH_DATE] = ""
            row[COL_FILENAME]     = ""
            row[COL_TITLE]        = kw["keyword"]
            row[COL_CATEGORY]     = category
            row[COL_STATUS]       = "KEYWORD"
            row[COL_PUBLISHED_AT] = ""
            row[COL_IG_POST]      = ""
            row[COL_FB_POST]      = ""
            rows_to_append.append(row)

        ws.append_rows(rows_to_append, value_input_option="RAW")
        print(f"  {len(keywords)} keywords written to Google Sheets ({SHEET_NAME}).")
    except Exception as exc:
        print(f"  WARN: Could not update Google Sheets: {exc}")

    return keywords


# ── Facebook post generation ───────────────────────────────────────────────────
def generate_fb_post(keyword: str, article_url: str) -> str:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    prompt = FB_POST_PROMPT.format(keyword=keyword, article_url=article_url)
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text.strip()


# ── Affiliate disclosure injection ────────────────────────────────────────────
def inject_disclosure(filepath: Path) -> None:
    html = filepath.read_text(encoding="utf-8")
    # Insert after the closing tag of the first <h1>
    match = re.search(r"(<h1[^>]*>.*?</h1>)", html, re.DOTALL | re.IGNORECASE)
    if match:
        end = match.end()
        html = html[:end] + "\n" + DISCLOSURE_HTML + html[end:]
    else:
        # Fallback: insert before first <p>
        html = html.replace("<p>", DISCLOSURE_HTML + "\n<p>", 1)
    filepath.write_text(html, encoding="utf-8")


# ── Git commit + push ──────────────────────────────────────────────────────────
def git_publish(filename: str, keyword: str) -> None:
    steps = [
        (["git", "add", f"posts/{filename}", "sitemap.xml"],
         "git add"),
        (["git", "commit", "-m", f"article: {keyword}"],
         "git commit"),
        (["git", "push"],
         "git push"),
    ]
    for cmd, label in steps:
        r = subprocess.run(cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  WARN: {label} failed: {r.stderr.strip()}")
        else:
            print(f"  {label} OK")


# ── Sheets: find matching KEYWORD row and update it ───────────────────────────
def update_sheet_row(ws, keyword: str, filename: str, ig_text: str, fb_text: str) -> None:
    today_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    all_rows = ws.get_all_values()

    target_row_index = None
    for i, row in enumerate(all_rows):
        while len(row) <= COL_STATUS:
            row.append("")
        title = row[COL_TITLE].strip().lower()
        status = row[COL_STATUS].strip().upper()
        if title == keyword.lower() and status == "KEYWORD":
            target_row_index = i
            break

    if target_row_index is None:
        print(f"  WARN: No KEYWORD row found for '{keyword}' in sheet — skipping sheet update.")
        return

    # gspread rows are 1-based; row 0 = header row 1 in sheet
    sheet_row = target_row_index + 1

    ws.update_cell(sheet_row, COL_FILENAME + 1,     filename)
    ws.update_cell(sheet_row, COL_STATUS + 1,        "PUBLISHED")
    ws.update_cell(sheet_row, COL_PUBLISHED_AT + 1,  today_iso)
    ws.update_cell(sheet_row, COL_IG_POST + 1,       ig_text)
    ws.update_cell(sheet_row, COL_FB_POST + 1,       fb_text)
    print(f"  Sheet row {sheet_row} updated to PUBLISHED.")


# ── generate subcommand ────────────────────────────────────────────────────────
def cmd_generate(keyword: str) -> None:
    print(f"Generating article for: {keyword}")

    # 1. Generate article content
    print("  [1/7] Generating article content...")
    gen = ContentGenerator()
    content_type = "buying_guide" if infer_category(keyword) == "Product Reviews" else "how_to"
    art_result = gen.generate_article(keyword, content_type=content_type)
    if not art_result.get("ok"):
        print(f"ERROR: Article generation failed: {art_result.get('error')}")
        sys.exit(1)

    article_data = art_result.get("article", {})
    if not article_data or "title" not in article_data:
        print("ERROR: Article JSON missing required 'title' field.")
        sys.exit(1)

    # 2. Save article HTML via WebsiteManager
    print("  [2/7] Saving article to /posts/...")
    mgr = WebsiteManager()
    save_result = mgr.create_article(article_data)
    if not save_result.get("ok"):
        print(f"ERROR: WebsiteManager failed: {save_result.get('error')}")
        sys.exit(1)

    filename = save_result["filename"]
    article_url = save_result["url"]
    filepath = Path(save_result["filepath"])
    print(f"  Saved: {filename}")
    print(f"  URL:   {article_url}")

    # 3. Inject affiliate disclosure
    print("  [3/7] Injecting affiliate disclosure...")
    inject_disclosure(filepath)

    # 4. Generate Instagram caption
    print("  [4/7] Generating Instagram caption...")
    intro = article_data.get("introduction", "")[:300]
    ig_result = gen.generate_instagram_caption(keyword, article_excerpt=intro)
    if ig_result.get("ok"):
        caption_data = ig_result.get("caption_data", {})
        ig_text = caption_data.get("caption", ig_result.get("content", ""))
        hashtags = caption_data.get("suggested_hashtags", [])
        if hashtags:
            ig_text = ig_text.rstrip() + "\n\n" + " ".join(f"#{h.lstrip('#')}" for h in hashtags[:25])
    else:
        ig_text = f"Better sleep starts with the right gear. Check out our guide on {keyword}. Link in bio."

    # 5. Generate Facebook post
    print("  [5/7] Generating Facebook post...")
    try:
        fb_text = generate_fb_post(keyword, article_url)
    except Exception as exc:
        print(f"  WARN: FB post generation failed: {exc}")
        fb_text = f"Looking to improve your sleep? We just published a new guide on {keyword}. {article_url}"

    # 6. Git commit + push
    print("  [6/7] Committing and pushing to GitHub...")
    git_publish(filename, keyword)

    # 7. Update Google Sheets
    print("  [7/7] Updating Google Sheets...")
    try:
        ws = get_worksheet()
        update_sheet_row(ws, keyword, filename, ig_text, fb_text)
    except Exception as exc:
        print(f"  WARN: Google Sheets update failed: {exc}")

    # Summary
    ig_preview = ig_text[:200].replace("\n", " ")
    fb_preview = fb_text[:200].replace("\n", " ")
    print("\n" + "=" * 60)
    print("DONE")
    print(f"Article URL : {article_url}")
    print(f"IG preview  : {ig_preview}...")
    print(f"FB preview  : {fb_preview}...")
    print("=" * 60)


# ── run subcommand ─────────────────────────────────────────────────────────────
def cmd_run(seed: str) -> None:
    keywords = cmd_research(seed)
    if not keywords:
        print("ERROR: No keywords returned from research.")
        sys.exit(1)

    # Auto-select keyword with highest intent_score
    top = max(keywords, key=lambda k: k.get("intent_score", 0))
    print(f"\nAuto-selected: '{top['keyword']}' (intent_score={top['intent_score']})")
    cmd_generate(top["keyword"])


# ── CLI entry point ────────────────────────────────────────────────────────────
def main() -> None:
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python seo_pipeline.py research <seed topic>")
        print("  python seo_pipeline.py generate <keyword>")
        print("  python seo_pipeline.py run <seed topic>")
        sys.exit(1)

    subcommand = sys.argv[1].lower()
    topic = sys.argv[2]

    if subcommand == "research":
        cmd_research(topic)
    elif subcommand == "generate":
        cmd_generate(topic)
    elif subcommand == "run":
        cmd_run(topic)
    else:
        print(f"ERROR: Unknown subcommand '{subcommand}'. Use research / generate / run.")
        sys.exit(1)


if __name__ == "__main__":
    main()
