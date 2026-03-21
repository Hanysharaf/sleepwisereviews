# SleepWise Daily Action Guide

## Project Status: Live & Scheduling Active
**Last Updated:** March 13, 2026

---

## What's Live Now

### Website
- **URL:** https://hanysharaf.github.io/sleepwisereviews/
- **Articles:** 26 articles (2020-2025 history)
- **Sitemap:** 32 URLs submitted to Google Search Console
- **All links working:** Categories, archive, footer, social icons

### Social Media
- **Pinterest:** https://www.pinterest.com/sleepwisereviews
- **Instagram:** https://www.instagram.com/sleepwise.reviews (5 posts live)
- **First Win:** Verified 205K account (@wellness.healthzone) reposting content!

### Instagram Scheduling (NEW!)
- **Platform:** Meta Business Suite
- **Content Plan:** `INSTAGRAM-CONTENT-PLAN.md`
- **Full Calendar:** `content/MARCH-2026-FULL-CALENDAR.md`

| Date | Topic | Time | Status |
|------|-------|------|--------|
| Mar 13 | Sleep Schedule Consistency | 20:00 | ✅ SCHEDULED |
| Mar 14 | Weighted Blanket Benefits | 09:00 | ✅ SCHEDULED |
| Mar 15 | White Noise Benefits | 10:00 | ✅ SCHEDULED |
| Mar 16-31 | See calendar | Various | ⏳ To Schedule |

### Content Ready (Full Month)
- ✅ March 2026 full content calendar created (19 posts)
- ✅ Images in `content/2026-03-XX-[day]/instagram/` folders
- ✅ Captions in `MARCH-2026-FULL-CALENDAR.md`
- Amazon affiliate links with tag: `sleepwiserevi-20`

### Automated Monitoring
- **Sitemap Checker:** Runs weekly (Monday 9 AM), only alerts on errors
- **Google Search Console:** Status pending - check manually

---

## What To Do When You Get Each Notification

### 1. Sleep Tip of the Day (Morning ~8 AM)

**When you see:**
> Sleep Tip of the Day
> Keep your bedroom at 65-68F...

**DO THIS:**
1. Check `content/[today's-date]/` folder
2. Open Pinterest
3. Upload the pin image
4. Copy title, description from README.txt
5. Add to "Sleep Tips" board
6. Done! (2-3 minutes)

---

### 2. Instagram Content Ready (~2 PM)

**Option A: Post Now (Manual)**
1. Check `content/[today's-date]/instagram/` folder
2. Open Instagram app
3. Upload the post image
4. Copy/paste caption from README.txt
5. Add hashtags in first comment
6. Post!

**Option B: Schedule via Meta Business Suite (Recommended)**
1. Go to https://business.facebook.com/latest/content_calendar
2. Click "Create post"
3. Click "Add photo/video" and select image from content folder
4. Copy caption from `MARCH-2026-FULL-CALENDAR.md`
5. Toggle "Set date and time"
6. Set the date and time from calendar
7. Click "Schedule"

**Time:** 5 minutes

---

### 3. Engagement Reminder (~6 PM)

**When you see:**
> Engagement Reminder

**DO THIS (pick 1-2):**
- [ ] Reply to any Instagram comments (2 min)
- [ ] Check Pinterest analytics (3 min)
- [ ] Save 5 pins from other sleep accounts (3 min)
- [ ] Follow 3-5 accounts in sleep/wellness niche (2 min)

**Time:** 5-10 minutes

---

### 4. Weekly Task (Monday ~10 AM)

**When you see:**
> Weekly Task: Monday

**DO THIS:**
1. Run `python automation/create_week_pins.py` (or ask Claude)
2. Schedule all pins in Pinterest
3. Review analytics from previous week

**Time:** 20-30 minutes once per week

---

## Quick Daily Checklist

```
Morning (5 min):
[ ] Post Pinterest pin from content folder

Afternoon (5 min):
[ ] Post Instagram content

Evening (5 min):
[ ] Do 1 engagement task

Total: 15 minutes/day
```

---

## Content Folders Structure

```
content/
  2026-03-09-monday/
    pinterest/
      01-pin-monday-temperature.png
    instagram/
      01-ig-monday-temperature.png
    README.txt  <-- Copy-paste content here!

  2026-03-10-tuesday/
    ...
```

---

## Weekly Schedule

| Day | Main Task |
|-----|-----------|
| Mon | Generate week's pins + schedule |
| Tue | Instagram focus day |
| Wed | Check analytics |
| Thu | Engagement focus |
| Fri | Research trending topics |
| Sat | Schedule weekend posts |
| Sun | Review week + check affiliate earnings |

---

## Your Links

- **Website:** https://hanysharaf.github.io/sleepwisereviews/
- **Pinterest:** https://www.pinterest.com/sleepwisereviews
- **Instagram:** https://www.instagram.com/sleepwise.reviews
- **Affiliate Tag:** `sleepwiserevi-20`
- **Bio Link:** `https://www.amazon.com/s?k=sleep+products&tag=sleepwiserevi-20`

---

## Automation Scripts

| Script | Purpose |
|--------|---------|
| `automation/create_content.py` | Create single day's content |
| `automation/create_week_pins.py` | Create full week of pins |
| `automation/create_bonus_pins.py` | Create bonus pins (analytics-based) |
| `automation/create_articles.py` | Generate website articles |

---

## Analytics Insights (Based on Pinterest Data)

**Top Performers:**
1. Weighted Blankets (52% of impressions)
2. "Best X for Sleep" format works well
3. Product-focused pins get more outbound clicks

**Strategy:**
- Create more weighted blanket content
- Use "Best [Product] for Sleep" titles
- Include clear Amazon CTA

---

## Need Help?

Open Claude Code and say:
- "Create Pinterest pins for this week"
- "Create Instagram content for [topic]"
- "Check Pinterest analytics"
- "Update the website"

---

## How to Resume with Claude Code

When starting a new session, say:

```
Read the SleepWise project at:
C:\Users\Hany\OneDrive - Petroleum Air Services\Projects\SleepReviewes

Check ACTION-GUIDE.md and ROADMAP.md for current status.
Then tell me what needs to be done today.
```

Or simply:
```
Continue SleepWise project - check what's pending
```

Claude will:
1. Read the project files
2. Check content folders for posting status
3. Tell you what to do today
