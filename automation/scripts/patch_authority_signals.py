"""
patch_authority_signals.py
Adds visible Harry Soul byline + Article JSON-LD schema to SleepWise posts.

Idempotent: skips posts that already have the byline / schema.
Safe: works on a single file (--file) or whole posts/ dir (--all).
Run with --dry-run first to see what would change without writing.

Usage:
  python patch_authority_signals.py --file posts/best-adjustable-bed-frame.html --dry-run
  python patch_authority_signals.py --file posts/best-adjustable-bed-frame.html
  python patch_authority_signals.py --all --dry-run
  python patch_authority_signals.py --all
"""
from __future__ import annotations
import argparse, json, re, sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
POSTS_DIR = REPO / "posts"

BYLINE_HTML = '''
    <div class="author-box" style="display:flex;align-items:center;gap:1rem;margin:1rem 0 1.5rem;padding:1rem;background:rgba(26,34,56,0.5);border:1px solid rgba(201,168,76,0.2);border-radius:8px;font-family:sans-serif;">
      <div class="author-avatar" style="font-size:2rem;">\U0001F634</div>
      <div class="author-info">
        <div class="author-name" style="color:#F0E6C8;font-weight:500;font-size:0.95rem;">By <a href="../pages/about.html" style="color:#C9A84C;text-decoration:none;">Harry Soul</a> - SleepWiseReviews</div>
        <div class="author-role" style="color:#7A85A0;font-size:0.82rem;">Independent Sleep Researcher</div>
      </div>
    </div>
'''.rstrip("\n")

INTRO_RE = re.compile(r'(</h1>)', re.IGNORECASE)
TITLE_RE = re.compile(r'<title>([^<]+)</title>', re.IGNORECASE)
META_DESC_RE = re.compile(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']', re.IGNORECASE)
CANONICAL_RE = re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', re.IGNORECASE)
ARTICLE_SCHEMA_PRESENT = re.compile(r'"@type"\s*:\s*"Article"', re.IGNORECASE)
HAS_BYLINE = re.compile(r'class=["\']author-name["\']', re.IGNORECASE)
HEAD_END = re.compile(r'</head>', re.IGNORECASE)


def build_article_schema(title: str, description: str, canonical: str, modified_iso: str) -> str:
    clean_title = title.replace(" - SleepWiseReviews", "").replace(" | SleepWiseReviews", "").strip()
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": clean_title,
        "description": description,
        "url": canonical,
        "datePublished": "2025-01-01T00:00:00+00:00",
        "dateModified": modified_iso,
        "author": {
            "@type": "Person",
            "name": "Harry Soul",
            "url": "https://sleepwisereviews.com/pages/about.html",
            "jobTitle": "Independent Sleep Researcher",
        },
        "publisher": {
            "@type": "Organization",
            "name": "SleepWiseReviews",
            "url": "https://sleepwisereviews.com",
            "logo": {
                "@type": "ImageObject",
                "url": "https://sleepwisereviews.com/favicon.svg",
            },
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
    }
    return '<script type="application/ld+json">\n' + json.dumps(schema, indent=2, ensure_ascii=False) + '\n</script>'


def patch_one(path: Path, dry_run: bool = False) -> dict:
    result = {"file": path.name, "byline_added": False, "schema_added": False, "skipped_reason": None}
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        result["skipped_reason"] = "non-utf8"
        return result
    new_text = text
    changed = False

    if not HAS_BYLINE.search(new_text):
        m = INTRO_RE.search(new_text)
        if m:
            insert_at = m.end()
            new_text = new_text[:insert_at] + "\n\n" + BYLINE_HTML + "\n" + new_text[insert_at:]
            result["byline_added"] = True
            changed = True
        else:
            result["skipped_reason"] = "no article-intro anchor"

    if not ARTICLE_SCHEMA_PRESENT.search(new_text):
        title_m = TITLE_RE.search(new_text)
        desc_m = META_DESC_RE.search(new_text)
        canon_m = CANONICAL_RE.search(new_text)
        if title_m and desc_m and canon_m:
            mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()
            schema_block = build_article_schema(
                title_m.group(1).strip(),
                desc_m.group(1).strip(),
                canon_m.group(1).strip(),
                mtime,
            )
            head_end = HEAD_END.search(new_text)
            if head_end:
                insert_at = head_end.start()
                new_text = new_text[:insert_at] + schema_block + "\n" + new_text[insert_at:]
                result["schema_added"] = True
                changed = True
        else:
            if not result["skipped_reason"]:
                result["skipped_reason"] = "missing title/desc/canonical"

    if changed and not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return result


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--file", type=str, help="single post file (relative to repo)")
    g.add_argument("--all", action="store_true", help="patch every file in posts/")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    targets = []
    if args.file:
        p = (REPO / args.file).resolve()
        if not p.exists():
            p = Path(args.file).resolve()
        if not p.exists():
            print(f"file not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        targets = [p]
    else:
        targets = sorted(POSTS_DIR.glob("*.html"))

    by, sc, sk, na = 0, 0, 0, 0
    for p in targets:
        r = patch_one(p, dry_run=args.dry_run)
        if r["byline_added"]:
            by += 1
        if r["schema_added"]:
            sc += 1
        if r["skipped_reason"]:
            sk += 1
        if not r["byline_added"] and not r["schema_added"] and not r["skipped_reason"]:
            na += 1
        if args.file or args.dry_run:
            print(f"  {r}")

    print()
    print(f"SUMMARY ({'dry-run' if args.dry_run else 'applied'}): bylines={by}  schemas={sc}  skipped_with_reason={sk}  already_complete={na}  total_files={len(targets)}")


if __name__ == "__main__":
    main()
