slugs = [
    ('best-mattress-systemic-sclerosis', 'best-mattress-amyloidosis', 'Best Mattress for Systemic Sclerosis (Scleroderma)', '7 picks for diffuse &amp; CREST scleroderma &mdash; skin fibrosis fragility cushioning, Raynaud\'s overlap thermal control, GERD esophageal dysmotility elevation, ILD orthopnea support &amp; joint contracture positioning.'),
    ('best-mattress-eosinophilic-esophagitis', 'best-mattress-systemic-sclerosis', 'Best Mattress for Eosinophilic Esophagitis', '7 picks for Th2 eosinophilic infiltration &mdash; food impaction risk head elevation, dysphagia positioning, PPI-responsive vs PPI-unresponsive management &amp; atopic march comorbidity surfaces.'),
    ('best-mattress-pulmonary-hypertension', 'best-mattress-eosinophilic-esophagitis', 'Best Mattress for Pulmonary Hypertension', '7 picks for WHO Group 1-5 PH &mdash; 30-45 degree orthopnea elevation, RV failure peripheral edema, OSA overlap 70-80% coverage, supplemental oxygen integration &amp; syncope prevention.'),
    ('best-mattress-graves-disease', 'best-mattress-pulmonary-hypertension', 'Best Mattress for Graves\' Disease', '7 picks for TRAb-driven hyperthyroidism &mdash; BMR-elevated heat intolerance cooling, palpitation motion isolation, ophthalmopathy proptosis elevation &amp; pretibial myxedema lower extremity comfort.'),
    ('best-mattress-myelofibrosis', 'best-mattress-graves-disease', 'Best Mattress for Myelofibrosis', '7 picks for JAK2/CALR/MPL myeloproliferative neoplasm &mdash; massive splenomegaly accommodation, cytokine-driven night sweats, marrow-fibrosis bone pain &amp; thrombocytopenia bruising protection.'),
    ('best-mattress-primary-aldosteronism', 'best-mattress-myelofibrosis', 'Best Mattress for Primary Aldosteronism (Conn\'s Syndrome)', '7 picks for aldosterone-driven resistant hypertension &mdash; non-dipping nocturnal BP management, hypokalemic muscle cramp relief, polyuria nocturia egress support &amp; MRA therapy comfort.'),
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
