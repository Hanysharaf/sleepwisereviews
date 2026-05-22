# Spec 001: Static Site & Content Library

**Principle refs:** I (Static-First), II (Affiliate Compliance), V (Template Consistency)
**Status:** LIVE

---

## What It Is

GitHub Pages static site hosting 158 published HTML articles and 10 static pages. All content is committed HTML files — no database, no CMS.

---

## Components

### Published Content
| Location | Count | Purpose |
|----------|-------|---------|
| `posts/` | 154 articles | Blog content (reviews, guides, science, special topics, lifestyle) |
| `pages/` | 10 pages | Static pages (about, privacy, affiliate disclosure, 6 category landing pages, 404) |
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

- **Google Analytics 4**: `G-ZKGY2B72WH` — injected into all 160 HTML pages
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
- [ ] `link-in-bio.html` exists but no confirmed Instagram profile linking to it
- [ ] Email capture via Brevo — form exists on site, but only 1 subscriber recorded
- [ ] No structured data (JSON-LD schema) on any articles — missing FAQ schema, Product schema, Review schema
- [ ] Internal linking is manual — no automated cross-link audit
