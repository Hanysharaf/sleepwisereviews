slugs = [
    ('best-mattress-cluster-headaches', 'best-mattress-morton-neuroma', 'Best Mattress for Cluster Headaches', '7 picks for trigeminal autonomic cephalalgia sleep disruption &mdash; circadian rhythm entrainment, hypothalamic activation period management, verapamil positioning &amp; REM-phase cluster attack timing.'),
    ('best-mattress-post-mastectomy', 'best-mattress-cluster-headaches', 'Best Mattress for Post-Mastectomy Recovery', '7 picks for post-surgical breast recovery &mdash; implant &amp; tissue expander pressure avoidance, axillary dissection positioning, seroma prevention via lateral decubitus management &amp; chemotherapy fatigue support.'),
    ('best-mattress-post-concussion-syndrome', 'best-mattress-post-mastectomy', 'Best Mattress for Post-Concussion Syndrome', '7 picks for mTBI recovery sleep &mdash; vestibular hypersensitivity motion reduction, photophobia light interruption management, sleep architecture disruption &amp; cervicogenic headache concurrent positioning.'),
    ('best-mattress-hiatal-hernia', 'best-mattress-post-concussion-syndrome', 'Best Mattress for Hiatal Hernia', '7 picks for sliding &amp; paraesophageal hernia sleep &mdash; 30-45 degree head elevation for gastric reflux, left lateral decubitus preference, nocturnal regurgitation prevention &amp; GERD distinction.'),
    ('best-mattress-cauda-equina-syndrome', 'best-mattress-hiatal-hernia', 'Best Mattress for Cauda Equina Syndrome', '7 picks for cauda equina nerve root recovery &mdash; saddle anesthesia pressure avoidance, bladder &amp; bowel dysfunction nocturia egress support, neurogenic claudication positioning &amp; post-surgical spinal decompression care.'),
    ('best-mattress-myelomeningocele', 'best-mattress-cauda-equina-syndrome', 'Best Mattress for Myelomeningocele (Spina Bifida)', '7 picks for spina bifida myelomeningocele sleep &mdash; sac &amp; repair site pressure avoidance, hydrocephalus VP shunt positioning, latex allergy material requirements &amp; hip dislocation risk management.'),
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
