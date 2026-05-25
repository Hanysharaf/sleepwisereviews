import re

# 1. Sitemap
sitemap_path = 'sitemap.xml'
content = open(sitemap_path, encoding='utf-8').read()
entry = '''  <url>
    <loc>https://sleepwisereviews.com/posts/best-queen-size-mattress.html</loc>
    <lastmod>2026-05-25</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
</urlset>'''
content = content.replace('</urlset>', entry)
open(sitemap_path, 'w', encoding='utf-8').write(content)
print('Sitemap URLs:', content.count('<loc>'))

# 2. CATEGORIES in generate_posts_index.py
idx_path = 'generate_posts_index.py'
idx = open(idx_path, encoding='utf-8').read()
old = "'best-firm-mattress'"
new = "'best-firm-mattress', 'best-queen-size-mattress'"
if old in idx and 'best-queen-size-mattress' not in idx:
    idx = idx.replace(old, new)
    open(idx_path, 'w', encoding='utf-8').write(idx)
    print('CATEGORIES updated')
else:
    print('CATEGORIES already updated or anchor not found')

# 3. Homepage card — insert BEFORE best-firm-mattress, matching card-cat format
idx_html = 'index.html'
content = open(idx_html, encoding='utf-8').read()
anchor = '        <a class="article-card" href="posts/best-firm-mattress.html">'
new_card = (
    '        <a class="article-card" href="posts/best-queen-size-mattress.html">\n'
    '          <div class="card-cat">Mattresses &amp; Bedding</div>\n'
    '          <h3>Best Queen Size Mattress 2025</h3>\n'
    '          <p>The most-bought mattress size tested head-to-head -- 7 queen mattresses ranked for couples, solo sleepers, and value hunters. Saatva, DreamCloud, Purple, Nectar, Helix, Leesa, Casper reviewed.</p>\n'
    '          <div class="card-meta"><span>7 Products Reviewed</span><span>May 2025</span></div>\n'
    '        </a>\n'
)
if anchor in content and 'best-queen-size-mattress' not in content:
    content = content.replace(anchor, new_card + anchor)
    open(idx_html, 'w', encoding='utf-8').write(content)
    print('Homepage card inserted')
else:
    print('Anchor not found or card already present')
