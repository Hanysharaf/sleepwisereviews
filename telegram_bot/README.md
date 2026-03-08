# SleepWise Telegram Command Bot

A lightweight Telegram bot that receives commands and triggers GitHub Actions workflows.

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Show welcome message and available commands |
| `/help` | Show help message |
| `/article [topic]` | Generate a new article (optional topic) |
| `/summary` | Get daily summary now |
| `/status` | Check automation status |
| `/instagram [topic]` | Prepare Instagram content |
| `/test` | Test all API connections |

## Setup

### 1. Create GitHub Personal Access Token

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name like "SleepWise Bot"
4. Select scopes:
   - `repo` (Full control of private repositories)
   - `workflow` (Update GitHub Action workflows)
5. Copy the token (you won't see it again)

### 2. Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select the `telegram_bot` folder or connect the main repo
4. Add environment variables:
   - `TELEGRAM_BOT_TOKEN`: Your bot token from BotFather
   - `TELEGRAM_CHAT_ID`: Your chat ID
   - `GITHUB_TOKEN`: The personal access token from step 1
   - `GITHUB_REPO`: `Hanysharaf/sleepwisereviews`
5. Deploy!

### 3. Alternative: Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create sleepwise-command-bot

# Set environment variables
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set TELEGRAM_CHAT_ID=your_chat_id
heroku config:set GITHUB_TOKEN=your_github_token
heroku config:set GITHUB_REPO=Hanysharaf/sleepwisereviews

# Deploy
git push heroku main
```

## Local Testing

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export TELEGRAM_BOT_TOKEN=your_token
export TELEGRAM_CHAT_ID=your_chat_id
export GITHUB_TOKEN=your_github_token
export GITHUB_REPO=Hanysharaf/sleepwisereviews

# Run
python bot.py
```

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Telegram      │────▶│  Command Bot    │────▶│  GitHub Actions │
│   (You send     │     │  (Railway)      │     │  (Runs tasks)   │
│    commands)    │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
                                                ┌─────────────────┐
                                                │  Automation     │
                                                │  Agent          │
                                                │  (Sends results │
                                                │   to Telegram)  │
                                                └─────────────────┘
```

## Security

- The bot only responds to the authorized `TELEGRAM_CHAT_ID`
- All other users receive "Unauthorized" message
- GitHub token is stored securely in environment variables
