"""
inject_adsense.py — Add Google AdSense auto-ads to all HTML files on SleepWiseReviews.

Usage:
    python inject_adsense.py --pub-id ca-pub-XXXXXXXXXXXXXXXX
    python inject_adsense.py --pub-id ca-pub-XXXXXXXXXXXXXXXX --dry-run
    python inject_adsense.py --pub-id ca-pub-XXXXXXXXXXXXXXXX --exclude category-

Run from repo root. Updates posts/ and root HTML files.
"""

import argparse
from pathlib import Path

ADSENSE_SNIPPET = """
    <!-- Google AdSense Auto-Ads -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={pub_id}"
         crossorigin="anonymous"></script>"""

MARKER = "pagead2.googlesyndication.com"


def inject_file(path: Path, pub_id: str, dry_run: bool = False) -> bool:
    content = path.read_text(encoding="utf-8")

    if MARKER in content:
        print(f"  SKIP (already has AdSense): {path.name}")
        return False

    if "</head>" not in content:
        print(f"  SKIP (no </head> tag): {path.name}")
        return False

    snippet = ADSENSE_SNIPPET.format(pub_id=pub_id)
    updated = content.replace("</head>", f"{snippet}\n</head>", 1)

    if dry_run:
        print(f"  DRY-RUN: would inject into {path.name}")
        return True

    path.write_text(updated, encoding="utf-8")
    print(f"  INJECTED: {path.name}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Inject Google AdSense into SleepWiseReviews HTML files")
    parser.add_argument("--pub-id", required=True, help="AdSense publisher ID (ca-pub-XXXXXXXX)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--exclude", default="", help="Skip files whose name contains this string")
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent.parent

    targets = list((repo_root / "posts").glob("*.html"))
    targets += [f for f in repo_root.glob("*.html") if "INDEX" not in f.name.upper()]

    if args.exclude:
        targets = [f for f in targets if args.exclude not in f.name]

    injected = skipped = 0
    print(f"Publisher ID: {args.pub_id} | Files: {len(targets)} | Dry run: {args.dry_run}")
    print("-" * 60)

    for path in sorted(targets):
        if inject_file(path, args.pub_id, dry_run=args.dry_run):
            injected += 1
        else:
            skipped += 1

    print("-" * 60)
    print(f"Injected: {injected} | Skipped: {skipped}")


if __name__ == "__main__":
    main()
