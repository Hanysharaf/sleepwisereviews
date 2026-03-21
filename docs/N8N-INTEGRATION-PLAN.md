# SleepWise Reviews - n8n Integration Plan

**Decision:** Using n8n instead of Buffer/Tailwind for automation
**Status:** Planning Phase
**Created:** March 21, 2026

---

## Why n8n?

✅ **Free & Open Source** - No monthly fees
✅ **Self-Hosted** - Full control over data
✅ **Flexible** - Can automate Pinterest, Instagram, Telegram, and more
✅ **Custom Workflows** - Exactly what we need, nothing more
✅ **Better than Buffer** - More features, no $6/month cost

---

## n8n Deployment Options

### Option 1: Cloud Hosting (Recommended for Quick Start)
- **Railway.app** - Already using for Telegram bot
- **Cost:** Free tier (enough for this project)
- **Setup Time:** 10-15 minutes
- **Pros:** Easy setup, always online, automatic updates
- **Cons:** Requires Railway account

### Option 2: Local + Cloudflare Tunnel
- **Run locally** on your PC with Cloudflare tunnel for webhooks
- **Cost:** Free
- **Pros:** Complete control, unlimited executions
- **Cons:** PC must be running, more technical setup

### Option 3: Docker on VPS
- **DigitalOcean/Linode** - $5/month
- **Pros:** Professional, reliable, 24/7 uptime
- **Cons:** Monthly cost

**Recommendation:** Start with Railway (free tier), move to VPS if needed

---

## Workflows to Build

### Workflow 1: Daily Pinterest Posting
**Trigger:** Schedule (3 times daily: 8 AM, 2 PM, 6 PM UTC)
**Actions:**
1. Read next pin from `automation/data/pinterest_queue.json`
2. Post to Pinterest via Pinterest API
3. Mark as posted in `automation/data/pinterest_posted.json`
4. Send success notification to Telegram
5. Update stats in `automation/data/state.json`

**Required Credentials:**
- Pinterest Access Token
- Telegram Bot Token

---

### Workflow 2: Daily Instagram Reminder
**Trigger:** Schedule (12 PM UTC daily)
**Actions:**
1. Check if Instagram content exists for today
2. Send Telegram message with:
   - Image preview
   - Caption text
   - Hashtags
   - Link to content folder

**Required Credentials:**
- Telegram Bot Token

---

### Workflow 3: Daily Summary Report
**Trigger:** Schedule (8 PM UTC daily)
**Actions:**
1. Fetch Pinterest analytics (views, saves, clicks)
2. Read today's stats from state.json
3. Format summary message with:
   - Pins posted today
   - Total impressions
   - Website link
   - Top performing pin
4. Send to Telegram

**Required Credentials:**
- Pinterest API
- Telegram Bot Token

---

### Workflow 4: Content Queue Monitor
**Trigger:** Schedule (Weekly, Monday 9 AM)
**Actions:**
1. Check pinterest_queue.json length
2. If < 5 pins remaining:
   - Send alert to Telegram
   - Suggest: "Time to create more pins!"
3. Generate weekly analytics report

---

### Workflow 5: Website Uptime Monitor
**Trigger:** Schedule (Every 6 hours)
**Actions:**
1. Check if https://hanysharaf.github.io/sleepwisereviews/ is online
2. Verify sitemap.xml is accessible
3. Check key article pages
4. Alert if any issues found

---

## Pinterest API Setup for n8n

### Step 1: Create Pinterest App
1. Go to https://developers.pinterest.com/apps/
2. Create new app:
   - **App name:** SleepWise Reviews Automation
   - **Description:** Automated posting for sleep product reviews
   - **Website:** https://hanysharaf.github.io/sleepwisereviews/
3. Request API access
4. Get credentials:
   - App ID
   - App Secret

### Step 2: Get Access Token
Pinterest requires OAuth 2.0 flow. n8n has built-in Pinterest OAuth support:

1. In n8n: Add Credentials → Pinterest OAuth2
2. Copy redirect URI from n8n
3. Add redirect URI in Pinterest app settings
4. Complete OAuth flow in n8n
5. Token stored automatically

### Step 3: Board Selection
- Board ID: `1104437646027276054` (already have this)
- Board Name: Your main SleepWise board

---

## n8n Installation Steps

### Quick Start (Railway - Recommended)

1. **Fork n8n Template:**
   ```
   https://railway.app/template/n8n
   ```

2. **Deploy to Railway:**
   - Click "Deploy Now"
   - Set environment variables:
     - `N8N_BASIC_AUTH_ACTIVE=true`
     - `N8N_BASIC_AUTH_USER=admin`
     - `N8N_BASIC_AUTH_PASSWORD=your_secure_password`
   - Wait for deployment (2-3 minutes)

3. **Access n8n:**
   - Railway will give you a URL: `https://your-app.up.railway.app`
   - Login with credentials you set

4. **Configure Credentials:**
   - Pinterest OAuth2
   - Telegram Bot Token (already have)
   - HTTP Request node for GitHub API

---

## Integration with Existing System

### Current System:
- `automation/auto_scheduler.py` - Python automation
- GitHub Actions - Runs every 2 hours
- Telegram bot - Sends notifications

### New System with n8n:
- **n8n** - Handles Pinterest posting + scheduling
- **Keep GitHub Actions** - Website updates, monitoring
- **Keep Python** - Content generation (create_pins.py, etc.)
- **Telegram** - All notifications route through n8n

### Migration Plan:
1. ✅ Set up n8n on Railway
2. ✅ Create Workflow 1 (Pinterest posting)
3. ✅ Test with 1-2 pins
4. ✅ Create other workflows
5. ✅ Disable simulation mode in Python
6. ✅ Full automation live

---

## Data Flow Architecture

```
[Pinterest Queue JSON]
        ↓
   [n8n Workflow]
        ↓
  [Pinterest API] → Post Pin
        ↓
 [Update JSON files]
        ↓
  [Telegram Alert] → "Posted: [pin title]"
```

---

## Files to Update

### 1. automation/config.py
Add n8n webhook URLs:
```python
N8N_WEBHOOK_BASE = "https://your-n8n.railway.app/webhook"
N8N_POST_PIN_WEBHOOK = f"{N8N_WEBHOOK_BASE}/post-pinterest"
```

### 2. docs/ROADMAP.md
Update Phase 3 to reflect n8n decision

### 3. automation/modules/n8n_integration.py (NEW)
Helper functions to trigger n8n workflows

### 4. .env.example
Add:
```
N8N_WEBHOOK_URL=https://your-n8n.railway.app/webhook/post-pinterest
N8N_API_KEY=your_n8n_api_key
```

---

## Timeline

### Week 1: Setup & Testing
- Day 1: Deploy n8n to Railway
- Day 2: Set up Pinterest OAuth
- Day 3: Build Workflow 1 (Pinterest posting)
- Day 4: Test with 2-3 pins
- Day 5: Build Workflow 2-3

### Week 2: Full Automation
- Day 1: Build remaining workflows
- Day 2: Connect all data sources
- Day 3: Full testing cycle
- Day 4: Go live with automation
- Day 5: Monitor and adjust

---

## Success Metrics

After n8n is live, we should see:
- ✅ 3 Pinterest pins posted daily (automatic)
- ✅ Zero manual work required
- ✅ Daily Telegram reports with stats
- ✅ Content queue management alerts
- ✅ 100% uptime monitoring

---

## Cost Comparison

| Service | Monthly Cost | Notes |
|---------|-------------|-------|
| Buffer | $6 | Limited features |
| Tailwind | $15 | Pinterest only |
| **n8n (Railway)** | **$0** | **Free tier sufficient** |
| n8n (VPS) | $5 | If we outgrow free tier |

**Savings:** $6-15/month = $72-180/year

---

## Next Steps

**Ready to start?**

1. Create Railway account (if needed)
2. Deploy n8n from template
3. Set up Pinterest OAuth credentials
4. Build first workflow together
5. Test with your Pinterest queue

**Estimated Time:** 1-2 hours for complete setup

---

## Resources

- **n8n Documentation:** https://docs.n8n.io/
- **n8n Pinterest Node:** https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.pinterest/
- **Railway n8n Template:** https://railway.app/template/n8n
- **Pinterest API Docs:** https://developers.pinterest.com/docs/

---

*SleepWise Reviews - n8n Integration Plan | March 2026*
