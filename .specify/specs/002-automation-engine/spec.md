# Spec 002: Python Automation Engine

**Principle refs:** I (Static-First), IV (One Article → All Channels)
**Status:** LIVE (core modules), PARTIAL (some integrations inactive)

---

## What It Is

Python-based automation system in `automation/` that orchestrates content generation, image creation, social media queuing, and site publishing. Triggered by GitHub Actions (every 2 hours) or Telegram bot commands.

---

## Module Inventory (`automation/modules/`)

| Module | Purpose | Status |
|--------|---------|--------|
| `content_generator.py` | Generates articles and social content via Claude API (Anthropic) | ACTIVE |
| `website_manager.py` | Creates article HTML from template, updates `sitemap.xml`, commits to repo | ACTIVE |
| `n8n_integration.py` | Reads/writes `pinterest_queue.json` — the handoff point for n8n Cloud | ACTIVE |
| `telegram_reporter.py` | Sends daily reports and notifications via Telegram bot | ACTIVE |
| `telegram_bot.py` | Telegram command handler (runs on Railway) | ACTIVE |
| `affiliate_manager.py` | Manages affiliate product library, seasonal campaigns, commission rates | ACTIVE (no revenue yet) |
| `image_generator.py` | Creates branded social media images via Pillow (local image gen) | ACTIVE |
| `instagram_prep.py` | Prepares Instagram carousel posts and captions | PARTIAL — images generated, posting not automated |
| `pinterest_poster.py` | Posts pins to Pinterest API, tracks posted URLs in `pinterest_posted.json` | BLOCKED — Pinterest API consumer type restriction |
| `queue_sender.py` | Sends content queues to external platforms | ACTIVE |
| `buffer_integration.py` | Posts to social via Buffer API | AVAILABLE — not activated ($6/month) |
| `make_integration.py` | Webhook integration for Make.com | AVAILABLE — not activated |

---

## Script Inventory (`automation/scripts/`)

| Script | Purpose | Status |
|--------|---------|--------|
| `build_carousels_batch.py` | Builds multi-slide Instagram carousels (5 slides each) | ACTIVE |
| `generators/create_articles.py` | Batch generator for backdated + future articles | ONE-TIME (done) |
| `generators/create_content.py` | Pillow-based image generator for Pinterest + Instagram | ACTIVE |
| `generators/create_week_pins.py` | Generates 6 Pinterest pins/week | ACTIVE |
| `generators/create_week_instagram.py` | Generates weekly Instagram post batch (Tue–Sun) | ACTIVE |
| `generators/generate_ig_images.py` | DALL-E 3 image generator — reads Google Sheets prompts, uploads to GitHub | ACTIVE |
| `generators/create_bonus_pins.py` | Creates bonus pins based on analytics insights | ACTIVE |
| `populate_content_calendar.py` | One-time: populated 56 scheduled articles in Google Sheets | DONE |
| `sync_prompts_to_sheet.py` | Syncs `ig_image_prompts.txt` to Google Sheets | ACTIVE |
| `update_sheet_urls.py` | Pushes generated slide URLs + QA status back to Google Sheets | ACTIVE |
| `fix_content_types.py` | Batch-fixes content type classifications in Google Sheets | ONE-TIME (done) |

---

## Data Files (`automation/data/`)

| File | Purpose |
|------|---------|
| `pinterest_queue.json` | Pins pending posting — written by Python, read by n8n |
| `pinterest_posted.json` | History of posted Pinterest pins with URLs |
| `instagram_queue.json` | Instagram posts queued — populated from Google Sheets |
| `content_queue.json` | General content queue |
| `slide_content.json` | Instagram carousel slide content |
| `ig_image_prompts.txt` | DALL-E 3 prompts for Instagram images |
| `state.json` | Current automation state + last run timestamp |
| `task_history.json` | Log of completed automation tasks |
| `telegram_history.json` | History of Telegram notifications |
| `automation.log` | Full agent activity log |
| `sleepwise.db` | SQLite database |
| `google_credentials.json` | Google Sheets API credentials |
| `service_account.json` | Google service account credentials |

---

## GitHub Actions Workflows

### `automation.yml` — SleepWise Automation Agent
- **Trigger:** Schedule every 2 hours + manual dispatch
- **Manual task options:** `test`, `article`, `summary`, `content_prep`, `instagram_notify`, `engagement_tips`
- **What it does:** Runs Python automation agent, commits state changes to repo

### `publish-scheduler.yml` — Publish Scheduled Articles
- **Trigger:** Daily 08:00 UTC (10:00 Cairo)
- **What it does:** Reads Google Sheets content calendar → publishes due articles to `/posts/` → updates `sitemap.xml` → sends Telegram notification

### `sitemap-checker.yml` — Sitemap Status Checker
- **Trigger:** Weekly Monday 09:00 UTC
- **What it does:** Verifies `sitemap.xml` accessibility → sends Telegram alert ONLY on failure

---

## Environment Variables Required

```
TELEGRAM_BOT_TOKEN        — From @BotFather
TELEGRAM_CHAT_ID          — Authorized chat ID (security gate)
ANTHROPIC_API_KEY         — Claude content generation
GITHUB_TOKEN              — Repo write access (auto-provided in Actions)
MAKE_WEBHOOK_URL          — Make.com webhook (optional)
BUFFER_ACCESS_TOKEN       — Buffer social posting (optional, $6/month)
PINTEREST_ACCESS_TOKEN    — Pinterest direct API (blocked)
CLOUDINARY_URL            — Image hosting (optional)
IMGUR_CLIENT_ID           — Image hosting fallback (optional)
```

---

## Entry Point

```bash
cd automation
python auto_scheduler.py --status          # check state
python auto_scheduler.py --test-telegram   # test Telegram
python auto_scheduler.py --post-pinterest 1 # simulate pin
python auto_scheduler.py --daily-report   # send report
```

---

## Gaps

- [ ] `auto_scheduler.py` is referenced in CLAUDE.md quick commands but not listed in the module/script inventory — needs verification it exists
- [ ] `pinterest_poster.py` exists but Pinterest direct API is blocked (consumer type restriction) — module is dormant
- [ ] `buffer_integration.py` exists but not activated — $6/month Buffer subscription needed
- [ ] No retry logic on GitHub Actions failures — if the 2-hour run fails silently, no alert is sent
- [ ] `sleepwise.db` schema unknown — no documentation on what's stored there
- [ ] `google_credentials.json` and `service_account.json` in `data/` — these are secrets and should NOT be committed to the repo; stored in GitHub Actions Secrets instead
