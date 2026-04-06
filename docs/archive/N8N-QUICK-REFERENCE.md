# n8n Quick Reference Card - SleepWise Reviews

## 🔑 Credentials Needed

| Credential | Type | Where to Get | Name in n8n |
|------------|------|--------------|-------------|
| Pinterest | OAuth2 | developers.pinterest.com | `Pinterest - SleepWise` |
| Telegram | API Token | @BotFather | `Telegram - SleepWise Bot` |
| GitHub | PAT | github.com/settings/tokens | `GitHub API - SleepWise` |

---

## 📊 Workflows Overview

### 1. Pinterest Auto-Poster ⭐ MAIN WORKFLOW
- **Schedule:** 8 AM, 2 PM, 6 PM UTC (3x daily)
- **Purpose:** Auto-post pins from queue
- **Nodes:** 10 nodes
- **Status:** Must be ACTIVE ✅

**Flow:**
```
Cron → Fetch Queue → Get Pin → Post Pinterest → Update Queue → Commit GitHub → Telegram
```

---

### 2. Daily Analytics Report
- **Schedule:** 8 PM UTC daily
- **Purpose:** Send daily stats report
- **Nodes:** 5 nodes

---

### 3. Instagram Reminder
- **Schedule:** 12 PM UTC daily
- **Purpose:** Remind to post IG content
- **Nodes:** 3 nodes

---

### 4. Content Queue Monitor
- **Schedule:** Monday 9 AM UTC weekly
- **Purpose:** Alert if queue low
- **Nodes:** 4 nodes

---

## 🎯 Critical Settings

### Pinterest Node Settings
```
Board ID: 1104437646027276054
Title: ={{ $json.title }}
Description: ={{ $json.description }}
Link: ={{ $json.link }}
Image URL: ={{ $json.image_url }}
```

### GitHub API URLs
```
Get File:
GET https://api.github.com/repos/Hanysharaf/sleepwisereviews/contents/automation/data/pinterest_queue.json

Update File:
PUT https://api.github.com/repos/Hanysharaf/sleepwisereviews/contents/automation/data/pinterest_queue.json

Raw File (Read):
GET https://raw.githubusercontent.com/Hanysharaf/sleepwisereviews/main/automation/data/pinterest_queue.json
```

### Telegram Chat ID
```
Your Chat ID: [Enter your numeric Telegram Chat ID]
```

---

## ⏰ Schedule Cheat Sheet

| Time (UTC) | Workflow | Action |
|------------|----------|--------|
| 8:00 AM | Pinterest Auto-Poster | Post pin #1 |
| 9:00 AM | Queue Monitor (Mon only) | Check queue |
| 12:00 PM | Instagram Reminder | Send IG tip |
| 2:00 PM | Pinterest Auto-Poster | Post pin #2 |
| 6:00 PM | Pinterest Auto-Poster | Post pin #3 |
| 8:00 PM | Daily Report | Send stats |

**Total:** 3 pins/day = 21 pins/week = ~90 pins/month

---

## 🔧 Common Code Snippets

### Get First Pin from Queue
```javascript
const queue = $input.first().json;
if (!Array.isArray(queue) || queue.length === 0) {
  throw new Error('Queue is empty!');
}
const pin = queue[0];
return { json: { ...pin, fullQueue: queue } };
```

### Update Queue (Remove First)
```javascript
const fullQueue = $('Get First Pin').first().json.fullQueue;
const updatedQueue = fullQueue.slice(1);
return {
  json: {
    updatedQueue: updatedQueue,
    queueLength: updatedQueue.length
  }
};
```

### Format Telegram Message
```javascript
let msg = `📌 Pinterest Pin Posted!\n\n`;
msg += `✅ ${$('Get First Pin').first().json.title}\n\n`;
msg += `🔗 ${$('Create Pinterest Pin').first().json.url}\n\n`;
msg += `📊 Queue: ${$('Update Queue').first().json.queueLength} remaining`;
return { json: { message: msg } };
```

### Calculate Daily Stats
```javascript
const posted = $input.first().json;
const today = new Date().toISOString().split('T')[0];
const todayPosts = posted.filter(p =>
  p.posted_at && p.posted_at.startsWith(today)
);
return {
  json: {
    count: todayPosts.length,
    posts: todayPosts
  }
};
```

---

## 🚨 Troubleshooting Quick Fixes

### Pinterest Post Fails
```
1. Check credential connected (green ✅)
2. Verify Board ID: 1104437646027276054
3. Test image URL in browser
4. Check Pinterest rate limits
```

### GitHub Commit Fails
```
1. Verify PAT has 'repo' scope
2. Check file SHA is current
3. Test credential with simple GET first
4. Ensure JSON is valid
```

### Workflow Not Triggering
```
1. Check "Active" toggle is ON
2. Verify cron expression correct
3. Check n8n Cloud status
4. Review execution history
```

### Queue Empty Error
```
1. Check queue file on GitHub
2. Manually add pins to queue
3. Verify file path correct
4. Check JSON format valid
```

---

## 📈 Monitoring Checklist

### Daily (5 min)
- [ ] Check Telegram for all notifications
- [ ] Verify 3 pins posted
- [ ] Review daily report stats
- [ ] Check queue count

### Weekly (10 min)
- [ ] Review queue monitor alert
- [ ] Check Pinterest analytics
- [ ] Refill queue if < 5 pins
- [ ] Review execution history

### Monthly (30 min)
- [ ] Pinterest performance review
- [ ] Generate new pin content
- [ ] Optimize posting times
- [ ] Update content strategy

---

## 🎯 Expected Daily Activity

**Morning (8 AM UTC):**
```
✅ Pin posted to Pinterest
📱 Telegram: "Pinterest Pin Posted!"
```

**Midday (12 PM UTC):**
```
📱 Telegram: "Instagram Reminder!"
```

**Afternoon (2 PM UTC):**
```
✅ Pin posted to Pinterest
📱 Telegram: "Pinterest Pin Posted!"
```

**Evening (6 PM UTC):**
```
✅ Pin posted to Pinterest
📱 Telegram: "Pinterest Pin Posted!"
```

**Night (8 PM UTC):**
```
📱 Telegram: "Daily Report"
   - 3 pins posted
   - Links to pins
   - Queue status
```

---

## 🔗 Important Links

| Resource | URL |
|----------|-----|
| n8n Cloud | https://app.n8n.cloud |
| Pinterest | https://pinterest.com/sleepwisereviews |
| Pinterest Board ID | 1104437646027276054 |
| GitHub Repo | https://github.com/Hanysharaf/sleepwisereviews |
| Queue File | automation/data/pinterest_queue.json |
| Posted History | automation/data/pinterest_posted.json |
| Website | https://hanysharaf.github.io/sleepwisereviews/ |

---

## 🆘 Emergency Procedures

### Pause All Automation
1. Go to n8n Cloud
2. Toggle each workflow to "Inactive"
3. Automation stops immediately

### Manual Post (if automation fails)
1. Go to Pinterest
2. Create pin manually
3. Use queue file for content
4. Update queue file on GitHub

### Restore Queue
If queue gets corrupted:
```json
[
  {
    "title": "Your Pin Title",
    "description": "Your description",
    "link": "https://hanysharaf.github.io/sleepwisereviews/",
    "image_url": "https://images.unsplash.com/photo-xxx?w=800",
    "category": "tips"
  }
]
```

---

## 💡 Pro Tips

1. **Keep Queue Stocked:** Always maintain 10+ pins
2. **Monitor Executions:** Check n8n execution history weekly
3. **Backup Queue:** Keep copy of queue locally
4. **Test Changes:** Use "Execute Workflow" before activating
5. **Time Zones:** All times in UTC - convert to your local time
6. **Rate Limits:** Pinterest allows 150 req/hour (we use ~3/day)
7. **Image URLs:** Use Unsplash - reliable, free, high-quality

---

## 📱 Telegram Commands

Your Railway Telegram bot still works for manual tasks:
- `/status` - Check automation status
- `/article [topic]` - Generate article
- `/caption [text]` - Create IG caption

---

**Quick Start:**
1. Set up 3 credentials in n8n
2. Build Pinterest Auto-Poster workflow
3. Test with "Execute Workflow"
4. Activate workflow
5. Monitor first 24 hours

**That's it! You're automated!** 🎉

---

*SleepWise Reviews - n8n Quick Reference | March 2026*
