# Make.com — Instagram Auto-Poster Setup
## SleepWise Reviews | Phase 1

---

## What This Does

Every day at your chosen time, Make.com will:
1. Read the next post from `instagram_queue.json` on GitHub
2. Post it to your Instagram Business account
3. Mark it as posted and update the file on GitHub

**10 posts ready in queue** (ig_002 → ig_011). Zero manual work once live.

---

## Before You Start

Confirm you have:
- [ ] Make.com account (already created)
- [ ] Instagram account switched to **Business or Creator** (required for API posting)
- [ ] Instagram connected to a **Facebook Page** (Meta requirement)
- [ ] GitHub PAT with `repo` scope

---

## Step 1 — Add Credentials in Make.com

Go to **Connections** in Make.com and add these two:

### A. GitHub Connection
- Click **Add** → search `GitHub` → select **GitHub**
- Name it: `GitHub - SleepWise`
- Auth method: **Personal Access Token**
- Token: your GitHub PAT (needs `repo` read + write scope)
- Test → Save

### B. Instagram for Business Connection
- Click **Add** → search `Instagram` → select **Instagram for Business**
- Name it: `Instagram - SleepWise`
- Click **Sign in with Facebook** → authorize your Facebook Page + Instagram account
- Save

---

## Step 2 — Create the Scenario

Go to **Scenarios** → **Create a new scenario**

### Module 1: GitHub — Get a File
Search `GitHub` → **Get a File**

| Field | Value |
|-------|-------|
| Connection | `GitHub - SleepWise` |
| Repository Owner | `Hanysharaf` |
| Repository Name | `sleepwisereviews` |
| File Path | `automation/data/instagram_queue.json` |
| Branch | `main` |

### Module 2: JSON — Parse JSON
Search `JSON` → **Parse JSON**

| Field | Value |
|-------|-------|
| JSON String | `{{1.content}}` (content from Module 1) |

### Module 3: Tools — Get First Item
Search `Tools` → **Get First Item of Array**
(or use a **Set Variable** to map `{{2.array[1]}}` — the first item in the parsed array)

| Field | Value |
|-------|-------|
| Array | `{{2.array}}` |

### Module 4: Instagram for Business — Create a Photo Post
Search `Instagram for Business` → **Create a Post**

| Field | Value |
|-------|-------|
| Connection | `Instagram - SleepWise` |
| Image URL | `{{3.image_url}}` |
| Caption | `{{3.caption}}` `{{nl}}` `{{nl}}` `{{3.hashtags}}` `{{nl}}` `{{nl}}` `{{3.product_link}}` |

> `{{nl}}` = newline in Make.com. Add blank lines between caption, hashtags, and link for clean formatting.

### Module 5: GitHub — Update a File
Search `GitHub` → **Update a File**

This marks the posted item and removes it from the queue.

| Field | Value |
|-------|-------|
| Connection | `GitHub - SleepWise` |
| Repository Owner | `Hanysharaf` |
| Repository Name | `sleepwisereviews` |
| File Path | `automation/data/instagram_queue.json` |
| Branch | `main` |
| Content | Use a **JSON — Create JSON** module first to rebuild the array without item `{{3.id}}` |
| Commit Message | `Auto: posted {{3.id}} - {{3.topic}}` |

> For the queue update: Use a **Tools — Array Aggregator** or **JSON — Create JSON** to rebuild the array skipping the first item (`slice(1)`).

---

## Step 3 — Set the Schedule

Click the **clock icon** on the scenario:
- Type: **Every day**
- Time: Pick your preferred time (recommendation: 9:00 AM local time)
- Timezone: Set to your timezone

---

## Step 4 — Test Before Activating

1. Click **Run once** — this triggers the scenario manually
2. Check each module shows a green checkmark
3. Verify the post appeared on your Instagram profile
4. Check `instagram_queue.json` on GitHub — first item should be gone

---

## Queue Status

| File | Location | Posts ready |
|------|----------|-------------|
| `instagram_queue.json` | `automation/data/` | 10 (ig_002 → ig_011) |

Image URLs are served via GitHub raw content:
```
https://raw.githubusercontent.com/Hanysharaf/sleepwisereviews/main/images/instagram/ig-XXX.png
```

---

## Adding More Posts Later

Add new items to `instagram_queue.json` following this structure:
```json
{
  "id": "ig_013",
  "topic": "Your Topic",
  "caption": "Your caption text here",
  "hashtags": "#Tag1 #Tag2 #Tag3",
  "image_url": "https://raw.githubusercontent.com/Hanysharaf/sleepwisereviews/main/images/instagram/ig-013.png",
  "product_link": "https://www.amazon.com/s?k=your-product&tag=sleepwiserevi-20",
  "posted": false
}
```

Upload matching image to `images/instagram/ig-013.png` and push to GitHub.

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| GitHub 404 | Check file path — must be `automation/data/instagram_queue.json` |
| Instagram auth error | Re-authorize the Facebook connection |
| Image rejected | Instagram requires min 320px wide, max 1440px. Check image dimensions. |
| Queue empty | Add new items to `instagram_queue.json` |
| SHA mismatch on GitHub update | Re-run — SHA updates after each write |
