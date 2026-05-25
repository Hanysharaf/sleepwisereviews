"""Add BreadcrumbList JSON-LD schema to all posts."""
import re, json, os

POSTS_DIR = os.path.join(os.path.dirname(__file__), 'posts')
BASE_URL = 'https://sleepwisereviews.com'

def make_breadcrumb(post_title, post_url):
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "SleepWise Reviews",
                "item": BASE_URL + "/"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Sleep Guides",
                "item": BASE_URL + "/posts/"
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": post_title,
                "item": post_url
            }
        ]
    }
    return '<script type="application/ld+json">\n' + json.dumps(schema, indent=2) + '\n</script>'

updated = 0
skipped = 0

for fname in sorted(os.listdir(POSTS_DIR)):
    if not fname.endswith('.html'):
        continue

    fpath = os.path.join(POSTS_DIR, fname)
    with open(fpath, encoding='utf-8') as f:
        html = f.read()

    if 'BreadcrumbList' in html:
        skipped += 1
        continue

    if '</head>' not in html:
        skipped += 1
        continue

    title_m = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL)
    raw_title = re.sub(r'<[^>]+>', '', title_m.group(1)).strip() if title_m else fname
    title = re.sub(r'\s*[|\-–]\s*(SleepWise.*|Sleep.*)$', '', raw_title).strip()

    post_url = f'{BASE_URL}/posts/{fname}'
    schema_block = make_breadcrumb(title, post_url)

    new_html = html.replace('</head>', schema_block + '\n</head>', 1)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_html)

    updated += 1

print(f'Updated: {updated}  Skipped: {skipped}')
