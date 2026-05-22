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

## Gaps

- [ ] Sheet ID and tab names not documented in any spec — if the sheet is renamed or recreated, all scripts break silently
- [ ] `google_credentials.json` and `service_account.json` in `data/` directory — these are secrets; should be in GitHub Actions Secrets, not the filesystem
- [ ] No column schema document — column positions are hardcoded in scripts; adding a column breaks everything
- [ ] No status for Facebook posts column — Facebook pipeline not yet in the calendar
- [ ] No Pinterest queue column in Google Sheets — Pinterest uses `pinterest_queue.json` separately (two separate systems for the same calendar concept)
- [ ] Social post content for already-published articles not retroactively added to the sheet
