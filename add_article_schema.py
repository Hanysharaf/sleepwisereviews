"""Add Article JSON-LD schema to all editorial (non-best-of) posts."""
import re, json, os
from datetime import datetime

POSTS_DIR = os.path.join(os.path.dirname(__file__), 'posts')
BASE_URL = 'https://sleepwisereviews.com/posts/'
AUTHOR = {
    "@type": "Organization",
    "name": "SleepWise Reviews",
    "url": "https://sleepwisereviews.com/"
}
PUBLISHER = {
    "@type": "Organization",
    "name": "SleepWise Reviews",
    "logo": {
        "@type": "ImageObject",
        "url": "https://sleepwisereviews.com/images/og-default.png"
    }
}
DATE_PUBLISHED = "2025-09-01"  # site launch approximate date
DATE_MODIFIED = datetime.now().strftime('%Y-%m-%d')

BEST_OF_PREFIX = 'best-'

def make_article_schema(title, description, url):
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title[:110],
        "description": description[:300],
        "url": url,
        "image": "https://sleepwisereviews.com/images/og-default.png",
        "datePublished": DATE_PUBLISHED,
        "dateModified": DATE_MODIFIED,
        "author": AUTHOR,
        "publisher": PUBLISHER,
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": url
        }
    }

updated = 0
skipped = 0

for fname in sorted(os.listdir(POSTS_DIR)):
    if not fname.endswith('.html'):
        continue

    # Skip best-of posts (they already have ItemList schema; Article may conflict)
    if fname.startswith(BEST_OF_PREFIX):
        skipped += 1
        continue

    fpath = os.path.join(POSTS_DIR, fname)
    with open(fpath, encoding='utf-8') as f:
        html = f.read()

    if '"Article"' in html or '"NewsArticle"' in html:
        skipped += 1
        continue

    if '</head>' not in html:
        skipped += 1
        continue

    title_m = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL)
    raw_title = re.sub(r'<[^>]+>', '', title_m.group(1)).strip() if title_m else fname
    title = re.sub(r'\s*[|\-–]\s*(SleepWise.*|Sleep.*)$', '', raw_title).strip()

    desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html)
    description = desc_m.group(1).strip() if desc_m else title

    url = BASE_URL + fname
    schema = make_article_schema(title, description, url)
    block = '<script type="application/ld+json">\n' + json.dumps(schema, indent=2) + '\n</script>'

    new_html = html.replace('</head>', block + '\n</head>', 1)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_html)

    updated += 1

print(f'Updated: {updated}  Skipped: {skipped}')
