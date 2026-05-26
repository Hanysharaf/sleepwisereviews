slugs = [
    ('best-mattress-spasticity', 'best-mattress-discogenic-pain', 'Best Mattress for Spasticity', '7 picks for UMN spasticity from MS, stroke &amp; SCI &mdash; velocity-dependent resistance management, Uhthoff phenomenon cooling, tactile trigger minimization &amp; nocturnal spasm positioning.'),
    ('best-mattress-ehlers-danlos-vascular', 'best-mattress-spasticity', 'Best Mattress for Vascular EDS', '7 picks for COL3A1 vascular Ehlers-Danlos &mdash; arterial fragility pressure management, bruise-prone skin protection, 32 mmHg threshold avoidance &amp; distinction from hypermobile EDS positioning.'),
    ('best-mattress-night-terrors', 'best-mattress-ehlers-danlos-vascular', 'Best Mattress for Night Terrors', '7 picks for NREM Stage 3 arousal disorder &mdash; deep sleep architecture support, heat-trigger reduction, motion isolation for partner safety &amp; distinction from nightmares &amp; REM sleep behavior disorder.'),
    ('best-mattress-sleep-bruxism', 'best-mattress-night-terrors', 'Best Mattress for Sleep Bruxism', '7 picks for nocturnal jaw clenching &amp; grinding &mdash; cervical alignment to reduce masseter-SCM cascade, thermal regulation for stage fragmentation, TMD distinction &amp; pillow height interaction.'),
    ('best-mattress-chronic-sinusitis', 'best-mattress-sleep-bruxism', 'Best Mattress for Chronic Sinusitis', '7 picks for perennial sinus inflammation &mdash; 10-15 degree head elevation for gravity drainage, VOC mucosal irritation reduction, dust mite allergen management &amp; CPAP-sinusitis overlap positioning.'),
    ('best-mattress-psoriasis', 'best-mattress-chronic-sinusitis', 'Best Mattress for Psoriasis', '7 picks for psoriasis plaque management during sleep &mdash; Koebner phenomenon prevention, heat-flare reduction via cooling surfaces, low-friction covers &amp; pressure relief at plaque-prone sites.'),
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
