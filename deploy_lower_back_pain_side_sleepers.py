import subprocess

# 1 — Sitemap
content = open('sitemap.xml', encoding='utf-8').read()
entry = '''  <url>
    <loc>https://sleepwisereviews.com/posts/best-mattress-lower-back-pain-side-sleepers.html</loc>
    <lastmod>2026-05-25</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
</urlset>'''
content = content.replace('</urlset>', entry)
open('sitemap.xml', 'w', encoding='utf-8').write(content)
print('Sitemap URLs:', content.count('<loc>'))

# 2 — CATEGORIES (Health Conditions)
idx = open('generate_posts_index.py', encoding='utf-8').read()
old = "'best-mattress-combination-sleepers'"
new = "'best-mattress-combination-sleepers', 'best-mattress-lower-back-pain-side-sleepers'"
if old in idx and 'best-mattress-lower-back-pain-side-sleepers' not in idx:
    idx = idx.replace(old, new)
    open('generate_posts_index.py', 'w', encoding='utf-8').write(idx)
    print('CATEGORIES updated')
else:
    print('CATEGORIES already updated or anchor not found')

# 3 — Homepage card
html = open('index.html', encoding='utf-8').read()
anchor = '        <a class="article-card" href="posts/best-mattress-combination-sleepers.html">'
card = (
    '        <a class="article-card" href="posts/best-mattress-lower-back-pain-side-sleepers.html">\n'
    '          <div class="card-cat">Health Conditions</div>\n'
    '          <h3>Best Mattress for Lower Back Pain Side Sleepers 2025</h3>\n'
    '          <p>Side sleeping with lower back pain needs shoulder relief AND lumbar support. 7 zoned hybrids ranked for this dual requirement. Helix Midnight Luxe, Saatva, Casper Wave tested.</p>\n'
    '          <div class="card-meta"><span>7 Products Reviewed</span><span>May 2025</span></div>\n'
    '        </a>\n'
)
if anchor in html and 'best-mattress-lower-back-pain-side-sleepers' not in html:
    html = html.replace(anchor, card + anchor)
    open('index.html', 'w', encoding='utf-8').write(html)
    print('Homepage card inserted')
else:
    print('Homepage card already present or anchor not found')

# 4 — Regenerate posts index
result = subprocess.run(['python', 'generate_posts_index.py'], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print('STDERR:', result.stderr)

# 5 — Git
subprocess.run(['git', 'add',
    'posts/best-mattress-lower-back-pain-side-sleepers.html',
    'sitemap.xml',
    'generate_posts_index.py',
    'index.html',
    'posts/index.html'
], check=True)
result = subprocess.run(['git', 'commit', '-m',
    'feat(health): best-mattress-lower-back-pain-side-sleepers -- 379 URLs, dual shoulder+lumbar guide'
], capture_output=True, text=True)
print(result.stdout)
result = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print(result.stderr)
