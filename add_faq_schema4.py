"""
Inject JSON-LD FAQ schema into editorial posts — batch 4 of 5.
"""
import json
from pathlib import Path

FAQS = {
    'sleep-paralysis-explained.html': [
        ("What is sleep paralysis?",
         "Sleep paralysis is a brief inability to move or speak occurring at the transition between sleep and wakefulness — usually when emerging from REM sleep. REM atonia (the muscle paralysis that prevents acting out dreams) extends briefly into waking consciousness. Episodes last seconds to a few minutes and resolve spontaneously. It affects approximately 8% of the general population and is not dangerous, though it can be frightening, especially when accompanied by hallucinations."),
        ("Why does sleep paralysis happen?",
         "It occurs when REM muscle atonia persists after consciousness returns. Risk factors include sleep deprivation, irregular schedules, supine sleeping, high stress, and narcolepsy. It most commonly occurs during REM-rich sleep in the morning or during daytime naps. Certain medications and disrupted sleep schedules increase frequency."),
        ("How do I stop a sleep paralysis episode?",
         "Try moving your eyes or wiggling a finger or toe — small movements break paralysis before large muscle groups. Steady breathing reduces the panic response that prolongs episodes. To prevent recurrence: maintain consistent sleep timing, avoid sleeping on your back, address sleep deprivation, and manage stress. Recurring episodes warrant evaluation for narcolepsy."),
        ("Are sleep paralysis hallucinations dangerous?",
         "No — they are neurologically generated perceptions, not external threats. The dreaming brain partially activates as consciousness returns, producing visual, auditory, and tactile hallucinations. The classic experiences (a presence in the room, pressure on the chest, visual figures) are consistent across cultures and have a single neurological explanation. Understanding the mechanism significantly reduces fear."),
    ],
    'hypnic-jerk-explained.html': [
        ("What is a hypnic jerk?",
         "A hypnic jerk (sleep start) is an involuntary muscle contraction at the boundary between wakefulness and Stage 1 sleep. It is often accompanied by a sensation of falling. Hypnic jerks are experienced by 60-70% of people and are completely normal — not a sign of neurological disease. They tend to occur more frequently when overtired, highly caffeinated, or anxious."),
        ("Why do hypnic jerks happen?",
         "The leading theories: as the brain transitions to sleep and motor control relaxes, a neural misfiring triggers a protective reflex contraction; or they represent an artifact of the EEG transition between waking and sleep states. They are more common with sleep deprivation, high caffeine intake, and elevated stress — all of which create a more jarring wakefulness-to-sleep transition."),
        ("Are hypnic jerks harmful?",
         "Occasional hypnic jerks are completely harmless and require no treatment. If they occur multiple times per night, prevent sleep onset consistently, or are accompanied by pain or daytime symptoms, evaluation is warranted to rule out periodic limb movement disorder. Jerks exclusively at sleep onset (rather than throughout the night) are benign."),
        ("How do I reduce hypnic jerks?",
         "Most effective approaches: consistent sleep schedule to reduce accumulated sleep deprivation (the primary trigger), limiting caffeine especially after noon, stress management before bed, and progressive muscle relaxation as part of a wind-down routine. Avoiding strenuous exercise within 2 hours of bed reduces the neuromuscular arousal that predisposes to hypnic jerks."),
    ],
    'rem-behavior-disorder.html': [
        ("What is REM behavior disorder?",
         "REM behavior disorder (RBD) is a sleep disorder where the normal muscle atonia of REM sleep fails, allowing people to physically act out their dreams — talking, shouting, punching, kicking, or jumping out of bed while remaining asleep. Unlike sleepwalking (which occurs in NREM sleep), RBD dreams are vivid and typically involve being chased or attacked. It is most common in men over 50 and is a significant clinical marker."),
        ("Is REM behavior disorder serious?",
         "Yes — for two reasons. First, acting out dreams creates injury risk to the sleeper and bed partner. Second, idiopathic RBD (without another known cause) is a strong predictor of neurodegenerative disease: over 80% of idiopathic RBD patients develop Parkinson's disease, Lewy body dementia, or multiple system atrophy within 10-25 years. RBD represents a prodromal phase of synucleinopathies, making diagnosis and monitoring critically important."),
        ("How is REM behavior disorder treated?",
         "Clonazepam (low dose, 0.25-0.5mg at bedtime) reduces RBD episodes in 90% of cases and is the most commonly used treatment. Melatonin (3-12mg at bedtime) is an alternative with fewer side effects, particularly for older adults. Environmental safety measures (bed rails, mattresses on the floor, removing sharp objects from the bedroom) are essential. There is no proven treatment to delay the associated neurodegeneration."),
        ("How is REM behavior disorder diagnosed?",
         "Diagnosis requires a polysomnography (sleep study) with EMG monitoring showing loss of REM atonia with associated behaviors. A clinical diagnosis can be made when a bed partner reliably reports dream-enacting behaviors in the appropriate age-sex demographic, but polysomnography is the gold standard and can distinguish RBD from other parasomnias. A neurological evaluation to assess for early Parkinson's features is typically recommended after diagnosis."),
    ],
    'rem-rebound-explained.html': [
        ("What is REM rebound?",
         "REM rebound is the compensatory increase in REM sleep duration and intensity that occurs after a period of REM deprivation. When REM sleep is suppressed (by alcohol, certain medications, or sleep deprivation), REM pressure builds. On recovery nights, the brain rushes to make up the deficit with earlier REM onset, more frequent REM periods, and more vivid dreams. This is why people have intense, vivid dreams after drinking, after stopping SSRIs, or after a period of sleep deprivation."),
        ("Why do I have intense dreams when I stop drinking?",
         "Alcohol suppresses REM sleep. While drinking regularly, the brain experiences cumulative REM deprivation. When alcohol is stopped or reduced, REM rebound produces unusually vivid, often disturbing dreams as the brain attempts to recover REM sleep debt. This typically lasts 1-4 weeks depending on the duration and amount of prior alcohol use. It is a normal neurological process, not a sign of a problem."),
        ("Is REM rebound harmful?",
         "REM rebound itself is a homeostatic process and not harmful. However, the vivid or disturbing dreams it produces can be distressing and disrupt sleep quality during the rebound period. In severe cases — such as stopping high-dose benzodiazepines or alcohol after heavy use — REM rebound can be intense enough to require medical management. The underlying cause of REM suppression (the medication or substance) is the concern, not the rebound."),
        ("How long does REM rebound last?",
         "For alcohol: 1-3 weeks of significantly elevated REM intensity, with gradual normalization. For SSRIs or SNRIs (which suppress REM): discontinuation dreams can persist for 2-6 weeks. For acute sleep deprivation: one to two recovery nights typically produce REM rebound, with normalization on the third night. The more prolonged the suppression, the longer the rebound period."),
    ],
    'light-sleep-importance.html': [
        ("Is light sleep important?",
         "Yes — Stage 2 (N2) light sleep is the most abundant sleep stage, constituting about 50% of total sleep in adults, and has critical functions. Sleep spindles generated during Stage 2 consolidate procedural and motor memories. K-complexes may protect sleep continuity by preventing arousal from external sounds. Stage 2 also serves as the transitional stage that precedes and follows both deep sleep and REM — disrupting it undermines the architecture of the entire night."),
        ("What happens if you only get light sleep?",
         "A night predominantly of light sleep (with insufficient Stage 3 and REM) produces the classic 'unrefreshed despite sleeping' experience. Physical recovery is impaired (growth hormone requires slow-wave sleep), memory consolidation is incomplete, and emotional regulation is compromised. Conditions that fragment sleep — sleep apnea, pain, environmental disruptions — often preserve total sleep time while replacing deep and REM sleep with Stage 2 and Stage 1."),
        ("Can you feel rested from light sleep alone?",
         "Occasionally — a brief 20-minute power nap primarily in Stage 2 produces a significant alertness boost because Stage 2 clears accumulated adenosine faster than being awake. But as a substitute for a full night of sleep, light sleep alone is not sufficient for the restorative functions that require slow-wave and REM stages. People with sleep apnea who get predominantly light sleep consistently report non-restorative sleep despite adequate total hours."),
        ("Does more light sleep mean worse sleep quality?",
         "Not necessarily — the distribution of sleep stages normally varies across the night, and higher light sleep percentages in the second half of the night are normal. Problematic light sleep dominance occurs when it replaces expected deep sleep in the first half of the night, or when sleep fragmentation (apnea events, arousals) repeatedly interrupts cycling through all stages. The key metric is whether you wake feeling rested, not the exact stage percentages."),
    ],
    'polyphasic-sleep.html': [
        ("What is polyphasic sleep?",
         "Polyphasic sleep refers to sleeping in multiple shorter periods across the 24-hour day rather than one consolidated nocturnal block (monophasic sleep) or one night block plus one afternoon nap (biphasic sleep). Common schedules include Uberman (six 20-minute naps, ~2 hours total), Dymaxion (four 30-minute naps), and Everyman (one core sleep of 3-4.5 hours plus 2-3 naps). Proposed by sleep hackers as a way to reduce total sleep time."),
        ("Is polyphasic sleep actually effective?",
         "For most extreme schedules (Uberman, Dymaxion), the evidence does not support their viability. These schedules attempt to subsist on 2-4 hours of sleep daily — below the established minimum for adult health — by distributing it across nap periods. Independent research and systematic documentation show significant cognitive impairment, immune dysfunction, and mood disruption in people attempting these schedules. Biphasic sleep (night sleep + one afternoon nap) is evolutionarily supported and beneficial."),
        ("Is biphasic sleep healthy?",
         "Yes — biphasic sleep (a longer nocturnal period plus one daytime nap) is supported by both anthropological and epidemiological evidence. Many non-industrialized cultures naturally sleep this way. A 20-60 minute afternoon nap reduces mortality risk in Mediterranean populations and improves cognitive performance. The natural post-lunch alertness dip at 1-3pm is a circadian feature that suggests biphasic sleep may be a normal human pattern."),
        ("Can you train yourself to need less sleep?",
         "No — the widely held belief that you can train your brain to function on less sleep is not supported by research. Sleep restriction studies consistently show that cognitive performance continues to decline over days of restriction even as subjective sleepiness plateaus. What happens is adaptation of sleepiness perception, not adaptation of sleep need. The only confirmed genetic pathway to reduced sleep need (DEC2 mutation) affects under 3% of the population."),
    ],
    'polyphasic-sleep-schedules.html': [
        ("What are the most common polyphasic sleep schedules?",
         "Main schedules: Monophasic (one 7-9 hour block — standard); Siesta/Biphasic (5-7 hours at night + 20-90 minute afternoon nap — supported by evidence); Everyman (one core block of 3-4.5 hours + 2-3 naps, 5-6 hours total); Uberman (six 20-minute naps spread across 24 hours, 2 hours total); Dymaxion (four 30-minute naps every 6 hours, 2 hours total). Siesta and Biphasic are the only schedules with positive health evidence."),
        ("Which polyphasic schedule is safest?",
         "Biphasic sleep (standard nighttime sleep plus one afternoon nap of 20-30 minutes) is the safest and most evidence-backed alternative to monophasic sleep. It aligns with the circadian system's natural architecture (the post-lunch dip), improves afternoon performance, and maintains adequate slow-wave and REM sleep. Extreme polyphasic schedules that reduce total sleep below 6 hours are not safely sustainable for most people."),
        ("Does Uberman sleep schedule work?",
         "Systematic self-reports and the limited available research suggest Uberman (2 hours total in six 20-minute naps) is not sustainably viable for most people. Achieving it requires the brain to enter REM sleep almost immediately (within minutes of sleep onset), a trait typically limited to narcoleptic individuals or severely sleep-deprived people. Adherents who persist report cognitive fog, emotional dysregulation, and social impairment. Most eventually abandon it."),
        ("What is the healthiest amount of sleep per day?",
         "7-9 hours for adults, supported by consistent findings across cardiovascular, metabolic, cognitive, and mortality outcomes. Sleeping under 6 hours or over 9 hours (when not recovering from deprivation) are both associated with increased mortality in large population studies. The 7-8 hour midpoint is the most consistently optimal range. Individual variation exists — some naturally need 7 hours, others 9 — but the need for under 6 hours is extremely rare genetically."),
    ],
    'sleep-disorders-overview.html': [
        ("What are the most common sleep disorders?",
         "By prevalence: insomnia disorder (10-15% chronic, 30-35% occasional), obstructive sleep apnea (17-24% of adults, largely undiagnosed), restless legs syndrome (5-15%), circadian rhythm disorders (delayed sleep phase in ~0.2%, shift work disorder in shift workers), parasomnias (sleepwalking 3-4%, sleep paralysis 8%), and narcolepsy (~0.05%). Most sleep disorders are underdiagnosed — OSA in particular is estimated at 80-90% undiagnosed."),
        ("How do I know if I have a sleep disorder?",
         "Key indicators warranting evaluation: consistently taking more than 30 minutes to fall asleep, waking multiple times per night with difficulty returning to sleep, excessive daytime sleepiness despite 7-8 hours in bed, loud snoring with witnessed breathing pauses, bed partner reporting you stop breathing, regularly acting out dreams, restless or uncomfortable leg sensations at night, or feeling unrefreshed every morning despite adequate sleep duration."),
        ("Can sleep disorders be cured?",
         "Most sleep disorders are highly treatable. Insomnia responds to CBT-I with 70-80% remission rate. Sleep apnea is effectively managed with CPAP, oral appliance therapy, or surgery — none are cures, but symptoms resolve with treatment. RLS responds to iron supplementation (when deficiency is present), dopamine agonists, or alpha-2-delta ligands. Circadian rhythm disorders respond to light therapy and melatonin. Narcolepsy is managed (not cured) with stimulants and sodium oxybate."),
        ("When should I see a doctor for sleep problems?",
         "Immediately if: you witness someone stop breathing during sleep (potential sleep apnea emergency). Promptly if: insomnia has persisted for 3+ months, daytime sleepiness is affecting safety (driving, operating machinery), you regularly act out dreams, or you experience leg discomfort that disrupts sleep regularly. A starting point is your primary care physician, who can order home sleep tests and refer to a sleep medicine specialist for complex presentations."),
    ],
    'microsleep-dangers.html': [
        ("What is a microsleep?",
         "Microsleep is an involuntary episode of sleep lasting 0.5-15 seconds that occurs during wakeful activity, typically during monotonous tasks (driving, lectures, reading). The person usually has no awareness that it occurred. Microsleeps represent the brain forcibly entering sleep despite efforts to remain awake. They become frequent when sleep debt exceeds approximately 17-18 hours of accumulated wakefulness or during chronic insufficient sleep."),
        ("How dangerous are microsleeps while driving?",
         "Extremely dangerous. At highway speeds (70 mph), a 1-second microsleep covers approximately 100 feet without driver input or braking. Drowsy driving is estimated to cause 100,000 crashes annually in the US (CDC data), contributing to 1,550 deaths. Microsleeps impair driving similarly to a blood alcohol concentration of 0.05-0.08%. A driver may feel alert between microsleeps, making drowsy driving a deceptive hazard — the subjective sense of alertness can persist even while microsleeps occur."),
        ("How do I know if I'm having microsleeps?",
         "Signs you are experiencing microsleeps: sudden head nods or jerks, brief memory gaps in what you were just hearing or reading, blinking heavily, difficulty keeping your eyes focused, drifting between lanes while driving, and missing exits you know well. The absence of memory for a moment while driving is a strong indicator. If these occur, sleep is urgently needed — caffeine and opening windows do not reliably prevent microsleeps."),
        ("Can microsleeps happen without feeling tired?",
         "Yes — this is one of the most dangerous aspects of chronic sleep deprivation. People who have been sleep-restricted for several days adapt their subjective sense of sleepiness (they feel 'fine') while their brains continue to experience microsleeps and declining performance. Studies show that chronically sleep-deprived individuals underestimate their impairment. Microsleeps can occur in someone who does not feel overtly sleepy but is carrying significant sleep debt."),
    ],
    'sleep-ptsd.html': [
        ("How does PTSD affect sleep?",
         "PTSD disrupts sleep through multiple converging mechanisms: nightmares (a diagnostic criterion for PTSD, occurring in 70-90% of patients), hypervigilance preventing sleep onset and maintenance, hyperarousal activating the HPA axis with chronically elevated cortisol and norepinephrine, avoidance of sleep itself as a conditioned threat (people with PTSD may fear going to sleep because of nightmares), and frequent nocturnal arousals triggered by trauma-related stimuli. Sleep disruption then worsens PTSD symptom severity — another bidirectional cycle."),
        ("What is the best treatment for PTSD nightmares?",
         "Image Rehearsal Therapy (IRT) is the most evidence-supported treatment for PTSD nightmares. It involves rescripting the nightmare into a non-threatening alternative ending while awake, then rehearsing the new version mentally daily. Prazosin (an alpha-1 blocker) is the most studied pharmacological treatment for nightmares in PTSD, with 8 of 9 randomized trials showing benefit. EMDR and CBT for PTSD also reduce nightmare frequency as secondary outcomes."),
        ("Can PTSD cause sleep apnea?",
         "PTSD and sleep apnea co-occur at high rates — studies show 40-50% prevalence of OSA in PTSD populations, compared to 20-30% in age-matched controls. The mechanisms include: chronic stress causing upper airway muscle tension changes, the autonomic dysregulation of PTSD affecting breathing control, and the REM disruption in PTSD reducing the stage where OSA severity is typically highest. PTSD also makes CPAP adherence harder, creating a treatment challenge."),
        ("Does sleep improve with PTSD treatment?",
         "Yes, though sleep often requires independent treatment alongside PTSD therapy. Trauma-focused therapies (CPT, PE, EMDR) reduce PTSD severity and improve sleep as a secondary outcome, but nightmares and insomnia often persist even after PTSD symptom remission. CBT-I delivered simultaneously with PTSD treatment produces better sleep outcomes than treating either alone. Some sleep medicine programs now integrate trauma-informed CBT-I with first-line PTSD treatment."),
    ],
    'sleep-creativity.html': [
        ("Does sleep improve creativity?",
         "Yes — REM sleep is particularly associated with creative problem-solving. During REM, the hippocampus connects new information with distant memory structures that were not consciously associated during waking. Classic creative insights that occur during sleep or upon waking (Kekule's benzene ring structure, the sewing machine needle design) represent REM-facilitated integration of disparate knowledge. Studies show 30-40% higher performance on creative problems after sleep compared to an equivalent waking period."),
        ("What is the hypnagogic state and why is it creative?",
         "The hypnagogic state is the transitional period between wakefulness and Stage 1 sleep, characterized by loosely associated imagery and thought. The prefrontal cortex begins deactivating while the default mode network (associated with divergent thinking) remains active. This produces a mental environment where unusual associations form that the awake mind would censor. Edison, Dalí, and others deliberately napped to exploit this state, waking themselves when they fell fully asleep."),
        ("Does REM sleep make you more creative?",
         "Yes. REM sleep activates the associative network — connections between remote concepts — more strongly than any other sleep stage or waking state. This produces the metaphorical and analogical thinking that characterizes creative insight. Artists, musicians, and writers historically report that sleep produces solutions to creative problems that waking cognition could not find. The phenomenon is well-documented in laboratory creativity tasks: REM-rich sleep produces reliably better performance on insight problems."),
        ("How can I use sleep to solve creative problems?",
         "Practical approaches: deliberately think about an unsolved creative problem for 5-10 minutes immediately before bed (incubation), sleep a full night with REM-rich sleep, and have a notebook ready to capture insights upon waking (the hypnopompic transition). Strategic napping — sleeping for 60-90 minutes (one full cycle including REM) after working on a problem — is similarly effective. The brain needs the problem clearly primed before sleep to work on it during REM."),
    ],
    'sleep-longevity.html': [
        ("How does sleep affect lifespan?",
         "Sleep duration and quality are among the strongest behavioral predictors of longevity in epidemiological research. Consistently sleeping under 6 hours or over 9 hours is associated with 12-30% higher all-cause mortality in meta-analyses of large cohort studies. Sleep supports virtually every longevity-relevant biological process: cardiovascular repair, immune function, cellular repair, hormonal regulation, and amyloid clearance from the brain. Inadequate sleep accelerates biological aging at the cellular level."),
        ("Does sleeping less shorten your life?",
         "Based on current evidence, yes — chronic short sleep is associated with shorter lifespan. A large UK Biobank study found that sleeping under 6 hours was associated with 30% higher risk of premature death from all causes, particularly cardiovascular and cancer mortality. The effect is dose-dependent and remains significant after controlling for other lifestyle factors. This does not mean every night of short sleep is harmful — it is the chronic pattern that drives risk."),
        ("What is the optimal sleep duration for longevity?",
         "The 7-8 hour range consistently shows the lowest all-cause mortality risk in large population studies. The relationship is U-shaped: both too little (under 6 hours) and too much (over 9 hours) are associated with increased mortality. The over-9-hour association likely reflects reverse causation (illness causing longer sleep) rather than sleep itself causing harm. For healthy adults, 7-9 hours is the target range."),
        ("Does napping affect longevity?",
         "Regular daytime napping (2-3 times per week) is associated with lower cardiovascular mortality in Mediterranean populations (the Siestas and health study). However, napping in populations where it is not culturally established shows inconsistent associations — some studies suggest napping is a marker of poor nighttime sleep rather than a cause of mortality. For adults with adequate nighttime sleep, a brief afternoon nap is either neutral or slightly beneficial for longevity markers."),
    ],
    'sleep-and-pain.html': [
        ("Why does pain get worse at night?",
         "Multiple mechanisms converge to increase pain perception at night: cortisol (which has anti-inflammatory properties) reaches its daily nadir around midnight, removing its daytime pain-buffering effect. Increased attention to pain in the absence of daytime distractions amplifies the signal. The horizontal position increases blood flow to inflamed areas (joint pain, headaches). Pro-inflammatory cytokines peak in the early morning, amplifying pain signals during the transition from sleep to waking."),
        ("Does poor sleep make pain worse?",
         "Yes — sleep deprivation lowers the pain threshold measurably. Even one night of disrupted sleep reduces pain tolerance by 15-25%. The mechanism involves reduced opioidergic pain modulation (the brain's internal pain-suppression system becomes less effective without adequate sleep) and increased inflammatory markers. This bidirectionality — pain disrupts sleep, sleep deprivation worsens pain — creates a self-reinforcing cycle that is the central challenge in managing chronic pain."),
        ("What sleeping position reduces pain?",
         "Side sleeping with proper support reduces pain for most conditions. For low back pain: side sleeping with a pillow between the knees reduces lumbar rotation stress. For shoulder pain: sleep on the non-affected shoulder with a body pillow for upper arm support. For neck pain: a contoured pillow that maintains cervical neutral (head level with the spine) is important regardless of position. For hip pain: a medium-firm mattress with a topper to pad the trochanter reduces awakening from pressure pain."),
        ("Does lack of sleep cause chronic pain?",
         "Sleep deprivation does not cause chronic pain conditions outright, but it is a significant perpetuating and amplifying factor. In fibromyalgia, the bidirectionality is particularly pronounced — disturbed sleep (specifically the loss of slow-wave sleep due to alpha-delta wave intrusion) may be the primary driver of the pain amplification rather than a symptom. Restoring sleep quality is a therapeutic priority in fibromyalgia treatment precisely because the sleep-pain cycle can be entered from either direction."),
    ],
    'shift-work-sleep.html': [
        ("How do shift workers get enough sleep?",
         "The most effective strategies: create a complete blackout sleeping environment (blackout curtains and sleep mask are equally important during day shifts); use white noise or earplugs to mask daytime noise; communicate a strict do-not-disturb window to household members; anchor sleep to consistent clock times even on days off (within 1-2 hours variation); and consider split sleep (4-5 hours immediately after the shift + a 2-hour nap before the next shift) if one long block is difficult."),
        ("What are the health risks of shift work?",
         "Shift work is classified as a probable carcinogen by WHO (Group 2A) based on epidemiological data. Documented health risks include: 40-60% higher risk of type 2 diabetes, 23-40% higher cardiovascular disease risk, higher cancer incidence (breast and prostate), metabolic syndrome, increased depression and anxiety rates, and increased accident and injury rates. The risks are proportional to the degree of circadian misalignment and years of shift work exposure."),
        ("Is night shift or rotating shift worse for health?",
         "Rotating shifts are generally worse than permanent night shifts. Permanent night shift workers can partially adapt their circadian clock; rotating shift workers never allow adaptation before the schedule changes again. The frequency of rotation matters: slower rotation (7+ days at each phase) allows partial adaptation; faster rotation (every 2-3 days) produces continuous circadian disruption. Backward rotation (nights → evenings → days, following the natural delay direction of the clock) is easier than forward rotation."),
        ("How do shift workers protect sleep quality?",
         "Priority interventions: vitamin D supplementation (2,000-4,000 IU) to compensate for sunlight deprivation; melatonin (0.5-1mg) taken 30 minutes before the intended sleep block; scheduled meal timing aligned with the work schedule (not random eating, which creates peripheral clock disruption); regular aerobic exercise during waking hours; and annual cardiovascular screening given the elevated risk profile."),
    ],
    'sleep-business-travel.html': [
        ("How do you sleep well when traveling for business?",
         "Priority tactics: carry a portable white noise app or machine (hotel HVAC and hallway noise are the top sleep disruptors); bring a blackout travel mask or small travel blinds (hotel curtains are inconsistent); request rooms away from elevators and ice machines; maintain your home bedtime on the travel destination time zone from the first night (not doing so creates additional jet lag); bring your own travel pillow if pillow preference affects your sleep; and limit alcohol at business dinners, which worsens jet lag recovery."),
        ("Does jet lag affect business performance?",
         "Significantly — and in ways that are not fully compensated by caffeine. Jet lag impairs complex decision-making, emotional regulation, and creative thinking for 1-5 days after crossing 3+ time zones. Cognitive tests on traveling executives show measurable performance deficits that persist even when subjects feel 'fine.' For high-stakes negotiations or presentations, scheduling important meetings after at least 2-3 nights of adapted sleep in the destination time zone produces measurably better outcomes."),
        ("Is melatonin effective for business travel jet lag?",
         "Yes, for eastward travel. 0.5mg at the destination bedtime for 3-4 nights accelerates adaptation and reduces jet lag duration by 1-2 days on typical 5-8 time zone crossings. For westward travel (which is easier due to the natural delay direction of the circadian clock), melatonin provides less benefit. Timing matters: taking melatonin at the wrong phase can worsen adaptation. Use at the destination bedtime, not at the departure city's bedtime."),
        ("Should you try to sleep on long flights?",
         "Yes — but strategically. For long-haul eastward flights: sleep aligned with the destination nighttime, not departure city nighttime. For westward flights: staying awake and arriving tired at destination nighttime accelerates adaptation. Use a neck pillow, eye mask, and earplugs or noise-canceling headphones. Avoid alcohol on overnight flights — it helps you fall asleep faster but fragments sleep quality significantly and worsens next-day jet lag."),
    ],
    'sleep-travel-tips.html': [
        ("How can I sleep better in hotels?",
         "Most effective hotel sleep strategies: request a room away from elevators, ice machines, and street-facing walls; bring a portable white noise app or machine; use the Do Not Disturb sign and tape over any light-emitting electronics; set the room temperature to 65-68°F before sleeping; bring a travel sleep mask for rooms with inadequate blackout curtains; and bring your own pillow if sleeping away from home reliably affects your sleep (your scent and familiar firmness matter)."),
        ("How do you sleep on an airplane?",
         "Best practices: recline as soon as possible; use a travel neck pillow that supports the head in neutral rather than dropping forward; bring earplugs or noise-canceling headphones and an eye mask; avoid alcohol (worsens sleep quality); take 0.5mg melatonin timed to the destination nighttime if on an overnight flight; and wear comfortable, non-restrictive clothing. Window seats allow leaning against the cabin wall and avoid being disturbed by others."),
        ("How long does travel fatigue last?",
         "Travel fatigue from long flights (without significant time zone change) typically resolves within 1-2 days of rest. Jet lag from significant time zone changes (3+ hours) takes approximately 1 day per zone crossed without intervention, or 2-4 days with melatonin and light therapy. The direction matters: eastward recovery takes longer than westward. Planning important activities 2-3 days after a significant eastward crossing allows most people to be performing well."),
        ("Is it better to stay awake or sleep on arrival after a long flight?",
         "For eastward travel (most common transatlantic direction): stay awake until local bedtime on the arrival day, even if exhausted. This maximizes sleep pressure at the destination bedtime, producing better first-night sleep and faster adaptation. A short nap (20 minutes) if arrival is in the afternoon is acceptable; longer naps delay nighttime sleep. For westward travel, sleeping at the destination nighttime is easier — the clock naturally delays in that direction."),
    ],
    'sleep-camping.html': [
        ("Does camping outside reset your sleep schedule?",
         "Yes — and dramatically. A landmark study (Wright et al., 2013) found that one week of camping without artificial light shifted participants' circadian clocks an average of 2 hours earlier, bringing sleep timing into alignment with sunset and sunrise. Melatonin onset advanced by nearly 2 hours. The effect was replicated in a weekend camping study, showing that even two days of natural light exposure significantly improves circadian alignment."),
        ("Why do people sleep better when camping?",
         "Camping provides concentrated doses of the two most powerful sleep regulators: natural light (bright daytime light that strengthens circadian amplitude) and darkness (no artificial light after sunset that would normally delay melatonin). Without screens and artificial lighting, the brain synchronizes to the solar cycle. Social pressures to stay up late are also removed. The result is sleep that occurs earlier, is more consolidated, and feels more restorative."),
        ("Is sleeping outside good for sleep?",
         "The research supports it. Natural light exposure is a potent circadian synchronizer — brighter than most indoor environments even on overcast days. The absence of artificial light at night restores natural melatonin timing. Fresh air and mild temperature variation reinforce circadian cycles. People who camp regularly tend to show stronger circadian amplitude on actigraphy than those who stay indoors. The benefits translate partially to urban life if morning outdoor light exposure is maintained."),
        ("How can I replicate camping sleep benefits at home?",
         "Key translatable strategies: maximize bright light exposure in the morning (outdoor time within 1 hour of waking, or a 10,000-lux light therapy lamp); dim all indoor lighting after sunset and switch to warm-spectrum bulbs; eliminate all screens 90 minutes before bed; use blackout curtains and create complete darkness; keep bedroom temperature at 65-68°F; and maintain a consistent sleep-wake schedule aligned with natural sunrise times rather than maximally delayed by artificial light."),
    ],
    'sleep-new-baby.html': [
        ("How do new parents cope with sleep deprivation?",
         "The most effective coping strategies: sleep when the baby sleeps (even brief naps of 20-30 minutes restore alertness significantly); divide night duty explicitly with a partner (one person 'on call' while the other gets a consolidated block); accept help from family for daytime care; maintain basic sleep hygiene within the chaos (dark, cool room for adult sleep); and accept temporary cognitive and mood impairment as normal rather than pathological."),
        ("When do newborns start sleeping through the night?",
         "Most newborns begin consolidating sleep into longer nighttime stretches between 3-6 months, though this varies widely. 'Sleeping through the night' typically means a 5-6 hour stretch rather than 8 hours, and many healthy babies continue night waking until 12-18 months. Premature infants, breastfed babies (who wake more frequently for feeding), and temperamentally sensitive babies tend toward longer waking periods. Night waking at 12 months is developmentally normal even if exhausting."),
        ("How do sleep deprivation and new parenthood affect mental health?",
         "Significantly. Severe sleep deprivation from infant care is the primary precipitant of postpartum depression in non-predisposed individuals and significantly worsens it in those with predisposition. Sleep deprivation reduces emotional regulation, increases irritability and anxiety, and reduces bonding capacity — all of which affect the parenting relationship. Postpartum depression screening should include assessment of sleep quality and quantity, and sleep support should be part of treatment."),
        ("Is it safe to sleep with a newborn?",
         "The AAP (American Academy of Pediatrics) recommends against bed-sharing due to documented risk of sleep-related infant death (SIDS, suffocation). The recommendation is room-sharing without bed-sharing — having the infant in a separate sleep surface in the parents' room for at least 6 months. Risk is highest with soft sleep surfaces, alcohol or drug use, parental smoking, and extreme parental fatigue. If parents choose to bed-share, understanding and minimizing risk factors is critical."),
    ],
    'sleep-menstrual-cycle.html': [
        ("How does the menstrual cycle affect sleep?",
         "Sleep quality changes predictably across the menstrual cycle. In the follicular phase (day 1 of period through ovulation), estrogen rises and sleep is generally best. Ovulation produces a brief cortisol spike that may disturb sleep for 1-2 nights. In the luteal phase (post-ovulation to period), progesterone rises (mildly sedating) but body temperature increases by 0.3-0.5°C, increasing nighttime awakening, and premenstrual symptoms (bloating, pain, mood changes) additionally disrupt sleep in the 1-7 days before menstruation."),
        ("Why is sleep worse before your period?",
         "The premenstrual sleep disruption (premenstrual dysphoric disorder sleep problems in severe cases) reflects dropping progesterone and estrogen in the late luteal phase, rising prostaglandins (which cause cramping and inflammation), elevated body temperature from progesterone-driven thermogenesis, and the physical symptoms of PMS (bloating, breast tenderness, headaches). Women with PMDD report significantly worse sleep quality and more depression in the premenstrual week compared to mid-cycle."),
        ("Does ovulation affect sleep?",
         "Yes. Around ovulation, the LH surge and estrogen peak produce a subtle but measurable sleep disruption in some women. More significant is the progesterone-driven temperature rise after ovulation — the luteal phase temperature increase of 0.3-0.5°C challenges the core body temperature drop required for sleep onset. Women who track basal body temperature for fertility awareness often notice sleep disruption coinciding with this temperature rise."),
        ("Can birth control affect sleep?",
         "Yes. Combined oral contraceptives suppress natural progesterone production, eliminating the luteal phase temperature rise but also removing progesterone's mild sleep-promoting effects. Progestin-only pills have variable effects depending on the specific progestin. Some women report improved sleep consistency on hormonal contraceptives due to elimination of cycle variability; others report insomnia or mood changes. IUDs (hormonal or copper) generally have less systemic sleep impact than oral contraceptives."),
    ],
    'morning-lark-night-owl.html': [
        ("Are morning people or night people healthier?",
         "In the current structure of society (with early school and work start times), morning chronotypes have health advantages because their sleep timing aligns with social demands. Evening chronotypes experience chronic circadian misalignment (social jet lag) that is associated with higher rates of metabolic syndrome, depression, and cardiovascular risk. In a society with flexible scheduling, the advantage would largely disappear — chronotype itself is not the health determinant; alignment between chronotype and schedule is."),
        ("Is being a night owl genetic?",
         "Approximately 50% of chronotype variation is heritable, attributed to polymorphisms in circadian clock genes (CLOCK, PER2, CRY1, CRY2). Genome-wide studies have identified 340+ genetic variants associated with chronotype preference. However, chronotype is also significantly influenced by age (peaks toward eveningness in adolescence, then gradually advances), light exposure habits, and social entrainment. Genetics sets a range; lifestyle determines where within that range you fall."),
        ("Can a night owl become a morning person?",
         "Partially — behavioral and environmental interventions can advance chronotype by 1-2 hours in most people. Morning bright light therapy (10,000-lux lamp or outdoor sun within 30 minutes of the target wake time), consistent early wake times, evening light reduction, and low-dose melatonin at the target bedtime collectively advance the clock. However, a strong genetic evening chronotype cannot be fully converted to morning — forcing it creates chronic misalignment worse than accepting the chronotype."),
        ("What time do night owls wake up naturally?",
         "True evening chronotypes, sleeping on their natural schedule without social constraints, typically fall asleep between 1-4am and wake between 9am-12pm. The midpoint of sleep (midpoint between natural sleep onset and natural wake) is the most accurate chronotype measure. Studies of populations without artificial light show a natural midpoint range of approximately 2-4am, with evening chronotypes clustering at the later end of this distribution."),
    ],
    'chronobiology-basics.html': [
        ("What is chronobiology?",
         "Chronobiology is the scientific study of biological rhythms — the cyclical changes in physiology, behavior, and biochemistry that occur over time. These rhythms operate at multiple timescales: circadian (approximately 24-hour cycles in sleep, hormones, temperature), ultradian (less than 24 hours — 90-minute sleep cycles, 90-minute REM-NREM cycles while awake), and infradian (longer than 24 hours — menstrual cycles, seasonal rhythms). Understanding these rhythms underlies modern sleep medicine, shift work research, and chronotherapy."),
        ("What is a zeitgeber?",
         "A zeitgeber (German for 'time giver') is an external environmental signal that synchronizes the internal circadian clock to the 24-hour day. The primary zeitgeber is light — specifically morning bright light that activates ipRGCs in the retina to signal the suprachiasmatic nucleus. Secondary zeitgebers include meal timing, exercise, social interaction, and temperature changes. Without zeitgebers, the internal clock runs slightly longer than 24 hours (approximately 24.2 hours), gradually drifting out of sync with the day."),
        ("What is the free-running period?",
         "The free-running period (tau) is the natural, unentrained period of the circadian clock — what the clock would do without external zeitgebers. In humans, tau averages approximately 24.2 hours. Because tau is slightly longer than 24 hours, the clock naturally drifts later without morning light exposure to advance it. This is why isolation in constant conditions (underground, polar night) causes people to gradually drift toward later sleep timing."),
        ("How does chronobiology apply to medicine?",
         "Chronotherapy applies chronobiological principles to optimize medical treatment timing. Examples: blood pressure medications are most effective when taken at night (when blood pressure rises paradoxically in some patients), chemotherapy drugs have different efficacy and toxicity profiles depending on time of administration, surgery outcomes vary by time of day (afternoon cardiac surgery has lower complications than morning), and statins are most effective taken in the evening (when HMG-CoA reductase is most active). Chronotherapy is an emerging field with significant clinical implications."),
    ],
    'sleep-consistency-importance.html': [
        ("Why is a consistent sleep schedule important?",
         "Consistent sleep timing is the single most impactful sleep behavior because it determines circadian entrainment — the alignment between your internal clock and the 24-hour day. The circadian system coordinates every bodily function: hormone release, immune activity, metabolism, organ repair, and neurotransmitter cycling. Variable sleep timing creates a recurring phase mismatch that disrupts all of these systems simultaneously. Even one hour of variability between weekdays and weekends measurably impairs health metrics."),
        ("Does going to bed at the same time matter?",
         "Wake time is more important than bedtime for circadian anchoring, because morning light and the cortisol awakening response are the primary reset signals for the clock. However, a consistent bedtime is important for predictable melatonin onset and adequate sleep drive at the intended sleep window. Ideally, both are consistent. If only one can be controlled (common in people with variable evening commitments), wake time takes priority."),
        ("How many days does it take to establish a sleep schedule?",
         "Most people notice improvement in sleep onset and morning wakefulness within 5-7 days of consistent timing. Full circadian stabilization — where sleep pressure, melatonin onset, and cortisol patterns are all optimally aligned — typically takes 2-4 weeks. The process resets if consistency is broken significantly (sleeping 2+ hours later on weekends). Maintaining the schedule is more important than any other sleep hygiene measure."),
        ("What happens to your body when your sleep schedule is irregular?",
         "Irregular sleep timing (social jet lag) is associated with: increased BMI and obesity risk, higher insulin resistance, elevated inflammatory markers, worse mood and emotional regulation, impaired cognitive performance, and reduced cardiovascular health markers. A study of 61,000+ adults found that sleep irregularity was associated with 38% higher heart disease risk, 27% higher metabolic syndrome risk, and lower life satisfaction — independent of total sleep duration."),
    ],
    'sleep-goal-setting.html': [
        ("How do I set realistic sleep goals?",
         "Start with assessment: track your actual sleep for one week without changes (bedtime, wake time, subjective quality). Identify the largest gap — is it onset latency, duration, early morning waking, or quality? Set a single specific goal: 'I will wake at 6:30am every day for 3 weeks' rather than 'I will sleep better.' Make it achievable and measurable. Track the one metric that matters most for your specific issue rather than trying to optimize everything simultaneously."),
        ("What is the 2-week sleep reset?",
         "A structured 2-week sleep reset targets the most impactful behaviors simultaneously: fixed wake time (set for the full 2 weeks), no naps, no caffeine after 1pm, bedroom reserved for sleep only, no screens 90 minutes before bed, and 65-68°F bedroom temperature. This period typically produces significant improvement in sleep onset latency and sleep continuity as the circadian clock stabilizes and sleep drive accumulates appropriately. Results are often visible by day 10-12."),
        ("How do I track sleep without a wearable?",
         "A paper sleep diary is the most validated low-tech tracking method. Record daily: bedtime, estimated sleep onset time, number of nighttime awakenings, final wake time, and a subjective 1-10 quality rating. Calculate weekly averages. Sleep diaries outperform wearable accuracy for sleep onset latency and subjective quality — they capture perception, which is the primary target in insomnia treatment. Digital apps that require only morning journaling (Sleep Cycle, Sleepio) are validated alternatives."),
        ("What is sleep efficiency and how do I improve it?",
         "Sleep efficiency is the percentage of time in bed that is spent asleep: (minutes asleep / minutes in bed) x 100. Healthy sleep efficiency is 85-95%. Low efficiency — spending long periods awake in bed — is a hallmark of insomnia and is addressed by sleep restriction therapy: temporarily limiting time in bed to match current sleep capacity, then gradually extending as efficiency improves. Going to bed only when sleepy and getting out of bed if unable to sleep within 20 minutes also improves efficiency."),
    ],
    'sleep-journal-guide.html': [
        ("Why keep a sleep journal?",
         "A sleep journal provides data that memory cannot. Subjective sleep perception is unreliable — people consistently underestimate how long they slept and overestimate how long they were awake. A journal reveals patterns: which nights are consistently worse (weekdays? after alcohol?), whether sleep onset or early waking is the primary problem, and how behaviors (exercise, caffeine, screen time) correlate with sleep quality. This data is required for CBT-I sleep restriction calculations and is the foundation of evidence-based insomnia treatment."),
        ("What should I write in a sleep journal?",
         "The minimum useful sleep diary: bedtime, estimated time to fall asleep, number of awakenings and their duration, final wake time, time out of bed, and a 1-10 subjective quality rating. Optional additions: daytime naps, caffeine intake and timing, exercise, alcohol, stress level, and medications. Morning completion (recording immediately upon waking) is more accurate than evening recall. Two weeks of data provides sufficient baseline for CBT-I treatment planning."),
        ("How long should I keep a sleep journal?",
         "Two weeks establishes a reliable baseline pattern. For CBT-I treatment, journals are maintained throughout the therapy period (typically 6-8 weeks) to calculate sleep window adjustments and track progress. For general self-awareness, even one week of data reveals patterns most people were unaware of. Long-term intermittent journaling (one week every few months) can catch emerging sleep disruption before it becomes chronic."),
        ("Does tracking sleep make insomnia worse?",
         "It can, for people with high sleep anxiety. Monitoring sleep closely can increase hyperarousal and make sleep a performance event — which worsens insomnia. This is why CBT-I therapists typically instruct patients to complete the diary immediately upon waking rather than checking the clock throughout the night. If tracking increases sleep anxiety, switching to a minimal-data approach (just quality rating and total estimated hours) or pausing tracking while focusing on behavioral aspects of CBT-I is appropriate."),
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
