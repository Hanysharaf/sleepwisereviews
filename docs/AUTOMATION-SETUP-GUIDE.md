# SleepWise Automation - Complete Setup Guide

> **Goal:** Fully automated social media posting with Telegram notifications
> **Budget:** $0-$15/month (mostly free options available)
> **Time to Setup:** 30-60 minutes

---

## Quick Start (5 Minutes)

### Step 1: Create Telegram Bot (FREE)
1. Open Telegram, search for **@BotFather**
2. Send `/newbot`
3. Name it: `SleepWise Bot`
4. Username: `sleepwise_yourname_bot`
5. **Copy the token** (looks like: `123456789:ABCdef...`)

### Step 2: Get Your Chat ID
1. Search for **@userinfobot** on Telegram
2. Send `/start`
3. **Copy your ID number**

### Step 3: Create .env File
```bash
cd O:\MyFiles\Projects\SleepReviewes
copy .env.example .env
```

Edit `.env` and add:
```
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_id_here
```

### Step 4: Test It!
```bash
cd O:\MyFiles\Projects\SleepReviewes\automation
python -c "from modules.telegram_bot import TelegramBot; TelegramBot().test_connection()"
```

You should receive a message in Telegram!

---

## Full Automation Options

### Option A: Make.com (FREE - Recommended)
**Best for:** 100% free automation, 1000 posts/month

1. **Sign up:** https://make.com (free account)

2. **Create Instagram Scenario:**
   - New Scenario > Webhook (trigger)
   - Add Instagram > Create a Post
   - Copy webhook URL

3. **Create Pinterest Scenario:**
   - New Scenario > Webhook (trigger)
   - Add Pinterest > Create a Pin
   - Copy webhook URL

4. **Add to .env:**
   ```
   MAKE_WEBHOOK_URL=https://hook.make.com/your-url-here
   ```

5. **How it works:**
   - Scheduler generates content
   - Sends to Make.com webhook
   - Make.com posts to Instagram/Pinterest
   - You get Telegram notification

---

### Option B: Buffer ($6/month - Easiest)
**Best for:** Simple setup, reliable posting

1. **Sign up:** https://buffer.com
2. Connect Instagram & Pinterest
3. Get access token: Settings > Apps & Extras
4. Add to `.env`:
   ```
   BUFFER_ACCESS_TOKEN=your_token_here
   ```

---

### Option C: GitHub Actions (FREE - Set & Forget)
**Best for:** Runs automatically without your computer

1. **Create workflow file:**

```yaml
# .github/workflows/automation.yml
name: SleepWise Automation

on:
  schedule:
    # Runs every hour
    - cron: '0 * * * *'
  workflow_dispatch:

jobs:
  run-scheduler:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run scheduler
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          BUFFER_ACCESS_TOKEN: ${{ secrets.BUFFER_ACCESS_TOKEN }}
        run: |
          cd automation
          python auto_scheduler.py
```

2. **Add secrets to GitHub:**
   - Go to repo > Settings > Secrets > Actions
   - Add each environment variable

---

## Complete Installation

### Prerequisites
```bash
# Install Python dependencies
cd O:\MyFiles\Projects\SleepReviewes
pip install -r requirements.txt

# Additional for image generation
pip install Pillow
```

### Verify Installation
```bash
cd automation
python auto_scheduler.py --status
```

Expected output:
```
=== SleepWise Scheduler Status ===
Last run: Never
Posts today: 0
Total posts: 0
Pending Instagram: 0
Content queue: 0 items

Integrations:
  Telegram: Configured
  Claude API: Configured
  Buffer: Not configured
```

---

## Daily Operations

### Generate Content
```bash
# Generate Instagram post about weighted blankets
python auto_scheduler.py --generate-post "weighted blankets"

# Run all daily tasks
python auto_scheduler.py --run-now
```

### Run Continuously (on your PC)
```bash
python auto_scheduler.py --continuous --interval 60
```

### What Gets Automated

| Time | Task | Description |
|------|------|-------------|
| 06:00 | Daily Tip | Sleep tip sent to Telegram |
| 12:00 | Instagram Notify | Post content ready notification |
| 16:00 | Engagement Tips | Engagement reminder |
| 20:00 | Daily Summary | Stats report to Telegram |

---

## Scaling: Add New Products

### Via Code
```python
from modules.affiliate_manager import AffiliateManager

manager = AffiliateManager()

# Add new product
manager.add_product("new-product-id", {
    "name": "Amazing Sleep Product",
    "category": "weighted_blankets",
    "asin": "B0XXXXXXXXX",
    "price_range": "$50-$100",
    "keywords": ["sleep", "comfort"],
    "best_for": ["hot sleepers"],
    "season": ["summer"]
})
```

### Via JSON File
Edit `automation/data/affiliate_products.json`:
```json
{
  "new-product": {
    "name": "New Product Name",
    "category": "supplements",
    "asin": "B0XXXXXXXXX",
    "price_range": "$20-$30",
    "active": true
  }
}
```

---

## Seasonal Automation

The system automatically adjusts content based on season:

| Season | Featured Products | Hooks |
|--------|------------------|-------|
| Spring | Cooling, supplements | "Spring allergies ruining sleep?" |
| Summer | Cooling products, masks | "Too hot to sleep?" |
| Fall | Weighted blankets, heated | "Get cozy this fall" |
| Winter | Heated, weighted | "Sleep through holiday stress" |

### Special Campaigns (Auto-triggered)
- **Black Friday** (Nov 20-30): All products, deal hooks
- **Prime Day** (July, October): Amazon exclusives

---

## Image Generation

Generate branded images automatically:
```bash
cd automation
python -c "
from modules.image_generator import ImageGenerator
gen = ImageGenerator()
gen.generate_weekly_images()
"
```

Images saved to: `automation/data/images/`

---

## Telegram Commands

You'll receive these automatically:

### Daily Tip (6 AM)
```
🌙 Daily Sleep Tip

Keep your bedroom between 65-68°F for optimal sleep.

Share this with someone who needs better sleep!
```

### Instagram Ready (12 PM)
```
📸 Instagram Post Ready!

Copy this caption:
[Full caption with hashtags]

Best time to post: 12:00 PM
Update link in bio to: sleepwisereviews.com/article

Instructions:
1. Open Meta Business Suite
2. Create new post
3. Paste caption above
...
```

### Daily Report (8 PM)
```
🌙 SleepWise Bot Report
━━━━━━━━━━━━━━━━━━━━━━━
Daily Report - March 17, 2026

Today's Activity:
Posts created: 3
Posts published: 2
Pending posts: 5

Keep up the great work! 🚀
```

---

## Troubleshooting

### "Telegram credentials not configured"
- Check `.env` file exists
- Verify TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are set
- Run: `python -c "import os; print(os.getenv('TELEGRAM_BOT_TOKEN'))"`

### "Claude API not configured"
- Get API key from https://console.anthropic.com
- Add to `.env`: `ANTHROPIC_API_KEY=your_key`

### "Buffer not configured"
- This is optional - system falls back to Telegram notifications
- For auto-posting, sign up at buffer.com

### Images not generating
- Install Pillow: `pip install Pillow`
- Check fonts exist or system fonts available

---

## Cost Breakdown

| Service | Cost | What You Get |
|---------|------|--------------|
| Telegram Bot | FREE | Unlimited notifications |
| Make.com | FREE | 1,000 ops/month (enough for daily posting) |
| Cloudinary | FREE | 25GB image hosting |
| GitHub Actions | FREE | 2,000 min/month automation |
| **Total** | **$0/month** | Full automation |

### Optional Upgrades
| Service | Cost | Benefit |
|---------|------|---------|
| Buffer | $6/month | Easier setup, more reliable |
| Make.com Pro | $9/month | Unlimited operations |
| Claude API | ~$5/month | More content generation |

---

## Next Steps

1. **Today:** Set up Telegram bot + test connection
2. **Tomorrow:** Create Make.com account + connect Instagram
3. **This Week:** Generate first week of content
4. **Ongoing:** Check Telegram daily, system handles the rest

---

## Support Files Created

```
automation/
├── auto_scheduler.py          # Main orchestrator
├── config.py                  # Configuration
├── modules/
│   ├── telegram_bot.py        # Telegram notifications
│   ├── buffer_integration.py  # Auto-posting via Buffer
│   ├── content_generator.py   # Claude AI content
│   ├── instagram_prep.py      # Instagram content prep
│   ├── image_generator.py     # Branded image creation
│   └── affiliate_manager.py   # Product/link management
├── data/
│   ├── affiliate_products.json
│   ├── instagram_queue.json
│   └── images/
└── templates/
    └── content_calendar.json
```

---

*Last Updated: March 17, 2026*
*SleepWise Automation v2.0*
