"""Fix broken card markup in index.html.

The reviews-archive-grid section had 308 cards using <div class="card-cat"> as the
WRAPPER (the class is normally an inner label). That means:
  - card was not clickable (no <a> wrapper)
  - .article-card CSS never applied (no class match) — cards looked unstyled
  - .card-meta span spacing rule never applied — "7 picksBudget Guide" ran together

This converter rewrites the broken pattern to match the working <a class="article-card">
pattern used elsewhere in the same grid.

Idempotent: safe to run multiple times.
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(ROOT, 'index.html')

with open(INDEX_PATH, encoding='utf-8') as f:
    html = f.read()

# Pattern: the broken Structure B block.
# <div class="card-cat">
#   <span class="cat-badge"[ style="..."]>CATEGORY</span>
#   <h3><a href="HREF">TITLE</a></h3>
#   <p>DESCRIPTION</p>
#   <div class="card-meta">...</div>
# </div>
#
# Replaced with Structure A (already used by working cards in the same grid):
# <a class="article-card" href="HREF">
#   <div class="card-cat">CATEGORY</div>
#   <h3>TITLE</h3>
#   <p>DESCRIPTION</p>
#   <div class="card-meta">...</div>
# </a>

PATTERN = re.compile(
    r'<div class="card-cat">\s*'
    r'<span class="cat-badge"(?:\s+style="[^"]*")?>([^<]*)</span>\s*'
    r'<h3><a href="([^"]+)">([^<]+)</a></h3>\s*'
    r'<p>(.*?)</p>\s*'
    r'<div class="card-meta">(.*?)</div>\s*'
    r'</div>',
    re.DOTALL,
)


def _replace(match):
    cat = match.group(1).strip()
    href = match.group(2).strip()
    title = match.group(3).strip()
    desc = match.group(4).strip()
    meta = match.group(5).strip()
    return (
        f'<a class="article-card" href="{href}">\n'
        f'              <div class="card-cat">{cat}</div>\n'
        f'              <h3>{title}</h3>\n'
        f'              <p>{desc}</p>\n'
        f'              <div class="card-meta">{meta}</div>\n'
        f'            </a>'
    )


new_html, n = PATTERN.subn(_replace, html)

if n == 0:
    print('No broken cards found — nothing to change.')
else:
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f'Converted {n} broken card wrappers to <a class="article-card">.')
