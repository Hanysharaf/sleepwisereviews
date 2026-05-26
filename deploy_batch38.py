slugs = [
    ('best-mattress-stress-fracture', 'best-mattress-hip-labral-tear', 'Best Mattress for Stress Fracture', '7 picks for tibial &amp; femoral bone stress fractures &mdash; weight-off-loading during sleep, boot/cast accommodation, bone edema elevation &amp; cortical fracture site pressure mapping.'),
    ('best-mattress-meniscus-tear', 'best-mattress-stress-fracture', 'Best Mattress for Meniscus Tear', '7 picks for medial &amp; lateral meniscal damage &mdash; knee flexion/rotation avoidance, post-meniscectomy vs. repair positioning, leg elevation for swelling &amp; pillow-between-knees technique.'),
    ('best-mattress-acl-reconstruction-recovery', 'best-mattress-meniscus-tear', 'Best Mattress for ACL Reconstruction Recovery', '7 picks for post-surgical ACL graft protection &mdash; brace accommodation, ligamentization arc support, quad inhibition positioning &amp; 9-12 month recovery trial strategy.'),
    ('best-mattress-shoulder-labral-tear', 'best-mattress-acl-reconstruction-recovery', 'Best Mattress for Shoulder Labral Tear', '7 picks for glenoid labral &amp; SLAP tears &mdash; affected-shoulder compression avoidance, biceps anchor unloading, glenohumeral impingement reduction &amp; post-surgical arm positioning.'),
    ('best-mattress-nerve-impingement', 'best-mattress-shoulder-labral-tear', 'Best Mattress for Nerve Impingement', '7 picks for cervical &amp; lumbar nerve root compression &mdash; foraminal stenosis relief, spinal decompression during sleep, arm/leg positioning for C6-C7 &amp; L4-S1 tension reduction.'),
    ('best-mattress-rib-fracture-recovery', 'best-mattress-nerve-impingement', 'Best Mattress for Rib Fracture Recovery', '7 picks for rib fracture healing &mdash; lateral thoracic pressure minimization, respiratory splinting prevention, breathing mechanics by sleep position &amp; 6-8 week healing timeline support.'),
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
