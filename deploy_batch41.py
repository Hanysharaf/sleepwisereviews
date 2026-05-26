slugs = [
    ('best-mattress-thoracic-spine-pain', 'best-mattress-plantar-plate-injury', 'Best Mattress for Thoracic Spine Pain', '7 picks for mid-back T1-T12 pain &mdash; thoracic kyphosis prevention, facet &amp; rib articulation pressure relief, Scheuermann\'s disease support &amp; prone sleeping tradeoff management.'),
    ('best-mattress-coccydynia', 'best-mattress-thoracic-spine-pain', 'Best Mattress for Coccydynia', '7 picks for tailbone &amp; coccyx pain &mdash; sacrococcygeal pressure suspension, supine sleeping modifications, coccygeal cushion compatibility &amp; post-traumatic fracture recovery support.'),
    ('best-mattress-lymphedema', 'best-mattress-coccydynia', 'Best Mattress for Lymphedema', '7 picks for primary &amp; secondary lymphedema &mdash; gravity-dependent lymphatic drainage optimization, arm vs. leg elevation angles, compression garment accommodation &amp; lymph capillary pressure management.'),
    ('best-mattress-pelvic-girdle-pain', 'best-mattress-lymphedema', 'Best Mattress for Pelvic Girdle Pain', '7 picks for SPD &amp; sacroiliac instability &mdash; hip adduction avoidance, relaxin-driven ligament laxity support, pillow-between-knees mechanics &amp; postpartum PGP resolution.'),
    ('best-mattress-myofascial-pain-syndrome', 'best-mattress-pelvic-girdle-pain', 'Best Mattress for Myofascial Pain Syndrome', '7 picks for trigger point pain &mdash; pressure mapping over active trigger points, referred pain pattern management, local energy crisis prevention &amp; distinction from fibromyalgia central sensitization.'),
    ('best-mattress-discogenic-pain', 'best-mattress-myofascial-pain-syndrome', 'Best Mattress for Discogenic Pain', '7 picks for internal disc disruption &mdash; annular tear intradiscal pressure reduction, lumbar lordosis maintenance, morning stiffness from disc imbibition &amp; distinction from herniated disc and DDD.'),
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
