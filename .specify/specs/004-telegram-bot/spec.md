# Spec 004: Telegram Bot & Notifications

**Principle refs:** I (Static-First)
**Status:** LIVE (Railway deployment)

---

## What It Is

Two-component Telegram system: (1) a command bot that lets Hany trigger automation from his phone, and (2) a reporter that sends automated daily reports and alerts.

---

## Architecture

```
Hany's phone (Telegram)
  → sends command to @[bot_name]
  → Telegram Bot (Railway) receives it
  → Verifies TELEGRAM_CHAT_ID (security gate — only authorized chat ID allowed)
  → Calls GitHub Actions API to trigger workflow
  → GitHub Actions runs automation task
  → Reports result back via Telegram
```

---

## Components

### Command Bot (`telegram_bot/bot.py`)
- Platform: Railway.app
- Framework: async/await (python-telegram-bot)
- Security: Only responds to `TELEGRAM_CHAT_ID` — all other senders ignored

**Commands:**
| Command | Action |
|---------|--------|
| `/start` | Welcome message |
| `/help` | List available commands |
| `/article` | Trigger article generation via GitHub Actions |
| `/summary` | Trigger daily summary report |
| `/status` | Check automation status |
| `/instagram` | Trigger Instagram content prep |
| `/test` | Test the bot is alive |

### Reporter (`automation/modules/telegram_reporter.py`)
- Called by automation engine (not Railway-hosted)
- Sends: daily reports, error alerts, sitemap check results (failures only)
- History tracked in `automation/data/telegram_history.json`

---

## Deployment Files

| File | Purpose |
|------|---------|
| `telegram_bot/bot.py` | Main async bot handler |
| `telegram_bot/requirements.txt` | Bot deps: telegram, aiohttp, anthropic |
| `telegram_bot/Procfile` | Process definition for Railway/Heroku |
| `telegram_bot/railway.toml` | Railway.app config |
| `telegram_bot/.env.example` | Env vars template for bot |
| `telegram_bot/README.md` | Setup guide |

---

## Environment Variables

```
TELEGRAM_BOT_TOKEN    — From @BotFather
TELEGRAM_CHAT_ID      — Authorized chat ID
ANTHROPIC_API_KEY     — LLM for text improvement (optional)
GITHUB_TOKEN          — Triggers GitHub Actions workflows
GITHUB_REPO           — e.g. Hanysharaf/sleepwisereviews
```

---

## Notification Events

| Event | Notification Sent |
|-------|------------------|
| Article published | Yes — title + URL |
| Daily automation report | Yes — summary stats |
| Sitemap check PASS | No (silent) |
| Sitemap check FAIL | Yes — error details |
| GitHub Actions manual trigger | Yes — task started + result |

---

## Gaps

- [ ] Railway free tier may have cold start delays (30s+) — commands feel unresponsive
- [ ] No `/pin` command to trigger Pinterest content generation from phone
- [ ] No `/revenue` command to pull Amazon Associates stats
- [ ] LLM integration (`anthropic` in requirements) is optional — unclear if it's used in production or just available
- [ ] No error recovery — if Railway bot crashes, no auto-restart notification to Hany
- [ ] `telegram_reporter.py` sends Telegram messages but no two-way loop — Hany can't reply with corrections or approvals
