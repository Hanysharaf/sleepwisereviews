import re

# 1. Sitemap
content = open('sitemap.xml', encoding='utf-8').read()
entry = '''  <url>
    <loc>https://sleepwisereviews.com/posts/best-pillow-top-mattress.html</loc>
    <lastmod>2026-05-25</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
</urlset>'''
content = content.replace('</urlset>', entry)
open('sitemap.xml', 'w', encoding='utf-8').write(content)
print('Sitemap URLs:', content.count('<loc>'))

# 2. CATEGORIES
idx = open('generate_posts_index.py', encoding='utf-8').read()
old = "'best-queen-size-mattress'"
new = "'best-queen-size-mattress', 'best-pillow-top-mattress'"
if old in idx and 'best-pillow-top-mattress' not in idx:
    idx = idx.replace(old, new)
    open('generate_posts_index.py', 'w', encoding='utf-8').write(idx)
    print('CATEGORIES updated')
else:
    print('Already updated or anchor not found')

# 3. Homepage card
html = open('index.html', encoding='utf-8').read()
anchor = '        <a class="article-card" href="posts/best-queen-size-mattress.html">'
new_card = (
    '        <a class="article-card" href="posts/best-pillow-top-mattress.html">\n'
    '          <div class="card-cat">Mattresses &amp; Bedding</div>\n'
    '          <h3>Best Pillow Top Mattress 2025</h3>\n'
    '          <p>Cloud-like comfort meets real support -- 7 pillow top mattresses tested for plushness, durability, and sag resistance. Saatva, WinkBed, Beautyrest, and more ranked.</p>\n'
    '          <div class="card-meta"><span>7 Products Reviewed</span><span>May 2025</span></div>\n'
    '        </a>\n'
)
if anchor in html and 'best-pillow-top-mattress' not in html:
    html = html.replace(anchor, new_card + anchor)
    open('index.html', 'w', encoding='utf-8').write(html)
    print('Homepage card inserted')
else:
    print('Anchor not found or already present')
