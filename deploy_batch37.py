slugs = [
    ('best-mattress-shin-splints', 'best-mattress-patellar-tendinopathy', 'Best Mattress for Shin Splints', '7 picks for medial tibial stress syndrome &mdash; bedding weight on periosteum, prone loading avoidance, lower-leg elevation &amp; morning stiffness differentiation from stress fracture.'),
    ('best-mattress-rotator-cuff-tear', 'best-mattress-shin-splints', 'Best Mattress for Rotator Cuff Tear', '7 picks for supraspinatus &amp; infraspinatus tears &mdash; affected-shoulder compression avoidance, post-surgical sling accommodation, subacromial pressure reduction &amp; contralateral arm positioning.'),
    ('best-mattress-achilles-rupture-recovery', 'best-mattress-rotator-cuff-tear', 'Best Mattress for Achilles Rupture Recovery', '7 picks for post-rupture &amp; surgical recovery &mdash; boot/cast accommodation, equinus contracture prevention, 15-25 degree elevation protocol &amp; NWB transfer safety.'),
    ('best-mattress-hamstring-tendinopathy', 'best-mattress-achilles-rupture-recovery', 'Best Mattress for Hamstring Tendinopathy', '7 picks for proximal hamstring tendinopathy &mdash; ischial tuberosity compression avoidance, hip flexion tensile loading reduction, deep hip flexion avoidance &amp; morning gel phenomenon management.'),
    ('best-mattress-iliotibial-band-syndrome', 'best-mattress-hamstring-tendinopathy', 'Best Mattress for IT Band Syndrome', '7 picks for iliotibial band friction &mdash; lateral knee pressure relief in side sleeping, hip alignment for TFL tension reduction, zoned support &amp; pelvic drop prevention.'),
    ('best-mattress-hip-labral-tear', 'best-mattress-iliotibial-band-syndrome', 'Best Mattress for Hip Labral Tear', '7 picks for acetabular labral damage &mdash; deep hip flexion avoidance, mattress sinkage impingement prevention, FAI accommodation &amp; side-lying labral protection strategies.'),
]

with open('sitemap.xml', 'r', encoding='utf-8') as f:
    sitemap = f.read()
with open('generate_posts_index.py', 'r', encoding='utf-8') as f:
    gen = f.read()
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

anchor = '<a class="article-card" href="posts/best-mattress-arthritis.html">'

for slug, prev_slug, title, desc in slugs:
    entry_check = 'posts/' + slug + '.html'
    if entry_check not in sitemap:
        entry = '  <url>\n    <loc>https://sleepwisereviews.com/posts/' + slug + '.html</loc>\n    <lastmod>2026-05-26</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n</urlset>'
        sitemap = sitemap.replace('</urlset>', entry)
        print('Sitemap: added ' + slug)
    else:
        print('Sitemap: already has ' + slug)
    if slug not in gen:
        gen = gen.replace("'" + prev_slug + "'", "'" + prev_slug + "', '" + slug + "'")
        print('CATEGORIES: added ' + slug)
    else:
        print('CATEGORIES: already has ' + slug)
    card_check = 'href="posts/' + slug + '.html"'
    if card_check not in html:
        card = (
            '        <div class="card-cat">\n'
            '          <span class="cat-badge" style="background:#dc2626">Health</span>\n'
            '          <h3><a href="posts/' + slug + '.html">' + title + '</a></h3>\n'
            '          <p>' + desc + '</p>\n'
            '          <div class="card-meta"><span>7 picks</span><span>Health</span></div>\n'
            '        </div>\n'
            '        '
        )
        html = html.replace(anchor, card + anchor)
        print('Card: added ' + slug)
    else:
        print('Card: already has ' + slug)

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap)
with open('generate_posts_index.py', 'w', encoding='utf-8') as f:
    f.write(gen)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Sitemap now has', sitemap.count('<loc>'), 'URLs')
