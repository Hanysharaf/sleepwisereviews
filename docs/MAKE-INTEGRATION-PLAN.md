# SleepWise Reviews - Make.com Integration Plan

**Decision:** Using Make.com for automation (replacing n8n)
**Status:** Phase 1 — Instagram Auto-Poster
**Updated:** April 2026

---

## Why Make.com?

- **Stable** — 13 years old (formerly Integromat), backed by Celonis
- **Google-ecosystem friendly** — native Google Drive, Sheets, Gmail modules
- **Low cost** — $9/month Core (10,000 ops/month), free tier to start
- **No server** — runs in Make.com's cloud, works when computer is off
- **Expandable** — serves all future passive income branches (dropshipping, digital products)

---

## Phase 1 — Instagram Auto-Poster (Active)

### Scenario: Daily Instagram Post

**Trigger:** Schedule (daily, time TBD by Hany)

**Flow:**
1. GitHub → read `automation/data/instagram_queue.json`
2. Extract first unposted item
3. Instagram for Business → Create Photo Post (caption + image URL)
4. GitHub → update `instagram_queue.json` (mark item as posted)

**Credentials needed:**
| Credential | Where to get |
|------------|-------------|
| Instagram Business account | Meta Business Suite — must be Business or Creator account |
| GitHub PAT (read + write) | github.com/settings/tokens |

---

## Data Files

- `automation/data/instagram_queue.json` — posts waiting to be published
- `automation/data/instagram_posted.json` — history of published posts

---

## Python Integration

`automation/modules/make_integration.py` — triggers Make.com scenarios via webhook when called from Python.

Env vars required:
```
MAKE_WEBHOOK_BASE=https://hook.eu1.make.com/your-webhook-id
MAKE_WEBHOOK_SECRET=your_secret
```

---

## Phases Deferred

| Phase | What | When |
|-------|------|------|
| Phase 2 | Pinterest Auto-Poster (3x daily) | After IG is stable |
| Phase 3 | Daily Summary Report | After Pinterest live |
| Phase 4 | Content Queue Monitor | After Phase 3 |
| Phase 5 | Uptime Monitor | Low priority |
| Later | Telegram notifications | When re-enabled |

---

## Cost

| Plan | Price | Ops/month | Active scenarios |
|------|-------|-----------|-----------------|
| Free | $0 | 1,000 | 2 |
| Core | $9/month | 10,000 | Unlimited |

Start on free tier to test. Upgrade to Core when all phases are live.

---

*SleepWise Reviews - Make.com Integration Plan | April 2026*
