slug = "best-mattress-rheumatoid-arthritis"

# 1. Sitemap
with open("sitemap.xml", "r", encoding="utf-8") as f:
    sitemap = f.read()

entry_check = "posts/" + slug + ".html"
if entry_check not in sitemap:
    entry = (
        "  <url>\n"
        "    <loc>https://sleepwisereviews.com/posts/" + slug + ".html</loc>\n"
        "    <lastmod>2026-05-25</lastmod>\n"
        "    <changefreq>monthly</changefreq>\n"
        "    <priority>0.7</priority>\n"
        "  </url>\n"
        "</urlset>"
    )
    sitemap = sitemap.replace("</urlset>", entry)
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap)
    print("Sitemap updated")
else:
    print("Sitemap already has entry")

count = sitemap.count("<loc>")
print(f"Sitemap now has {count} URLs")

# 2. CATEGORIES -- Health Conditions (after best-mattress-ehlers-danlos)
with open("generate_posts_index.py", "r", encoding="utf-8") as f:
    gen = f.read()

if slug not in gen:
    gen = gen.replace(
        "'best-mattress-ehlers-danlos'",
        "'best-mattress-ehlers-danlos', 'best-mattress-rheumatoid-arthritis'"
    )
    with open("generate_posts_index.py", "w", encoding="utf-8") as f:
        f.write(gen)
    print("CATEGORIES updated")
else:
    print("CATEGORIES already has entry")

# 3. Homepage card
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

card_check = 'href="posts/best-mattress-rheumatoid-arthritis.html"'
anchor = '<a class="article-card" href="posts/best-mattress-arthritis.html">'

card = (
    '        <div class="card-cat">\n'
    '          <span class="cat-badge" style="background:#dc2626">Health Conditions</span>\n'
    '          <h3><a href="posts/best-mattress-rheumatoid-arthritis.html">Best Mattress for Rheumatoid Arthritis</a></h3>\n'
    '          <p>7 picks for RA flares, morning stiffness &amp; systemic inflammation &mdash; pressure relief for multi-joint involvement, cooling for nocturnal fever, edge support for fatigue.</p>\n'
    '          <div class="card-meta"><span>7 picks</span><span>Health Conditions</span></div>\n'
    '        </div>\n'
    '        '
)

if card_check not in html:
    html = html.replace(anchor, card + anchor)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Homepage card inserted")
else:
    print("Homepage card already present")
