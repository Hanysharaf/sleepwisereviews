"""Generate per-category browse pages (Spec 009 — Level 2).

Reads CATEGORIES / CAT_ANCHOR from generate_posts_index.py without triggering
its side-effects, then builds a card-grid HTML page per category with article
title + excerpt + 'Read' link + scoped search.

Usage:
    python generate_category_pages.py                # build all 12
    python generate_category_pages.py sleep-science  # build one (test bed)
"""
import ast
import html as html_mod
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
POSTS_DIR = os.path.join(ROOT, 'posts')
OUT_DIR = os.path.join(POSTS_DIR, 'category')
BASE_URL = 'https://sleepwisereviews.com'

# Show this many article cards initially; the rest are hidden behind a
# "Show all X articles" button. Search bar still matches across the full set.
INITIAL_VISIBLE = 50


# ---------------------------------------------------------------------------
# Load CATEGORIES + CAT_ANCHOR from sibling script without executing it.
# Uses AST to walk dict/list/str literal nodes manually.
# ---------------------------------------------------------------------------
def _ast_to_value(node):
    """Convert an ast literal node (Dict/List/Constant/Tuple/Set) to Python value."""
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Dict):
        return {_ast_to_value(k): _ast_to_value(v) for k, v in zip(node.keys, node.values)}
    if isinstance(node, ast.List):
        return [_ast_to_value(e) for e in node.elts]
    if isinstance(node, ast.Tuple):
        return tuple(_ast_to_value(e) for e in node.elts)
    if isinstance(node, ast.Set):
        return {_ast_to_value(e) for e in node.elts}
    raise ValueError(f'Unsupported AST node: {type(node).__name__}')


def _load_constants():
    src_path = os.path.join(ROOT, 'generate_posts_index.py')
    with open(src_path, encoding='utf-8') as f:
        tree = ast.parse(f.read())
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            t = node.targets[0]
            if isinstance(t, ast.Name) and t.id in ('CATEGORIES', 'CAT_ANCHOR'):
                out[t.id] = _ast_to_value(node.value)
    return out['CATEGORIES'], out['CAT_ANCHOR']


CATEGORIES, CAT_ANCHOR = _load_constants()
SLUG_TO_NAME = {slug: name for name, slug in CAT_ANCHOR.items()}

CAT_DESCRIPTIONS = {
    'insomnia-cbti': 'Evidence-based approaches to insomnia, CBT-I techniques, anxiety, and sleep disorders.',
    'sleep-science': 'How sleep actually works — stages, circadian rhythm, dreams, and the biology of rest.',
    'caffeine-nutrition': 'What you eat and drink — caffeine, melatonin, magnesium, alcohol, and food timing.',
    'sleep-environment': 'Temperature, light, sound, and bedroom setup — engineering the perfect sleep space.',
    'health-conditions': 'Sleep apnea, fibromyalgia, chronic pain, and 200+ medical conditions that affect sleep.',
    'life-stages': 'Pregnancy, kids, teens, menopause, and seniors — sleep needs change with life.',
    'timing-jet-lag': 'Jet lag, shift work, daylight saving, social jetlag, and resetting your schedule.',
    'napping-performance': 'Power naps, sleep inertia, athletic performance, and cognitive output.',
    'guides-plans': 'Step-by-step plans, checklists, challenges, and chronotype-based routines.',
    'mattresses-bedding': 'Mattresses, pillows, sheets, toppers — buying guides and material comparisons.',
    'sleep-products': 'Sleep masks, white noise machines, weighted blankets, trackers, and gadgets.',
    'supplements': 'Melatonin, magnesium, ashwagandha, L-theanine, CBD — what works and what does not.',
}


# ---------------------------------------------------------------------------
# Title + description extraction
# ---------------------------------------------------------------------------
_title_re = re.compile(r'<title[^>]*>(.*?)</title>', re.DOTALL | re.IGNORECASE)
# Backreference matches the same quote char that opened the attribute, so
# apostrophes inside double-quoted descriptions don't terminate the match.
_desc_re = re.compile(
    r'<meta\s+name=(["\'])description\1\s+content=(["\'])(.*?)\2',
    re.IGNORECASE | re.DOTALL,
)
_strip_suffix = re.compile(r'\s*[|\-–]\s*(SleepWise.*|Sleep.*)$', re.IGNORECASE)


def extract_meta(slug):
    """Return (title, description) for a post slug."""
    path = os.path.join(POSTS_DIR, slug + '.html')
    if not os.path.isfile(path):
        return ('', '')
    with open(path, encoding='utf-8') as f:
        src = f.read()
    title = ''
    m = _title_re.search(src)
    if m:
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        title = _strip_suffix.sub('', title).strip()
        title = html_mod.unescape(title)
    desc = ''
    m = _desc_re.search(src)
    if m:
        desc = html_mod.unescape(m.group(3).strip())
    if not title:
        title = slug.replace('-', ' ').title()
    return (title, desc)


def trim_excerpt(text, max_chars=160):
    if not text:
        return ''
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) <= max_chars:
        return text
    cut = text[:max_chars].rsplit(' ', 1)[0]
    return cut + '…'


# ---------------------------------------------------------------------------
# Page template
# ---------------------------------------------------------------------------
PAGE_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{cat_name} — SleepWise Reviews ({count} Articles)</title>
  <meta name="description" content="{meta_desc}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:title" content="{cat_name} — SleepWise Reviews" />
  <meta property="og:description" content="{meta_desc}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="https://sleepwisereviews.com/images/og-default.png" />
  <meta property="og:site_name" content="SleepWise Reviews" />
{schema_block}
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --bg: #0a1628; --card: #111e33; --gold: #c9a84c; --gold-dim: rgba(201,168,76,0.15);
      --text: #e8e0d0; --muted: #8899aa; --border: rgba(201,168,76,0.15);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: var(--bg); color: var(--text); font-family: 'Outfit', 'Georgia', sans-serif; line-height: 1.65; }}
    header {{ background: var(--card); border-bottom: 1px solid var(--border); padding: 1rem 3%; display: flex; align-items: center; justify-content: space-between; }}
    .logo {{ color: var(--gold); text-decoration: none; font-size: 1.3rem; font-weight: 700; }}
    .logo span {{ color: var(--text); }}
    header .home-link {{ color: var(--muted); font-size: 0.9rem; text-decoration: none; }}
    header .home-link:hover {{ color: var(--gold); }}
    main {{ max-width: 1400px; margin: 0 auto; padding: 2rem 3% 3rem; }}
    .breadcrumb {{ font-size: 0.88rem; color: var(--muted); margin-bottom: 1.2rem; }}
    .breadcrumb a {{ color: var(--gold); text-decoration: none; }}
    .breadcrumb a:hover {{ text-decoration: underline; }}
    .breadcrumb .sep {{ margin: 0 0.4rem; opacity: 0.6; }}
    .page-hero {{ margin-bottom: 1.5rem; }}
    h1 {{ font-size: 2.1rem; color: var(--gold); margin-bottom: 0.4rem; line-height: 1.2; }}
    .subtitle {{ color: var(--muted); font-size: 0.98rem; max-width: 720px; }}
    .search-wrap {{ margin: 1.5rem 0 2.2rem; position: relative; max-width: 720px; }}
    .search-wrap input {{
      width: 100%; padding: 0.85rem 1.2rem 0.85rem 3rem;
      background: var(--card); border: 1px solid var(--border);
      border-radius: 8px; color: var(--text); font-family: inherit; font-size: 1rem;
      outline: none; transition: border-color 0.2s;
    }}
    .search-wrap input:focus {{ border-color: var(--gold); }}
    .search-wrap input::placeholder {{ color: var(--muted); }}
    .search-wrap svg {{ position: absolute; left: 1rem; top: 50%; transform: translateY(-50%); opacity: 0.5; pointer-events: none; }}
    .card-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1.4rem; }}
    .article-card {{
      background: var(--card); border: 1px solid var(--border); border-radius: 12px;
      padding: 1.3rem 1.4rem; display: flex; flex-direction: column;
      transition: border-color 0.2s, transform 0.2s;
      text-decoration: none; color: var(--text);
    }}
    .article-card:hover {{ border-color: var(--gold); transform: translateY(-2px); }}
    .article-card h3 {{ font-size: 1.02rem; font-weight: 600; color: #f0e6c8; margin-bottom: 0.55rem; line-height: 1.35; }}
    .article-card .excerpt {{ font-size: 0.88rem; color: var(--muted); flex: 1; margin-bottom: 0.9rem; line-height: 1.55; }}
    .article-card .read-more {{ color: var(--gold); font-size: 0.85rem; font-weight: 600; }}
    .article-card.batch-hidden {{ display: none; }}
    .show-more-wrap {{ text-align: center; margin: 2.2rem 0 0.5rem; }}
    .show-more-btn {{
      display: inline-flex; align-items: center; gap: 0.5rem;
      padding: 0.85rem 1.8rem; border-radius: 10px;
      background: var(--gold-dim); color: var(--gold); border: 1px solid var(--gold);
      font-family: inherit; font-size: 0.95rem; font-weight: 600;
      cursor: pointer; text-decoration: none;
      transition: background 0.2s, color 0.2s;
    }}
    .show-more-btn:hover {{ background: var(--gold); color: #07101f; }}
    .show-more-count {{ color: var(--muted); font-size: 0.85rem; margin-top: 0.6rem; }}
    .no-results {{ display: none; background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 1.8rem 2rem; }}
    .no-results h3 {{ color: var(--gold); font-size: 1rem; margin-bottom: 0.5rem; }}
    .no-results p {{ color: var(--muted); font-size: 0.9rem; }}
    footer {{ text-align: center; padding: 2rem; color: var(--muted); font-size: 0.85rem; border-top: 1px solid var(--border); margin-top: 3rem; }}
    footer a {{ color: var(--gold); text-decoration: none; }}
    footer a:hover {{ text-decoration: underline; }}
    @media (max-width: 700px) {{
      h1 {{ font-size: 1.55rem; }}
      .card-grid {{ grid-template-columns: 1fr; gap: 1rem; }}
      main {{ padding: 1.5rem 4% 2rem; }}
    }}
  </style>
</head>
<body>
  <header>
    <a class="logo" href="../../">SleepWise<span>Reviews</span></a>
    <a class="home-link" href="../../">← Home</a>
  </header>
  <main>
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../">All Sleep Guides &amp; Articles</a>
      <span class="sep">›</span>
      <span>{cat_name}</span>
    </nav>
    <div class="page-hero">
      <h1>{cat_name}</h1>
      <p class="subtitle">{count} articles · {description}</p>
    </div>
    <div class="search-wrap">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
      <input type="text" id="search" placeholder="Search within {cat_name}..." autocomplete="off" />
    </div>
    <div class="no-results" id="no-results">
      <h3>No articles in this topic match your search</h3>
      <p>Try a different keyword, or <a href="../" style="color:var(--gold);">browse all topics</a>.</p>
    </div>
    <div class="card-grid" id="card-grid">
{cards_html}    </div>
{show_more_block}  </main>
  <footer>
    <p><a href="../">← Back to All Sleep Guides &amp; Articles</a></p>
    <p style="margin-top:0.6rem;">&copy; 2025-2026 <a href="../../">SleepWise Reviews</a> · Evidence-based sleep guidance</p>
  </footer>
  <script>
    (function() {{
      var input = document.getElementById('search');
      var noResults = document.getElementById('no-results');
      var grid = document.getElementById('card-grid');
      var showMoreBtn = document.getElementById('show-more');
      var cards = grid.querySelectorAll('.article-card');
      var showMoreClicked = false;

      function revealAll() {{
        for (var i = 0; i < cards.length; i++) {{
          cards[i].classList.remove('batch-hidden');
        }}
        if (showMoreBtn) showMoreBtn.parentNode.style.display = 'none';
        showMoreClicked = true;
      }}

      if (showMoreBtn) {{
        showMoreBtn.addEventListener('click', revealAll);
      }}

      input.addEventListener('input', function() {{
        var q = this.value.toLowerCase().trim();
        if (!q) {{
          for (var i = 0; i < cards.length; i++) cards[i].style.display = '';
          if (showMoreBtn && !showMoreClicked) showMoreBtn.parentNode.style.display = '';
          grid.style.display = '';
          noResults.style.display = 'none';
          return;
        }}
        if (showMoreBtn) showMoreBtn.parentNode.style.display = 'none';
        var anyVisible = false;
        for (var i = 0; i < cards.length; i++) {{
          var hay = cards[i].getAttribute('data-search') || '';
          var match = hay.indexOf(q) !== -1;
          cards[i].style.display = match ? 'flex' : 'none';
          if (match) anyVisible = true;
        }}
        noResults.style.display = anyVisible ? 'none' : 'block';
        grid.style.display = anyVisible ? '' : 'none';
      }});
    }})();
  </script>
</body>
</html>
'''


def build_card(slug, title, desc, hidden=False):
    excerpt = trim_excerpt(desc, 160)
    search_blob = (title + ' ' + (desc or '')).lower()
    title_html = html_mod.escape(title)
    excerpt_html = html_mod.escape(excerpt)
    cls = 'article-card batch-hidden' if hidden else 'article-card'
    return (
        f'      <a class="{cls}" href="../{slug}.html" '
        f'data-search="{html_mod.escape(search_blob, quote=True)}">\n'
        f'        <h3>{title_html}</h3>\n'
        f'        <p class="excerpt">{excerpt_html}</p>\n'
        f'        <span class="read-more">Read →</span>\n'
        f'      </a>\n'
    )


def build_category_page(cat_name, slug):
    article_slugs = CATEGORIES.get(cat_name, [])
    valid = [s for s in article_slugs if os.path.isfile(os.path.join(POSTS_DIR, s + '.html'))]
    cards = []
    for idx, s in enumerate(valid):
        title, desc = extract_meta(s)
        cards.append(build_card(s, title, desc, hidden=(idx >= INITIAL_VISIBLE)))

    hidden_count = max(0, len(valid) - INITIAL_VISIBLE)
    if hidden_count > 0:
        show_more_block = (
            '    <div class="show-more-wrap" id="show-more-wrap">\n'
            f'      <button type="button" class="show-more-btn" id="show-more">'
            f'Show all {len(valid)} articles</button>\n'
            f'      <p class="show-more-count">Showing {INITIAL_VISIBLE} of {len(valid)} · '
            f'or use the search above to find a specific topic</p>\n'
            '    </div>\n'
        )
    else:
        show_more_block = ''

    description = CAT_DESCRIPTIONS.get(slug, f'{cat_name} articles on SleepWise Reviews.')
    canonical = f'{BASE_URL}/posts/category/{slug}.html'
    meta_desc = f'{len(valid)} {cat_name.lower()} articles — {description}'
    if len(meta_desc) > 160:
        meta_desc = meta_desc[:157] + '...'

    schema = {
        '@context': 'https://schema.org',
        '@type': 'CollectionPage',
        'name': f'{cat_name} — SleepWise Reviews',
        'description': description,
        'url': canonical,
        'mainEntity': {
            '@type': 'ItemList',
            'numberOfItems': len(valid),
            'itemListElement': [
                {
                    '@type': 'ListItem',
                    'position': i + 1,
                    'url': f'{BASE_URL}/posts/{s}.html',
                }
                for i, s in enumerate(valid)
            ],
        },
        'publisher': {
            '@type': 'Organization',
            'name': 'SleepWise Reviews',
            'url': f'{BASE_URL}/',
        },
    }
    schema_block = '  <script type="application/ld+json">\n' + json.dumps(schema, indent=2) + '\n  </script>'

    page = PAGE_TEMPLATE.format(
        cat_name=html_mod.escape(cat_name),
        count=len(valid),
        description=html_mod.escape(description),
        meta_desc=html_mod.escape(meta_desc, quote=True),
        canonical=canonical,
        schema_block=schema_block,
        cards_html=''.join(cards),
        show_more_block=show_more_block,
    )

    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, slug + '.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(page)
    return out_path, len(valid)


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None
    if target:
        cat_name = SLUG_TO_NAME.get(target)
        if not cat_name:
            print(f'Unknown category slug: {target}')
            print(f'Valid: {sorted(SLUG_TO_NAME.keys())}')
            sys.exit(1)
        path, n = build_category_page(cat_name, target)
        print(f'Built {path} ({n} articles)')
    else:
        for cat_name, slug in CAT_ANCHOR.items():
            path, n = build_category_page(cat_name, slug)
            print(f'Built {path} ({n} articles)')


if __name__ == '__main__':
    main()
