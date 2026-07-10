"""Normalize all cards in the homepage "Every Guide We've Published" grid +
add "Show all X reviews" pagination (first 100 visible, rest behind a button).

Variants normalized to the canonical pattern:

  <a class="article-card" href="HREF">
    <div class="card-cat">CATEGORY</div>
    <h3>TITLE</h3>
    <p>DESCRIPTION</p>
    <div class="card-meta"><span>...</span><span>...</span></div>   <!-- optional -->
  </a>

Handles three input variants:
  V1 (already canonical):     unchanged
  V3 (article-card-title):    category looked up from CATEGORIES dict,
                              description pulled from the post's <meta name=description>
  V4 (article-thumb):         emoji dropped, article-tag -> card-cat,
                              article-title -> h3, article-excerpt -> p

Idempotent: re-running is a no-op once normalized.
"""
import ast
import html as html_mod
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(ROOT, 'index.html')
POSTS_DIR = os.path.join(ROOT, 'posts')

INITIAL_VISIBLE = 100


# ---------------------------------------------------------------------------
# Load CATEGORIES dict from generate_posts_index.py without executing it
# ---------------------------------------------------------------------------
def _ast_to_value(node):
    if isinstance(node, ast.Constant): return node.value
    if isinstance(node, ast.Dict): return {_ast_to_value(k): _ast_to_value(v) for k, v in zip(node.keys, node.values)}
    if isinstance(node, ast.List): return [_ast_to_value(e) for e in node.elts]
    if isinstance(node, ast.Tuple): return tuple(_ast_to_value(e) for e in node.elts)
    if isinstance(node, ast.Set): return {_ast_to_value(e) for e in node.elts}
    raise ValueError(f'Unsupported node: {type(node).__name__}')


def load_categories():
    with open(os.path.join(ROOT, 'generate_posts_index.py'), encoding='utf-8') as f:
        tree = ast.parse(f.read())
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            t = node.targets[0]
            if isinstance(t, ast.Name) and t.id == 'CATEGORIES':
                out = _ast_to_value(node.value)
                break
    return out


CATEGORIES = load_categories()
SLUG_TO_CAT = {slug: cat for cat, slugs in CATEGORIES.items() for slug in slugs}


# ---------------------------------------------------------------------------
# Meta description extraction (for cards missing a <p>)
# ---------------------------------------------------------------------------
_desc_re = re.compile(
    r'<meta\s+name=(["\'])description\1\s+content=(["\'])(.*?)\2',
    re.IGNORECASE | re.DOTALL,
)


def post_description(slug):
    path = os.path.join(POSTS_DIR, slug + '.html')
    if not os.path.isfile(path):
        return ''
    with open(path, encoding='utf-8') as f:
        src = f.read()
    m = _desc_re.search(src)
    return html_mod.unescape(m.group(3).strip()) if m else ''


def trim(text, n=180):
    text = re.sub(r'\s+', ' ', (text or '').strip())
    if len(text) <= n:
        return text
    return text[:n].rsplit(' ', 1)[0] + '...'


# ---------------------------------------------------------------------------
# Locate the reviews-archive-section block in the file
# ---------------------------------------------------------------------------
def find_section_bounds(src):
    start = src.find('<div class="reviews-archive-section">')
    if start == -1:
        raise SystemExit('reviews-archive-section not found')
    i = start + len('<div class="reviews-archive-section">')
    depth = 1
    while i < len(src) and depth > 0:
        nxt_open = src.find('<div', i)
        nxt_close = src.find('</div>', i)
        if nxt_close == -1:
            break
        if nxt_open != -1 and nxt_open < nxt_close:
            depth += 1
            i = nxt_open + 4
        else:
            depth -= 1
            i = nxt_close + len('</div>')
    return start, i


# ---------------------------------------------------------------------------
# Variant converters
# ---------------------------------------------------------------------------

# V4: article-thumb + article-body wrapper.
RE_V4 = re.compile(
    r'<a class="article-card" href="([^"]+)">\s*'
    r'<div class="article-thumb">[^<]*</div>\s*'
    r'<div class="article-body">\s*'
    r'<span class="article-tag">([^<]*)</span>\s*'
    r'<div class="article-title">([^<]*)</div>\s*'
    r'<div class="article-excerpt">(.*?)</div>\s*'
    r'</div>\s*'
    r'</a>',
    re.DOTALL,
)


def convert_v4(match):
    href, cat, title, excerpt = match.groups()
    return (
        f'<a class="article-card" href="{href}">\n'
        f'              <div class="card-cat">{cat.strip()}</div>\n'
        f'              <h3>{title.strip()}</h3>\n'
        f'              <p>{excerpt.strip()}</p>\n'
        f'            </a>'
    )


# V3: article-card-meta + article-card-title (no description in card)
RE_V3 = re.compile(
    r'<a class="article-card" href="([^"]+)">\s*'
    r'<div class="article-card-meta">([^<]*)</div>\s*'
    r'<div class="article-card-title">([^<]*)</div>\s*'
    r'</a>',
    re.DOTALL,
)


def convert_v3(match):
    href, meta, title = match.groups()
    slug = href.replace('posts/', '').replace('.html', '').strip()
    cat = SLUG_TO_CAT.get(slug, 'Sleep Guide')
    desc = trim(post_description(slug))
    desc_html = f'\n              <p>{html_mod.escape(desc)}</p>' if desc else ''
    return (
        f'<a class="article-card" href="{href}">\n'
        f'              <div class="card-cat">{cat}</div>\n'
        f'              <h3>{title.strip()}</h3>{desc_html}\n'
        f'            </a>'
    )


# ---------------------------------------------------------------------------
# Pagination: mark cards >= INITIAL_VISIBLE with batch-hidden
# ---------------------------------------------------------------------------

RE_ANCHOR = re.compile(r'<a class="article-card"(?P<rest>[^>]*)>')


def add_pagination_to_section(section):
    cards = list(RE_ANCHOR.finditer(section))
    total = len(cards)
    if total <= INITIAL_VISIBLE:
        return section, total, 0
    out = []
    last = 0
    for idx, m in enumerate(cards):
        out.append(section[last:m.start()])
        if idx >= INITIAL_VISIBLE:
            out.append(f'<a class="article-card batch-hidden"{m.group("rest")}>')
        else:
            out.append(m.group(0))
        last = m.end()
    out.append(section[last:])
    return ''.join(out), total, max(0, total - INITIAL_VISIBLE)


# ---------------------------------------------------------------------------
# CSS + JS injection
# ---------------------------------------------------------------------------

EXTRA_CSS = '''
    /* Archive pagination — Spec 009 follow-up */
    .reviews-archive-grid .article-card.batch-hidden { display: none; }
    .archive-show-more-wrap { text-align: center; margin: 2.4rem 0 0.5rem; }
    .archive-show-more-btn {
      display: inline-flex; align-items: center; gap: 0.5rem;
      padding: 0.9rem 2rem; border-radius: 10px;
      background: rgba(201,168,76,0.15); color: #c9a84c;
      border: 1px solid #c9a84c; font-family: inherit;
      font-size: 0.95rem; font-weight: 600; cursor: pointer;
      transition: background 0.2s, color 0.2s;
    }
    .archive-show-more-btn:hover { background: #c9a84c; color: #07101f; }
    .archive-show-more-count { color: #8899aa; font-size: 0.85rem; margin-top: 0.6rem; }
'''

EXTRA_JS = '''
  <script>
    (function() {
      var btn = document.getElementById('archive-show-more');
      if (!btn) return;
      btn.addEventListener('click', function() {
        var hidden = document.querySelectorAll('.reviews-archive-grid .article-card.batch-hidden');
        for (var i = 0; i < hidden.length; i++) hidden[i].classList.remove('batch-hidden');
        var wrap = document.getElementById('archive-show-more-wrap');
        if (wrap) wrap.style.display = 'none';
      });
    })();
  </script>
'''


# ---------------------------------------------------------------------------
# Main rewrite
# ---------------------------------------------------------------------------
with open(INDEX_PATH, encoding='utf-8') as f:
    src = f.read()

start, end = find_section_bounds(src)
section = src[start:end]

v4_count = 0
v3_count = 0


def _v4_wrap(m):
    global v4_count
    v4_count += 1
    return convert_v4(m)


def _v3_wrap(m):
    global v3_count
    v3_count += 1
    return convert_v3(m)


section = RE_V4.sub(_v4_wrap, section)
section = RE_V3.sub(_v3_wrap, section)

# Insert the show-more button right before the section closes
section, total_cards, hidden_cards = add_pagination_to_section(section)

if hidden_cards > 0:
    # Insert the button block just before the final </div></div> of the section.
    # Easiest: append before the LAST </div> of the section text (the section's outer close).
    button_html = (
        '        <div class="archive-show-more-wrap" id="archive-show-more-wrap">\n'
        f'          <button type="button" class="archive-show-more-btn" id="archive-show-more">'
        f'Show all {total_cards} reviews</button>\n'
        f'          <p class="archive-show-more-count">Showing {INITIAL_VISIBLE} of {total_cards} '
        'reviews · or <a href="posts/" style="color:#c9a84c;">browse by topic</a></p>\n'
        '        </div>\n'
    )
    # Find the closing of the reviews-archive-grid (innermost) and insert button after that close
    grid_open = section.find('<div class="reviews-archive-grid">')
    if grid_open == -1:
        raise SystemExit('grid open not found inside section')
    # Walk to matching close of that grid div
    i = grid_open + len('<div class="reviews-archive-grid">')
    depth = 1
    while i < len(section) and depth > 0:
        no = section.find('<div', i)
        nc = section.find('</div>', i)
        if nc == -1: break
        if no != -1 and no < nc:
            depth += 1; i = no + 4
        else:
            depth -= 1; i = nc + len('</div>')
    insert_at = i  # just after grid's </div>
    section = section[:insert_at] + '\n' + button_html + section[insert_at:]

new_src = src[:start] + section + src[end:]

# Inject CSS into the head's <style> block (append before its </style>)
style_close = new_src.find('</style>')
if style_close != -1 and EXTRA_CSS.strip() not in new_src:
    new_src = new_src[:style_close] + EXTRA_CSS + new_src[style_close:]

# Inject JS just before </body> (only if not already present)
if 'archive-show-more' in new_src and "id='archive-show-more'" not in new_src and 'archive-show-more-btn' in EXTRA_JS:
    if EXTRA_JS.strip() not in new_src:
        body_close = new_src.rfind('</body>')
        if body_close != -1:
            new_src = new_src[:body_close] + EXTRA_JS + new_src[body_close:]

if new_src != src:
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(new_src)

print(f'V4 cards normalized: {v4_count}')
print(f'V3 cards normalized: {v3_count}')
print(f'Total cards in grid: {total_cards}')
print(f'Hidden behind Show More: {hidden_cards}')
