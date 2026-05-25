"""
Inject JSON-LD FAQ schema into editorial posts — batch 2.
Skips posts that already have schema markup.
"""
import json
from pathlib import Path

FAQS = {
    'sleep-stages-explained.html': [
        ("What are the stages of sleep?",
         "Sleep consists of four stages cycling throughout the night. Stage 1 (N1): light sleep, 1-7 minutes, easily awakened. Stage 2 (N2): true sleep, 10-25 minutes, heart rate slows, temperature drops, sleep spindles protect against waking. Stage 3 (N3): slow-wave or deep sleep, hardest to wake from, critical for physical restoration, memory consolidation, and immune function. REM: vivid dreaming, emotional processing, near-paralysis of voluntary muscles. A full cycle takes 90 minutes; adults complete 4-6 cycles per night."),
        ("How much deep sleep do you need per night?",
         "Adults typically get 15-25% of total sleep as slow-wave (deep) sleep, equating to 60-90 minutes in a 7-8 hour night. Deep sleep is concentrated in the first half of the night — your first two sleep cycles have the most. You cannot directly increase deep sleep percentage, but you can protect it: avoid alcohol, maintain a consistent sleep schedule, and ensure adequate total sleep duration."),
        ("What happens if you don't get enough REM sleep?",
         "REM sleep deprivation impairs emotional regulation, memory consolidation, and creative problem-solving. After REM deprivation, the brain shows REM rebound — dramatically increasing REM percentage on recovery nights. Chronic REM suppression (common with alcohol and some antidepressants) is associated with increased anxiety, depression risk, and impaired learning. Most REM occurs in the last 2-3 hours of sleep — cutting sleep short eliminates disproportionate amounts of REM."),
        ("Which sleep stage is most important?",
         "All stages serve essential functions that cannot be fully compensated by other stages. Slow-wave sleep is most critical for physical restoration (growth hormone release, immune function, tissue repair). REM sleep is most critical for emotional processing, memory integration, and cognitive function. Stage 2 sleep constitutes the largest portion of sleep and has important roles in motor learning and cognitive consolidation. The question is somewhat like asking which meal of the day is most important."),
    ],
    'waking-at-3am.html': [
        ("Why do I wake up at 3am every night?",
         "3am waking has several common causes: the sleep cycle structure (the last slow-wave sleep cycle typically ends around 3-4am, and the subsequent REM-rich light sleep is more vulnerable to waking), cortisol fluctuation (cortisol begins rising around 3-5am to prepare for waking, and in people with anxiety or HPA axis dysregulation, this rise is too steep), blood sugar drops (common in people who eat late and in those with insulin resistance), and alcohol metabolism (alcohol consumed in the evening is fully metabolized around 3-4am, causing rebound arousal)."),
        ("How do I stop waking up at 3am?",
         "The approach depends on the cause. For anxiety-driven waking: cognitive restructuring and stimulus control (don't lie awake in bed). For cortisol-driven waking: stress management, consistent sleep timing, and avoiding stimulants after noon. For blood sugar-driven waking: eat a small protein-fat snack before bed (prevents hypoglycemia) and reduce simple carbohydrates in the evening. For alcohol-related waking: stop drinking 4+ hours before bed. Magnesium glycinate at bedtime reduces nocturnal cortisol fluctuation for many people."),
        ("Is waking up at 3am normal?",
         "Brief awakening at sleep cycle transitions (every 90 minutes) is entirely normal and does not require treatment. The problem is the inability to return to sleep. Waking and returning to sleep within 5-10 minutes is physiologically normal; lying awake for 30+ minutes at 3am multiple nights per week indicates a disruption worth addressing. Older adults wake more frequently as slow-wave sleep decreases — this is normal aging, not insomnia."),
        ("What does waking at 3am mean spiritually?",
         "Various spiritual traditions assign meaning to 3am waking, but sleep medicine attributes it to physiology — the end of slow-wave sleep cycles and the beginning of cortisol rise. The consistency of the timing (3-4am) is physiological, not mystical: it reflects reproducible circadian events. Assigning meaning to sleep disruption can increase anxiety about the awakening itself, which is counterproductive to returning to sleep."),
    ],
    'insomnia-types.html': [
        ("What are the different types of insomnia?",
         "Insomnia is classified by duration and pattern. By duration: acute insomnia (days to weeks, usually triggered by stress or disruption) and chronic insomnia (3+ nights per week, 3+ months). By pattern: sleep onset insomnia (difficulty falling asleep), sleep maintenance insomnia (difficulty staying asleep), and early morning awakening (waking before desired and unable to return to sleep). Most chronic insomnia involves multiple patterns simultaneously."),
        ("What is the difference between acute and chronic insomnia?",
         "Acute insomnia is triggered by a specific event (stress, illness, schedule disruption) and resolves within days to weeks as the trigger resolves. Chronic insomnia persists for 3+ months and is maintained by behavioral and cognitive factors independent of the original trigger — hyperarousal, conditioned bed-wakefulness, sleep anxiety, and maladaptive coping. The distinction matters because acute insomnia benefits from reassurance and sleep hygiene, while chronic insomnia requires CBT-I."),
        ("What causes insomnia?",
         "Insomnia has predisposing, precipitating, and perpetuating factors (the 3-P model). Predisposing: genetics, anxiety tendency, female sex, older age. Precipitating: stress, illness, loss, schedule disruption. Perpetuating: spending too long in bed, using bed for non-sleep activities, catastrophizing about sleep, napping to compensate, and excessive monitoring of sleep — the behaviors that convert acute to chronic insomnia. CBT-I targets the perpetuating factors."),
        ("Can insomnia be cured permanently?",
         "Yes, for the majority of people. CBT-I produces durable remission in 70-80% of chronic insomnia cases, with benefits maintained at 1-year follow-up. The key is addressing the behavioral and cognitive perpetuating factors, not just the symptoms. Sleep medications provide temporary relief but do not address underlying perpetuating factors — when discontinued, insomnia often returns. CBT-I that achieves genuine remission — not just controlled symptoms — is considered a cure."),
    ],
    'melatonin-guide.html': [
        ("What does melatonin actually do?",
         "Melatonin is a hormone produced by the pineal gland that signals darkness to the body. It does not directly cause sleep — it shifts the circadian clock and lowers the threshold for sleep initiation. The brain's circadian clock uses melatonin to coordinate 'biological night' across organ systems, suppressing wakefulness signals and preparing the body for sleep. It is not a sedative; it is a timing signal."),
        ("What is the correct dose of melatonin for sleep?",
         "The physiologically relevant dose is 0.3-0.5mg. This matches natural peak melatonin concentrations. The 5-10mg doses sold in most US pharmacies are 10-30x this amount and act primarily as sedatives rather than circadian signals. Low doses (0.3-0.5mg) taken 30-60 minutes before target bedtime produce the circadian effect; high doses cause grogginess and may downregulate natural melatonin production over time."),
        ("When should I take melatonin?",
         "For sleep onset support: 30-60 minutes before target bedtime. For jet lag (eastward): at the destination bedtime on the night of arrival and 2-3 subsequent nights. For delayed sleep phase (consistently can't sleep before midnight): 2-3 hours before the desired bedtime, not at the desired bedtime. Timing matters more than dose — melatonin taken at the wrong circadian phase can worsen the problem it is trying to solve."),
        ("Is melatonin safe to take every night?",
         "Short-term use (weeks to months) at low doses (0.3-0.5mg) appears safe in adults. Long-term daily use has limited safety data. There is theoretical concern that chronic supplementation may suppress natural melatonin production, though this has not been definitively demonstrated in adults. Melatonin is not recommended for chronic insomnia maintenance — CBT-I is the appropriate treatment. Use melatonin for circadian timing issues, not as a nightly sleep aid."),
    ],
    'caffeine-half-life-sleep.html': [
        ("How long does caffeine stay in your system?",
         "Caffeine has a half-life of 5-7 hours in most adults, meaning half of a consumed dose remains active after that period. A 200mg coffee at 2pm still leaves 100mg active at 7-9pm, and 50mg at midnight. Individual variation is significant — genetic differences in CYP1A2 (the enzyme that metabolizes caffeine) make some people fast metabolizers (half-life ~3 hours) and others slow metabolizers (half-life 10+ hours)."),
        ("What time should I stop drinking coffee for good sleep?",
         "For the average adult with a 5-7 hour half-life and a 10pm bedtime, the cutoff is around 2pm for the last caffeinated drink. For slow metabolizers, the cutoff may need to be noon. The general rule — no caffeine after 2pm — works for most people, but those who consistently have trouble falling asleep should experiment with earlier cutoffs. Even decaf coffee contains 5-20mg caffeine and should be considered."),
        ("Does caffeine cause insomnia?",
         "Caffeine does not cause insomnia directly, but it can unmask or worsen it. By blocking adenosine receptors, caffeine suppresses the sleep drive signal that would normally make falling asleep easy. In people already predisposed to insomnia (high physiological arousal, anxiety), this adenosine suppression keeps them awake past the window where natural sleepiness would have overcame wakefulness."),
        ("What is the caffeine crash and how do I avoid it?",
         "The caffeine crash occurs when caffeine clears from adenosine receptors, and the adenosine that accumulated behind the block floods in simultaneously. The larger the caffeine dose, the worse the crash. Avoiding the crash: use lower doses more consistently (2-3 smaller servings rather than 1 large one), don't use caffeine to fight true sleep debt (it will hit harder when it clears), and stop caffeine by 2pm to allow partial adenosine clearance before evening."),
    ],
    'blue-light-melatonin.html': [
        ("How does blue light affect melatonin?",
         "Blue light (wavelength approximately 460-480nm) is the most potent suppressor of melatonin production because the intrinsically photosensitive retinal ganglion cells (ipRGCs) that connect to the suprachiasmatic nucleus (the circadian clock) are maximally sensitive to this wavelength. Even 30-60 minutes of blue-enriched light exposure in the evening can delay melatonin onset by 1-3 hours and reduce total melatonin output by 50%."),
        ("Do blue light glasses actually work for sleep?",
         "Amber-lens blue light blocking glasses (those that appear orange or amber, not clear) substantially reduce melatonin suppression from screens. Studies show 40-58% reduction in melatonin suppression compared to no glasses. Yellow-tinted or 'gaming' glasses block far less and have minimal impact on sleep. The glasses address the light component; they do not address the cognitive arousal from stimulating screen content."),
        ("What is the best way to reduce blue light exposure at night?",
         "In order of effectiveness: (1) Stop using screens 90+ minutes before bed — eliminates both blue light and cognitive stimulation; (2) Switch indoor lighting to warm/red-spectrum bulbs (2700K or lower) after sunset; (3) Wear amber-lens blue light blocking glasses starting 90 minutes before bed; (4) Enable night mode/True Tone on devices (reduces but does not eliminate the effect). Options 1 and 2 are more effective than glasses alone."),
        ("How long before bed should you avoid blue light?",
         "90 minutes is the evidence-based minimum for meaningful melatonin preservation. The melatonin onset window — called DLMO (dim-light melatonin onset) — begins approximately 2 hours before natural sleep time. Blue light exposure during this window suppresses the rising melatonin curve. For maximal effect, begin reducing blue light exposure as darkness falls rather than waiting until just before bed."),
    ],
    'sleep-memory-learning.html': [
        ("How does sleep improve memory?",
         "Sleep consolidates memory through three mechanisms. During slow-wave sleep, the hippocampus replays newly acquired experiences, transferring them to long-term cortical storage. During REM sleep, new information is integrated with existing knowledge — this is the mechanism behind insight and creative problem-solving. Stage 2 sleep, with its sleep spindles, consolidates procedural and motor memories. Sleeping within 24 hours of learning is necessary for full consolidation; the benefit is lost if sleep is delayed significantly."),
        ("Is it better to study before sleeping?",
         "Yes — studying in the hours before sleep produces better retention than studying in the morning and staying awake, controlling for total time elapsed. The sleeping brain consolidates material learned closest to sleep onset most efficiently. However, the quality of pre-sleep studying matters: passive review is consolidated; deep processing (practice problems, self-testing) produces stronger encoding that sleep can consolidate more effectively."),
        ("Can a nap help you remember things?",
         "Yes. A 60-90 minute nap (long enough to include slow-wave sleep) produces memory consolidation equivalent to a full night of sleep for material learned that morning. A 20-minute nap improves procedural motor memories and alertness without producing the same consolidation effect as longer naps. The benefit of napping for learning is most pronounced when total nighttime sleep is under 7 hours."),
        ("Does pulling an all-nighter affect memory?",
         "Significantly and durably. Sleep deprivation reduces hippocampal activity by approximately 40%, impairing new encoding as well as the consolidation of previously learned material. Studying all night before an exam trades consolidation of everything studied during the week for the marginal information studied during the night — a poor trade. Material studied without subsequent sleep is forgotten at 2-3x the normal rate."),
    ],
    'circadian-rhythm-basics.html': [
        ("What is the circadian rhythm?",
         "The circadian rhythm is a roughly 24-hour biological clock present in virtually every cell of the body. It is generated by a genetic feedback loop (the CLOCK-BMAL1/PER-CRY loop) and synchronized daily by external time cues (zeitgebers), primarily light. The master clock resides in the suprachiasmatic nucleus (SCN) of the hypothalamus, which coordinates peripheral clocks in organs, tissues, and cells throughout the body, aligning their function with the 24-hour day."),
        ("What disrupts the circadian rhythm?",
         "The most powerful circadian disruptors are: light at the wrong time (especially evening blue light from screens and indoor lighting), irregular sleep-wake schedules, trans-meridian travel (jet lag), shift work, eating at misaligned times, and social jet lag. Even moderate irregularity — varying sleep times by 1.5+ hours between weekdays and weekends — measurably impairs circadian amplitude and metabolic health."),
        ("How do I reset my circadian rhythm?",
         "Light is the primary lever. Morning bright light exposure (outdoor sunlight or 10,000-lux light therapy) advances a delayed clock; evening light avoidance prevents further delay. A fixed wake time drives circadian stabilization faster than any other single intervention. Low-dose melatonin (0.3-0.5mg) at the desired bedtime accelerates phase shift. Temperature cues (cool room at night), meal timing, and exercise timing are secondary but additive zeitgebers."),
        ("What time does the circadian rhythm peak?",
         "The circadian rhythm has multiple peaks for different functions. Core body temperature peaks in the late afternoon (5-7pm), which is also when physical performance peaks. Cognitive performance peaks mid-morning (around 10am) for analytical tasks and late morning-early afternoon for creative work. Melatonin begins rising approximately 2 hours before natural sleep time (DLMO — dim-light melatonin onset). Cortisol peaks within 30-45 minutes of waking (cortisol awakening response)."),
    ],
    'sleep-anxiety-techniques.html': [
        ("What is the best technique for falling asleep with anxiety?",
         "Physiological sighing (a double inhale through the nose followed by a long exhale through the mouth) is the fastest evidence-based technique for acute anxiety reduction before sleep. It offloads CO2 rapidly, activating the parasympathetic nervous system within seconds. Progressive muscle relaxation (systematically tensing and releasing muscle groups) reduces physiological tension within 10-15 minutes. Cognitive techniques (scheduling worry time, acceptance-based approaches) address the cognitive component that keeps the brain alert."),
        ("Does anxiety cause insomnia or does insomnia cause anxiety?",
         "Both — they are bidirectional. Anxiety activates the HPA axis, elevating cortisol and reducing the parasympathetic tone needed for sleep onset. But insomnia then creates anxiety about sleep itself (sleep anxiety), creating a secondary anxiety loop independent of the original anxiety. Hyperarousal — the chronic elevation of physiological and cognitive arousal — is the common pathway. This is why CBT-I (which directly targets hyperarousal) is effective even when the original anxiety was not about sleep."),
        ("How do I stop my mind from racing at night?",
         "Scheduled worry time (30 minutes in the late afternoon, separate from bed) gives the anxious mind a sanctioned window to process concerns, reducing the urge to do so in bed. 4-7-8 breathing (inhale 4 counts, hold 7, exhale 8) activates the parasympathetic nervous system. Body scan meditation shifts attention away from racing thoughts toward physical sensation. Stimulus control (leaving bed when unable to sleep for 20 minutes) breaks the conditioned association between bed and mental activation."),
        ("Is melatonin effective for anxiety-related sleep problems?",
         "Limited for anxiety specifically. Melatonin is a circadian signal, not an anxiolytic — it does not reduce the physiological arousal that anxiety creates. Magnesium glycinate (200-400mg) has more relevance for anxiety-driven insomnia because it supports GABA pathway activity, which directly reduces physiological hyperarousal. L-theanine (200mg) shows modest anti-anxiety effects that may help sleep onset. Neither replaces CBT-I for anxiety-related chronic insomnia."),
    ],
    'sleep-cortisol-stress.html': [
        ("How does stress affect sleep?",
         "Stress activates the hypothalamic-pituitary-adrenal (HPA) axis, elevating cortisol and the sympathetic nervous system. Elevated nighttime cortisol delays melatonin onset, increases sleep onset latency, reduces slow-wave sleep, and fragments sleep architecture. Chronic stress also activates the prefrontal cortex during the pre-sleep period (worry, rumination), creating cognitive hyperarousal on top of physiological hyperarousal. Together, these mechanisms explain why stressful periods reliably produce poor sleep."),
        ("What time of day is cortisol highest?",
         "Cortisol peaks in the cortisol awakening response (CAR), occurring within 30-45 minutes of waking. This natural morning peak serves as a circadian anchor — it drives morning alertness and calibrates daytime energy. A secondary, smaller peak can occur in the late afternoon. Cortisol is lowest in the early morning hours (midnight to 3am). The problematic pattern in insomnia is premature cortisol rise around 3-4am, which causes early morning awakening."),
        ("How do I lower cortisol at night?",
         "Most effective interventions: consistent bedtime (prevents anticipatory HPA axis activation), magnesium glycinate (reduces cortisol-driven physiological hyperarousal via GABA support), scheduled worry time separate from bed, limiting news and stressful content after 8pm, warm bath or shower 1-2 hours before bed (passive body cooling activates parasympathetic nervous system), and diaphragmatic breathing for 5-10 minutes before sleep."),
        ("Does poor sleep raise cortisol?",
         "Yes — bidirectionally. Poor sleep elevates daytime cortisol, which then worsens the following night's sleep. Studies show a 37-45% elevation in next-day cortisol after a night of restricted sleep. Chronic sleep restriction creates a self-perpetuating cortisol-insomnia cycle. Breaking this cycle typically requires simultaneous improvement in sleep quality (via CBT-I or sleep hygiene) and stress management practices."),
    ],
    'deep-sleep-benefits.html': [
        ("What does deep sleep do for the body?",
         "Slow-wave (deep) sleep is the primary recovery phase. During this stage: growth hormone is released (70% of daily output), tissue repair and muscle protein synthesis occur, the immune system produces cytokines and T-cells, the glymphatic system flushes amyloid-beta and tau from the brain, blood pressure reaches its lowest point of the day, and hippocampal-cortical memory transfer occurs. Deprivation of even one night of deep sleep measurably impairs all of these functions."),
        ("How can I get more deep sleep?",
         "Deep sleep percentage is partly genetic but influenced by several modifiable factors. Sleep timing matters most — deep sleep is concentrated in the first half of the night. Going to bed earlier within your natural sleep window increases total deep sleep. Avoiding alcohol (which suppresses slow-wave sleep even when it helps you fall asleep initially), regular aerobic exercise (increases slow-wave sleep in the subsequent night), and consistent wake time all increase deep sleep. Cold bedroom temperature (65-68°F) supports slow-wave sleep quality."),
        ("How much deep sleep is normal?",
         "Adults average 15-25% of total sleep as slow-wave sleep — roughly 60-90 minutes in a 7-8 hour night. This percentage declines with age: adults over 60 may get only 5-10%. Deep sleep percentages below 10% in younger adults are associated with impaired cognitive function and immune response. The exact percentage varies significantly between individuals — what matters is adequate total sleep and consistent sleep timing."),
        ("What happens if you don't get enough deep sleep?",
         "Deep sleep deprivation produces: impaired physical recovery (elevated muscle soreness, slower healing), increased infection susceptibility (cytokine production is disrupted), cognitive impairment (memory consolidation requires slow-wave sleep), accumulation of amyloid-beta proteins (linked to Alzheimer's risk), elevated next-day cortisol, and increased appetite (ghrelin rises and leptin falls). These effects accumulate with chronic deprivation even when total sleep hours appear adequate."),
    ],
    'rem-sleep-benefits.html': [
        ("What does REM sleep do?",
         "REM (Rapid Eye Movement) sleep serves critical functions: emotional memory processing (replaying emotional experiences without stress neurochemicals, reducing emotional charge), memory integration (connecting new information with existing knowledge structures, enabling insight), creative problem-solving (the REM-associated neural pattern supports non-linear thinking), and regulatory functions for mood, empathy, and emotional reactivity. REM deprivation produces irritability, emotional dysregulation, and impaired social cognition."),
        ("How much REM sleep do you need?",
         "Adults average 20-25% of total sleep as REM — roughly 90-110 minutes in a 7-8 hour night. REM is concentrated in the last third of the night; cutting sleep by 1-2 hours eliminates disproportionate amounts of REM. The ideal REM amount is individual — what matters is waking without emotional dysregulation, irritability, or difficulty processing experiences. Consistently vivid or disturbing dreams can indicate REM rebound from prior deprivation or suppression."),
        ("What disrupts REM sleep?",
         "The strongest REM disruptors are: alcohol (suppresses REM in the first half of the night, causing REM rebound in the second half), many antidepressants (SSRIs, SNRIs), sedative medications (benzodiazepines), sleep deprivation (which produces REM rebound on recovery nights), and sleep apnea (which fragments REM through repeated arousals). These are also why people taking SSRIs or drinking regularly often report vivid, disturbing dreams when they stop — REM rebounds."),
        ("Can you get too much REM sleep?",
         "Unusually high REM percentages can indicate: REM rebound from prior deprivation, REM behavior disorder (acting out dreams — a risk factor for Parkinson's disease), or narcolepsy (which features abnormal direct-to-REM sleep onset). In healthy adults, very high REM percentages are uncommon and typically represent recovery from chronic deprivation. If REM behavior disorder symptoms are present (talking, moving during sleep), evaluation by a sleep physician is warranted."),
    ],
    'snoring-causes-fixes.html': [
        ("What causes snoring?",
         "Snoring occurs when the upper airway is partially obstructed, causing tissues to vibrate as air passes through. Common causes: airway anatomy (deviated septum, enlarged tonsils or adenoids, elongated uvula), airway muscle relaxation during sleep (especially during REM), obesity (fat deposits around the throat narrow the airway), sleeping position (supine sleeping promotes airway collapse), alcohol (relaxes upper airway muscles), nasal congestion (forces mouth breathing), and age (muscle tone decreases with age)."),
        ("How do I stop snoring immediately?",
         "Positional interventions work fastest: sleeping on your side (rather than your back) reduces snoring in 50-60% of positional snorers. Nasal strips or dilators reduce snoring from nasal congestion. Elevating the head of the bed 4-6 inches can reduce airway collapse. For mouth breathing, a chin strap or mouth tape keeps the mouth closed. These are management tools — they do not address underlying airway anatomy or sleep apnea."),
        ("When is snoring dangerous?",
         "Snoring combined with witnessed breathing pauses, gasping or choking sounds, excessive daytime sleepiness, morning headaches, or frequent nighttime urination indicates possible obstructive sleep apnea, which requires evaluation. Snoring with these symptoms is associated with significant cardiovascular risk — hypertension, arrhythmia, and stroke. Loud snoring in the absence of these symptoms (primary snoring) is less dangerous but still warrants evaluation if it affects bed partners."),
        ("Does weight loss stop snoring?",
         "For weight-related snoring, yes. Fat deposits in the neck area narrow the upper airway — a neck circumference above 17 inches in men and 15 inches in women is a risk factor for sleep apnea. Even 10% weight loss significantly reduces snoring severity and apnea index in overweight individuals. For anatomical snoring (deviated septum, elongated uvula), weight loss has less impact."),
    ],
    'wind-down-routine.html': [
        ("What is an effective bedtime routine for adults?",
         "An effective wind-down routine follows a consistent sequence starting 60-90 minutes before bed: dim lighting (eliminate overhead bright lights, use warm lamps), avoid screens or use amber-lens blue light glasses, reduce mental activation (stop work tasks, news, social media), perform a consistent transition activity (reading physical books, light stretching, journaling), and a brief physical transition (warm shower or bath 60-90 minutes before bed cools core temperature through vasodilation). Consistency matters more than specific activities."),
        ("How long should a bedtime routine be?",
         "30-60 minutes for adults is the evidence-supported window. The goal is physiological deactivation: cortisol begins declining, core body temperature starts dropping, and melatonin rises during this window. Too short (under 15 minutes) doesn't allow sufficient physiological deactivation. Too long or too structured can itself become anxiety-producing if sleep doesn't arrive precisely on schedule."),
        ("Does taking a bath before bed help sleep?",
         "Yes — but the timing matters. A warm bath or shower taken 60-90 minutes before bed raises peripheral skin temperature, causing heat dissipation that drops core body temperature. This core temperature drop signals the circadian clock that it's sleep time. The effect is a reduction in sleep onset latency of approximately 10-15 minutes on average. The bath temperature doesn't need to be very hot — warm water (40-42°C) is sufficient."),
        ("Should you exercise as part of your bedtime routine?",
         "Vigorous exercise within 2 hours of bed elevates core temperature and sympathetic arousal, typically delaying sleep onset. Light stretching or yoga in the 30-minute pre-bed window is beneficial — it activates the parasympathetic nervous system and addresses muscle tension without raising core temperature. The optimal time for sleep-supportive exercise (regular moderate aerobic activity) is morning or afternoon, not evening."),
    ],
    'sleep-quality-vs-quantity.html': [
        ("Is sleep quality or quantity more important?",
         "Both matter and cannot be fully separated. 8 hours of fragmented, light sleep produces worse outcomes than 7 hours of consolidated, deep sleep. However, below approximately 6 hours per night, quantity becomes the dominant factor — no quality improvement compensates for severe sleep restriction. The practical hierarchy: ensure adequate quantity (7-8 hours) first, then optimize quality through timing, environment, and sleep hygiene."),
        ("How do you measure sleep quality?",
         "Objective measures: sleep efficiency (time asleep/time in bed, healthy >85%), sleep onset latency (time to fall asleep, healthy <20 minutes), number of awakenings, and sleep stage distribution. Consumer sleep trackers provide estimates of these metrics with 70-80% accuracy compared to lab polysomnography. Subjective measure: the most valid single question is 'How rested do you feel upon waking?' — consistently rating below 6/10 indicates a quality problem."),
        ("What reduces sleep quality?",
         "The main reducers of sleep quality (as distinct from quantity): alcohol (suppresses slow-wave and REM sleep), sleep apnea (fragments all stages through repeated arousals), pain (causes arousals at sleep cycle transitions), inconsistent sleep timing (reduces circadian amplitude), light and noise in the sleep environment, and hyperarousal from anxiety or stress (prevents deep sleep stages). Most of these are modifiable."),
        ("Can you feel rested with 6 hours of sleep?",
         "Most adults cannot, despite feeling adapted. Cognitive performance studies consistently show measurable impairment at 6 hours per night that worsens over days without full subjective awareness of the impairment. Genetic short sleepers (who genuinely function optimally on 6 hours) exist but constitute under 5% of the population. The subjective sense of adaptation to sleep restriction is documented in research — people rate themselves as 'fine' while their reaction times and cognitive scores continue to decline."),
    ],
    'ultimate-sleep-guide.html': [
        ("What is the most important factor for good sleep?",
         "Consistency of sleep timing — specifically wake time, maintained 7 days a week — has the largest and most consistent effect across all research. It anchors the circadian clock, regulates adenosine accumulation, and makes everything else (falling asleep, staying asleep, feeling rested) easier. All other sleep hygiene factors are additive on top of this foundation."),
        ("What are the best evidence-based sleep tips?",
         "In order of evidence strength: (1) Consistent wake time daily; (2) Bedroom temperature 65-68°F; (3) Total darkness (blackout curtains or sleep mask); (4) No caffeine after 2pm; (5) No alcohol within 4 hours of bed; (6) No screens 90 minutes before bed or amber-lens blue light glasses; (7) Exercise regularly (morning/afternoon preferred); (8) Reserve the bed for sleep only (stimulus control). These eight habits address the most consistently studied sleep factors."),
        ("How do you build a sleep schedule that actually works?",
         "Start with a fixed wake time that fits your life. Set it. Use an alarm every day for 3 weeks regardless of when you fell asleep. After wake time is anchored, count back 7.5 hours (5 complete 90-minute cycles) — that is your target sleep time. Begin a 30-60 minute wind-down routine at that point. The schedule works when you follow it even on weekends, even after bad nights, even when you feel tired. Exceptions reset the clock and restart the adaptation period."),
        ("What is sleep hygiene and does it actually work?",
         "Sleep hygiene is the set of behavioral and environmental practices that support sleep. For chronic insomnia, sleep hygiene alone has modest effectiveness — typically reducing sleep onset latency by 15-20 minutes and improving sleep efficiency by 10-15%. It works best as a foundation for CBT-I (the first-line treatment for chronic insomnia). For otherwise healthy people who sleep poorly due to environmental or behavioral factors, sleep hygiene alone is often sufficient."),
    ],
    'sleep-athletic-performance.html': [
        ("How does sleep affect athletic performance?",
         "Sleep directly affects athletic performance through several pathways: growth hormone release during slow-wave sleep drives muscle protein synthesis and tissue repair; REM sleep consolidates motor learning from training; sleep deprivation reduces maximal strength by 10-30%, endurance by 10-20%, reaction time, and decision-making speed. Cognitive tasks that require quick decisions (basketball, tennis, martial arts) are particularly impaired by sleep loss."),
        ("How much sleep do athletes need?",
         "Elite athletes require more sleep than the general adult recommendation. Studies show that sleeping 10 hours per night (or extending sleep by 1-2 hours) improves athletic performance metrics — sprint times, shooting accuracy, reaction time — compared to the athletes' baseline. The general recommendation for competing athletes is 9-10 hours, with daytime naps to supplement. Sleep is the most underutilized performance enhancer in sport."),
        ("Should athletes nap before a competition?",
         "A 20-minute power nap taken 6+ hours before competition improves reaction time, alertness, and cognitive performance without causing sleep inertia. Athletes who are sleep-restricted should prioritize this. A longer nap (60-90 minutes) provides more restoration but risks sleep inertia at wake time — allow 60 minutes of recovery time before competition. Napping within 4 hours of evening competition can fragment nighttime sleep."),
        ("Does sleep improve muscle recovery?",
         "Yes. 70% of daily growth hormone output occurs during slow-wave sleep. Protein synthesis rates are elevated overnight. Inflammatory markers (interleukin-6, TNF-alpha) that spike after training are resolved during sleep. The practical implication: prioritizing sleep after intense training sessions produces faster recovery than nutritional strategies alone. Consistently poor sleep results in elevated cortisol and impaired anabolic signaling regardless of nutrition and training quality."),
    ],
    'teen-sleep-guide.html': [
        ("Why do teenagers need so much sleep?",
         "Adolescents require 8-10 hours of sleep because the brain is undergoing significant development during this period. The prefrontal cortex (responsible for decision-making, impulse control, and emotional regulation) is actively pruned and myelinated throughout adolescence. Sleep, particularly slow-wave and REM sleep, is when this neural remodeling occurs. Adolescents also have higher adenosine clearance requirements due to greater waking brain activity."),
        ("Why can't teenagers fall asleep at night?",
         "Puberty causes a biological shift in the circadian clock — the sleep phase is delayed by 1.5-2 hours. This is not a lifestyle choice or lack of discipline: melatonin onset occurs 2 hours later in adolescents than in children or adults. Teenagers physically cannot fall asleep before 11pm in most cases. School start times before 8:30am create a structural sleep deprivation problem that the American Academy of Pediatrics has formally addressed with a policy statement advocating for later start times."),
        ("How can I help my teenager sleep better?",
         "Most effective interventions: consistent sleep and wake times (including weekends, within 1 hour variance), no devices in the bedroom at night (phone chargers in the hallway), no caffeine after 4pm, gradually darkening the bedroom 30-60 minutes before the target sleep time, and — if possible — advocating for school start times no earlier than 8:30am. Melatonin at low dose (0.5mg) at the desired bedtime can help shift the delayed phase over 1-2 weeks."),
        ("What happens to teens who don't get enough sleep?",
         "Adolescent sleep deprivation has serious documented consequences: impaired memory consolidation (affecting academic performance), increased depression and anxiety risk, 3x greater risk of drowsy driving crashes, impaired prefrontal function (increased impulsivity, risk-taking, and emotional reactivity), and metabolic effects including insulin resistance. The CDC reports that 72% of US high school students are chronically sleep-deprived — a public health crisis."),
    ],
    'morning-habits-sleep.html': [
        ("What morning habits improve sleep the following night?",
         "Morning light exposure is the most powerful morning habit for sleep. Bright light (outdoor sun or 10,000-lux lamp) within 30 minutes of waking sets the circadian clock and determines when melatonin will rise that evening. Morning exercise (any moderate aerobic activity) deepens slow-wave sleep the following night. Consistent wake time — even after a poor night — maintains adenosine regulation. Avoiding caffeine in the first 90 minutes of waking (allowing cortisol to peak naturally before supplementing with caffeine) produces more stable energy without afternoon crashes."),
        ("Does morning exercise help sleep?",
         "Yes — morning aerobic exercise is associated with improved sleep quality, deeper slow-wave sleep, and fewer nighttime awakenings compared to afternoon or evening exercise. Outdoor morning exercise doubles the benefit by combining physical activity with bright light exposure. Even 20-30 minutes of brisk walking improves sleep quality in sedentary adults within 4-6 weeks. The mechanism involves adenosine, body temperature rhythms, and circadian zeitgeber reinforcement."),
        ("Why shouldn't you hit snooze in the morning?",
         "Snoozing creates fragmented micro-sleep that produces sleep inertia (grogginess) without providing restorative slow-wave or REM sleep. Each 9-minute snooze cycle is too short to enter meaningful sleep stages. More importantly, snoozing tells your brain that the alarm time is not real, gradually delaying your true wake time and destabilizing circadian rhythm. Setting one alarm at the latest acceptable wake time is more effective than multiple snooze cycles."),
        ("Is morning sunlight really important for sleep?",
         "Yes — it is the most powerful circadian synchronizer available. The suprachiasmatic nucleus (circadian master clock) receives direct light input from the retina. Morning sunlight within 30-60 minutes of waking suppresses residual melatonin, triggers the cortisol awakening response, and sets the 14-16 hour timer for that evening's melatonin onset. People who get bright morning light consistently fall asleep faster and sleep more deeply than those who don't."),
    ],
    'sleep-and-weight-loss.html': [
        ("Does sleep affect weight loss?",
         "Yes, significantly. Sleep deprivation increases ghrelin (appetite hormone) and reduces leptin (satiety hormone), producing a 24% increase in hunger and strong cravings for high-calorie foods. Sleep-restricted dieters lose 55% less fat and 60% more muscle mass than adequate-sleep dieters on the same calorie deficit. Poor sleep impairs insulin sensitivity, increases cortisol (which promotes fat storage), and reduces the metabolic rate. Sleep is not optional for successful fat loss."),
        ("How much sleep do you need to lose weight?",
         "7-8 hours per night is associated with optimal fat loss outcomes when combined with caloric deficit. Studies specifically comparing 5.5 hours versus 8.5 hours of sleep during a caloric deficit found that the 5.5-hour group lost 70% of their weight loss from muscle, while the 8.5-hour group lost 80% from fat. The difference in hormonal environment (insulin, cortisol, ghrelin, leptin) between sleep-deprived and well-rested dieters explains this divergence."),
        ("Why do you gain weight when you don't sleep?",
         "Multiple mechanisms operate simultaneously: ghrelin elevation (increases appetite by 24%), leptin reduction (impairs satiety signaling), cortisol elevation (promotes visceral fat storage and muscle breakdown), insulin resistance (reduces glucose uptake into muscle, increases fat storage), reduced energy for physical activity, and impaired willpower for dietary choices. These hormonal shifts accumulate over days of sleep restriction even when caloric intake is held constant."),
        ("Does sleeping more help you lose weight?",
         "Restoring adequate sleep from a sleep-deprived baseline helps. Studies on habitually short sleepers (under 6 hours) who extended sleep to 7-8 hours show reduced appetite, lower cortisol, improved insulin sensitivity, and modest weight loss without intentional dietary changes. However, sleeping beyond 8-9 hours does not produce additional weight loss benefit and is associated with other health risks when it represents excessive sleep."),
    ],
    'sleep-and-alzheimers.html': [
        ("Does poor sleep cause Alzheimer's disease?",
         "Poor sleep does not definitively cause Alzheimer's, but there is a strong bidirectional relationship. Sleep deprivation impairs the glymphatic system's clearance of amyloid-beta and tau proteins — the proteins that accumulate in Alzheimer's disease. Even one night of sleep deprivation increases amyloid-beta in the cerebrospinal fluid by 25-30%. Chronic sleep disruption is consistently associated with higher Alzheimer's risk in longitudinal studies. Conversely, early Alzheimer's disrupts sleep — the two accelerate each other."),
        ("Does sleeping less than 6 hours increase Alzheimer's risk?",
         "Yes, based on multiple longitudinal studies. A large study published in Nature Communications found that consistently sleeping 6 hours or fewer at age 50-60 was associated with a 30% increased dementia risk over the following 25 years. This persisted after controlling for other dementia risk factors. The mechanism likely involves impaired glymphatic clearance of amyloid-beta during the missing slow-wave sleep."),
        ("How does sleep protect the brain from Alzheimer's?",
         "During sleep — particularly slow-wave sleep — the brain's glymphatic system operates at 10x its waking capacity, flushing cerebrospinal fluid through brain tissue and clearing metabolic waste products including amyloid-beta and tau. These are the same proteins that aggregate into the plaques and tangles of Alzheimer's disease. Regular, adequate slow-wave sleep appears to be one of the brain's primary protective mechanisms against the protein accumulation that drives Alzheimer's pathology."),
        ("What sleep habits reduce Alzheimer's risk?",
         "Based on current evidence: sleep 7-8 hours per night consistently; prioritize slow-wave sleep (avoid alcohol, maintain cool bedroom, consistent sleep timing); evaluate for and treat sleep apnea (untreated OSA accelerates amyloid-beta accumulation); maintain regular physical activity (increases slow-wave sleep and glymphatic efficiency); and protect sleep continuity (fragmented sleep impairs glymphatic clearance even when total hours are adequate)."),
    ],
    'sleep-heart-health.html': [
        ("How does sleep affect the heart?",
         "Sleep is a critical recovery period for cardiovascular function. Blood pressure drops 10-20% during healthy sleep (dipping), giving the heart and arteries restorative recovery. Poor sleep — especially sleep apnea, short sleep duration, and fragmented sleep — is associated with hypertension, atrial fibrillation, coronary artery disease, and increased risk of heart attack and stroke. Adults sleeping under 6 hours have 20% higher cardiovascular mortality than those sleeping 7-8 hours."),
        ("Can sleep apnea damage the heart?",
         "Yes. Untreated obstructive sleep apnea repeatedly drops blood oxygen saturation, triggers sympathetic nervous system activation, and spikes blood pressure with each apnea event — sometimes hundreds of times per night. This nightly stress produces: hypertension (60% of OSA patients have it), atrial fibrillation (2-4x higher risk), left ventricular hypertrophy, and 2-3x higher risk of heart attack and stroke. CPAP treatment significantly reduces cardiovascular risk in moderate-to-severe OSA."),
        ("Does poor sleep raise blood pressure?",
         "Yes. A single night of sleep restriction elevates next-day blood pressure by 3-5 mmHg on average. Chronic short sleep (under 6 hours) is associated with a 37% increased hypertension risk. The mechanism involves sustained sympathetic nervous system activation, elevated cortisol, and impaired nighttime blood pressure dipping. Non-dipping blood pressure (failure to reduce by 10%+ during sleep) is an independent cardiovascular risk factor."),
        ("What is the best sleeping position for heart health?",
         "Left side sleeping is generally recommended for people with heart conditions, as it may facilitate cardiac output and reduce the workload on the heart. For sleep apnea — a major cardiovascular risk factor — any position except supine (on the back) reduces apnea severity by 30-50%. The cardiovascular benefit of positional therapy for OSA outweighs any specific preference for left vs. right side."),
    ],
    'bedroom-temperature-sleep.html': [
        ("What temperature should your bedroom be for sleep?",
         "The optimal bedroom temperature for most adults is 65-68°F (18-20°C). Core body temperature must drop 1-2°F to initiate and maintain sleep — an environment that is too warm prevents this thermoregulatory drop. Individual variation exists: some sleep best at 63°F, others at 70°F. If you wake at night sweating or kicking off covers, your room is too warm; if you cannot fall asleep and feel restless, consider that your room may also be too warm, even if it doesn't feel excessively hot."),
        ("Does a hot shower before bed help sleep?",
         "Yes — when timed correctly. A warm shower (not ice cold) taken 60-90 minutes before bed raises peripheral skin temperature, causing vasodilation that transfers body heat away from the core. This produces a core body temperature drop that mimics the natural circadian temperature decline associated with sleep onset. Studies show it reduces sleep onset latency by 10-15 minutes on average. The effect is lost if the shower is taken immediately before bed."),
        ("Do cooling mattress pads actually help sleep?",
         "For hot sleepers, yes. Active cooling mattress pads (water-circulating systems) reduce skin temperature by 2-4°F, significantly reducing nighttime awakenings from heat. Passive cooling pads (gel, phase-change materials) provide moderate improvement for mild warmth but have limited capacity for people who consistently sleep hot. Studies show temperature-regulated sleep produces more slow-wave sleep and fewer nighttime awakenings in temperature-sensitive sleepers."),
        ("Is it bad to sleep in a cold room?",
         "No — sleeping in a cool-to-cold room (60-68°F) generally improves sleep quality. There is no evidence that cool room temperatures harm sleep health. The exception is very cold rooms (below 60°F) without adequate blankets, which can prevent the body from maintaining necessary core temperature for restorative sleep. The relationship between room temperature and sleep quality is U-shaped — too warm and too cold are both suboptimal, with the sweet spot around 65-68°F."),
    ],
    'sleep-depression.html': [
        ("How does sleep affect depression?",
         "Sleep and depression have a strong bidirectional relationship. Depression causes sleep disruption in 90% of cases — typically insomnia (difficulty falling or staying asleep) or hypersomnia (excessive sleep). Conversely, chronic insomnia is a major risk factor for developing depression, with odds ratios of 2-3x. Sleep deprivation worsens depression severity; improving sleep quality is a therapeutic goal in depression treatment and significantly reduces symptom burden."),
        ("Why do depressed people sleep so much?",
         "Hypersomnia in depression likely reflects the brain's protective response to the neuroinflammation and neurotransmitter dysregulation that characterize depression — sleep is a primary repair period. However, excessive sleep (over 9 hours) paradoxically worsens depression symptoms and maintains the circadian disruption that perpetuates depressive episodes. This is why most depression treatment protocols include consistent wake times rather than unlimited sleep."),
        ("Can fixing sleep cure depression?",
         "Sleep improvement alone does not cure depression, but it consistently reduces severity. CBT-I delivered alongside depression treatment produces better antidepressant outcomes than antidepressants alone. Sleep deprivation therapy (paradoxically, staying awake for 36 hours) can produce rapid but temporary antidepressant effects — used in clinical settings. Normalizing sleep architecture (particularly REM patterns, which are abnormal in depression) appears to be a mechanism through which both medications and therapy exert antidepressant effects."),
        ("What sleep problems are common in depression?",
         "The most common patterns: difficulty falling asleep (initial insomnia), waking in the early morning and being unable to return to sleep (terminal insomnia), excessive daytime sleepiness, non-restorative sleep (feeling unrefreshed despite adequate hours), and abnormal REM sleep (earlier REM onset, higher REM density, and disturbing dream content). Early morning awakening — waking 2-3 hours before desired, usually 4-5am, with a shift to negative mood — is particularly characteristic of major depression."),
    ],
    'sleep-and-diabetes.html': [
        ("How does sleep affect blood sugar?",
         "Sleep deprivation reduces insulin sensitivity by 20-30% in healthy adults after just one week of restricted sleep (6 hours/night). The mechanism involves elevated cortisol (which promotes glucose release) and reduced glucose transporter activity. In people with type 2 diabetes, poor sleep significantly worsens glycemic control — HbA1c levels are consistently higher in those sleeping under 6 hours. Sleep is a modifiable variable in diabetes management that is frequently overlooked."),
        ("Can poor sleep cause diabetes?",
         "Chronic sleep restriction is an independent risk factor for type 2 diabetes. People sleeping 5-6 hours per night have a 28% higher diabetes risk than those sleeping 7-8 hours (meta-analysis of 10 prospective studies, 18+ years follow-up). The mechanism involves impaired insulin secretion, reduced insulin sensitivity, and increased appetite for carbohydrates — together creating a metabolic environment that promotes insulin resistance over time."),
        ("Why do diabetics have trouble sleeping?",
         "People with type 2 diabetes experience sleep disruption through multiple mechanisms: nocturia (frequent nighttime urination from blood sugar spikes), peripheral neuropathy causing pain or restless legs that disrupt sleep, obstructive sleep apnea (3x more common in type 2 diabetes), hypoglycemia events that cause awakening, and the metabolic effects of chronic hyperglycemia on sleep architecture. Treating sleep disorders in diabetic patients directly improves glycemic control."),
        ("What is the connection between sleep apnea and diabetes?",
         "Obstructive sleep apnea and type 2 diabetes co-occur at rates far above chance — approximately 58-70% of type 2 diabetics have OSA. The relationship is bidirectional: intermittent hypoxia from OSA impairs insulin signaling, and obesity (a driver of both conditions) worsens both simultaneously. CPAP treatment for OSA in diabetics produces modest but meaningful improvements in insulin sensitivity and HbA1c, particularly in those with severe OSA."),
    ],
}


def make_schema(faqs):
    entities = []
    for q, a in faqs:
        entities.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a}
        })
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities
    }
    return '<script type="application/ld+json">\n' + json.dumps(schema, indent=2) + '\n</script>'


updated = 0
skipped = 0
for fname, faqs in FAQS.items():
    if not faqs:
        continue
    p = Path(f'posts/{fname}')
    if not p.exists():
        print(f'MISSING: {fname}')
        continue
    html = p.read_text(encoding='utf-8')
    if 'application/ld+json' in html:
        print(f'SKIP (has schema): {fname}')
        skipped += 1
        continue

    schema_block = make_schema(faqs)
    if '</head>' in html:
        html = html.replace('</head>', schema_block + '\n</head>', 1)
        p.write_text(html, encoding='utf-8')
        print(f'OK: {fname} ({len(faqs)} Q&As)')
        updated += 1
    else:
        print(f'NO HEAD TAG: {fname}')

print(f'\nUpdated: {updated}  Skipped: {skipped}')
