# Technical Plan: Growth Plan (organic traffic + affiliate revenue)

**Status**: Draft - waiting on constitution decision (see Constitution Check)
**Spec**: .specify/specs/010-growth-plan/spec.md
**Created**: 2026-10-21

---

## Constitution Check

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Static-First | Compliant | All pages are HTML files committed to the repo. Tracking is a markdown file in the repo. |
| II. Affiliate Compliance | Compliant | Disclosure before the first affiliate link on every page; tag `sleepwiserevi-20` on every Amazon link; no affiliate URLs on Reddit or social. |
| III. Search Intent Before Volume | Review needed | Answer pages ("does tart cherry juice help sleep") are informational, and the keyword rule limits keywords to the product niche. Justified: they feed the product pages through the hub and internal links, and SERP data shows these are the queries that rank. Needs an amendment or a scoped exception. |
| IV. One Article -> All Channels | Review needed | Rule says every article must produce Instagram and Facebook posts or the run fails. The growth work is page quality and structure, not new social output. Needs an amendment or a scoped exception. |
| V. Template Consistency | Compliant | Reuse the existing template and the wave-1 `.quick-answer` and `.comparison-table` styles. No per-page layout changes. |

Governance: every spec must reference a principle by Roman numeral. Spec 010 references II, III and V (to be added to spec.md). Two items above need a constitutional amendment (v1.1.0) before the affected pages ship.

Proposed amendment wording:
- III: add "Evidence/answer pages are allowed when they link to a purchase-intent page in the same hub."
- IV: add "Evidence/answer pages and hub pages are exempt from the social-post output; the pipeline completes without them."

---

## What already exists (checked 2026-10-21 in the repo)

This plan builds on the existing site. Most of the 10 questions already have pages:

| Question | Existing pages (examples) | Gap |
|---|---|---|
| Natural sleep aid | natural-sleep-aids | none; upgrade |
| Which supplement works best / sleep vitamins | best-sleep-supplements-guide, best-deep-sleep-supplement, best-vitamin-d-sleep | many overlapping pages |
| Magnesium for sleep | article-magnesium-sleep, best-magnesium-glycinate-sleep, best-magnesium-for-sleep-anxiety + 5 more | 8 overlapping pages: pick one canonical |
| Tart cherry | best-tart-cherry-supplement | no "does tart cherry juice help sleep" answer |
| Sleep mask / earplugs | best-sleep-masks, best-earplugs-sleeping | wave 2 done; link only |
| Weighted blanket | best-weighted-blanket (+6 variants) | wave 1 done; link only |
| White noise | best-white-noise-machine (+4 variants) | wave 1 done; link only |
| Melatonin | melatonin-guide, best-melatonin-supplements, unpublished "why melatonin stops working" draft | publish draft; fix overstatements flagged 2026-10-04 |
| Natural aid for elderly | none | only real new page |

Wave 1 (7 pages) and wave 2 (17 pages) already use the evidence-first format (quick answer, table, real sources, freshness). So the work is: pick one canonical page per question, upgrade it, and point the overlapping pages at it with internal links. Nothing is deleted or rewritten from scratch. The constitution amendment below only ratifies what wave 1 and 2 already did.

## Architecture Overview

One hub page links to ten evidence-first answer pages. Each answer page leads with a direct answer, a comparison table, a "what the research shows" section with real citations, honest limits and an affiliate disclosure with at most one or two product picks. Search Console query data decides which existing pages are upgraded and which are new. A weekly tracker file records the numbers against the 90-day targets.

## Tech Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Pages | Static HTML in `/posts/` and `/pages/` | Constitution I and V |
| Search data | Search Console performance export | Only trusted source of query, position and click data |
| Research sources | AASM, NIH, CDC, Cochrane, PubMed top-level URLs | Matches the existing wave-1 rule: never invent deep links or DOIs |
| Tracker | `deliverables/SleepWiseReviews/growth-tracker.md` | Simple, versioned, readable by every session |
| Reddit | Existing account, comments by hand or via the browser tool | No links, subreddit rules respected |

## Data Model

### Target page
| Field | Type | Notes |
|-------|------|-------|
| question | Text | One of the 10 target questions |
| url | Text | Existing page or "new" |
| status | Text | mapped / drafted / published / indexed / refreshed |
| position | Number | From Search Console, weekly |
| impressions | Number | 30-day |
| clicks | Number | 30-day |

### Weekly row
| Field | Type | Notes |
|-------|------|-------|
| week | Date | Monday |
| clicks, impressions | Number | Search Console, last 30 days |
| pages published | Number | Of 10 plus hub |
| reddit karma / removals | Number | From the profile |
| associates clicks / orders / earnings | Number | Manual from the Associates dashboard |

**Relationships**: Weekly row aggregates the Target pages.

## Implementation Strategy

### Phase 1: Foundation (days 1-30)
Export Search Console queries; confirm the canonical page for each of the 10 questions from the table above (using impressions and position to choose); verify properties and sitemap; build the hub shell; upgrade the first three canonical pages (melatonin including the unpublished draft, magnesium, natural sleep aids); request indexing within the daily quota; create the tracker; first Reddit post.

### Phase 2: US1 and US2 - upgrade and hub (days 31-60)
Upgrade the remaining canonical pages and write the two new ones (tart cherry juice answer, natural sleep aid for elderly); point the overlapping magnesium, melatonin and supplement pages at their canonical page; complete the hub with methodology, byline and disclosure; interlink every page to the hub and two related pages; re-index.

### Phase 3: US4 - convert (days 61-90)
Add honest picks and price bands to the five accessory pages with the most impressions; refresh pages sitting at positions 11-20; start the weekly Associates log; check Amazon Associates policy before any new link placement.

### Authority track: US6 (starts day 15, runs to day 90)
Why: Search Console shows pages stuck at positions 55 to 118. Honest quality edits are necessary but cannot create authority on their own; relevant sites linking to us can.
- **Days 15-30:** build the target list (40 sites). Record current referring domains from Search Console Links. Publish one citable asset: the evidence table from the hub as a short, link-ready "sleep aids: what the evidence says" reference.
- **Days 31-60:** send 5 personalised outreach messages a week (resource-page additions, corrections of outdated pages, offering the evidence table to roundup and newsletter writers). Find unlinked mentions and ask for the link.
- **Days 61-90:** follow up once, record results, double down on the message types that got replies, drop the rest.
- **Rules:** no paid links, no link swaps at scale, no private blog networks, no fake credentials or personas. Harry Soul is the pen name; outreach never claims medical credentials. Affiliate relationship is disclosed if asked. Reddit stays link-free.
- **Expectation:** a low-authority site usually earns few links in 90 days. The target is 3 earned links and 70 messages; a miss is information, not failure.

### Ongoing: US3 and US5
Weekly Search Console review; Reddit check each session, no links.

## Validation Approach

- Each page: pass the constitution quality gates plus citations that resolve and a visible byline, date and disclosure.
- Each week: update the tracker and compare to the 90-day table in the spec.
- Day 30, 60, 90: review against targets; stop or change any track that has not moved.

## Open Questions / Risks

- Constitution amendment for III and IV needs Hany's approval before affected pages ship.
- Indexing quota (about 10 manual requests per day) limits how fast new pages are requested.
- Traffic may lag: new pages usually need weeks to rank. Targets are set for that.
- Amazon Associates link rules for Reddit or social must be confirmed before any link is shared there.
- Many posts depend on citations; if a source cannot be verified it is left out, not invented.
