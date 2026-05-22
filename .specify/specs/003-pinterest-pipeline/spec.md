# Spec 003: Pinterest Automation Pipeline

**Principle refs:** I (Static-First), IV (One Article → All Channels)
**Status:** LIVE via n8n Cloud (3 pins/day)

---

## What It Is

Automated Pinterest posting pipeline. Python generates pin content and images, writes to a JSON queue file, n8n Cloud reads the queue and posts to Pinterest. 3 pins posted per day.

---

## Architecture

```
Python (create_week_pins.py)
  → generates 6 pins/week with images + captions
  → writes to automation/data/pinterest_queue.json

n8n Cloud workflow
  → reads pinterest_queue.json via HTTP (raw GitHub)
  → posts each pin to Pinterest API
  → removes posted items from queue

automation/modules/n8n_integration.py
  → manages queue read/write from Python side

automation/modules/pinterest_poster.py
  → tracks posted pins in pinterest_posted.json
  → (direct API posting — currently blocked)
```

---

## Content Generation

- Script: `automation/scripts/generators/create_week_pins.py`
- Generates 6 pins/week (about 3 days of content)
- Bonus pins from analytics insights: `create_bonus_pins.py`
- Image generation: `automation/modules/image_generator.py` (Pillow) + `automation/scripts/generators/create_content.py`
- Top performing niche: **Weighted Blankets = 52% of Pinterest impressions**
- Best format: "Best X for Sleep" — product-focused pins

---

## Pinterest API Status

- Direct API posting (`pinterest_poster.py`): **BLOCKED**
  - Reason: Pinterest API requires "consumer type" approval — application denied/pending
  - Workaround: n8n Cloud handles API calls instead
- n8n Cloud: **ACTIVE** (free tier, 3 pins/day)

---

## Data Flow

1. Python writes pins to `pinterest_queue.json` (array of `{title, description, image_url, link}`)
2. n8n reads the file via raw GitHub URL on a schedule
3. n8n posts to Pinterest Board ID: `1104437646027276054`
4. `pinterest_posted.json` tracks post history (URL, date, status)

---

## Analytics

- Pinterest profile: https://www.pinterest.com/sleepwisereviews
- Board ID: `1104437646027276054`
- Insights documented in `docs/pinterest-insights.md`
- Weighted Blankets: highest impression share
- "Best X for Sleep" product pins: highest click rate

---

## Gaps

- [ ] n8n free tier limit — if posting frequency increases past free tier, need paid plan or switch to Buffer ($6/month via `buffer_integration.py`)
- [ ] No automated analytics pull — Pinterest impressions/clicks are checked manually (in `dream/weekly-check.md`)
- [ ] Image hosting: pins reference image URLs — need to confirm all image URLs are stable (GitHub raw URLs can break)
- [ ] `create_bonus_pins.py` relies on manual analytics input — not yet connected to Pinterest API analytics
- [ ] No A/B testing on pin formats — all pins use same template
