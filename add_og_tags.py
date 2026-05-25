"""Add Open Graph and Twitter Card meta tags to all posts."""
import re, os

POSTS_DIR = os.path.join(os.path.dirname(__file__), 'posts')
BASE_URL = 'https://sleepwisereviews.com/posts/'
SITE_NAME = 'SleepWise Reviews'
OG_IMAGE = 'https://sleepwisereviews.com/images/og-default.png'

def make_og_block(title, description, url):
    return (
        f'  <meta property="og:title" content="{title}" />\n'
        f'  <meta property="og:description" content="{description}" />\n'
        f'  <meta property="og:type" content="article" />\n'
        f'  <meta property="og:url" content="{url}" />\n'
        f'  <meta property="og:site_name" content="{SITE_NAME}" />\n'
        f'  <meta property="og:image" content="{OG_IMAGE}" />\n'
        f'  <meta name="twitter:card" content="summary_large_image" />\n'
        f'  <meta name="twitter:title" content="{title}" />\n'
        f'  <meta name="twitter:description" content="{description}" />\n'
    )

updated = 0
fixed_url = 0
skipped = 0

for fname in sorted(os.listdir(POSTS_DIR)):
    if not fname.endswith('.html'):
        continue

    fpath = os.path.join(POSTS_DIR, fname)
    with open(fpath, encoding='utf-8') as f:
        html = f.read()

    page_url = BASE_URL + fname

    # Fix existing wrong URLs (github.io references)
    if 'og:url' in html and 'github.io' in html:
        html = re.sub(
            r'<meta property="og:url" content="[^"]*github\.io[^"]*" />',
            f'<meta property="og:url" content="{page_url}" />',
            html
        )
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        fixed_url += 1

    if 'og:title' in html:
        skipped += 1
        continue

    # Extract title and description
    title_m = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL)
    raw_title = re.sub(r'<[^>]+>', '', title_m.group(1)).strip() if title_m else fname
    # Strip site suffix
    title = re.sub(r'\s*[|\-–]\s*(SleepWise.*|Sleep.*)$', '', raw_title).strip()

    desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html)
    description = desc_m.group(1).strip() if desc_m else f'Expert guide to {title.lower()} — research-backed tips for better sleep.'

    # Escape for HTML attributes
    title_esc = title.replace('"', '&quot;')
    desc_esc = description[:200].replace('"', '&quot;')

    og_block = make_og_block(title_esc, desc_esc, page_url)

    # Inject before </head>
    if '</head>' not in html:
        skipped += 1
        continue

    new_html = html.replace('</head>', og_block + '</head>', 1)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_html)

    updated += 1

print(f'Added OG tags: {updated}')
print(f'Fixed wrong URLs: {fixed_url}')
print(f'Skipped (already had OG): {skipped}')
