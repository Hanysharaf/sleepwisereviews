"""Generate posts/index.html — a categorized index of all posts."""
import os, re, json

POSTS_DIR = os.path.join(os.path.dirname(__file__), 'posts')
BASE_URL = 'https://sleepwisereviews.com/posts/'

EXCLUDED = {'index'}

CATEGORIES = {
    'Insomnia & CBT-I': ['insomnia-types', 'cbt-i-guide', 'sleep-anxiety-techniques', 'sleep-when-anxious', 'sleep-disorders-overview', 'sleep-paralysis-explained', 'sleep-ptsd', 'rem-behavior-disorder', 'rem-rebound-explained'],
    'Sleep Science': ['sleep-stages-explained', 'circadian-rhythm-basics', 'chronobiology-basics', 'adenosine-sleep-drive', 'sleep-genetics', 'brain-during-sleep', 'dreams-science', 'deep-sleep-benefits', 'rem-sleep-benefits', 'light-sleep-importance', 'sleep-memory-learning', 'sleep-immune-system'],
    'Caffeine & Nutrition': ['caffeine-half-life-sleep', 'blue-light-melatonin', 'melatonin-guide', 'alcohol-sleep-quality', 'sleep-food-connection', 'magnesium-deficiency-sleep', 'magnesium-types-sleep', 'natural-sleep-aids', 'sleep-fasting', 'sleep-hydration', 'sleep-hydration-guide', 'sleep-and-alcohol-free', 'gut-microbiome-sleep', 'sleep-and-thyroid', 'sleep-and-gut-health'],
    'Sleep Environment': ['bedroom-temperature-sleep', 'sleep-environment-optimization', 'sleep-sanctuary-guide', 'bedroom-plants-sleep', 'bedroom-tech-sleep', 'sleep-screen-detox', 'sleep-temperature-regulation', 'sleep-light-therapy', 'altitude-sleep', 'sleep-camping'],
    'Health Conditions': ['sleep-apnea-warning-signs', 'sleep-apnea-diagnosis', 'home-sleep-apnea-test', 'snoring-causes-fixes', 'restless-legs-syndrome', 'sleep-chronic-pain', 'sleep-fibromyalgia', 'sleep-and-pain', 'sleep-depression', 'sleep-mental-health', 'sleep-heart-health', 'sleep-and-diabetes', 'sleep-and-alzheimers', 'sleep-autism-spectrum', 'bad-mattress-health-effects', 'sleep-after-surgery', 'sleep-skin-health', 'sleep-after-covid'],
    'Life Stages': ['pregnancy-sleep-guide', 'kids-sleep-guide', 'kids-screen-time-sleep', 'teen-sleep-guide', 'aging-and-sleep', 'women-sleep-differences', 'menopause-sleep', 'sleep-menstrual-cycle', 'sleep-new-baby', 'couples-sleep-problems', 'best-pregnancy-pillows', 'best-body-pillow', 'best-white-noise-machine-baby'],
    'Timing & Jet Lag': ['reset-sleep-schedule', 'jet-lag-guide', 'sleep-travel-tips', 'sleep-business-travel', 'social-jetlag', 'daylight-saving-sleep', 'shift-work-shift', 'night-shift-optimization', 'polyphasic-sleep', 'polyphasic-sleep-schedules', 'sleep-consistency-importance', 'weekend-sleep-mistake', 'wrong-sleeping-in-weekends', 'shift-work-sleep', 'best-travel-pillow'],
    'Napping & Performance': ['power-nap-science', 'napping-science', 'sleep-inertia', 'microsleep-dangers', 'sleep-athletic-performance', 'sleep-exercise-timing', 'sleep-productivity', 'sleep-goal-setting', 'sleep-longevity', 'sleep-creativity', 'sleep-mental-performance'],
    'Guides & Plans': ['ultimate-sleep-guide', 'sleep-hygiene-checklist', 'wind-down-routine', 'morning-habits-sleep', 'sleep-journal-guide', '30-day-sleep-challenge', 'sleep-debt-accumulation', 'sleep-debt-recovery', 'summer-sleep-guide', 'winter-sleep-guide', 'sleep-exam-study', 'sleep-tracking-worth-it', 'sleep-tracking-data', 'hypnic-jerk-explained', 'lucid-dreaming-guide', 'sleep-myth-8-hours', 'sleep-myths-series', 'sleep-quality-vs-quantity', 'waking-at-3am', 'sleep-chronotypes', 'morning-lark-night-owl', 'sleep-cortisol-stress', 'sleep-and-hormones', 'sleep-loneliness', 'sleep-grief', 'sleep-adhd', 'sleep-and-weight-loss', 'does-sex-before-bed-help-sleep', 'sex-and-sleep-intimacy-quality', 'how-much-sleep-do-i-need', 'how-to-fall-asleep-fast', 'best-sleep-position'],
    'Mattresses & Bedding': ['best-mattresses-back-pain', 'best-mattresses-couples-2026', 'best-mattress-toppers', 'best-cooling-mattress-pads', 'best-cooling-pillows', 'best-cooling-sheets', 'best-linen-sheets', 'best-bamboo-sheets', 'best-mattress-stomach-sleepers', 'best-mattress-side-sleepers', 'best-mattress-back-sleepers', 'best-pillow-sleep-position', 'best-pillow-side-sleepers', 'best-pillow-neck-pain', 'best-grounding-sheets', 'best-memory-foam-pillow', 'mattress-buying-guide', 'memory-foam-vs-hybrid-mattress', 'latex-vs-memory-foam-mattress', 'best-mattresses-under-500', 'best-smart-mattresses', 'best-latex-mattress', 'best-duvet-insert', 'best-mattress-protector', 'best-cooling-mattress-topper', 'best-silk-pillowcase', 'best-adjustable-bed-frame', 'best-cooling-comforter', 'best-down-alternative-comforter', 'best-mattress-pad'],
    'Sleep Products': ['best-sleep-masks', 'best-blackout-curtains', 'best-humidifiers-sleep', 'best-sleep-headphones', 'article-white-noise-machines', 'best-white-noise-machines-sleeping', 'best-light-therapy-lamps', 'best-blue-light-glasses', 'best-aromatherapy-sleep', 'best-cpap-alternatives', 'article-weighted-blanket', 'best-anti-snoring-devices', 'best-sleep-monitors', 'best-sleep-apps', 'best-sleep-tracking-rings', 'best-earplugs-sleeping', 'best-sunrise-alarm-clocks', 'best-weighted-blankets-adults', 'best-knee-pillow', 'best-bed-wedge-pillow', 'best-alarm-clock-heavy-sleepers', 'best-electric-blanket'],
    'Supplements': ['best-melatonin-supplements', 'best-sleep-supplements-guide', 'best-valerian-root-supplements', 'article-magnesium-sleep', 'sleep-medications-truth', 'best-ashwagandha-sleep', 'best-magnesium-glycinate', 'best-sleep-gummies', 'best-l-theanine-supplement', 'best-melatonin-for-kids'],
}

# Build title map
title_map = {}
for fn in os.listdir(POSTS_DIR):
    if not fn.endswith('.html'):
        continue
    slug = fn.replace('.html', '')
    if slug in EXCLUDED:
        continue
    with open(os.path.join(POSTS_DIR, fn), encoding='utf-8') as f:
        html = f.read()
    tm = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL)
    title = re.sub(r'<[^>]+>', '', tm.group(1)).strip() if tm else slug.replace('-', ' ').title()
    title = re.sub(r'\s*[|\-–]\s*(SleepWise.*|Sleep.*)$', '', title).strip()
    title_map[slug] = title

# Build category sections HTML
category_html = ''
for cat_name, slugs in CATEGORIES.items():
    valid_slugs = [s for s in slugs if os.path.exists(os.path.join(POSTS_DIR, s + '.html'))]
    if not valid_slugs:
        continue
    links = ''
    for slug in valid_slugs:
        title = title_map.get(slug, slug.replace('-', ' ').title())
        links += f'      <li><a href="{slug}.html">{title}</a></li>\n'
    category_html += f'''  <section class="cat-section">
    <h2>{cat_name} <span class="count">({len(valid_slugs)})</span></h2>
    <ul class="post-list">
{links}    </ul>
  </section>

'''

# Track uncategorized posts
all_categorized = set()
for slugs in CATEGORIES.values():
    all_categorized.update(slugs)
all_posts = set(fn.replace('.html', '') for fn in os.listdir(POSTS_DIR) if fn.endswith('.html') and fn.replace('.html', '') not in EXCLUDED)
uncategorized = all_posts - all_categorized
if uncategorized:
    links = ''
    for slug in sorted(uncategorized):
        title = title_map.get(slug, slug.replace('-', ' ').title())
        links += f'      <li><a href="{slug}.html">{title}</a></li>\n'
    category_html += f'''  <section class="cat-section">
    <h2>Other Guides <span class="count">({len(uncategorized)})</span></h2>
    <ul class="post-list">
{links}    </ul>
  </section>

'''

# Schema
schema = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "All Sleep Guides — SleepWise Reviews",
    "description": "Complete index of 162 sleep guides covering insomnia, mattresses, sleep science, and health conditions.",
    "url": "https://sleepwisereviews.com/posts/",
    "publisher": {
        "@type": "Organization",
        "name": "SleepWise Reviews",
        "url": "https://sleepwisereviews.com/"
    }
}
schema_block = '<script type="application/ld+json">\n' + json.dumps(schema, indent=2) + '\n</script>'

total_count = len([f for f in os.listdir(POSTS_DIR) if f.endswith('.html')])

html_out = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>All Sleep Guides — SleepWise Reviews ({total_count} Articles)</title>
  <meta name="description" content="Complete index of {total_count} sleep guides — insomnia, mattresses, sleep science, health conditions, and more. Evidence-based sleep research in one place." />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://sleepwisereviews.com/posts/" />
  <meta property="og:title" content="All Sleep Guides — SleepWise Reviews ({total_count} Articles)" />
  <meta property="og:description" content="Complete categorized index of {total_count} science-backed sleep guides." />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://sleepwisereviews.com/posts/" />
  <meta property="og:image" content="https://sleepwisereviews.com/images/og-default.png" />
  <meta property="og:site_name" content="SleepWise Reviews" />
  {schema_block}
  <style>
    :root {{
      --bg: #0a1628; --card: #111e33; --gold: #c9a84c;
      --text: #e8e0d0; --muted: #8899aa; --border: rgba(201,168,76,0.15);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: var(--bg); color: var(--text); font-family: 'Georgia', serif; line-height: 1.7; }}
    header {{ background: var(--card); border-bottom: 1px solid var(--border); padding: 1rem 2rem; display: flex; align-items: center; justify-content: space-between; }}
    .logo {{ color: var(--gold); text-decoration: none; font-size: 1.3rem; font-weight: 700; }}
    .logo span {{ color: var(--text); }}
    main {{ max-width: 960px; margin: 0 auto; padding: 3rem 1.5rem; }}
    h1 {{ font-size: 2rem; color: var(--gold); margin-bottom: 0.5rem; }}
    .subtitle {{ color: var(--muted); margin-bottom: 3rem; font-size: 1.05rem; }}
    .cat-section {{ margin-bottom: 2.5rem; }}
    .cat-section h2 {{ font-size: 1.2rem; color: var(--gold); border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; margin-bottom: 1rem; }}
    .count {{ color: var(--muted); font-size: 0.85rem; font-family: sans-serif; }}
    .post-list {{ list-style: none; columns: 2; column-gap: 2rem; }}
    .post-list li {{ break-inside: avoid; margin-bottom: 0.4rem; }}
    .post-list a {{ color: var(--text); text-decoration: none; font-size: 0.9rem; }}
    .post-list a:hover {{ color: var(--gold); }}
    footer {{ text-align: center; padding: 2rem; color: var(--muted); font-size: 0.85rem; border-top: 1px solid var(--border); }}
    footer a {{ color: var(--gold); }}
    @media (max-width: 600px) {{ .post-list {{ columns: 1; }} }}
  </style>
</head>
<body>
  <header>
    <a class="logo" href="../">SleepWise<span>Reviews</span></a>
    <a href="../" style="color:var(--muted);font-size:0.9rem;text-decoration:none;">← Home</a>
  </header>
  <main>
    <h1>All Sleep Guides</h1>
    <p class="subtitle">{total_count} articles covering sleep science, insomnia, mattresses, health conditions, and more.</p>
{category_html}  </main>
  <footer>
    <p>&copy; 2025–2026 <a href="../">SleepWise Reviews</a> · Evidence-based sleep guidance</p>
  </footer>
</body>
</html>
'''

output_path = os.path.join(POSTS_DIR, 'index.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_out)

print(f'Generated posts/index.html ({total_count} posts, {len(CATEGORIES)} categories)')
if uncategorized:
    print(f'Uncategorized: {len(uncategorized)} posts → {sorted(uncategorized)}')
