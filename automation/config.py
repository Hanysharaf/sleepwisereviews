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
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

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

    # Educational topics (inspired by sleep books: Why We Sleep, Sleep Smarter, etc.)
    "educational_topics": [
        "why we need 8 hours of sleep",
        "sleep stages and REM cycles explained",
        "how sleep affects memory and learning",
        "the science of circadian rhythms",
        "sleep deprivation effects on health",
        "how blue light disrupts sleep",
        "the role of melatonin in sleep",
        "sleep and mental health connection",
        "how exercise improves sleep quality",
        "caffeine and sleep relationship",
        "sleep hygiene best practices",
        "power naps benefits and timing",
        "sleep and weight loss connection",
        "how temperature affects sleep",
        "dreams and their purpose",
        "sleep disorders overview",
        "sleep tips for shift workers",
        "creating the perfect sleep environment",
        "sleep and aging relationship",
        "meditation and sleep quality"
    ],

    # Product topics (affiliate content)
    "product_topics": [
        "weighted blankets",
        "sleep pillows",
        "white noise machines",
        "sleep trackers",
        "mattress toppers",
        "sleep masks",
        "aromatherapy diffusers",
        "blue light glasses",
        "sleep supplements",
        "bedroom optimization",
        "cooling mattress pads",
        "smart alarm clocks",
        "blackout curtains",
        "essential oils for sleep",
        "sleep headphones"
    ],

    # Combined topics list (for random selection)
    "topics": [
        # Educational
        "why we need 8 hours of sleep",
        "sleep stages and REM cycles",
        "how sleep affects memory",
        "circadian rhythms explained",
        "sleep and mental health",
        # Products
        "weighted blankets",
        "sleep pillows",
        "white noise machines",
        "sleep trackers",
        "sleep masks"
    ],

    "content_types": [
        "educational_article",    # Sleep science content
        "product_review",         # Single product review
        "buying_guide",           # Best X for Y
        "how_to",                 # How to improve sleep
        "comparison",             # Product vs product
        "tips_list",              # 10 tips for better sleep
        "book_insights"           # Key insights from sleep books
    ],

    # Book references for educational content
    "book_inspirations": [
        "Why We Sleep by Matthew Walker",
        "Sleep Smarter by Shawn Stevenson",
        "The Sleep Solution by W. Chris Winter",
        "The Promise of Sleep by William Dement",
        "Say Good Night to Insomnia by Gregg Jacobs"
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
        "04:00": "content_prep",
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
    if not ANTHROPIC_API_KEY:
        issues.append("ANTHROPIC_API_KEY not set")

    return {
        "valid": len(issues) == 0,
        "issues": issues
    }
