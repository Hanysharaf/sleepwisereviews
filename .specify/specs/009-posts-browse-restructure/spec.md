# Spec 009: Posts Browse Restructure — Two-Level Topic Browse

**Principle refs:** I (Static-First), V (Template Consistency)
**Status:** PLANNED
**Created:** 2026-05-27
**Trigger:** Hany flagged 2026-05-27 — current `/posts/index.html` "card view looks bad" (P0a). One flat page with 12 inline article lists does not scale to 621 articles.

---

## What It Is

Replace the current single-page categorized index (`/posts/index.html`, all 12 categories rendered inline as `<ul>` lists) with a two-level topic browse:

- **Level 1 — Topics landing** (`/posts/index.html`): 12 category cards in a grid + one cross-category search bar that searches all 621 article titles.
- **Level 2 — Topic detail** (`/posts/category/<slug>.html`, one per category): article cards for that category only + one search bar scoped to that category + breadcrumb back to Level 1.

The page title "All Sleep Guides & Articles" appears on both levels and is a clickable link back to Level 1.

---

## Why

1. **UX:** Current page is a wall of links — no visual hierarchy, no scannable category overview. Mobile especially poor.
2. **SEO:** Hub-and-spoke topic clusters improve internal link equity to high-converting condition/product pages. Each category gets its own indexable hub URL.
3. **Scale:** 621 articles in one page is not the right surface area for a first-time visitor. Topic-first navigation reduces choice fatigue.

---

## Behavior

### Level 1 — `/posts/index.html` (Topics landing)

| Element | Spec |
|---------|------|
| Page title | `<h1>All Sleep Guides & Articles</h1>` — wrapped in `<a href="/posts/">` (self-link; serves as the universal "back to topics" anchor from Level 2) |
| Subtitle | `621 science-backed articles across 12 topics` |
| Search bar | Searches all 621 article titles. Match → article appears in a results panel below the search box, grouped by category, with a category badge under each title. Hides the category grid while results are visible. Empty input → restores category grid. |
| Category grid | 12 cards, responsive (3 columns desktop, 2 tablet, 1 mobile) |
| Card content | Icon (inline SVG, lucide-style) · Category name · Article count · One-line description · "Browse →" |
| Card click target | Entire card is a link to `/posts/category/<slug>.html` |
| No article lists | Article titles are NOT rendered on Level 1 except inside the search results panel |

### Level 2 — `/posts/category/<slug>.html` (Topic detail)

| Element | Spec |
|---------|------|
| Breadcrumb | `<a href="/posts/">All Sleep Guides & Articles</a> → <span>{Category Name}</span>` |
| Page heading | `<h1>{Category Name}</h1>` with subtitle `{count} articles` |
| Search bar | Searches only article titles within this category. Empty → all cards visible. Match → only matching cards visible. No match → "no results" panel with contact CTAs (same as current `posts/index.html`). |
| Article grid | One card per article in this category, responsive (3 columns desktop, 2 tablet, 1 mobile) |
| Card content | Article title · short excerpt (~140 chars from the article's `<meta name="description">`) · "Read →" link |
| Card click target | Entire card is a link to `/posts/<slug>.html` |
| Footer link | `← Back to All Sleep Guides & Articles` |

### Categories (12)

| Slug | Display Name |
|------|--------------|
| `insomnia-cbti` | Insomnia & CBT-I |
| `sleep-science` | Sleep Science |
| `caffeine-nutrition` | Caffeine & Nutrition |
| `sleep-environment` | Sleep Environment |
| `health-conditions` | Health Conditions |
| `life-stages` | Life Stages |
| `timing-jet-lag` | Timing & Jet Lag |
| `napping-performance` | Napping & Performance |
| `guides-plans` | Guides & Plans |
| `mattresses-bedding` | Mattresses & Bedding |
| `sleep-products` | Sleep Products |
| `supplements` | Supplements |

Category-to-article mapping is the existing `CATEGORIES` dict in `generate_posts_index.py` — unchanged.

---

## File Changes

### Modified
- `generate_posts_index.py` — extended to:
  1. Render new `/posts/index.html` (cards-only Level 1)
  2. Render 12 `/posts/category/<slug>.html` files (Level 2)
  3. Extract `<meta name="description">` from each article HTML for the card excerpt
  4. Persist a single shared CSS block in both templates (same look-and-feel as current index — dark navy `#0a1628` / gold `#c9a84c`)
  5. Add canonical, OG, and JSON-LD `CollectionPage` schema to each Level 2 page

### New
- `posts/category/` directory created (12 files)
- One small JSON file `posts/search-index.json` (optional, only if needed for Level 1 cross-category search performance — defer until performance test on real data; first pass embeds the searchable index inline in the page as a JS object since ~621 titles fits comfortably)

### Updated
- `sitemap.xml` — append the 12 new category URLs
- `automation/modules/website_manager.py` — if it has a posts-index trigger, ensure it calls the extended generator (no behavior change otherwise)

### Unchanged
- All 621 existing article files in `/posts/*.html`
- Homepage `index.html`
- All category landing pages in `/pages/` (different from new `/posts/category/`)
- Existing redirects, robots.txt, .nojekyll
- All existing internal links pointing to `/posts/` continue to work (Level 1 is still served at that URL)

---

## Acceptance

A pipeline run is complete when ALL of the following are true:

1. **Level 1 rendered** — `/posts/index.html` exists, shows 12 cards, no inline article lists, search box works across all 621 titles
2. **Level 2 rendered** — All 12 `/posts/category/<slug>.html` files exist, each shows article cards for its category with scoped search
3. **Heading link works** — Clicking "All Sleep Guides & Articles" on any Level 2 page navigates to `/posts/`
4. **Card click works** — Clicking a category card on Level 1 navigates to the correct Level 2 page
5. **Article click works** — Clicking an article card on Level 2 navigates to the correct article
6. **Sitemap updated** — All 12 new URLs present in `sitemap.xml`
7. **No broken articles** — All 621 articles remain reachable; canonical-audit passes
8. **Mobile renders cleanly** — At 375px width, Level 1 shows 1-col card grid; Level 2 shows 1-col article cards; both search bars usable

---

## Out of Scope (this spec)

- Article card thumbnails (no images — title + excerpt only for v1)
- Filter chips beyond the search box (e.g. price, mattress type) — deferred to a future spec if usage warrants
- Server-side search — Pages stay static; search is client-side JS
- Category description content — first version uses one stock sentence per category; copy-polish is a separate task
- Multi-language

---

## SEO Notes

- Each Level 2 page is a `CollectionPage` per schema.org with a name, description, and `mainEntity` listing its articles. This is stronger topic-cluster signal than the current single flat page.
- Internal link graph: Level 1 → 12 Level 2 hubs → 621 articles. Each article currently has 2+ internal links to other articles (existing rule); this restructure ADDS topic-hub backlinks without removing existing ones.
- Sitemap priority: `/posts/index.html` = 0.9, `/posts/category/*.html` = 0.8, individual articles = 0.7 (current).

---

## Implementation Order

1. Extend `generate_posts_index.py` to support both Level 1 and Level 2 generation
2. Write a category-page HTML template string with shared CSS
3. Build Level 2 first (one category — e.g. `sleep-science` — has only 12 articles, smallest test bed)
4. Verify Level 2 looks right on desktop + mobile + search works
5. Build remaining 11 Level 2 pages
6. Rebuild Level 1 with cards-only layout
7. Update `sitemap.xml`
8. Local preview (open `index.html` and one category page in browser)
9. Commit + push — GitHub Pages auto-deploys
10. Verify live URLs all load and link correctly
