"""
build_carousels_batch.py
Build carousel slides (s2-s5) for IG-003 to IG-031, skipping already-complete posts.
Reads content from slide_content.json — no external API calls.

After building:
  - Slides saved locally as images/instagram/ig-NNN/s1-s5.png
  - Generates review.html for browser-based QA

Usage:
    python build_carousels_batch.py            # build all + generate review HTML
    python build_carousels_batch.py --post IG-005  # single post only
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

# Allow importing build_carousel from parent
sys.path.insert(0, str(Path(__file__).parent.parent))
from build_carousel import IMAGES_DIR, add_hook_overlay, make_point_slide, make_cta_slide

BASE            = Path(__file__).parent.parent.parent
CONTENT_JSON    = BASE / "automation" / "data" / "slide_content.json"

SKIP_POSTS      = {"IG-001", "IG-002", "IG-010"}   # already fully built
CTA             = "Full review -> sleepwisereviews.com"


# ── Load slide content ────────────────────────────────────────────────────────
def load_content(post_ids=None) -> list[dict]:
    data = json.loads(CONTENT_JSON.read_text(encoding="utf-8"))
    posts = []
    for pid, entry in sorted(data.items()):
        if pid in SKIP_POSTS:
            continue
        if post_ids and pid not in post_ids:
            continue
        posts.append({
            "post_id":   pid,
            "hook":      entry["hook"],
            "points":    entry["points"],
            "cta":       entry.get("cta", CTA),
        })
    return posts


# ── Build one post ────────────────────────────────────────────────────────────
def build_post(post: dict) -> dict:
    pid       = post["post_id"]
    pid_lower = pid.lower()
    folder    = IMAGES_DIR / pid_lower

    print(f"\n>> {pid}")

    # Preserve clean photo before adding hook overlay
    s1    = folder / "s1.png"
    s1_bg = folder / "s1_bg.png"
    if not s1_bg.exists() and s1.exists():
        shutil.copy2(s1, s1_bg)
        print(f"   saved s1_bg.png (clean copy)")
    elif not s1.exists():
        print(f"   WARNING: s1.png not found — skipping hook overlay")

    # Build slides
    add_hook_overlay(pid_lower, post["hook"])
    for i, pt in enumerate(post["points"], start=2):
        make_point_slide(pid_lower, i, pt)
        print(f"   s{i}: {pt[:60]}...")
    make_cta_slide(pid_lower, post["cta"])
    print(f"   s5: CTA slide")

    return {
        "post_id":   pid,
        "pid_lower": pid_lower,
        "hook":      post["hook"],
        "points":    post["points"],
    }


# ── HTML review page ──────────────────────────────────────────────────────────
def write_review_html(built: list[dict], out_path: Path):
    cards = ""
    for b in built:
        pid = b["pid_lower"]
        slides_html = ""
        for n in range(1, 6):
            img_path = IMAGES_DIR / pid / f"s{n}.png"
            if img_path.exists():
                url   = img_path.as_uri()
                label = "s1 (hero+hook)" if n == 1 else f"s{n}"
                slides_html += f"""
                <div class="slide">
                  <p class="label">{label}</p>
                  <img src="{url}" width="200">
                </div>"""

        cards += f"""
        <div class="post-card" id="{pid}">
          <h2>{b['post_id']}</h2>
          <p class="hook">{b['hook']}</p>
          <div class="slides">{slides_html}</div>
          <div class="actions">
            <button class="pass-btn" onclick="mark('{pid}','PASS')">PASS</button>
            <input type="text" class="comment-input" id="comment-{pid}" placeholder="Add comment...">
            <button class="comment-btn" onclick="markComment('{pid}')">Comment &amp; Review</button>
          </div>
          <div class="status" id="status-{pid}"></div>
        </div>"""

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>SleepWise -- Carousel Review</title>
<style>
  body {{ font-family: sans-serif; background: #0f0f23; color: #eee; padding: 20px; }}
  h1 {{ color: #ffbf80; }}
  .post-card {{ background: #1a1a40; border-radius: 12px; padding: 20px; margin: 24px 0; }}
  h2 {{ color: #ffbf80; margin: 0 0 8px; }}
  .hook {{ color: #aaa; font-style: italic; margin: 0 0 16px; }}
  .slides {{ display: flex; gap: 12px; flex-wrap: wrap; }}
  .slide {{ text-align: center; }}
  .label {{ font-size: 11px; color: #888; margin: 4px 0; }}
  .slide img {{ border-radius: 8px; border: 2px solid #333; }}
  .actions {{ margin-top: 16px; display: flex; gap: 10px; align-items: center; }}
  .pass-btn {{ background: #2d7a2d; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-size: 14px; }}
  .pass-btn:hover {{ background: #3a9a3a; }}
  .comment-btn {{ background: #4a4a80; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-size: 14px; }}
  .comment-input {{ flex: 1; padding: 8px 12px; border-radius: 8px; border: 1px solid #444; background: #111; color: #eee; font-size: 14px; }}
  .status {{ margin-top: 10px; font-weight: bold; font-size: 14px; }}
  .status.pass {{ color: #4caf50; }}
  .status.review {{ color: #ff9800; }}
  .sticky-bar {{ position: sticky; top: 0; background: #0f0f23; border-bottom: 1px solid #333; padding: 12px 0; margin-bottom: 20px; display: flex; align-items: center; gap: 16px; z-index: 100; }}
  .summary {{ color: #aaa; font-size: 14px; }}
  .done-btn {{ background: #1a5276; color: white; border: none; padding: 12px 28px; border-radius: 8px; cursor: pointer; font-size: 15px; font-weight: bold; }}
  .done-btn:hover {{ background: #2471a3; }}
  .done-btn.all-done {{ background: #1e8449; }}
  .done-btn.all-done:hover {{ background: #27ae60; }}
</style>
</head>
<body>
<div class="sticky-bar">
  <button class="done-btn" id="done-btn" onclick="finishReview()">Done — Export Results</button>
  <span class="summary" id="summary">0 / {len(built)} reviewed</span>
</div>
<h1>SleepWise Reviews -- Carousel QA</h1>
<p style="color:#888">{len(built)} posts | Click PASS to approve or add a comment for revision</p>
{cards}
<script>
const results = {{}};
const total = {len(built)};
function updateSummary() {{
  const n = Object.keys(results).length;
  const passes = Object.values(results).filter(r => r.action === 'PASS').length;
  document.getElementById('summary').textContent = n + ' / ' + total + ' reviewed (' + passes + ' PASS)';
  if (n === total) {{
    document.getElementById('done-btn').className = 'done-btn all-done';
    document.getElementById('done-btn').textContent = 'All Done! Export Results';
  }}
}}
function mark(pid, action) {{
  results[pid] = {{action, comment: ''}};
  document.getElementById('status-' + pid).textContent = 'PASS';
  document.getElementById('status-' + pid).className = 'status pass';
  console.log('QA_RESULT:' + JSON.stringify({{pid, action, comment: ''}}));
  updateSummary();
}}
function markComment(pid) {{
  const comment = document.getElementById('comment-' + pid).value.trim();
  results[pid] = {{action: 'REVIEW', comment}};
  document.getElementById('status-' + pid).textContent = 'REVIEW: ' + comment;
  document.getElementById('status-' + pid).className = 'status review';
  console.log('QA_RESULT:' + JSON.stringify({{pid, action: 'REVIEW', comment}}));
  updateSummary();
}}
function finishReview() {{
  const lines = Object.entries(results).map(([pid, r]) =>
    'QA_RESULT:' + JSON.stringify({{pid, action: r.action, comment: r.comment}})
  ).join('\\n');
  if (!lines) {{ alert('No posts reviewed yet.'); return; }}
  const pass = Object.values(results).filter(r => r.action === 'PASS').length;
  const review = Object.keys(results).length - pass;
  alert('Review complete!\\n\\nPASS: ' + pass + '\\nNEEDS REVIEW: ' + review + '\\n\\nCheck browser console for QA_RESULT lines.');
  console.log('=== FINAL QA EXPORT ===');
  console.log(lines);
}}
</script>
</body>
</html>"""
    out_path.write_text(html, encoding="utf-8")
    print(f"\nReview page: {out_path}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser()
    parser.add_argument("--post", help="Build a single post only (e.g. IG-005)")
    args = parser.parse_args()

    if args.post:
        posts = load_content([args.post.upper()])
    else:
        posts = load_content()

    print(f"Building {len(posts)} carousels (skipping: {', '.join(sorted(SKIP_POSTS))})")

    built  = []
    errors = []
    for post in posts:
        try:
            result = build_post(post)
            built.append(result)
        except Exception as e:
            print(f"   ERROR {post['post_id']}: {e}")
            errors.append(post["post_id"])

    print(f"\n{'='*50}")
    print(f"Built: {len(built)} | Errors: {len(errors)}")
    if errors:
        print(f"Failed: {errors}")

    if built:
        review_path = BASE / "automation" / "data" / "review.html"
        write_review_html(built, review_path)

    return built, errors


if __name__ == "__main__":
    main()
