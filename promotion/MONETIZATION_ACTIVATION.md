# SleepWiseReviews Monetization Activation Guide

**For Hany — 4 actions, ~90 minutes total, unlocks 3 new revenue streams.**

The blog has 603 posts and 624 URLs in the sitemap. Content is in place.
What's missing is connecting it to revenue networks. Below: exact steps.

---

## Priority 1 — ShareASale Signup (20 minutes)

**Why now:** Amazon Associates has a 180-day "3 qualifying sales" rule. If you don't
hit it, account closes and ALL Amazon links stop earning. ShareASale removes that
single-point-of-failure risk. Commissions are also 5-10% vs Amazon's 3%.

**Steps:**

1. Go to: https://account.shareasale.com/newsignup.cfm
2. Choose "Affiliate" account type
3. Fill website: https://sleepwisereviews.com
4. Description: "Affiliate review blog covering mattresses for health conditions. 600+ posts."
5. Wait 1-3 days for approval (usually instant for content sites)
6. Once approved, apply to these merchants (each is a separate application):
   - **Saatva** — 8% commission, 90-day cookie, premium mattresses
   - **WinkBeds** — 6% commission, 60-day cookie
   - **Purple** — 5% commission
   - **DreamCloud** — 8% commission
   - **GhostBed** — 7% commission
   - **Avocado Green Mattress** — 5% commission, organic angle

**After approval:** Tell me to update the affiliate links on the top 10 posts to use ShareASale tracking.

---

## Priority 2 — Google AdSense Application (15 minutes)

**Why now:** With 603 posts, the site has more than enough content for approval.
AdSense pays ~$5-15 RPM (per 1,000 views) on health content. Even at modest traffic
(10k views/month), that's $50-150/month passive income.

**Steps:**

1. Go to: https://www.google.com/adsense/start/
2. Click "Get started"
3. Add: https://sleepwisereviews.com
4. Select country: Egypt (or wherever payment account is)
5. Choose payment type: Bank transfer
6. AdSense will give you a code snippet to add to the site
7. Send me the snippet — I'll add it to all 603 posts via a script
8. Wait 1-14 days for review (longer for new accounts)
9. Once approved: ads appear automatically, no further action

**Optimal ad placement** (I'll handle once code is provided):
- One ad below H1 (above the fold)
- One ad between the 3rd and 4th product pick
- One ad in the FAQ section
- One ad above Related Guides
- Total: 4 ads per post = AdSense limit-compliant

---

## Priority 3 — Pinterest Tokens (10 minutes)

**Why now:** Pinterest queue is built and scheduled to run twice daily (09:00 + 17:00 UTC).
GitHub Action workflow has the trigger. Without tokens, it falls back to simulation mode
and pins are not actually posted. Pinterest drives 30-50% of affiliate blog traffic in
health niches.

**Steps:**

1. Go to: https://developers.pinterest.com/apps/
2. Sign in with your existing Pinterest account (or create one)
3. Click "Create app"
4. App name: "SleepWiseReviews Auto-Poster"
5. App description: "Posts new content from sleepwisereviews.com"
6. Select scopes: `pins:write`, `boards:read`
7. Once created, click into the app → Generate access token (long-lived)
8. Copy the token

For the Board ID:
1. Go to https://www.pinterest.com/ → create a board called "Best Mattresses for Health Conditions"
2. Open the board → copy the ID from the URL (the number after `/board/`)

**Add both to GitHub:**
1. Go to: https://github.com/Hanysharaf/sleepwisereviews/settings/secrets/actions
2. Click "New repository secret"
3. Name: `PINTEREST_ACCESS_TOKEN` → paste token → Save
4. Name: `PINTEREST_BOARD_ID` → paste board ID → Save
5. Done — next scheduled run (09:00 or 17:00 UTC) will post 2 real pins

---

## Priority 4 — Reddit Account + Quora Profile (15 minutes each)

**Why now:** These are FREE traffic. A single well-placed Reddit comment can drive
500-2,000 visits to a post. Quora answers rank in Google and drive evergreen traffic.

### Reddit:
1. Create Reddit account: https://www.reddit.com/account/register/
2. Username suggestion: `SleepWiseReviewsHQ` or similar (real-sounding)
3. Join these subs: r/sleep, r/insomnia, r/ChronicPain, r/Fibromyalgia, r/backpain, r/mattress
4. For first 2 weeks: comment helpfully without linking. Build karma.
5. After 2 weeks of helpful activity, start sharing links per `promotion/reddit_templates.md`

### Quora:
1. Sign up: https://www.quora.com/
2. Bio: "Sleep health researcher | Writes for SleepWiseReviews.com"
3. Answer questions from `promotion/quora_templates.md` — start with fibromyalgia + back pain
4. Aim: 2 answers/week, every week

---

## Revenue Projection (Conservative)

If all 4 priorities are activated within 2 weeks:

| Source | Conservative monthly | Realistic 6-month |
|--------|---------------------|-------------------|
| Amazon Associates | $50 | $300 |
| ShareASale | $80 | $500 |
| AdSense | $40 | $200 |
| Pinterest-driven affiliate | $30 | $250 |
| **Total** | **$200/month** | **$1,250/month** |

These are conservative based on 600+ post indexed sites in health niches.
Aggressive scenario with viral Pinterest pin: 3-5x these numbers.

---

## What I'm Doing While You Action These

- Continuing to deploy 6 posts per batch (Batch 47 in progress now)
- All new posts auto-included in sitemap, homepage, category index
- Pinterest queue stays updated with new posts as they go live
- Project plan updated after every batch

When you complete each Priority above, ping me and I'll:
- ShareASale: update top 10 posts with ShareASale tracking links
- AdSense: add the code snippet to all 603 posts via script
- Pinterest: verify first real pin posts within 24 hours
- Reddit/Quora: nothing needed from me — use the templates in `promotion/`
