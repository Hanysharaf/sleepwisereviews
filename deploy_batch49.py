slugs = [
    ('best-mattress-eczema', 'best-mattress-primary-aldosteronism', 'Best Mattress for Eczema', '7 picks for atopic dermatitis sleep &mdash; dust mite barrier covers, scratch-itch cycle thermal regulation, organic chemical-free flare-trigger avoidance &amp; breathable cotton/bamboo cover materials.'),
    ('best-mattress-vertigo', 'best-mattress-eczema', 'Best Mattress for Vertigo', '7 picks for vestibular dysfunction sleep &mdash; 30-degree head elevation to reduce BPPV crystal displacement, adjustable base Epley compatibility, slow-recovery foam &amp; safe-egress edge support.'),
    ('best-mattress-perimenopause', 'best-mattress-vertigo', 'Best Mattress for Perimenopause', '7 picks for ovarian decline sleep &mdash; active cooling for vasomotor hot flashes, progesterone-loss sleep onset support, anxiety/insomnia management &amp; emerging joint pain pressure relief.'),
    ('best-mattress-menieres-disease', 'best-mattress-perimenopause', 'Best Mattress for Meniere\'s Disease', '7 picks for endolymphatic hydrops &mdash; 30-45 degree head elevation for pressure reduction, motion isolation to prevent attack triggers, tinnitus noise isolation &amp; fall-prevention edge support.'),
    ('best-mattress-hidradenitis-suppurativa', 'best-mattress-menieres-disease', 'Best Mattress for Hidradenitis Suppurativa', '7 picks for follicular occlusion disease &mdash; apocrine-area pressure relief (axilla/groin/buttocks), breathable friction-reducing cooling, antimicrobial covers for Staph colonization &amp; tunnel/sinus tract comfort.'),
    ('best-mattress-rosacea', 'best-mattress-hidradenitis-suppurativa', 'Best Mattress for Rosacea', '7 picks for vasomotor flushing skin disease &mdash; cool surfaces to prevent flush triggers, hypoallergenic materials, ocular rosacea head elevation, demodex consideration &amp; fragrance-free cover requirements.'),
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
