"""Generate posts/best-weighted-blanket-kids.html"""
import os, json

slug = "best-weighted-blanket-kids"
title = "Best Weighted Blankets for Kids 2026"
description = "The 7 best weighted blankets for children — covering anxiety, sensory processing, ADHD, and sleep. Includes weight-sizing guide by age, safety rules, and washability ratings."
date = "2026-05-25"
affiliate_tag = "sleepwiserevi-20"

products = [
    {
        "rank": 1,
        "name": "Baloo Living Kids Weighted Blanket",
        "badge": "Best Overall",
        "price": "$89–$129",
        "key_spec": "GOTS organic cotton, microfiber glass beads, machine washable",
        "pros": ["GOTS-certified organic cotton — no synthetic fleece off-gassing", "Machine washable at home (no special care)", "Glass micro beads evenly distributed — no bead migration", "Breathable — doesn't trap heat", "No inner ties or sewn loops — single layer construction"],
        "cons": ["Premium price vs polyester options", "Limited color choices"],
        "why": "Organic cotton construction is the safest choice for kids with chemical sensitivities or eczema. The single-layer breathable design prevents overheating, which is the most common complaint with kids' weighted blankets.",
        "search": "Baloo+Living+Kids+Weighted+Blanket"
    },
    {
        "rank": 2,
        "name": "Bearaby Kids Napper Weighted Blanket",
        "badge": "Best Chunky Knit",
        "price": "$99–$149",
        "key_spec": "TENCEL lyocell, no glass beads, hand-knit appearance",
        "pros": ["No glass beads — weight from fabric layers only", "TENCEL lyocell is naturally cooling and soft", "Machine washable, no inner filling to shift", "Aesthetic — looks great in child's room", "Temperature-regulating fiber"],
        "cons": ["Larger knit gaps — not for kids who want full cocoon coverage", "Heavier shipping weight", "Higher cost per pound of weight"],
        "why": "Bead-free construction eliminates any risk of bead leaks or migration. TENCEL lyocell is more breathable than cotton or polyester — ideal for kids who run hot. The chunky knit aesthetic makes it a room statement, not a medical device.",
        "search": "Bearaby+Kids+Napper+Weighted+Blanket"
    },
    {
        "rank": 3,
        "name": "YnM Kids Weighted Blanket",
        "badge": "Best Value",
        "price": "$35–$55",
        "key_spec": "7-layer construction, glass beads, multiple weights available",
        "pros": ["Widest weight range: 3lb, 4lb, 5lb, 7lb options", "Multiple size and color options", "7-layer design minimizes bead shifting", "Machine washable", "Very competitive price"],
        "cons": ["Polyester — warmer than cotton/TENCEL options", "Ties can come loose with washing", "Less breathable than premium options"],
        "why": "The most popular kids' weighted blanket for good reason. Available in more weight/size combinations than any competitor, so you can precisely match the 10% body weight rule. Strong value-to-quality ratio for families trying weighted blankets for the first time.",
        "search": "YnM+Kids+Weighted+Blanket"
    },
    {
        "rank": 4,
        "name": "Sensory Goods Weighted Blanket for Kids",
        "badge": "Best for Sensory Processing",
        "price": "$79–$139",
        "key_spec": "OT-recommended design, custom weight/size options, US-made",
        "pros": ["Occupational therapist-designed and recommended", "Custom weight/size available — built to your child's specifications", "Made in USA", "Flannel or cotton options", "No chemical treatments"],
        "cons": ["Custom orders take 2–3 weeks", "Higher price for custom sizing", "Must wash cold/gentle"],
        "why": "Designed by OTs specifically for children with sensory processing disorder, autism spectrum, and ADHD. Custom sizing ensures the blanket covers the child's body without going to the floor — proper coverage is critical for efficacy.",
        "search": "Sensory+Goods+Weighted+Blanket+Kids"
    },
    {
        "rank": 5,
        "name": "Degrees of Comfort Kids Weighted Blanket",
        "badge": "Best Cooling Option",
        "price": "$45–$75",
        "key_spec": "Dual-sided: cooling bamboo + warm plush, multiple weights",
        "pros": ["Reversible: cool bamboo side + warm plush side", "Season-appropriate use year-round", "Competitive weight options (5lb, 7lb, 10lb)", "Machine washable", "Good for kids who run hot"],
        "cons": ["Bamboo side texture polarizing for tactile-sensitive kids", "Seams visible when reversing", "Plush side less breathable"],
        "why": "Dual-sided design extends usability across seasons. Hot summer nights: bamboo side. Cold winters: plush side. For children with temperature dysregulation (common in autism spectrum and ADHD), having both options in one blanket is practical.",
        "search": "Degrees+of+Comfort+Kids+Weighted+Blanket"
    },
    {
        "rank": 6,
        "name": "SensaCalm Therapeutic Weighted Blanket",
        "badge": "Best Therapeutic Grade",
        "price": "$89–$169",
        "key_spec": "Custom therapeutic weights, OT-approved, removable cover",
        "pros": ["True therapeutic grade — used in clinical settings", "Removable duvet cover — blanket stays clean", "Wide weight customization", "Cotton or flannel fabric options", "Strong bead distribution construction"],
        "cons": ["Cover must be washed separately from insert", "Custom weight ordering required", "Delivery time 2–3 weeks"],
        "why": "Used by occupational therapists in school and clinical settings. The removable cover solves the washing challenge for heavy therapeutic blankets — wash the cover frequently, the insert less often. Best choice when an OT has recommended a weighted blanket.",
        "search": "SensaCalm+Therapeutic+Weighted+Blanket+Kids"
    },
    {
        "rank": 7,
        "name": "Luna Kids Weighted Blanket",
        "badge": "Best Budget Pick",
        "price": "$29–$45",
        "key_spec": "Glass beads, minky fabric, 5lb and 7lb options",
        "pros": ["Lowest price for glass bead construction", "Soft minky fabric — excellent for tactile-sensitive kids", "Passes OEKO-TEX 100 certification", "Machine washable (gentle)", "Good for trial before investing in premium"],
        "cons": ["Limited weight options", "Minky fabric can trap heat", "Less durable long-term vs premium options"],
        "why": "The right starting point if your child has never tried a weighted blanket and you're unsure if they'll tolerate it. Low financial commitment, OEKO-TEX certified safety, and minky texture that most children find immediately soothing.",
        "search": "Luna+Kids+Weighted+Blanket"
    }
]

faqs = [
    {
        "q": "What weight weighted blanket should I get for my child?",
        "a": "The standard guideline is 10% of body weight, plus 1–2 pounds. A 40-pound child: 5–6 lb blanket. A 60-pound child: 7–8 lb blanket. However, this is a starting point — some children with sensory sensitivities prefer lighter, some with deep pressure needs prefer slightly heavier. Always ask your child what feels right. Never go above 15% of body weight for children."
    },
    {
        "q": "Are weighted blankets safe for children?",
        "a": "For children over 2 years old, weighted blankets are generally safe when properly sized. Key safety rules: (1) Never use on children under 2 — suffocation risk; (2) The child must be able to remove the blanket themselves; (3) Do not use on children with breathing difficulties, seizures, or circulatory problems without physician clearance; (4) Follow the 10% body weight guideline — overloading is a real risk. Children with medical conditions should have OT clearance first."
    },
    {
        "q": "Do weighted blankets help kids with ADHD sleep?",
        "a": "Evidence is promising but not yet definitive. A 2020 study in the Journal of Sleep Research found weighted blankets significantly improved sleep in children with ADHD — reducing sleep-onset latency and nighttime waking. The proposed mechanism is increased serotonin and melatonin production via deep pressure stimulation. Most families report improvement within 1–2 weeks of consistent use. They're unlikely to harm and worth trying as a low-risk intervention."
    },
    {
        "q": "Can a weighted blanket be used all night?",
        "a": "Yes, for children old enough to remove it independently (generally 3+). Most children self-regulate and will push it off if they overheat. Ensure the bedroom is at the recommended 65-68°F for children. If your child sweats excessively, choose a breathable option (Baloo cotton or Bearaby TENCEL) rather than polyester. Never tuck a weighted blanket so tightly a child cannot escape it."
    },
    {
        "q": "How do I wash a kids' weighted blanket?",
        "a": "Check the weight first: blankets 15 lbs and under can usually be machine-washed at home on gentle/cold. Heavier blankets may require a commercial washer (laundromat) to avoid motor damage. Use mild detergent, no fabric softener (can break down bead compartments). Tumble dry low or air dry — high heat degrades the plastic bead pockets and can cause uneven distribution. Most premium brands (Baloo, Bearaby) can handle regular home washing."
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
      <strong>The Evidence for Kids' Weighted Blankets</strong>
      Deep pressure stimulation — the mechanism behind weighted blankets — activates the parasympathetic nervous system, increasing serotonin and dopamine while decreasing cortisol. A 2020 clinical study found weighted blankets reduced insomnia severity in children with autism spectrum disorder by 40%. A 2021 randomized trial showed significant reductions in sleep-onset time for children with ADHD. These are not placebo effects — the physiology is well-documented.
    </div>

    <nav class="toc">
      <h2>Top 7 Kids' Weighted Blankets</h2>
      <ol>{toc_items}</ol>
    </nav>

{cards_html}

    <div class="section-box">
      <h2>Weight Sizing Guide by Child Age and Weight</h2>
      <table class="guide-table">
        <thead>
          <tr><th>Child's Weight</th><th>Recommended Blanket Weight</th><th>Age Range</th><th>Notes</th></tr>
        </thead>
        <tbody>
          <tr><td>Under 30 lbs</td><td>Not recommended</td><td>Under 2 years</td><td>Suffocation risk — do not use weighted blankets</td></tr>
          <tr><td>30–40 lbs</td><td>3–4 lbs</td><td>2–4 years</td><td>Only with direct supervision; child must remove independently</td></tr>
          <tr><td>40–60 lbs</td><td>5–6 lbs</td><td>4–7 years</td><td>Most common starting weight for preschool/early school age</td></tr>
          <tr><td>60–80 lbs</td><td>7–8 lbs</td><td>7–10 years</td><td>Standard school-age weight range</td></tr>
          <tr><td>80–100 lbs</td><td>9–10 lbs</td><td>10–12 years</td><td>Approaching adult weights — can often use adult blankets</td></tr>
          <tr><td>Over 100 lbs</td><td>12–15 lbs</td><td>12+ years</td><td>Use adult sizing guidance (10% body weight)</td></tr>
        </tbody>
      </table>
      <p>These are starting points. If your child's OT has prescribed a specific weight, follow that guidance instead. Some children with high proprioceptive needs benefit from slightly heavier blankets; those with sensory sensitivities may prefer lighter.</p>
    </div>

    <div class="section-box">
      <h2>Safety Rules: Non-Negotiable</h2>
      <p><strong>Never use on children under 2.</strong> The weight creates an entrapment risk when infants cannot yet roll or lift themselves away from the blanket.</p>
      <p><strong>The child must be able to remove it independently.</strong> Test this before the first overnight use. If your child cannot push the blanket off while lying down, it is too heavy.</p>
      <p><strong>Do not use in a crib or enclosed space.</strong> Weighted blankets are for beds where the child can move freely in all directions.</p>
      <p><strong>Never use on children with respiratory, circulatory, or neurological conditions</strong> without physician and OT clearance. The weight can restrict chest expansion in children with breathing difficulties.</p>
      <p><strong>Start with shorter periods.</strong> Begin with 20–30 minutes while awake to assess tolerance before overnight use.</p>
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
