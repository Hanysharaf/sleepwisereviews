"""Generate posts/index.html — a categorized index of all posts."""
import os, re, json

POSTS_DIR = os.path.join(os.path.dirname(__file__), 'posts')
BASE_URL = 'https://sleepwisereviews.com/posts/'

EXCLUDED = {'index'}

CATEGORIES = {
    'Insomnia & CBT-I': ['insomnia-types', 'cbt-i-guide', 'sleep-anxiety-techniques', 'sleep-when-anxious', 'sleep-disorders-overview', 'sleep-paralysis-explained', 'sleep-ptsd', 'rem-behavior-disorder', 'rem-rebound-explained'],
    'Sleep Science': ['sleep-stages-explained', 'circadian-rhythm-basics', 'chronobiology-basics', 'adenosine-sleep-drive', 'sleep-genetics', 'brain-during-sleep', 'dreams-science', 'deep-sleep-benefits', 'rem-sleep-benefits', 'light-sleep-importance', 'sleep-memory-learning', 'sleep-immune-system'],
    'Caffeine & Nutrition': ['caffeine-half-life-sleep', 'blue-light-melatonin', 'melatonin-guide', 'alcohol-sleep-quality', 'sleep-food-connection', 'magnesium-deficiency-sleep', 'magnesium-types-sleep', 'natural-sleep-aids', 'sleep-fasting', 'sleep-hydration', 'sleep-hydration-guide', 'sleep-and-alcohol-free', 'gut-microbiome-sleep', 'sleep-and-thyroid', 'sleep-and-gut-health'],
    'Sleep Environment': ['bedroom-temperature-sleep', 'sleep-environment-optimization', 'sleep-sanctuary-guide', 'bedroom-plants-sleep', 'bedroom-tech-sleep', 'sleep-screen-detox', 'sleep-temperature-regulation', 'sleep-light-therapy', 'altitude-sleep', 'sleep-camping', 'best-blackout-curtain-liner'],
    'Health Conditions': ['sleep-apnea-warning-signs', 'sleep-apnea-diagnosis', 'home-sleep-apnea-test', 'snoring-causes-fixes', 'restless-legs-syndrome', 'sleep-chronic-pain', 'sleep-fibromyalgia', 'sleep-and-pain', 'sleep-depression', 'sleep-mental-health', 'sleep-heart-health', 'sleep-and-diabetes', 'sleep-and-alzheimers', 'sleep-autism-spectrum', 'bad-mattress-health-effects', 'sleep-after-surgery', 'sleep-skin-health', 'sleep-after-covid', 'best-mouthguard-teeth-grinding', 'best-cpap-mask-side-sleepers', 'best-pillow-for-cervical-spondylosis', 'best-mattress-fibromyalgia', 'best-anti-snoring-pillow', 'best-cpap-humidifier', 'best-pillow-for-side-sleepers-shoulder-pain', 'best-cpap-machine-travel', 'best-mattress-sciatica', 'best-mattress-migraines', 'best-mattress-diabetes', 'best-mattress-plantar-fasciitis', 'best-mattress-copd', 'best-mattress-anxiety', 'best-mattress-pcos', 'best-mattress-endometriosis', 'best-mattress-depression', 'best-mattress-heart-failure', 'best-mattress-obesity', 'best-mattress-long-covid', 'best-mattress-ptsd', 'best-mattress-adhd', 'best-mattress-asthma', 'best-mattress-bipolar', 'best-mattress-autism', 'best-mattress-ibs', 'best-mattress-interstitial-cystitis', 'best-mattress-hypothyroidism', 'best-mattress-cancer-treatment', 'best-mattress-epilepsy', 'best-mattress-osteoarthritis', 'best-mattress-gout', 'best-mattress-hiv-aids', 'best-mattress-stroke-recovery', 'best-mattress-multiple-chemical-sensitivity', 'best-mattress-kidney-disease', 'best-mattress-copd-overlap', 'best-mattress-inflammatory-bowel-disease', 'best-mattress-spinal-cord-injury', 'best-mattress-alzheimers-dementia', 'best-mattress-traumatic-brain-injury', 'best-mattress-psoriatic-arthritis', 'best-mattress-type1-diabetes', 'best-mattress-sickle-cell-disease', 'best-mattress-lupus-nephritis', 'best-mattress-chronic-pain', 'best-mattress-hypermobile-eds', 'best-mattress-pots', 'best-mattress-lyme-disease', 'best-mattress-mcas', 'best-mattress-als', 'best-mattress-huntingtons-disease', 'best-mattress-cerebral-palsy', 'best-mattress-muscular-dystrophy', 'best-mattress-sleep-apnea', 'best-mattress-narcolepsy', 'best-mattress-crohns-disease', 'best-mattress-osteoporosis', 'best-mattress-tourette-syndrome', 'best-mattress-pelvic-floor-dysfunction', 'best-mattress-dysautonomia', 'best-mattress-raynauds', 'best-mattress-celiac-disease', 'best-mattress-tinnitus', 'best-mattress-chronic-hives', 'best-mattress-hashimotos', 'best-mattress-sjogrens-syndrome', 'best-mattress-polymyalgia-rheumatica', 'best-mattress-bursitis', 'best-mattress-peripheral-artery-disease', 'best-mattress-complex-regional-pain', 'best-mattress-sacroiliac-joint-pain', 'best-mattress-costochondritis', 'best-mattress-interstitial-lung-disease', 'best-mattress-ehlers-danlos-classical', 'best-mattress-spinal-stenosis-cervical', 'best-mattress-marfan-syndrome', 'best-mattress-osteogenesis-imperfecta', 'best-mattress-scleroderma', 'best-mattress-thoracic-outlet-syndrome', 'best-mattress-avascular-necrosis-hip', 'best-mattress-temporomandibular-joint-disorder', 'best-mattress-shoulder-impingement', 'best-mattress-piriformis-syndrome', 'best-mattress-venous-insufficiency', 'best-mattress-post-laminectomy-syndrome', 'best-mattress-myasthenia-gravis', 'best-mattress-hemophilia', 'best-mattress-knee-pain', 'best-mattress-frozen-shoulder', 'best-mattress-carpal-tunnel-syndrome', 'best-mattress-polymyositis', 'best-mattress-spondylolisthesis', 'best-mattress-meralgia-paresthetica', 'best-mattress-achilles-tendinopathy', 'best-mattress-patellofemoral-syndrome', 'best-mattress-cubital-tunnel-syndrome', 'best-mattress-trigeminal-neuralgia', 'best-mattress-pudendal-neuralgia', 'best-mattress-lateral-epicondylitis', 'best-mattress-herniated-disc', 'best-mattress-back-pain', 'best-mattress-chronic-back-pain', 'best-mattress-side-sleeper-shoulder-pain', 'best-mattress-scoliosis', 'best-mattress-neck-pain', 'best-mattress-snoring', 'best-mattress-acid-reflux', 'best-mattress-insomnia', 'best-mattress-spinal-stenosis', 'best-mattress-degenerative-disc', 'best-mattress-stomach-sleepers-back-pain', 'best-mattress-stomach-sleepers-lower-back-pain', 'best-mattress-neuropathy', 'best-mattress-chronic-fatigue', 'best-mattress-lupus', 'best-mattress-multiple-sclerosis', 'best-mattress-ankylosing-spondylitis', 'best-mattress-ehlers-danlos', 'best-mattress-rheumatoid-arthritis', 'best-mattress-restless-legs', 'best-mattress-parkinsons'],
    'Life Stages': ['best-mattress-college-students', 'best-mattress-petite-sleeper', 'best-mattress-heavy-sleepers', 'best-mattress-studio-apartment', 'best-mattress-bunk-beds', 'best-mattress-college-dorm', 'best-mattress-rv', 'best-mattress-murphy-bed', 'best-mattress-daybed', 'best-mattress-trundle-bed', 'best-mattress-overheating-pregnancy', 'best-mattress-tall-person', 'best-mattress-teenager', 'best-mattress-teen-athlete', 'best-mattress-newlyweds', 'best-mattress-postpartum', 'best-mattress-knee-replacement', 'best-mattress-hip-replacement', 'best-mattress-overweight', 'best-mattress-kids', 'best-mattress-pregnancy', 'pregnancy-sleep-guide', 'kids-sleep-guide', 'kids-screen-time-sleep', 'teen-sleep-guide', 'aging-and-sleep', 'women-sleep-differences', 'menopause-sleep', 'sleep-menstrual-cycle', 'sleep-new-baby', 'couples-sleep-problems', 'best-pregnancy-pillows', 'best-pregnancy-pillow-back-pain', 'best-body-pillow', 'best-body-pillow-side-sleepers', 'best-white-noise-machine-baby', 'best-crib-mattress', 'best-toddler-pillow', 'best-baby-monitor-sleep', 'best-weighted-blanket-kids', 'best-kids-alarm-clock', 'best-mattress-seniors', 'best-mattress-for-seniors', 'best-mattress-topper-seniors', 'best-cooling-pillow-menopause'],
    'Timing & Jet Lag': ['reset-sleep-schedule', 'jet-lag-guide', 'sleep-travel-tips', 'sleep-business-travel', 'social-jetlag', 'daylight-saving-sleep', 'shift-work-shift', 'night-shift-optimization', 'polyphasic-sleep', 'polyphasic-sleep-schedules', 'sleep-consistency-importance', 'weekend-sleep-mistake', 'wrong-sleeping-in-weekends', 'shift-work-sleep', 'best-travel-pillow'],
    'Napping & Performance': ['power-nap-science', 'napping-science', 'sleep-inertia', 'microsleep-dangers', 'sleep-athletic-performance', 'sleep-exercise-timing', 'sleep-productivity', 'sleep-goal-setting', 'sleep-longevity', 'sleep-creativity', 'sleep-mental-performance'],
    'Guides & Plans': ['ultimate-sleep-guide', 'sleep-hygiene-checklist', 'wind-down-routine', 'morning-habits-sleep', 'sleep-journal-guide', '30-day-sleep-challenge', 'sleep-debt-accumulation', 'sleep-debt-recovery', 'summer-sleep-guide', 'winter-sleep-guide', 'sleep-exam-study', 'sleep-tracking-worth-it', 'sleep-tracking-data', 'hypnic-jerk-explained', 'lucid-dreaming-guide', 'sleep-myth-8-hours', 'sleep-myths-series', 'sleep-quality-vs-quantity', 'waking-at-3am', 'sleep-chronotypes', 'morning-lark-night-owl', 'sleep-cortisol-stress', 'sleep-and-hormones', 'sleep-loneliness', 'sleep-grief', 'sleep-adhd', 'sleep-and-weight-loss', 'does-sex-before-bed-help-sleep', 'sex-and-sleep-intimacy-quality', 'how-much-sleep-do-i-need', 'how-to-fall-asleep-fast', 'best-sleep-position', 'best-bath-soak-sleep', 'best-overnight-face-mask', 'sleep-myth-older-people-less-sleep'],
    'Mattresses & Bedding': ['best-mattresses-back-pain', 'best-mattresses-couples-2026', 'best-mattress-toppers', 'best-cooling-mattress-pads', 'best-cooling-pillows', 'best-cooling-pillow-hot-sleepers', 'best-cooling-sheets', 'best-linen-sheets', 'best-bamboo-sheets', 'best-mattress-stomach-sleepers', 'best-mattress-side-sleepers', 'best-mattress-back-sleepers', 'best-pillow-sleep-position', 'best-pillow-side-sleepers', 'best-pillow-neck-pain', 'best-grounding-sheets', 'best-memory-foam-pillow', 'mattress-buying-guide', 'memory-foam-vs-hybrid-mattress', 'latex-vs-memory-foam-mattress', 'best-mattresses-under-500', 'best-smart-mattresses', 'best-latex-mattress', 'best-natural-latex-mattress', 'best-duvet-insert', 'best-mattress-protector', 'best-cooling-mattress-topper', 'best-silk-pillowcase', 'best-adjustable-bed-frame', 'best-cooling-comforter', 'best-down-alternative-comforter', 'best-mattress-pad', 'best-pillow-back-sleepers', 'best-pillow-stomach-sleepers', 'best-hotel-pillow', 'best-buckwheat-pillow', 'best-contour-pillow', 'best-water-pillow', 'best-latex-pillow', 'best-organic-mattress', 'best-split-king-adjustable-base', 'best-mattress-topper-back-pain', 'best-mattress-night-sweats', 'best-mattress-menopause', 'best-mattress-firm-vs-medium', 'best-mattress-hot-sleepers', 'best-adjustable-pillow', 'best-foam-mattress-under-500', 'best-mattress-pressure-relief', 'best-mattress-heavy-people', 'best-pillow-shoulder-pain', 'best-bed-frame-heavy-person', 'best-mattress-topper-hot-sleepers', 'best-adjustable-base-bed-frame', 'best-mattress-adjustable-base', 'best-mattress-back-pain-side-sleeper', 'best-mattress-shoulder-pain', 'best-mattress-hip-pain', 'best-mattress-arthritis', 'best-heated-mattress-pad', 'best-cervical-pillow', 'best-mattress-topper-memory-foam', 'best-latex-mattress-topper', 'best-bamboo-pillow', 'best-waterproof-mattress-protector', 'best-feather-pillow', 'best-percale-sheets', 'best-tencel-sheets', 'best-sateen-sheets', 'best-flannel-sheets', 'best-cooling-mattress-pad', 'best-down-pillow', 'best-silk-sheets', 'best-linen-duvet-cover', 'best-bamboo-mattress-topper', 'best-cooling-sheets-for-night-sweats', 'best-organic-cotton-sheets', 'best-mattress-under-1000', 'best-duvet-insert-for-hot-sleepers', 'best-pillow-for-stomach-sleepers-neck-pain', 'best-murphy-bed-mattress', 'best-bed-in-a-box', 'best-hybrid-mattress', 'best-innerspring-mattress', 'best-mattress-topper-side-sleepers', 'best-weighted-blanket', 'best-white-noise-machine', 'best-memory-foam-mattress', 'best-cooling-pillow', 'best-king-size-mattress', 'best-firm-mattress', 'best-queen-size-mattress', 'best-pillow-top-mattress', 'best-plush-mattress', 'best-twin-xl-mattress', 'best-mattress-guest-room', 'best-twin-mattress', 'best-mattress-twin-xl', 'best-queen-mattress', 'best-king-mattress', 'best-california-king-mattress', 'best-full-size-mattress', 'best-mattress-heavy-side-sleepers', 'best-cooling-mattress-hot-sleepers', 'best-mattress-couples-different-preferences', 'best-adjustable-mattress', 'best-mattress-petite-side-sleepers', 'best-mattress-combination-sleepers', 'best-mattress-restless-sleeper', 'best-mattress-lower-back-pain-side-sleepers', 'best-mattress-under-200', 'best-mattress-under-300', 'best-mattress-under-500', 'best-mattress-topper', 'best-cooling-mattress', 'best-full-mattress', 'best-futon-mattress', 'best-mattress-couples', 'best-mattress-athlete', 'best-mattress-shift-workers', 'best-mattress-no-box-spring', 'best-mattress-platform-bed'],
    'Sleep Products': ['best-sleep-masks', 'best-sleep-mask', 'best-blackout-curtains', 'best-humidifiers-sleep', 'best-sleep-headphones', 'article-white-noise-machines', 'best-white-noise-machines-sleeping', 'best-light-therapy-lamps', 'best-blue-light-glasses', 'best-aromatherapy-sleep', 'best-cpap-alternatives', 'article-weighted-blanket', 'best-anti-snoring-devices', 'best-sleep-monitors', 'best-sleep-apps', 'best-sleep-tracking-rings', 'best-earplugs-sleeping', 'best-sunrise-alarm-clocks', 'best-weighted-blankets-adults', 'best-knee-pillow', 'best-bed-wedge-pillow', 'best-lumbar-support-pillow', 'best-alarm-clock-heavy-sleepers', 'best-electric-blanket', 'best-cpap-pillow', 'best-air-purifier-sleep', 'best-sleep-tracking-smartwatch', 'best-sleep-headphones-side-sleepers', 'best-weighted-blanket-anxiety', 'best-foot-warmer-bed', 'best-anti-snoring-mouthpiece', 'best-sleep-socks', 'best-neck-massager-sleep', 'best-sound-machine-tinnitus', 'best-diffuser-sleep', 'best-eye-pillow', 'best-heating-pad-sleep', 'best-bedroom-fan-sleep', 'best-massage-gun-sleep', 'best-under-mattress-sleep-tracker', 'best-sleep-shirt', 'best-cooling-towel-sleep', 'best-sleep-pillow-spray', 'best-acupressure-mat-sleep', 'best-red-light-therapy-sleep', 'best-sleep-balm', 'best-sleep-robe', 'best-bed-fan-sheet', 'best-mouth-tape-sleep', 'best-nasal-dilator-sleep', 'best-sleep-headband', 'best-foam-roller-sleep', 'best-weighted-eye-mask', 'best-grounding-mat-sleep', 'best-bamboo-pajamas-sleep', 'best-sleep-cooling-pad', 'best-oura-ring-alternatives', 'best-sleep-tracker-no-subscription', 'best-smart-alarm-clock', 'best-sleep-mask-travel', 'best-wedge-pillow-acid-reflux', 'best-earplugs-snoring-partner', 'best-cooling-weighted-blanket', 'best-smart-home-sleep-setup', 'best-white-noise-machine-adults', 'best-anti-snoring-chin-strap', 'best-sleep-mask-blackout', 'best-nasal-strips-sleep'],
    'Supplements': ['best-melatonin-supplements', 'best-sleep-supplements-guide', 'best-valerian-root-supplements', 'article-magnesium-sleep', 'sleep-medications-truth', 'best-ashwagandha-sleep', 'best-magnesium-glycinate', 'best-sleep-gummies', 'best-l-theanine-supplement', 'best-melatonin-for-kids', 'best-magnesium-spray-sleep', 'best-sleep-supplement-stack', 'best-sleep-tea', 'best-magnesium-lotion-sleep', 'best-melatonin-patch', 'best-glycine-supplement', 'best-tart-cherry-supplement', 'best-cbd-sleep', 'best-5-htp-supplement-sleep', 'best-passionflower-supplement-sleep', 'best-sleep-supplement-powder', 'best-lemon-balm-supplement-sleep', 'best-pregnenolone-sleep', 'best-magnesium-for-sleep-anxiety', 'best-sleep-supplement-anxiety', 'best-vitamin-d-sleep', 'best-omega-3-sleep', 'best-magnesium-threonate-sleep', 'best-sleep-aids-over-the-counter', 'best-melatonin-gummies-adults', 'best-sleep-supplement-melatonin', 'best-magnesium-glycinate-sleep', 'best-sleep-supplement-women', 'best-sleep-aid-for-anxiety', 'best-deep-sleep-supplement'],
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

CAT_ANCHOR = {
    'Insomnia & CBT-I': 'insomnia-cbti',
    'Sleep Science': 'sleep-science',
    'Caffeine & Nutrition': 'caffeine-nutrition',
    'Sleep Environment': 'sleep-environment',
    'Health Conditions': 'health-conditions',
    'Life Stages': 'life-stages',
    'Timing & Jet Lag': 'timing-jet-lag',
    'Napping & Performance': 'napping-performance',
    'Guides & Plans': 'guides-plans',
    'Mattresses & Bedding': 'mattresses-bedding',
    'Sleep Products': 'sleep-products',
    'Supplements': 'supplements',
}

# Build category sections HTML
category_html = ''
for cat_name, slugs in CATEGORIES.items():
    valid_slugs = [s for s in slugs if os.path.exists(os.path.join(POSTS_DIR, s + '.html'))]
    if not valid_slugs:
        continue
    anchor = CAT_ANCHOR.get(cat_name, cat_name.lower().replace(' ', '-').replace('&', '').replace('--', '-'))
    links = ''
    for slug in valid_slugs:
        title = title_map.get(slug, slug.replace('-', ' ').title())
        links += f'          <li><a href="{slug}.html">{title}</a></li>\n'
    category_html += f'''      <section class="cat-section" id="{anchor}">
        <h2>{cat_name} <span class="count">({len(valid_slugs)})</span></h2>
        <ul class="post-list">
{links}        </ul>
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
        links += f'          <li><a href="{slug}.html">{title}</a></li>\n'
    category_html += f'''      <section class="cat-section">
        <h2>Other Guides <span class="count">({len(uncategorized)})</span></h2>
        <ul class="post-list">
{links}        </ul>
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
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --bg: #0a1628; --card: #111e33; --gold: #c9a84c; --gold-dim: rgba(201,168,76,0.15);
      --text: #e8e0d0; --muted: #8899aa; --border: rgba(201,168,76,0.15);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: var(--bg); color: var(--text); font-family: 'Outfit', 'Georgia', sans-serif; line-height: 1.7; }}
    header {{ background: var(--card); border-bottom: 1px solid var(--border); padding: 1rem 3%; display: flex; align-items: center; justify-content: space-between; }}
    .logo {{ color: var(--gold); text-decoration: none; font-size: 1.3rem; font-weight: 700; }}
    .logo span {{ color: var(--text); }}
    main {{ max-width: 1400px; margin: 0 auto; padding: 2.5rem 3%; }}
    .page-hero {{ margin-bottom: 2rem; }}
    h1 {{ font-size: 2rem; color: var(--gold); margin-bottom: 0.4rem; }}
    .subtitle {{ color: var(--muted); font-size: 1rem; }}
    .search-wrap {{ margin: 1.5rem 0 2.5rem; position: relative; }}
    .search-wrap input {{
      width: 100%; padding: 0.85rem 1.2rem 0.85rem 3rem;
      background: var(--card); border: 1px solid var(--border);
      border-radius: 8px; color: var(--text); font-family: inherit; font-size: 1rem;
      outline: none; transition: border-color 0.2s;
    }}
    .search-wrap input:focus {{ border-color: var(--gold); }}
    .search-wrap input::placeholder {{ color: var(--muted); }}
    .search-wrap svg {{ position: absolute; left: 1rem; top: 50%; transform: translateY(-50%); opacity: 0.5; pointer-events: none; }}
    .no-results {{ display: none; }}
    .no-results-panel {{
      background: var(--card); border: 1px solid var(--border); border-radius: 12px;
      padding: 1.8rem 2rem; margin: 0.5rem 0 2rem;
    }}
    .no-results-panel h3 {{ color: var(--gold); font-size: 1rem; margin-bottom: 0.5rem; }}
    .no-results-panel p {{ color: var(--muted); font-size: 0.9rem; margin-bottom: 1.2rem; }}
    .contact-options {{ display: flex; flex-wrap: wrap; gap: 0.75rem; margin-bottom: 1.2rem; }}
    .contact-btn {{
      display: inline-flex; align-items: center; gap: 0.4rem;
      padding: 0.5rem 1.1rem; border-radius: 8px; font-size: 0.88rem;
      font-family: inherit; text-decoration: none; font-weight: 600;
      border: 1px solid var(--border); color: var(--text); background: rgba(255,255,255,0.04);
      transition: border-color 0.2s, color 0.2s;
    }}
    .contact-btn:hover {{ border-color: var(--gold); color: var(--gold); }}
    .contact-btn.gold {{ background: var(--gold); color: #07101f; border-color: var(--gold); }}
    .contact-btn.gold:hover {{ background: #e8c96a; }}
    .faq-anchor-link {{ color: var(--gold); font-size: 0.88rem; }}
    .cat-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 2rem; }}
    .cat-section {{ background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 1.4rem 1.6rem; }}
    .cat-section h2 {{ font-size: 1rem; font-weight: 600; color: var(--gold); border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; margin-bottom: 0.9rem; }}
    .count {{ color: var(--muted); font-size: 0.8rem; font-weight: 400; }}
    .post-list {{ list-style: none; }}
    .post-list li {{ margin-bottom: 0.35rem; }}
    .post-list a {{ color: var(--text); text-decoration: none; font-size: 0.88rem; line-height: 1.4; display: block; }}
    .post-list a:hover {{ color: var(--gold); }}
    .hidden-cat {{ display: none; }}
    footer {{ text-align: center; padding: 2rem; color: var(--muted); font-size: 0.85rem; border-top: 1px solid var(--border); margin-top: 2rem; }}
    footer a {{ color: var(--gold); }}
    @media (max-width: 900px) {{ .cat-grid {{ grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.2rem; }} }}
    @media (max-width: 500px) {{ .cat-grid {{ grid-template-columns: 1fr; }} h1 {{ font-size: 1.5rem; }} }}
  </style>
</head>
<body>
  <header>
    <a class="logo" href="../">SleepWise<span>Reviews</span></a>
    <a href="../" style="color:var(--muted);font-size:0.9rem;text-decoration:none;">← Home</a>
  </header>
  <main>
    <div class="page-hero">
      <h1>All Sleep Guides</h1>
      <p class="subtitle">{total_count} science-backed articles covering mattresses, insomnia, supplements, sleep science, and more.</p>
    </div>
    <div class="search-wrap">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
      <input type="text" id="search" placeholder="Search {total_count} articles — try 'mattress', 'melatonin', 'back pain'..." autocomplete="off" />
    </div>
    <div class="no-results" id="no-results">
      <div class="no-results-panel">
        <h3>No articles match your search</h3>
        <p>Try a different keyword, or let us help you find what you need:</p>
        <div class="contact-options">
          <a href="#faq-section" class="contact-btn" onclick="document.getElementById('faq-section').scrollIntoView({{behavior:'smooth'}});return false;">&#x2753; Browse our FAQ</a>
          <a href="mailto:hello@sleepwisereviews.com" class="contact-btn">&#x2709; Email Us</a>
          <a href="https://www.instagram.com/sleepwisereviews/" class="contact-btn" rel="noopener noreferrer" target="_blank">&#x1F4F7; Instagram DM</a>
          <a href="https://www.facebook.com/sleepwisereviews/" class="contact-btn" rel="noopener noreferrer" target="_blank">&#x1F4AC; Facebook</a>
          <a href="https://sleepwisereviews.com/subscribe.html" class="contact-btn gold">&#x1F4E7; Weekly Sleep Tips</a>
        </div>
        <p style="font-size:0.82rem;">We publish new guides every week. <a href="https://sleepwisereviews.com/subscribe.html" class="faq-anchor-link">Subscribe</a> and we'll send the right guide to your inbox.</p>
      </div>
    </div>
    <div class="cat-grid" id="cat-grid">
{category_html}    </div>
  </main>
  <section id="faq-section" style="max-width:1400px;margin:3rem auto 0;padding:0 3% 2rem;">
    <h2 style="color:var(--gold);font-size:1.3rem;margin-bottom:1.5rem;padding-top:1rem;border-top:1px solid var(--border);">Common Questions</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:1.2rem;">
      <div style="background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1.2rem 1.4rem;">
        <h3 style="font-size:0.95rem;color:#f0e6c8;margin-bottom:0.4rem;">What is the best mattress for back pain?</h3>
        <p style="font-size:0.85rem;color:var(--muted);margin-bottom:0.6rem;">Medium-Firm (5.5-7/10) hybrids with zoned support perform best for most back pain types.</p>
        <a href="best-mattresses-back-pain.html" style="color:var(--gold);font-size:0.82rem;">Read our back pain mattress guide &#x2192;</a>
      </div>
      <div style="background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1.2rem 1.4rem;">
        <h3 style="font-size:0.95rem;color:#f0e6c8;margin-bottom:0.4rem;">How do I fall asleep faster?</h3>
        <p style="font-size:0.85rem;color:var(--muted);margin-bottom:0.6rem;">CBT-I techniques, consistent sleep schedules, and bedroom temperature control are the most evidence-backed approaches.</p>
        <a href="how-to-fall-asleep-fast.html" style="color:var(--gold);font-size:0.82rem;">Read our fast sleep guide &#x2192;</a>
      </div>
      <div style="background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1.2rem 1.4rem;">
        <h3 style="font-size:0.95rem;color:#f0e6c8;margin-bottom:0.4rem;">Which supplements actually help with sleep?</h3>
        <p style="font-size:0.85rem;color:var(--muted);margin-bottom:0.6rem;">Magnesium glycinate, low-dose melatonin (0.3mg), and L-theanine have the strongest clinical evidence.</p>
        <a href="best-sleep-supplements-guide.html" style="color:var(--gold);font-size:0.82rem;">Read our supplements guide &#x2192;</a>
      </div>
      <div style="background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1.2rem 1.4rem;">
        <h3 style="font-size:0.95rem;color:#f0e6c8;margin-bottom:0.4rem;">What pillow is best for side sleepers?</h3>
        <p style="font-size:0.85rem;color:var(--muted);margin-bottom:0.6rem;">Side sleepers need a higher loft (4-6 inches) to fill the gap between head and shoulder for neutral neck alignment.</p>
        <a href="best-pillow-side-sleepers.html" style="color:var(--gold);font-size:0.82rem;">Read our side sleeper pillow guide &#x2192;</a>
      </div>
      <div style="background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1.2rem 1.4rem;">
        <h3 style="font-size:0.95rem;color:#f0e6c8;margin-bottom:0.4rem;">How much sleep do adults actually need?</h3>
        <p style="font-size:0.85rem;color:var(--muted);margin-bottom:0.6rem;">Most adults need 7-9 hours. Chronotype, age, and activity level all influence the exact amount for each individual.</p>
        <a href="how-much-sleep-do-i-need.html" style="color:var(--gold);font-size:0.82rem;">Read the full sleep needs guide &#x2192;</a>
      </div>
      <div style="background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1.2rem 1.4rem;">
        <h3 style="font-size:0.95rem;color:#f0e6c8;margin-bottom:0.4rem;">Still can't find what you need?</h3>
        <p style="font-size:0.85rem;color:var(--muted);margin-bottom:0.6rem;">Send us a message and we'll point you to the right guide — or write a new one.</p>
        <a href="mailto:hello@sleepwisereviews.com" style="color:var(--gold);font-size:0.82rem;">Email us &#x2192;</a>
        &nbsp;&nbsp;
        <a href="https://www.instagram.com/sleepwisereviews/" style="color:var(--gold);font-size:0.82rem;" rel="noopener noreferrer" target="_blank">Instagram DM &#x2192;</a>
      </div>
    </div>
  </section>
  <footer>
    <p>&copy; 2025-2026 <a href="../">SleepWise Reviews</a> · Evidence-based sleep guidance</p>
  </footer>
  <script>
    const input = document.getElementById('search');
    const noResults = document.getElementById('no-results');
    const catGrid = document.getElementById('cat-grid');
    input.addEventListener('input', function() {{
      const q = this.value.toLowerCase().trim();
      let anyVisible = false;
      document.querySelectorAll('.cat-section').forEach(sec => {{
        let secVisible = false;
        sec.querySelectorAll('.post-list li').forEach(li => {{
          const match = !q || li.textContent.toLowerCase().includes(q);
          li.style.display = match ? '' : 'none';
          if (match) secVisible = true;
        }});
        sec.style.display = secVisible ? '' : 'none';
        if (secVisible) anyVisible = true;
      }});
      noResults.style.display = (!anyVisible && q) ? 'block' : 'none';
      catGrid.style.display = (!anyVisible && q) ? 'none' : '';
    }});
  </script>
</body>
</html>
'''

output_path = os.path.join(POSTS_DIR, 'index.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_out)

print(f'Generated posts/index.html ({total_count} posts, {len(CATEGORIES)} categories)')
if uncategorized:
    print(f'Uncategorized: {len(uncategorized)} posts → {sorted(uncategorized)}')
