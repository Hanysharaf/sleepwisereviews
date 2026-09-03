# Spec 001: Static Site & Content Library

**Principle refs:** I (Static-First), II (Affiliate Compliance), V (Template Consistency)
**Status:** LIVE

---

## What It Is

GitHub Pages static site hosting 633 published HTML articles and 15 static pages. All content is committed HTML files — no database, no CMS.

---

## Components

### Published Content
| Location | Count | Purpose |
|----------|-------|---------|
| `posts/` | 633 articles (verified 2026-08-21) | Blog content (reviews, guides, science, special topics, lifestyle) |
| `pages/` | 15 pages (verified 2026-08-21) | Static pages (about, privacy, affiliate disclosure, 6 category landing pages, 404, + editorial-standards/how-we-test/is-the-sale-real/warranty-reality-check added since) |
| `index.html` | 1 | Homepage |
| `link-in-bio.html` | 1 | Social media "link in bio" landing page |
| `sitemap.xml` | 1 | All indexed URLs — updated on every article publish |

### Article Categories
| Category | Article Count |
|----------|--------------|
| Sleep Science / Education | 50+ |
| Product Reviews | 35+ |
| Practical Guides | 30+ |
| Special Topics | 25+ |
| Lifestyle | 14+ |

### Article Structure (all articles follow this template)
- `<title>` — SEO meta title
- `<meta name="description">` — Meta description
- Breadcrumb nav
- H1 — exact target keyword
- Table of contents
- Affiliate disclosure (before first affiliate link)
- H2 sections per sub-question
- Product recommendations with Amazon affiliate links (`sleepwiserevi-20` tag)
- FAQ block
- Internal links to 2+ related articles
- Social sharing buttons
- Sticky buy bar (product pages)
- Footer with site nav

### Template
- File: `automation/templates/article_template.html`
- Managed by: `automation/modules/website_manager.py`

---

## Deployment

- Platform: GitHub Pages
- Repo: `Hanysharaf/sleepwisereviews`
- Branch: `main`
- Custom domain: `sleepwisereviews.com` (via `CNAME`)
- Deploy trigger: every push to main (GitHub Pages auto-deploys)

---

## Analytics

- **Google Analytics 4**: `G-ZKGY2B72WH` — site-wide by decision (2026-08-31, Hany). Backfilled onto all 457 posts, 12 category hub pages, the post-generator template, and 2 internal artifact files (`automation/data/review.html`, `docs/SleepWiseReviews-ActionPlan.html`) — Hany chose full coverage over excluding internal files. Tool: `automation/scripts/patch_ga4_tag.py`, idempotent — re-run after any future gap. Confirmed: 725 of 725 HTML files tagged.
- **Google Search Console**: verified via GA tag; `sitemap.xml` submitted (30 pages discovered as of last audit)

---

## Affiliate

- Program: Amazon Associates US
- Tag: `sleepwiserevi-20`
- Revenue (March 2026): 38 clicks, 0 conversions, $0 earnings
- Other programs registered: ClickBank, ShareASale, Impact (available in `affiliate_manager.py` — not yet generating traffic)

---

## Gaps

- [ ] Search Console shows only 30 pages indexed out of 160 — needs investigation
- [ ] 154 articles span 2020–2026 (backdated for credibility) — may dilute authority signals; no audit of which are driving traffic
- [x] ~~`link-in-bio.html` exists but no confirmed Instagram profile linking to it~~ — RESOLVED per spec 006, which records this as CONFIRMED (not independently re-verified against the live Instagram profile in this pass).
- [ ] Email capture via Brevo — form exists on site, but only 1 subscriber recorded
- [x] ~~No structured data (JSON-LD schema) on any articles~~ — PARTIALLY RESOLVED. Verified 2026-08-21: 502 of 633 article files carry `"@type": "Article"` JSON-LD (E-E-A-T authority patcher, commit `5435e57`) — the "on any articles" claim is false. 131 of 633 still lack it (likely older/un-patched posts). FAQ/Product/Review schema still not confirmed present anywhere — needs Hany's input if that matters.
- [ ] Internal linking is manual — no automated cross-link audit
- [x] ~~Footer/header nav 404s (privacy/about/disclaimer/contact/reviews/guides)~~ — RESOLVED 2026-09-02/03. Full-site audit (2026-08-28) found footer links on 280/634 posts pointing at `/privacy.html`, `/about.html` etc. that don't exist — real files live under `pages/` with different names. Fixed via script across two passes: footer (179 files, 339 links repointed, 27 removed where no real target exists — contact/reviews/guides pages don't exist anywhere in the repo) then header nav (21 files, 33 links — `/reviews` and `/guides` turned out to have real targets after all, `pages/category-product-reviews.html` and `pages/category-guides.html`, just weren't linked correctly). Commits `88b2246`, `8909b86`.
- [x] ~~Related-article cross-links broken~~ — RESOLVED 2026-09-02. Two bugs: double-prefix `posts/posts/...` (60 links, 10 files) and slug mismatches where the linked filename was never the real published slug (30 links, 25 files — audit's original estimate of ~10 undercounted this). Commit `88b2246`.
- [x] ~~335/634 posts missing Open Graph tags~~ — RESOLVED 2026-09-02/03. 330 backfilled directly (the other 5 flagged by the audit turned out to be noindex redirect stubs, not broken pages). Separately found 45 posts (16 custom + 29 default og:image) pointing at an `assets/` folder that doesn't exist anywhere in this repo — a same-named `automation/data/broken_covers_backup_2026-07-12/` folder looked like it might be a real backup but turned out to be an unrelated Instagram content-queue artifact. All 45 repointed to the real working default `images/og-default.png` (already used successfully by 584 other posts) since no real asset recovery was possible. Commits `88b2246`, `8909b86`.
- [ ] Homepage anchor IDs (`#guides`, `#about`) referenced by some templates don't exist on `index.html` (only `#reviews` does) — found 2026-09-03 while fixing header nav, not yet actioned.
