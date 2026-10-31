"""One-off: apply queue_normalize to every file in scheduled/ (not scheduled/_published). No network."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "automation"))
from queue_normalize import normalize_html  # noqa: E402

changed = 0
for f in sorted((ROOT / "scheduled").glob("*.html")):
    old = f.read_text(encoding="utf-8")
    new = normalize_html(old, f.name, ROOT / "pages")
    if new != old:
        f.write_text(new, encoding="utf-8")
        changed += 1
print("changed", changed)
