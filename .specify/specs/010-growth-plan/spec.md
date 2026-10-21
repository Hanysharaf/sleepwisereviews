# Feature Specification: Growth Plan (organic traffic + affiliate revenue)

**Status**: Draft
**Created**: 2026-10-21
**Feature Directory**: .specify/specs/010-growth-plan
**Principles referenced**: II (Affiliate Compliance), III (Search Intent), V (Template Consistency)

---

## Problem Statement

SleepWiseReviews has 600+ posts but almost no search traffic: 2 web search clicks in the last 3 months (Search Console, checked 2026-10-21) and an average position near 64 (June baseline). More posts have not moved this. The site lacks topical authority and trust signals on the questions people actually search, so it earns no meaningful affiliate revenue.

## User Stories

### US1 (P1): Own the top 10 niche questions with evidence-first answers
**As a** reader with a sleep problem, **I want to** get a direct, sourced answer to my question, **so that** I can decide what to try and trust the page.

**Acceptance Criteria**:
- [ ] Each of the 10 target questions (see `deliverables/SleepWiseReviews/niche-competitor-analysis-2026-10-21.md`) has one page that answers it in the first screen.
- [ ] Each page shows what the research says, with real citations from AASM, NIH, CDC, Cochrane or PubMed, and states the limits of the evidence.
- [ ] Each page has a visible byline, last-reviewed date and affiliate disclosure.
- [ ] No page claims first-hand testing that did not happen.

### US2 (P1): A hub that connects the answers
**As a** reader, **I want to** one page that organises sleep aids by what the evidence supports, **so that** I can find the right topic fast.

**Acceptance Criteria**:
- [ ] One hub page links to all 10 answer pages and states how products and claims are selected.
- [ ] Every answer page links back to the hub and to 2 related pages.
- [ ] Hub shows byline, disclosure and methodology above the fold.

### US3 (P1): Target keywords from real search data
**As the** site owner, **I want to** choose pages to improve from our own Search Console queries, **so that** effort goes where Google already shows us.

**Acceptance Criteria**:
- [ ] A ranked list of queries with impressions and position is produced from Search Console, starting with positions 8 to 30.
- [ ] Each of the 10 target questions is mapped to an existing page or marked "new".
- [ ] The list is refreshed on a fixed schedule.

### US4 (P2): Affiliate revenue from pages that already get impressions
**As the** site owner, **I want to** place honest product recommendations on the pages that already earn impressions, **so that** traffic turns into commission.

**Acceptance Criteria**:
- [ ] The 5 accessory pages with the most impressions each have a clear pick, price band and disclosure.
- [ ] Affiliate links appear only on the site, never in Reddit comments.
- [ ] Affiliate performance (clicks, orders, earnings) is recorded weekly.

### US5 (P2): A credible Reddit presence (no links)
**As the** site owner, **I want to** build the u/IcyHamster1512 account through genuinely helpful answers, **so that** it becomes a trusted reference.

**Acceptance Criteria**:
- [ ] Replies follow subreddit rules, contain no links and make no medical-advice claims.
- [ ] Reply style is varied and shorter, not templated.
- [ ] Account karma, removals and replies are checked each session.

## Success Criteria

- Baseline (Search Console, web, last 3 months to 2026-10-21): 2 clicks, 5.45K impressions (about 1.8K per 30 days), average position 54.8, CTR 0%.
- 10 of 10 target questions have a published, sourced answer page by day 60, plus the hub.
- Weekly progress review recorded in the session log every week, with the current numbers and the next action.

### 90-day targets (proposed, achievable for a young low-authority site)

| Measure (per 30 days, read at end of window) | Baseline | Day 30 | Day 60 | Day 90 |
|---|---|---|---|---|
| Search clicks | 0-1 | 3 | 10 | 25 |
| Impressions | about 1.8K | 2.5K | 3.5K | 5K |
| 10 target pages, average position | not tracked | mapped | 35 | 25 |
| Target pages in positions 11-20 | 0 | 2 | 5 | 8 |
| Canonical pages upgraded to evidence-first (of 10; 2 are new) + hub | 0 | 3 | 10 + hub | 10 + hub, refreshed |
| Organic-attributed affiliate orders | 0 | 0 | 0 | at least 1 |
| Reddit karma / removed comments | 15 / 0 | 25 / 0 | 40 / 0 | 60 / 0 |
| Reddit standalone posts (no links) | 0 | 1 | 2 | 4 |

Site-wide average position is not a target: new pages dilute it. Track the 10 target pages instead.

### 90-day split

- **Days 1-30 - Foundation:** pull Search Console queries and map the 10 questions to existing or new pages; fix the Search Console properties and sitemap; publish the hub shell and 3 answer pages (melatonin, magnesium, natural sleep aids); request indexing within the daily quota; 1 Reddit post; weekly Reddit check.
- **Days 31-60 - Build:** publish the remaining 7 answer pages and complete the hub; interlink every page to the hub and 2 related pages; re-index; start recording Amazon Associates numbers weekly.
- **Days 61-90 - Convert and refine:** add honest picks and disclosure to the 5 top accessory pages; refresh pages sitting at positions 11-20 using Search Console data; review what moved and drop what did not.

## Scope

**In scope**:
- The 10 target question pages and the hub
- Search Console query review and mapping
- Honest affiliate placement on top accessory pages
- Reddit account, no links

**Out of scope**:
- Mass-editing the 600 older mattress posts
- Paid ads
- Social pipelines (Pinterest, Instagram) changes
- Fake testing claims, fake personas or invented credentials

## Assumptions

- Harry Soul stays the permanent pen name; ownership disclosed, Hany's face and name not public.
- Search volumes are not available without a keyword tool; Search Console data is the source of truth.
- Amazon Associates policy on where links may appear is checked before any new link placement.

## Dependencies

- Search Console access for sleepwisereviews.com
- Existing pages from spec 008 (SEO content machine) and wave 1 and 2 AI-Overview pages
- Source access for research citations (AASM, NIH, CDC, Cochrane, PubMed)
