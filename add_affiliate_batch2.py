from pathlib import Path
import re as re_mod

adds = {
    '30-day-sleep-challenge.html': [
        ('sleep+tracker+ring+habit+30+day+challenge+monitor', '30-Day Sleep Tracker', 'Track your 30-day sleep improvements with a wearable sleep tracker. HRV and sleep efficiency data make the progress of each weekly challenge visible. Seeing objective improvement sustains motivation through the harder weeks of the protocol.'),
        ('white+noise+machine+sleep+habit+sound+masking+bedroom', 'White Noise Machine for Sleep Habit Foundation', 'A consistent acoustic environment is one of the most underrated sleep habit foundations. White noise eliminates the variable sound intrusions that undermine every other sleep habit you build during the challenge.'),
    ],
    'aging-and-sleep.html': [
        ('sunrise+alarm+clock+older+adults+circadian+wake+up', 'Sunrise Alarm Clock for Circadian Anchoring', 'Age-related circadian changes make morning light exposure more important, not less. A sunrise alarm triggers cortisol release at the right time even in winter darkness, helping maintain the sleep-wake timing that shifts with age.'),
    ],
    'brain-during-sleep.html': [
        ('magnesium+glycinate+deep+sleep+brain+glymphatic+system', 'Magnesium Glycinate for Deep Sleep Enhancement', 'Deep sleep is when the glymphatic system clears metabolic waste from the brain. Magnesium glycinate (200-400mg) has the most consistent evidence for deepening slow-wave sleep among non-prescription supplements, supporting this nightly cleaning cycle.'),
    ],
    'dreams-science.html': [
        ('sleep+mask+REM+eye+movement+blackout+dreaming', 'Blackout Sleep Mask for REM Enhancement', 'Total darkness during sleep increases REM sleep density and dream vividness. A contoured blackout sleep mask that does not press on the eyelids allows natural rapid eye movement without restriction.'),
    ],
    'gut-microbiome-sleep.html': [
        ('magnesium+glycinate+gut+sleep+microbiome+supplement+prebiotics', 'Magnesium Glycinate for Gut-Sleep Connection', 'Magnesium supports both the gut-brain axis and sleep quality through multiple pathways. Deficiency is associated with both microbiome disruption and poor sleep architecture. Glycinate form is gentle on the gut lining compared to oxide or citrate.'),
        ('probiotic+sleep+gut+health+microbiome+supplement+evening', 'Probiotic for Gut-Sleep Support', 'The gut-brain axis bidirectionally influences sleep quality. Evening probiotic supplementation supports the microbiome environment that produces sleep-relevant neurotransmitter precursors including serotonin and GABA precursors during overnight fermentation.'),
    ],
    'lucid-dreaming-guide.html': [
        ('dream+journal+notebook+wake+back+to+bed+WBTB+lucid', 'Dream Journal for MILD and WBTB Technique', 'A physical dream journal kept on the nightstand is the foundational tool for MILD and WILD lucid dreaming practice. Writing immediately on waking dramatically increases dream recall, which is the prerequisite for reality testing and prospective memory setting.'),
    ],
    'morning-habits-sleep.html': [
        ('light+therapy+lamp+morning+habit+cortisol+circadian+10000', 'Morning Light Therapy Lamp', 'Bright light exposure within 30 minutes of waking is the single most effective morning habit for sleep architecture. It anchors your cortisol peak to early morning, making evening melatonin release and sleep onset more reliable. A 10,000-lux lamp delivers the required photon dose in 20 minutes.'),
        ('sunrise+alarm+clock+morning+habit+wake+light+gradual', 'Sunrise Alarm Clock for Consistent Morning Timing', 'Waking at the same time every day is the cornerstone of good sleep. A sunrise alarm gradually brightens 20-30 minutes before your wake time, making consistent early rising easier without the abrupt cortisol shock of a standard alarm.'),
    ],
    'morning-lark-night-owl.html': [
        ('light+therapy+lamp+chronotype+morning+circadian+lark+owl', 'Light Therapy for Chronotype Management', 'Light therapy can shift your circadian phase by 1-2 hours over several weeks. Night owls who need to wake earlier use morning light therapy immediately after their target wake time. Morning larks who want to extend evening alertness use dim lighting and blue-light blocking glasses instead.'),
        ('blue+light+blocking+glasses+night+owl+evening+chronotype', 'Blue Light Blocking Glasses for Night Owls', 'Blocking short-wavelength blue light in the 2-3 hours before your target bedtime delays melatonin suppression and accelerates sleep onset for chronically delayed sleepers. More practical than avoiding all screens; most effective when combined with morning light exposure.'),
    ],
    'polyphasic-sleep.html': [
        ('sleep+eye+mask+nap+blackout+polyphasic+daytime', 'Blackout Sleep Mask for Polyphasic Naps', 'Polyphasic sleep schedules require reliable, fast sleep onset during daytime nap windows. A total-blackout sleep mask eliminates the ambient light that prevents the rapid transitions to Stage 2 and REM sleep that polyphasic sleepers need to achieve in compressed nap periods.'),
        ('sleep+tracker+polyphasic+ring+stages+multiple+naps', 'Sleep Tracker for Polyphasic Stage Monitoring', 'Polyphasic schedules require accurate REM and deep sleep tracking to verify that the compressed schedule delivers sufficient slow-wave and REM. A ring-based sleep tracker provides the continuous monitoring needed across multiple daily nap periods.'),
    ],
    'rem-rebound-explained.html': [
        ('magnesium+glycinate+REM+sleep+supplement+rebound+recovery', 'Magnesium Glycinate for REM Recovery', 'During REM rebound recovery, magnesium glycinate (200-400mg) supports the GABA pathways that facilitate deep and REM sleep. It does not suppress the rebound process but helps ensure the recovery occurs in a physiologically supported environment.'),
        ('sleep+tracker+wearable+REM+monitoring+rebound+stages', 'Sleep Tracker to Monitor REM Rebound', 'A wearable sleep tracker lets you observe your own REM rebound objectively after alcohol cessation, medication changes, or sleep deprivation recovery. Watching REM percentage normalize over days is motivating and validates the recovery process.'),
    ],
    'sleep-after-surgery.html': [
        ('cooling+pillow+surgery+recovery+sleep+gel+copper', 'Cooling Pillow for Post-Surgery Sleep', 'Post-surgical inflammation elevates body temperature, disrupting sleep quality. A gel-infused or copper-infused cooling pillow dissipates heat from the head and neck, the primary source of night-time heat buildup. More accessible than full mattress cooling systems during recovery.'),
        ('body+pillow+surgery+recovery+position+support+side', 'Body Pillow for Surgery Recovery Positioning', 'Maintaining a specific sleep position during surgical recovery is essential for healing and avoiding incision stress. A full body pillow or wedge system supports the recovery position through the night without requiring active conscious effort.'),
    ],
    'sleep-and-alcohol-free.html': [
        ('magnesium+glycinate+alcohol+free+sleep+GABA+withdrawal', 'Magnesium Glycinate for Alcohol-Free Sleep', 'Alcohol withdrawal (even from moderate regular use) temporarily reduces GABA signaling, causing rebound wakefulness and fragmented sleep. Magnesium glycinate at 200-400mg before bed supports the GABA system during the 2-4 week adaptation to alcohol-free sleep.'),
        ('sleep+tracker+ring+alcohol+free+HRV+improvement+monitor', 'Sleep Tracker to Measure HRV Improvement', 'HRV improvement is one of the most measurable and motivating benefits of alcohol cessation. A sleep ring that tracks nightly HRV shows the improvement curve within 2-4 weeks, providing objective data that sustains motivation during the adaptation period.'),
    ],
    'sleep-athletic-performance.html': [
        ('sleep+tracker+athletes+hrv+recovery+sport+ring+wearable', 'Sleep Tracker for Athletic Recovery', 'HRV-based recovery scoring from sleep trackers is now standard practice for elite athletes. A ring or wrist tracker provides the nightly HRV data needed to make evidence-based training load decisions and avoid overtraining syndrome from accumulated sleep debt.'),
        ('magnesium+glycinate+athletic+recovery+sleep+muscle+supplement', 'Magnesium Glycinate for Athletic Sleep Recovery', 'Athletes deplete magnesium through sweat and heavy training loads. Magnesium glycinate (300-400mg before bed) supports deep sleep architecture and muscle recovery signaling. Consistently associated with improved sleep quality in physically active populations.'),
    ],
    'sleep-autism-spectrum.html': [
        ('weighted+blanket+autism+sleep+anxiety+deep+pressure', 'Weighted Blanket for Sensory Sleep Support', 'Weighted blankets provide deep pressure stimulation that activates the parasympathetic nervous system in many autistic individuals. Multiple studies demonstrate improved sleep onset and reduced nighttime waking in children and adults with autism who use 10-15% body-weight blankets.'),
        ('white+noise+machine+autism+sensory+sleep+sound+masking', 'White Noise Machine for Sensory Sleep Environment', 'Consistent acoustic environment reduces the sensory unpredictability that can disrupt sleep in autistic individuals. White noise or brown noise at consistent volume masks the variable environmental sounds that can trigger arousal from light sleep stages.'),
    ],
    'sleep-cortisol-stress.html': [
        ('magnesium+glycinate+cortisol+stress+sleep+HPA+supplement', 'Magnesium Glycinate for Cortisol Regulation', 'Magnesium is a natural HPA axis regulator. Low magnesium status is associated with elevated cortisol reactivity, creating a cycle where stress depletes magnesium and magnesium deficiency amplifies the cortisol stress response. Glycinate form is specifically relevant for stress-related sleep issues.'),
        ('sleep+tracker+HRV+cortisol+stress+monitor+wearable+recovery', 'Sleep Tracker for Stress-Sleep Monitoring', 'HRV from a nightly sleep tracker is the most accessible objective measure of HPA axis activation. Tracking HRV trends over weeks shows you whether your stress management interventions are actually reducing autonomic load during sleep.'),
    ],
    'sleep-grief.html': [
        ('magnesium+glycinate+grief+sleep+anxiety+cortisol+supplement', 'Magnesium Glycinate for Grief-Related Sleep Disruption', 'Grief activates the cortisol stress response continuously. Magnesium glycinate supports the GABA pathways that cortisol suppresses, without creating dependency. At 200-400mg before bed, it addresses the physiological component of grief-related insomnia.'),
        ('weighted+blanket+grief+comfort+sleep+anxiety+deep+pressure', 'Weighted Blanket for Grief-Related Sleep Anxiety', 'The deep pressure stimulation from a weighted blanket activates the parasympathetic nervous system. Many people experiencing grief report that the physical weight provides a comfort cue that reduces pre-sleep anxiety and shortens sleep onset.'),
    ],
    'sleep-hydration.html': [
        ('water+bottle+nightstand+hydration+sleep+waking+thirst', 'Nightstand Water Bottle for Sleep Hydration', 'Mild dehydration (as little as 1-2% body weight) increases cortisol and reduces sleep quality. Keeping a water bottle on the nightstand for pre-sleep hydration reduces the risk of waking due to thirst and supports the overnight urine concentration process.'),
        ('sleep+tracker+hrv+hydration+monitor+wearable+recovery', 'Sleep Tracker to Monitor Hydration Impact', 'HRV drops measurably with dehydration. A nightly sleep tracker lets you observe the correlation between your hydration habits and sleep quality over days and weeks, making the sleep-hydration relationship personally concrete and actionable.'),
    ],
    'sleep-immune-system.html': [
        ('vitamin+D3+K2+immune+sleep+supplement+winter+immunity', 'Vitamin D3 + K2 for Immune-Sleep Support', 'Vitamin D deficiency impairs both immune function and sleep architecture. D3 with K2 (for calcium metabolism safety) at 2000-4000 IU supports the immune-sleep link, particularly in winter months when sunlight exposure is insufficient.'),
    ],
    'sleep-inertia.html': [
        ('coffee+nap+caffeine+timing+sleep+inertia+wake+up', 'Smart Coffee Timer for Caffeine Napping', 'The caffeine nap (200mg caffeine immediately before a 20-minute nap) is the highest-evidence intervention for sleep inertia. Caffeine takes 20-30 minutes to cross the blood-brain barrier, so it activates precisely as you wake. Any automatic coffee maker with a 20-minute delay makes this practical.'),
    ],
    'sleep-journal-guide.html': [
        ('sleep+journal+notebook+quality+gratitude+bedtime+routine', 'Sleep Journal and Bedtime Notebook', 'A sleep journal serves two functions: cognitive offloading (writing tomorrow tasks reduces pre-sleep rumination) and pattern recognition (tracking sleep quality against lifestyle variables reveals personal sleep saboteurs over weeks). A dedicated notebook kept on the nightstand works better than digital apps for pre-sleep use.'),
        ('magnesium+glycinate+sleep+journal+quality+supplement+track', 'Magnesium Glycinate to Track in Your Sleep Journal', 'Adding magnesium glycinate (200-400mg before bed) while using a sleep journal lets you track the intervention with your own data. Most people see improvement in sleep onset time within 1-2 weeks — visible in daily journal quality ratings.'),
    ],
    'sleep-light-therapy.html': [
        ('light+therapy+lamp+10000+lux+SAD+circadian+morning', 'Light Therapy Lamp — 10,000 Lux', 'A 10,000-lux light therapy lamp used for 20-30 minutes at your target wake time delivers the photon dose that advances circadian phase. Most effective for SAD, delayed sleep phase disorder, and anyone who wakes in darkness during winter months.'),
        ('blue+light+blocking+glasses+evening+melatonin+screen', 'Blue Light Blocking Glasses for Evening Use', 'Blocking blue light in the 90-120 minutes before your target bedtime significantly increases melatonin production speed and onset time. Most effective for people who use screens in the evening and whose sleep timing is delayed relative to their schedule requirements.'),
    ],
    'sleep-loneliness.html': [
        ('weighted+blanket+loneliness+sleep+comfort+physical+touch', 'Weighted Blanket for Loneliness and Sleep', 'Weighted blankets activate the same deep-touch pressure pathways stimulated by physical contact. Research shows reduced cortisol and increased oxytocin response to deep pressure. For sleep disruption related to loneliness or social isolation, the weight provides a non-pharmaceutical parasympathetic activation cue.'),
        ('white+noise+machine+loneliness+sleep+companion+sound', 'White Noise Machine for Sleep Environment', 'An empty, quiet bedroom amplifies loneliness-related hyperarousal. White noise provides a consistent, benign ambient sound that reduces the contrast of silence that can trigger rumination. Simple but consistently effective for people sleeping alone for the first time.'),
    ],
    'sleep-longevity.html': [
        ('sleep+tracker+longevity+hrv+aging+biological+wearable', 'Sleep Tracker for Longevity Monitoring', 'HRV decline with age can be slowed with sleep optimization. A nightly sleep tracker shows how lifestyle interventions affect HRV trend, providing the closest available consumer approximation of biological age trajectory. Long-term HRV data is the sleep longevity metric with the strongest association with all-cause mortality risk.'),
        ('magnesium+glycinate+longevity+sleep+deep+wave+supplement', 'Magnesium Glycinate for Sleep Longevity', 'Magnesium deficiency accelerates with age and is associated with reduced deep sleep, increased cortisol, and elevated inflammatory markers. Magnesium glycinate supplementation at 200-400mg before bed is the most evidence-supported non-prescription intervention for age-related deep sleep loss.'),
    ],
    'sleep-memory-learning.html': [
        ('sleep+tracker+deep+REM+memory+learning+academic+student', 'Sleep Tracker for Memory Consolidation Monitoring', 'Memory consolidation occurs during slow-wave sleep (declarative memory) and REM sleep (procedural and emotional memory). A sleep tracker lets students and knowledge workers observe how their study and lifestyle choices affect the sleep stages most critical for learning.'),
        ('magnesium+glycinate+memory+learning+sleep+supplement+student', 'Magnesium Glycinate for Learning-Sleep Support', 'Magnesium supports both synaptic plasticity (learning) and sleep architecture (consolidation). For students, 200-400mg of magnesium glycinate before bed addresses both sides of the sleep-memory equation without pharmaceutical risk.'),
    ],
    'sleep-mental-health.html': [
        ('magnesium+glycinate+anxiety+depression+sleep+mental+health', 'Magnesium Glycinate for Sleep-Mental Health', 'Bidirectional: poor sleep worsens mental health, mental health problems disrupt sleep. Magnesium glycinate addresses both by supporting GABA signaling (reducing physiological anxiety) and improving sleep architecture. 200-400mg before bed is a well-tolerated starting point alongside professional mental health treatment.'),
        ('weighted+blanket+anxiety+depression+sleep+comfort+pressure', 'Weighted Blanket for Anxiety-Related Sleep Disruption', 'Multiple studies show that weighted blankets reduce self-reported anxiety and improve sleep quality in clinical anxiety populations. Deep pressure stimulation activates the parasympathetic nervous system via the same mechanoreceptor pathway as social touch.'),
    ],
    'sleep-myths-series.html': [
        ('sleep+supplement+melatonin+magnesium+glycinate+evidence', 'Evidence-Based Sleep Supplements', 'The myths in this series often lead people toward ineffective interventions. Magnesium glycinate (GABA support) and low-dose melatonin (0.5mg, not 10mg) are the two supplements with the strongest evidence base for primary sleep issues. Skip the rest until these are optimized.'),
    ],
    'sleep-paralysis-explained.html': [
        ('sleep+tracker+ring+REM+monitor+paralysis+episodes', 'Sleep Tracker to Monitor REM Patterns', 'Sleep paralysis occurs during REM sleep, particularly during transitions. A wearable sleep tracker that monitors REM duration and timing helps identify the sleep conditions that make sleep paralysis more likely: irregular schedule, sleep deprivation, back sleeping, and REM rebound.'),
        ('white+noise+machine+sleep+paralysis+anxiety+environment', 'White Noise Machine for Sleep Paralysis Anxiety', 'Sleep environment consistency reduces the hyperarousal that triggers sleep paralysis. White noise creates a predictable acoustic environment that reduces startle responses and the sleep-stage transition disturbances associated with higher sleep paralysis frequency.'),
    ],
    'sleep-quality-vs-quantity.html': [
        ('sleep+tracker+quality+efficiency+wearable+hrv+monitor', 'Sleep Tracker for Quality Measurement', 'Sleep efficiency (time asleep vs time in bed) is the most clinically validated marker of sleep quality. A wearable tracker makes this number visible nightly, showing whether your 8 hours produces genuine restorative sleep or fragmented light-stage cycling.'),
        ('magnesium+glycinate+sleep+quality+deep+wave+supplement+200mg', 'Magnesium Glycinate for Sleep Quality', 'Quality sleep requires adequate deep sleep (slow-wave) and REM. Magnesium glycinate (200-400mg before bed) consistently shows improvement in subjective sleep quality and sleep efficiency in randomized trials, primarily by supporting the GABA pathways that govern sleep architecture.'),
    ],
    'sleep-travel-tips.html': [
        ('travel+sleep+kit+eye+mask+earplugs+neck+pillow+airplane', 'Complete Sleep Travel Kit', 'A sleep travel kit covering the three main in-flight sleep disruptors: noise (foam earplugs), light (total-blackout eye mask), and neck position (memory foam travel pillow). All three are needed for actual sleep on long-haul flights; individual items are partial solutions.'),
        ('melatonin+0.5mg+travel+jet+lag+time+zone+sleep+kit', 'Low-Dose Melatonin for Travel', 'For eastward travel, 0.5mg melatonin taken at destination bedtime for 3 nights accelerates clock reset. Low dose is critical: 5-10mg causes grogginess that counteracts the purpose. Timing matters more than dose; use your phone to set a reminder at destination bedtime from your home timezone.'),
    ],
    'snoring-causes-fixes.html': [
        ('nasal+strips+snoring+breathe+right+nasal+dilator+sleep', 'Nasal Strips for Nasal-Origin Snoring', 'If your snoring occurs with your mouth closed or is primarily nasal in character, nasal strips address the cause directly: they mechanically widen the nasal valve and reduce nasal resistance. Ineffective for mouth-breathing or throat-based snoring but highly effective for nasal congestion.'),
        ('anti+snoring+mouthpiece+mandibular+MAD+boil+bite+jaw', 'MAD Anti-Snoring Mouthpiece', 'For throat-based snoring (most common), a mandibular advancement device repositions the lower jaw forward to tension the soft palate and prevent vibration. Boil-and-bite versions allow home fitting. The most evidence-supported OTC device for reducing snoring frequency and intensity.'),
    ],
    'social-jetlag.html': [
        ('blue+light+blocking+glasses+social+jetlag+evening+screen', 'Blue Light Blocking Glasses for Social Jetlag', 'Evening screen use is a major driver of social jetlag by delaying the circadian clock into weekend nights. Blue light blocking glasses worn after sunset preserve melatonin production and reduce the weekend phase delay that creates Monday grogginess.'),
    ],
    'summer-sleep-guide.html': [
        ('cooling+mattress+pad+summer+sleep+hot+weather+temperature', 'Cooling Mattress Pad for Summer Sleep', 'Summer sleep disruption is primarily thermoregulatory. A cooling mattress pad that actively dissipates body heat addresses the root cause more directly than fans or air conditioning alone. Most effective for people who share a bed with a heat-generating partner.'),
        ('blackout+curtains+summer+heat+light+morning+bedroom', 'Blackout Curtains for Summer Morning Light', 'Summer sleep is disrupted by both heat and early morning light. Blackout curtains address both: they block the early dawn light that suppresses melatonin prematurely and provide a layer of thermal insulation against solar heating of the bedroom.'),
    ],
    'teen-sleep-guide.html': [
        ('blackout+curtains+teen+sleep+morning+light+school', 'Blackout Curtains for Teen Bedrooms', 'Teenagers have a biologically later circadian phase and need darkness to extend sleep into the morning. Blackout curtains allow the additional 60-90 minutes of sleep that early school schedules prevent, reducing the cumulative sleep debt that impairs academic performance and mood.'),
        ('white+noise+machine+teen+sleep+study+environment+focus', 'White Noise Machine for Teen Study and Sleep', 'Consistent acoustic environment during both study and sleep improves both focus and sleep quality in teenagers. White noise reduces the variable household sounds that interrupt concentration during homework and trigger micro-arousals during sleep.'),
    ],
    'waking-at-3am.html': [
        ('magnesium+glycinate+3am+waking+cortisol+supplement+sleep', 'Magnesium Glycinate for 3am Waking', 'Early morning waking (3-4am) is often driven by cortisol rising prematurely due to elevated stress or low magnesium. Magnesium glycinate at 200-400mg at bedtime blunts the cortisol spike through GABA support, extending the second half of sleep in many people who wake consistently at 3am.'),
        ('sleep+tracker+wake+3am+cortisol+HRV+monitor+pattern', 'Sleep Tracker to Identify 3am Wake Patterns', 'A nightly sleep tracker identifies whether your 3am waking is tied to REM transitions, breathing disturbances, heart rate spikes, or HRV drops. Distinguishing stress-cortisol waking from sleep apnea events requires data, not guessing. The pattern guides the right intervention.'),
    ],
    'weekend-sleep-mistake.html': [
        ('blue+light+glasses+weekend+evening+social+jetlag+screen', 'Blue Light Blocking Glasses for Weekend Evenings', 'Weekend social jetlag is driven by later evening light exposure on Friday and Saturday nights. Blue light blocking glasses preserve melatonin production during evening social activities without requiring behavioral change, reducing the Monday sleep debt.'),
        ('sunrise+alarm+weekend+consistency+sleep+schedule+wake', 'Sunrise Alarm Clock for Weekend Wake Consistency', 'The most effective fix for weekend sleep debt is maintaining a consistent wake time. A sunrise alarm makes waking at a consistent time on weekends feel natural rather than forced, by triggering cortisol release gradually rather than abruptly.'),
    ],
    'women-sleep-differences.html': [
        ('magnesium+glycinate+women+hormonal+sleep+PMS+menstrual+cycle', 'Magnesium Glycinate for Hormonal Sleep Disruption', 'Magnesium deficiency worsens PMS symptoms and the sleep disruption associated with the luteal phase. 200-400mg magnesium glycinate before bed during the 7-10 days before menstruation addresses both the GABA component of pre-menstrual anxiety and the sleep architecture disruption.'),
        ('cooling+pillow+women+night+sweats+hormonal+sleep+menopause', 'Cooling Pillow for Hormonal Night Sweats', 'Hormonal temperature dysregulation at any life stage (PMS, perimenopause, menopause) responds to active cooling during sleep. A copper or gel-infused cooling pillow dissipates the head and neck heat that triggers nighttime waking during hormonal fluctuations.'),
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

total_changed = 0
for fname, items in adds.items():
    p = Path(f'posts/{fname}')
    if not p.exists():
        print(f'MISSING: {fname}')
        continue
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
        total_changed += 1
    else:
        print(f'NO CHANGE: {fname}')

print(f'\nTotal files changed: {total_changed}')
