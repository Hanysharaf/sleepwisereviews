import re

# Sitemap
content = open('sitemap.xml', encoding='utf-8').read()
entry = '''  <url>
    <loc>https://sleepwisereviews.com/posts/best-plush-mattress.html</loc>
    <lastmod>2026-05-25</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
</urlset>'''
content = content.replace('</urlset>', entry)
open('sitemap.xml', 'w', encoding='utf-8').write(content)
print('Sitemap URLs:', content.count('<loc>'))

# CATEGORIES
idx = open('generate_posts_index.py', encoding='utf-8').read()
old = "'best-pillow-top-mattress'"
new = "'best-pillow-top-mattress', 'best-plush-mattress'"
if old in idx and 'best-plush-mattress' not in idx:
    idx = idx.replace(old, new)
    open('generate_posts_index.py', 'w', encoding='utf-8').write(idx)
    print('CATEGORIES updated')
else:
    print('Already updated')

# Homepage card
html = open('index.html', encoding='utf-8').read()
anchor = '        <a class="article-card" href="posts/best-pillow-top-mattress.html">'
new_card = (
    '        <a class="article-card" href="posts/best-plush-mattress.html">\n'
    '          <div class="card-cat">Mattresses &amp; Bedding</div>\n'
    '          <h3>Best Plush Mattress 2025</h3>\n'
    '          <p>Soft without sag -- 7 plush mattresses tested for pressure relief, cooling, and durability. Saatva, Nectar, Purple, Helix, Casper, and more ranked by real-world results.</p>\n'
    '          <div class="card-meta"><span>7 Products Reviewed</span><span>May 2025</span></div>\n'
    '        </a>\n'
)
if anchor in html and 'best-plush-mattress' not in html:
    html = html.replace(anchor, new_card + anchor)
    open('index.html', 'w', encoding='utf-8').write(html)
    print('Homepage card inserted')
else:
    print('Already present or anchor not found')
