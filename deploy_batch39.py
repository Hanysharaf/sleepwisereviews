slugs = [
    ('best-mattress-wrist-fracture-recovery', 'best-mattress-rib-fracture-recovery', 'Best Mattress for Wrist Fracture Recovery', '7 picks for distal radius &amp; ulna fractures &mdash; cast/splint accommodation, forearm elevation for edema, CRPS risk management &amp; 6-12 week healing arc support.'),
    ('best-mattress-ankle-fracture-recovery', 'best-mattress-wrist-fracture-recovery', 'Best Mattress for Ankle Fracture Recovery', '7 picks for bimalleolar &amp; trimalleolar fractures &mdash; boot accommodation, 15-20 degree ankle elevation, NWB crutch transfer safety &amp; plantarflexion prevention during sleep.'),
    ('best-mattress-hip-fracture-recovery', 'best-mattress-ankle-fracture-recovery', 'Best Mattress for Hip Fracture Recovery', '7 picks for post-surgical hip fractures &mdash; anti-rotation pillow positioning, log-roll transfer edge support, 90-degree precautions &amp; pressure ulcer prevention for elderly patients.'),
    ('best-mattress-post-spinal-fusion', 'best-mattress-hip-fracture-recovery', 'Best Mattress for Post Spinal Fusion', '7 picks for lumbar &amp; cervical fusion recovery &mdash; log-roll technique support, no-twist precautions, adjacent segment disease protection &amp; 3-12 month fusion healing arc.'),
    ('best-mattress-shoulder-replacement-recovery', 'best-mattress-post-spinal-fusion', 'Best Mattress for Shoulder Replacement Recovery', '7 picks for TSA &amp; reverse TSA recovery &mdash; sling accommodation, reclined sleeping weeks 0-6, glenohumeral prosthesis protection &amp; 9-12 month transition to flat sleeping.'),
    ('best-mattress-bunion-surgery-recovery', 'best-mattress-shoulder-replacement-recovery', 'Best Mattress for Bunion Surgery Recovery', '7 picks for hallux valgus correction recovery &mdash; surgical boot surface management, forefoot pressure avoidance, NWB transfer safety &amp; 6-12 week osteotomy healing support.'),
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
