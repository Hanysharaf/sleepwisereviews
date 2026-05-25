"""Add ItemList JSON-LD schema to best-of posts."""
import re, json, os
from urllib.parse import urlparse, parse_qs

POSTS_DIR = os.path.join(os.path.dirname(__file__), 'posts')

# Generic k= values to exclude from ItemList (category searches, not products)
GENERIC_TERMS = {
    'sleep supplements', 'sleep products', 'sleep mask', 'weighted blanket',
    'blackout curtains', 'cooling pillow', 'sleep tracker', 'sleep ring',
    'smart mattress', 'mattress topper', 'melatonin', 'valerian root',
    'blue light glasses', 'light therapy lamp', 'sleep monitor', 'sleep app',
    'sleep headphones', 'grounding sheets', 'humidifier', 'aromatherapy diffuser',
    'cpap alternative', 'anti snoring device', 'pillow', 'mattress',
    'blackout', 'curtains', 'lamps', 'rings', 'glasses',
}

def k_to_name(k_param):
    """Convert URL k= parameter to title-cased product name."""
    name = k_param.replace('+', ' ').replace('%20', ' ')
    # Title case but keep brand abbreviations uppercase
    words = name.split()
    result = []
    for w in words:
        if re.match(r'^[A-Z]{2,}$', w) or re.match(r'^\d', w):
            result.append(w)
        else:
            result.append(w.capitalize())
    return ' '.join(result)

def extract_products(html):
    """Extract product names and Amazon links from HTML."""
    # Try product-title divs first (structured posts)
    titles = re.findall(r'<div class="product-title">(.*?)</div>', html)
    links = re.findall(r'href="(https://www\.amazon\.com/s\?k=[^"]+)"', html)

    if titles and len(titles) >= 3:
        # Pair titles with their links (titles appear in order alongside links)
        # Filter links to only specific product ones (not generic)
        specific_links = []
        for l in links:
            qs = parse_qs(urlparse(l).query)
            k = qs.get('k', [''])[0].replace('+', ' ').lower()
            if k not in GENERIC_TERMS and len(k) > 10:
                specific_links.append(l)

        products = []
        for i, title in enumerate(titles):
            clean_title = re.sub(r'<[^>]+>', '', title).strip()
            link = specific_links[i] if i < len(specific_links) else None
            products.append((clean_title, link))
        return products

    # Fall back to decoding k= params
    specific_links = []
    for l in links:
        qs = parse_qs(urlparse(l).query)
        k = qs.get('k', [''])[0].replace('+', ' ').lower()
        if k not in GENERIC_TERMS and len(k) > 12:
            specific_links.append((l, k))

    # Deduplicate by k value
    seen = set()
    products = []
    for l, k in specific_links:
        if k not in seen:
            seen.add(k)
            products.append((k_to_name(k), l))

    return products

def make_itemlist_schema(title, url, products):
    items = []
    for i, (name, prod_url) in enumerate(products, 1):
        item = {
            "@type": "ListItem",
            "position": i,
            "name": name,
        }
        if prod_url:
            item["url"] = prod_url
        items.append(item)

    schema = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": title,
        "url": url,
        "numberOfItems": len(products),
        "itemListElement": items
    }
    return '<script type="application/ld+json">\n' + json.dumps(schema, indent=2) + '\n</script>'

BEST_OF_FILES = [
    'best-anti-snoring-devices.html',
    'best-aromatherapy-sleep.html',
    'best-blackout-curtains.html',
    'best-blue-light-glasses.html',
    'best-cooling-mattress-pads.html',
    'best-cooling-pillows.html',
    'best-cpap-alternatives.html',
    'best-grounding-sheets.html',
    'best-humidifiers-sleep.html',
    'best-light-therapy-lamps.html',
    'best-mattress-toppers.html',
    'best-mattresses-back-pain.html',
    'best-mattresses-couples-2026.html',
    'best-melatonin-supplements.html',
    'best-pillow-sleep-position.html',
    'best-sleep-apps.html',
    'best-sleep-headphones.html',
    'best-sleep-masks.html',
    'best-sleep-monitors.html',
    'best-sleep-position.html',
    'best-sleep-supplements-guide.html',
    'best-sleep-tracking-rings.html',
    'best-smart-mattresses.html',
    'best-valerian-root-supplements.html',
]

BASE_URL = 'https://sleepwisereviews.com/posts/'

updated = 0
skipped = 0

for fname in BEST_OF_FILES:
    fpath = os.path.join(POSTS_DIR, fname)
    if not os.path.exists(fpath):
        print(f'MISSING: {fname}')
        skipped += 1
        continue

    with open(fpath, encoding='utf-8') as f:
        html = f.read()

    if 'ItemList' in html:
        print(f'SKIP (has ItemList): {fname}')
        skipped += 1
        continue

    if '</head>' not in html:
        print(f'SKIP (no </head>): {fname}')
        skipped += 1
        continue

    # Extract page title
    title_m = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL)
    page_title = re.sub(r'<[^>]+>', '', title_m.group(1)).strip() if title_m else fname.replace('.html', '').replace('-', ' ').title()
    # Strip site name suffix if present
    page_title = re.sub(r'\s*[|\-–]\s*Sleep.*$', '', page_title).strip()

    products = extract_products(html)
    if len(products) < 2:
        print(f'SKIP (too few products={len(products)}): {fname}')
        skipped += 1
        continue

    page_url = BASE_URL + fname
    schema_block = make_itemlist_schema(page_title, page_url, products)

    new_html = html.replace('</head>', schema_block + '\n</head>', 1)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f'OK: {fname} ({len(products)} items)')
    updated += 1

print(f'\nUpdated: {updated}  Skipped: {skipped}')
