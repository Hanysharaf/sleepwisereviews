"""
add_slide_content_046_059.py
Adds IG-046 to IG-059 entries to slide_content.json (June batch).
Run once, then delete this script.
"""
import json
from pathlib import Path

QUEUE_FILE = Path(__file__).resolve().parent.parent / "data" / "slide_content.json"

NEW_ENTRIES = {
  "IG-046": {
    "hook": "Why your blackout curtains might not actually be working",
    "points": [
      "Light leaks around edges, not through fabric | Standard blackout curtains block 99% of direct light but leave 1-2 inch gaps at every edge. At 3am with streetlights, that gap suppresses melatonin.",
      "The solution is overlap, not material | Curtains need to extend 4-6 inches beyond the window frame on each side. Ceiling-mount the rod as high as possible.",
      "Your phone screen is brighter than you think | Most streetlights produce 0.1-1 lux at window level. Your phone at minimum brightness is 2-10 lux. Phone = your biggest light leak."
    ],
    "cta": "Fix your bedroom today -> sleepwisereviews.com"
  },
  "IG-047": {
    "hook": "The 90-minute sleep cycle and why alarm timing beats duration",
    "points": [
      "Sleep works in 90-minute cycles | Each cycle moves through light, deep, and REM sleep. Waking mid-cycle causes grogginess (sleep inertia). Waking at the end feels natural.",
      "Do the math backwards from your alarm | Target 7.5 hours (5 cycles), 6 hours (4 cycles), or 9 hours (6 cycles). The grogginess is from timing, not duration.",
      "Apps that detect your sleep phase | Sleep Cycle and Oura alarms wake you during light sleep within a 30-minute window. Less inertia, same wake time."
    ],
    "cta": "Wake up right -> sleepwisereviews.com"
  },
  "IG-048": {
    "hook": "Sleep debt is real and one weekend cannot fix it",
    "points": [
      "You accumulate debt that compounds | Losing 2 hours per weeknight = 10 hours of sleep debt by Friday. Your brain is operating like it has been awake 24+ hours straight.",
      "Weekend recovery is incomplete | One Saturday lie-in helps but resets your circadian timing, making Monday worse. Sleep researchers call this social jet lag.",
      "The real fix is cumulative consistency | Going to bed 30 minutes earlier each night, held consistently, reduces debt without disrupting your rhythm."
    ],
    "cta": "Start recovering tonight -> sleepwisereviews.com"
  },
  "IG-049": {
    "hook": "What REM sleep actually does (and why alcohol ruins it)",
    "points": [
      "REM is your emotional processor | During REM, your brain replays emotional memories and strips away the charge. Insufficient REM means you wake still affected by yesterday.",
      "REM is also creative problem solving | Insights happen during REM as the brain makes non-obvious connections without the noise of conscious thought.",
      "Alcohol destroys REM | Even one drink suppresses REM in the second half of the night. You fall asleep faster but spend 3-6am in lighter, non-restorative sleep."
    ],
    "cta": "Protect your REM -> sleepwisereviews.com"
  },
  "IG-050": {
    "hook": "The real reason you cannot sleep on Sunday nights",
    "points": [
      "It is not anxiety, it is your circadian clock | Sleeping in Saturday and Sunday delays your rhythm by 1-2 hours. On Sunday night, your body thinks it is 10pm when the clock says midnight.",
      "The fix is a consistent wake time, not bedtime | You cannot control when you fall asleep. You can control when you get up. A fixed weekend wake time prevents the drift.",
      "Morning light on weekends is the reset | 10 minutes of bright outdoor light within 30 minutes of waking re-anchors your circadian clock on weekends."
    ],
    "cta": "Fix your Sunday sleep -> sleepwisereviews.com"
  },
  "IG-051": {
    "hook": "Melatonin: why you are probably taking too much",
    "points": [
      "Your body produces 0.1-0.6mg naturally | Most supplements are 5-10mg, up to 100x your body's output. At this dose it is a sedative, not a melatonin signal.",
      "Low-dose timing is what matters | 0.5mg taken 90 minutes before your target sleep time shifts your circadian phase. High dose at bedtime bypasses this mechanism.",
      "Who melatonin actually helps | Jet lag, shift work, delayed sleep phase syndrome. For insomnia from lifestyle factors, melatonin is the wrong tool."
    ],
    "cta": "Use it correctly -> sleepwisereviews.com"
  },
  "IG-052": {
    "hook": "Why you sleep worse when you travel (fix in 24 hours)",
    "points": [
      "East vs west travel matters | Flying east (losing hours) is harder. Your circadian clock adjusts at about 1 hour per day. New York to London takes 5 days to fully adjust.",
      "Light is the reset tool | Get bright outdoor light at your destination's morning time immediately on arrival. Do not wear sunglasses your first morning.",
      "Low-dose melatonin at destination bedtime | 0.5mg at 10pm local time for 2-3 nights. Combined with morning light, this cuts adjustment time in half."
    ],
    "cta": "Travel recovery guide -> sleepwisereviews.com"
  },
  "IG-053": {
    "hook": "Your brain cleans itself while you sleep (and stops when you don't)",
    "points": [
      "The glymphatic system | During deep sleep, cerebrospinal fluid flushes through brain tissue removing waste, including amyloid beta linked to Alzheimer's. Only happens at sufficient sleep depth.",
      "Side sleeping optimizes brain drainage | Research shows lateral sleeping position enhances glymphatic clearance vs back or stomach sleeping.",
      "Short sleep means less cleaning | Chronically sleeping under 7 hours reduces glymphatic activity. One proposed mechanism behind the sleep-dementia link."
    ],
    "cta": "Sleep for your brain -> sleepwisereviews.com"
  },
  "IG-054": {
    "hook": "L-theanine: the sleep supplement no one talks about",
    "points": [
      "It comes from green tea | L-theanine is the amino acid that counters caffeine's jitteriness. At higher doses before bed, it promotes a relaxed, drowsy state.",
      "It works on racing thoughts specifically | L-theanine reduces beta wave activity associated with active thinking. If you cannot stop thinking at bedtime, this is the tool.",
      "Dose: 100-200mg, 30-60 min before bed | Pairs well with magnesium glycinate. Stack them for better results than either alone. No morning grogginess."
    ],
    "cta": "Try the stack tonight -> sleepwisereviews.com"
  },
  "IG-055": {
    "hook": "How to choose a mattress without getting tricked",
    "points": [
      "Firmness scales are not standardized | A 7 firm from one brand is a 5 medium from another. Ask instead: what is the ILD of the comfort layer?",
      "Your sleep position is the real input | Side sleepers need softer comfort layers. Back sleepers need medium support. Stomach sleepers need the firmest option.",
      "The real test is 30 days | Your back adapts. A mattress that feels wrong in week 1 may be correct by week 4. Only brands with 90-day trials give you enough time to know."
    ],
    "cta": "Mattress buying guide -> sleepwisereviews.com"
  },
  "IG-056": {
    "hook": "Sleep apnea signs you can check without a sleep study",
    "points": [
      "Classic signs beyond snoring | Waking with headaches, dry mouth, needing to urinate 2+ times nightly, excessive daytime sleepiness despite 7+ hours in bed.",
      "Home screening tools exist | The STOP-BANG questionnaire is a validated clinical screening tool available free online. Score 3+ warrants formal evaluation.",
      "Untreated apnea is a cardiovascular risk | Recurrent oxygen drops stress the heart and raise blood pressure. The sleep deprivation is secondary to the cardiac risk."
    ],
    "cta": "Learn the warning signs -> sleepwisereviews.com"
  },
  "IG-057": {
    "hook": "Caffeine and sleep: the actual science most guides skip",
    "points": [
      "Half-life is 5-6 hours | A 3pm coffee is 50% strength at 8pm, 25% at midnight. Caffeine suppresses deep sleep without necessarily preventing sleep onset.",
      "You can fall asleep with caffeine still active | This is why you can sleep after coffee and still wake unrefreshed. The deep sleep is suppressed, not the onset.",
      "Caffeine blocks adenosine | Adenosine is your sleepiness signal. Caffeine does not give energy, it blocks the signal you are tired. The sleep debt still accumulates."
    ],
    "cta": "Set your cutoff correctly -> sleepwisereviews.com"
  },
  "IG-058": {
    "hook": "The best sleep position for your spine (physio-backed)",
    "points": [
      "Side sleeping wins | Lateral position keeps the spine neutral for most people, reduces snoring, and optimizes brain drainage. Left side also reduces acid reflux.",
      "Stomach sleeping is the worst | Rotating the cervical spine to one side for hours causes or worsens chronic neck problems. Fix: pillow at your side to prevent rolling.",
      "Pillow loft is the critical variable | Side sleepers need 4-6 inches of loft. Most pillows compress to 2-3 inches by morning. Look for adjustable fill."
    ],
    "cta": "Fix your sleep position -> sleepwisereviews.com"
  },
  "IG-059": {
    "hook": "The one-week habit that permanently improved my sleep",
    "points": [
      "Pick one wake time and hold it for 7 days | Your circadian rhythm is anchored by wake time more than bedtime. Consistent wake time = consistent melatonin timing = consistent sleep onset.",
      "Light within 30 minutes of waking | 10 minutes of outdoor light tells your clock the day has started. This anchors the rhythm and makes the next night's sleep onset earlier.",
      "Stop the phone for the first 30 minutes | Morning phone use spikes cortisol before the natural cortisol peak has subsided. Light first, phone second."
    ],
    "cta": "Try it this week -> sleepwisereviews.com"
  }
}

data = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
data.update(NEW_ENTRIES)
QUEUE_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"slide_content.json now has {len(data)} entries")
print(f"Last key: {sorted(data.keys())[-1]}")
