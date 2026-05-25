"""Generate posts/best-mattress-firm-vs-medium.html"""
import os, json

slug = "best-mattress-firm-vs-medium"
title = "Firm vs Medium Mattress: Which Is Right for You? (2026 Guide)"
description = "The complete guide to choosing between firm and medium firmness mattresses. Covers sleep position, body weight, back pain, couples, and our top picks in each firmness level."
date = "2026-05-25"
affiliate_tag = "sleepwiserevi-20"

products = [
    {
        "rank": 1,
        "name": "Saatva Classic (Firm or Medium Firm)",
        "badge": "Best Premium Firm",
        "price": "$1,299–$2,599",
        "key_spec": "Dual innerspring, lumbar zone support, choose Firm or Luxury Firm",
        "pros": ["Available in 3 firmness levels: Plush Soft, Luxury Firm, Firm", "Lumbar enhancement zone for back pain", "Euro pillow top on Luxury Firm feels firm-but-cushioned", "White glove delivery included", "365-night trial, lifetime warranty"],
        "cons": ["Premium price — one of the most expensive options", "Innerspring feel — not for memory foam lovers", "Heavy — difficult to move without help"],
        "why": "The Saatva Luxury Firm (6/10 scale) hits the sweet spot that most people searching 'firm vs medium' actually need: supportive enough for back and stomach sleepers, with enough surface cushion to prevent pressure points. Available in both Firm (8/10) and Luxury Firm — you choose at purchase.",
        "search": "Saatva+Classic+Firm+Mattress"
    },
    {
        "rank": 2,
        "name": "WinkBeds WinkBed Plus (Firm)",
        "badge": "Best Firm for Heavy Sleepers",
        "price": "$1,299–$2,299",
        "key_spec": "Designed for 250lb+ sleepers, firmer support, Euro pillow top",
        "pros": ["Specifically engineered for heavier body types", "Prevents the sinking that makes standard mattresses feel soft", "European pillow top adds comfort without sacrificing support", "Lifetime warranty, 120-night trial", "Reinforced edge support"],
        "cons": ["Very firm — may feel hard for lighter sleepers", "Expensive", "Heavy to move"],
        "why": "Standard mattresses rated 'firm' often feel medium to heavier sleepers because body weight compresses the materials more. WinkBed Plus is calibrated for the physics of heavier bodies — it feels genuinely firm at 250lb+ where other mattresses would feel medium-soft.",
        "search": "WinkBeds+Plus+Firm+Mattress+Heavy+Sleepers"
    },
    {
        "rank": 3,
        "name": "DreamCloud Premier (Medium Firm)",
        "badge": "Best Value Medium Firm",
        "price": "$799–$1,599",
        "key_spec": "Hybrid, medium firm (6.5/10), cashmere blend cover, 365-night trial",
        "pros": ["365-night trial — longest in the industry", "Lifetime warranty", "Cashmere blend cover with premium feel", "Hybrid coil + foam construction", "Good motion isolation for couples"],
        "cons": ["Heavier construction — difficult to move", "Edge support average vs competitors", "Not ideal for strict stomach sleepers"],
        "why": "Medium firm is the most popular firmness for a reason: it accommodates the widest range of sleepers. DreamCloud Premier's 365-night trial removes all purchase risk — if medium firm doesn't work, you return it. At this price with a lifetime warranty, it's the best value in this category.",
        "search": "DreamCloud+Premier+Medium+Firm+Mattress"
    },
    {
        "rank": 4,
        "name": "Nectar Premier Copper (Medium Firm)",
        "badge": "Best Cooling Medium Firm",
        "price": "$799–$1,499",
        "key_spec": "Copper-infused memory foam, medium firm, 365-night trial, lifetime warranty",
        "pros": ["Copper infusion draws heat away from body", "Medium firm memory foam suits side and back sleepers", "365-night trial, lifetime warranty", "Strong motion isolation", "Good pressure point relief"],
        "cons": ["Memory foam — slower response than hybrid", "Copper cooling is partially marketing vs physics", "Off-gassing possible on delivery"],
        "why": "For side and combo sleepers who want medium firm with memory foam contouring, the Nectar Premier Copper delivers at a competitive price. The copper infusion genuinely helps conductivity — useful for hot sleepers who want medium firm foam.",
        "search": "Nectar+Premier+Copper+Medium+Firm+Mattress"
    },
    {
        "rank": 5,
        "name": "Plank Firm Mattress by Brooklyn Bedding",
        "badge": "Firmest Available",
        "price": "$599–$1,299",
        "key_spec": "Dual-sided: Firm one side, Ultra Firm other side, 120-night trial",
        "pros": ["Dual-sided: flip for Firm vs Ultra-Firm feel", "Best truly firm option for stomach sleepers and firm preference sleepers", "Competitive price for the firmness level", "Good edge support", "Flipping extends mattress life"],
        "cons": ["No pillow top — harder feel throughout", "May be too firm for most back sleepers", "Not suitable for side sleepers"],
        "why": "When someone truly needs a firm mattress — stomach sleepers, very heavy sleepers, or those advised by a physical therapist to sleep on a hard surface — the Plank delivers what others advertise but don't achieve. Flippable design gives you Firm or Ultra-Firm.",
        "search": "Plank+Firm+Mattress+Brooklyn+Bedding"
    },
    {
        "rank": 6,
        "name": "Leesa Sapira Hybrid (Medium)",
        "badge": "Best True Medium",
        "price": "$999–$1,899",
        "key_spec": "Hybrid, true 5/10 medium, 100-night trial, foam + coil construction",
        "pros": ["True medium (5/10) — not medium-firm branded as medium", "Good for combo sleepers who switch positions", "Hybrid construction: bounce + contouring", "Comfortable for most body types under 250lb", "B Corp certified company"],
        "cons": ["100-night trial is shorter than competitors", "Not ideal for heavier sleepers over 250lb", "Less motion isolation than foam-only options"],
        "why": "Many mattresses labeled 'medium' are actually 6-7/10 firmness — medium firm. Leesa's Sapira Hybrid is a genuine 5/10 medium, making it the right choice for combo sleepers and those who found medium-firm mattresses too stiff.",
        "search": "Leesa+Sapira+Hybrid+Medium+Mattress"
    },
    {
        "rank": 7,
        "name": "Awara Natural Hybrid (Medium Firm)",
        "badge": "Best Organic Medium Firm",
        "price": "$999–$1,899",
        "key_spec": "GOLS organic latex, GOTS organic cotton, medium firm, lifetime warranty",
        "pros": ["GOLS + GOTS certified organic materials", "Natural latex: responsive, durable, cooling", "Lifetime warranty", "365-night trial", "No synthetic foam off-gassing"],
        "cons": ["Natural latex smell initially (normal, dissipates)", "Heavy — latex is denser than foam", "Premium price for organic certification"],
        "why": "For buyers who want medium firm without synthetic materials — organic cotton, GOLS-certified latex, no chemical flame retardants — Awara delivers without compromise. Latex medium firm is more responsive than memory foam medium firm, which some sleepers strongly prefer.",
        "search": "Awara+Natural+Hybrid+Organic+Mattress"
    }
]

faqs = [
    {
        "q": "Is firm or medium firmness better for back pain?",
        "a": "Research favors medium firm for most back pain sufferers. A landmark 2003 RCT (Kovacs et al.) found medium-firm mattresses reduced back pain significantly more than firm mattresses in chronic low back pain patients. The exception: stomach sleepers with back pain, who need firmer support to prevent lumbar hyperextension. Your sleep position, not your back pain severity, should drive the firmness choice."
    },
    {
        "q": "What firmness should side sleepers choose?",
        "a": "Side sleepers should choose medium to medium-soft (4-6/10 firmness). Side sleeping creates significant pressure at the shoulder and hip — a firm mattress causes painful pressure points that restrict blood flow and cause sleep disruption. The mattress needs to allow the shoulder to sink 2-3 inches while maintaining spinal alignment at the hip. Firm mattresses fail this test for most side sleepers."
    },
    {
        "q": "What firmness should stomach sleepers choose?",
        "a": "Stomach sleepers need firm to extra-firm (7-9/10). This is the most important firmness rule: stomach sleeping on a soft or medium mattress causes extreme lumbar hyperextension because the hips sink lower than the torso. This position compresses lumbar discs and is a leading cause of lower back pain. A firm mattress keeps the spine in a neutral position. Stomach sleepers should also use a very thin pillow or no pillow."
    },
    {
        "q": "How does body weight affect mattress firmness?",
        "a": "Heavier sleepers compress mattress materials more deeply, making any given mattress feel softer. A 150lb person on a 'medium firm' mattress experiences medium firm. A 250lb person on the same mattress may experience it as medium soft. This is why dedicated mattresses for heavier sleepers (like WinkBed Plus) are engineered with stronger coil support and higher-density foams. Rule: if you're over 230lb, size up one firmness level from your theoretical preference."
    },
    {
        "q": "Can couples with different firmness preferences share a mattress?",
        "a": "Several solutions exist: (1) Medium firm is statistically the best compromise for couples with different preferences; (2) Split firmness kings let each side choose independently; (3) Adjustable air mattresses (Sleep Number) let each partner set their own firmness; (4) A quality mattress topper can soften one side. Medium firm is the best starting point — easier to soften with a topper than to firm up."
    }
]

schema = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "Article",
            "headline": title,
            "description": description,
            "datePublished": date,
            "dateModified": date,
            "author": {"@type": "Organization", "name": "SleepWise Reviews"},
            "publisher": {"@type": "Organization", "name": "SleepWise Reviews", "url": "https://sleepwisereviews.com/"},
            "mainEntityOfPage": f"https://sleepwisereviews.com/posts/{slug}.html"
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://sleepwisereviews.com/"},
                {"@type": "ListItem", "position": 2, "name": "All Guides", "item": "https://sleepwisereviews.com/posts/"},
                {"@type": "ListItem", "position": 3, "name": title, "item": f"https://sleepwisereviews.com/posts/{slug}.html"}
            ]
        },
        {
            "@type": "ItemList",
            "name": title,
            "numberOfItems": len(products),
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": p["rank"],
                    "name": p["name"],
                    "url": f"https://www.amazon.com/s?k={p['search']}&tag={affiliate_tag}"
                } for p in products
            ]
        },
        {
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
                for f in faqs
            ]
        }
    ]
}

def product_card(p):
    pros = ''.join(f'<li>{x}</li>' for x in p['pros'])
    cons = ''.join(f'<li>{x}</li>' for x in p['cons'])
    url = f"https://www.amazon.com/s?k={p['search']}&tag={affiliate_tag}"
    return f'''
  <article class="product-card" id="pick-{p['rank']}">
    <div class="product-header">
      <div class="rank-badge">#{p['rank']}</div>
      <div class="product-title-block">
        <span class="best-badge">{p['badge']}</span>
        <h2 class="product-name">{p['name']}</h2>
        <div class="spec-chips">
          <span class="chip price-chip">{p['price']}</span>
          <span class="chip">{p['key_spec']}</span>
        </div>
      </div>
    </div>
    <div class="why-box"><strong>Why we picked it:</strong> {p['why']}</div>
    <div class="pros-cons-grid">
      <div class="pros-col"><h4>Pros</h4><ul>{pros}</ul></div>
      <div class="cons-col"><h4>Cons</h4><ul>{cons}</ul></div>
    </div>
    <a class="buy-btn" href="{url}" rel="nofollow noopener noreferrer" target="_blank">Check Price on Amazon &rarr;</a>
  </article>'''

def faq_block(faqs):
    items = ''.join(f'''
    <div class="faq-item">
      <h3 class="faq-q">{f['q']}</h3>
      <p class="faq-a">{f['a']}</p>
    </div>''' for f in faqs)
    return f'<section class="faq-section"><h2>Frequently Asked Questions</h2>{items}</section>'

cards_html = ''.join(product_card(p) for p in products)
faq_html = faq_block(faqs)
schema_block = '<script type="application/ld+json">\n' + json.dumps(schema, indent=2) + '\n</script>'
toc_items = ''.join(f'<li><a href="#pick-{p["rank"]}">{p["name"]}</a> <span class="toc-badge">{p["badge"]}</span></li>' for p in products)

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | SleepWise Reviews</title>
  <meta name="description" content="{description}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://sleepwisereviews.com/posts/{slug}.html" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="https://sleepwisereviews.com/posts/{slug}.html" />
  <meta property="og:image" content="https://sleepwisereviews.com/images/og-default.png" />
  <meta property="og:site_name" content="SleepWise Reviews" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{description}" />
  {schema_block}
  <style>
    :root {{
      --bg: #0a1628; --card: #111e33; --gold: #c9a84c;
      --text: #e8e0d0; --muted: #8899aa; --border: rgba(201,168,76,0.15);
      --green: #4caf82; --red: #c9504c;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: var(--bg); color: var(--text); font-family: 'Georgia', serif; line-height: 1.7; }}
    header {{ background: var(--card); border-bottom: 1px solid var(--border); padding: 1rem 2rem; display: flex; align-items: center; justify-content: space-between; }}
    .logo {{ color: var(--gold); text-decoration: none; font-size: 1.3rem; font-weight: 700; }}
    .logo span {{ color: var(--text); }}
    main {{ max-width: 860px; margin: 0 auto; padding: 3rem 1.5rem; }}
    h1 {{ font-size: 2rem; color: var(--gold); margin-bottom: 0.75rem; }}
    .intro {{ color: var(--muted); font-size: 1.05rem; margin-bottom: 2.5rem; }}
    .science-box {{ background: var(--card); border-left: 3px solid var(--gold); padding: 1.2rem 1.5rem; border-radius: 6px; margin-bottom: 2.5rem; font-size: 0.95rem; color: var(--text); }}
    .science-box strong {{ color: var(--gold); display: block; margin-bottom: 0.4rem; }}
    .toc {{ background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 1.5rem 2rem; margin-bottom: 3rem; }}
    .toc h2 {{ color: var(--gold); font-size: 1.1rem; margin-bottom: 1rem; }}
    .toc ol {{ padding-left: 1.2rem; }}
    .toc li {{ margin-bottom: 0.4rem; font-size: 0.9rem; }}
    .toc a {{ color: var(--text); text-decoration: none; }}
    .toc a:hover {{ color: var(--gold); }}
    .toc-badge {{ color: var(--muted); font-size: 0.8rem; font-family: sans-serif; margin-left: 0.3rem; }}
    .product-card {{ background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 2rem; margin-bottom: 2.5rem; }}
    .product-header {{ display: flex; gap: 1.2rem; align-items: flex-start; margin-bottom: 1.2rem; }}
    .rank-badge {{ background: var(--gold); color: #0a1628; font-weight: 700; font-size: 1.1rem; font-family: sans-serif; width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }}
    .product-title-block {{ flex: 1; }}
    .best-badge {{ background: rgba(201,168,76,0.15); color: var(--gold); font-size: 0.78rem; font-family: sans-serif; padding: 0.2rem 0.7rem; border-radius: 20px; border: 1px solid var(--border); text-transform: uppercase; letter-spacing: 0.05em; }}
    .product-name {{ font-size: 1.25rem; color: var(--text); margin: 0.4rem 0 0.6rem; }}
    .spec-chips {{ display: flex; flex-wrap: wrap; gap: 0.5rem; }}
    .chip {{ background: rgba(255,255,255,0.05); border: 1px solid var(--border); border-radius: 20px; padding: 0.2rem 0.8rem; font-size: 0.8rem; font-family: sans-serif; color: var(--muted); }}
    .price-chip {{ color: var(--gold); border-color: rgba(201,168,76,0.3); }}
    .why-box {{ background: rgba(201,168,76,0.07); border-left: 3px solid var(--gold); padding: 0.9rem 1.2rem; border-radius: 0 6px 6px 0; font-size: 0.95rem; margin-bottom: 1.2rem; }}
    .pros-cons-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.5rem; }}
    .pros-col h4 {{ color: var(--green); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; font-family: sans-serif; }}
    .cons-col h4 {{ color: var(--red); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; font-family: sans-serif; }}
    .pros-col ul, .cons-col ul {{ list-style: none; }}
    .pros-col li::before {{ content: '+ '; color: var(--green); font-weight: 700; }}
    .cons-col li::before {{ content: '- '; color: var(--red); font-weight: 700; }}
    .pros-col li, .cons-col li {{ font-size: 0.9rem; margin-bottom: 0.35rem; }}
    .buy-btn {{ display: inline-block; background: var(--gold); color: #0a1628; font-weight: 700; font-family: sans-serif; padding: 0.75rem 2rem; border-radius: 6px; text-decoration: none; font-size: 0.95rem; transition: opacity 0.2s; }}
    .buy-btn:hover {{ opacity: 0.85; }}
    .guide-table {{ width: 100%; border-collapse: collapse; margin: 1rem 0 2rem; font-size: 0.9rem; }}
    .guide-table th {{ background: rgba(201,168,76,0.15); color: var(--gold); text-align: left; padding: 0.7rem 1rem; font-family: sans-serif; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.04em; }}
    .guide-table td {{ padding: 0.65rem 1rem; border-bottom: 1px solid var(--border); color: var(--text); vertical-align: top; }}
    .guide-table tr:last-child td {{ border-bottom: none; }}
    .section-box {{ background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 2rem; margin-bottom: 2.5rem; }}
    .section-box h2 {{ color: var(--gold); font-size: 1.3rem; margin-bottom: 1rem; }}
    .section-box p {{ font-size: 0.95rem; margin-bottom: 0.8rem; color: var(--text); }}
    .decision-box {{ background: rgba(201,168,76,0.07); border: 1px solid rgba(201,168,76,0.3); border-radius: 10px; padding: 1.5rem 2rem; margin-bottom: 2.5rem; }}
    .decision-box h2 {{ color: var(--gold); margin-bottom: 1rem; font-size: 1.2rem; }}
    .decision-box .rule {{ padding: 0.7rem 0; border-bottom: 1px solid var(--border); font-size: 0.95rem; }}
    .decision-box .rule:last-child {{ border-bottom: none; }}
    .decision-box .label {{ font-weight: bold; color: var(--gold); }}
    .faq-section {{ margin-top: 3rem; }}
    .faq-section h2 {{ color: var(--gold); font-size: 1.3rem; margin-bottom: 1.5rem; }}
    .faq-item {{ border-bottom: 1px solid var(--border); padding: 1.2rem 0; }}
    .faq-item:last-child {{ border-bottom: none; }}
    .faq-q {{ font-size: 1rem; color: var(--text); margin-bottom: 0.5rem; }}
    .faq-a {{ font-size: 0.9rem; color: var(--muted); }}
    footer {{ text-align: center; padding: 2rem; color: var(--muted); font-size: 0.85rem; border-top: 1px solid var(--border); margin-top: 4rem; }}
    footer a {{ color: var(--gold); }}
    .affiliate-disclaimer {{ background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: 6px; padding: 0.9rem 1.2rem; font-size: 0.8rem; color: var(--muted); margin-bottom: 2rem; font-family: sans-serif; }}
    @media (max-width: 600px) {{
      .pros-cons-grid {{ grid-template-columns: 1fr; }}
      .product-header {{ flex-direction: column; }}
      h1 {{ font-size: 1.5rem; }}
    }}
  </style>
</head>
<body>
  <header>
    <a class="logo" href="../">SleepWise<span>Reviews</span></a>
    <a href="../posts/" style="color:var(--muted);font-size:0.9rem;text-decoration:none;">All Guides</a>
  </header>
  <main>
    <h1>{title}</h1>
    <p class="intro">{description}</p>

    <div class="affiliate-disclaimer">We may earn a commission if you buy through links on this page. This doesn't affect our recommendations — we only feature products we'd personally endorse.</div>

    <div class="science-box">
      <strong>The Research on Mattress Firmness</strong>
      A 2003 randomized controlled trial in The Lancet found medium-firm mattresses reduced chronic lower back pain and sleep-related disability significantly more than firm mattresses. A 2015 study found subjective firmness preference and objective sleep quality were highest in the medium-firm range (5.6-6.5/10 on a 10-point firmness scale) for most adult sleepers. The takeaway: medium-firm is the evidence-based default. Depart from it only when sleep position requires it.
    </div>

    <div class="decision-box">
      <h2>Quick Decision Guide: Which Firmness For You?</h2>
      <div class="rule"><span class="label">Side sleeper, under 230lb:</span> Medium (4-5/10) — shoulder and hip need to sink</div>
      <div class="rule"><span class="label">Side sleeper, over 230lb:</span> Medium Firm (6/10) — more compression from weight</div>
      <div class="rule"><span class="label">Back sleeper, under 230lb:</span> Medium Firm (6-7/10) — best for lumbar support</div>
      <div class="rule"><span class="label">Back sleeper, over 230lb:</span> Firm (7-8/10) — prevents hip sinkage</div>
      <div class="rule"><span class="label">Stomach sleeper, any weight:</span> Firm (7-9/10) — prevents lumbar hyperextension</div>
      <div class="rule"><span class="label">Combo sleeper:</span> Medium Firm (6/10) — best all-positions compromise</div>
      <div class="rule"><span class="label">Couple with different preferences:</span> Medium Firm (6/10) or split king</div>
    </div>

    <nav class="toc">
      <h2>Top Firm and Medium Firm Mattress Picks</h2>
      <ol>{toc_items}</ol>
    </nav>

{cards_html}

    <div class="section-box">
      <h2>Firmness Scale Explained</h2>
      <table class="guide-table">
        <thead>
          <tr><th>Scale (1-10)</th><th>Label</th><th>Best For</th><th>Avoid If</th></tr>
        </thead>
        <tbody>
          <tr><td>1-3</td><td>Soft / Plush</td><td>Side sleepers under 150lb, those with hip/shoulder pain</td><td>Back or stomach sleepers</td></tr>
          <tr><td>4-5</td><td>Medium Soft</td><td>Side sleepers, lighter body types</td><td>Stomach sleepers</td></tr>
          <tr><td>5-6</td><td>Medium</td><td>Combo sleepers, couples, most body types</td><td>Severe stomach sleepers</td></tr>
          <tr><td>6-7</td><td>Medium Firm</td><td>Back sleepers, combo sleepers, most people</td><td>Petite side sleepers</td></tr>
          <tr><td>7-8</td><td>Firm</td><td>Stomach sleepers, heavy back sleepers</td><td>Side sleepers (pressure points)</td></tr>
          <tr><td>8-10</td><td>Extra Firm</td><td>Very heavy stomach sleepers, specific medical need</td><td>Most sleepers — too uncomfortable</td></tr>
        </tbody>
      </table>
      <p style="font-size:0.85rem;color:var(--muted);">Note: Firmness scales vary by brand. One brand's "6" may equal another's "7." Always check if brands publish their scale or read independent reviews that standardize the scale.</p>
    </div>

    <div class="section-box">
      <h2>The Firmness Marketing Problem</h2>
      <p>Mattress companies label firmness inconsistently. Brands often market everything as "medium firm" because it sells best. What one company calls "firm" may be another's "medium." The only reliable way to know: independent reviewers who use a standardized firmness scale, or long trial periods (365 nights) that let you test in real sleeping conditions.</p>
      <p>The best approach: identify your firmness need from the decision guide above, then choose a mattress with a long trial period. If it doesn't match your expectation of the firmness level, return it. Never trust firmness ratings alone without a trial period.</p>
    </div>

{faq_html}

    <div class="affiliate-disclaimer" style="margin-top:2rem;">Prices accurate at time of publication. Verify on Amazon before purchasing. Amazon links are affiliate links — we earn a small commission at no cost to you.</div>
  </main>
  <footer>
    <p>&copy; 2025–2026 <a href="../">SleepWise Reviews</a> &middot; Evidence-based sleep guidance &middot; <a href="../posts/">All Guides</a></p>
  </footer>
</body>
</html>'''

out = os.path.join(os.path.dirname(__file__), 'posts', f'{slug}.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'Written: {out}')
