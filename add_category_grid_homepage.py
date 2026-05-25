import os, subprocess

POSTS_DIR = 'posts'

CATEGORY_META = {
    'Mattresses & Bedding': {
        'icon': '&#x1F6CF;',
        'desc': 'Mattresses, pillows, toppers, sheets, and bedding — ranked by sleep position and budget.',
        'anchor': 'mattresses-bedding',
    },
    'Sleep Products': {
        'icon': '&#x1F3A7;',
        'desc': 'Sleep masks, white noise machines, trackers, blackout curtains, and gadgets that actually work.',
        'anchor': 'sleep-products',
    },
    'Supplements': {
        'icon': '&#x1F48A;',
        'desc': 'Melatonin, magnesium, valerian, and natural sleep aids ranked by clinical evidence strength.',
        'anchor': 'supplements',
    },
    'Guides & Plans': {
        'icon': '&#x1F4CB;',
        'desc': 'Step-by-step sleep improvement guides, wind-down routines, and 30-day sleep challenges.',
        'anchor': 'guides-plans',
    },
    'Health Conditions': {
        'icon': '&#x1FA7A;',
        'desc': 'Sleep with back pain, apnea, fibromyalgia, shoulder pain, sciatica, and chronic conditions.',
        'anchor': 'health-conditions',
    },
    'Life Stages': {
        'icon': '&#x1F476;',
        'desc': 'Pregnancy, baby years, teens, menopause, aging, and couples sleep — all stages covered.',
        'anchor': 'life-stages',
    },
    'Caffeine & Nutrition': {
        'icon': '&#x2615;',
        'desc': 'How caffeine timing, alcohol, magnesium, blue light, and food choices affect your sleep.',
        'anchor': 'caffeine-nutrition',
    },
    'Timing & Jet Lag': {
        'icon': '&#x2708;',
        'desc': 'Sleep schedule resets, jet lag recovery, shift work optimization, and circadian timing.',
        'anchor': 'timing-jet-lag',
    },
    'Sleep Science': {
        'icon': '&#x1F9E0;',
        'desc': 'Deep dives into sleep stages, REM, circadian rhythms, sleep genetics, and brain science.',
        'anchor': 'sleep-science',
    },
    'Napping & Performance': {
        'icon': '&#x26A1;',
        'desc': 'Power naps, athletic recovery, cognitive performance, creativity, and productivity science.',
        'anchor': 'napping-performance',
    },
    'Sleep Environment': {
        'icon': '&#x1F319;',
        'desc': 'Bedroom temperature, light control, tech detox, plants, and environment optimization.',
        'anchor': 'sleep-environment',
    },
    'Insomnia & CBT-I': {
        'icon': '&#x1F634;',
        'desc': 'Evidence-based CBT-I techniques, stimulus control, sleep restriction, and insomnia recovery.',
        'anchor': 'insomnia-cbti',
    },
}

CATEGORIES = {
    'Insomnia & CBT-I': ['insomnia-types', 'cbt-i-guide', 'sleep-anxiety-techniques', 'sleep-when-anxious', 'sleep-disorders-overview', 'sleep-paralysis-explained', 'sleep-ptsd', 'rem-behavior-disorder', 'rem-rebound-explained'],
    'Sleep Science': ['sleep-stages-explained', 'circadian-rhythm-basics', 'chronobiology-basics', 'adenosine-sleep-drive', 'sleep-genetics', 'brain-during-sleep', 'dreams-science', 'deep-sleep-benefits', 'rem-sleep-benefits', 'light-sleep-importance', 'sleep-memory-learning', 'sleep-immune-system'],
    'Caffeine & Nutrition': ['caffeine-half-life-sleep', 'blue-light-melatonin', 'melatonin-guide', 'alcohol-sleep-quality', 'sleep-food-connection', 'magnesium-deficiency-sleep', 'magnesium-types-sleep', 'natural-sleep-aids', 'sleep-fasting', 'sleep-hydration', 'sleep-hydration-guide', 'sleep-and-alcohol-free', 'gut-microbiome-sleep', 'sleep-and-thyroid', 'sleep-and-gut-health'],
    'Sleep Environment': ['bedroom-temperature-sleep', 'sleep-environment-optimization', 'sleep-sanctuary-guide', 'bedroom-plants-sleep', 'bedroom-tech-sleep', 'sleep-screen-detox', 'sleep-temperature-regulation', 'sleep-light-therapy', 'altitude-sleep', 'sleep-camping', 'best-blackout-curtain-liner'],
    'Health Conditions': ['sleep-apnea-warning-signs', 'sleep-apnea-diagnosis', 'home-sleep-apnea-test', 'snoring-causes-fixes', 'restless-legs-syndrome', 'sleep-chronic-pain', 'sleep-fibromyalgia', 'sleep-and-pain', 'sleep-depression', 'sleep-mental-health', 'sleep-heart-health', 'sleep-and-diabetes', 'sleep-and-alzheimers', 'sleep-autism-spectrum', 'bad-mattress-health-effects', 'sleep-after-surgery', 'sleep-skin-health', 'sleep-after-covid', 'best-mouthguard-teeth-grinding', 'best-cpap-mask-side-sleepers', 'best-pillow-for-cervical-spondylosis', 'best-mattress-fibromyalgia', 'best-anti-snoring-pillow', 'best-cpap-humidifier', 'best-pillow-for-side-sleepers-shoulder-pain', 'best-cpap-machine-travel', 'best-mattress-sciatica', 'best-mattress-back-pain', 'best-mattress-side-sleeper-shoulder-pain', 'best-mattress-stomach-sleepers-back-pain'],
    'Life Stages': ['pregnancy-sleep-guide', 'kids-sleep-guide', 'kids-screen-time-sleep', 'teen-sleep-guide', 'aging-and-sleep', 'women-sleep-differences', 'menopause-sleep', 'sleep-menstrual-cycle', 'sleep-new-baby', 'couples-sleep-problems', 'best-pregnancy-pillows', 'best-pregnancy-pillow-back-pain', 'best-body-pillow', 'best-body-pillow-side-sleepers', 'best-white-noise-machine-baby', 'best-crib-mattress', 'best-toddler-pillow', 'best-baby-monitor-sleep', 'best-weighted-blanket-kids', 'best-kids-alarm-clock', 'best-mattress-for-seniors', 'best-mattress-topper-seniors', 'best-cooling-pillow-menopause'],
    'Timing & Jet Lag': ['reset-sleep-schedule', 'jet-lag-guide', 'sleep-travel-tips', 'sleep-business-travel', 'social-jetlag', 'daylight-saving-sleep', 'shift-work-shift', 'night-shift-optimization', 'polyphasic-sleep', 'polyphasic-sleep-schedules', 'sleep-consistency-importance', 'weekend-sleep-mistake', 'wrong-sleeping-in-weekends', 'shift-work-sleep', 'best-travel-pillow'],
    'Napping & Performance': ['power-nap-science', 'napping-science', 'sleep-inertia', 'microsleep-dangers', 'sleep-athletic-performance', 'sleep-exercise-timing', 'sleep-productivity', 'sleep-goal-setting', 'sleep-longevity', 'sleep-creativity', 'sleep-mental-performance'],
    'Guides & Plans': ['ultimate-sleep-guide', 'sleep-hygiene-checklist', 'wind-down-routine', 'morning-habits-sleep', 'sleep-journal-guide', '30-day-sleep-challenge', 'sleep-debt-accumulation', 'sleep-debt-recovery', 'summer-sleep-guide', 'winter-sleep-guide', 'sleep-exam-study', 'sleep-tracking-worth-it', 'sleep-tracking-data', 'hypnic-jerk-explained', 'lucid-dreaming-guide', 'sleep-myth-8-hours', 'sleep-myths-series', 'sleep-quality-vs-quantity', 'waking-at-3am', 'sleep-chronotypes', 'morning-lark-night-owl', 'sleep-cortisol-stress', 'sleep-and-hormones', 'sleep-loneliness', 'sleep-grief', 'sleep-adhd', 'sleep-and-weight-loss', 'does-sex-before-bed-help-sleep', 'sex-and-sleep-intimacy-quality', 'how-much-sleep-do-i-need', 'how-to-fall-asleep-fast', 'best-sleep-position', 'best-bath-soak-sleep', 'best-overnight-face-mask'],
    'Mattresses & Bedding': ['best-mattresses-back-pain', 'best-mattresses-couples-2026', 'best-mattress-toppers', 'best-cooling-mattress-pads', 'best-cooling-pillows', 'best-cooling-pillow-hot-sleepers', 'best-cooling-sheets', 'best-linen-sheets', 'best-bamboo-sheets', 'best-mattress-stomach-sleepers', 'best-mattress-side-sleepers', 'best-mattress-back-sleepers', 'best-pillow-sleep-position', 'best-pillow-side-sleepers', 'best-pillow-neck-pain', 'best-grounding-sheets', 'best-memory-foam-pillow', 'mattress-buying-guide', 'memory-foam-vs-hybrid-mattress', 'latex-vs-memory-foam-mattress', 'best-mattresses-under-500', 'best-smart-mattresses', 'best-latex-mattress', 'best-duvet-insert', 'best-mattress-protector', 'best-cooling-mattress-topper', 'best-silk-pillowcase', 'best-adjustable-bed-frame', 'best-cooling-comforter', 'best-down-alternative-comforter', 'best-mattress-pad', 'best-pillow-back-sleepers', 'best-pillow-stomach-sleepers', 'best-hotel-pillow', 'best-buckwheat-pillow', 'best-contour-pillow', 'best-water-pillow', 'best-latex-pillow', 'best-organic-mattress', 'best-split-king-adjustable-base', 'best-mattress-topper-back-pain', 'best-mattress-firm-vs-medium', 'best-mattress-hot-sleepers', 'best-adjustable-pillow', 'best-foam-mattress-under-500', 'best-mattress-pressure-relief', 'best-mattress-heavy-people', 'best-pillow-shoulder-pain', 'best-bed-frame-heavy-person', 'best-mattress-topper-hot-sleepers', 'best-adjustable-base-bed-frame', 'best-mattress-back-pain-side-sleeper', 'best-mattress-arthritis', 'best-heated-mattress-pad', 'best-cervical-pillow', 'best-mattress-topper-memory-foam', 'best-latex-mattress-topper', 'best-bamboo-pillow', 'best-waterproof-mattress-protector', 'best-feather-pillow', 'best-percale-sheets', 'best-tencel-sheets', 'best-sateen-sheets', 'best-flannel-sheets', 'best-cooling-mattress-pad', 'best-down-pillow', 'best-silk-sheets', 'best-linen-duvet-cover', 'best-bamboo-mattress-topper', 'best-cooling-sheets-for-night-sweats', 'best-organic-cotton-sheets', 'best-mattress-under-1000', 'best-duvet-insert-for-hot-sleepers', 'best-pillow-for-stomach-sleepers-neck-pain', 'best-murphy-bed-mattress', 'best-bed-in-a-box', 'best-hybrid-mattress', 'best-innerspring-mattress', 'best-mattress-topper-side-sleepers', 'best-weighted-blanket', 'best-white-noise-machine', 'best-memory-foam-mattress', 'best-cooling-pillow', 'best-king-size-mattress', 'best-firm-mattress', 'best-queen-size-mattress', 'best-pillow-top-mattress', 'best-plush-mattress', 'best-twin-xl-mattress', 'best-full-size-mattress'],
    'Sleep Products': ['best-sleep-masks', 'best-sleep-mask', 'best-blackout-curtains', 'best-humidifiers-sleep', 'best-sleep-headphones', 'article-white-noise-machines', 'best-white-noise-machines-sleeping', 'best-light-therapy-lamps', 'best-blue-light-glasses', 'best-aromatherapy-sleep', 'best-cpap-alternatives', 'article-weighted-blanket', 'best-anti-snoring-devices', 'best-sleep-monitors', 'best-sleep-apps', 'best-sleep-tracking-rings', 'best-earplugs-sleeping', 'best-sunrise-alarm-clocks', 'best-weighted-blankets-adults', 'best-knee-pillow', 'best-bed-wedge-pillow', 'best-lumbar-support-pillow', 'best-alarm-clock-heavy-sleepers', 'best-electric-blanket', 'best-cpap-pillow', 'best-air-purifier-sleep', 'best-sleep-tracking-smartwatch', 'best-sleep-headphones-side-sleepers', 'best-weighted-blanket-anxiety', 'best-foot-warmer-bed', 'best-anti-snoring-mouthpiece', 'best-sleep-socks', 'best-neck-massager-sleep', 'best-sound-machine-tinnitus', 'best-diffuser-sleep', 'best-eye-pillow', 'best-heating-pad-sleep', 'best-bedroom-fan-sleep', 'best-massage-gun-sleep', 'best-under-mattress-sleep-tracker', 'best-sleep-shirt', 'best-cooling-towel-sleep', 'best-sleep-pillow-spray', 'best-acupressure-mat-sleep', 'best-red-light-therapy-sleep', 'best-sleep-balm', 'best-sleep-robe', 'best-bed-fan-sheet', 'best-mouth-tape-sleep', 'best-nasal-dilator-sleep', 'best-sleep-headband', 'best-foam-roller-sleep', 'best-weighted-eye-mask', 'best-grounding-mat-sleep', 'best-bamboo-pajamas-sleep', 'best-sleep-cooling-pad', 'best-oura-ring-alternatives', 'best-sleep-tracker-no-subscription', 'best-smart-alarm-clock', 'best-sleep-mask-travel', 'best-wedge-pillow-acid-reflux', 'best-earplugs-snoring-partner', 'best-cooling-weighted-blanket', 'best-smart-home-sleep-setup', 'best-white-noise-machine-adults', 'best-anti-snoring-chin-strap', 'best-sleep-mask-blackout', 'best-nasal-strips-sleep'],
    'Supplements': ['best-melatonin-supplements', 'best-sleep-supplements-guide', 'best-valerian-root-supplements', 'article-magnesium-sleep', 'sleep-medications-truth', 'best-ashwagandha-sleep', 'best-magnesium-glycinate', 'best-sleep-gummies', 'best-l-theanine-supplement', 'best-melatonin-for-kids', 'best-magnesium-spray-sleep', 'best-sleep-supplement-stack', 'best-sleep-tea', 'best-magnesium-lotion-sleep', 'best-melatonin-patch', 'best-glycine-supplement', 'best-tart-cherry-supplement', 'best-cbd-sleep', 'best-5-htp-supplement-sleep', 'best-passionflower-supplement-sleep', 'best-sleep-supplement-powder', 'best-lemon-balm-supplement-sleep', 'best-pregnenolone-sleep', 'best-magnesium-for-sleep-anxiety', 'best-sleep-supplement-anxiety', 'best-vitamin-d-sleep', 'best-omega-3-sleep', 'best-magnesium-threonate-sleep', 'best-sleep-aids-over-the-counter', 'best-melatonin-gummies-adults', 'best-sleep-supplement-melatonin', 'best-magnesium-glycinate-sleep', 'best-sleep-supplement-women', 'best-sleep-aid-for-anxiety', 'best-deep-sleep-supplement'],
}

# Compute article counts (only count posts that actually exist)
counts = {}
for cat_name, slugs in CATEGORIES.items():
    valid = [s for s in slugs if os.path.exists(os.path.join(POSTS_DIR, s + '.html'))]
    counts[cat_name] = len(valid)

total = sum(counts.values())

# CSS to inject
css_block = '''
    /* CATEGORY OVERVIEW GRID */
    .cat-overview-section { padding: 2.5rem 0 1rem; }
    .cat-overview-section .section-inner { max-width: 1400px; margin: 0 auto; padding: 0 1.5rem; }
    .cat-overview-label { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: var(--gold); margin-bottom: 0.5rem; }
    .cat-overview-title { font-size: 1.5rem; font-weight: 800; color: #f0e6c8; margin-bottom: 0.4rem; }
    .cat-overview-sub { font-size: 0.9rem; color: var(--muted); margin-bottom: 1.8rem; }
    .cat-overview-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
      gap: 1rem;
    }
    .cat-card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.2rem 1.4rem;
      text-decoration: none;
      color: var(--text);
      display: flex;
      flex-direction: column;
      transition: border-color 0.2s, transform 0.15s;
    }
    .cat-card:hover {
      border-color: rgba(201,168,76,0.45);
      transform: translateY(-2px);
    }
    .cat-card .cat-icon { font-size: 1.6rem; margin-bottom: 0.6rem; line-height: 1; }
    .cat-card .cat-name { font-size: 0.95rem; font-weight: 700; color: #f0e6c8; margin-bottom: 0.25rem; }
    .cat-card .cat-count { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: var(--gold); margin-bottom: 0.55rem; }
    .cat-card .cat-desc { font-size: 0.8rem; color: var(--muted); line-height: 1.5; flex-grow: 1; margin-bottom: 0.7rem; }
    .cat-card .cat-arrow { font-size: 0.8rem; color: var(--gold); font-weight: 600; margin-top: auto; }
    @media (max-width: 700px) { .cat-overview-grid { grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 0.75rem; } }
    @media (max-width: 420px) { .cat-overview-grid { grid-template-columns: 1fr 1fr; } }
'''

# Build category cards HTML
cards_html = ''
for cat_name, meta in CATEGORY_META.items():
    count = counts.get(cat_name, 0)
    if count == 0:
        continue
    cards_html += (
        f'          <a class="cat-card" href="posts/index.html#{meta["anchor"]}">\n'
        f'            <div class="cat-icon">{meta["icon"]}</div>\n'
        f'            <div class="cat-name">{cat_name}</div>\n'
        f'            <div class="cat-count">{count} Articles</div>\n'
        f'            <div class="cat-desc">{meta["desc"]}</div>\n'
        f'            <div class="cat-arrow">Browse all &#x2192;</div>\n'
        f'          </a>\n'
    )

section_html = (
    '      <!-- CATEGORY OVERVIEW -->\n'
    '      <section class="cat-overview-section">\n'
    '        <div class="cat-overview-section section-inner">\n'
    '          <div class="cat-overview-label">Complete Library</div>\n'
    f'          <h2 class="cat-overview-title">All Sleep Guides &amp; Articles</h2>\n'
    f'          <p class="cat-overview-sub">{total} articles across {len(CATEGORY_META)} categories &#x2014; independent sleep research and testing.</p>\n'
    '          <div class="cat-overview-grid">\n'
    + cards_html +
    '          </div>\n'
    '        </div>\n'
    '      </section>\n'
    '      <!-- END CATEGORY OVERVIEW -->\n'
)

# Inject CSS
html = open('index.html', encoding='utf-8').read()
original = html

css_anchor = '  </style>\n  <meta property="og:title"'
if css_anchor not in html:
    css_anchor = '  </style>\n</head>'
if css_anchor in html:
    html = html.replace(css_anchor, css_block + css_anchor, 1)
    print('CSS injected')
else:
    print('ERROR: CSS anchor not found')

# Inject section before ALL REVIEWS GRID
inject_marker = '      <!-- ALL REVIEWS GRID -->'
if inject_marker in html:
    html = html.replace(inject_marker, section_html + inject_marker, 1)
    print('Category grid section injected')
else:
    print('ERROR: ALL REVIEWS GRID marker not found')

if html != original:
    open('index.html', 'w', encoding='utf-8').write(html)
    print('Saved index.html')

# Regenerate posts/index.html (to pick up search updates)
import subprocess
result = subprocess.run(['python', 'generate_posts_index.py'], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print('STDERR:', result.stderr[:300])

# Git
subprocess.run(['git', 'add', 'index.html', 'posts/index.html', 'generate_posts_index.py'], check=True)
result = subprocess.run(['git', 'commit', '-m',
    'feat(ui): category overview grid on homepage + smart search fallback with FAQ and contact panel'
], capture_output=True, text=True)
print(result.stdout)
result = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print(result.stderr)
