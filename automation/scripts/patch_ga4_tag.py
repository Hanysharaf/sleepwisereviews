"""Backfill the GA4 tag onto posts that predate the tag being added to the post generator.

Idempotent: skips any file that already contains the GA4 tag. Safe to re-run.

Usage:
    python automation/scripts/patch_ga4_tag.py --all --dry-run
    python automation/scripts/patch_ga4_tag.py --file posts/some-post.html
    python automation/scripts/patch_ga4_tag.py --all
"""
import argparse
import sys
from pathlib import Path

GA4_ID = "G-ZKGY2B72WH"

SNIPPET = f"""<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA4_ID}');
</script>
"""

REPO_ROOT = Path(__file__).resolve().parents[2]
POSTS_DIR = REPO_ROOT / "posts"


def patch_file(path: Path, dry_run: bool) -> str:
    text = path.read_text(encoding="utf-8")
    if GA4_ID in text:
        return "skip-already-tagged"

    marker = "<head>"
    idx = text.find(marker)
    if idx == -1:
        return "fail-no-head-tag"

    insert_at = idx + len(marker)
    new_text = text[:insert_at] + "\n" + SNIPPET + text[insert_at:]

    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return "patched"


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Patch every post under posts/")
    group.add_argument("--file", type=str, help="Patch a single file (relative to repo root)")
    parser.add_argument("--dry-run", action="store_true", help="Report only, don't write")
    args = parser.parse_args()

    if args.file:
        targets = [REPO_ROOT / args.file]
    else:
        targets = sorted(POSTS_DIR.glob("*.html"))

    counts = {"patched": 0, "skip-already-tagged": 0, "fail-no-head-tag": 0}
    for path in targets:
        if not path.is_file():
            print(f"MISSING: {path}")
            continue
        result = patch_file(path, args.dry_run)
        counts[result] = counts.get(result, 0) + 1
        if result != "skip-already-tagged":
            print(f"{result}: {path.relative_to(REPO_ROOT)}")

    print("----")
    print(f"Total: {len(targets)}  Patched: {counts['patched']}  "
          f"Already tagged: {counts['skip-already-tagged']}  Failed: {counts['fail-no-head-tag']}")
    if args.dry_run:
        print("(dry run — no files written)")


if __name__ == "__main__":
    sys.exit(main())
