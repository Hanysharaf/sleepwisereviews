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

## Knowledge Graph

`graphify-out/` contains a built knowledge graph (145 infrastructure files: automation/, telegram_bot/, .specify/, docs/, scheduled/, .github/) — **366.7× token reduction per query**.

```bash
python -m graphify query "how does the Telegram bot trigger pin posts" --budget 2000
python -m graphify explain "auto_scheduler"
```

Excluded from graph: `posts/` (blog content), `images/`, `pages/` — content, not infrastructure.

## Batch Workflow

When generating new blog posts (or any large content batch), use the standard 6-agent pattern:

1. **Research** → 2. **Outline** → 3. **Draft** → 4. **SEO pass** → 5. **Internal linking** → 6. **Deploy**

When Sonnet hits rate limits mid-batch, fall back to Haiku for steps 4–5 (SEO + linking are deterministic enough). See `sleepwisereviews_batch_workflow` memory for the deploy script template.

**Instagram follow CTA is mandatory.** The Draft step (or Deploy step, if the footer is assembled then) must include a "Follow us on Instagram @sleepwise.reviews" CTA in the post footer, linking to `https://www.instagram.com/sleepwise.reviews`. Use `sleepwise.reviews` — with the dot — never `sleepwisereviews`; the no-dot handle is a wrong/nonexistent account and a recurring bug. Model the footer link on `posts/magnesium-deficiency-sleep.html`, which has a correctly-handled working example. Do not skip this for any new post.

**Heading hierarchy must not skip levels.** In the Draft step, product-roundup ("best-X") posts must nest each product's Pros/Cons directly under its H2 as H3 — never H4. Any intro block before the first product (TOC, "Key Features to Compare", "Quick Summary", etc.) is itself a top-level section and must be H2, not H3 — never insert an H3 before the first H2. One H1 per post; no other level may jump by more than one (H2 → H3 → H4, never H2 → H4). A 2026-09-23 audit found 351/639 published posts (all pre-dating the current batch workflow) violating this and backfilled them — see `sleepwise_heading_hierarchy_audit` memory.

## Project Documents

- **Constitution / full project doc**: `..\..\Ravi\projects\sleepwisereviews.md` — stack, Make.com scenario, Telegram bot, GitHub Actions, affiliate programs, current status, routing table
- **Spec inventory**: `.specify/specs/` — 8 specs (P0a/P0b/etc.) tracking SEO, redirects, homepage, topic browse, traffic baseline
- **Speckit constitution**: `.specify/memory/constitution.md`

## Robots.txt + .nojekyll

If a deploy regresses indexing, check that `.nojekyll` exists at site root (GitHub Pages will otherwise apply Jekyll filtering and break paths starting with `_`). robots.txt must not block `/posts/` or `/`. See `sleepwisereviews_spec` memory for the fix history.
