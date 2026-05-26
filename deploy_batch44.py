slugs = [
    ('best-mattress-gastroparesis', 'best-mattress-complex-regional-pain-syndrome', 'Best Mattress for Gastroparesis', '7 picks for delayed gastric emptying &mdash; left lateral decubitus positioning for gastric drainage, adjustable base HOB elevation, pylorus gravity management &amp; distinction from GERD esophageal mechanism.'),
    ('best-mattress-sleep-paralysis', 'best-mattress-gastroparesis', 'Best Mattress for Sleep Paralysis', '7 picks for isolated sleep paralysis &mdash; supine-episode prevention via sustained side-sleep surface design, REM-phase cooling, motion isolation &amp; distinction from narcolepsy &amp; PTSD nightmares.'),
    ('best-mattress-guillain-barre', 'best-mattress-sleep-paralysis', 'Best Mattress for Guillain-Barré Syndrome', '7 picks for GBS recovery phases &mdash; acute immobility pressure injury prevention, respiratory HOB elevation, remyelination sensory hypersensitivity management &amp; post-GBS fatigue arc support.'),
    ('best-mattress-dermatomyositis', 'best-mattress-guillain-barre', 'Best Mattress for Dermatomyositis', '7 picks for inflammatory myopathy with skin involvement &mdash; Gottron\'s papule pressure relief, proximal muscle weakness repositioning, ILD elevation &amp; calcinosis site cushioning.'),
    ('best-mattress-phantom-limb-pain', 'best-mattress-dermatomyositis', 'Best Mattress for Phantom Limb Pain', '7 picks for post-amputation sleep &mdash; residual limb pressure relief, phantom thermal sensation management, prosthetic removal compatibility &amp; stump neuroma compression prevention.'),
    ('best-mattress-morton-neuroma', 'best-mattress-phantom-limb-pain', 'Best Mattress for Morton\'s Neuroma', '7 picks for interdigital nerve compression &mdash; forefoot sinkage prevention, 3rd-4th metatarsal decompression, back-sleep forefoot positioning &amp; distinction from metatarsalgia &amp; plantar fasciitis.'),
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
