slug = "best-mattress-athlete"

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

# 2. CATEGORIES -- Performance (after best-mattress-hot-sleepers as nearest equivalent)
with open("generate_posts_index.py", "r", encoding="utf-8") as f:
    gen = f.read()

# Add to a Performance category or reuse existing Lifestyle/General
# Check what categories exist and find a good anchor
if slug not in gen:
    # Add after best-mattress-couples as part of general lifestyle picks
    gen = gen.replace(
        "'best-mattress-couples'",
        "'best-mattress-couples', 'best-mattress-athlete'"
    )
    with open("generate_posts_index.py", "w", encoding="utf-8") as f:
        f.write(gen)
    print("CATEGORIES updated")
else:
    print("CATEGORIES already has entry")

# 3. Homepage card
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

card_check = 'href="posts/best-mattress-athlete.html"'
anchor = '<a class="article-card" href="posts/best-mattress-arthritis.html">'

card = (
    '        <div class="card-cat">\n'
    '          <span class="cat-badge" style="background:#0e7490">Performance</span>\n'
    '          <h3><a href="posts/best-mattress-athlete.html">Best Mattress for Athletes</a></h3>\n'
    '          <p>7 picks for sports recovery &mdash; DOMS pressure relief, cooling for high-BMR bodies, growth hormone deep sleep, sport-by-sport firmness guide, Stanford performance data.</p>\n'
    '          <div class="card-meta"><span>7 picks</span><span>Performance</span></div>\n'
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
