"""Generate posts/best-travel-pillow.html"""
import os

BASE = os.path.dirname(__file__)
OUT = os.path.join(BASE, 'posts', 'best-travel-pillow.html')

TITLE = "Best Travel Pillows 2026: Top 7 for Flights, Road Trips & Long Hauls"
SLUG = "best-travel-pillow"
DESC = "Neck pain on flights starts with the wrong pillow. We compared 7 travel pillows — memory foam, inflatable, and hybrid — for neck support, packability, and comfort on red-eyes and long road trips."
TAG = "sleepwiserevi-20"

PRODUCTS = [
    {
        "name": "Cabeau Evolution Classic",
        "tag": "Cabeau",
        "badge": "Best Overall",
        "price": "~$40",
        "key": "Memory foam, flat-back design, adjustable tether, machine-washable cover",
        "pros": "Flat back presses against headrest so head doesn't fall forward; raised side panels support chin; machine-washable velour cover",
        "cons": "Doesn't compress as small as inflatables; slightly pricey for foam",
        "link": f"https://www.amazon.com/s?k=cabeau+evolution+classic+travel+pillow&tag={TAG}",
        "schema_name": "Cabeau Evolution Classic Memory Foam Travel Pillow",
    },
    {
        "name": "Trtl Pillow Plus",
        "tag": "Trtl",
        "badge": "Best Compact",
        "price": "~$60",
        "key": "Hidden ribbed support spine, fleece outer, folds flat to 4.5 inches",
        "pros": "Wraps like a scarf — packs flat and tiny; internal spine holds neck in upright position; great for window-seat sleepers",
        "cons": "Side support only — not suited for center or aisle seats without headrest; expensive",
        "link": f"https://www.amazon.com/s?k=trtl+pillow+plus+travel+neck+support&tag={TAG}",
        "schema_name": "Trtl Pillow Plus Neck Support Travel Pillow",
    },
    {
        "name": "BCOZZY Chin Supporting Travel Pillow",
        "tag": "BCOZZY",
        "badge": "Best for Chin Support",
        "price": "~$35",
        "key": "Overlapping front panels support chin, memory foam fill, adjustable overlap",
        "pros": "Overlapping arms prevent head from dropping chin-to-chest; works in upright seats with no headrest; soft and washable",
        "cons": "Bulkier than standard U-pillows; takes more bag space",
        "link": f"https://www.amazon.com/s?k=bcozzy+chin+supporting+travel+pillow&tag={TAG}",
        "schema_name": "BCOZZY Chin Supporting Memory Foam Travel Pillow",
    },
    {
        "name": "Dot&Dot Inflatable Travel Pillow",
        "tag": "Dot&Dot",
        "badge": "Best Inflatable",
        "price": "~$20",
        "key": "Inflatable ergonomic U-shape, adjustable firmness, packs to fist size",
        "pros": "Packs to 4x3 inches; adjustable firmness by inflation level; machine-washable cover; affordable",
        "cons": "Not as comfortable as foam; requires inflation — less convenient mid-flight",
        "link": f"https://www.amazon.com/s?k=dot+and+dot+inflatable+travel+pillow&tag={TAG}",
        "schema_name": "Dot&Dot Inflatable Ergonomic Travel Pillow",
    },
    {
        "name": "Cabeau Evolution S3",
        "tag": "Cabeau S3",
        "badge": "Best Memory Foam Compact",
        "price": "~$50",
        "key": "Memory foam, compresses to half size in included bag, airline seat strap",
        "pros": "Compresses into carry bag smaller than most foam pillows; seat strap attaches to headrest to hold in position; washable cover",
        "cons": "Compression takes effort; pricier than standard foam options",
        "link": f"https://www.amazon.com/s?k=cabeau+evolution+s3+travel+pillow&tag={TAG}",
        "schema_name": "Cabeau Evolution S3 Compressible Memory Foam Travel Pillow",
    },
    {
        "name": "MLVOC Travel Pillow",
        "tag": "MLVOC",
        "badge": "Best Budget",
        "price": "~$15",
        "key": "Memory foam U-shape, ergonomic contour, adjustable snap closure, washable cover",
        "pros": "Strong value for price; decent neck support; snap closure adjusts tightness; comes with eye mask and earplugs",
        "cons": "Foam density lower than premium picks; won't last as many trips",
        "link": f"https://www.amazon.com/s?k=mlvoc+travel+pillow+memory+foam&tag={TAG}",
        "schema_name": "MLVOC Memory Foam U-Shape Travel Pillow",
    },
    {
        "name": "Ostrich Pillow Light",
        "tag": "Ostrich Pillow",
        "badge": "Best for Upright Deep Sleep",
        "price": "~$55",
        "key": "360-degree wrap design, machine washable, works as nap mask + neck support",
        "pros": "Wraps entire neck and face to block light and support head in any direction; good for long overnight flights",
        "cons": "Gets hot; looks unusual; not for those bothered by full coverage around the face",
        "link": f"https://www.amazon.com/s?k=ostrich+pillow+light+travel&tag={TAG}",
        "schema_name": "Ostrich Pillow Light Wrap-Around Travel Pillow",
    },
]

SCHEMA_ITEMS = "\n".join([
    f'''    {{
      "@type": "ListItem",
      "position": {i+1},
      "name": "{p['schema_name']}",
      "url": "https://sleepwisereviews.com/posts/{SLUG}.html"
    }}{"," if i < len(PRODUCTS)-1 else ""}''' for i, p in enumerate(PRODUCTS)
])

FAQ_DATA = [
    ("What type of travel pillow is best for long flights?", "Memory foam U-pillows with a flat back (like the Cabeau Evolution) perform best on long flights because they prevent the head-bob forward that wakes you up. Inflatables are better for carry-on space but sacrifice comfort. For overnight transcontinental flights, memory foam is worth the extra bulk."),
    ("Why does my head fall forward with a standard travel pillow?", "Traditional U-pillows only support the sides of the neck. When you fall deeply asleep, your neck muscles relax and your head drops chin-to-chest through the open front. Pillows with overlapping front panels (BCOZZY) or a rigid spine (Trtl) solve this by blocking forward movement."),
    ("How do I keep my travel pillow from sliding off?", "Look for pillows with a tether clip or headrest strap that connects to the airline seat. The Cabeau Evolution Classic has an adjustable cord that clips to hold your head gently against the pillow. Without a strap, the pillow can shift when you nod off."),
    ("Are inflatable travel pillows worth it?", "Only if packing space is the primary constraint. Inflatables pack to fist size but offer significantly less comfort than foam. Good for short hops; for 8+ hour flights, the comfort difference becomes noticeable by hour 4."),
    ("What is the best travel pillow for neck pain?", "For existing neck pain, the Cabeau Evolution Classic or ComfiLife-style flat-back designs are best because they maintain the cervical curve in a neutral position. Avoid pillows that push your chin down or force the head to one side for extended periods."),
]

FAQ_SCHEMA = "\n".join([
    f'''    {{
      "@type": "Question",
      "name": "{q}",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "{a}"
      }}
    }}{"," if i < len(FAQ_DATA)-1 else ""}''' for i, (q, a) in enumerate(FAQ_DATA)
])

def card(p, idx):
    badge_html = f'<span class="badge">{p["badge"]}</span>' if p.get("badge") else ""
    return f'''
    <div class="product-card" id="product-{idx+1}">
      <div class="product-header">
        <div>
          <h2 class="product-name">{idx+1}. {p["name"]} {badge_html}</h2>
          <div class="product-meta"><strong>Price:</strong> {p["price"]} &nbsp;|&nbsp; <strong>Key Features:</strong> {p["key"]}</div>
        </div>
      </div>
      <div class="pros-cons">
        <div class="pros"><strong>Pros</strong><p>{p["pros"]}</p></div>
        <div class="cons"><strong>Cons</strong><p>{p["cons"]}</p></div>
      </div>
      <a class="buy-btn" href="{p["link"]}" target="_blank" rel="nofollow noopener noreferrer">Check Price on Amazon</a>
    </div>'''

CARDS_HTML = "\n".join(card(p, i) for i, p in enumerate(PRODUCTS))

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{TITLE} | SleepWise Reviews</title>
  <meta name="description" content="{DESC}">
  <link rel="canonical" href="https://sleepwisereviews.com/posts/{SLUG}.html">

  <!-- Open Graph -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="{TITLE}">
  <meta property="og:description" content="{DESC}">
  <meta property="og:url" content="https://sleepwisereviews.com/posts/{SLUG}.html">
  <meta property="og:site_name" content="SleepWise Reviews">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{TITLE}">
  <meta name="twitter:description" content="{DESC}">

  <!-- JSON-LD Schemas -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "ItemList",
    "name": "{TITLE}",
    "description": "{DESC}",
    "numberOfItems": {len(PRODUCTS)},
    "itemListElement": [
{SCHEMA_ITEMS}
    ]
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
{FAQ_SCHEMA}
    ]
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://sleepwisereviews.com/"}},
      {{"@type": "ListItem", "position": 2, "name": "Sleep Products", "item": "https://sleepwisereviews.com/posts/index.html"}},
      {{"@type": "ListItem", "position": 3, "name": "{TITLE}", "item": "https://sleepwisereviews.com/posts/{SLUG}.html"}}
    ]
  }}
  </script>

  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#1a1a2e;background:#f8f9fa;line-height:1.7}}
    header{{background:linear-gradient(135deg,#1a1a2e,#16213e);color:#fff;padding:20px 0;text-align:center}}
    header a{{color:#e94560;text-decoration:none;font-weight:700;font-size:1.4rem}}
    nav{{background:#16213e;padding:10px 0;text-align:center}}
    nav a{{color:#aaa;text-decoration:none;margin:0 12px;font-size:.9rem}}
    nav a:hover{{color:#e94560}}
    .container{{max-width:860px;margin:0 auto;padding:0 20px}}
    h1{{font-size:2rem;color:#1a1a2e;margin:30px 0 15px;line-height:1.3}}
    .intro{{font-size:1.05rem;color:#444;margin-bottom:30px;padding:20px;background:#fff;border-radius:10px;border-left:4px solid #e94560}}
    .product-card{{background:#fff;border-radius:12px;padding:24px;margin-bottom:24px;box-shadow:0 2px 8px rgba(0,0,0,.08);border-top:4px solid #e94560}}
    .product-name{{font-size:1.3rem;color:#1a1a2e;margin-bottom:8px}}
    .badge{{background:#e94560;color:#fff;font-size:.7rem;padding:3px 8px;border-radius:20px;margin-left:8px;vertical-align:middle;font-weight:600;text-transform:uppercase}}
    .product-meta{{font-size:.9rem;color:#666;margin-bottom:14px}}
    .pros-cons{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:16px}}
    .pros,.cons{{padding:12px;border-radius:8px;font-size:.9rem}}
    .pros{{background:#f0fdf4;border-left:3px solid #22c55e}}
    .cons{{background:#fff7ed;border-left:3px solid #f97316}}
    .pros strong,.cons strong{{display:block;margin-bottom:4px}}
    .buy-btn{{display:inline-block;background:#e94560;color:#fff;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:600;font-size:.95rem}}
    .buy-btn:hover{{background:#c73652}}
    .info-box{{background:#eef4ff;border:1px solid #6ea8fe;border-radius:10px;padding:18px 22px;margin:28px 0}}
    .info-box h3{{color:#1a3a6e;margin-bottom:10px}}
    .info-box p,.info-box li{{font-size:.95rem;color:#333}}
    table{{width:100%;border-collapse:collapse;margin:24px 0;font-size:.92rem}}
    th{{background:#1a1a2e;color:#fff;padding:10px 12px;text-align:left}}
    td{{padding:9px 12px;border-bottom:1px solid #e5e5e5}}
    tr:nth-child(even) td{{background:#f9f9f9}}
    .faq-section{{margin:40px 0}}
    .faq-section h2{{font-size:1.5rem;margin-bottom:20px;color:#1a1a2e}}
    details{{background:#fff;border-radius:8px;margin-bottom:10px;box-shadow:0 1px 4px rgba(0,0,0,.07)}}
    summary{{padding:14px 18px;cursor:pointer;font-weight:600;color:#1a1a2e;list-style:none;font-size:.98rem}}
    summary::-webkit-details-marker{{display:none}}
    details[open] summary{{color:#e94560}}
    .faq-answer{{padding:0 18px 14px;color:#444;font-size:.95rem;line-height:1.7}}
    .related-box{{background:#fff;border-radius:10px;padding:20px 24px;margin:32px 0;box-shadow:0 1px 6px rgba(0,0,0,.07)}}
    .related-box h3{{font-size:1rem;color:#1a1a2e;margin-bottom:12px}}
    .related-box ul{{list-style:none;display:flex;flex-wrap:wrap;gap:8px}}
    .related-box ul li a{{background:#f0f4ff;color:#1a1a2e;padding:6px 14px;border-radius:20px;text-decoration:none;font-size:.88rem;border:1px solid #dde4ff}}
    .related-box ul li a:hover{{background:#e94560;color:#fff;border-color:#e94560}}
    footer{{background:#1a1a2e;color:#aaa;text-align:center;padding:30px 20px;margin-top:50px;font-size:.85rem}}
    footer a{{color:#e94560;text-decoration:none}}
    @media(max-width:600px){{.pros-cons{{grid-template-columns:1fr}}h1{{font-size:1.5rem}}}}
  </style>
</head>
<body>

<header>
  <div class="container">
    <a href="../index.html">SleepWise Reviews</a>
    <p style="margin-top:6px;font-size:.9rem;color:#ccc">Evidence-based sleep product reviews</p>
  </div>
</header>
<nav>
  <div class="container">
    <a href="../index.html">Home</a>
    <a href="index.html">All Guides</a>
    <a href="sleep-travel-tips.html">Travel Sleep Tips</a>
    <a href="best-sleep-masks.html">Sleep Masks</a>
    <a href="best-earplugs-sleeping.html">Earplugs</a>
  </div>
</nav>

<div class="container">
  <article>
    <h1>{TITLE}</h1>

    <div class="intro">
      <strong>The head-bob problem:</strong> Standard U-pillows support the sides of your neck but leave the front open. When you finally drift off at 30,000 feet, your chin drops to your chest and jolts you awake. The best travel pillows solve this with chin support, flat backs, or rigid spines — so your head stays put through turbulence and layovers.
    </div>

    <div class="info-box">
      <h3>Travel Pillow Buying Checklist</h3>
      <ul style="margin-left:16px;margin-top:6px">
        <li><strong>Support type:</strong> Flat-back for no head-bob; chin panel for forward head prevention; wrap for full support</li>
        <li><strong>Pack size:</strong> Foam = bulkier; inflatable = fist-size; hybrid compressibles balance both</li>
        <li><strong>Seat type:</strong> Window seat benefits most from pillows; aisle seats need center support</li>
        <li><strong>Washability:</strong> Look for removable, machine-washable covers — travel pillows get grimy fast</li>
        <li><strong>Attachment:</strong> Headrest strap or snap closure keeps the pillow from sliding mid-flight</li>
      </ul>
    </div>

    <h2 style="font-size:1.4rem;margin:28px 0 14px">Top 7 Travel Pillows — Compared</h2>

{CARDS_HTML}

    <h2 style="font-size:1.4rem;margin:32px 0 16px">Travel Pillow Comparison Table</h2>
    <table>
      <thead>
        <tr>
          <th>Pillow</th>
          <th>Type</th>
          <th>Pack Size</th>
          <th>Chin Support</th>
          <th>Price</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>Cabeau Evolution Classic</td><td>Memory foam</td><td>Medium</td><td>Raised panels</td><td>~$40</td></tr>
        <tr><td>Trtl Pillow Plus</td><td>Fleece + spine</td><td>Flat/small</td><td>One-side only</td><td>~$60</td></tr>
        <tr><td>BCOZZY</td><td>Memory foam</td><td>Medium</td><td>Overlap panels</td><td>~$35</td></tr>
        <tr><td>Dot&amp;Dot Inflatable</td><td>Inflatable</td><td>Fist-size</td><td>Moderate</td><td>~$20</td></tr>
        <tr><td>Cabeau Evolution S3</td><td>Memory foam</td><td>Compressible</td><td>Raised panels</td><td>~$50</td></tr>
        <tr><td>MLVOC</td><td>Memory foam</td><td>Medium</td><td>Standard U</td><td>~$15</td></tr>
        <tr><td>Ostrich Pillow Light</td><td>Wrap-around</td><td>Medium</td><td>360 degree</td><td>~$55</td></tr>
      </tbody>
    </table>

    <div class="info-box" style="background:#f0fdf4;border-color:#22c55e">
      <h3>Flight Sleep Protocol — Beyond the Pillow</h3>
      <p>A good travel pillow is one piece of the puzzle. For red-eyes and long-hauls: set your watch to destination time before boarding, avoid alcohol (disrupts REM despite feeling sedating), take a low-dose melatonin (0.5mg) 30 minutes before your target sleep time in the destination zone, and use a sleep mask + earplugs to block cabin light and engine noise. The pillow keeps your neck comfortable; everything else sets the sleep conditions.</p>
    </div>

    <div class="faq-section">
      <h2>Frequently Asked Questions</h2>
      {"".join(f"""<details><summary>{q}</summary><div class="faq-answer">{a}</div></details>""" for q, a in FAQ_DATA)}
    </div>

    <div class="related-box">
      <h3>Related Guides</h3>
      <ul>
        <li><a href="sleep-travel-tips.html">Sleep Travel Tips</a></li>
        <li><a href="jet-lag-guide.html">Jet Lag Recovery Guide</a></li>
        <li><a href="best-sleep-masks.html">Best Sleep Masks</a></li>
        <li><a href="best-earplugs-sleeping.html">Best Earplugs for Sleeping</a></li>
        <li><a href="best-melatonin-supplements.html">Best Melatonin Supplements</a></li>
        <li><a href="sleep-business-travel.html">Sleep on Business Travel</a></li>
      </ul>
    </div>

  </article>
</div>

<footer>
  <div class="container">
    <p>SleepWise Reviews &copy; 2026 &mdash; <a href="../about.html">About</a> | <a href="../privacy.html">Privacy</a> | <a href="../affiliate-disclosure.html">Affiliate Disclosure</a></p>
    <p style="margin-top:8px">As an Amazon Associate we earn from qualifying purchases.</p>
  </div>
</footer>

</body>
</html>'''

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Written: {OUT}")
