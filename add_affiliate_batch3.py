from pathlib import Path
import re as re_mod

adds = {
    'aging-and-sleep.html': [
        ('low+dose+melatonin+0.5mg+sleep+older+adults+aging', 'Low-Dose Melatonin for Age-Related Sleep Changes', 'Melatonin production drops by 50-75% between ages 20 and 70. Supplementing with 0.3-0.5mg at bedtime replaces what the pineal gland no longer produces. Low doses avoid the grogginess that comes with pharmacological 5-10mg products.'),
        ('weighted+blanket+adults+15+pound+sleep+anxiety+calming', 'Weighted Blanket for Deeper Rest', 'Deep pressure stimulation from a weighted blanket activates the parasympathetic nervous system, reducing the nighttime cortisol elevation that becomes more common with age. The standard recommendation is 10% of body weight.'),
    ],
    'brain-during-sleep.html': [
        ('sleep+tracker+wearable+ring+sleep+stages+REM+deep', 'Sleep Tracker for Observing Your Sleep Architecture', 'A sleep tracker translates the science of sleep stages — slow-wave, REM, light — into your own nightly data. Seeing your actual deep sleep percentage is far more motivating than reading about what happens during sleep in general.'),
        ('magnesium+glycinate+deep+sleep+slow+wave+supplement', 'Magnesium Glycinate for Slow-Wave Sleep Support', 'Magnesium activates GABA receptors that promote slow-wave sleep — the consolidation phase where memory and tissue repair occur. Glycinate form avoids the laxative effect of magnesium oxide. 200-400mg taken 30-60 min before bed.'),
    ],
    'dreams-science.html': [
        ('sleep+journal+dream+diary+notebook+REM+tracking', 'Dream Journal for REM Sleep Awareness', 'Keeping a dream diary increases recall of REM-phase experiences and sharpens awareness of sleep quality over time. Write within 60 seconds of waking — the hippocampal memory trace degrades rapidly once the brain shifts out of the half-awake state.'),
        ('sleep+tracker+REM+sleep+stages+wrist+ring+accuracy', 'Sleep Tracker for Monitoring REM Duration', 'Modern wrist and ring trackers estimate REM duration from heart rate variability patterns with 70-80% accuracy compared to lab polysomnography. Enough precision to see whether alcohol, late eating, or stress is cutting your dreaming short.'),
    ],
    'kids-screen-time-sleep.html': [
        ('blue+light+blocking+glasses+kids+children+screen+amber+lens', 'Blue-Light Blocking Glasses for Children', 'Amber-lens glasses cut the 480nm wavelength that suppresses melatonin production. For children, whose crystalline lens lets through more short-wavelength light than adults, wearing these 1-2 hours before bed can advance sleep onset by 20-30 minutes.'),
        ('sunrise+alarm+clock+kids+wake+up+light+gradual+morning', 'Sunrise Alarm Clock for Children\'s Morning Routines', 'A gradual sunrise light in the bedroom trains children\'s cortisol to rise with a predictable light signal — the same mechanism as dawn. Paired with a consistent sleep schedule, this reduces the morning battle for school-age children.'),
    ],
    'kids-sleep-guide.html': [
        ('white+noise+machine+baby+kids+bedroom+sleep+womb+sound', 'White Noise Machine for Children\'s Bedrooms', 'White noise at 50-60dB masks household sounds that wake children at the transition between sleep cycles — the most common cause of multiple night wakings. Fan-based machines produce true broadband white noise; digital machines offer pitch variety.'),
        ('blackout+curtains+kids+nursery+bedroom+sleep+light+blocking', 'Blackout Curtains for Children\'s Rooms', 'Young children have a stronger melatonin response to light than adults. Total blackout curtains are the highest-ROI sleep intervention for early-morning waking (the 5am "it\'s bright, I\'m awake" pattern) and for naps during daylight hours.'),
    ],
    'lucid-dreaming-guide.html': [
        ('dream+journal+notebook+lucid+dreaming+reality+check+log', 'Dream Journal for Lucid Dreaming Practice', 'A physical dream journal is the foundational practice for lucid dreaming. Recording dreams within 60 seconds of waking builds the recall muscle needed to recognize dream signatures — patterns that, once noticed in waking life, eventually appear as triggers during the dream.'),
        ('sleep+mask+blackout+lucid+dreaming+REM+light+dark', 'Total Blackout Sleep Mask for REM Enhancement', 'A contoured blackout mask eliminates light intrusion that cuts REM sessions short. Deeper, longer REM periods give more time in the dream state — the window for lucidity practice. Look for contoured designs that allow natural eye movement during REM.'),
    ],
    'sleep-adhd.html': [
        ('weighted+blanket+ADHD+adults+sensory+calming+deep+pressure', 'Weighted Blanket for ADHD Sleep Onset', 'Deep pressure from a weighted blanket reduces the physiological hyperarousal that delays sleep onset in ADHD. The proprioceptive input signals safety to the nervous system. Most effective weight is 10% of body weight plus 1-2 pounds.'),
        ('white+noise+machine+ADHD+sleep+sound+masking+focus', 'White Noise Machine for ADHD Sleep Environment', 'The ADHD brain responds to novelty and is easily pulled out of sleep by unexpected sounds. A consistent white noise background masks the environmental irregularities — a car, a voice, a notification — that would otherwise trigger arousal.'),
    ],
    'sleep-fibromyalgia.html': [
        ('memory+foam+mattress+topper+fibromyalgia+pressure+relief+3+inch', 'Memory Foam Topper for Fibromyalgia Pressure Relief', 'Fibromyalgia amplifies pressure sensitivity at contact points. A 2-3 inch memory foam or latex topper redistributes pressure across a larger surface area, reducing the localized pain that fragments sleep. Often a higher ROI than a full mattress replacement.'),
        ('body+pillow+full+length+fibromyalgia+side+sleeping+support', 'Full Body Pillow for Fibromyalgia Positioning', 'A full body pillow maintains the side-sleeping position that reduces musculoskeletal strain and allows the spine to decompress during sleep. The continuous support prevents the unconscious repositioning movements that fragment sleep in fibromyalgia sufferers.'),
    ],
    'sleep-hygiene-checklist.html': [
        ('sunrise+alarm+clock+light+therapy+wake+up+gradual+morning', 'Sunrise Alarm Clock for Consistent Wake Time', 'Consistent wake time is the single most important sleep hygiene behavior — and a sunrise alarm makes it the path of least resistance. The gradual light raise mimics dawn, lifting cortisol naturally so the alarm goes off to an already-alert brain.'),
        ('blue+light+blocking+glasses+evening+sleep+amber+lens+screen', 'Blue-Light Blocking Glasses for Evening Screen Time', 'Evening blue light exposure delays melatonin onset by 1-3 hours. Amber-lens glasses worn 90 minutes before bed suppress the 480nm wavelength that drives this delay. The single highest-leverage behavioral intervention for sleep onset latency.'),
    ],
    'sleep-immune-system.html': [
        ('sleep+tracker+recovery+HRV+immune+function+wearable', 'Sleep Tracker for Recovery and Immune Monitoring', 'HRV (heart rate variability) during sleep is one of the most sensitive early indicators of immune stress — it drops measurably 1-2 days before symptoms appear. A sleep tracker with HRV monitoring lets you see when your body is fighting something before you feel it.'),
        ('zinc+magnesium+sleep+immune+supplement+ZMA+nighttime', 'Zinc + Magnesium for Sleep and Immune Support', 'Zinc is essential for T-cell production and is most actively recycled during sleep. Magnesium supports melatonin synthesis. Combined in a ZMA-style supplement, both are replenished during the overnight window when immune activity is highest.'),
    ],
    'sleep-inertia.html': [
        ('sunrise+alarm+clock+gradual+wake+sleep+inertia+morning+fog', 'Sunrise Alarm Clock for Reducing Morning Grogginess', 'Sleep inertia is worst when awakening occurs mid-cycle, in deep slow-wave sleep. A sunrise alarm clock triggers cortisol rise earlier, so you naturally surface to lighter sleep stages by alarm time. The difference in grogginess between cycle-aligned and mid-cycle waking is measurable in reaction time tests.'),
        ('light+therapy+lamp+10000+lux+morning+alertness+cortisol+wake', 'Light Therapy Lamp for Morning Cortisol Reset', 'Ten minutes of 10,000-lux light exposure within 30 minutes of waking is the fastest non-pharmacological intervention for sleep inertia. It suppresses residual melatonin and accelerates the cortisol awakening response — the hormone that drives alertness.'),
    ],
    'sleep-myths-series.html': [
        ('sleep+tracker+ring+wrist+objective+data+sleep+quality', 'Sleep Tracker for Fact-Checking Your Own Sleep', 'Many sleep myths persist because sleep is subjective — people genuinely misperceive how much they slept or how long it took to fall asleep. A wrist or ring tracker gives you objective data. Often the data disagrees with your perception, and the data tends to be right.'),
        ('magnesium+glycinate+200mg+sleep+evidence+supplement+GABA', 'Magnesium Glycinate — One of the Few Supplements With Evidence', 'Most sleep supplements are myths in pill form. Magnesium glycinate is an exception: it has plausible mechanism (GABA pathway support), multiple randomized trials, and a consistent safety profile. 200-400mg before bed, glycinate form for absorption.'),
    ],
    'sleep-productivity.html': [
        ('sunrise+alarm+clock+wake+productivity+morning+energy+light', 'Sunrise Alarm Clock for Productive Mornings', 'The first 30 minutes after waking sets the cognitive trajectory for the day. A sunrise alarm that wakes you in a lighter sleep stage — rather than jarring you out of deep sleep — produces measurably better working memory and reaction time in the first 2 hours.'),
    ],
    'sleep-tracking-data.html': [
        ('HRV+recovery+wearable+ring+sleep+score+interpretation+data', 'HRV-Tracking Wearable for Sleep Data Interpretation', 'Heart rate variability during sleep is the most actionable metric in modern sleep tracking. A downward HRV trend over several nights predicts cognitive decline before you feel it. Ring-form trackers measure HRV more accurately than wrist devices due to superior optical contact.'),
    ],
    'social-jetlag.html': [
        ('low+dose+melatonin+0.5mg+circadian+schedule+alignment+weekend', 'Low-Dose Melatonin for Weekend Schedule Alignment', 'Social jet lag accumulates when weekend sleep timing differs by 2+ hours from weekdays. 0.3-0.5mg melatonin taken at your target weekday bedtime on Friday and Saturday nights prevents the phase delay that causes Monday morning grogginess.'),
        ('sunrise+alarm+clock+consistent+wake+time+circadian+rhythm', 'Sunrise Alarm Clock for Consistent Wake Time', 'The most effective intervention for social jet lag is a fixed wake time 7 days a week. A sunrise alarm makes this achievable by replacing shock-arousal with a gradual cortisol signal — reducing the friction that causes people to sleep in on weekends.'),
    ],
}

btn_css = """
    .btn-gold {
      display: inline-block;
      background: var(--gold);
      color: var(--night);
      font-weight: 700;
      font-size: 0.92rem;
      padding: 0.75rem 1.75rem;
      border-radius: 6px;
      text-decoration: none;
      letter-spacing: 0.03em;
      transition: background 0.2s;
    }
    .btn-gold:hover { background: var(--gold-light); color: var(--night); text-decoration: none; }
"""

INJECT_POINTS = ['</main>', '</article>', '<footer', '<div class="sticky-buy-bar"']

for fname, items in adds.items():
    p = Path(f'posts/{fname}')
    html = p.read_text(encoding='utf-8')
    changed = False

    if '.btn-gold' not in html and '.cta-btn' not in html:
        html = html.replace('</style>', btn_css + '  </style>', 1)
        btn_class = 'btn-gold'
    elif '.btn-gold' in html:
        btn_class = 'btn-gold'
    else:
        btn_class = 'cta-btn'

    for query, title, desc in items:
        if query in html:
            print(f'  SKIP: {query[:40]}')
            continue

        block = (
            '\n  <!-- AFFILIATE CTA -->\n'
            '  <div class="product-cta" style="margin:2rem 0;padding:1.5rem;'
            'background:var(--card);border:1px solid rgba(201,168,76,0.3);'
            'border-radius:10px;text-align:center">\n'
            f'    <h3 style="font-family:\'Cormorant Garamond\',serif;font-size:1.3rem;'
            f'color:var(--star);margin-bottom:0.5rem">{title}</h3>\n'
            f'    <p style="color:var(--muted);font-size:0.88rem;margin-bottom:1rem;'
            f'max-width:500px;display:inline-block">{desc}</p><br>\n'
            f'    <a href="https://www.amazon.com/s?k={query}&tag=sleepwiserevi-20" '
            f'class="{btn_class}" target="_blank" rel="noopener">Check Price on Amazon &rarr;</a>\n'
            '    <p style="font-size:0.7rem;color:var(--muted);margin-top:0.5rem">'
            'As an Amazon Associate, SleepWiseReviews earns from qualifying purchases.</p>\n'
            '  </div>\n\n'
        )

        for inject_point in INJECT_POINTS:
            if inject_point in html:
                html = html.replace(inject_point, block + inject_point, 1)
                changed = True
                break

    if changed:
        p.write_text(html, encoding='utf-8')
        links = re_mod.findall(r'amazon\.com[^"]*sleepwiserevi-20', html)
        print(f'OK {fname}: {len(links)} links')
    else:
        print(f'NO CHANGE: {fname}')

print('Done')
