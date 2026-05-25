import subprocess

content = open('sitemap.xml', encoding='utf-8').read()
entry = '''  <url>
    <loc>https://sleepwisereviews.com/posts/best-cooling-mattress-hot-sleepers.html</loc>
    <lastmod>2026-05-25</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
</urlset>'''
content = content.replace('</urlset>', entry)
open('sitemap.xml', 'w', encoding='utf-8').write(content)
print('Sitemap URLs:', content.count('<loc>'))

idx = open('generate_posts_index.py', encoding='utf-8').read()
old = "'best-mattress-heavy-side-sleepers'"
new = "'best-mattress-heavy-side-sleepers', 'best-cooling-mattress-hot-sleepers'"
if old in idx and 'best-cooling-mattress-hot-sleepers' not in idx:
    idx = idx.replace(old, new)
    open('generate_posts_index.py', 'w', encoding='utf-8').write(idx)
    print('CATEGORIES updated')

html = open('index.html', encoding='utf-8').read()
anchor = '        <a class="article-card" href="posts/best-mattress-heavy-side-sleepers.html">'
card = (
    '        <a class="article-card" href="posts/best-cooling-mattress-hot-sleepers.html">\n'
    '          <div class="card-cat">Mattresses &amp; Bedding</div>\n'
    '          <h3>Best Cooling Mattress for Hot Sleepers 2025</h3>\n'
    '          <p>Waking up sweating ruins sleep quality. 7 mattresses ranked by airflow tech, gel infusions, phase change materials, and all-night cooling performance. Purple, Saatva, Bear, Casper tested.</p>\n'
    '          <div class="card-meta"><span>7 Products Reviewed</span><span>May 2025</span></div>\n'
    '        </a>\n'
)
if anchor in html and 'best-cooling-mattress-hot-sleepers' not in html:
    html = html.replace(anchor, card + anchor)
    open('index.html', 'w', encoding='utf-8').write(html)
    print('Homepage card inserted')

result = subprocess.run(['python', 'generate_posts_index.py'], capture_output=True, text=True)
print(result.stdout)

subprocess.run(['git', 'add',
    'posts/best-cooling-mattress-hot-sleepers.html',
    'sitemap.xml', 'generate_posts_index.py', 'index.html', 'posts/index.html'
], check=True)
result = subprocess.run(['git', 'commit', '-m',
    'feat(mattress): best-cooling-mattress-hot-sleepers -- 374 URLs, cooling tech comparison guide'
], capture_output=True, text=True)
print(result.stdout)
result = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print(result.stderr)
