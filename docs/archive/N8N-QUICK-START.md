# n8n Quick Start Guide for SleepWise Reviews

**Goal:** Get n8n running and posting to Pinterest in under 30 minutes

---

## Step 1: Deploy n8n to Railway (10 min)

### 1.1 Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub (free account)
3. Verify your email

### 1.2 Deploy n8n
1. Visit: https://railway.app/template/n8n
2. Click **"Deploy Now"**
3. Configure environment variables:
   ```
   N8N_BASIC_AUTH_ACTIVE=true
   N8N_BASIC_AUTH_USER=admin
   N8N_BASIC_AUTH_PASSWORD=YourSecurePassword123
   N8N_ENCRYPTION_KEY=create_a_random_32_char_string
   ```
4. Click **"Deploy"**
5. Wait 2-3 minutes for deployment

### 1.3 Access Your n8n Instance
1. Click on your new project in Railway
2. Click **"Settings"** → **"Generate Domain"**
3. Copy your URL: `https://your-app.up.railway.app`
4. Open in browser
5. Login with credentials you set above

✅ **You now have n8n running!**

---

## Step 2: Set Up Pinterest OAuth (15 min)

### 2.1 Create Pinterest App
1. Go to https://developers.pinterest.com/apps/
2. Click **"Create app"**
3. Fill in details:
   - **App name:** SleepWise Automation
   - **Description:** Automated posting for sleep product reviews
   - **Website:** https://hanysharaf.github.io/sleepwisereviews/
4. Click **"Create"**
5. Save your **App ID** and **App Secret**

### 2.2 Configure OAuth in n8n
1. In n8n, click **Settings** (gear icon) → **Credentials**
2. Click **"Add Credential"**
3. Search for **"Pinterest OAuth2"**
4. Fill in:
   - **Client ID:** Your App ID from Pinterest
   - **Client Secret:** Your App Secret from Pinterest
   - **Redirect URL:** Copy this from n8n
5. Go back to Pinterest Developer Portal
6. Add the Redirect URL to your app
7. In n8n, click **"Connect my account"**
8. Authorize the app
9. Save credentials

✅ **Pinterest connected to n8n!**

---

## Step 3: Create Your First Workflow (20 min)

### 3.1 Pinterest Posting Workflow

1. In n8n, click **"New Workflow"**
2. Name it: **"Pinterest Auto-Poster"**

### 3.2 Add Webhook Trigger
1. Click **"Add first step"**
2. Search for **"Webhook"**
3. Select **"Webhook" node**
4. Set:
   - **HTTP Method:** POST
   - **Path:** `post-pinterest`
5. Click **"Listen for test event"**
6. Copy the webhook URL

### 3.3 Add Pinterest Node
1. Click **"+"** button
2. Search for **"Pinterest"**
3. Select **"Pinterest" node**
4. Configure:
   - **Credential:** Select your Pinterest OAuth2
   - **Resource:** Pin
   - **Operation:** Create
   - **Board ID:** `1104437646027276054`
   - **Title:** `{{ $json.pin.title }}`
   - **Description:** `{{ $json.pin.description }}`
   - **Link:** `{{ $json.pin.link }}`
   - **Image URL:** `{{ $json.pin.image_url }}`

### 3.4 Add Telegram Notification
1. Click **"+"** after Pinterest node
2. Search for **"Telegram"**
3. Add **"Telegram" node**
4. Configure:
   - **Credential:** Add your Telegram Bot Token
   - **Chat ID:** Your Telegram Chat ID
   - **Text:**
     ```
     ✅ Pinterest Pin Posted!

     📌 {{ $node["Pinterest"].json.title }}
     🔗 {{ $node["Pinterest"].json.url }}
     📊 Posted at: {{ $now }}
     ```

### 3.5 Test the Workflow
1. Click **"Execute Workflow"**
2. In another terminal, test the webhook:

```bash
curl -X POST https://your-app.up.railway.app/webhook/post-pinterest \
  -H "Content-Type: application/json" \
  -d '{
    "pin": {
      "title": "Test Pin - Sleep Better Tonight",
      "description": "Testing automated Pinterest posting with n8n",
      "link": "https://hanysharaf.github.io/sleepwisereviews/",
      "image_url": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=800"
    }
  }'
```

3. Check Pinterest - you should see the pin!
4. Check Telegram - you should get a notification!

### 3.6 Activate the Workflow
1. In n8n, click **"Active"** toggle (top right)
2. Save the workflow

✅ **Your first workflow is live!**

---

## Step 4: Schedule Automatic Posting (10 min)

### 4.1 Create Scheduled Workflow
1. Create **new workflow:** "Pinterest Daily Schedule"
2. Add **"Schedule Trigger"** node:
   - **Trigger Interval:** Cron
   - **Cron Expression:** `0 8,14,18 * * *` (8 AM, 2 PM, 6 PM UTC)

### 4.2 Add Read Queue Node
1. Add **"Code"** node
2. Paste this code:

```javascript
// Read next pin from queue
const queuePath = 'automation/data/pinterest_queue.json';
// In production, you'd read from GitHub or a database
// For now, we'll use the webhook approach

return [
  {
    json: {
      trigger: 'schedule',
      time: new Date().toISOString()
    }
  }
];
```

### 4.3 Connect to Posting Workflow
1. Add **"HTTP Request"** node
2. Configure:
   - **Method:** POST
   - **URL:** Your webhook URL from Step 3
   - **Body:** Read from your queue file

### 4.4 Activate
1. Toggle **"Active"**
2. Save workflow

✅ **Automatic posting is now scheduled!**

---

## Step 5: Update Your .env File

Add to your local `.env`:

```bash
# n8n Configuration
N8N_WEBHOOK_BASE=https://your-app.up.railway.app/webhook
N8N_API_KEY=your_api_key_here
```

---

## Quick Commands to Test

### Test Pinterest Posting
```bash
cd automation
python -c "from modules.n8n_integration import N8NIntegration; n8n = N8NIntegration(); print(n8n.is_configured())"
```

### Trigger a Post via Python
```python
from modules.n8n_integration import N8NIntegration
import json

n8n = N8NIntegration()

# Load a pin from queue
with open('automation/data/pinterest_queue.json', 'r') as f:
    queue = json.load(f)
    pin = queue[0]  # First pin

# Post it
result = n8n.trigger_pinterest_post(pin)
print(json.dumps(result, indent=2))
```

---

## Troubleshooting

### "Webhook not found"
- Make sure workflow is **Active** (toggle on)
- Check the webhook path matches

### "Pinterest authentication failed"
- Re-do OAuth connection in n8n
- Make sure redirect URL is added in Pinterest app

### "Image URL invalid"
- Pinterest requires publicly accessible image URLs
- Use Unsplash or upload to Imgur/Cloudinary first

### Railway sleeping/stopping
- Railway free tier sleeps after inactivity
- Add a keep-alive workflow (ping every 10 min)
- Or upgrade to Hobby plan ($5/month for 24/7)

---

## Next Workflows to Build

1. **Daily Analytics Report** - Pull Pinterest stats, send to Telegram
2. **Instagram Reminder** - Daily content notification
3. **Content Queue Monitor** - Alert when queue is low
4. **Website Uptime Check** - Monitor site health

See `N8N-INTEGRATION-PLAN.md` for detailed workflow specs.

---

## Success Checklist

- [ ] Railway account created
- [ ] n8n deployed and accessible
- [ ] Pinterest OAuth connected
- [ ] Test pin posted successfully
- [ ] Telegram notification received
- [ ] Scheduled workflow active
- [ ] .env file updated

**Time Invested:** ~30-45 minutes
**Monthly Cost:** $0 (Railway free tier)
**Result:** Fully automated Pinterest posting! 🎉

---

*SleepWise Reviews - n8n Quick Start | March 2026*
