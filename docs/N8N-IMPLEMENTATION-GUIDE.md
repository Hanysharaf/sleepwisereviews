# n8n Implementation Guide - SleepWise Reviews
## Complete Step-by-Step Setup for app.n8n.cloud

**Last Updated:** March 21, 2026
**Estimated Time:** 2-3 hours total
**Cost:** $0/month (n8n Cloud free tier)

---

## 📋 Pre-Implementation Checklist

Before starting, ensure you have:
- [ ] n8n Cloud account (app.n8n.cloud)
- [ ] Pinterest account (@sleepwisereviews)
- [ ] Telegram Bot Token
- [ ] Telegram Chat ID
- [ ] GitHub Personal Access Token
- [ ] Queue file with 8 pins ready

---

## PHASE 1: n8n Cloud Setup & Credentials (30 min)

### Step 1.1: Access Your n8n Instance

1. Go to https://app.n8n.cloud
2. Sign in to your account
3. You should see your n8n dashboard

### Step 1.2: Configure Pinterest OAuth2 Credential

**CRITICAL: Pinterest requires OAuth2, not a simple API key**

1. **Create Pinterest App** (if not done):
   - Go to https://developers.pinterest.com/apps/
   - Click "Create app"
   - Fill in:
     - App name: `SleepWise Automation`
     - Description: `Automated posting for sleep product reviews`
     - Website: `https://hanysharaf.github.io/sleepwisereviews/`
   - Submit (may need approval - usually instant)

2. **In n8n Cloud:**
   - Click **"Credentials"** (left sidebar)
   - Click **"Add Credential"**
   - Search for **"Pinterest OAuth2 API"**
   - Select it

3. **Get Redirect URL from n8n:**
   - n8n will show: `OAuth Redirect URL`
   - Copy this URL (looks like: `https://app.n8n.cloud/rest/oauth2-credential/callback`)

4. **Add Redirect URL to Pinterest App:**
   - Go back to Pinterest Developer Portal
   - Open your app
   - Find **"Redirect URIs"** section
   - Paste the n8n URL
   - Save

5. **Complete OAuth in n8n:**
   - Back in n8n, enter:
     - **Client ID:** Your Pinterest App ID
     - **Client Secret:** Your Pinterest App Secret
   - Click **"Connect my account"**
   - Authorize Pinterest
   - Click **"Save"**
   - Name it: `Pinterest - SleepWise`

**Test it:**
- Click the credential
- Look for green checkmark ✅
- Should say "Connected"

---

### Step 1.3: Configure Telegram Credential

1. In n8n, click **"Credentials"** → **"Add Credential"**
2. Search for **"Telegram API"**
3. Enter:
   - **Access Token:** Your Telegram Bot Token
4. Click **"Save"**
5. Name it: `Telegram - SleepWise Bot`

---

### Step 1.4: Configure GitHub Credential

**You need a GitHub Personal Access Token (PAT)**

1. **Create GitHub PAT** (if you don't have one):
   - Go to: https://github.com/settings/tokens
   - Click **"Generate new token (classic)"**
   - Name: `n8n SleepWise Automation`
   - Select scopes:
     - ✅ `repo` (Full control)
     - ✅ `workflow` (if you'll trigger Actions)
   - Generate token
   - **COPY IT NOW** (you won't see it again!)

2. **In n8n:**
   - Credentials → Add → **"HTTP Header Auth"**
   - Header Name: `Authorization`
   - Header Value: `Bearer YOUR_GITHUB_PAT_HERE`
   - Save as: `GitHub API - SleepWise`

---

## PHASE 2: Build Pinterest Auto-Poster Workflow (45 min)

### Workflow Overview
```
Schedule (8 AM, 2 PM, 6 PM UTC)
  ↓
Fetch Queue from GitHub
  ↓
Extract First Pin
  ↓
Post to Pinterest
  ↓
Update Queue (remove posted pin)
  ↓
Commit to GitHub
  ↓
Send Telegram Notification
```

### Step 2.1: Create New Workflow

1. Click **"Workflows"** → **"Add Workflow"**
2. Name it: **"Pinterest Auto-Poster"**
3. Click the canvas to start adding nodes

---

### Step 2.2: Add Schedule Trigger

1. Click **"Add first node"** or the **"+"** button
2. Search for **"Schedule Trigger"**
3. Configure:
   - **Trigger Interval:** Cron
   - **Cron Expression:** `0 8,14,18 * * *`
   - This means: 8 AM, 2 PM (14:00), 6 PM (18:00) UTC daily

4. Click outside to save

**Test:** Click **"Execute Node"** - should show execution time

---

### Step 2.3: Fetch Pinterest Queue from GitHub

1. Click **"+"** after Schedule node
2. Search for **"HTTP Request"**
3. Configure:
   - **Method:** GET
   - **URL:**
     ```
     https://raw.githubusercontent.com/Hanysharaf/sleepwisereviews/main/automation/data/pinterest_queue.json
     ```
   - **Authentication:** None (public file)
   - **Response Format:** JSON

4. Name this node: `Fetch Queue`

**Test:** Click **"Execute Node"** - should show array of 8 pins

---

### Step 2.4: Extract First Pin (Function Node)

1. Click **"+"** after Fetch Queue
2. Search for **"Code"**
3. Select **"Code" node**
4. Paste this code:

```javascript
// Get the queue array
const queue = $input.first().json;

// Check if queue is empty
if (!Array.isArray(queue) || queue.length === 0) {
  throw new Error('Pinterest queue is empty! Add more pins.');
}

// Get the first pin
const pin = queue[0];

// Return it
return {
  json: {
    title: pin.title,
    description: pin.description,
    link: pin.link,
    image_url: pin.image_url,
    category: pin.category || 'general',
    // Also keep full queue for later update
    fullQueue: queue
  }
};
```

5. Name this node: `Get First Pin`

**Test:** Execute - should show one pin object

---

### Step 2.5: Post to Pinterest

1. Click **"+"** after Get First Pin
2. Search for **"Pinterest"**
3. Select **"Pinterest" node**
4. Configure:
   - **Credential:** Select `Pinterest - SleepWise`
   - **Resource:** Pin
   - **Operation:** Create
   - **Board ID:** `1104437646027276054`
   - **Title:** `={{ $json.title }}`
   - **Description:** `={{ $json.description }}`
   - **Link:** `={{ $json.link }}`
   - **Media Source:** Image URL
   - **Image URL:** `={{ $json.image_url }}`

5. Name this node: `Create Pinterest Pin`

**Test:** Execute - should post to Pinterest!
**Check Pinterest:** https://www.pinterest.com/sleepwisereviews/

---

### Step 2.6: Update Queue (Remove Posted Pin)

After posting successfully, we need to remove the pin from queue.

1. Click **"+"** after Pinterest node
2. Add **"Code" node**
3. Paste this code:

```javascript
// Get the full queue from earlier node
const fullQueue = $('Get First Pin').first().json.fullQueue;

// Remove the first pin (the one we just posted)
const updatedQueue = fullQueue.slice(1);

// Pinterest response
const pinterestResponse = $input.first().json;

return {
  json: {
    updatedQueue: updatedQueue,
    queueLength: updatedQueue.length,
    postedPin: {
      title: $('Get First Pin').first().json.title,
      url: pinterestResponse.url || pinterestResponse.id,
      posted_at: new Date().toISOString()
    }
  }
};
```

4. Name: `Update Queue`

---

### Step 2.7: Commit Queue to GitHub

This is the tricky part - we need to update the file on GitHub.

**Method 1: Using GitHub API (Recommended)**

1. Click **"+"** after Update Queue
2. Add **"HTTP Request" node**
3. Configure:

**First, get current file SHA:**
```
Method: GET
URL: https://api.github.com/repos/Hanysharaf/sleepwisereviews/contents/automation/data/pinterest_queue.json
Authentication: Use Credential "GitHub API - SleepWise"
```

4. Add another **"Code" node** after that:

```javascript
// Get current file SHA
const currentFile = $input.first().json;
const sha = currentFile.sha;

// Get updated queue
const updatedQueue = $('Update Queue').first().json.updatedQueue;

// Base64 encode the new content
const content = Buffer.from(JSON.stringify(updatedQueue, null, 2)).toString('base64');

return {
  json: {
    sha: sha,
    content: content,
    message: `🤖 n8n: Posted pin - ${$('Update Queue').first().json.queueLength} remaining`
  }
};
```

5. Add **"HTTP Request" node**:
```
Method: PUT
URL: https://api.github.com/repos/Hanysharaf/sleepwisereviews/contents/automation/data/pinterest_queue.json
Authentication: GitHub API credential
Body:
{
  "message": "={{ $json.message }}",
  "content": "={{ $json.content }}",
  "sha": "={{ $json.sha }}"
}
```

**This commits the updated queue back to GitHub!**

---

### Step 2.8: Send Telegram Notification

1. Click **"+"** at the end
2. Add **"Telegram" node**
3. Configure:
   - **Credential:** `Telegram - SleepWise Bot`
   - **Resource:** Message
   - **Operation:** Send Message
   - **Chat ID:** Your Telegram Chat ID (enter manually)
   - **Text:** Use this template:

```
📌 Pinterest Pin Posted!

✅ Title: {{ $('Get First Pin').first().json.title }}

🔗 URL: {{ $('Create Pinterest Pin').first().json.url }}

📊 Queue: {{ $('Update Queue').first().json.queueLength }} pins remaining

⏰ Posted at: {{ $now }}

View on Pinterest: {{ $('Create Pinterest Pin').first().json.url }}
```

4. Click **"Execute Workflow"** to test full workflow!

---

### Step 2.9: Add Error Handling

1. On the **Pinterest node**, click the three dots → **"Add Error Workflow"**
2. Add **"Error Trigger" node**
3. Connect to **"Telegram" node** with error message:

```
❌ Pinterest Post Failed!

Error: {{ $json.error.message }}

Node: {{ $json.error.node.name }}

I'll retry at next schedule.
```

---

### Step 2.10: Activate Workflow

1. Toggle **"Active"** switch (top right) to ON
2. Save the workflow
3. Your Pinterest auto-posting is now LIVE! 🎉

**Schedule:**
- 8:00 AM UTC
- 2:00 PM UTC
- 6:00 PM UTC

**What happens:**
- n8n fetches queue
- Posts pin to Pinterest
- Updates queue file on GitHub
- Sends you notification with URL
- All automatic!

---

## PHASE 3: Build Daily Analytics Report (30 min)

### Workflow Overview
```
Schedule (8 PM UTC daily)
  ↓
Fetch Posted Pins History
  ↓
Fetch State File
  ↓
Calculate Stats
  ↓
Format Report
  ↓
Send to Telegram
```

### Step 3.1: Create Workflow

1. New Workflow: **"Daily Analytics Report"**
2. Add **"Schedule Trigger"**
   - Cron: `0 20 * * *` (8 PM UTC daily)

### Step 3.2: Fetch Posted Pins

1. Add **"HTTP Request"**:
```
Method: GET
URL: https://raw.githubusercontent.com/Hanysharaf/sleepwisereviews/main/automation/data/pinterest_posted.json
```

### Step 3.3: Calculate Today's Stats

1. Add **"Code" node**:

```javascript
const posted = $input.first().json;
const today = new Date().toISOString().split('T')[0];

// Filter today's posts
const todayPosts = posted.filter(p =>
  p.posted_at && p.posted_at.startsWith(today)
);

// Get this week
const weekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString();
const weekPosts = posted.filter(p =>
  p.posted_at && p.posted_at >= weekAgo
);

return {
  json: {
    today_count: todayPosts.length,
    week_count: weekPosts.length,
    today_posts: todayPosts,
    total_all_time: posted.length
  }
};
```

### Step 3.4: Format Report

1. Add **"Code" node**:

```javascript
const stats = $input.first().json;

let report = `🌙 SleepWise Daily Report\n`;
report += `━━━━━━━━━━━━━━━━━━━━━━━\n\n`;
report += `📌 Pinterest Today: ${stats.today_count} pins\n\n`;

// List today's posts with URLs
if (stats.today_posts.length > 0) {
  report += `Posted:\n`;
  stats.today_posts.forEach(pin => {
    report += `  • ${pin.title}\n`;
    report += `    ${pin.pin_url}\n\n`;
  });
}

report += `📊 This Week: ${stats.week_count} pins\n`;
report += `📈 All Time: ${stats.total_all_time} pins\n\n`;
report += `🔗 Website: https://hanysharaf.github.io/sleepwisereviews/\n`;
report += `📱 Pinterest: https://www.pinterest.com/sleepwisereviews/\n`;

return {
  json: {
    report: report
  }
};
```

### Step 3.5: Send to Telegram

1. Add **"Telegram" node**:
   - Text: `={{ $json.report }}`
   - Parse Mode: `Markdown`

2. **Activate workflow** ✅

---

## PHASE 4: Build Instagram Reminder (15 min)

### Quick Setup

1. New Workflow: **"Instagram Content Reminder"**
2. Schedule Trigger: `0 12 * * *` (12 PM UTC)
3. Code node:

```javascript
const tips = [
  "Keep bedroom at 65-68°F for optimal sleep",
  "No screens 2 hours before bed",
  "Magnesium glycinate 400mg helps sleep",
  "Weighted blankets reduce anxiety",
  "White noise masks disruptive sounds"
];

const randomTip = tips[Math.floor(Math.random() * tips.length)];

return {
  json: {
    message: `📸 Instagram Reminder!\n\nToday's tip: ${randomTip}\n\nPost to @sleepwise.reviews now!`
  }
};
```

4. Telegram node with `{{ $json.message }}`
5. Activate ✅

---

## PHASE 5: Build Queue Monitor (15 min)

### Setup

1. New Workflow: **"Content Queue Monitor"**
2. Schedule: `0 9 * * 1` (Monday 9 AM)
3. HTTP Request: Fetch `pinterest_queue.json`
4. Code node:

```javascript
const queue = $input.first().json;
const queueLength = queue.length;

let alert = `📦 Queue Status Report\n\n`;
alert += `Pinterest Queue: ${queueLength} pins\n\n`;

if (queueLength < 5) {
  alert += `⚠️ WARNING: Queue running low!\n`;
  alert += `Action needed: Generate more pins\n`;
} else {
  alert += `✅ Queue healthy\n`;
}

return { json: { alert } };
```

5. Telegram node
6. Activate ✅

---

## PHASE 6: Testing & Validation (30 min)

### Test Checklist

1. **Pinterest Auto-Poster:**
   - [ ] Click "Execute Workflow"
   - [ ] Check Pinterest for new pin
   - [ ] Verify queue file updated on GitHub
   - [ ] Confirm Telegram notification received
   - [ ] Check queue count decreased by 1

2. **Daily Report:**
   - [ ] Execute manually
   - [ ] Verify stats are accurate
   - [ ] Check formatting in Telegram

3. **Instagram Reminder:**
   - [ ] Execute manually
   - [ ] Check message format

4. **Queue Monitor:**
   - [ ] Execute manually
   - [ ] Verify queue count shown

---

## PHASE 7: Migration from Old System (15 min)

### Disable GitHub Actions

1. Open `.github/workflows/automation.yml`
2. Add at top:
```yaml
# DEPRECATED: Automation migrated to n8n
# Last run: March 21, 2026
# See: docs/N8N-IMPLEMENTATION-GUIDE.md
```

3. Comment out the schedule:
```yaml
on:
  # schedule:
  #   - cron: '0 */2 * * *'  # Every 2 hours
  workflow_dispatch:  # Keep manual trigger for emergencies
```

4. Commit: `Migrate automation to n8n - disable scheduled runs`

---

## PHASE 8: Go Live! (Monitor First 24h)

### Launch Checklist

- [ ] All 4 workflows active in n8n
- [ ] GitHub Actions disabled
- [ ] Telegram notifications working
- [ ] Pinterest OAuth connected
- [ ] Test pin posted successfully

### Monitoring (First 24 Hours)

**Check at these times (UTC):**
- 8:00 AM - Should post pin
- 12:00 PM - Should send IG reminder
- 2:00 PM - Should post pin
- 6:00 PM - Should post pin
- 8:00 PM - Should send daily report

**Expected Results:**
- 3 Pinterest pins posted
- 1 IG reminder
- 1 daily report
- Queue reduced by 3 pins
- All Telegram notifications received

---

## Troubleshooting

### Pinterest Post Fails

**Error:** "Invalid board_id"
- Check Board ID: `1104437646027276054`
- Verify Pinterest credential connected

**Error:** "Rate limit exceeded"
- Pinterest allows 150 req/hour
- Add delay between posts (already done with schedule)

**Error:** "Invalid image URL"
- Check Unsplash URLs are accessible
- Try opening image_url in browser

### GitHub Commit Fails

**Error:** "422 Validation Failed"
- File SHA mismatch
- Solution: Always GET latest SHA before PUT

**Error:** "401 Unauthorized"
- GitHub PAT expired or wrong
- Regenerate PAT with `repo` scope

### Telegram Not Sending

**Error:** "Chat not found"
- Verify Chat ID is correct
- Must be numeric (no @ symbol)
- Start conversation with bot first

---

## Success Metrics

After 7 days, you should see:
- ✅ 21 Pinterest pins posted (3/day × 7)
- ✅ 7 daily reports sent
- ✅ 7 IG reminders sent
- ✅ 1 weekly queue monitor sent
- ✅ Queue reduced from 8 to 0 (need to refill!)

---

## Next Steps

1. **Week 1:** Monitor automation, fix any issues
2. **Week 2:** Generate more Pinterest pin content to refill queue
3. **Week 3:** Add advanced workflows (analytics, A/B testing)
4. **Week 4:** Optimize posting times based on Pinterest analytics

---

## Need Help?

1. Check n8n execution logs (Executions tab)
2. Review error messages in Telegram
3. Test individual nodes in isolation
4. Check GitHub commit history

---

**CONGRATULATIONS! 🎉**

You now have a fully automated, production-ready social media posting system powered by n8n!

**Monthly cost:** $0
**Time saved:** 15 min/day = 7.5 hours/month
**Annual savings vs Buffer:** $72/year

---

*SleepWise Reviews - n8n Implementation Guide | March 2026*
