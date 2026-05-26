slugs = [
    ('best-mattress-polycythemia-vera', 'best-mattress-addisons-disease', 'Best Mattress for Polycythemia Vera', '7 picks for JAK2 V617F myeloproliferative sleep disruption &mdash; hyperviscosity thrombosis risk positioning, aquagenic pruritus surface management, splenomegaly abdominal accommodation &amp; erythromelalgia thermal control.'),
    ('best-mattress-wilson-disease', 'best-mattress-polycythemia-vera', 'Best Mattress for Wilson\'s Disease', '7 picks for ATP7B copper accumulation &mdash; basal ganglia movement disorder management, hepatic encephalopathy sleep reversal support, copper arthropathy joint cushioning &amp; distinction from hemochromatosis.'),
    ('best-mattress-hemochromatosis', 'best-mattress-wilson-disease', 'Best Mattress for Hemochromatosis', '7 picks for HFE C282Y iron overload &mdash; MCP joint arthropathy pressure relief, hepatic fatigue support, iron cardiomyopathy positioning &amp; phlebotomy recovery comfort.'),
    ('best-mattress-porphyria', 'best-mattress-hemochromatosis', 'Best Mattress for Porphyria', '7 picks for heme biosynthesis defect &mdash; cutaneous photosensitivity light management, acute crisis abdominal pain, peripheral neuropathy allodynia surfaces &amp; AIP vs. PCT distinction.'),
    ('best-mattress-pheochromocytoma', 'best-mattress-porphyria', 'Best Mattress for Pheochromocytoma', '7 picks for chromaffin catecholamine excess &mdash; paroxysmal hypertension low-pressure surfaces, adrenergic crisis sweating management, post-surgical adrenal insufficiency &amp; distinction from paraganglioma.'),
    ('best-mattress-amyloidosis', 'best-mattress-pheochromocytoma', 'Best Mattress for Amyloidosis', '7 picks for amyloid fibril deposition &mdash; carpal tunnel wrist-neutral positioning, cardiac amyloid orthopnea elevation, macroglossia airway management &amp; AL vs. ATTR distinction.'),
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
