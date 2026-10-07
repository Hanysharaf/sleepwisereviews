# Spec 007: Content Calendar & Google Sheets Integration

**Principle refs:** IV (One Article → All Channels)
**Status:** LIVE — used for scheduling and queue management

---

## What It Is

Google Sheets document serving as the central content calendar: tracks article schedule, social media queue, image prompts, and publish status.

---

## Sheets Integration Points

| Script / Module | What It Does |
|----------------|-------------|
| `publish-scheduler.yml` (GitHub Actions) | Reads calendar daily at 08:00 UTC — publishes articles scheduled for today |
| `populate_content_calendar.py` | ONE-TIME: populated 56 scheduled articles into the sheet |
| `fix_content_types.py` | ONE-TIME: corrected content type classifications |
| `sync_prompts_to_sheet.py` | Writes DALL-E 3 prompts from `ig_image_prompts.txt` into sheet |
| `update_sheet_urls.py` | Writes generated image URLs + QA status back into sheet |
| `generators/generate_ig_images.py` | Reads image prompts from sheet |

---

## Calendar Columns (inferred from scripts)

| Column | Purpose |
|--------|---------|
| Article title | SEO target keyword |
| Content type | Category (product review, guide, science, etc.) |
| Publish date | Scheduled publish date |
| Status | `scheduled` → `published` |
| Instagram caption | Generated caption text |
| Instagram hashtags | 5–10 hashtags |
| Image prompt | DALL-E 3 / Gemini prompt for image gen |
| Image URL | Generated image URL (from GitHub or CDN) |
| Slide URLs (s1–s5) | Carousel slide image URLs |
| QA status | Review flag before posting |
| Article URL | Live URL after publish |

---

## Credentials

- `automation/data/google_credentials.json` — Google Sheets API credentials
- `automation/data/service_account.json` — Service account credentials
- Library: `gspread` (in `requirements.txt`)

---

## Sheet Identity

- Sheet name: "SleepWise Reviews - Content Calendar 2026"
- Sheet ID: `1KeWK1xO5eiD2YbFe63Fx8sV9Vf6jUwi57h71fc8zb5o`
- Tabs (verified 2026-10-07, read-only via the repo's service account; 10 tabs): `IG QUEUE`, `PINTEREST QUEUE` (91 rows), `TIKTOK QUEUE`, `YT SHORTS QUEUE`, `THREADS QUEUE`, `MONTHLY CALENDAR`, `PHASE CHECKPOINTS`, `ANALYTICS`, `CONTENT IDEAS`, `Content Calendar`.
- Tab `Content Calendar` is the article-publishing schedule (live, used daily by `automation/publish_scheduler.py` and `automation/seo_pipeline.py`; the "Publish Scheduled Articles" workflow ran successfully 2026-10-04 to 10-06). Columns: `publish_date`, `article_filename`, `article_title`, `category`, `status`, `published_at`. 56 data rows at 2026-10-07 (31 PENDING, 25 PUBLISHED). The "Calendar Columns (inferred from scripts)" table above describes the social-queue tabs, not this tab.
- Tab: `IG QUEUE`
- Columns (confirmed 2026-08-04, in order): ID, Scheduled Date, Content Type, Hook/Title, Caption, Hashtags, Visual Prompt, Image URL, Affiliate Link, Status, Posted At, Post URL, Notes, Platform, QA, Slide 2 URL, Slide 3 URL, Slide 4 URL, Slide 5 URL

## Gaps

- [x] ~~Sheet ID and tab names not documented in any spec~~ — RESOLVED 2026-08-04, see Sheet Identity above.
- [x] ~~`google_credentials.json` and `service_account.json` in `data/` directory — these are secrets; should be in GitHub Actions Secrets, not the filesystem~~ — RESOLVED. Verified 2026-08-21: both are gitignored and not committed.
- [x] ~~No column schema document~~ — RESOLVED 2026-08-04, see Sheet Identity above.
- [ ] No status for Facebook posts column — Facebook pipeline not yet in the calendar
- [x] ~~No Pinterest queue column in Google Sheets~~ — STALE, corrected 2026-10-07: a `PINTEREST QUEUE` tab with 91 rows exists in the sheet. `pinterest_queue.json` (20 items, last changed 2026-05-26) is a separate older local queue; the two are not synced.
- [ ] Social post content for already-published articles not retroactively added to the sheet
- [ ] QA status column is documented as "review flag before posting" but the Make.com posting scenario (spec 006) does not actually check it — only Status=PENDING gates posting. Documentation says one thing, the automation does another.
