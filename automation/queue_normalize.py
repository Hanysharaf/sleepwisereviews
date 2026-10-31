"""Mechanical fixes applied to every queued post before it goes live.

Standard library only. Idempotent: running it twice changes nothing the second time.
Fixes: category links to pages that do not exist, missing Instagram footer CTA,
missing Open Graph / Twitter tags, Amazon links without rel="sponsored nofollow",
Amazon links without the affiliate tag.
"""
import os
import re

AFFILIATE_TAG = "sleepwiserevi-20"
BASE_URL = "https://sleepwisereviews.com"
OG_IMAGE = BASE_URL + "/images/og-default.png"
AMAZON_REL = "nofollow noopener noreferrer sponsored"  # same value the live posts use

# Category pages the queued files link to but that were never created -> page that exists.
# practical/sleep-myths/sleep-health/sex-mattress/seasonal follow the remaps already done on live posts.
CATEGORY_MAP = {
    "category-practical.html": "category-guides.html",
    "category-sleep-myths.html": "category-sleep-science.html",
    "category-sleep-health.html": "category-sleep-science.html",
    "category-sex-mattress.html": "category-product-reviews.html",
    "category-seasonal.html": "category-sleep-science.html",
    "category-education.html": "category-sleep-science.html",
    "category-sex-sleep.html": "category-special-topics.html",
    "category-couples.html": "category-special-topics.html",
}

IG_BLOCK = (
    '      <div class="footer-col">\n'
    '        <h4>Follow Us</h4>\n'
    '        <ul>\n'
    '          <li><a href="https://www.instagram.com/sleepwise.reviews" target="_blank" '
    'rel="noopener noreferrer">Follow us on Instagram @sleepwise.reviews</a></li>\n'
    '        </ul>\n'
    '      </div>\n'
)

_CAT_HREF = re.compile(r'href="\.\./pages/(category-[a-z0-9-]+\.html)"')
_AMAZON_A = re.compile(r'<a\b[^>]*href="https?://(?:www\.)?amazon\.com[^"]*"[^>]*>', re.I)


def _fix_categories(html, pages_dir):
    def sub(m):
        name = m.group(1)
        if pages_dir and os.path.exists(os.path.join(pages_dir, name)):
            return m.group(0)
        return 'href="../pages/%s"' % CATEGORY_MAP.get(name, name)
    return _CAT_HREF.sub(sub, html)


def _fix_amazon_tag(a):
    def sub(m):
        url = m.group(1)
        if "tag=" in url:
            return m.group(0)
        return 'href="%s%stag=%s"' % (url, "&" if "?" in url else "?", AFFILIATE_TAG)
    return re.sub(r'href="(https?://(?:www\.)?amazon\.com[^"]*)"', sub, a, count=1)


def _fix_amazon(html):
    def sub(m):
        a = _fix_amazon_tag(m.group(0))
        rel = re.search(r'\srel="([^"]*)"', a)
        if rel and "sponsored" in rel.group(1).split() and "nofollow" in rel.group(1).split():
            return a
        if rel:
            return a.replace(rel.group(0), ' rel="%s"' % AMAZON_REL, 1)
        return a[:-1] + ' rel="%s">' % AMAZON_REL
    return _AMAZON_A.sub(sub, html)


def _fix_og(html, filename):
    title_m = re.search(r"<title>(.*?)</title>", html, re.S)
    desc_m = re.search(r'<meta name="description" content="([^"]*)"', html)
    title = title_m.group(1).strip() if title_m else ""
    title = re.sub(r"\s+-\s+SleepWiseReviews$", "", title)
    desc = desc_m.group(1) if desc_m else ""
    props = [
        ('property="og:title"', '<meta property="og:title" content="%s" />' % title),
        ('property="og:description"', '<meta property="og:description" content="%s" />' % desc),
        ('property="og:type"', '<meta property="og:type" content="article" />'),
        ('property="og:url"', '<meta property="og:url" content="%s/posts/%s" />' % (BASE_URL, filename)),
        ('property="og:site_name"', '<meta property="og:site_name" content="SleepWise Reviews" />'),
        ('property="og:image"', '<meta property="og:image" content="%s" />' % OG_IMAGE),
        ('name="twitter:card"', '<meta name="twitter:card" content="summary_large_image" />'),
        ('name="twitter:title"', '<meta name="twitter:title" content="%s" />' % title),
        ('name="twitter:description"', '<meta name="twitter:description" content="%s" />' % desc),
    ]
    add = "".join("  %s\n" % tag for key, tag in props if key not in html)
    if add and "</head>" in html:
        html = html.replace("</head>", add + "</head>", 1)
    return html


def _fix_ig(html):
    if "instagram.com/sleepwise.reviews" in html:
        return html
    for marker in ('<div class="footer-bottom">', "</footer>"):
        if marker in html:
            return html.replace(marker, IG_BLOCK + marker, 1)
    return html


def normalize_html(html, filename, pages_dir=None):
    html = _fix_categories(html, pages_dir)
    html = _fix_amazon(html)
    html = _fix_og(html, filename)
    html = _fix_ig(html)
    return html
