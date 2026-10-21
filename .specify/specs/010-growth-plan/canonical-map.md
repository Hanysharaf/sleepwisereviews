# Canonical map and Search Console findings (spec 010)

Source: Search Console, web, last 3 months to 2026-10-21, read live (968 queries, 3,943 impressions across them). Page-level mapping (which URL ranks for which query) is NOT done yet - see "Open".

## What the real query data says

Impressions by topic (sum of all matching queries):

| Topic | Queries | Impressions | Best sign |
|---|---|---|---|
| Weighted blanket | 53 | 834 | "weighted blanket price comparison" @ 10.4 (68 impr), "best cooling weighted blanket 2024" @ 9.4, "weighted blanket reviews 2024" @ 7.3 |
| Earplugs | 101 | 629 | all head terms at positions 70-95 |
| Snoring | 86 | 330 | "anti snoring devices" @ 60.7 (86 impr) |
| Mattress / toppers | 71 | 325 | "best firm mattress toppers" @ 26.7 |
| Sleep supplements / vitamins | 74 | 281 | "deep sleep supplement" @ 66.5 |
| Pregnancy pillow | 45 | 229 | "best pregnancy pillow" @ 84.3 |
| Natural sleep aid / sleep aid | 74 | 159 | long phrase queries only |
| Melatonin | 59 | 146 | "strongest melatonin" @ 63.4, "best melatonin" @ 73.5 |
| Magnesium | 30 | 103 | "best magnesium for sleep" @ 79.7 (61 impr) |
| Sleep mask | 30 | 80 | positions 60-70 |
| White noise | 32 | 51 | brand-name queries |
| Tart cherry | 0 | 0 | no queries |
| Elderly / senior | 0 | 0 | no queries |

Findings:
- "best weighted blanket" (386 impr) and "best weighted blankets" (176) sit at position 116-118. The page exists but is effectively not ranking. This is the biggest single pool of impressions.
- Three weighted-blanket queries already sit between positions 7 and 11: these are the closest to page 1 and the first things to improve.
- The 10 questions from the Guardian/Healthline/SERP research are real niche demand, but our site has almost no impressions on melatonin, magnesium, natural sleep aids, tart cherry or elderly. They build authority and AI-answer visibility; they are not where today's impressions are.
- Many "positions 1-8" queries are long assistant-style questions with 1 impression each ("which nutraceutical company makes..."). They are not human search volume; ignore them as signals.

## Priority change to the plan

Keep the 90-day plan and the 10 questions. Change the order of work inside it:
1. Weighted blanket first (quick wins at 7-11 plus a page not ranking at 117).
2. Earplugs and snoring next (large impression pools, all at positions 60-95).
3. Magnesium, melatonin and supplements third (these also carry the research-evidence angle).
4. Tart cherry and elderly last (no demand data yet; written for authority).

## Canonical page candidates (to confirm against page-level data)

| Question | Candidate canonical page | Notes |
|---|---|---|
| Weighted blanket | posts/best-weighted-blanket.html | wave-1 page; 6 variants exist |
| Earplugs | posts/best-earplugs-sleeping.html | wave-2 page; head terms at 70-95 |
| Natural sleep aid | posts/natural-sleep-aids.html | |
| Supplements / vitamins | posts/best-sleep-supplements-guide.html | |
| Magnesium | posts/best-magnesium-glycinate-sleep.html | 8 overlapping pages |
| Melatonin | posts/melatonin-guide.html + unpublished draft | claims flagged 2026-10-04 |
| Sleep mask | posts/best-sleep-masks.html | wave-2 |
| White noise | posts/best-white-noise-machine.html | wave-1 |
| Tart cherry | new: posts/does-tart-cherry-juice-help-sleep.html | |
| Elderly | new: posts/natural-sleep-aids-elderly.html | |

## Page-level data (Search Console Pages view, 3 months, read 2026-10-21)

| Page | Impressions | Avg position |
|---|---|---|
| posts/article-weighted-blanket.html | 878 | 91.9 |
| posts/best-earplugs-sleeping.html | 688 | 74.4 |
| posts/best-anti-snoring-devices.html | 465 | 53.8 |
| posts/best-smart-mattresses.html | 383 | 38.0 |
| posts/natural-sleep-aids.html | 306 | 68.8 |
| posts/best-pregnancy-pillows.html | 265 | 71.3 |
| posts/best-melatonin-supplements.html | 235 | 44.3 |
| posts/article-magnesium-sleep.html | 135 | 56.4 |
| posts/best-sleep-masks.html | 116 | 65.0 |

Correction: for weighted blankets Google ranks `article-weighted-blanket.html`, not the wave-1 page `best-weighted-blanket.html`. Canonical for weighted blanket = `article-weighted-blanket.html` (upgraded 2026-10-21, not yet committed). Magnesium canonical = `article-magnesium-sleep.html`.

## Done 2026-10-21: weighted blanket page (uncommitted)

`posts/article-weighted-blanket.html` edited in place: title/H1/meta to 2026 "Price and Cooling"; removed unsupported testing claims (30 nights, 14 blankets, 6 testers, 18 minutes faster, 12% deep sleep, 5 of 6 testers); "How We Tested" became "How We Compared" (editorial ratings, not lab measurements); FAQ rewritten with hedged evidence; added quick-answer, "Weighted Blanket Price Comparison" heading, Sources and Further Reading, related links to the 5 sibling pages; dates fixed; JSON-LD updated and valid. Backup of the original: session scratchpad.
Flagged, not changed: the "1,247 found this helpful" like counter is seeded, not real (site-wide template feature).

## Open

- Page-level data (which URL each query lands on) was not captured: the Search Console Pages view did not load in the browser tool. Next: open the Pages tab by hand or export CSV, then confirm or change the candidates above.
- Amazon Associates policy on link placement (T007) not yet checked.
