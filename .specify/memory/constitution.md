# SleepWiseReviews Constitution

## Core Principles

### I. Static-First Architecture
Every content artifact is a file committed to the GitHub repo. No database, no CMS, no server-side rendering. HTML files committed to the repo are the canonical source of truth. The site deploys automatically via GitHub Actions on every push — no manual deploy steps.

### II. Affiliate Compliance is Non-Negotiable
Every article containing affiliate links MUST include the Amazon Associates disclosure statement at the top of the article body. Social posts MUST NOT contain direct affiliate URLs. The affiliate tag `sleepwiserevi-20` MUST appear in every Amazon product link. Omitting disclosure is a policy violation that risks account termination.

### III. Search Intent Before Volume
Every keyword MUST demonstrate buyer intent (transactional or "best X for Y" informational with purchase signal). Search volume is a tiebreaker — intent comes first. No keyword enters the content calendar without a clear match to the sleep products niche: ear plugs, sleep masks, pillows, white noise machines, mattress toppers, weighted blankets.

### IV. One Article → All Channels
An article is the atomic unit of the pipeline. One keyword in = one HTML article + one Instagram post + one Facebook post + one Google Sheets calendar row updated. Social posts are never created without a published article. A partial pipeline run is a failure state — the pipeline MUST complete all outputs or none.

### V. Template Consistency
All article HTML MUST use the existing site template (header/footer/nav structure). No per-article layout customization. Any template change must be propagated to all existing articles before shipping new ones. New articles saved to `/posts/` for blog content or `/pages/` for evergreen guides.

## Quality Gates

Before a pipeline run is considered complete, ALL of the following must be true:

1. **Article committed** — HTML file is in `/posts/` or `/pages/` in the repo, pushed to main branch
2. **SEO elements present** — H1 equals exact target keyword; `<title>` and `<meta description>` are populated; at least 2 internal links to existing articles
3. **Affiliate disclosure present** — Disclosure statement appears before the first affiliate link in the article
4. **Tag verified** — All Amazon links contain `sleepwiserevi-20`
5. **Social posts written** — Instagram (150–200 words + hashtags + image prompt) and Facebook (100–150 words + article URL) posts are stored in Google Sheets
6. **No affiliate links in social** — Instagram and Facebook posts contain no direct affiliate URLs
7. **Calendar updated** — Google Sheets content calendar row status set to `published`
8. **Sitemap updated** — `sitemap.xml` includes the new article URL

## Governance

This constitution is owned by the SleepWiseReviews project. Amendments require running `/speckit-constitution` with the change described. All feature specs (`.specify/specs/*/spec.md`) must reference at least one principle by Roman numeral. A spec that would violate a principle requires an explicit constitutional amendment before the spec can proceed.

---

**Version**: 1.0.0 | **Ratified**: 2026-05-22 | **Last Amended**: 2026-05-22
