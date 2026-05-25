"""
expand_pinterest_queue.py
Appends 120 new pins to pinterest_queue.json covering uncovered posts.
Run once: python automation/scripts/expand_pinterest_queue.py
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent
QUEUE_FILE = BASE / "automation" / "data" / "pinterest_queue.json"

NEW_PINS = [
  # ── Sleep Tips / Science ─────────────────────────────────────────────────
  {
    "title": "The 10-3-2-1-0 Sleep Rule (Save This)",
    "description": "10 hrs: no caffeine. 3 hrs: no food. 2 hrs: no work. 1 hr: no screens. 0 snooze hits. Try all 5 for one week. Full breakdown at the link.",
    "link": "https://sleepwisereviews.com/posts/sleep-hygiene-checklist.html",
    "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800",
    "hashtags": ["sleephygiene", "sleeptips", "sleepbetter", "sleepscience"]
  },
  {
    "title": "30-Day Sleep Challenge That Actually Works",
    "description": "One small habit per day for 30 days. By day 30: faster sleep onset, deeper sleep, fewer 3am wake-ups. Free printable tracker inside.",
    "link": "https://sleepwisereviews.com/posts/30-day-sleep-challenge.html",
    "image_url": "https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?w=800",
    "hashtags": ["sleepchallenge", "sleepgoals", "betttersleep", "sleephabits"]
  },
  {
    "title": "Your Perfect Wind-Down Routine (Science-Backed)",
    "description": "What you do in the 90 mins before bed matters more than any supplement. Here's the routine that actually works — backed by circadian research.",
    "link": "https://sleepwisereviews.com/posts/wind-down-routine.html",
    "image_url": "https://images.unsplash.com/photo-1588714477688-cf28a50e94f7?w=800",
    "hashtags": ["winddownroutine", "bedtimeroutine", "sleephygiene", "eveningroutine"]
  },
  {
    "title": "Natural Sleep Aids That Science Actually Supports",
    "description": "Not all 'natural' means effective. These 6 have clinical evidence: magnesium glycinate, L-theanine, valerian, tart cherry, glycine, CBD. Full breakdown here.",
    "link": "https://sleepwisereviews.com/posts/natural-sleep-aids.html",
    "image_url": "https://images.unsplash.com/photo-1585776245991-cf89dd7fc73a?w=800",
    "hashtags": ["naturalsleepaid", "sleepsupplements", "holisticsleep", "sleephealth"]
  },
  {
    "title": "Waking Up at 3am Every Night? Here's Why",
    "description": "It's not insomnia. It's cortisol. Natural cortisol spikes at 3-4am. If you're stressed, it spikes harder = wide awake. Here's the fix.",
    "link": "https://sleepwisereviews.com/posts/waking-at-3am.html",
    "image_url": "https://images.unsplash.com/photo-1494349179014-de2e6e9d0c6a?w=800",
    "hashtags": ["wakeup3am", "sleepproblems", "cortisol", "insomniacure"]
  },
  {
    "title": "Sleeping In on Weekends Is Wrecking Your Monday",
    "description": "Weekend sleep shifts your clock 1.5 hours. Monday feels like jet lag because it IS jet lag. The fix: same wake time 7 days a week. Here's why.",
    "link": "https://sleepwisereviews.com/posts/weekend-sleep-mistake.html",
    "image_url": "https://images.unsplash.com/photo-1520315342629-6ea920342047?w=800",
    "hashtags": ["socialtjetlag", "sleepschedule", "mondaymorning", "circadianrhythm"]
  },
  {
    "title": "What Deep Sleep Actually Does to Your Brain",
    "description": "Slow-wave sleep flushes amyloid plaques, consolidates memory, and releases growth hormone. Miss it and you're running at 60%. Here's how to get more.",
    "link": "https://sleepwisereviews.com/posts/deep-sleep-benefits.html",
    "image_url": "https://images.unsplash.com/photo-1567300925823-1fa03e84cfa7?w=800",
    "hashtags": ["deepsleep", "sleepscience", "brainhealth", "slowwavesleep"]
  },
  {
    "title": "REM Sleep: What It Is and Why You Need More",
    "description": "REM is when your brain processes emotions, consolidates learning, and solves problems. Most people cut REM short by waking too early. Fix: don't cut the last 2 hours.",
    "link": "https://sleepwisereviews.com/posts/rem-sleep-benefits.html",
    "image_url": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=800",
    "hashtags": ["remsleep", "dreamstage", "sleepstages", "sleepscience"]
  },
  {
    "title": "Sleep Debt: How Much You Have and How to Pay It Back",
    "description": "You can't fully pay back sleep debt. But partial recovery IS possible. Here's what the science says about which damage reverses and what doesn't.",
    "link": "https://sleepwisereviews.com/posts/sleep-debt-recovery.html",
    "image_url": "https://images.unsplash.com/photo-1586348943529-beaae6c28db9?w=800",
    "hashtags": ["sleepdebt", "sleepdeprivation", "recoverysleep", "sleephealth"]
  },
  {
    "title": "Caffeine Has a 6-Hour Half-Life (Most People Don't Know This)",
    "description": "A 3pm coffee is still 25% active at midnight. That's why you can't fall asleep. Cut caffeine before 2pm if you want to be asleep by 10pm. Full guide here.",
    "link": "https://sleepwisereviews.com/posts/caffeine-half-life-sleep.html",
    "image_url": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800",
    "hashtags": ["caffeinesleep", "coffeeandleep", "sleephacks", "caffeine"]
  },
  # ── Temperature & Environment ─────────────────────────────────────────────
  {
    "title": "Best Bedroom Temperature for Sleep (It's Cooler Than You Think)",
    "description": "65-67°F is the sweet spot. Most people sleep at 72°F+. Your body needs to drop 1-2°F core temperature to initiate sleep. Warmer room = slower sleep onset.",
    "link": "https://sleepwisereviews.com/posts/bedroom-temperature-sleep.html",
    "image_url": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800",
    "hashtags": ["sleeptemperature", "bedroomtemp", "sleepenv", "sleephygiene"]
  },
  {
    "title": "How to Optimize Your Bedroom for Perfect Sleep",
    "description": "Dark, cool, quiet — and 3 things most guides miss. Complete bedroom sleep environment checklist with specific product recommendations for each item.",
    "link": "https://sleepwisereviews.com/posts/sleep-environment-optimization.html",
    "image_url": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800",
    "hashtags": ["bedroomsetup", "sleepsanctuary", "sleepenv", "bedroomdesign"]
  },
  {
    "title": "Create a Sleep Sanctuary in Your Bedroom This Weekend",
    "description": "5 changes under $100 that transform your bedroom into a sleep machine. Covers lighting, sound, scent, temperature, and one thing nobody talks about.",
    "link": "https://sleepwisereviews.com/posts/sleep-sanctuary-guide.html",
    "image_url": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800",
    "hashtags": ["sleepsanctuary", "bedroomgoals", "sleeproom", "homedecor"]
  },
  # ── Sleep + Health Conditions ─────────────────────────────────────────────
  {
    "title": "Can't Sleep Anxious? These Techniques Actually Work",
    "description": "Anxiety-driven insomnia needs a different approach than regular sleep hygiene. These 5 CBT-I techniques target the anxiety loop specifically. Evidence-based.",
    "link": "https://sleepwisereviews.com/posts/sleep-anxiety-techniques.html",
    "image_url": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=800",
    "hashtags": ["anxietysleep", "sleepanxiety", "cbti", "insomniahelp"]
  },
  {
    "title": "Sleep Inertia: Why You Feel Like a Zombie After 8 Hours",
    "description": "It's not laziness. It's biology. Sleep inertia peaks when you wake mid-cycle. The fix: time your alarm to 90-min cycle boundaries. Here's how to calculate yours.",
    "link": "https://sleepwisereviews.com/posts/sleep-inertia.html",
    "image_url": "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800",
    "hashtags": ["sleepinertia", "morninggrogginess", "wakeup", "sleepcycles"]
  },
  {
    "title": "Sleep and Weight Loss: The Missing Link Nobody Talks About",
    "description": "Sleeping under 7 hours increases ghrelin (hunger hormone) by 28% and cuts leptin (fullness hormone) by 18%. You can't diet your way out of bad sleep.",
    "link": "https://sleepwisereviews.com/posts/sleep-and-weight-loss.html",
    "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800",
    "hashtags": ["sleepweightloss", "sleepmetabolism", "weightlosshacks", "fatlosssleep"]
  },
  {
    "title": "Poor Sleep Doubles Your Heart Disease Risk (Here's What to Know)",
    "description": "Under 6 hours/night: 2x cardiovascular disease risk. The mechanism is cortisol + blood pressure dysregulation. Here's the sleep/heart connection explained.",
    "link": "https://sleepwisereviews.com/posts/sleep-heart-health.html",
    "image_url": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=800",
    "hashtags": ["sleephealth", "hearthealth", "cardiovascular", "sleepmedicine"]
  },
  {
    "title": "Sleep and Hormones: What Happens While You Sleep",
    "description": "Growth hormone, testosterone, cortisol, estrogen — they all follow your sleep cycle. One bad night shifts your hormonal balance for 48+ hours. Full guide here.",
    "link": "https://sleepwisereviews.com/posts/sleep-and-hormones.html",
    "image_url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1f?w=800",
    "hashtags": ["sleephormones", "hormonalhealth", "growthhhormone", "sleephealth"]
  },
  {
    "title": "Alcohol Before Bed Is Destroying Your Sleep Quality",
    "description": "One drink cuts REM sleep by 25%. Two drinks: 50% reduction. You pass out faster but get worse rest. Here's why and what to do instead.",
    "link": "https://sleepwisereviews.com/posts/alcohol-sleep-quality.html",
    "image_url": "https://images.unsplash.com/photo-1474919320905-37f9f86ea0b8?w=800",
    "hashtags": ["alcoholsleep", "noalcohol", "betttersleep", "sleepfacts"]
  },
  {
    "title": "Blue Light Before Bed: Exactly When to Stop and Why",
    "description": "Blue light (460nm) suppresses melatonin for 90 mins after exposure. If bedtime is 10pm, screens off by 8:30pm. Blue light glasses help but don't fully compensate.",
    "link": "https://sleepwisereviews.com/posts/blue-light-melatonin.html",
    "image_url": "https://images.unsplash.com/photo-1592921870789-04563d55041c?w=800",
    "hashtags": ["bluelight", "melatonin", "screentime", "sleephygiene"]
  },
  # ── Specific Sleep Topics ─────────────────────────────────────────────────
  {
    "title": "Hypnic Jerk: Why You Twitch When Falling Asleep",
    "description": "That falling sensation + body jerk when drifting off — it's a hypnic jerk. 70% of people experience it. It's harmless. Here's the brain science behind it.",
    "link": "https://sleepwisereviews.com/posts/hypnic-jerk-explained.html",
    "image_url": "https://images.unsplash.com/photo-1520206183501-b80df61043c2?w=800",
    "hashtags": ["hypnicjerk", "sleepscience", "brainsleep", "sleepcuriosity"]
  },
  {
    "title": "Sleep Paralysis: What's Actually Happening and How to Stop It",
    "description": "You wake up but can't move. Sometimes you see/hear things. This is sleep paralysis — and it's harmless but terrifying. Here's what causes it and how to end it.",
    "link": "https://sleepwisereviews.com/posts/sleep-paralysis-explained.html",
    "image_url": "https://images.unsplash.com/photo-1559757175-5700dde675bc?w=800",
    "hashtags": ["sleepparalysis", "sleepdisorders", "sleepscience", "raredisorder"]
  },
  {
    "title": "Science of Dreams: Why We Dream and What It Means",
    "description": "Dreams happen in REM sleep. They help process emotions, consolidate memories, and prepare you for future challenges. What your dream themes reveal about your stress levels.",
    "link": "https://sleepwisereviews.com/posts/dreams-science.html",
    "image_url": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=800",
    "hashtags": ["dreaming", "remsleep", "dreamscience", "subconscious"]
  },
  {
    "title": "Power Nap Science: The Exact Length for Each Goal",
    "description": "10 min: alertness boost. 20 min: memory + energy. 90 min: full sleep cycle (avoid grogginess). Never 30-60 min — you wake up mid-cycle. Full guide here.",
    "link": "https://sleepwisereviews.com/posts/power-nap-science.html",
    "image_url": "https://images.unsplash.com/photo-1510771463146-e89e6e86560e?w=800",
    "hashtags": ["napping", "powernap", "napsci", "sleephacks"]
  },
  {
    "title": "CBT-I: The Only Evidence-Based Insomnia Cure",
    "description": "Cognitive Behavioral Therapy for Insomnia outperforms sleep medication in every long-term study. And unlike pills, the effect GROWS over time. Here's what it involves.",
    "link": "https://sleepwisereviews.com/posts/cbt-i-guide.html",
    "image_url": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800",
    "hashtags": ["cbti", "insomniacure", "sleeptherapy", "cognitivebehavioral"]
  },
  {
    "title": "Night Owl vs. Morning Person: It's Mostly Genetics",
    "description": "Chronotype (whether you're a lark or owl) is 50% genetic. You can shift it by 1-2 hours with discipline. Shifting more than that fights your biology. Here's what works.",
    "link": "https://sleepwisereviews.com/posts/morning-lark-night-owl.html",
    "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800",
    "hashtags": ["chronotype", "morningperson", "nightowl", "circadianrhythm"]
  },
  {
    "title": "Sleep Stages Explained: What Happens in Each Stage",
    "description": "N1, N2, N3 (deep sleep), REM — each stage does something different. You cycle through 4-6 times per night. Interrupting any stage has specific consequences.",
    "link": "https://sleepwisereviews.com/posts/sleep-stages-explained.html",
    "image_url": "https://images.unsplash.com/photo-1587467512961-120760940315?w=800",
    "hashtags": ["sleepstages", "remslleep", "deepsleep", "sleepscience"]
  },
  {
    "title": "Sleep Improves Memory by 40% — Here's the Mechanism",
    "description": "During sleep, the hippocampus replays the day's events and transfers memories to long-term storage. Pulling an all-nighter before an exam is the worst possible strategy.",
    "link": "https://sleepwisereviews.com/posts/sleep-memory-learning.html",
    "image_url": "https://images.unsplash.com/photo-1456324504439-367cee3b3c32?w=800",
    "hashtags": ["sleepandmemory", "learningsleep", "brainhealth", "studytips"]
  },
  {
    "title": "Reset Your Sleep Schedule in 3 Days (Not 3 Weeks)",
    "description": "Pull forward (going to bed earlier): 15 min per night. Pull backward (staying up later): 1 hour per night. The math matters. Full reset protocol here.",
    "link": "https://sleepwisereviews.com/posts/reset-sleep-schedule.html",
    "image_url": "https://images.unsplash.com/photo-1494972308805-463bc619d34e?w=800",
    "hashtags": ["sleepschedule", "resetsleep", "circadianrhythm", "sleepfix"]
  },
  # ── Specific Populations ──────────────────────────────────────────────────
  {
    "title": "Why Women Sleep Worse Than Men (And What to Do About It)",
    "description": "Hormonal fluctuations across the menstrual cycle affect sleep architecture. Progesterone = sedating. Estrogen drop = lighter sleep. Evidence-based strategies inside.",
    "link": "https://sleepwisereviews.com/posts/women-sleep-differences.html",
    "image_url": "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?w=800",
    "hashtags": ["womenshealth", "womensleep", "hormones", "sleepforwomen"]
  },
  {
    "title": "Pregnancy Sleep Guide: Every Trimester Explained",
    "description": "First trimester: exhaustion from progesterone. Second: insomnia kicks in. Third: reflux + frequent urination. Evidence-based solutions for each stage.",
    "link": "https://sleepwisereviews.com/posts/pregnancy-sleep-guide.html",
    "image_url": "https://images.unsplash.com/photo-1490013616936-7190b0e5a5f3?w=800",
    "hashtags": ["pregnancysleep", "firsttrimester", "pregnancyhealth", "maternitytips"]
  },
  {
    "title": "Teen Sleep Crisis: Why Teenagers Can't Sleep Early",
    "description": "Puberty biologically shifts sleep timing 2-3 hours later. A teen with a 10:30pm sleep onset isn't being lazy — their melatonin just doesn't release until then.",
    "link": "https://sleepwisereviews.com/posts/teen-sleep-guide.html",
    "image_url": "https://images.unsplash.com/photo-1544717305-2782549b5136?w=800",
    "hashtags": ["teensleep", "adolescentsleep", "sleepteens", "parentingtips"]
  },
  {
    "title": "Kids Sleep Guide: How Much Sleep at Every Age",
    "description": "Newborns: 14-17 hrs. Toddlers: 11-14 hrs. School age: 9-11 hrs. Teens: 8-10 hrs. Most kids get 1-2 hrs less than they need. Impact on learning and behavior.",
    "link": "https://sleepwisereviews.com/posts/kids-sleep-guide.html",
    "image_url": "https://images.unsplash.com/photo-1555252333-9f8e92e65df9?w=800",
    "hashtags": ["kidssleep", "childrensleep", "parenting", "babysleep"]
  },
  {
    "title": "Menopause and Sleep: The Complete Guide",
    "description": "Hot flashes disrupt sleep architecture. Estrogen loss shortens REM. Night sweats cause cortisol spikes. Evidence-based interventions that don't require HRT.",
    "link": "https://sleepwisereviews.com/posts/menopause-sleep.html",
    "image_url": "https://images.unsplash.com/photo-1476703993599-0035a21b17a9?w=800",
    "hashtags": ["menopausesleep", "hotflashes", "womenshealth", "perimenopause"]
  },
  # ── Travel & Shift Work ───────────────────────────────────────────────────
  {
    "title": "Jet Lag Recovery: Beat It in Half the Time",
    "description": "Eastward travel is harder than westward. Melatonin timing matters. Light exposure is the master switch. This protocol beats jet lag in 2-3 days instead of 5-7.",
    "link": "https://sleepwisereviews.com/posts/jet-lag-guide.html",
    "image_url": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=800",
    "hashtags": ["jetlag", "travelhealth", "traveltips", "circadianrhythm"]
  },
  {
    "title": "Sleep on Planes, Trains, and Buses (Actually Work)",
    "description": "Position, noise, pressure, light — 4 variables that decide whether you sleep in transit. The gear that actually helps vs the stuff travelers waste money on.",
    "link": "https://sleepwisereviews.com/posts/sleep-travel-tips.html",
    "image_url": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=800",
    "hashtags": ["travelsleep", "planesteep", "travelgear", "businesstrip"]
  },
  # ── Exercise & Productivity ───────────────────────────────────────────────
  {
    "title": "Best Time to Exercise for Sleep Quality (Not When You Think)",
    "description": "Morning exercise advances your sleep phase (earlier sleep onset). Evening exercise (5-7pm) raises core temp beneficially — falling temp improves sleep quality. Late night (9pm+): skip it.",
    "link": "https://sleepwisereviews.com/posts/sleep-exercise-timing.html",
    "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800",
    "hashtags": ["exercisesleep", "workoutsleep", "fitnesshack", "sleepperformance"]
  },
  {
    "title": "Sleep and Productivity: Why 6 Hours Isn't Fine",
    "description": "After 17 hours awake, cognitive performance equals a blood alcohol of 0.05%. After 24 hours: 0.10% (legally drunk). You can't power through sleep deprivation.",
    "link": "https://sleepwisereviews.com/posts/sleep-productivity.html",
    "image_url": "https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=800",
    "hashtags": ["sleepproductivity", "workperformance", "sleephacks", "focustips"]
  },
  {
    "title": "How Sleep Makes You More Creative",
    "description": "REM sleep combines distant ideas — it's literally a creativity generator. The solution that came to you in the morning wasn't luck. It was your brain doing overnight work.",
    "link": "https://sleepwisereviews.com/posts/sleep-creativity.html",
    "image_url": "https://images.unsplash.com/photo-1452421822248-d4c2b47f0c81?w=800",
    "hashtags": ["sleepcreativiy", "creativesleep", "remsleep", "brainhacks"]
  },
  # ── Snoring & Apnea ──────────────────────────────────────────────────────
  {
    "title": "How to Stop Snoring: What Actually Works",
    "description": "Positional snoring vs anatomical vs apnea — different causes need different solutions. Mandibular devices beat anti-snoring pillows. Evidence-based comparison here.",
    "link": "https://sleepwisereviews.com/posts/snoring-causes-fixes.html",
    "image_url": "https://images.unsplash.com/photo-1518622358385-8ea7d0794bf6?w=800",
    "hashtags": ["snoring", "stopsnoringtips", "snoringfix", "sleepapnea"]
  },
  {
    "title": "Sleep Apnea Warning Signs Most People Miss",
    "description": "It's not just loud snoring. Gasping, headaches, dry mouth, daytime fatigue — all signs. Untreated apnea: 3x heart disease risk. Know the signs before it's serious.",
    "link": "https://sleepwisereviews.com/posts/sleep-apnea-warning-signs.html",
    "image_url": "https://images.unsplash.com/photo-1559757175-5700dde675bc?w=800",
    "hashtags": ["sleepapnea", "sleepapneasigns", "snoring", "sleepmedicine"]
  },
  # ── Supplements Deep Dives ────────────────────────────────────────────────
  {
    "title": "Melatonin: Complete Guide to Dose, Timing, and Type",
    "description": "Most people take 5-10mg. Studies show 0.3-0.5mg works better. Timing matters more than dose. Extended release vs fast release have different use cases. Full guide.",
    "link": "https://sleepwisereviews.com/posts/melatonin-guide.html",
    "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800",
    "hashtags": ["melatonin", "melatonindose", "sleepsupplement", "naturalsleep"]
  },
  {
    "title": "Magnesium Deficiency Signs That Are Destroying Your Sleep",
    "description": "Restless legs, muscle cramps, racing thoughts at night, 3am waking — all signs of low magnesium. The test most doctors don't run. How to fix it.",
    "link": "https://sleepwisereviews.com/posts/magnesium-deficiency-sleep.html",
    "image_url": "https://images.unsplash.com/photo-1585776245991-cf89dd7fc73a?w=800",
    "hashtags": ["magnesiumdeficiency", "magnesiumsleep", "mineraldeficiency", "sleepfix"]
  },
  {
    "title": "Valerian Root: Does It Actually Help Sleep?",
    "description": "Valerian binds to GABA receptors similar to benzodiazepines — but milder, no dependence. Works better with 4-6 weeks of consistent use than single nights. Evidence review.",
    "link": "https://sleepwisereviews.com/posts/best-valerian-root-supplements.html",
    "image_url": "https://images.unsplash.com/photo-1466692476868-aef1dfb1e735?w=800",
    "hashtags": ["valerianroot", "naturalsleepaid", "sleepsupplements", "herbalsleep"]
  },
  # ── Mattress & Bedding ────────────────────────────────────────────────────
  {
    "title": "Memory Foam vs Hybrid Mattress: Which Is Right for You?",
    "description": "Memory foam: motion isolation, pressure relief, runs hot. Hybrid: cooler, edge support, better for heavier people. The side sleeper vs back sleeper guide.",
    "link": "https://sleepwisereviews.com/posts/memory-foam-vs-hybrid-mattress.html",
    "image_url": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800",
    "hashtags": ["mattressguide", "memoryfoan", "hybridmattress", "mattressbuying"]
  },
  {
    "title": "How to Buy a Mattress Without Getting Ripped Off",
    "description": "Mattress stores mark up 50-75%. The best mattresses are online-only brands. What specs actually predict comfort. How to interpret trial periods. Complete buyer's guide.",
    "link": "https://sleepwisereviews.com/posts/mattress-buying-guide.html",
    "image_url": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800",
    "hashtags": ["mattressbuyingguide", "bestmattress", "mattresstips", "sleepinvestment"]
  },
  # ── Sleep Tracking ────────────────────────────────────────────────────────
  {
    "title": "Sleep Tracking Rings: Oura vs Others — 60-Day Test",
    "description": "Oura matched clinical polysomnography at 79% accuracy. Fitbit: 68%. Apple Watch: 71%. If you're spending money on a sleep tracker, here's the data to guide you.",
    "link": "https://sleepwisereviews.com/posts/best-sleep-tracking-rings.html",
    "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800",
    "hashtags": ["ouraringng", "sleeptracker", "wearables", "sleeptech"]
  },
  {
    "title": "Is Sleep Tracking Worth It? Honest Assessment",
    "description": "Sleep trackers help some people, harm others. 'Orthosomnia' (obsessing over sleep score) is real. When tracking helps vs when it makes sleep worse. Read before buying.",
    "link": "https://sleepwisereviews.com/posts/sleep-tracking-worth-it.html",
    "image_url": "https://images.unsplash.com/photo-1510771463146-e89e6e86560e?w=800",
    "hashtags": ["sleeptracking", "ouraing", "sleepatach", "quantifiedself"]
  },
  # ── Circadian & Chronobiology ─────────────────────────────────────────────
  {
    "title": "Your Circadian Rhythm: What It Is and How to Hack It",
    "description": "Your internal clock controls sleep, metabolism, immune function, and mood. Light is the master signal. These 4 inputs dominate everything else combined.",
    "link": "https://sleepwisereviews.com/posts/circadian-rhythm-basics.html",
    "image_url": "https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=800",
    "hashtags": ["circadianrhythm", "bioclock", "sleepscience", "chronobiology"]
  },
  {
    "title": "Social Jet Lag: The Hidden Sleep Problem Affecting Millions",
    "description": "If your weekday and weekend sleep schedules differ by 2+ hours, you have social jet lag. It's associated with obesity, depression, and poor academic performance.",
    "link": "https://sleepwisereviews.com/posts/social-jetlag.html",
    "image_url": "https://images.unsplash.com/photo-1520206183501-b80df61043c2?w=800",
    "hashtags": ["socialjetlag", "circadianrhythm", "weekendsleep", "sleepdisruption"]
  },
  # ── Seasonal Sleep ────────────────────────────────────────────────────────
  {
    "title": "How to Sleep Better in Summer Heat (Without AC All Night)",
    "description": "Cooling sheets, strategic fans, cold showers at the right time, and the wet sock method (it works). Complete summer sleep survival guide for hot climates.",
    "link": "https://sleepwisereviews.com/posts/summer-sleep-guide.html",
    "image_url": "https://images.unsplash.com/photo-1504701954957-2010ec3bcec1?w=800",
    "hashtags": ["summersleep", "heatandsleep", "sleepinheat", "coolingsleep"]
  },
  {
    "title": "Winter Sleep Tips: Dark Mornings and Shorter Days",
    "description": "Less light = more melatonin = harder to wake up and lower mood. Light therapy lamps solve this in 2 weeks. The winter sleep protocol that keeps your clock stable.",
    "link": "https://sleepwisereviews.com/posts/winter-sleep-guide.html",
    "image_url": "https://images.unsplash.com/photo-1511131341194-24e2eeeebb09?w=800",
    "hashtags": ["wintersleep", "lighttherapy", "sad", "seasonalsleep"]
  },
  # ── Sleep Journals & Habits ───────────────────────────────────────────────
  {
    "title": "Sleep Journal Method: Track Your Way to Better Sleep",
    "description": "A 7-day sleep journal reveals patterns you'd never notice otherwise: which nights you sleep best, which habits correlate with bad nights. Template and guide here.",
    "link": "https://sleepwisereviews.com/posts/sleep-journal-guide.html",
    "image_url": "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=800",
    "hashtags": ["sleepjournal", "sleeptracker", "sleephabits", "selfimprovement"]
  },
  {
    "title": "Morning Habits That Supercharge Sleep Quality Tonight",
    "description": "What you do in the first 30 minutes of your day determines how easily you'll sleep 16 hours later. Light, food timing, and exercise all set your circadian anchor.",
    "link": "https://sleepwisereviews.com/posts/morning-habits-sleep.html",
    "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800",
    "hashtags": ["morninghabits", "morningroutine", "sleepprep", "circadianrhythm"]
  },
  # ── Additional Product Pins ───────────────────────────────────────────────
  {
    "title": "Best Sleep Masks Tested: Blackout vs Silk vs Contour",
    "description": "A sleep mask that leaks light is useless. We tested 9 masks for blackout percentage, weight, and breathability. The $12 winner beat the $40 brand names.",
    "link": "https://sleepwisereviews.com/posts/best-sleep-masks.html",
    "image_url": "https://images.unsplash.com/photo-1611604548018-d56bbd85d681?w=800",
    "hashtags": ["sleepmask", "blackoutsleep", "eyemask", "sleepgear"]
  },
  {
    "title": "Best Sleep Headphones for Side Sleepers (No Ear Pain)",
    "description": "Standard headphones crush your ear if you sleep on your side. Headband speakers, ultra-thin buds, and bone conduction all solve this differently. What works best.",
    "link": "https://sleepwisereviews.com/posts/best-sleep-headphones.html",
    "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800",
    "hashtags": ["sleepheadphones", "whitenoiesleep", "sleepsound", "sidesleeper"]
  },
  {
    "title": "Light Therapy Lamps: How to Use Them for Better Sleep",
    "description": "10,000 lux for 20-30 minutes within 30 minutes of waking resets your circadian clock. Which lamps hit 10,000 lux vs which lie about it. Tested results.",
    "link": "https://sleepwisereviews.com/posts/best-light-therapy-lamps.html",
    "image_url": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=800",
    "hashtags": ["lighttherapy", "sad", "seasonaldepression", "circadianlight"]
  },
  {
    "title": "Cooling Mattress Pads: Do They Actually Help Sleep?",
    "description": "Active cooling pads (ChiliSleep, Eight Sleep) drop mattress temp by 15°F. Passive toppers cool 2-3°F. The difference matters. Which one works for your budget.",
    "link": "https://sleepwisereviews.com/posts/best-cooling-mattress-pads.html",
    "image_url": "https://images.unsplash.com/photo-1567468788249-b12c40fe4e4b?w=800",
    "hashtags": ["coolingmattress", "hottsleeper", "bedtemp", "sleeptemperature"]
  },
  {
    "title": "Blue Light Glasses: Which Ones Actually Block Sleep-Disrupting Light",
    "description": "Most blue light glasses block 5-20% of blue light. You need ones that block 90%+ of 450-480nm range. How to check the specs, and our top picks.",
    "link": "https://sleepwisereviews.com/posts/best-blue-light-glasses.html",
    "image_url": "https://images.unsplash.com/photo-1574258495973-f010dfbb5371?w=800",
    "hashtags": ["bluelightglasses", "bluelight", "screentime", "sleephygiene"]
  },
  {
    "title": "Humidifiers for Sleep: Right Humidity Is 40-60%",
    "description": "Dry air causes micro-awakenings, dry throat, and congestion. Under 30% humidity: bad sleep. Over 60%: mold risk. Best humidifiers that maintain the sweet spot.",
    "link": "https://sleepwisereviews.com/posts/best-humidifiers-sleep.html",
    "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800",
    "hashtags": ["humidifier", "bedroomhumidity", "dryair", "sleepenv"]
  },
  {
    "title": "Best Aromatherapy for Sleep: The Evidence Behind the Scents",
    "description": "Lavender reduces sleep onset by 9 minutes in clinical trials. Bergamot and chamomile have supporting evidence too. Which products deliver actual therapeutic concentration.",
    "link": "https://sleepwisereviews.com/posts/best-aromatherapy-sleep.html",
    "image_url": "https://images.unsplash.com/photo-1600334089648-b0d9d3028eb2?w=800",
    "hashtags": ["aromatherapy", "lavandersleep", "essentialoils", "naturalsleep"]
  },
  {
    "title": "Grounding Sheets: Real Science or Sleep Wellness Hype?",
    "description": "Earthing/grounding reduces cortisol and synchronizes cortisol rhythm to natural cycles in two peer-reviewed studies. It's not magic — it's electron transfer. Honest review.",
    "link": "https://sleepwisereviews.com/posts/best-grounding-sheets.html",
    "image_url": "https://images.unsplash.com/photo-1519699047748-de8e457a634e?w=800",
    "hashtags": ["groundingsheets", "earthing", "grounding", "sleepwellness"]
  },
  {
    "title": "CPAP Alternatives for Mild Sleep Apnea",
    "description": "If CPAP compliance is a problem, mandibular advancement devices, positional therapy, and EPAP devices all have clinical evidence for mild-moderate apnea. Comparison guide.",
    "link": "https://sleepwisereviews.com/posts/best-cpap-alternatives.html",
    "image_url": "https://images.unsplash.com/photo-1559757175-5700dde675bc?w=800",
    "hashtags": ["cpap", "cpapalternative", "sleepapnea", "breathingsleep"]
  },
  {
    "title": "Smart Mattresses Worth Buying in 2026",
    "description": "Eight Sleep, Sleep Number, ReST — do smart mattresses improve sleep enough to justify $2,000-$4,000? The data from 6 months of testing. Honest ROI analysis.",
    "link": "https://sleepwisereviews.com/posts/best-smart-mattresses.html",
    "image_url": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800",
    "hashtags": ["smartmattress", "eightsleep", "sleepnumber", "slleeptech"]
  },
  {
    "title": "Sleep Apps That Actually Improve Sleep (Not Just Track It)",
    "description": "Headspace Sleep, Calm, Pzizz, and Slumber all promise better sleep. Which ones have evidence behind the claims. Which are just audio players. Honest breakdown.",
    "link": "https://sleepwisereviews.com/posts/best-sleep-apps.html",
    "image_url": "https://images.unsplash.com/photo-1512428813834-c702c7702b78?w=800",
    "hashtags": ["sleepapp", "meditationsleep", "sleepaudio", "insomniapp"]
  },
  # ── Sleep and Specific Conditions ─────────────────────────────────────────
  {
    "title": "Sleep and Skin Health: The Beauty Sleep Science",
    "description": "Collagen production peaks during deep sleep. Growth hormone (released at sleep onset) drives skin repair. Consistently bad sleep = 30% more fine lines in 6 weeks.",
    "link": "https://sleepwisereviews.com/posts/sleep-skin-health.html",
    "image_url": "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?w=800",
    "hashtags": ["beautysleep", "skinandsleep", "collagen", "skincare"]
  },
  {
    "title": "Sleep and Mental Health: The Bidirectional Link",
    "description": "Poor sleep causes depression. Depression causes poor sleep. The loop is real and vicious. Breaking it requires addressing both sides simultaneously. Evidence-based guide.",
    "link": "https://sleepwisereviews.com/posts/sleep-mental-health.html",
    "image_url": "https://images.unsplash.com/photo-1499084732479-de2c02d45fd4?w=800",
    "hashtags": ["sleepmentalhealth", "depressionlsleep", "mentalhealth", "anxiety"]
  },
  {
    "title": "Sleep and Longevity: Why Matthew Walker Calls It the Elixir of Life",
    "description": "Every study linking short sleep to earlier mortality. What the data says about the optimal sleep duration for lifespan. It's not 8 hours — it's 7-8 hours.",
    "link": "https://sleepwisereviews.com/posts/sleep-longevity.html",
    "image_url": "https://images.unsplash.com/photo-1559757175-5700dde675bc?w=800",
    "hashtags": ["sleeplongevity", "longevity", "sleephealth", "aginghacks"]
  },
  {
    "title": "Sleep and Immune System: Why You Get Sick When Sleep-Deprived",
    "description": "Sleeping under 6 hours makes you 4x more likely to catch a cold. Cytokine production, T-cell function, and antibody response all drop dramatically with sleep loss.",
    "link": "https://sleepwisereviews.com/posts/sleep-immune-system.html",
    "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800",
    "hashtags": ["sleepimmune", "immunesystem", "getsicksleep", "healthysleep"]
  },
  {
    "title": "Sleep and Gut Health: Your Gut Bacteria Follow Your Sleep Clock",
    "description": "Gut microbiome diversity reduces by 50% with just 2 nights of poor sleep. Irregular sleep timing disrupts gut bacteria more than diet alone. The bidirectional relationship.",
    "link": "https://sleepwisereviews.com/posts/sleep-and-gut-health.html",
    "image_url": "https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=800",
    "hashtags": ["sleepguthealth", "microbiome", "gutsleep", "guthealth"]
  },
  {
    "title": "Brain During Sleep: Hour-by-Hour Breakdown",
    "description": "Hour 1: falling asleep. Hour 2: first deep sleep. Hour 4: first full REM. Hour 6: maximum REM pressure. What your brain is doing at each stage throughout the night.",
    "link": "https://sleepwisereviews.com/posts/brain-during-sleep.html",
    "image_url": "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800",
    "hashtags": ["brainsleep", "sleepscience", "neuroscience", "sleepcycles"]
  },
  # ── Food + Sleep ──────────────────────────────────────────────────────────
  {
    "title": "Foods That Help You Sleep (Backed by Science)",
    "description": "Tart cherry: melatonin. Kiwi: serotonin. Turkey: tryptophan. Walnuts: melatonin + omega-3. The foods that improve sleep quality vs the ones that wreck it.",
    "link": "https://sleepwisereviews.com/posts/sleep-food-connection.html",
    "image_url": "https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=800",
    "hashtags": ["foodforsleep", "sleepfoods", "tartcherry", "sleepdiet"]
  },
  # ── Additional Pins for Existing High-Value Posts ─────────────────────────
  {
    "title": "Side Sleeper Pillow: Exactly What to Look For",
    "description": "High loft (5-6 inches). Medium-firm. Adjustable fill = best option. Our 60-night test compared 8 pillows across these metrics. The winner costs under $60.",
    "link": "https://sleepwisereviews.com/posts/best-pillow-side-sleepers.html",
    "image_url": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800",
    "hashtags": ["sidesleeeper", "pillowsupport", "neckpain", "sleeppillow"]
  },
  {
    "title": "Pregnancy Pillow: C vs U vs Wedge — What's Right for You?",
    "description": "C-shaped: full body support, great if you have a partner sharing the bed. U-shaped: most support, takes up more space. Wedge: targeted bump support, smallest. Comparison here.",
    "link": "https://sleepwisereviews.com/posts/best-pregnancy-pillows.html",
    "image_url": "https://images.unsplash.com/photo-1490013616936-7190b0e5a5f3?w=800",
    "hashtags": ["pregnancypillow", "maternitypillow", "pregnancysleep", "momsleep"]
  },
  {
    "title": "Weighted Blanket: How to Choose the Right Weight",
    "description": "10% of body weight is the starting guideline. But it's actually 8-12% depending on your preference. Too heavy: sleep disturbance. Too light: no benefit. Full guide.",
    "link": "https://sleepwisereviews.com/posts/article-weighted-blanket.html",
    "image_url": "https://images.unsplash.com/photo-1582149547059-eb1c0af88b8f?w=800",
    "hashtags": ["weightedblanket", "sensoryprocessing", "weightedblanketguide", "anxietyblanket"]
  },
  {
    "title": "Sunrise Alarm Clocks: Do They Make Waking Up Easier?",
    "description": "Light gradually increases 20-30 minutes before alarm time. Suppresses residual melatonin. Result: 63% report easier waking in clinical trial. The models that actually work.",
    "link": "https://sleepwisereviews.com/posts/best-sunrise-alarm-clocks.html",
    "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800",
    "hashtags": ["sunriseclock", "lightalarm", "wakeupeasy", "morningroutine"]
  },
  {
    "title": "Earplugs for Sleeping: NRR 33 Is What You Actually Need",
    "description": "NRR 33 blocks ~22 real-world dB. That's enough to reduce a snoring partner from 70dB to 48dB — below the sleep disruption threshold. The $15 option that delivers.",
    "link": "https://sleepwisereviews.com/posts/best-earplugs-sleeping.html",
    "image_url": "https://images.unsplash.com/photo-1594744803329-e58b31de8bf5?w=800",
    "hashtags": ["earplugs", "sleepnoise", "snoring", "bettersleep"]
  },
  {
    "title": "Mattress for Back Pain: Firmness Is Not the Answer",
    "description": "Medium-firm beats firm and soft for lumbar support in people under 200 lbs. Over 200 lbs: hybrid medium. The research-backed mattress selection guide for bad backs.",
    "link": "https://sleepwisereviews.com/posts/best-mattresses-back-pain.html",
    "image_url": "https://images.unsplash.com/photo-1486739985386-d4fae04ca6f7?w=800",
    "hashtags": ["backpainmattress", "mattressforback", "lumbarsupport", "sleepbackpain"]
  },
  {
    "title": "Best Mattresses Under $500 That Outperform $2,000 Brands",
    "description": "We pressure-tested 9 beds under $500. Three outscored mattresses at 3x the price. What foam layers and coil count actually matter vs what's marketing.",
    "link": "https://sleepwisereviews.com/posts/best-mattresses-under-500.html",
    "image_url": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800",
    "hashtags": ["cheapmattress", "budgetmattress", "mattressreview", "bestvalue"]
  },
]

def main():
    existing = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
    combined = existing + NEW_PINS
    QUEUE_FILE.write_text(json.dumps(combined, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Queue expanded: {len(existing)} -> {len(combined)} pins")
    print(f"Days at 4/day: {len(combined) // 4}")

if __name__ == "__main__":
    main()
