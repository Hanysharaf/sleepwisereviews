slugs = [
    ('best-mattress-raynaud-phenomenon', 'best-mattress-myelomeningocele', 'Best Mattress for Raynaud\'s Phenomenon', '7 picks for cold-induced vasospasm sleep management &mdash; peripheral vasoconstriction prevention, triphasic color response timing, thermal retention surface design &amp; distinction from primary vs. secondary Raynaud\'s.'),
    ('best-mattress-hyperparathyroidism', 'best-mattress-raynaud-phenomenon', 'Best Mattress for Hyperparathyroidism', '7 picks for PTH excess &amp; hypercalcemia sleep disruption &mdash; demineralized bone pressure management, calcium-driven CNS fatigue, nocturia egress support &amp; distinction from hypoparathyroidism.'),
    ('best-mattress-cushing-syndrome', 'best-mattress-hyperparathyroidism', 'Best Mattress for Cushing\'s Syndrome', '7 picks for hypercortisolism sleep disruption &mdash; HPA axis nocturnal nadir abolition, central obesity pressure distribution, corticosteroid osteoporosis management &amp; distinction from Cushing\'s disease.'),
    ('best-mattress-temporal-arteritis', 'best-mattress-cushing-syndrome', 'Best Mattress for Temporal Arteritis (Giant Cell Arteritis)', '7 picks for GCA granulomatous vasculitis &mdash; scalp tenderness pressure management, 15-20 degree head elevation for venous pressure, corticosteroid osteoporosis precautions &amp; PMR overlap positioning.'),
    ('best-mattress-acromegaly', 'best-mattress-temporal-arteritis', 'Best Mattress for Acromegaly', '7 picks for IGF-1 excess &amp; GH arthropathy sleep &mdash; acral enlargement surface accommodation, sleep apnea soft tissue management, GH hyperhidrosis cooling &amp; distinction from gigantism.'),
    ('best-mattress-addisons-disease', 'best-mattress-acromegaly', 'Best Mattress for Addison\'s Disease', '7 picks for primary adrenal insufficiency &mdash; orthostatic hypotension rising mechanics, cortisol-deficiency fatigue support, temperature dysregulation management &amp; adrenal crisis morning risk reduction.'),
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
