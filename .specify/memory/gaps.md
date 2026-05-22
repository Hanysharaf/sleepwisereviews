# SleepWiseReviews — Gap Analysis

*Generated: 2026-05-22 | Based on full project audit*

---

## Critical Gaps (blocking revenue or automation)

| # | Gap | Spec | Impact |
|---|-----|------|--------|
| G1 | Instagram auto-posting NOT live | 006 | Content piles up in queue but nothing gets posted |
| G2 | Facebook pipeline does not exist | 008 | No Facebook presence at all — zero channel |
| G3 | Meta MCP not set up (ig-mcp + facebook-mcp-server) | 006, 008 | Blocking G1 and G2 |
| G4 | SEO content machine not built | 008 | No systematic keyword → article pipeline |
| G5 | ~~Only 30 of 160 pages indexed in Search Console~~ **PARTIALLY FIXED 2026-05-22** | 001 | `robots.txt` and `.nojekyll` added and pushed. Next: resubmit sitemap in Search Console. Root cause: missing robots.txt (Google couldn't auto-discover sitemap) + missing .nojekyll (Jekyll processing on static HTML site). All 169 sitemap URLs verified against real files — no broken links. |
| G6 | 38 clicks, 0 conversions (March 2026) | 001 | Affiliate revenue = $0 |

---

## Infrastructure Gaps (technical debt)

| # | Gap | Spec | Risk |
|---|-----|------|------|
| I1 | `google_credentials.json` + `service_account.json` in data/ directory | 007 | Secrets committed to repo = security violation |
| I2 | Pinterest direct API blocked (consumer type) | 003 | n8n is workaround but not officially supported path |
| I3 | `auto_scheduler.py` referenced in CLAUDE.md but not in module inventory | 002 | May not exist — needs verification |
| I4 | `sleepwise.db` schema undocumented | 002 | Unknown what's stored there |
| I5 | GitHub raw image URLs used for Pinterest — can break | 003 | Pins could go dead if repo structure changes |
| I6 | No retry/alert on GitHub Actions failures | 002 | Silent failures — automation can stop without notice |

---

## Content Gaps

| # | Gap | Spec | Notes |
|---|-----|------|-------|
| C1 | No JSON-LD structured data on articles | 001 | Missing FAQ schema, Product schema, Review schema — affects rich results |
| C2 | Internal linking is manual with no audit | 001 | Many articles likely have 0 or 1 internal links |
| C3 | Email list: 1 subscriber via Brevo | 001 | Email channel completely undeveloped |
| C4 | `link-in-bio.html` content not verified against current article catalog | 006 | May be out of date |
| C5 | Backdated articles (2020–2024) may not have accurate publication dates for SEO | 001 | Google may distrust artificial history |

---

## Missing Features

| # | Feature | Spec | Priority |
|---|---------|------|----------|
| M1 | Keyword research automation | 008 | High — feeds entire SEO pipeline |
| M2 | Single-command pipeline trigger | 008 | High — manual multi-step process now |
| M3 | Facebook post generation + posting | 008 | High — zero presence |
| M4 | Revenue tracking automation (pull from Amazon Associates API) | — | Medium |
| M5 | `/pin` Telegram command | 004 | Low |
| M6 | Search Console ranking tracker | — | Medium — needed to find position 5–15 articles to optimize |
| M7 | A/B testing for pin/post formats | 003, 006 | Low |
| M8 | Pinterest analytics pull automation | 003 | Medium |

---

## Next Priorities (suggested order)

1. **Fix G5** — diagnose Search Console indexing gap (160 pages, only 30 indexed) — this is a foundational SEO problem
2. **Fix G3** — set up Meta MCP (ig-mcp + facebook-mcp-server)
3. **Fix G1** — connect Instagram auto-posting via ig-mcp
4. **Build M1 + M2** — keyword research + single-command pipeline (Spec 008)
5. **Build M3** — Facebook posting pipeline
6. **Fix I1** — move Google credentials to GitHub Actions Secrets
