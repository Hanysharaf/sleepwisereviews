# SleepWiseReviews Project

## Overview
A sleep product review website built as a static HTML site hosted on GitHub Pages, with social media automation.

## URLs
- **Live Site**: https://hanysharaf.github.io/sleepwisereviews/
- **GitHub Repo**: https://github.com/Hanysharaf/sleepwisereviews
- **Pinterest**: https://www.pinterest.com/sleepwisereviews (Board ID: 1104437646027276054)
- **Instagram**: https://www.instagram.com/sleepwise.reviews

## Analytics (added 2026-04-01)
- **Google Analytics 4**: G-ZKGY2B72WH — injected into all 160 HTML pages
- **Google Search Console**: Verified via GA tag, sitemap.xml submitted (30 pages discovered)
- **Amazon Associates**: March 2026 — 38 clicks, $0.00 earnings, 0 conversions
- **Email**: Brevo form exists — check subscriber count at app.brevo.com
- **dream/ folder**: Evaluation workspace with audit, revenue-log, content-gaps, weekly-check

## Automation Status

### Working:
- n8n Cloud: 3 Pinterest pins/day (free, live)
- Telegram notifications (daily tips, content reminders, reports)
- GitHub Actions runs every 2 hours

### Not Automated:
- Instagram — decision pending (in or out)
- Pinterest direct API still blocked ("consumer type not supported")

## Folder Structure
```
SleepReviewes/
├── automation/           # Main automation system
│   ├── modules/          # Core modules
│   ├── data/             # Queues, state, logs
│   ├── scripts/          # Content generators
│   └── templates/        # Content templates
├── content/archive/      # Past social media content
├── docs/                 # All documentation
├── images/               # Product photos, logos, templates
├── pages/                # Static website pages
├── posts/                # Blog articles (150 articles — see posts/INDEX.md)
├── telegram_bot/         # Railway-hosted bot
└── index.html            # Homepage
```

## Quick Commands
```bash
cd automation

# Check status
python auto_scheduler.py --status

# Test Telegram
python auto_scheduler.py --test-telegram

# Post pin (simulation mode)
python auto_scheduler.py --post-pinterest 1

# Daily report
python auto_scheduler.py --daily-report
```

## Environment Variables (.env)
- TELEGRAM_BOT_TOKEN - From @BotFather
- TELEGRAM_CHAT_ID - Your chat ID
- ANTHROPIC_API_KEY - For content generation
- PINTEREST_ACCESS_TOKEN - (Not working due to API restrictions)

## To Enable Full Pinterest Automation
Choose one:
1. **Buffer** ($6/month) - Add BUFFER_ACCESS_TOKEN to .env
2. **Tailwind** ($15/month) - Best for Pinterest-specific features

## Content Strategy
- Weighted Blankets = 52% of Pinterest impressions (focus here)
- "Best X for Sleep" format performs well
- Product-focused pins get more clicks
- Amazon affiliate tag: sleepwiserevi-20
