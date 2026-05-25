from pathlib import Path
import re as re_mod

adds = {
    'natural-sleep-aids.html': [
        ('valerian+root+sleep+supplement+GABA+standardized', 'Valerian Root — GABA-Supporting Sleep Aid', 'Valerian root supports the GABA pathway at doses of 300-600mg taken 30-60 minutes before bed. Most studies show benefit after 2 weeks of consistent use. Choose a product standardized to 0.8% valerenic acid for consistent potency.'),
        ('melatonin+0.5mg+low+dose+sleep+supplement', 'Low-Dose Melatonin (0.5mg)', 'The physiologically relevant dose for sleep onset is 0.3-0.5mg, not 5-10mg. Pharmacological doses cause next-day grogginess and downregulate natural production. Look for 0.5mg products or cut a 1mg tablet in half.'),
    ],
    'mattress-buying-guide.html': [
        ('medium+firm+hybrid+mattress+pocketed+coil+back+pain', 'Medium-Firm Hybrid Mattress', 'The most evidence-supported firmness for back and combination sleepers: medium-firm (5-6/10) hybrid with pocketed coils and 2-4 inches of comfort foam. Look for at least 6 inches of coil depth and individually wrapped coils for motion isolation.'),
        ('adjustable+loft+pillow+side+sleepers+shredded+memory+foam', 'Adjustable Loft Pillow for Any Sleep Position', 'A shredded memory foam pillow with adjustable fill lets you dial in the exact loft for spinal neutral after a new mattress purchase changes your shoulder-to-head distance requirements.'),
    ],
    'best-aromatherapy-sleep.html': [
        ('lavender+essential+oil+100+percent+pure+sleep+linalool', 'Lavender Essential Oil 100% Pure', 'Studies using inhalation of genuine lavender oil show measurable reductions in sleep latency. Only pure Lavandula angustifolia produces the studied effect. Avoid synthetic fragrances entirely.'),
        ('essential+oil+diffuser+bedroom+ultrasonic+timer+auto+off', 'Ultrasonic Essential Oil Diffuser with Timer', 'A diffuser with a 60-minute auto-off timer runs during the pre-sleep period and shuts off automatically. Ultrasonic diffusers produce cool mist that also adds mild humidity, a secondary benefit for nasal passages during sleep.'),
    ],
    'sleep-medications-truth.html': [
        ('magnesium+glycinate+sleep+non+prescription+supplement+200mg', 'Magnesium Glycinate — Non-Prescription Sleep Support', 'Among non-prescription sleep interventions, magnesium glycinate (200-400mg) has the strongest evidence base. It works via GABA pathways, the same mechanism as benzodiazepines, but without dependency risk.'),
        ('sleep+tracker+ring+hrv+wearable+monitor+wrist', 'Sleep Tracker for Objective Progress Monitoring', 'A sleep tracker provides objective data showing sleep efficiency improve over weeks even when subjective sleep perception lags behind reality. HRV trends also identify when cortisol dysregulation is contributing to insomnia.'),
    ],
    'restless-legs-syndrome.html': [
        ('magnesium+glycinate+restless+legs+syndrome+supplement', 'Magnesium Glycinate for RLS', 'Magnesium deficiency is one of the most common correctable contributors to restless legs syndrome. Magnesium glycinate at 200-400mg before bed addresses the neuromuscular excitability component of RLS. Often reduces symptom frequency within 2-3 weeks.'),
        ('compression+leg+sleeve+restless+legs+circulation+evening', 'Compression Leg Sleeves for RLS Relief', 'Compression therapy has modest but consistent evidence for RLS symptom reduction. The counterstimulation effect appears to interrupt the sensory-motor urge cycle. Graduated compression sleeves worn in the evening before bed are the most accessible form of this intervention.'),
    ],
    'sleep-chronic-pain.html': [
        ('body+pillow+side+sleeper+chronic+pain+full+support', 'Full Body Pillow for Pain Position Support', 'A full body pillow allows chronic pain sufferers to achieve and maintain a supported side-sleeping position. The continuous support prevents the compensatory movements that fragment sleep. Particularly effective for hip, lower back, and fibromyalgia pain.'),
        ('memory+foam+mattress+topper+pressure+relief+chronic+pain', 'Memory Foam Topper for Pressure Point Relief', 'A 2-3 inch memory foam or latex topper significantly reduces pressure at pain-sensitive points (hips, shoulders, knees) without replacing the mattress. Often the highest-ROI intervention for chronic pain sufferers on an inadequate existing mattress.'),
    ],
    'sleep-sanctuary-guide.html': [
        ('white+noise+machine+sleep+bedroom+sound+masking+50dB', 'White Noise Machine for Sound Masking', 'White noise at 50-55dB masks variable environmental sounds that trigger micro-arousals. Fan-based machines produce true white noise; digital machines offer more sound variety. Either type dramatically improves sleep continuity in noisy environments.'),
        ('sunrise+alarm+clock+smart+wake+up+light+gradual', 'Sunrise Alarm Clock for Consistent Wake-Up', 'A sunrise alarm gradually brightens over 20-30 minutes before your wake time, entraining your cortisol rise to a natural light signal. Paired with blackout curtains, this creates a controlled light environment.'),
    ],
    'memory-foam-vs-hybrid-mattress.html': [
        ('latex+mattress+topper+2+inch+pressure+relief+firmness', 'Latex Mattress Topper for Firmness Adjustment', 'If your mattress is slightly off in firmness, a 2-3 inch natural latex topper adjusts surface feel without replacing the mattress. Latex adds responsiveness to slow-moving memory foam and reduces the stuck feeling some sleepers find disruptive.'),
        ('best+pillow+side+sleeper+memory+foam+adjustable+loft+cervical', 'Matching Pillow for Your Mattress Type', 'Pillow loft requirements change based on mattress firmness. A firmer mattress needs a higher loft pillow; a softer mattress needs a flatter pillow. Adjustable-fill pillows let you calibrate after your mattress purchase.'),
    ],
    'night-shift-optimization.html': [
        ('blackout+sleep+mask+night+shift+workers+daytime+sleep+total', 'Total Blackout Sleep Mask for Daytime Sleep', 'Night shift workers sleeping during the day face full daylight. A high-quality total-blackout sleep mask eliminates light from both front and sides. Combine with ear plugs or white noise to address the second major daytime sleep disruptor.'),
        ('melatonin+0.5mg+low+dose+shift+work+sleep+schedule', 'Low-Dose Melatonin for Phase-Shifted Sleep', 'For night shift workers, 0.5-1mg melatonin taken 30 minutes before your daytime sleep period signals that this is sleep time. Keep doses low to avoid grogginess on your next shift.'),
    ],
    'jet-lag-guide.html': [
        ('melatonin+0.5mg+jet+lag+travel+time+zone+eastward', 'Low-Dose Melatonin for Jet Lag', 'For eastward travel, 0.5mg melatonin taken at the destination bed time for 3-4 nights accelerates clock resynchronization. Reduces jet lag recovery by 1-2 days on typical 5-8 hour crossings.'),
        ('light+therapy+lamp+portable+usb+travel+jet+lag+10000', 'Portable Light Therapy Lamp for Travel', 'A portable 10,000-lux light therapy lamp used at destination wake time is the most powerful tool for resetting your clock during travel. Some compact models are USB-C powered and pack into a laptop bag.'),
    ],
    'cbt-i-guide.html': [
        ('sleep+diary+tracker+insomnia+CBT+sleep+restriction+log', 'Sleep Diary for CBT-I Tracking', 'CBT-I requires accurate baseline data on your sleep patterns. A physical sleep diary used consistently for 2+ weeks before starting gives you the numbers needed to calculate your initial sleep window for sleep restriction therapy.'),
        ('magnesium+glycinate+sleep+quality+CBT+adjunct+200mg', 'Magnesium Glycinate as CBT-I Adjunct', 'Magnesium glycinate (200-400mg) can be used alongside CBT-I without interference. It reduces physiological hyperarousal, the background cortisol elevation that makes falling asleep harder even when CBT-I has addressed the cognitive components.'),
    ],
    'power-nap-science.html': [
        ('sleep+eye+mask+nap+blackout+light+blocking+contoured', 'Blackout Sleep Mask for Office Napping', 'A high-quality total-blackout sleep mask eliminates light stimulation that prevents sleep onset during daytime naps. Look for contoured designs that do not touch the eyelids, allowing REM eye movement during deeper naps.'),
        ('white+noise+machine+small+portable+office+nap+travel', 'Portable White Noise Machine for Napping', 'A compact white noise machine creates the acoustic conditions for sleep onset in open-plan offices, cars, or planes. 50-55dB of steady noise masks the variable sounds that keep the brain in alert mode during attempted naps.'),
    ],
    'pregnancy-sleep-guide.html': [
        ('pregnancy+wedge+pillow+side+sleeping+support+bump', 'Pregnancy Wedge Pillow for Targeted Support', 'A pregnancy wedge pillow is more compact than a full-body pillow and can be positioned precisely where support is needed. Many pregnant women prefer the wedge for travel and warmer months when a full pillow creates too much heat.'),
        ('cooling+mattress+pad+pregnancy+hot+flashes+temperature+regulate', 'Cooling Mattress Pad for Pregnancy Heat', 'Pregnancy raises basal body temperature by 0.5-1 degree Celsius. A cooling mattress pad with active temperature regulation addresses the heat component of pregnancy sleep disruption that no pillow positioning can fix.'),
    ],
    'sleep-apnea-warning-signs.html': [
        ('CPAP+pillow+cutout+side+sleeper+sleep+apnea+mask', 'CPAP-Compatible Side Sleeper Pillow', 'Side sleeping reduces apnea severity by 30-50%. For CPAP users, CPAP-specific pillows with cutouts prevent mask seal disruption, a major cause of CPAP non-compliance. Solves a problem that causes many people to abandon treatment.'),
        ('anti+snoring+mouthpiece+MAD+boil+bite+mandibular+OTC', 'MAD Anti-Snoring Mouthpiece', 'For mild OSA or primary snoring, a mandibular advancement device repositions the jaw forward to prevent airway collapse. Boil-and-bite versions allow home fitting. Consult a sleep physician before substituting for prescribed CPAP in confirmed OSA.'),
    ],
    'reset-sleep-schedule.html': [
        ('blackout+curtains+bedroom+sleep+total+darkness+99+percent', 'Blackout Curtains for Consistent Darkness', 'Regulating your sleep schedule requires consistent darkness at your target bedtime. Blackout curtains rated for 99%+ light blocking eliminate the seasonal variation that derails schedule resets.'),
        ('melatonin+0.3mg+low+dose+circadian+sleep+schedule+reset', 'Low-Dose Melatonin for Schedule Reset', 'During a sleep schedule reset, 0.3-0.5mg melatonin taken 30 minutes before your target bedtime accelerates the phase shift. Keep the dose low to preserve the daytime alertness needed to complete the reset.'),
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
            print(f'  SKIP: {query[:35]}')
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
