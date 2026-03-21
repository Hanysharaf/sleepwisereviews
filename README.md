# SleepWise Reviews

Sleep health affiliate website with automated social media posting.

**Live Site:** https://hanysharaf.github.io/sleepwisereviews/

## Project Structure

```
SleepReviewes/
├── automation/           # Main automation system
│   ├── modules/          # Core modules (telegram, pinterest, etc.)
│   ├── data/             # Queue files, state, logs
│   ├── templates/        # Content templates
│   └── scripts/          # Content generators (one-time use)
├── content/              # Social media content
│   └── archive/          # Past content by month
├── docs/                 # All documentation
├── images/               # All images
│   ├── product-photos/   # Product photography
│   ├── logos/            # Brand logos
│   └── pinterest-templates/  # Pin templates
├── pages/                # Website static pages
├── posts/                # Blog articles (HTML)
├── telegram_bot/         # Telegram bot (runs on Railway)
├── index.html            # Homepage
└── sitemap.xml           # SEO sitemap
```

## Quick Start

### n8n Cloud Automation (PRIMARY SYSTEM)
All automation runs on **n8n Cloud** - no manual intervention needed!

**Current Status:** ✅ Live & Auto-Posting
**Platform:** app.n8n.cloud
**Cost:** $0/month

**Setup Guides:**
- `docs/N8N-IMPLEMENTATION-GUIDE.md` - Complete setup instructions
- `docs/N8N-QUICK-REFERENCE.md` - Quick reference card

### Python Scripts (Manual Backup)
```bash
cd automation
python auto_scheduler.py --status           # Check status
python auto_scheduler.py --post-pinterest 1  # Manual post
python auto_scheduler.py --daily-report      # Generate report
```

## Automation Schedule (n8n Cloud)

| Time (UTC) | Workflow | Action |
|------------|----------|--------|
| 08:00 | Pinterest Auto-Poster | Post pin #1 |
| 09:00 | Queue Monitor | Check queue (Mon only) |
| 12:00 | Instagram Reminder | Send IG tip |
| 14:00 | Pinterest Auto-Poster | Post pin #2 |
| 18:00 | Pinterest Auto-Poster | Post pin #3 |
| 20:00 | Daily Analytics | Send stats report |

**Total:** 3 Pinterest pins/day, all automatic! 🎉

## Key Files

**n8n Automation (PRIMARY):**
- `docs/N8N-IMPLEMENTATION-GUIDE.md` - Complete n8n setup guide
- `docs/N8N-QUICK-REFERENCE.md` - Quick reference card
- `automation/data/pinterest_queue.json` - Content queue (n8n reads/writes)
- `automation/data/pinterest_posted.json` - Posted history with URLs

**Python Scripts (BACKUP/MANUAL):**
- `automation/auto_scheduler.py` - Manual operations
- `automation/modules/pinterest_poster.py` - Pinterest API wrapper

## Documentation

**n8n Automation:**
- `docs/N8N-IMPLEMENTATION-GUIDE.md` - Step-by-step setup (START HERE!)
- `docs/N8N-QUICK-REFERENCE.md` - Quick reference card
- `docs/N8N-INTEGRATION-PLAN.md` - Architecture overview

**General:**
- `docs/ROADMAP.md` - Project roadmap & milestones
- `docs/SOCIAL-MEDIA-CONTENT-PACK.md` - Content strategy
- `docs/ACTION-GUIDE.md` - Daily action guide

## Environment Variables

Copy `.env.example` to `.env` and fill in:
- `TELEGRAM_BOT_TOKEN` - From @BotFather
- `TELEGRAM_CHAT_ID` - Your chat ID
- `ANTHROPIC_API_KEY` - For content generation (optional)
