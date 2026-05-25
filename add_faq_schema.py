"""
Inject JSON-LD FAQ schema into educational posts.
Skips posts that already have schema markup.
"""
import json
from pathlib import Path

FAQS = {
    'sleep-hygiene-checklist.html': [
        ("What is sleep hygiene?",
         "Sleep hygiene refers to the set of behavioral and environmental practices that support consistent, high-quality sleep. The most evidence-backed habits include a fixed wake time 7 days a week, avoiding caffeine after 2pm, blocking light exposure in the 90 minutes before bed, and keeping bedroom temperature between 65-68°F."),
        ("What is the single most important sleep hygiene habit?",
         "A consistent wake time, maintained even on weekends, is the most impactful sleep hygiene behavior. It anchors your circadian rhythm, regulates adenosine buildup, and makes falling asleep easier within 2-3 weeks of consistent practice."),
        ("How long does it take for sleep hygiene to work?",
         "Most people notice improvement in sleep onset latency within 1-2 weeks of consistent practice. Full circadian stabilization — where falling and staying asleep becomes effortless — typically takes 3-4 weeks of unbroken routine."),
        ("Does screen time before bed really affect sleep?",
         "Yes. The blue-spectrum light from screens suppresses melatonin production, delaying sleep onset by 30-90 minutes. Either stop using screens 90 minutes before bed, or use amber-lens blue light blocking glasses, which cut the 480nm wavelength that drives melatonin suppression."),
    ],
    'cbt-i-guide.html': [
        ("What is CBT-I and how does it work?",
         "Cognitive Behavioral Therapy for Insomnia (CBT-I) is a structured program that addresses the behavioral and cognitive patterns that perpetuate chronic insomnia. Core components include sleep restriction therapy (temporarily limiting time in bed to build sleep drive), stimulus control (using the bed only for sleep), and cognitive restructuring (correcting beliefs about sleep that cause hyperarousal). It is the first-line treatment recommended by the American Academy of Sleep Medicine — above sleep medications."),
        ("Is CBT-I better than sleeping pills?",
         "Yes, according to clinical evidence. CBT-I produces superior long-term outcomes compared to pharmacological treatment. Sleep medications provide faster initial relief but cause tolerance, dependency, and rebound insomnia. CBT-I produces durable improvements that persist years after treatment ends. The American College of Physicians recommends CBT-I as the first-line treatment for chronic insomnia."),
        ("How long does CBT-I take to work?",
         "Most people see significant improvement in 4-8 weeks. Sleep restriction therapy, the most powerful component, often produces noticeable change within the first 1-2 weeks — though sleep initially feels worse before improving. Full benefit typically requires 6-8 weeks of consistent practice."),
        ("Can I do CBT-I on my own without a therapist?",
         "Yes. Self-guided CBT-I using workbooks or digital programs produces outcomes comparable to therapist-delivered CBT-I in mild-to-moderate insomnia. The most important component — keeping a sleep diary and applying sleep restriction — can be done independently. Digital programs like Sleepio and the Insomnia Coach app (free, from the VA) provide structured guidance."),
    ],
    'sleep-apnea-warning-signs.html': [
        ("What are the main warning signs of sleep apnea?",
         "The primary warning signs are loud snoring with witnessed breathing pauses, waking with a dry mouth or headache, excessive daytime sleepiness despite adequate time in bed, waking frequently to urinate at night, and difficulty concentrating. Not everyone with sleep apnea snores — especially women and those with central sleep apnea."),
        ("Can you have sleep apnea without snoring?",
         "Yes. Approximately 20-30% of people with sleep apnea do not snore significantly, particularly women, children, and people with central sleep apnea (where the brain fails to signal breathing properly). Excessive daytime sleepiness, morning headaches, and frequent nighttime awakenings are the most common non-snoring indicators."),
        ("How is sleep apnea diagnosed?",
         "Sleep apnea is diagnosed through a sleep study (polysomnography) or a home sleep apnea test (HSAT). Home tests are now widely prescribed for uncomplicated cases. They measure oxygen saturation, airflow, and respiratory effort overnight. An Apnea-Hypopnea Index (AHI) of 5-14 is mild, 15-29 is moderate, 30+ is severe."),
        ("What is the first step if I suspect I have sleep apnea?",
         "Track your symptoms — daytime sleepiness, morning headaches, snoring reports from a partner — and bring them to your primary care physician. They can order a home sleep test, which is covered by most insurance. Do not self-treat with OTC devices without a diagnosis, as untreated sleep apnea carries serious cardiovascular risks."),
    ],
    'reset-sleep-schedule.html': [
        ("How do I fix a completely reversed sleep schedule?",
         "The fastest method is light-anchored phase advance: wake at your target time regardless of how little you slept, expose yourself to bright light (10,000 lux or outdoor sunlight) within 30 minutes of waking, take 0.3-0.5mg melatonin 30 minutes before your target bedtime, and maintain the schedule for at least 7 consecutive days. The first 2-3 days are difficult — the sleep drive built from restricting sleep accelerates the reset."),
        ("How long does it take to reset a sleep schedule?",
         "Minor disruptions (1-2 hours off) correct within 3-5 days. Moderate disruptions (3-4 hours off, such as returning from jet lag or rotating shifts) take 7-10 days. A fully reversed schedule (day-night flip) takes 2-3 weeks with active intervention, or longer without it."),
        ("Does melatonin help reset sleep schedule?",
         "Yes, at low doses. Melatonin at 0.3-0.5mg taken 30 minutes before your target bedtime signals circadian phase shift. Higher doses (5-10mg) provide sedation but do not produce a stronger phase-shifting effect — they cause next-day grogginess and can downregulate natural melatonin production."),
        ("Can you reset your sleep schedule in one day?",
         "No. The circadian clock shifts at a maximum rate of approximately 1-2 hours per day, even with optimal light and melatonin intervention. Attempting to force a full shift overnight creates sleep deprivation without fixing the underlying clock timing. A gradual 7-14 day approach produces durable results."),
    ],
    'jet-lag-guide.html': [
        ("How long does jet lag last?",
         "Jet lag duration scales with time zone distance: roughly 1 day of recovery per time zone crossed. Eastward travel is harder — the circadian clock advances more slowly than it delays. A 6-hour eastward crossing typically takes 5-7 days without intervention; active measures (light therapy, timed melatonin) can cut this to 3-4 days."),
        ("Does melatonin help with jet lag?",
         "Yes, when used correctly. For eastward travel, 0.3-0.5mg taken at the destination bedtime for 3-4 nights accelerates clock resynchronization. For westward travel, melatonin is less necessary — the clock delays naturally. Key: keep the dose low (0.5mg maximum) to avoid grogginess that worsens daytime adaptation."),
        ("What is the fastest way to recover from jet lag?",
         "The most effective combination is: (1) light therapy at destination wake time to advance or delay the clock, (2) 0.5mg melatonin at destination bedtime, (3) staying awake until local bedtime on arrival day, and (4) avoiding naps longer than 20 minutes. Light is the most powerful zeitgeber — a 10,000-lux lamp for 20-30 minutes each morning accelerates adaptation faster than melatonin alone."),
        ("Should I adjust to the new time zone immediately upon arrival?",
         "Yes for trips lasting 4+ days. Immediately adopt the local schedule — meals, light exposure, sleep timing — rather than maintaining home time. For trips shorter than 3 days, maintaining your home schedule may be more practical and reduces adaptation stress."),
    ],
    'night-shift-optimization.html': [
        ("How do night shift workers get enough sleep?",
         "The key interventions are: complete blackout for the sleep environment (blackout curtains + sleep mask), total noise elimination (earplugs or white noise machine), communicating a do-not-disturb period to household members, and anchoring sleep timing consistently — sleeping at the same time each day even on days off. The sleep environment matters more for shift workers than any supplement."),
        ("What is the best sleep schedule for night shift?",
         "The most sustainable approach is a split sleep schedule: 4-5 hours immediately after the shift, followed by a 2-3 hour nap before the next shift. This aligns the longer sleep block with the afternoon cortisol dip and reduces the circadian misalignment penalty. A single 7-8 hour block mid-day works if the environment is sufficiently dark and quiet."),
        ("Does melatonin help night shift workers sleep during the day?",
         "Yes. 0.5-1mg melatonin taken 30 minutes before daytime sleep signals the brain that it's time to sleep despite daylight. Keep the dose low — higher doses cause grogginess that spills into the next shift. Blackout curtains to eliminate light intrusion are more important than melatonin, but both together produce the strongest effect."),
        ("How do night shift workers protect their health long-term?",
         "Vitamin D supplementation (2000-4000 IU daily) compensates for sunlight deprivation. Timed meals — eating at consistent times aligned with the work schedule — help synchronize peripheral organ clocks. Annual cardiovascular screening is warranted given the documented metabolic risks of chronic shift work."),
    ],
    'natural-sleep-aids.html': [
        ("What are the most evidence-based natural sleep aids?",
         "The strongest evidence supports: magnesium glycinate (200-400mg) for sleep quality via GABA pathway support, low-dose melatonin (0.3-0.5mg) for sleep onset and circadian timing, and L-theanine (200mg) for reducing anxiety-related sleep disruption. Valerian root has mixed evidence — some studies show benefit after 2+ weeks. Most herbal sleep supplements lack rigorous clinical evidence."),
        ("Is melatonin safe for long-term use?",
         "Short-term use (1-3 months) at low doses (0.3-0.5mg) is considered safe. Long-term daily use at pharmacological doses (5-10mg) has not been well-studied and may downregulate the brain's natural melatonin production. Melatonin is most appropriate for circadian timing issues (jet lag, shift work, delayed sleep phase) rather than maintenance insomnia."),
        ("What is the best dose of melatonin for sleep?",
         "The physiologically relevant dose is 0.3-0.5mg — this matches natural peak melatonin levels. The 5-10mg doses sold in most US pharmacies are 10-30x the effective dose and primarily cause sedation rather than circadian signal. Use 0.5mg taken 30-60 minutes before target bedtime."),
        ("Does magnesium help with sleep?",
         "Yes, with the right form and dose. Magnesium glycinate at 200-400mg taken before bed has the best evidence and absorption profile. It activates GABA receptors, reducing the physiological arousal that delays sleep onset. Magnesium oxide (the most common and cheapest form) is poorly absorbed. Look for glycinate, malate, or threonate forms."),
    ],
    'mattress-buying-guide.html': [
        ("What mattress firmness is best for sleep?",
         "For most adults, medium-firm (5-6 on a 1-10 scale) provides the best balance of pressure relief and spinal support. Side sleepers who weigh under 130 lbs do better with medium (4-5). Back and stomach sleepers above 230 lbs tend to need firm (7-8). The most reliable way to find your ideal firmness is a mattress with a trial period of 90+ nights."),
        ("How often should you replace a mattress?",
         "Most quality mattresses last 7-10 years. Signs it needs replacing: you wake with more pain than when you went to bed, visible sagging of more than 1 inch, and you sleep better in hotels or on other surfaces. Memory foam and latex tend to outlast innerspring. Check the mattress warranty — it reflects manufacturer confidence in durability."),
        ("What is the difference between memory foam and hybrid mattresses?",
         "Memory foam contours closely and excels at pressure relief and motion isolation, but retains heat and has a slow, sinking response that some find claustrophobic. Hybrid mattresses combine a pocketed coil base (for support, airflow, and bounce) with a comfort foam layer (for pressure relief). Hybrids sleep cooler and are easier to move on; memory foam provides better isolation for motion-sensitive couples."),
        ("Is an expensive mattress worth it?",
         "Diminishing returns set in around $1,200-1,500 for a queen. The most important features — pocketed coils, 2-4 inches of quality comfort foam, durable edge support — are available at this price point. Mattresses above $2,500 primarily offer branding and materials premium without proportional sleep improvement. A mattress with a 100+ night trial is worth more than a higher price tag."),
    ],
    'sleep-medications-truth.html': [
        ("Are sleeping pills safe to take long-term?",
         "Most prescription sleep medications are not recommended for long-term use. Benzodiazepines and Z-drugs (zolpidem, eszopiclone) cause tolerance, dependency, and rebound insomnia within 2-4 weeks. Older antihistamine-based OTC pills (diphenhydramine) cause tolerance within days and have anticholinergic effects that worsen cognition in older adults. CBT-I is the recommended first-line treatment for chronic insomnia."),
        ("What sleep medication is least habit-forming?",
         "Among prescription options, low-dose doxepin (Silenor) and suvorexant (Belsomra) have lower dependency risk than benzodiazepines. Low-dose trazodone is widely used off-label with good tolerability. Melatonin receptor agonists (ramelteon) are non-addictive and appropriate for circadian timing issues. Discuss options with a sleep physician rather than defaulting to the most-advertised option."),
        ("Why do sleeping pills stop working?",
         "Tolerance develops because the brain downregulates the receptors that sleeping pills target. GABA-A receptor sensitivity decreases with benzodiazepine and Z-drug use within 1-4 weeks, requiring higher doses for the same effect. Stopping after tolerance creates rebound insomnia worse than the original problem — the main driver of long-term dependency."),
        ("What can I take instead of sleeping pills?",
         "CBT-I is the evidence-based first-line alternative. For supplements, magnesium glycinate (200-400mg) has the best evidence among non-prescription options. Low-dose melatonin (0.3mg) addresses circadian timing. L-theanine reduces anxiety-driven sleep disruption. These are adjuncts — CBT-I addresses the behavioral patterns that perpetuate insomnia while supplements address physiology."),
    ],
    'power-nap-science.html': [
        ("How long should a power nap be?",
         "10-20 minutes is the optimal power nap duration. This window captures Stage 1 and early Stage 2 sleep — which restore alertness and motor performance — without entering slow-wave sleep. Entering slow-wave sleep (which happens around 25-30 minutes) causes sleep inertia: the groggy, disoriented feeling that persists for 30-60 minutes after waking."),
        ("What is a NASA nap?",
         "NASA researchers found that a 26-minute nap improved pilot performance by 34% and alertness by 100%. The precise duration is less important than staying under 30 minutes — the 26-minute figure comes from accounting for 5-6 minutes of sleep onset latency, giving approximately 20 minutes of actual sleep."),
        ("Does napping affect nighttime sleep?",
         "Naps taken before 3pm and limited to 20 minutes have minimal impact on nighttime sleep for most adults. Naps taken after 3pm or longer than 30 minutes reduce sleep drive enough to delay nighttime sleep onset. People with insomnia should avoid naps entirely, as daytime sleep reduces the adenosine buildup that drives nighttime sleepiness."),
        ("Is it better to nap or drink coffee when tired?",
         "A nap cup of coffee before a 20-minute nap — drinking coffee immediately before napping, then waking when caffeine kicks in — combines both benefits. Caffeine takes 20-30 minutes to reach peak plasma concentration, meaning it activates precisely when you wake from the nap. This produces greater alertness than either intervention alone."),
    ],
    'sleep-chronic-pain.html': [
        ("How does chronic pain affect sleep?",
         "Chronic pain disrupts sleep through two mechanisms: pain-triggered arousals that fragment sleep architecture, and the stress response to ongoing pain that elevates nocturnal cortisol and suppresses slow-wave sleep. This creates a bidirectional cycle — pain disrupts sleep, and sleep deprivation lowers the pain threshold, increasing pain sensitivity the following day."),
        ("What sleeping position is best for chronic pain?",
         "Side sleeping with proper support is generally best for most pain conditions. For back pain: side sleeping with a pillow between the knees reduces lumbar rotation stress. For hip pain: a body pillow prevents the top leg from dropping forward. For shoulder pain: lying on the non-affected shoulder with arm extended slightly reduces impingement. Stomach sleeping is the worst position for spinal alignment regardless of pain type."),
        ("Does a new mattress help with chronic pain?",
         "A medium-firm mattress reduces chronic low back pain better than a firm mattress, according to a large Spanish randomized controlled trial. However, if a full mattress replacement isn't feasible, a 2-3 inch memory foam or latex topper provides significant pressure relief at the hip, shoulder, and knee contact points — often the highest-ROI intervention for chronic pain on an inadequate existing mattress."),
        ("What supplements help chronic pain and sleep?",
         "Magnesium glycinate (200-400mg) reduces the musculoskeletal hyperexcitability that amplifies pain during the night. Tart cherry extract contains natural melatonin and anti-inflammatory compounds. Low-dose melatonin (0.5mg) combined with positioning aids tends to produce better results than supplements alone for pain-related sleep disruption."),
    ],
    'memory-foam-vs-hybrid-mattress.html': [
        ("Is memory foam or hybrid better for back pain?",
         "Hybrids perform slightly better for back pain in most studies due to better spinal alignment. The pocketed coil base in hybrids provides zoned support — firmer under the hips and lower back, softer at the shoulders — that memory foam achieves less consistently. However, a medium-firm memory foam mattress outperforms a firm hybrid for most back sleepers under 180 lbs."),
        ("Which sleeps cooler: memory foam or hybrid?",
         "Hybrid mattresses sleep significantly cooler. The pocketed coil layer allows convective airflow that pure foam cannot match. Traditional memory foam retains body heat; gel-infused and open-cell formulations help but don't fully resolve the issue. If you consistently sleep hot, a hybrid with a breathable cover is the better choice."),
        ("How long does a hybrid mattress last compared to memory foam?",
         "High-quality hybrids and memory foam mattresses both last 8-10 years. Low-quality examples of each last 5-7 years. The weakest component in a hybrid is the comfort foam layer — if it's less than 2 inches thick, it will compress first. The weakest component in an all-foam mattress is the base foam — it should be at least 5-6 inches of high-density (1.8+ lb/ft³) foam."),
        ("Is a hybrid mattress worth the extra cost?",
         "For hot sleepers, couples with different firmness preferences, or those over 200 lbs: yes. Hybrids provide better temperature regulation, edge support, and responsiveness. For lightweight or average-weight side sleepers who sleep cool and alone, a quality all-foam mattress at a lower price point often performs as well or better for pressure relief."),
    ],
    'restless-legs-syndrome.html': [
        ("What causes restless legs syndrome (RLS)?",
         "RLS has both genetic and environmental causes. The strongest modifiable factors are iron deficiency (even at serum ferritin levels considered 'normal' by standard ranges — RLS improves with ferritin above 75 ng/mL), magnesium deficiency, and dopamine pathway dysfunction. Secondary RLS is common in pregnancy, kidney disease, and with certain medications including antihistamines, antidepressants, and antinausea drugs."),
        ("Does magnesium help restless legs syndrome?",
         "Yes, particularly for cases related to magnesium deficiency. Magnesium glycinate at 200-400mg before bed reduces the neuromuscular excitability component of RLS. Several small studies show symptom reduction. It works best when magnesium levels are below optimal — testing serum magnesium and RBC magnesium before supplementing is worthwhile."),
        ("What aggravates restless legs syndrome?",
         "The strongest RLS triggers are: caffeine (worsens dopamine regulation), alcohol (disrupts sleep architecture and worsens symptoms in the second half of the night), antihistamines (Benadryl is a particularly common culprit — widely used as a sleep aid but dramatically worsens RLS), prolonged sitting, and heat."),
        ("When should I see a doctor for restless legs syndrome?",
         "When symptoms occur 3+ nights per week and disrupt sleep, a physician evaluation is warranted. Request iron studies (ferritin specifically, not just hemoglobin) and a full medication review. Severe RLS is treated with dopamine agonists or alpha-2-delta ligands — these require prescription and monitoring for augmentation (the paradoxical worsening of RLS with dopamine medications over time)."),
    ],
    'pregnancy-sleep-guide.html': [
        ("Why is sleep so difficult during pregnancy?",
         "Sleep disruption in pregnancy has multiple overlapping causes: increased urinary frequency from fetal pressure on the bladder, physical discomfort from the growing abdomen, heartburn worsened by the hormone progesterone (which relaxes the esophageal sphincter), restless legs syndrome (affects 30% of pregnant women due to folate and iron demands), and elevated basal body temperature from increased metabolic rate."),
        ("What is the safest sleeping position during pregnancy?",
         "Left side sleeping (SOS — Sleep on Side) is recommended from the second trimester onward. This position optimizes blood flow through the inferior vena cava to the fetus and reduces pressure on the liver. Research shows that supine sleeping in the third trimester is associated with increased stillbirth risk — the mechanism is compression of the aorta and inferior vena cava. Right side sleeping is also acceptable."),
        ("What pillow is best for pregnancy?",
         "A full-length body pillow or C-shaped pregnancy pillow provides the most comprehensive support, supporting the belly, back, and knees simultaneously to maintain the side-lying position. A pregnancy wedge pillow is more compact and works well for targeted support under the belly or behind the back for women who prefer a regular pillow for their head."),
        ("Is it safe to take melatonin during pregnancy?",
         "The evidence on melatonin during pregnancy is insufficient to make a clear safety recommendation. The American College of Obstetricians and Gynecologists does not endorse melatonin use during pregnancy. Behavioral interventions — cool room temperature, blackout curtains, positioning pillows, and consistent sleep timing — are the preferred first-line approaches."),
    ],
    'sleep-sanctuary-guide.html': [
        ("What temperature should a bedroom be for sleep?",
         "The optimal bedroom temperature for sleep is 65-68°F (18-20°C). Core body temperature drops 1-2°F as part of the sleep initiation process. A room that is too warm prevents this drop and delays sleep onset. Individual variation exists — some sleep well at 63°F, others at 70°F — but most adults fall in the 65-68°F range."),
        ("Does a white noise machine actually help sleep?",
         "Yes, for people in noise-disrupted environments. White noise at 50-55dB masks the variable sounds (traffic, voices, pipes) that trigger micro-arousals during sleep transitions. The masking effect is more important than the sound itself — consistent ambient noise prevents the startle response to sudden sounds. Fan-based white noise machines produce true broadband noise; digital machines offer more variety."),
        ("Should you sleep with the door open or closed?",
         "Closed is safer and often better for sleep quality. A closed bedroom door delays smoke and fire spread by up to 3 minutes, reduces noise from other parts of the home, and helps maintain the cool, stable temperature associated with better sleep. The trade-off in air circulation is minor compared to these benefits."),
        ("How dark should a bedroom be for sleep?",
         "As dark as possible — ideally under 1 lux, which is near-total darkness. Even low light exposure during sleep suppresses melatonin and increases cortisol, reducing sleep quality measurably. Blackout curtains that block 99%+ of light are the most effective intervention for light-polluted environments. A sleep mask achieves similar results and is portable."),
    ],
    'aging-and-sleep.html': [
        ("Why do older adults sleep less?",
         "Aging reduces melatonin production by 50-75% between ages 20 and 70, weakens circadian rhythm amplitude, reduces slow-wave sleep percentage, and advances sleep phase (causing earlier bedtimes and wake times). The sleep architecture shift is neurological — older brains produce less adenosine drive and have less GABA activity during sleep. This is normal aging, not insomnia, though the two frequently co-occur."),
        ("How much sleep do older adults need?",
         "The National Sleep Foundation recommends 7-8 hours for adults over 65 — the same as younger adults. The common belief that older adults need less sleep is a myth. What changes with age is the ability to get consolidated sleep, not the requirement for it. Many older adults are chronically sleep-deprived because they cannot achieve the 7-8 hours they still need."),
        ("What helps older adults sleep better?",
         "The most evidence-backed interventions are CBT-I (first-line treatment for insomnia in all ages), low-dose melatonin (0.3-0.5mg at target bedtime to compensate for reduced natural production), morning light exposure to reinforce circadian rhythm, and reducing evening light and screen exposure. Physical activity during the day — even a 30-minute walk — significantly improves sleep quality in older adults."),
        ("When does sleep change with aging?",
         "Sleep architecture begins shifting noticeably around age 40-50. Slow-wave sleep percentage declines by approximately 2% per decade after age 30. By age 60, many adults experience phase advancement (earlier sleep onset and wake times), more fragmented sleep, and reduced ability to sleep in. These changes accelerate in those with chronic illness, sedentary lifestyle, or low vitamin D."),
    ],
    'alcohol-sleep-quality.html': [
        ("Does alcohol help you sleep?",
         "Alcohol helps with sleep onset — it reduces the time to fall asleep — but significantly degrades sleep quality. It suppresses REM sleep in the first half of the night and causes rebound arousal in the second half as the liver metabolizes it. The net result is fragmented, shallow sleep with reduced slow-wave and REM phases. Most people wake earlier and feel less rested despite falling asleep faster."),
        ("How much alcohol affects sleep quality?",
         "Even moderate amounts (1-2 drinks) measurably reduce sleep quality. Studies show dose-dependent REM suppression and increased sleep fragmentation. The timing matters: alcohol consumed 4+ hours before bed has largely metabolized before peak sleep, reducing but not eliminating the disruption. Alcohol within 2 hours of bedtime produces the most significant sleep quality reduction."),
        ("How long does alcohol affect sleep?",
         "A single moderate drink (1.5 units) metabolizes at roughly 1 unit per hour. For a 2-drink evening, full metabolism takes approximately 3-4 hours. Sleep disruption typically peaks 4-5 hours after drinking as blood alcohol drops and rebound arousal occurs — this is the classic 3am awakening pattern in regular drinkers."),
        ("Does alcohol cause sleep apnea?",
         "Alcohol worsens existing sleep apnea by relaxing the upper airway muscles that maintain airway patency. For borderline cases, alcohol can trigger apnea events that would not otherwise occur. People with diagnosed OSA are advised to avoid alcohol entirely within 4 hours of sleep. Even without diagnosed apnea, alcohol increases snoring and upper airway resistance during sleep."),
    ],
    'adenosine-sleep-drive.html': [
        ("What is adenosine and why does it make you sleepy?",
         "Adenosine is a byproduct of cellular energy metabolism that accumulates in the brain during wakefulness. It binds to adenosine receptors in the basal forebrain and hypothalamus, progressively increasing sleepiness as concentrations rise. After approximately 16 hours of wakefulness, adenosine levels are high enough to produce overwhelming sleep pressure. During sleep, adenosine is cleared by the glymphatic system, restoring wakefulness capacity for the next day."),
        ("How does caffeine block sleepiness?",
         "Caffeine is an adenosine receptor antagonist — it blocks adenosine receptors without activating them, preventing the sleepiness signal from being received. Adenosine continues accumulating behind the block; when caffeine clears (half-life 5-7 hours), the accumulated adenosine floods the now-unblocked receptors all at once — producing the 'caffeine crash.' Caffeine does not eliminate adenosine; it delays the sleep signal."),
        ("What is sleep pressure and how does it work?",
         "Sleep pressure (Process S in the two-process model of sleep) is the homeostatic drive to sleep that builds with each hour of wakefulness and is discharged by sleep. It is primarily mediated by adenosine accumulation. It works in tandem with the circadian clock (Process C), which modulates arousal independently of sleep pressure. Good sleep requires both high adenosine drive at bedtime and correct circadian timing."),
        ("Does sleep debt accumulate?",
         "Yes. Chronic sleep restriction (6 hours/night for 2 weeks) produces cognitive impairment equivalent to 48 hours of total sleep deprivation, while subjective sleepiness plateaus — people feel adapted but are objectively impaired. Recovery from sleep debt is also slow: one night of recovery sleep does not fully restore cognitive performance. Weekends cannot fully repay a week of sleep restriction."),
    ],
    'social-jetlag.html': [
        ("What is social jet lag?",
         "Social jet lag refers to the discrepancy between your biologically preferred sleep timing (chronotype) and the sleep timing imposed by your work or school schedule. When people compensate on weekends by sleeping 2+ hours later than weekday schedules allow, they experience a recurring phase shift equivalent to crossing 2 time zones every weekend. This chronic circadian misalignment is associated with metabolic and cardiovascular health risks."),
        ("How much social jet lag is harmful?",
         "A social jet lag of 1 hour is associated with a 33% increased risk of obesity. Above 2 hours is associated with significant metabolic syndrome risk and reduced cognitive performance on Monday-Tuesday. The harmful effects appear dose-dependent — each additional hour of social jet lag correlates with worsening health markers."),
        ("How do I reduce social jet lag?",
         "The primary intervention is narrowing the gap between weekday and weekend sleep timing. Strategies include: moving bedtime 30 minutes earlier starting Thursday night; using a sunrise alarm clock for a consistent, friction-reduced wake time; taking 0.3-0.5mg melatonin at your target weekday bedtime on Friday and Saturday nights; and avoiding bright light exposure on weekend mornings if you tend to sleep late."),
        ("Is social jet lag the same as regular jet lag?",
         "They involve the same mechanism — circadian misalignment — but differ in pattern. Travel jet lag is acute and resolves as you adapt to a new time zone. Social jet lag is chronic and recurring, reset every Monday. Travel jet lag is typically worse in the short term; social jet lag is more harmful cumulatively due to its weekly repetition."),
    ],
    'sleep-immune-system.html': [
        ("How does sleep affect the immune system?",
         "Sleep is the primary recovery window for immune function. During slow-wave sleep, the body releases cytokines (signaling proteins that coordinate immune responses), produces T-cells and natural killer cells, and consolidates immunological memory from recent exposures. Sleep deprivation reduces natural killer cell activity by 70% after one night of poor sleep, and vaccine antibody responses are significantly lower in sleep-deprived individuals."),
        ("How many hours of sleep do you need for immune function?",
         "7-8 hours for most adults. People sleeping under 6 hours are 4.2x more likely to develop a cold when exposed to rhinovirus, compared to those sleeping 7+ hours (Carnegie Mellon study). The immune threshold appears to be around 7 hours — below this, susceptibility to infection increases markedly."),
        ("Does poor sleep increase cancer risk?",
         "Chronic sleep disruption is associated with increased cancer risk, particularly for breast, colorectal, and prostate cancers. The mechanism involves melatonin suppression (melatonin has oncostatic properties), reduced natural killer cell activity, and chronic inflammation from sleep deprivation. Night shift workers have elevated cancer risk — a relationship strong enough that WHO classified shift work as a probable carcinogen in 2007."),
        ("Can you boost your immune system by sleeping more?",
         "Up to a point. Sleeping the recommended 7-8 hours reliably supports immune function. Sleeping 9+ hours in a healthy adult does not provide additional immune benefit. However, during active infection or illness, the body increases sleep drive deliberately — fever and cytokines promote sleep — and allowing extra sleep during illness genuinely accelerates recovery."),
    ],
    'brain-during-sleep.html': [
        ("What does the brain do during sleep?",
         "During sleep, the brain consolidates memories (transferring them from hippocampus to cortex), clears metabolic waste products via the glymphatic system (including amyloid-beta and tau proteins linked to Alzheimer's), regulates emotional processing through REM sleep, repairs synaptic connections weakened by wakefulness, and processes hormones including growth hormone (released primarily during slow-wave sleep)."),
        ("What is the glymphatic system?",
         "The glymphatic system is a waste-clearance network that flushes cerebrospinal fluid through the brain during sleep, removing metabolic waste products including the proteins amyloid-beta and tau — the same proteins that accumulate in Alzheimer's disease. Glymphatic flow is 10x more active during sleep than wakefulness. Chronic sleep deprivation impairs this clearance, and early Alzheimer's is associated with sleep disruption years before cognitive symptoms appear."),
        ("What happens to the brain during REM sleep?",
         "During REM (Rapid Eye Movement) sleep, brain activity resembles wakefulness — the prefrontal cortex is partially deactivated while the limbic and visual areas are highly active. This creates the vivid, narrative dreams of REM. REM sleep is critical for emotional memory processing: experiences encoded during the day are replayed without the stress neurochemicals (norepinephrine) that were present during the experience, allowing emotional memories to be processed without re-traumatization."),
        ("Does sleeping help with learning and memory?",
         "Yes, significantly. Sleep within 24 hours of learning is required for memory consolidation. The hippocampus replays newly acquired information during slow-wave sleep, transferring it to long-term cortical storage. REM sleep integrates new information with existing knowledge, enabling insight and pattern recognition. Students who sleep after studying demonstrate 30-40% better recall than those who remain awake the same number of hours."),
    ],
    'lucid-dreaming-guide.html': [
        ("What is lucid dreaming?",
         "Lucid dreaming occurs when a dreamer becomes aware they are dreaming while the dream continues. This metacognitive awareness allows varying degrees of conscious influence over the dream environment. Lucidity exists on a spectrum from weak awareness (knowing you are dreaming but unable to influence events) to strong lucidity (full awareness with ability to direct narrative and environment)."),
        ("How do I start lucid dreaming?",
         "The most effective beginner techniques are reality testing (performing reality checks during the day until the habit carries into dreams) and Wake Back to Bed (WBTB). For WBTB: wake after 5-6 hours of sleep, stay awake for 20-30 minutes while reading about lucid dreaming, then return to sleep — this places you directly into REM-rich sleep with heightened metacognitive awareness. Keep a dream journal from the first day to build recall."),
        ("Are there risks to lucid dreaming?",
         "Lucid dreaming itself is not harmful. The WBTB technique temporarily disrupts sleep, so it should not be practiced every night or by those with insomnia. Some people experience sleep paralysis during lucid dreaming attempts — this is not dangerous (the brain briefly maintains REM muscle atonia while regaining consciousness) but can be frightening until understood. Lucid dreaming does not interfere with sleep quality when practiced infrequently."),
        ("What percentage of people can lucid dream?",
         "Approximately 55% of adults report experiencing at least one lucid dream in their lifetime. About 23% experience them monthly. Regular, controllable lucid dreaming is rarer — studies suggest 11-13% of people have frequent lucid dreams. With deliberate practice, most people can achieve occasional lucid dreams within 3-4 weeks; consistent lucid dreaming takes months of practice."),
    ],
    'sleep-inertia.html': [
        ("What is sleep inertia?",
         "Sleep inertia is the temporary impairment — grogginess, disorientation, reduced performance — that occurs immediately upon waking. It peaks within 1-3 minutes of waking and resolves in 15-30 minutes for most people, though in severe cases it can persist up to 4 hours. It is caused by residual adenosine in the brain (which hasn't fully cleared despite sleep) and the abrupt transition from sleep neurochemistry to wakefulness."),
        ("Why is it so hard to wake up in the morning?",
         "The severity of morning grogginess depends on which sleep stage you were in when you woke. Waking from slow-wave (deep) sleep produces the worst sleep inertia — the brain was in its most suppressed arousal state. Waking from light sleep (Stage 1 or 2) produces minimal inertia. Circadian timing also matters: waking before your natural cortisol awakening response peaks (typically 30-45 minutes after your biological wake time) produces more grogginess."),
        ("How do you get rid of sleep inertia fast?",
         "The fastest evidence-based interventions are: bright light exposure within 5 minutes of waking (suppresses residual melatonin and accelerates cortisol rise), cold water on the face (activates the sympathetic nervous system), and the 'nap-a-latte' technique (drink coffee immediately before a 20-minute nap so caffeine peaks at wake time). Alarm placement across the room forces movement, which also accelerates arousal."),
        ("What time should I wake up to avoid sleep inertia?",
         "Waking at the end of a 90-minute sleep cycle minimizes sleep inertia because you surface from lighter sleep. Count back from your target wake time in 90-minute intervals from when you want to fall asleep (not when you get into bed). A sunrise alarm clock that gradually brightens 20-30 minutes before your alarm time tends to catch you in a lighter sleep stage than a sudden alarm does."),
    ],
    'sleep-adhd.html': [
        ("Why do people with ADHD have trouble sleeping?",
         "ADHD is associated with delayed circadian rhythm in approximately 75% of cases — the body clock runs 1.5-2 hours later than neurotypical adults. This creates a structural mismatch between biological sleep timing and social/work demands. ADHD also involves dysregulated dopamine and norepinephrine systems that elevate arousal and delay sleep onset. Racing thoughts, difficulty disengaging from stimulating activities ('revenge bedtime procrastination'), and rejection-sensitive dysphoria all contribute."),
        ("Does melatonin help ADHD sleep problems?",
         "Low-dose melatonin (0.5-1mg) taken 30-60 minutes before target bedtime has good evidence for ADHD-related delayed sleep phase. It advances the delayed circadian clock without causing next-day sedation. Several pediatric studies show melatonin reduces sleep onset latency in ADHD children by 30-50 minutes. It works best combined with consistent bedtime routine and reduced evening screen time."),
        ("Do ADHD medications affect sleep?",
         "Yes, significantly. Stimulant medications (amphetamines, methylphenidate) extend wakefulness and can delay sleep onset by 1-2 hours when dosed too late. Taking the last dose before noon reduces this effect. Non-stimulant medications (atomoxetine, guanfacine) have less impact on sleep and sometimes improve it. Any medication timing concern should be discussed with the prescribing physician."),
        ("What helps ADHD adults sleep?",
         "Most effective interventions: weighted blanket (deep pressure reduces hyperarousal), white noise machine (masks novel sounds that pull ADHD attention), consistent bedtime and wake time (reduces circadian variability), blue light blocking glasses 90 minutes before bed, and a wind-down routine that explicitly 'turns off' work and stimulating activities. Low-dose melatonin addresses the delayed circadian phase component."),
    ],
    'sleep-fibromyalgia.html': [
        ("Why does fibromyalgia cause sleep problems?",
         "Fibromyalgia disrupts sleep through amplified pain (which triggers arousals at contact points), alpha wave intrusion into slow-wave sleep (producing non-restorative sleep even when total hours appear adequate), and the central sensitization that makes the nervous system hypersensitive to sensory input including temperature, pressure, and noise during sleep. Poor sleep then lowers pain threshold, creating a self-perpetuating cycle."),
        ("What is alpha-delta sleep in fibromyalgia?",
         "Alpha-delta sleep is the intrusion of alpha brain waves (associated with relaxed wakefulness) into delta sleep (slow-wave or deep sleep). It is common in fibromyalgia and produces sleep that is technically present on EEG but functionally non-restorative. People wake feeling unrefreshed despite sleeping 8+ hours because slow-wave sleep was interrupted by awake-state brain activity throughout the night."),
        ("What sleeping position is best for fibromyalgia?",
         "Side sleeping with a body pillow between the knees and supporting the abdomen is generally best, as it reduces pressure at the hip and lumbar junction and prevents the compensatory movements that fragment sleep. A medium-soft mattress or 2-3 inch memory foam topper reduces pressure at pain-sensitive contact points. Avoid stomach sleeping, which places the spine in sustained extension and worsens morning stiffness."),
        ("Does CBT-I work for fibromyalgia insomnia?",
         "Yes. CBT-I has demonstrated effectiveness for fibromyalgia-related insomnia in multiple trials, with improvements in both sleep quality and pain perception. The cognitive restructuring component is particularly important in fibromyalgia, where fear of not sleeping (and the pain consequences the next day) creates hyperarousal that perpetuates insomnia. CBT-I is recommended even when pharmacological treatment for fibromyalgia is also used."),
    ],
    'dreams-science.html': [
        ("Why do we dream?",
         "There is no single agreed-upon answer, but the strongest current theories are: memory consolidation and integration (REM sleep replays waking experiences to extract patterns and build long-term memory), emotional processing (REM sleep processes emotional memories without stress neurochemicals, reducing emotional charge), and threat simulation (an evolutionary function where the sleeping brain rehearses responses to threats). These theories are not mutually exclusive."),
        ("What does it mean when you dream about something?",
         "Dreams primarily reflect recent experiences, persistent concerns, and emotionally significant memories. The continuity hypothesis holds that dream content mirrors waking life preoccupations. There is no scientific evidence for symbolic dream interpretation (that specific objects consistently represent specific meanings). Dreams may help process difficult experiences — common after loss or stress — but the content itself is not considered diagnostically meaningful."),
        ("Why do we forget dreams so quickly?",
         "Dream memory is fragile because the hippocampus — the brain's memory recorder — is only partially active during REM sleep, and norepinephrine (which strengthens memory encoding) is at near-zero levels. Dreams are encoded briefly but not transferred to long-term storage unless you wake during or immediately after REM and actively rehearse the content. Writing dreams down within 60 seconds of waking dramatically improves retention."),
        ("What causes nightmares?",
         "Nightmares are linked to REM sleep and are more common when: REM sleep is suppressed (by alcohol or medications) and rebounds strongly (REM rebound), during high-stress periods (PTSD is the most severe form), when body temperature is elevated, and after certain medications (beta-blockers, SSRIs, mefloquine). Frequent nightmares in adults warrant evaluation — they are a primary symptom of PTSD and can be treated with Image Rehearsal Therapy."),
    ],
    'kids-screen-time-sleep.html': [
        ("How does screen time affect children's sleep?",
         "Screen time affects children's sleep through three mechanisms: blue light emission suppresses melatonin production, delaying sleep onset by 30-60 minutes; cognitively stimulating content increases arousal that persists after the screen is off; and social media content creates emotional activation that increases cortisol. Children's crystalline lens allows more blue light transmission than adults, making them more sensitive to this effect."),
        ("How long before bed should kids stop screen time?",
         "The American Academy of Pediatrics recommends no screens within 1 hour of bedtime. Research suggests 90 minutes produces better outcomes for sleep quality than 60 minutes. The goal is allowing melatonin onset to begin before the child gets into bed. Blue light blocking glasses can reduce but do not eliminate the cognitive arousal component — physical screen removal is more reliable."),
        ("What screen time limits are recommended by age?",
         "American Academy of Pediatrics guidelines: Under 18 months — no screen time except video calls. 18-24 months — only high-quality programming with caregiver co-viewing. 2-5 years — limit to 1 hour/day of high-quality content. 6 and older — consistent limits on both time and content type, ensuring it does not displace sleep, physical activity, or social interaction."),
        ("How do I get my child to stop using screens before bed?",
         "Device charging outside the bedroom (a physical barrier) is more effective than rules alone. A visual timer that announces when screen time ends gives children warning rather than abrupt termination, reducing resistance. A consistent wind-down routine (bath, reading, dim light) replacing the screen habit provides an alternative. Blue light blocking glasses as a transitional measure help if complete screen removal is not immediately achievable."),
    ],
    'kids-sleep-guide.html': [
        ("How much sleep do children need by age?",
         "American Academy of Sleep Medicine recommendations: Infants 4-12 months — 12-16 hours including naps. Toddlers 1-2 years — 11-14 hours including naps. Preschoolers 3-5 years — 10-13 hours including naps. School age 6-12 years — 9-12 hours. Teenagers 13-18 years — 8-10 hours. These are total sleep hours; naps count for younger children."),
        ("How do I get my toddler to sleep through the night?",
         "The most evidence-based approaches are: consistent bedtime routine (30-45 minutes of predictable steps), same bedroom environment at sleep onset and during night wakings, and gradual withdrawal (Ferber method) or extinction with parental check-ins. The key principle is that children learn to sleep in the same conditions as when they fell asleep — if they need a parent present to fall asleep initially, they will need them again at each night waking."),
        ("What time should children go to bed?",
         "Backtrack from the necessary wake time by the required sleep hours for the child's age, then subtract 15-20 minutes for sleep onset latency. For a school-age child needing 10 hours who wakes at 6:30am: bedtime should be around 8:00-8:30pm. Young children (under 5) have earlier circadian peaks and often do best with 7-7:30pm bedtimes, which is counterintuitively early but reduces overtiredness and early morning waking."),
        ("Why do teenagers stay up so late?",
         "Puberty causes a biological delay in the circadian clock — the melatonin onset shifts 2-3 hours later. This is not behavioral defiance; it is a documented neurobiological change that makes it physically impossible for most adolescents to fall asleep before 11pm. School start times before 8:30am create chronic sleep deprivation in teenagers. The American Academy of Pediatrics advocates for middle and high school start times no earlier than 8:30am."),
    ],
    'sleep-myths-series.html': [
        ("Is 8 hours of sleep the right amount for everyone?",
         "No. The recommended range for adults is 7-9 hours, with natural variation. Approximately 5% of adults are genuine 'short sleepers' who function optimally on 6 hours — this is genetic, not a trained adaptation. Approximately 3% require 9+ hours. The 8-hour figure is a population median, not a universal prescription. What matters is sleeping enough to wake without an alarm feeling rested."),
        ("Can you catch up on sleep on weekends?",
         "Partially and incompletely. Cognitive performance improves with recovery sleep, but the cumulative damage from a week of sleep restriction is not fully reversed by 2 days of extra sleep. Metabolic markers (glucose tolerance, inflammation) require longer recovery. Regular weekend catch-up also creates social jet lag — shifting sleep timing disrupts the circadian clock and makes Monday mornings harder."),
        ("Does alcohol help you sleep?",
         "No — it only helps you fall asleep faster while reducing sleep quality. Alcohol suppresses REM sleep and causes rebound arousal in the second half of the night as the liver metabolizes it. The net effect is fragmented, shallow sleep with less slow-wave and REM content. The faster sleep onset is a sedative effect, not healthy sleep."),
        ("Is snoring harmless?",
         "Not necessarily. Snoring is a symptom of upper airway resistance; loud, frequent snoring with witnessed breathing pauses is the primary symptom of obstructive sleep apnea, which affects 30% of adults and is associated with serious cardiovascular and metabolic risks. Primary snoring (without apnea) is less dangerous but still disrupts bed partners. Loud snoring warrants evaluation with a home sleep test."),
    ],
    'sleep-hygiene-checklist.html': [],  # already defined above
}

# Remove duplicates from the dict (sleep-hygiene-checklist appears twice)
FAQS.pop('sleep-hygiene-checklist.html', None)
FAQS['sleep-hygiene-checklist.html'] = [
    ("What is sleep hygiene?",
     "Sleep hygiene refers to the set of behavioral and environmental practices that support consistent, high-quality sleep. The most evidence-backed habits include a fixed wake time 7 days a week, avoiding caffeine after 2pm, blocking light exposure in the 90 minutes before bed, and keeping bedroom temperature between 65-68°F."),
    ("What is the single most important sleep hygiene habit?",
     "A consistent wake time, maintained even on weekends, is the most impactful sleep hygiene behavior. It anchors your circadian rhythm, regulates adenosine buildup, and makes falling asleep easier within 2-3 weeks of consistent practice."),
    ("How long does it take for sleep hygiene to work?",
     "Most people notice improvement in sleep onset latency within 1-2 weeks of consistent practice. Full circadian stabilization typically takes 3-4 weeks of unbroken routine."),
    ("Does screen time before bed really affect sleep?",
     "Yes. Blue-spectrum light from screens suppresses melatonin production, delaying sleep onset by 30-90 minutes. Either stop using screens 90 minutes before bed, or use amber-lens blue light blocking glasses, which cut the 480nm wavelength that drives melatonin suppression."),
]


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
    # Inject before </head>
    if '</head>' in html:
        html = html.replace('</head>', schema_block + '\n</head>', 1)
        p.write_text(html, encoding='utf-8')
        print(f'OK: {fname} ({len(faqs)} Q&As)')
        updated += 1
    else:
        print(f'NO HEAD TAG: {fname}')

print(f'\nUpdated: {updated}  Skipped: {skipped}')
