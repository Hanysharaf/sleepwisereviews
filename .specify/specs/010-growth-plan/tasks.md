# Implementation Tasks: Growth Plan (organic traffic + affiliate revenue)

**Spec**: .specify/specs/010-growth-plan/spec.md
**Plan**: .specify/specs/010-growth-plan/plan.md
**Total tasks**: 42
**Created**: 2026-10-21
**Day 1**: 2026-10-21 | **Day 30**: 2026-11-20 | **Day 60**: 2026-12-20 | **Day 90**: 2027-01-19

Paths are relative to `Projects/SleepReviewes/` unless stated. Pages live in `posts/` or `pages/`.

---

## Phase 1: Setup (days 1-7)

- [x] T001 Create the weekly tracker with the 90-day target table from spec.md in `deliverables/SleepWiseReviews/growth-tracker.md` (in the Ravi folder)
- [x] T002 Record the day-1 baseline (2 clicks, 5.45K impressions, position 54.8, Reddit karma 15) as the first row of `deliverables/SleepWiseReviews/growth-tracker.md`
- [ ] T003 [P] Export Search Console queries and pages for the last 3 months to `automation/data/gsc_queries_2026-10-21.csv`
- [ ] T004 [P] Verify the `sc-domain:sleepwisereviews.com` property is the one in use, check ownership methods and the sitemap status in Search Console, and write the result to the tracker

## Phase 2: Foundation (days 1-14)

- [ ] T005 Map each of the 10 questions to its candidate pages using `automation/data/gsc_queries_2026-10-21.csv` and write the choice of one canonical page per question to `.specify/specs/010-growth-plan/canonical-map.md`
- [ ] T006 For the overlapping magnesium, melatonin and supplement pages, list which pages should point to the canonical page in `.specify/specs/010-growth-plan/canonical-map.md`
- [ ] T007 Check the Amazon Associates operating policy on where affiliate links may appear and record the answer in `.specify/specs/010-growth-plan/canonical-map.md`
- [ ] T008 Confirm the Search Console indexing request quota and plan the request order for the first 10 pages in the tracker

## Phase 3: Evidence-first answers and hub (P1, US1 + US2) - days 8-60

**Goal**: ten canonical pages in evidence-first format and one hub connecting them.
**Done when**: all 10 canonical pages show a first-screen answer, a table, real citations with limits, byline, date and disclosure; the hub links to all 10 and each page links back.

Days 8-30 (first three, plus hub shell):
- [ ] T009 [US1] Review `scheduled/why-melatonin-stops-working.html`, fix any claim the evidence does not support, and publish it with sources
- [ ] T010 [US1] Correct the overstated pineal-downregulation and dependency claims in `posts/melatonin-guide.html` and `posts/wrong-using-melatonin-sleeping-pill.html` (flagged 2026-10-04; needs Hany's OK before editing)
- [ ] T011 [P] [US1] Upgrade the canonical magnesium page chosen in T005 (candidate `posts/best-magnesium-glycinate-sleep.html`) to evidence-first format
- [ ] T012 [P] [US1] Upgrade `posts/natural-sleep-aids.html` to evidence-first format
- [ ] T013 [US2] Build the hub shell `pages/sleep-aids-evidence-hub.html` with methodology block, byline and disclosure
- [ ] T014 [US1] Add `sitemap.xml` entries for new and changed pages in `sitemap.xml`
- [ ] T015 [US1] Request indexing for the pages from T009, T011, T012 and T013 in Search Console (within the daily quota)

Days 31-60 (remaining pages):
- [ ] T016 [P] [US1] Upgrade the canonical page for "which sleep supplement works best" (candidate `posts/best-sleep-supplements-guide.html`)
- [ ] T017 [P] [US1] Upgrade the canonical page for "vitamins and supplements for sleep and anxiety" (candidate `posts/best-sleep-supplement-anxiety.html`)
- [ ] T018 [P] [US1] Write the new page "does tart cherry juice help you sleep" in `posts/does-tart-cherry-juice-help-sleep.html`
- [ ] T019 [P] [US1] Write the new page "best natural sleep aid for the elderly" in `posts/natural-sleep-aids-elderly.html`
- [ ] T020 [P] [US1] Link the wave-1 and wave-2 pages (sleep masks, earplugs, weighted blanket, white noise) into the hub from `pages/sleep-aids-evidence-hub.html` without rewriting them
- [ ] T021 [US2] Complete the hub: link all 10 canonical pages and add 2 related links on every canonical page
- [ ] T022 [US1] Point the overlapping magnesium, melatonin and supplement pages at their canonical page with an internal link, as listed in `.specify/specs/010-growth-plan/canonical-map.md`
- [ ] T023 [US1] Add `sitemap.xml` entries for the new pages and the hub in `sitemap.xml`
- [ ] T024 [US1] Request indexing for the remaining pages in Search Console (spread over several days within the quota)

## Phase 4: Keyword targeting from real data (P1, US3) - ongoing

**Goal**: effort follows Search Console data.
**Done when**: a ranked query list exists, every question is mapped, and the list is refreshed monthly.

- [ ] T025 [US3] Produce the ranked query list (positions 8-30 first) in `deliverables/SleepWiseReviews/gsc-query-priorities.md`
- [ ] T026 [US3] Refresh `deliverables/SleepWiseReviews/gsc-query-priorities.md` on day 30, day 60 and day 90

## Phase 5: Convert (P2, US4) - days 61-90

**Goal**: honest picks on the pages that already earn impressions.
**Done when**: the 5 top accessory pages each have a pick, price band and disclosure, and Associates numbers are logged weekly.

- [ ] T027 [US4] Choose the 5 accessory pages with the most impressions from `automation/data/gsc_queries_2026-10-21.csv` and list them in `.specify/specs/010-growth-plan/canonical-map.md`
- [ ] T028 [US4] Add a clear pick, price band and disclosure before the first affiliate link on each of the 5 pages, with tag `sleepwiserevi-20` on every Amazon link
- [ ] T029 [US4] Record Associates clicks, orders and earnings every week in `deliverables/SleepWiseReviews/growth-tracker.md`

## Phase 6: Reddit credibility (P2, US5) - ongoing

**Goal**: u/IcyHamster1512 grows through helpful answers, no links.
**Done when**: karma is 60 with no removals by day 90.

- [ ] T030 [US5] Re-check the 4 replies posted on 2026-10-21 for answers, and record karma and removals in `deliverables/SleepWiseReviews/growth-tracker.md`
- [ ] T031 [US5] Publish one link-free standalone post on wake-time versus bedtime on r/sleep and record it in the tracker (day 30)
- [ ] T032 [US5] Reply to 3 fresh threads per week, short and varied, following subreddit rules

## Phase 7: Off-site authority (P1, US6) - days 15-90

**Goal**: earn relevant links and mentions without paid or manipulative tactics.
**Done when**: 70 outreach messages sent, 3 earned links recorded, referring domains tracked monthly.

- [ ] T035 [US6] Record today's referring domains and top linking sites from Search Console Links in `deliverables/SleepWiseReviews/growth-tracker.md`
- [ ] T036 [US6] Build the list of 40 target sites (sleep and health resource pages, sleep blogs and newsletters, reviewer roundups, university and library lists) with the page to link and a contact route in `deliverables/SleepWiseReviews/authority-targets.md`
- [ ] T037 [P] [US6] Publish a short citable reference page from the hub evidence table at `pages/sleep-aids-evidence-table.html` (sourced, dated, no affiliate links) and add it to `sitemap.xml`
- [ ] T038 [P] [US6] Write three outreach templates (resource-page addition, outdated-page correction, roundup or newsletter offer) in `deliverables/SleepWiseReviews/authority-outreach-templates.md`; each leads with value, discloses the pen name honestly and makes no credential claims
- [ ] T039 [US6] Search for unlinked mentions of SleepWiseReviews and Harry Soul and list them with the request to add a link in `deliverables/SleepWiseReviews/authority-targets.md`
- [ ] T040 [US6] Send 5 personalised outreach messages per week (Hany sends or approves each) and log sender, date, template and reply in `deliverables/SleepWiseReviews/authority-targets.md`
- [ ] T041 [US6] Follow up once on each message after 7 days and record earned links in `deliverables/SleepWiseReviews/growth-tracker.md`
- [ ] T042 [US6] On day 60 and day 90, review which message types got replies, stop the ones that did not, and write the result in `deliverables/SleepWiseReviews/growth-tracker.md`

## Final Phase: Polish and Validation

- [ ] T033 Run the constitution quality gates on every new or changed page (SEO elements, disclosure before first affiliate link, tag, sitemap) and note failures in the tracker
- [ ] T034 Review the tracker against the 90-day table on day 30, day 60 and day 90; stop or change any track that has not moved

---

## Dependency Graph

- Phase 2 needs T003 and T004 from Phase 1.
- Phase 3 needs T005 (canonical map) from Phase 2; T010 needs Hany's OK.
- T021 needs T013 and all upgraded pages; T022 needs T006.
- Phase 4 needs T003. Phase 5 needs T027 after Phase 3 pages are live. Phase 6 runs alongside everything.
- T033 and T034 follow each milestone.

## Parallelization Opportunities

- T003 and T004
- T011 and T012
- T016, T017, T018, T019 and T020

## MVP Scope

Phases 1, 2 and the first half of Phase 3 (T001-T015): tracker, canonical map, melatonin fix, magnesium and natural-sleep-aids upgrades, hub shell and indexing. This is the day-30 milestone.
