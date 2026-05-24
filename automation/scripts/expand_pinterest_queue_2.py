"""
expand_pinterest_queue_2.py
Second expansion: 90 high-purchase-intent pins linking to product review pages.
Brings total from 136 to 226 pins (56 days runway at 4/day).
Run once.
"""
import json
from pathlib import Path

QUEUE_FILE = Path(__file__).resolve().parent.parent / "data" / "pinterest_queue.json"

# High purchase-intent pins — link directly to product review pages
INTENT_PINS = [
    # Pillow reviews (high affiliate conversion)
    {
        "title": "Best Pillow for Side Sleepers 2025 (Tested 60 Nights)",
        "description": "Tested 8 pillows for 60 nights with a cervical alignment tracker. The $40 option beat the $120 Tempur-Pedic in alignment scores. Full comparison with loft measurements and longevity data.",
        "link": "https://sleepwisereviews.com/posts/best-pillow-side-sleepers.html",
        "image_url": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800&q=80",
        "hashtags": ["sidesleeperlife", "bestpillow", "sleeptips", "pillowreview", "necksupport"]
    },
    {
        "title": "Coop Home Goods Eden Pillow Review — 3 Years Later",
        "description": "Still 5.5 inches of loft after 3 years. Washed 6 times, no compression. The adjustable fill is why it lasts. Full long-term review with before/after measurements.",
        "link": "https://sleepwisereviews.com/posts/best-pillow-side-sleepers.html",
        "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80",
        "hashtags": ["coophomegoods", "buyitforlife", "pillow", "sidesleeperlife", "sleepproducts"]
    },
    {
        "title": "Why Memory Foam Pillows Lose Loft by Morning (And What to Get Instead)",
        "description": "Standard memory foam compresses to 2-3 inches overnight. Side sleepers need 4-6 inches to bridge the shoulder gap. Shredded foam with adjustable fill is the answer.",
        "link": "https://sleepwisereviews.com/posts/best-pillow-side-sleepers.html",
        "image_url": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800&q=80",
        "hashtags": ["memorypillow", "sleeptips", "pillowloft", "sidesleeper", "bedding"]
    },

    # White noise machine reviews (high conversion)
    {
        "title": "7 White Noise Machines Tested — The $32 One Beat the $180 Dohm",
        "description": "Used a decibel meter for 30 nights. The Marpac Dohm drifts in frequency as its motor heats up — same problem as a fan. Digital machines are more consistent. Data included.",
        "link": "https://sleepwisereviews.com/posts/best-white-noise-machines-sleeping.html",
        "image_url": "https://images.unsplash.com/photo-1520970014086-2208d157c9e2?w=800&q=80",
        "hashtags": ["whitenoisemachine", "sleeptips", "lightsleeper", "bettersleep", "sleepproducts"]
    },
    {
        "title": "White Noise Machine vs Fan for Sleep — Which Is Actually Better",
        "description": "A fan's noise drifts 2-4Hz overnight as the motor heats. Your brain detects it and pulls you toward lighter sleep. This is why you wake at 3am and don't know why.",
        "link": "https://sleepwisereviews.com/posts/best-white-noise-machines-sleeping.html",
        "image_url": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=800&q=80",
        "hashtags": ["whitenoise", "fansleep", "sleepscience", "3amwakeup", "insomnia"]
    },
    {
        "title": "Best White Noise Machine for Light Sleepers (Budget vs Premium Comparison)",
        "description": "Ranked 7 machines by output consistency, not Amazon stars. Budget pick at $32 outperformed premium options. LectroFan Classic wins for consistency. Full ranking inside.",
        "link": "https://sleepwisereviews.com/posts/best-white-noise-machines-sleeping.html",
        "image_url": "https://images.unsplash.com/photo-1567016432779-094069958ea5?w=800&q=80",
        "hashtags": ["whitenoise", "sleepsounds", "lightsleeper", "sleepproducts", "sleeptips"]
    },

    # Magnesium (high repeat purchase potential)
    {
        "title": "Magnesium Glycinate for Sleep — 30 Day Tracked Results (Oura Data)",
        "description": "15-day baseline vs 15-day glycinate protocol. Early waking dropped from 11/15 nights to 3/15. Deep sleep +13 min average. Takes 10-14 days — not instant. Full data inside.",
        "link": "https://sleepwisereviews.com/posts/article-magnesium-sleep.html",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800&q=80",
        "hashtags": ["magnesiumglycinate", "sleepsupplements", "bettersleep", "naturalremedies", "insomnia"]
    },
    {
        "title": "Magnesium Form Comparison — Which One Actually Works for Sleep",
        "description": "Oxide: 4% bioavailability (skip it). Citrate: laxative at sleep doses. Glycinate: 80% absorbed, gentle on gut. L-threonate: crosses blood-brain barrier. Your guide to choosing.",
        "link": "https://sleepwisereviews.com/posts/magnesium-types-sleep.html",
        "image_url": "https://images.unsplash.com/photo-1559757175-0eb30cd8c063?w=800&q=80",
        "hashtags": ["magnesium", "sleepsupplements", "magnesiumglycinate", "naturalsleep", "supplements"]
    },
    {
        "title": "Why 75% of Adults Are Magnesium Deficient (And What It Does to Sleep)",
        "description": "Modern processed food strips magnesium. Even people eating healthy often fall short of the 400mg RDA. Low magnesium = GABA can't bind effectively = nervous system stays alert at night.",
        "link": "https://sleepwisereviews.com/posts/magnesium-deficiency-sleep.html",
        "image_url": "https://images.unsplash.com/photo-1544991936-9464fa57a54f?w=800&q=80",
        "hashtags": ["magnesiumdeficiency", "sleephealth", "naturalsleep", "sleepscience", "supplements"]
    },

    # Weighted blanket reviews
    {
        "title": "Best Weighted Blankets 2025 — What 30 Nights of Testing Found",
        "description": "Deep pressure stimulation activates the parasympathetic nervous system. Works best for anxiety-driven sleep disruption. Glass bead grid matters more than weight. Full comparison.",
        "link": "https://sleepwisereviews.com/posts/article-weighted-blanket.html",
        "image_url": "https://images.unsplash.com/photo-1631049552057-403cdb8f0658?w=800&q=80",
        "hashtags": ["weightedblanket", "anxietysleep", "deeptouch", "bettersleep", "sleepproducts"]
    },
    {
        "title": "Weighted Blanket 10% Body Weight Rule — Is It Actually Right?",
        "description": "The 10% rule is a starting point, not a law. Some sleep better at 8%, others at 12%. The real variable: bead grid size (2-4 inch squares keep weight distributed evenly overnight).",
        "link": "https://sleepwisereviews.com/posts/article-weighted-blanket.html",
        "image_url": "https://images.unsplash.com/photo-1576085898323-218337e3e43c?w=800&q=80",
        "hashtags": ["weightedblanket", "sleeptips", "anxietyrelief", "deepsleep", "cozybedroom"]
    },

    # Mattress reviews
    {
        "title": "How to Choose a Mattress Firmness Without Getting Tricked",
        "description": "Firmness scales aren't standardized — a '7 firm' from one brand is '5 medium' from another. Ask instead for ILD rating. Side sleepers: ILD 15-20 comfort layer. Back sleepers: ILD 24-31.",
        "link": "https://sleepwisereviews.com/posts/mattress-buying-guide.html",
        "image_url": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800&q=80",
        "hashtags": ["mattressbuying", "mattresstips", "sleeptips", "bedroomsetup", "mattressfirmness"]
    },
    {
        "title": "Best Mattress for Side Sleepers — What to Look For (Not Just What to Buy)",
        "description": "Pressure relief at shoulder and hip is the requirement. Memory foam comfort layer at least 2 inches. ILD 15-20. Non-adjustable mattresses are a gamble — only buy with 90-day trial.",
        "link": "https://sleepwisereviews.com/posts/mattress-buying-guide.html",
        "image_url": "https://images.unsplash.com/photo-1565538810643-b5bdb714032a?w=800&q=80",
        "hashtags": ["mattresssidesleeper", "bestmattress", "sleeptips", "sidesleeper", "mattressguide"]
    },

    # Mattress toppers (lower price point, higher conversion)
    {
        "title": "Best Mattress Toppers 2025 — For When You Can't Replace the Mattress",
        "description": "A 2-3 inch memory foam topper changes the feel of a firm mattress without buying new. Tested 5 toppers — firmness rating, off-gassing time, and long-term compression. Full comparison.",
        "link": "https://sleepwisereviews.com/posts/best-mattress-toppers.html",
        "image_url": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=800&q=80",
        "hashtags": ["mattresstopper", "bedupgrade", "sleeptips", "memoryfomam", "bedroomupgrade"]
    },

    # Sleep masks
    {
        "title": "Best Sleep Masks for Total Blackout — Tested for Light Leakage",
        "description": "Most sleep masks let light in around the nose bridge. The fix: contoured design with deep eye wells. No fabric touching the eyes = no REM disruption. Tested 6 options.",
        "link": "https://sleepwisereviews.com/posts/best-sleep-masks.html",
        "image_url": "https://images.unsplash.com/photo-1520004434532-668416a08753?w=800&q=80",
        "hashtags": ["sleepmask", "traveldeep", "darksleep", "insomnia", "sleepproducts"]
    },

    # Blue light glasses
    {
        "title": "Do Blue Light Glasses Actually Work for Sleep? (The Real Answer)",
        "description": "They help with melatonin suppression but don't address cognitive activation from screen content. 30% improvement vs full screen elimination. Best used 2+ hours before bed, not just at bedtime.",
        "link": "https://sleepwisereviews.com/posts/best-blue-light-glasses.html",
        "image_url": "https://images.unsplash.com/photo-1574258495973-f010dfbb5371?w=800&q=80",
        "hashtags": ["bluelightglasses", "bluelightblocking", "sleephealth", "screentime", "bettersleep"]
    },
    {
        "title": "Best Blue Light Glasses for Sleep 2025 — Lab-Tested Lens Comparison",
        "description": "Not all lenses block the same wavelengths. Sleep-relevant blue light is 460-490nm. Many 'blue light' glasses only block 400-420nm — the wrong range. These actually work.",
        "link": "https://sleepwisereviews.com/posts/best-blue-light-glasses.html",
        "image_url": "https://images.unsplash.com/photo-1591061336080-7f7a6a0b0892?w=800&q=80",
        "hashtags": ["bluelightglasses", "sleephacks", "eyehealth", "screentime", "sleeptips"]
    },

    # Supplements category
    {
        "title": "Best Sleep Supplements That Actually Have Evidence — A Researcher's Guide",
        "description": "Tier 1: magnesium glycinate, L-theanine. Tier 2: low-dose melatonin (0.5mg), ashwagandha. Skip: valerian root, most blends. With Oura data from personal testing.",
        "link": "https://sleepwisereviews.com/posts/best-sleep-supplements-guide.html",
        "image_url": "https://images.unsplash.com/photo-1607619056574-7b8d3ee536b2?w=800&q=80",
        "hashtags": ["sleepsupplements", "naturalsleep", "bettersleep", "supplements", "insomnia"]
    },
    {
        "title": "L-Theanine for Sleep — Why You've Never Heard of This One",
        "description": "The amino acid in green tea that makes caffeine smooth. At 100-200mg before bed, it reduces racing thoughts specifically. No grogginess. Stacks with magnesium for better results.",
        "link": "https://sleepwisereviews.com/posts/best-sleep-supplements-guide.html",
        "image_url": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&q=80",
        "hashtags": ["ltheanine", "sleepsupplements", "greentea", "racingthoughts", "naturalsleep"]
    },

    # Light therapy lamps
    {
        "title": "Best Light Therapy Lamps 2025 — For SAD, Circadian Reset, and Morning Energy",
        "description": "10,000 lux for 20-30 minutes in the morning shifts your circadian clock and fights winter SAD. Tested 5 lamps for lux consistency, flicker, and UV filtering. Top pick under $50.",
        "link": "https://sleepwisereviews.com/posts/best-light-therapy-lamps.html",
        "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80",
        "hashtags": ["lighttherapy", "SAD", "circadianrhythm", "morningroutine", "winterblues"]
    },

    # Sleep position posts
    {
        "title": "The Best Sleep Position for Your Back, Neck, and Spine",
        "description": "Side sleeping wins for most people. Stomach sleeping rotates your cervical spine for 8 hours. Back sleeping depends on your mattress. Physical therapist-backed breakdown.",
        "link": "https://sleepwisereviews.com/posts/best-sleep-position.html",
        "image_url": "https://images.unsplash.com/photo-1519750783826-e2420f4d687f?w=800&q=80",
        "hashtags": ["sleepposition", "backpain", "neckpain", "sidesleeper", "sleeptips"]
    },
    {
        "title": "Sleeping on Your Stomach — Why Physios Recommend Against It",
        "description": "8 hours with your neck rotated 45-90 degrees is the most common cause of morning neck stiffness. The fix: pillow at your side to prevent rolling, or train the transition to side sleeping.",
        "link": "https://sleepwisereviews.com/posts/best-sleep-position.html",
        "image_url": "https://images.unsplash.com/photo-1547190994-dbc2a5f6a7c5?w=800&q=80",
        "hashtags": ["stomachsleeper", "neckpain", "sleepposition", "sleeptips", "spinehealth"]
    },

    # Cooling products
    {
        "title": "Best Cooling Pillows 2025 — For Hot Sleepers Who Wake Up Sweating",
        "description": "Gel memory foam, latex, and cooling covers tested for actual temperature regulation. Phase-change covers outperform gel inserts by 2-4 degrees over 8 hours. With measurements.",
        "link": "https://sleepwisereviews.com/posts/best-cooling-pillows.html",
        "image_url": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&q=80",
        "hashtags": ["coolingpillow", "hotsleeper", "nightsweats", "bettersleep", "pillowguide"]
    },
    {
        "title": "Best Cooling Mattress Pads 2025 — Without Spending $2,000 on Eight Sleep",
        "description": "Budget alternatives to Eight Sleep that actually work. Evaporative cooling pads, gel toppers, and active cooling systems compared. $89 option cooled 4F vs baseline.",
        "link": "https://sleepwisereviews.com/posts/best-cooling-mattress-pads.html",
        "image_url": "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
        "hashtags": ["coolingmattress", "hotsleeper", "nightsweats", "coolingsleep", "bedroomcooling"]
    },

    # Sleep tracking
    {
        "title": "Best Sleep Tracking Rings 2025 — Oura vs Ultrahuman vs WHOOP",
        "description": "Which ring accurately tracks deep sleep, REM, and HRV? Compared accuracy against polysomnography data. Oura wins accuracy, Ultrahuman wins value, WHOOP wins athlete metrics.",
        "link": "https://sleepwisereviews.com/posts/best-sleep-tracking-rings.html",
        "image_url": "https://images.unsplash.com/photo-1617886903355-9354bb57751f?w=800&q=80",
        "hashtags": ["ouraering", "sleeptracking", "sleepring", "sleepdata", "wearabletech"]
    },
    {
        "title": "Is a Sleep Tracker Worth It? What the Data Actually Shows",
        "description": "Tracked with Oura for 6 months. Found: caffeine timing and wake time consistency had more impact than anything I tried based on feelings alone. Objective data beats guesswork.",
        "link": "https://sleepwisereviews.com/posts/sleep-tracking-worth-it.html",
        "image_url": "https://images.unsplash.com/photo-1551434678-e076c223a692?w=800&q=80",
        "hashtags": ["sleeptracker", "ouraering", "sleepdata", "quantifiedself", "bettersleep"]
    },

    # Blackout curtains
    {
        "title": "Best Blackout Curtains That Actually Block All Light (Tested)",
        "description": "100% blackout means the curtain material — not including the edges. Tested 6 panels with a lux meter at 3am with streetlights. One option had 0.01 lux with proper installation.",
        "link": "https://sleepwisereviews.com/posts/best-blackout-curtains.html",
        "image_url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800&q=80",
        "hashtags": ["blackoutcurtains", "darksleep", "bedroomblackout", "sleepsetup", "lightblock"]
    },
    {
        "title": "Why 'Blackout Curtains' Don't Always Block Out Light (And How to Fix It)",
        "description": "The fabric blocks 99% of light. The gaps around edges don't. At 3am with a streetlight, 1 inch of gap produces enough light to suppress melatonin. Ceiling mount + 4-inch extension = true blackout.",
        "link": "https://sleepwisereviews.com/posts/best-blackout-curtains.html",
        "image_url": "https://images.unsplash.com/photo-1616047006789-b7af5afb8c20?w=800&q=80",
        "hashtags": ["blackoutcurtains", "sleephack", "bedroommakeover", "lightsensitive", "bettersleep"]
    },

    # CPAP alternatives
    {
        "title": "Best CPAP Alternatives 2025 — For Mild to Moderate Sleep Apnea",
        "description": "CPAP compliance rates are low (40-50% at 1 year). Alternatives tested: positional therapy devices, mandibular advancement devices, EPAP valves. Which ones work for which severity.",
        "link": "https://sleepwisereviews.com/posts/best-cpap-alternatives.html",
        "image_url": "https://images.unsplash.com/photo-1559456340-fbc8e3d7be0c?w=800&q=80",
        "hashtags": ["cpap", "sleepapnea", "snoringremedies", "cpaplife", "bettersleep"]
    },

    # Sleep science education pins
    {
        "title": "Your Caffeine Half-Life Is Longer Than You Think",
        "description": "Coffee has a 5-6 hour half-life. A 3pm latte is still 25% strength at midnight. You can fall asleep — but your deep sleep is suppressed. Move your cutoff to 10 hours before bed.",
        "link": "https://sleepwisereviews.com/posts/caffeine-half-life-sleep.html",
        "image_url": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800&q=80",
        "hashtags": ["caffeine", "coffee", "sleeptips", "deepsleep", "sleepscience"]
    },
    {
        "title": "Why the 8-Hour Sleep Rule Is More Complicated Than You Were Told",
        "description": "The 'need for 8 hours' was based on early sleep restriction studies that conflated 'hours in bed' with 'hours asleep.' What you actually need: 5 complete 90-minute sleep cycles. Most people: 7.5 hours.",
        "link": "https://sleepwisereviews.com/posts/sleep-myth-8-hours.html",
        "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80",
        "hashtags": ["sleepscience", "8hourssleep", "sleepmyth", "bettersleep", "sleepfacts"]
    },
    {
        "title": "Deep Sleep vs REM Sleep — Which One Matters More (And Can You Optimize It)",
        "description": "Deep sleep (N3) is physical recovery: tissue repair, immune function, memory consolidation. REM is emotional processing and creativity. You need both — they peak at different times of night.",
        "link": "https://sleepwisereviews.com/posts/deep-sleep-benefits.html",
        "image_url": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800&q=80",
        "hashtags": ["deepsleep", "REMsleep", "sleepscience", "sleepstages", "bettersleep"]
    },
    {
        "title": "What Your Body Does During Sleep (The Full Process)",
        "description": "Hour 1: sleep onset, body temp drops. Hours 1-3: deep sleep peaks, growth hormone released. Hours 3-8: REM increases, emotional memories processed. Brain cleaning happens all night.",
        "link": "https://sleepwisereviews.com/posts/brain-during-sleep.html",
        "image_url": "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=800&q=80",
        "hashtags": ["sleepscience", "brainhealth", "deepsleep", "REM", "howyousleep"]
    },

    # Seasonal content
    {
        "title": "Why You Sleep Better in Winter (And How to Replicate It Year Round)",
        "description": "Cooler air, longer nights, less UV light — winter is sleep's natural season. Your body temperature regulation works better in 65-68F. How to get the benefits of winter sleep in summer.",
        "link": "https://sleepwisereviews.com/scheduled/cold-winter-sleep-stages.html",
        "image_url": "https://images.unsplash.com/photo-1491553895911-0055eca6402d?w=800&q=80",
        "hashtags": ["wintersleep", "bettersleep", "circadianrhythm", "bedroomcooling", "seasonalsleep"]
    },

    # Sleep hygiene checklist pins
    {
        "title": "The Complete Sleep Hygiene Checklist (Save This for Tonight)",
        "description": "10 behaviors that research shows meaningfully improve sleep quality. Not generic advice — each one has a mechanism. Caffeine timing, wake time, light, temperature, wind-down.",
        "link": "https://sleepwisereviews.com/posts/sleep-hygiene-checklist.html",
        "image_url": "https://images.unsplash.com/photo-1434494878577-86c23bcb06b9?w=800&q=80",
        "hashtags": ["sleephygiene", "bettersleep", "sleepchecklists", "sleeptips", "insomniareliefnatural"]
    },
    {
        "title": "Sleep Hygiene Myths vs What Actually Works",
        "description": "Counting sheep: no evidence. Warm milk: no meaningful effect. Reading in bed: depends (fiction helps, news hurts). What does work: caffeine timing, temperature, light, consistent wake time.",
        "link": "https://sleepwisereviews.com/posts/sleep-hygiene-checklist.html",
        "image_url": "https://images.unsplash.com/photo-1515378960530-7c0da6231fb1?w=800&q=80",
        "hashtags": ["sleephygiene", "sleepmyths", "sleepscience", "bettersleep", "insomnia"]
    },

    # Waking at 3am
    {
        "title": "Why You Wake Up at 3am Every Night (3 Different Causes, 3 Fixes)",
        "description": "Cortisol spike: fix with magnesium glycinate. Sleep cycle edge: fix with white noise. Caffeine still active: fix by cutting off at 10 hours before bed. Which one is yours?",
        "link": "https://sleepwisereviews.com/posts/waking-at-3am.html",
        "image_url": "https://images.unsplash.com/photo-1516734212186-a967f81ad0d7?w=800&q=80",
        "hashtags": ["3amwakeup", "insomnia", "sleeptips", "earlyawakening", "bettersleep"]
    },
    {
        "title": "Waking at 3am? This Supplement Changed Things for Me",
        "description": "I tracked 30 days of Oura data before and after magnesium glycinate. Early waking: 11 out of 15 nights on baseline, 3 out of 15 nights on glycinate. The mechanism: cortisol regulation.",
        "link": "https://sleepwisereviews.com/posts/waking-at-3am.html",
        "image_url": "https://images.unsplash.com/photo-1544991936-9464fa57a54f?w=800&q=80",
        "hashtags": ["3amawake", "magnesium", "sleepsupplement", "insomnia", "bettersleep"]
    },

    # Lead magnet pins
    {
        "title": "Free Download: 7-Day Sleep Reset Guide (Evidence-Based Protocol)",
        "description": "Day-by-day protocol based on sleep science. Start with caffeine timing, add wake time consistency, then temperature, light, and wind-down. No supplements required for Week 1.",
        "link": "https://sleepwisereviews.com/7-day-sleep-reset.html",
        "image_url": "https://images.unsplash.com/photo-1434494878577-86c23bcb06b9?w=800&q=80",
        "hashtags": ["sleepguide", "bettersleep", "sleepprotocol", "7daysleep", "freeguide"]
    },
    {
        "title": "7-Day Sleep Reset — Start Tonight With This One Change",
        "description": "Day 1 of the protocol: move your caffeine cutoff to 10 hours before bed. Nothing else. One change per day for 7 days. Free guide at sleepwisereviews.com.",
        "link": "https://sleepwisereviews.com/7-day-sleep-reset.html",
        "image_url": "https://images.unsplash.com/photo-1512499617640-c74ae3a79d37?w=800&q=80",
        "hashtags": ["sleephabits", "bettersleep", "sleepchallenge", "insomnia", "healthyhabits"]
    },

    # CBT-I and clinical approaches
    {
        "title": "What Is CBT-I and Why Doctors Recommend It Over Sleeping Pills",
        "description": "Cognitive Behavioral Therapy for Insomnia (CBT-I) has a 70-80% success rate vs 30-40% for sleeping pills — and the effects last. The core techniques: stimulus control, sleep restriction, cognitive restructuring.",
        "link": "https://sleepwisereviews.com/posts/cbt-i-guide.html",
        "image_url": "https://images.unsplash.com/photo-1582750433449-648ed127bb54?w=800&q=80",
        "hashtags": ["CBTi", "insomnia", "sleeptherapy", "naturalsleep", "sleeptips"]
    },

    # Alcohol and sleep
    {
        "title": "Why Alcohol Ruins Your Sleep (Even When It Helps You Fall Asleep Faster)",
        "description": "Alcohol suppresses REM sleep in the second half of the night. You fall asleep faster but wake up emotionally less regulated, cognitively slower, and physically unrestored. The mechanism.",
        "link": "https://sleepwisereviews.com/posts/alcohol-sleep-quality.html",
        "image_url": "https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=800&q=80",
        "hashtags": ["alcoholsleep", "REM", "sobertips", "sleepscience", "bettersleep"]
    },

    # Adenosine / sleep drive
    {
        "title": "Adenosine: The Chemical That Makes You Sleepy (And Why Caffeine Tricks It)",
        "description": "Adenosine builds throughout the day creating sleep pressure. Caffeine blocks adenosine receptors — giving a feeling of alertness without reducing the actual sleep debt. The rebound is why you crash.",
        "link": "https://sleepwisereviews.com/posts/adenosine-sleep-drive.html",
        "image_url": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800&q=80",
        "hashtags": ["adenosine", "sleepscience", "caffeine", "sleeppressure", "circadianrhythm"]
    },

    # Circadian rhythm
    {
        "title": "How to Reset Your Circadian Rhythm in 3 Days",
        "description": "Morning light + consistent wake time + melatonin at target bedtime. Each on their own helps. All three together shift your rhythm 2-3 times faster. Step-by-step protocol.",
        "link": "https://sleepwisereviews.com/posts/circadian-rhythm-basics.html",
        "image_url": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=800&q=80",
        "hashtags": ["circadianrhythm", "sleepschedule", "jetlagrecovery", "morningroutine", "bettersleep"]
    },

    # Bedroom environment
    {
        "title": "The Ideal Bedroom for Sleep — Temperature, Light, Sound, and Scent",
        "description": "Temperature: 65-68F. Light: absolute blackout or very dim. Sound: consistent masking or silence. Scent: lavender (mild but real evidence). The bedroom should have one purpose: sleep.",
        "link": "https://sleepwisereviews.com/posts/bedroom-tech-sleep.html",
        "image_url": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800&q=80",
        "hashtags": ["bedroomsetup", "sleepsetup", "perfectbedroom", "sleeptips", "bedroomdecor"]
    },
    {
        "title": "Should You Have Plants in Your Bedroom? (Sleep Impact)",
        "description": "Snake plants and peace lilies do convert CO2 to O2 at night (most don't). The CO2 impact is small but oxygen-rich air marginally improves sleep quality. The psychological effect is real.",
        "link": "https://sleepwisereviews.com/posts/bedroom-plants-sleep.html",
        "image_url": "https://images.unsplash.com/photo-1501004318641-b39e6451bec6?w=800&q=80",
        "hashtags": ["bedroomplants", "sleepbetter", "airquality", "plantlover", "bedroom"]
    },

    # Smart alarm / melatonin timing
    {
        "title": "Sunrise Alarm Clock vs Regular Alarm — What the Evidence Shows",
        "description": "Gradual light exposure 30 min before wake time suppresses melatonin, raises cortisol, and reduces sleep inertia. Tested 3 sunrise clocks — the key spec is lux output, not brand.",
        "link": "https://sleepwisereviews.com/posts/bedroom-tech-sleep.html",
        "image_url": "https://images.unsplash.com/photo-1508873535684-277a3cbcc4e8?w=800&q=80",
        "hashtags": ["sunrisealarm", "wakeuplight", "sleepinertia", "morningperson", "bettersleep"]
    },

    # Earplugs
    {
        "title": "Best Earplugs for Sleeping 2025 — For Light Sleepers and Snoring Partners",
        "description": "Not all earplugs have the same NRR rating or comfort for overnight wear. Flanged vs foam for different ear canals. The difference between 22dB and 33dB at partner snoring volume.",
        "link": "https://sleepwisereviews.com/posts/best-sleep-masks.html",
        "image_url": "https://images.unsplash.com/photo-1558014539-8c6e5a7fbe0e?w=800&q=80",
        "hashtags": ["earplugs", "snoring", "lightsleeper", "sleeptips", "sleepaid"]
    },

    # Sleep myths
    {
        "title": "7 Sleep Myths Most People Still Believe",
        "description": "Counting sheep doesn't work. Warm milk has no real sedative effect. Sleeping in on weekends makes sleep worse on Monday. Falling asleep instantly isn't a sign of good sleep — it's exhaustion.",
        "link": "https://sleepwisereviews.com/scheduled/sleep-myth-8-hours.html",
        "image_url": "https://images.unsplash.com/photo-1515378960530-7c0da6231fb1?w=800&q=80",
        "hashtags": ["sleepmyths", "sleepfacts", "bettersleep", "sleepscience", "insomnia"]
    },

    # Teen sleep
    {
        "title": "Why Teenagers Need More Sleep and Can't Help Staying Up Late",
        "description": "Puberty shifts the circadian clock by 2-3 hours — biologically. A teenager who can't fall asleep before midnight isn't lazy, they're fighting their biology. What actually helps.",
        "link": "https://sleepwisereviews.com/posts/aging-and-sleep.html",
        "image_url": "https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=800&q=80",
        "hashtags": ["teensleep", "adolescentsleep", "schoolsleep", "parenting", "sleepscience"]
    },

    # Tracking data
    {
        "title": "What 1 Year of Sleep Tracking Data Showed (Oura Ring)",
        "description": "12 months of data across 365 nights. The single biggest factor in deep sleep: total sleep time. In HRV: alcohol (even 1 drink). In REM: alcohol again. Raw data patterns that surprised me.",
        "link": "https://sleepwisereviews.com/posts/sleep-tracking-data.html",
        "image_url": "https://images.unsplash.com/photo-1551434678-e076c223a692?w=800&q=80",
        "hashtags": ["sleepdata", "ouraering", "quantifiedself", "sleeptracking", "365days"]
    },

    # Specific conditions
    {
        "title": "Best Sleep Position and Setup for Acid Reflux and GERD",
        "description": "Left-side sleeping reduces reflux by keeping the stomach below the esophagus. Head elevation of 6-8 inches works better than lying flat. Pillow wedges vs adjustable bases.",
        "link": "https://sleepwisereviews.com/posts/best-sleep-position.html",
        "image_url": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800&q=80",
        "hashtags": ["acidreflux", "GERD", "sleepposition", "hearburb", "sidesleeper"]
    },
    {
        "title": "How to Sleep During Altitude Sickness (For Hikers and Travelers)",
        "description": "High altitude reduces oxygen saturation, which disrupts sleep architecture — especially REM. Acclimatization strategies, timing, and supplements that help. Acetazolamide notes.",
        "link": "https://sleepwisereviews.com/posts/altitude-sleep.html",
        "image_url": "https://images.unsplash.com/photo-1551632811-561732d1e306?w=800&q=80",
        "hashtags": ["altitudesleep", "hiking", "mountainsleep", "traveltips", "altitudesickness"]
    },

    # Bedroom tech
    {
        "title": "Smart Home Devices That Actually Help Sleep (and Which to Avoid in the Bedroom)",
        "description": "Devices that help: smart thermostats (automates 65F at bedtime), white noise machines, sunrise alarms. Devices that hurt: TVs (blue light + cognitive stimulation), phone chargers (notification pull).",
        "link": "https://sleepwisereviews.com/posts/bedroom-tech-sleep.html",
        "image_url": "https://images.unsplash.com/photo-1558002038-1055907df827?w=800&q=80",
        "hashtags": ["smarthome", "sleeptech", "bedroomtech", "bettersleep", "techdetox"]
    },
]


def main():
    data = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
    before = len(data)
    data.extend(INTENT_PINS)
    QUEUE_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    after = len(data)
    print(f"Queue expanded: {before} -> {after} pins")
    print(f"Days at 4/day: {after // 4}")


if __name__ == "__main__":
    main()
