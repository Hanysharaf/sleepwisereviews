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

**FAQPage JSON-LD must always be paired with a visible FAQ section — never JSON-only.** If a post's schema includes `"@type": "FAQPage"`, the same questions and answers — same wording, no paraphrasing — must also render as real content on the page: `<h2>Frequently Asked Questions</h2>` followed by one `<h3>` (question) + `<p>` (answer) pair per JSON-LD entry, wrapped in `.faq-visible-item` blocks inside a `.faq-visible-section` container (CSS: `var(--gold, #c9a84c)` for question text, `var(--text, #e8eaf0)` for answers, `var(--border, #1e2d45)` for item dividers — these var() fallbacks make the block render correctly regardless of which color-variable family the post's own `<style>` block uses). Insert it as a sibling among the post's other top-level H2 sections, placed right before whichever comes first: `.related-articles`, `.related-guides`, `</main>`, or `<footer>`. Google's structured-data guideline requires marked-up content to actually be visible to readers — JSON-only FAQ content risks losing rich-result eligibility or a manual action for spammy markup. A 2026-09-24 audit found 261 posts with this gap by raw pattern-matching, but a proper check (parsing DOM Q/A across all three template shapes in use — `.faq-item` divs, `<details><summary>`, and bare heading+`<p>` pairs — then comparing against JSON-LD Q/A text) narrowed the real "zero visible representation" set to 168, which were backfilled; 91 further posts render a FAQ with different wording than their schema (a separate, unresolved issue — do not conflate the two) — see `sleepwise_faq_visible_content_audit` memory.

**Every post must carry a Related Guides section — no post should link to nothing else on the site.** In the Internal Linking step (or Draft/Deploy, if internal links are assembled then), every post — including generic product-roundup posts (`best-pillow`, `best-topper`, `best-sheets`, `best-gadget`, etc.), not just condition-guide posts — must include a `<section class="related-guides">` block with 3–5 links to genuinely topical posts (same product category, adjacent condition/use-case, or a relevant educational article) — never a "6 most recent posts" or fully-random fallback. Each link is a card with the target's real title and a one-line reason it's relevant, e.g.:
```html
<section class="related-guides" style="background:var(--card,#111e33);border-top:2px solid var(--border,#1e3a5f);padding:2rem 1.25rem;margin-top:2rem;">
  <div style="max-width:820px;margin:0 auto;">
    <h2 style="color:var(--gold,#c9a84c);font-size:1.05rem;letter-spacing:.04em;margin-bottom:1rem;text-transform:uppercase;">Related Guides</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem;">
      <div style="background:var(--bg,#0a1628);border:1px solid var(--border,#1e3a5f);border-radius:.5rem;padding:1rem;">
        <h3 style="font-size:.9rem;font-weight:700;margin:0 0 .35rem;line-height:1.3;"><a href="TARGET.html" style="color:var(--gold,#c9a84c);text-decoration:none;">Target Post Title</a></h3>
        <p style="font-size:.8rem;color:var(--muted,#8892a4);margin:0;line-height:1.4;">One-line reason this is genuinely related.</p>
      </div>
      <!-- 2-4 more cards -->
    </div>
  </div>
</section>
```
Use `var(--x, #hex)` fallbacks (not hardcoded hex) exactly as shown — same reasoning as the FAQ guardrail above — so the block renders correctly regardless of which color-variable family the post's own `<style>` block defines. Insert it right before `<footer` (all templates in use close every content wrapper before that point, so a full-bleed section is always safe there). A 2026-09-24 audit found 116 of 202 generic product-roundup posts had zero internal links anywhere in the body (condition-guide posts were ~89% covered via this same pattern) — backfilled with topically-curated links per post, not mechanical/recent-post filler — see `sleepwise_related_posts_backfill` memory. **This step lives in the workflow, not only in `automation/templates/article_template.html`** — that template is currently dormant (the real publish pipeline is `automation/publish_scheduler.py` copying pre-authored files from `scheduled/`, per `sleepwise_actual_publish_pipeline` memory), so relying on the template alone would not have caught this gap; the template also has the corresponding `{{RELATED_SECTION}}` placeholder for completeness, but the enforcement point is this workflow step.

## Project Documents

- **Constitution / full project doc**: `..\..\Ravi\projects\sleepwisereviews.md` — stack, Make.com scenario, Telegram bot, GitHub Actions, affiliate programs, current status, routing table
- **Spec inventory**: `.specify/specs/` — 8 specs (P0a/P0b/etc.) tracking SEO, redirects, homepage, topic browse, traffic baseline
- **Speckit constitution**: `.specify/memory/constitution.md`

## Robots.txt + .nojekyll

If a deploy regresses indexing, check that `.nojekyll` exists at site root (GitHub Pages will otherwise apply Jekyll filtering and break paths starting with `_`). robots.txt must not block `/posts/` or `/`. See `sleepwisereviews_spec` memory for the fix history.
