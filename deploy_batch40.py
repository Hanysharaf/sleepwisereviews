slugs = [
    ('best-mattress-cervical-radiculopathy', 'best-mattress-bunion-surgery-recovery', 'Best Mattress for Cervical Radiculopathy', '7 picks for C5-C8 nerve root compression &mdash; pillow height for cervical lordosis, shoulder sinkage to reduce foraminal narrowing, arm positioning by nerve level &amp; brachial plexus tension management.'),
    ('best-mattress-lumbar-radiculopathy', 'best-mattress-cervical-radiculopathy', 'Best Mattress for Lumbar Radiculopathy', '7 picks for L4-S1 nerve root compression &mdash; lumbar lordosis maintenance, leg pillow to reduce straight-leg tension, dermatomal level-specific positioning &amp; foraminal stenosis relief.'),
    ('best-mattress-vertebral-compression-fracture', 'best-mattress-lumbar-radiculopathy', 'Best Mattress for Vertebral Compression Fracture', '7 picks for osteoporotic VCF recovery &mdash; TLSO brace accommodation, kyphosis progression prevention, log-roll technique support &amp; post-kyphoplasty positioning for elderly patients.'),
    ('best-mattress-whiplash', 'best-mattress-vertebral-compression-fracture', 'Best Mattress for Whiplash', '7 picks for cervical WAD Grade I-IV &mdash; pillow height for neutral lordosis, motion isolation for acute phase, soft tissue 6-12 week healing support &amp; chronic WAD conversion risk reduction.'),
    ('best-mattress-knee-cartilage-repair', 'best-mattress-whiplash', 'Best Mattress for Knee Cartilage Repair', '7 picks for microfracture, MACI &amp; OAT procedures &mdash; cartilage graft protection during NWB phase, CPM machine accommodation, 9-18 month recovery arc &amp; extended trial strategy.'),
    ('best-mattress-plantar-plate-injury', 'best-mattress-knee-cartilage-repair', 'Best Mattress for Plantar Plate Injury', '7 picks for 2nd MTP joint plantar plate tears &mdash; forefoot sinkage prevention, dorsiflexion avoidance during sleep, crossover toe deformity prevention &amp; 6-12 week healing support.'),
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
