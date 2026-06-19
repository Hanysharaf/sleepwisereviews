"""Normalize non-canonical cards in the homepage reviews-archive-grid.

Canonical card shape:
  <a class="article-card" href="posts/SLUG.html">
    <div class="card-cat">CATEGORY</div>
    <h3>TITLE</h3>
    <p>DESCRIPTION</p>
    <div class="card-meta"><span>SPAN1</span><span>SPAN2</span></div>
  </a>

A card is left BYTE-IDENTICAL iff it has a card-cat AND none of the
forbidden markers. Everything else is rebuilt from posts/SLUG.html.
"""
import os
import re
import sys
import ast

ROOT = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(ROOT, 'index.html')
POSTS_DIR = os.path.join(ROOT, 'posts')

GRID_OPEN = '<div class="reviews-archive-grid">'
GRID_CLOSE = '</div><!-- /reviews-archive-grid -->'

FORBIDDEN = ['article-thumb', 'article-excerpt', 'article-tag',
             'article-card-title', 'article-card-meta', 'article-body']

# ---------------------------------------------------------------------------
# Load CATEGORIES dict from generate_posts_index.py -> reverse slug->category
# ---------------------------------------------------------------------------
def load_categories():
    path = os.path.join(ROOT, 'generate_posts_index.py')
    src = open(path, encoding='utf-8').read()
    m = re.search(r'CATEGORIES\s*=\s*\{', src)
    start = m.start()
    # find matching close brace
    depth = 0
    i = src.index('{', start)
    j = i
    while j < len(src):
        if src[j] == '{':
            depth += 1
        elif src[j] == '}':
            depth -= 1
            if depth == 0:
                break
        j += 1
    dict_src = src[i:j + 1]
    # CATEGORIES is a pure dict-of-list-of-str literal; ast.literal_eval is
    # safe (no code execution, only literals).
    cats = ast.literal_eval(dict_src)
    slug_to_cat = {}
    for cat, slugs in cats.items():
        for s in slugs:
            slug_to_cat[s] = cat
    return slug_to_cat


# ---------------------------------------------------------------------------
# Grid extraction
# ---------------------------------------------------------------------------
def read_raw(path):
    """Read preserving original line endings (no newline translation)."""
    return open(path, encoding='utf-8', newline='').read()


def detect_eol(text):
    return '\r\n' if '\r\n' in text else '\n'


def read_index():
    return read_raw(INDEX)


def grid_bounds(html):
    a = html.index(GRID_OPEN) + len(GRID_OPEN)
    b = html.index(GRID_CLOSE)
    return a, b


def split_cards(grid_text):
    """Return list of (prefix_ws, card_text) for each anchor block.

    Splits on '<a class="article-card"'. Each card runs from its opening
    anchor tag to (and including) its closing </a>. Returns the full text
    between anchors so reassembly is lossless.
    """
    marker = '<a class="article-card"'
    idxs = [m.start() for m in re.finditer(re.escape(marker), grid_text)]
    cards = []
    for k, start in enumerate(idxs):
        end = idxs[k + 1] if k + 1 < len(idxs) else len(grid_text)
        cards.append((start, end, grid_text[start:end]))
    return cards


def card_href(card):
    m = re.search(r'href="(posts/[^"]+\.html)"', card)
    return m.group(1) if m else None


def card_slug(card):
    m = re.search(r'href="posts/([^"]+)\.html"', card)
    return m.group(1) if m else None


# A card is canonical iff every class= attribute it carries is in this set.
CANONICAL_CLASSES = {'article-card', 'card-cat', 'card-meta'}


def card_classes(card):
    return [m.group(1) for m in re.finditer(r'class="([^"]+)"', card)]


def is_canonical(card):
    """Canonical iff it has a <div class="card-cat"> and every class on the
    card is in CANONICAL_CLASSES (so no thumb/badge/category-tag/etc.)."""
    if '<div class="card-cat">' not in card:
        return False
    for cls in card_classes(card):
        if cls not in CANONICAL_CLASSES:
            return False
    return True


def card_shape(card):
    has_cat = '<div class="card-cat">' in card
    extra = sorted(set(c for c in card_classes(card)
                       if c not in CANONICAL_CLASSES))
    return has_cat, tuple(extra)


# ---------------------------------------------------------------------------
# Post-file field extraction
# ---------------------------------------------------------------------------
_title_re = re.compile(r'<title[^>]*>(.*?)</title>', re.DOTALL | re.IGNORECASE)
_desc_re = re.compile(
    r'<meta\s+name="description"\s+content="(.*?)"', re.DOTALL | re.IGNORECASE)
_postcat_re = re.compile(r'<div class="card-cat">(.*?)</div>', re.DOTALL)
_date_re = re.compile(r'"date(?:Published|Modified)"\s*:\s*"([0-9]{4}-[0-9]{2})')

_strip_suffix = re.compile(
    r'\s*[|\-–]\s*Sleep\s*Wise\s*Reviews\s*$', re.IGNORECASE)

MONTHS = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']


def post_fields(slug):
    path = os.path.join(POSTS_DIR, slug + '.html')
    if not os.path.exists(path):
        return None
    html = open(path, encoding='utf-8').read()
    tm = _title_re.search(html)
    title = None
    if tm:
        title = re.sub(r'<[^>]+>', '', tm.group(1)).strip()
        title = _strip_suffix.sub('', title).strip()
    dm = _desc_re.search(html)
    desc = dm.group(1).strip() if dm else None
    cm = _postcat_re.search(html)
    postcat = re.sub(r'<[^>]+>', '', cm.group(1)).strip() if cm else None
    date = None
    dt = _date_re.search(html)
    if dt:
        y, mo = dt.group(1).split('-')
        date = '%s %s' % (MONTHS[int(mo)], y)
    return {'title': title, 'desc': desc, 'postcat': postcat, 'date': date}


# ---------------------------------------------------------------------------
# Existing-card fallback extraction (V4/V3)
# ---------------------------------------------------------------------------
def existing_title(card):
    # try class-bearing title divs/headings, then a plain <h3>/<h2>
    for cls in ('article-title', 'article-card-title', 'card-title'):
        m = re.search(
            r'<(?:div|h2|h3)[^>]*class="%s"[^>]*>(.*?)</(?:div|h2|h3)>' % cls,
            card, re.DOTALL)
        if m:
            return re.sub(r'<[^>]+>', '', m.group(1)).strip()
    m = re.search(r'<h3[^>]*>(.*?)</h3>', card, re.DOTALL)
    if m:
        return re.sub(r'<[^>]+>', '', m.group(1)).strip()
    return None


def existing_tag(card):
    m = re.search(r'<span class="article-tag">(.*?)</span>', card, re.DOTALL)
    return m.group(1).strip() if m else None


# Map a V4 article-tag to a canonical category label when slug not in dict.
TAG_TO_CAT = {
    'Mattress': 'Mattresses & Bedding',
    'Mattresses': 'Mattresses & Bedding',
    'Bedding': 'Mattresses & Bedding',
    'Pillow': 'Mattresses & Bedding',
    'Guide': 'Guides & Plans',
    'Health': 'Health Conditions',
    'Supplement': 'Supplements',
    'Supplements': 'Supplements',
    'Product': 'Sleep Products',
    'Products': 'Sleep Products',
    'Relationship': 'Life Stages',
    'Life Stage': 'Life Stages',
    'Science': 'Sleep Science',
}

# Span1 label by category type.
def span1_for_category(cat):
    if cat in ('Mattresses & Bedding', 'Sleep Products', 'Supplements'):
        return 'Review'
    return 'Guide'


def esc_cat(s):
    """Escape a category label the way canonical cards do.

    Canonical grid labels use '&amp;' (e.g. 'Mattresses &amp; Bedding').
    Only a bare '&' (not already part of an entity) is escaped; titles and
    descriptions are taken verbatim from the post's already-escaped
    <title>/<meta> and are not re-escaped here.
    """
    return re.sub(r'&(?!amp;|lt;|gt;|quot;|#\d+;|#x[0-9a-fA-F]+;)', '&amp;', s)


def build_card(slug, href, indent, category, title, desc, date, eol='\n'):
    span1 = span1_for_category(category)
    category = esc_cat(category)
    if date:
        meta = '<span>%s</span><span>%s</span>' % (span1, date)
    else:
        meta = '<span>%s</span>' % span1
    # The opening anchor is emitted WITHOUT leading indent: the slot in the
    # grid already begins exactly at '<a'. Inner lines and the closing </a>
    # carry the indent so the card aligns with its neighbours.
    lines = [
        '<a class="article-card" href="%s">' % href,
        '%s  <div class="card-cat">%s</div>' % (indent, category),
        '%s  <h3>%s</h3>' % (indent, title),
        '%s  <p>%s</p>' % (indent, desc),
        '%s  <div class="card-meta">%s</div>' % (indent, meta),
        '%s</a>' % indent,
    ]
    return eol.join(lines)


def rebuild_card(card, slug_to_cat):
    href = card_href(card)
    slug = card_slug(card)
    fields = post_fields(slug) or {}
    # category
    category = fields.get('postcat') or slug_to_cat.get(slug)
    if not category:
        tag = existing_tag(card)
        category = TAG_TO_CAT.get(tag) if tag else None
    if not category:
        category = 'Guides & Plans'
    # title
    title = fields.get('title') or existing_title(card) or \
        slug.replace('-', ' ').title()
    # description
    desc = fields.get('desc')
    if not desc:
        # fall back to existing excerpt only if not truncated
        m = re.search(r'<div class="article-excerpt">(.*?)</div>', card,
                      re.DOTALL)
        if m:
            ex = m.group(1).strip()
            if ex and ex[-1] in '.!?':
                desc = ex
    if not desc:
        desc = title + '.'
    date = fields.get('date')
    # indent: leading whitespace before the anchor on its line.
    # Determine from the trailing whitespace just before this card in grid;
    # we use a fixed canonical indent matching most cards: 14 spaces handled
    # by caller. Here we infer from card's own first non-anchor line.
    return href, category, title, desc, date


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'report'
    target = sys.argv[2] if len(sys.argv) > 2 else INDEX

    html = read_raw(target)
    eol = detect_eol(html)
    ga, gb = grid_bounds(html)
    grid = html[ga:gb]
    cards = split_cards(grid)

    slug_to_cat = load_categories()

    # Instrument: histogram of shapes
    from collections import Counter
    hist = Counter()
    canonical = []
    rebuild = []
    for start, end, card in cards:
        has_cat, extra = card_shape(card)
        key = ('cat' if has_cat else 'nocat', extra)
        hist[key] += 1
        if is_canonical(card):
            canonical.append((start, end, card))
        else:
            rebuild.append((start, end, card))

    print('total anchors: %d' % len(cards))
    print('canonical (cat + no forbidden): %d' % len(canonical))
    print('to-rebuild: %d' % len(rebuild))
    print('--- shape histogram ---')
    for key, n in sorted(hist.items(), key=lambda x: -x[1]):
        print('  %-6s forbidden=%-40s : %d' % (key[0], key[1] or '()', n))

    assert sum(hist.values()) == len(cards) == 481, 'count mismatch'

    if mode == 'report':
        # Report rebuild slugs + missing posts
        missing = []
        for s, e, c in rebuild:
            slug = card_slug(c)
            if not os.path.exists(os.path.join(POSTS_DIR, slug + '.html')):
                missing.append(slug)
        print('--- rebuild slugs missing post files: %d ---' % len(missing))
        for m in missing:
            print('  MISSING:', m)
        return

    if mode == 'transform':
        out_path = sys.argv[3] if len(sys.argv) > 3 else target
        new_grid = grid
        # Process rebuilds from last to first to keep offsets valid.
        n_rebuilt = 0
        examples = []
        for start, end, card in sorted(rebuild, key=lambda x: -x[0]):
            # Split the slot into the anchor body (...</a>) and the trailing
            # inter-card whitespace, which we must preserve byte-for-byte.
            mt = re.search(r'^(.*?</a>)(\s*)$', card, re.DOTALL)
            body, trailing = mt.group(1), mt.group(2)
            # infer indent: whitespace before '<a' on its line
            line_start = grid.rfind('\n', 0, start) + 1
            indent = grid[line_start:start]
            if indent.strip():
                indent = '              '  # default 14 spaces
            href, category, title, desc, date = rebuild_card(card, slug_to_cat)
            new_body = build_card(card_slug(card), href, indent, category,
                                  title, desc, date, eol)
            new_grid = new_grid[:start] + new_body + trailing + new_grid[end:]
            n_rebuilt += 1
            if len(examples) < 6:
                examples.append(new_body)
        new_html = html[:ga] + new_grid + html[gb:]
        # newline='' so the \r\n we embedded are written verbatim (no
        # double-translation), preserving the source file's CRLF endings.
        open(out_path, 'w', encoding='utf-8', newline='').write(new_html)
        print('rebuilt %d cards -> %s' % (n_rebuilt, out_path))
        for ex in examples[-3:]:
            print('--- example ---')
            print(ex)


if __name__ == '__main__':
    main()
