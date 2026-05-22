# Spec 008: SEO Content Machine

**Principle refs:** III (Search Intent Before Volume), II (Affiliate Compliance), IV (One Article → All Channels), I (Static-First), V (Template Consistency)
**Status:** NOT BUILT — planned feature

---

## What It Is

End-to-end pipeline triggered from Claude Code: seed topic in → article committed + Instagram post + Facebook post + Google Sheets calendar row updated. No manual copy-paste between steps.

---

## Pipeline

```
Seed topic (e.g. "best ear plugs for sleeping")
  ↓
STEP 1: Keyword Research
  → Find top 10 buyer-intent questions from Google (People Also Ask, autocomplete)
  → Rank by: buyer intent first, search volume second, competition last
  → Filter: must match sleep niche (ear plugs, masks, pillows, white noise, toppers, blankets)
  → Output: 10 keyword rows written to Google Sheets content calendar

STEP 2: Article Generation (one keyword at a time)
  → Input: one keyword row from Google Sheets
  → Generate: 1,200–2,000 word HTML article
  → Structure: H1 = exact keyword | intro | H2 per sub-question | product recs + affiliate links | FAQ | conclusion
  → SEO: meta title | meta description | alt text | 2+ internal links to existing articles
  → Disclosure: Amazon Associates disclosure at top (Constitution Principle II)
  → Affiliate tag: sleepwiserevi-20 in all Amazon links
  → Template: use article_template.html (Constitution Principle V)
  → Output: HTML file saved to /posts/ or /pages/

STEP 3: Social Posts
  → Input: the article just generated
  → Output A — Instagram post:
      150–200 words | hook + tip + CTA "link in bio" | 5–10 hashtags | Canva image prompt
      NO affiliate links (Constitution Principle II)
  → Output B — Facebook post:
      100–150 words | conversational tone | CTA to article URL
      NO affiliate links
  → Store both in Google Sheets (same row as the article)

STEP 4: Publish
  → Commit article HTML to GitHub repo → GitHub Actions deploys automatically
  → Update sitemap.xml (via website_manager.py)
  → Update Google Sheets row status → "published"
  → Instagram post → ig-mcp (when Meta MCP is set up) OR manual queue to instagram_queue.json
  → Facebook post → facebook-mcp-server (when Meta MCP is set up) OR stored for manual posting
```

---

## Trigger

Single Claude Code command:
```
/speckit-run seo-content-machine --seed "best ear plugs for sleeping"
```
Or conversationally: "Run the SEO pipeline for [topic]"

---

## Keyword Research — Free Sources Only

| Source | Method | Priority |
|--------|--------|----------|
| Google People Also Ask | Scrape / WebSearch | First |
| Google autocomplete | Query variations ("best _ for sleeping") | Second |
| Ahrefs free tier | Manual lookup | Third |
| Answer the Public (free) | Pattern queries | Fourth |

Scoring criteria (in order):
1. Buyer intent signal ("best", "top", "review", "vs", "for sleeping")
2. Niche match (sleep products only)
3. Search volume (higher = better, but not required)
4. Competition (lower = better)

---

## Article Quality Requirements

Before any article is committed:
- [ ] H1 = exact target keyword (no variation)
- [ ] `<title>` populated (format: `Keyword | SleepWiseReviews`)
- [ ] `<meta name="description">` populated (150–160 chars)
- [ ] Affiliate disclosure appears before first Amazon link
- [ ] All Amazon links contain `sleepwiserevi-20`
- [ ] At least 2 internal links to existing articles
- [ ] Word count 1,200–2,000
- [ ] Uses `article_template.html` (not a custom layout)

---

## Social Post Quality Requirements

Before social posts are stored in Google Sheets:
- [ ] Instagram: 150–200 words, has CTA "link in bio", has 5–10 hashtags
- [ ] Instagram: NO affiliate URLs
- [ ] Facebook: 100–150 words, has article URL
- [ ] Facebook: NO affiliate URLs
- [ ] Both posts reference the article topic (not generic sleep content)

---

## Success Criteria (per pipeline run)

1. 1 article committed and live at `sleepwisereviews.com/posts/<slug>.html`
2. Instagram post stored in Google Sheets (same row, "ig_post" column)
3. Facebook post stored in Google Sheets (same row, "fb_post" column)
4. Row status = `published`
5. `sitemap.xml` updated
6. No manual copy-paste required

---

## Dependencies / Blockers

| Dependency | Status | Blocker |
|------------|--------|---------|
| Claude API (article gen) | ACTIVE | None |
| Google Sheets (calendar write) | ACTIVE | None |
| GitHub repo (article commit) | ACTIVE | None |
| `website_manager.py` (sitemap update) | ACTIVE | None |
| ig-mcp (Instagram posting) | NOT SET UP | Needs Meta Business account + ig-mcp install |
| facebook-mcp-server (FB posting) | NOT SET UP | Needs Meta app submission |
| Keyword research automation | NOT BUILT | Need to implement scraping or Ahrefs free API |

---

## Gaps vs Current State

- [ ] No keyword research script exists — this is entirely new work
- [ ] No single-command pipeline trigger — steps are currently separate scripts, not one flow
- [ ] Facebook has no module or integration at all — `make_integration.py` and `buffer_integration.py` don't cover Facebook organic posts
- [ ] Google Sheets schema needs Facebook post column added
- [ ] Meta MCP (ig-mcp + facebook-mcp-server) must be set up before publish step is fully automated
