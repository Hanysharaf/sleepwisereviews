# Spec 005: Image Generation

**Principle refs:** I (Static-First), IV (One Article → All Channels)
**Status:** MULTI-ENGINE — Pillow (active), DALL-E 3 (active), Gemini Imagen 3 (active)

---

## What It Is

Three-engine image generation pipeline for producing Pinterest pins, Instagram carousels, and general social media images.

---

## Engines

### Engine 1: Pillow (Local, Free)
- **Module:** `automation/modules/image_generator.py`
- **Script:** `automation/scripts/generators/create_content.py`
- **What it generates:** Branded Pinterest pins and Instagram posts with text overlays
- **Image specs:** Custom colors/dimensions per platform
- **Dependencies:** `Pillow` (in `requirements.txt`)
- **Cost:** Free (local processing)

### Engine 2: DALL-E 3 (AI, Paid)
- **Script:** `automation/scripts/generators/generate_ig_images.py`
- **Workflow:**
  1. Reads prompts from `automation/data/ig_image_prompts.txt`
  2. Also reads prompts from Google Sheets (via `sync_prompts_to_sheet.py`)
  3. Calls DALL-E 3 API to generate images
  4. Uploads generated images to GitHub repo
  5. Updates Google Sheets with image URLs + QA status via `update_sheet_urls.py`
- **Cost:** OpenAI API (per image)

### Engine 3: Gemini Imagen 3.0 (AI, Paid)
- **Script:** `execute_prompts.py` (repo root)
- **What it does:** Reads prompts → calls Google Gemini Imagen 3.0 → saves images locally
- **Cost:** Google AI API (per image)

---

## Instagram Carousel Builder
- **Script:** `automation/scripts/build_carousels_batch.py`
- **What it builds:** Multi-slide carousels (5 slides: s1–s5)
- **Input:** `automation/data/slide_content.json`
- **Output:** Slide images per carousel
- **Module:** `automation/modules/instagram_prep.py` handles carousel assembly and captions

---

## Image Hosting

Images are referenced by URL in queue files. Hosting options configured in `.env`:
- **GitHub repo** (primary) — images committed to repo, served via GitHub raw URLs
- **Cloudinary** (optional) — `CLOUDINARY_URL` in env
- **Imgur** (optional fallback) — `IMGUR_CLIENT_ID` in env

---

## Gaps

- [ ] GitHub raw URLs for images can be unreliable at scale — no CDN in front of them
- [ ] No image size/quality validation before posting — oversized images can fail at Pinterest/Instagram
- [ ] DALL-E 3 costs are unbounded — no monthly spend cap enforced in code
- [ ] Gemini Imagen (`execute_prompts.py`) is a standalone script at repo root — not integrated into the automation pipeline
- [ ] No image A/B testing — all images use same visual template; no tracking of which image styles drive more clicks
- [ ] Carousel images built but Instagram posting is not yet automated — carousels sit in queue
