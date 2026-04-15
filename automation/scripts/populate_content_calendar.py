"""
populate_content_calendar.py
One-time script: fills the Content Calendar sheet tab with all 56 scheduled articles.
"""
import gspread
from pathlib import Path

SPREADSHEET_ID = "1KeWK1xO5eiD2YbFe63Fx8sV9Vf6jUwi57h71fc8zb5o"
SERVICE_ACCT = Path(__file__).parent.parent / "data" / "service_account.json"

gc = gspread.service_account(filename=str(SERVICE_ACCT))
ws = gc.open_by_key(SPREADSHEET_ID).worksheet("Content Calendar")

articles = [
    ["20-04-2026", "sex-and-sleep-intimacy-quality.html", "Sex and Sleep: How Intimacy Affects Your Sleep Quality", "Sex & Sleep", "PENDING", ""],
    ["27-04-2026", "sleep-myth-8-hours.html", "Sleep Myth: You Need Exactly 8 Hours Every Night", "Sleep Myths", "PENDING", ""],
    ["04-05-2026", "wrong-sleeping-in-weekends.html", "Wrong: Sleeping In on Weekends. Right: Sleep Consistency Tools That Actually Work", "Wrong vs Right", "PENDING", ""],
    ["11-05-2026", "best-mattresses-couples-2026.html", "Best Mattresses for Couples in 2026: Motion Isolation, Noise, and Firmness", "Sex & Mattress", "PENDING", ""],
    ["18-05-2026", "does-sex-before-bed-help-sleep.html", "Does Sex Before Bed Actually Help You Sleep? The Science", "Sex & Sleep", "PENDING", ""],
    ["25-05-2026", "sleep-myth-older-people-less-sleep.html", "Sleep Myth: Older People Need Less Sleep", "Sleep Myths", "PENDING", ""],
    ["01-06-2026", "wrong-using-melatonin-sleeping-pill.html", "Wrong: Using Melatonin Like a Sleeping Pill. Right: How Melatonin Actually Works", "Wrong vs Right", "PENDING", ""],
    ["08-06-2026", "poor-sleep-tanks-libido.html", "How Poor Sleep Tanks Your Libido: The Hormone Explanation", "Sex & Sleep", "PENDING", ""],
    ["15-06-2026", "motion-isolation-mattress-couples.html", "Motion Isolation in Mattresses: Why Couples Need It More Than Singles", "Sex & Mattress", "PENDING", ""],
    ["22-06-2026", "sleep-cool-together-summer-couples.html", "How to Sleep Cool Together: The Couples Guide to Summer Heat and Your Mattress", "Seasonal", "PENDING", ""],
    ["29-06-2026", "wrong-counting-sheep.html", "Wrong: Counting Sheep. Right: The Cognitive Shuffle and 4-7-8 Method", "Wrong vs Right", "PENDING", ""],
    ["06-07-2026", "sleep-testosterone-men.html", "Sleep Testosterone Connection: Why Sleep-Deprived Men Have Lower T", "Sex & Sleep", "PENDING", ""],
    ["13-07-2026", "mattress-firmness-couples.html", "Mattress Firmness for Couples: Sleep AND Intimacy Need Different Things", "Sex & Mattress", "PENDING", ""],
    ["20-07-2026", "sleep-myth-train-body-less-sleep.html", "Sleep Myth: You Can Train Your Body to Need Less Sleep", "Sleep Myths", "PENDING", ""],
    ["27-07-2026", "wrong-tv-on-sleeping.html", "Wrong: Sleeping with the TV On. Right: White Noise and Sleep Headphones", "Wrong vs Right", "PENDING", ""],
    ["03-08-2026", "orgasms-and-sleep-science.html", "Orgasms and Sleep: What Your Body Does in the Hour After Sex", "Sex & Sleep", "PENDING", ""],
    ["10-08-2026", "best-mattress-toppers-couples.html", "Best Mattress Toppers for Couples: 5 Options for Every Budget", "Sex & Mattress", "PENDING", ""],
    ["17-08-2026", "sleep-myth-sleeping-pills-insomnia.html", "Sleep Myth: Sleeping Pills Are the Best Fix for Insomnia", "Sleep Myths", "PENDING", ""],
    ["24-08-2026", "wrong-bedroom-temperature.html", "Wrong: Your Bedroom Temperature Setup. Right: The Evidence-Based Cool Sleep System", "Wrong vs Right", "PENDING", ""],
    ["31-08-2026", "couples-sleep-together-worse.html", "Why Couples Who Sleep Together Sometimes Sleep Worse (And the Fix)", "Sex & Sleep", "PENDING", ""],
    ["07-09-2026", "edge-support-mattress-couples.html", "Edge Support in Mattresses: The Feature Couples Overlook", "Sex & Mattress", "PENDING", ""],
    ["14-09-2026", "sleep-myth-reading-before-bed.html", "Sleep Myth: Reading Before Bed Always Helps You Sleep", "Sleep Myths", "PENDING", ""],
    ["21-09-2026", "wrong-alarm-clock-misuse.html", "Wrong: Alarm Clock Misuse. Right: The Smart Wake Strategy That Leaves You Rested", "Wrong vs Right", "PENDING", ""],
    ["28-09-2026", "relationship-partner-sleep-deprived.html", "What Happens to Your Relationship When One Partner Is Chronically Sleep-Deprived", "Sex & Sleep", "PENDING", ""],
    ["05-10-2026", "sleep-myth-snoring-not-dangerous.html", "Sleep Myth: Snoring Is Just Annoying - Not Dangerous", "Sleep Myths", "PENDING", ""],
    ["12-10-2026", "wrong-warm-milk-before-bed.html", "Wrong: Warm Milk Before Bed. Right: The Sleep Foods and Supplements That Actually Work", "Wrong vs Right", "PENDING", ""],
    ["19-10-2026", "best-split-king-mattresses-couples.html", "Best Split King and Dual Comfort Mattresses for Couples With Different Sleep Needs", "Sex & Mattress", "PENDING", ""],
    ["26-10-2026", "dst-fall-back-sleep-architecture.html", "How the End of Daylight Saving Time Disrupts Your Sleep Architecture", "Seasonal", "PENDING", ""],
    ["02-11-2026", "wrong-pre-sleep-routine.html", "Wrong: Your Pre-Sleep Routine Done Wrong. Right: The Evidence-Based 60-Minute Wind-Down", "Wrong vs Right", "PENDING", ""],
    ["09-11-2026", "sleep-myth-warm-milk.html", "Sleep Myth: Warm Milk Before Bed Is an Old Wives Tale (Or Is It?)", "Sleep Myths", "PENDING", ""],
    ["16-11-2026", "sleep-sex-feedback-loop.html", "The Sleep-Sex Feedback Loop: How Better Sleep Leads to Better Intimacy", "Sex & Sleep", "PENDING", ""],
    ["16-11-2026", "wrong-insomnia-cbt-stimulus-control.html", "Wrong: How You Handle Insomnia at Night. Right: CBT-I Stimulus Control Explained", "Wrong vs Right", "PENDING", ""],
    ["23-11-2026", "black-friday-sleep-deals-2026.html", "Black Friday Sleep Deals 2026: The Best Mattresses, Pillows, and Sleep Gear on Sale", "Seasonal", "PENDING", ""],
    ["23-11-2026", "sleep-myth-stay-in-bed.html", "Sleep Myth: You Should Stay in Bed If You Cannot Sleep", "Sleep Myths", "PENDING", ""],
    ["30-11-2026", "wrong-new-year-sleep-resolutions.html", "Wrong: New Year Sleep Resolutions Done Wrong. Right: The One Change That Actually Moves the Needle", "Wrong vs Right", "PENDING", ""],
    ["07-12-2026", "holiday-gift-guide-sleep-2026.html", "The Ultimate Holiday Gift Guide for Better Sleep 2026", "Seasonal", "PENDING", ""],
    ["07-12-2026", "gifts-that-improve-sleep.html", "Gifts That Actually Improve Sleep: What to Buy (and What to Skip)", "Seasonal", "PENDING", ""],
    ["14-12-2026", "cold-winter-sleep-stages.html", "How Cold Winter Nights Affect Your Sleep Stage Distribution", "Education", "PENDING", ""],
    ["21-12-2026", "sleeping-through-holidays.html", "Sleeping Through the Holidays: How to Protect Your Sleep When Your Schedule Breaks Down", "Practical", "PENDING", ""],
    ["28-12-2026", "bedroom-noise-sleep-sounds.html", "Bedroom Noise vs Sleep: Which Sounds Help, Which Hurt, and Why", "Education", "PENDING", ""],
    ["04-01-2027", "new-year-sleep-metrics-2027.html", "New Year, Better Sleep: The 5 Sleep Metrics Worth Tracking in 2027", "Practical", "PENDING", ""],
    ["11-01-2027", "sleep-deprivation-decision-making.html", "How Sleep Deprivation Changes Your Decision-Making (The Research Is Uncomfortable)", "Education", "PENDING", ""],
    ["18-01-2027", "brown-noise-pink-white-noise-sleep.html", "The Science of Brown Noise vs Pink Noise vs White Noise for Sleep", "Education", "PENDING", ""],
    ["25-01-2027", "indoor-light-sleep-hormones.html", "How Indoor Light After Dark Hijacks Your Sleep Hormones (And the Fix)", "Education", "PENDING", ""],
    ["01-02-2027", "old-mattress-health-effects.html", "Can Your Mattress Make You Sick? How an Old or Wrong Mattress Affects Your Health", "Education", "PENDING", ""],
    ["08-02-2027", "sleep-sex-feedback-loop-valentines.html", "The Sleep-Sex Feedback Loop - Valentines Edition: How Sleep Transforms Your Relationship", "Sex & Sleep", "PENDING", ""],
    ["15-02-2027", "best-mattresses-couples-2027-valentines.html", "Best Mattresses for Couples 2027: Valentines Buyers Guide", "Sex & Mattress", "PENDING", ""],
    ["22-02-2027", "sleep-position-relationship-couples.html", "What Your Sleep Position Reveals About Your Relationship (And What Couples Can Do About It)", "Couples", "PENDING", ""],
    ["01-03-2027", "bedroom-electronics-audit-sleep.html", "The Bedroom Electronics Audit: A Room-by-Room Light and EMF Guide for Better Sleep", "Practical", "PENDING", ""],
    ["08-03-2027", "dst-spring-forward-sleep-recovery.html", "How Daylight Saving Time Spring Forward Disrupts Your Sleep and the 5-Day Recovery Plan", "Seasonal", "PENDING", ""],
    ["15-03-2027", "sleep-apnea-unusual-risk-factors.html", "Sleep Apnea Risk Factors You Have Not Considered (Beyond Weight and Snoring)", "Education", "PENDING", ""],
    ["22-03-2027", "science-of-winding-down-sleep.html", "The Science of Winding Down: Why Your Brain Needs a Buffer Zone Before Sleep", "Education", "PENDING", ""],
    ["29-03-2027", "couples-sleep-audit.html", "How a Couples Sleep Audit Can Save Your Relationship (And Your Rest)", "Couples", "PENDING", ""],
    ["05-04-2027", "cheap-vs-expensive-sleep-products.html", "The Hidden Cost of Cheap Sleep Products: What the Research Says About Quality vs Price", "Education", "PENDING", ""],
    ["12-04-2027", "one-year-sleep-tracking-results.html", "One Year of Tracking My Sleep: What Actually Changed (Site Anniversary Roundup)", "Anniversary", "PENDING", ""],
    ["19-04-2027", "sleepwisereviews-ultimate-buying-guide-2027.html", "The SleepWiseReviews Ultimate Buying Guide: Every Product Category Ranked for 2027", "Anniversary", "PENDING", ""],
]

ws.append_rows(articles, value_input_option="RAW")
print(f"Done. Added {len(articles)} articles to Content Calendar tab.")
