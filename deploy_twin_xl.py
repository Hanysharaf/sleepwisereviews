content = open('sitemap.xml', encoding='utf-8').read()
entry = '''  <url>
    <loc>https://sleepwisereviews.com/posts/best-twin-xl-mattress.html</loc>
    <lastmod>2026-05-25</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
</urlset>'''
content = content.replace('</urlset>', entry)
open('sitemap.xml', 'w', encoding='utf-8').write(content)
print('Sitemap URLs:', content.count('<loc>'))

idx = open('generate_posts_index.py', encoding='utf-8').read()
old = "'best-plush-mattress'"
new = "'best-plush-mattress', 'best-twin-xl-mattress'"
if old in idx and 'best-twin-xl-mattress' not in idx:
    idx = idx.replace(old, new)
    open('generate_posts_index.py', 'w', encoding='utf-8').write(idx)
    print('CATEGORIES updated')

html = open('index.html', encoding='utf-8').read()
anchor = '        <a class="article-card" href="posts/best-plush-mattress.html">'
card = (
    '        <a class="article-card" href="posts/best-twin-xl-mattress.html">\n'
    '          <div class="card-cat">Mattresses &amp; Bedding</div>\n'
    '          <h3>Best Twin XL Mattress 2025</h3>\n'
    '          <p>College dorms, adjustable bases, tall sleepers -- 7 Twin XL mattresses ranked by trial, cooling, and durability. Saatva, Nectar, Purple, Casper, Helix, and more.</p>\n'
    '          <div class="card-meta"><span>7 Products Reviewed</span><span>May 2025</span></div>\n'
    '        </a>\n'
)
if anchor in html and 'best-twin-xl-mattress' not in html:
    html = html.replace(anchor, card + anchor)
    open('index.html', 'w', encoding='utf-8').write(html)
    print('Homepage card inserted')
