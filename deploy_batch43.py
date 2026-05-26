slugs = [
    ('best-mattress-bursitis', 'best-mattress-psoriasis', 'Best Mattress for Bursitis', '7 picks for hip, shoulder &amp; knee bursitis &mdash; intrabursal pressure reduction, trochanteric bursitis side-sleeping, subacromial compression avoidance &amp; zoned pressure relief at bursa-prone sites.'),
    ('best-mattress-complex-regional-pain-syndrome', 'best-mattress-bursitis', 'Best Mattress for Complex Regional Pain Syndrome (CRPS)', '7 picks for CRPS Type I &amp; II &mdash; allodynia surface management, Koebner-equivalent pressure avoidance, vasomotor dysregulation cooling &amp; limb elevation for edema control.'),
    ('best-mattress-interstitial-cystitis', 'best-mattress-complex-regional-pain-syndrome', 'Best Mattress for Interstitial Cystitis', '7 picks for IC &amp; painful bladder syndrome &mdash; pelvic floor pressure neutralization, nocturia egress support, sacral cushioning &amp; neutral pelvic alignment for urothelial pain management.'),
    ('best-mattress-polymyalgia-rheumatica', 'best-mattress-interstitial-cystitis', 'Best Mattress for Polymyalgia Rheumatica', '7 picks for PMR bilateral shoulder &amp; hip girdle pain &mdash; IL-6 morning stiffness reduction, corticosteroid osteoporosis precautions, easy transfer edge support &amp; responsive repositioning surfaces.'),
    ('best-mattress-thoracic-outlet-syndrome', 'best-mattress-polymyalgia-rheumatica', 'Best Mattress for Thoracic Outlet Syndrome', '7 picks for neurogenic &amp; vascular TOS &mdash; costoclavicular space management, overhead arm position prevention, scalene tension reduction via cervical alignment &amp; shoulder sinkage calibration.'),
    ('best-mattress-costochondritis', 'best-mattress-thoracic-outlet-syndrome', 'Best Mattress for Costochondritis', '7 picks for costal cartilage inflammation &mdash; thoracic pressure distribution, Tietze syndrome distinction, sternal contact area management &amp; breathing mechanics during back &amp; side sleeping.'),
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
