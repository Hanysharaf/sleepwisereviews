"""
SleepWise Automation Agent - Configuration
Environment variables and settings for the automation system.
"""

import os
from pathlib import Path
from datetime import datetime, timezone

# =============================================================================
# Base Paths
# =============================================================================
BASE_DIR = Path(__file__).parent
PROJECT_ROOT = BASE_DIR.parent
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "templates"

# Website paths
POSTS_DIR = PROJECT_ROOT / "posts"
PAGES_DIR = PROJECT_ROOT / "pages"
PRODUCTS_DIR = PROJECT_ROOT / "products"

# =============================================================================
# API Keys (from environment variables)
# =============================================================================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
PINTEREST_ACCESS_TOKEN = os.getenv("PINTEREST_ACCESS_TOKEN", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# =============================================================================
# Pinterest Configuration
# =============================================================================
PINTEREST_CONFIG = {
    "api_base_url": "https://api.pinterest.com/v5",
    "pins_per_day": 4,
    "boards": {
        "sleep_tips": "",  # Fill with actual board ID
        "product_reviews": "",  # Fill with actual board ID
        "sleep_science": "",  # Fill with actual board ID
    },
    "default_hashtags": [
        "sleeptips", "bettersleep", "sleephealth", "sleepwell",
        "healthysleep", "sleepbetter", "sleepscience", "restfulsleep"
    ]
}

# =============================================================================
# Instagram Configuration (Semi-automated)
# =============================================================================
INSTAGRAM_CONFIG = {
    "posts_per_day": 1,
    "best_posting_times": ["09:00", "12:00", "17:00", "20:00"],
    "default_hashtags": [
        "sleep", "sleeptips", "bettersleep", "sleephealth",
        "wellness", "selfcare", "healthylifestyle", "restfulsleep",
        "sleepwell", "goodnight", "sleepy", "naptime",
        "relaxation", "mindfulness", "healthyliving"
    ],
    "max_hashtags": 30
}

# =============================================================================
# Content Generation (Claude API)
# =============================================================================
CONTENT_CONFIG = {
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 4096,
    "article_length": 1500,  # words
    "topics": [
        "weighted blankets",
        "sleep pillows",
        "white noise machines",
        "sleep trackers",
        "mattress toppers",
        "sleep masks",
        "aromatherapy diffusers",
        "blue light glasses",
        "sleep supplements",
        "bedroom optimization"
    ],
    "content_types": [
        "product_review",
        "buying_guide",
        "how_to",
        "comparison",
        "tips_list"
    ]
}

# =============================================================================
# Website Configuration
# =============================================================================
WEBSITE_CONFIG = {
    "base_url": "https://sleepwisereviews.com",  # Update with actual URL
    "articles_per_week": 1,
    "sitemap_path": PROJECT_ROOT / "sitemap.xml",
    "template_path": TEMPLATES_DIR / "article_template.html"
}

# =============================================================================
# Scheduling Configuration
# =============================================================================
SCHEDULE_CONFIG = {
    "timezone": "UTC",
    "tasks": {
        "00:00": "pinterest_pin",
        "04:00": "content_prep",
        "08:00": "pinterest_pin",
        "12:00": "instagram_notify",
        "16:00": "engagement_tips",
        "20:00": "daily_summary"
    },
    "weekly_tasks": {
        "sunday": ["generate_article"]
    }
}

# =============================================================================
# Telegram Report Templates
# =============================================================================
TELEGRAM_TEMPLATES = {
    "header": "🌙 SleepWise Bot Report\n━━━━━━━━━━━━━━━━━━━━━━━\n",
    "pinterest_success": "📌 Pinterest:\n✅ Pin posted: \"{title}\"\n   Board: {board}\n   Link: {url}\n",
    "instagram_ready": "📸 Instagram Ready:\n🖼️ Image prepared\n📝 Caption:\n{caption}\n\n👆 Copy this to Meta Business Suite!\n",
    "daily_summary": "📊 Daily Summary:\n• Pinterest pins: {pins_count}\n• Pending IG posts: {ig_pending}\n• Website articles: {articles_count}\n",
    "weekly_summary": "📈 Weekly Stats:\n• Total pins: {total_pins}\n• New articles: {new_articles}\n• Content prepared: {content_count}\n"
}

# =============================================================================
# State File Paths
# =============================================================================
STATE_FILE = DATA_DIR / "state.json"
HISTORY_FILE = DATA_DIR / "task_history.json"
CALENDAR_FILE = TEMPLATES_DIR / "content_calendar.json"

# =============================================================================
# Utility Functions
# =============================================================================
def get_current_hour() -> int:
    """Get current hour in UTC."""
    return datetime.now(timezone.utc).hour

def get_current_day() -> str:
    """Get current day name in lowercase."""
    return datetime.now(timezone.utc).strftime("%A").lower()

def is_github_actions() -> bool:
    """Check if running in GitHub Actions environment."""
    return os.getenv("GITHUB_ACTIONS", "false").lower() == "true"

def validate_config() -> dict:
    """Validate that all required configuration is present."""
    issues = []

    if not TELEGRAM_BOT_TOKEN:
        issues.append("TELEGRAM_BOT_TOKEN not set")
    if not TELEGRAM_CHAT_ID:
        issues.append("TELEGRAM_CHAT_ID not set")
    if not PINTEREST_ACCESS_TOKEN:
        issues.append("PINTEREST_ACCESS_TOKEN not set")
    if not ANTHROPIC_API_KEY:
        issues.append("ANTHROPIC_API_KEY not set")

    return {
        "valid": len(issues) == 0,
        "issues": issues
    }
