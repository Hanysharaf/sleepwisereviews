slug = "best-mattress-petite-sleeper"

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

# 2. CATEGORIES — Life Stages
with open("generate_posts_index.py", "r", encoding="utf-8") as f:
    gen = f.read()

if slug not in gen:
    gen = gen.replace(
        "'best-mattress-college-students'",
        "'best-mattress-college-students', 'best-mattress-petite-sleeper'"
    )
    with open("generate_posts_index.py", "w", encoding="utf-8") as f:
        f.write(gen)
    print("CATEGORIES updated")
else:
    print("CATEGORIES already has entry")

# 3. Homepage card
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

card_check = 'href="posts/best-mattress-petite-sleeper.html"'
anchor = '<a class="article-card" href="posts/best-mattress-arthritis.html">'

card = (
    '        <div class="card-cat">\n'
    '          <span class="cat-badge">Life Stages</span>\n'
    '          <h3><a href="posts/best-mattress-petite-sleeper.html">Best Mattress for Petite Sleepers</a></h3>\n'
    '          <p>7 mattresses for lightweight frames under 130 lbs &mdash; the too-firm problem explained, ILD guide by weight and position, and the Purple Grid advantage at low body weights.</p>\n'
    '          <div class="card-meta"><span>7 picks</span><span>Life Stages</span></div>\n'
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
