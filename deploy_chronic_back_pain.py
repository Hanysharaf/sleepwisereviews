slug = "best-mattress-chronic-back-pain"

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

# 2. CATEGORIES in generate_posts_index.py
with open("generate_posts_index.py", "r", encoding="utf-8") as f:
    gen = f.read()

if slug not in gen:
    # Insert after best-mattress-back-pain in Health Conditions
    gen = gen.replace(
        "'best-mattress-back-pain'",
        "'best-mattress-back-pain', 'best-mattress-chronic-back-pain'"
    )
    with open("generate_posts_index.py", "w", encoding="utf-8") as f:
        f.write(gen)
    print("CATEGORIES updated")
else:
    print("CATEGORIES already has entry")

# 3. Homepage card
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

card_check = 'href="posts/best-mattress-chronic-back-pain.html"'
anchor = '<a class="article-card" href="posts/best-mattress-arthritis.html">'

card = (
    '        <div class="card-cat">\n'
    '          <span class="cat-badge">Health Conditions</span>\n'
    '          <h3><a href="posts/best-mattress-chronic-back-pain.html">Best Mattress for Chronic Back Pain</a></h3>\n'
    '          <p>Expert picks for long-term chronic back pain relief — zoned support, pressure distribution, and durability built for serious sufferers.</p>\n'
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
