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

### Run Automation Status
```bash
cd automation
python auto_scheduler.py --status
```

### Post to Pinterest
```bash
python auto_scheduler.py --post-pinterest 2
```

### Send Daily Report
```bash
python auto_scheduler.py --daily-report
```

### Run Full Automation
```bash
python auto_scheduler.py --run-now
```

## Automation Schedule

| Time (UTC) | Task |
|------------|------|
| 06:00 | Daily sleep tip |
| 08:00 | Post 2 Pinterest pins |
| 12:00 | Instagram content |
| 14:00 | Post 2 Pinterest pins |
| 18:00 | Post 1 Pinterest pin |
| 20:00 | Daily report with links |

## Key Files

- `automation/auto_scheduler.py` - Main scheduler (use this)
- `automation/modules/pinterest_poster.py` - Pinterest posting with queue
- `automation/modules/telegram_bot.py` - Telegram notifications
- `automation/data/pinterest_queue.json` - Content queue

## Documentation

See `docs/` folder:
- `AUTOMATION-SETUP-GUIDE.md` - Full setup instructions
- `SOCIAL-MEDIA-CONTENT-PACK.md` - Content strategy
- `launch-guide.md` - Launch checklist

## Environment Variables

Copy `.env.example` to `.env` and fill in:
- `TELEGRAM_BOT_TOKEN` - From @BotFather
- `TELEGRAM_CHAT_ID` - Your chat ID
- `ANTHROPIC_API_KEY` - For content generation (optional)
