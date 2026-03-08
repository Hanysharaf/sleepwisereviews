"""
SleepWise Telegram Command Bot
Receives commands via Telegram and triggers GitHub Actions workflows.
"""

import os
import logging
import asyncio
from datetime import datetime, timezone
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)
import aiohttp

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO", "Hanysharaf/sleepwisereviews")

# GitHub API endpoint for workflow dispatch
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/actions/workflows/automation.yml/dispatches"


def is_authorized(update: Update) -> bool:
    """Check if the user is authorized to use the bot."""
    chat_id = str(update.effective_chat.id)
    return chat_id == TELEGRAM_CHAT_ID


async def trigger_workflow(task: str, topic: str = None) -> dict:
    """Trigger GitHub Actions workflow via API."""
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    payload = {
        "ref": "main",
        "inputs": {
            "task": task
        }
    }

    # Add topic if provided (for article generation)
    if topic:
        payload["inputs"]["topic"] = topic

    async with aiohttp.ClientSession() as session:
        async with session.post(GITHUB_API_URL, headers=headers, json=payload) as response:
            if response.status == 204:
                return {"ok": True, "message": "Workflow triggered successfully"}
            else:
                error_text = await response.text()
                return {"ok": False, "message": f"Failed: {response.status} - {error_text}"}


# =============================================================================
# Command Handlers
# =============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message with available commands."""
    if not is_authorized(update):
        await update.message.reply_text("Unauthorized. This bot is private.")
        return

    welcome = """
Welcome to SleepWise Command Bot!

Available Commands:
/article [topic] - Generate a new article
/summary - Get daily summary now
/status - Check automation status
/instagram [topic] - Prepare Instagram post
/test - Test all API connections
/help - Show this help message

Example:
/article weighted blankets for anxiety
"""
    await update.message.reply_text(welcome)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show help message."""
    await start(update, context)


async def article_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate a new article."""
    if not is_authorized(update):
        await update.message.reply_text("Unauthorized.")
        return

    # Get topic from command arguments
    topic = " ".join(context.args) if context.args else None

    await update.message.reply_text(
        f"Starting article generation...\n"
        f"Topic: {topic or 'Random (from content calendar)'}\n\n"
        f"This may take 2-3 minutes. I'll notify you when done!"
    )

    # Trigger workflow
    result = await trigger_workflow("article", topic)

    if result["ok"]:
        await update.message.reply_text(
            "GitHub Actions workflow triggered!\n"
            "Check back in a few minutes for the result."
        )
    else:
        await update.message.reply_text(f"Failed to trigger workflow: {result['message']}")


async def summary_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Get daily summary."""
    if not is_authorized(update):
        await update.message.reply_text("Unauthorized.")
        return

    await update.message.reply_text("Generating daily summary...")

    result = await trigger_workflow("summary")

    if result["ok"]:
        await update.message.reply_text("Summary workflow triggered! You'll receive it shortly.")
    else:
        await update.message.reply_text(f"Failed: {result['message']}")


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check automation status."""
    if not is_authorized(update):
        await update.message.reply_text("Unauthorized.")
        return

    now = datetime.now(timezone.utc)

    status_message = f"""
SleepWise Automation Status

Bot Status: Online
Time: {now.strftime('%Y-%m-%d %H:%M UTC')}

GitHub Actions: Active
Scheduled Tasks:
  - 04:00 UTC: Content Prep
  - 12:00 UTC: Instagram Notify
  - 16:00 UTC: Engagement Tips
  - 20:00 UTC: Daily Summary
  - Sunday 12:00: Article Generation

Use /test to verify API connections.
"""
    await update.message.reply_text(status_message)


async def instagram_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Prepare Instagram content."""
    if not is_authorized(update):
        await update.message.reply_text("Unauthorized.")
        return

    topic = " ".join(context.args) if context.args else None

    await update.message.reply_text(
        f"Preparing Instagram content...\n"
        f"Topic: {topic or 'Random'}"
    )

    # This would trigger content_prep task
    result = await trigger_workflow("content_prep")

    if result["ok"]:
        await update.message.reply_text("Instagram content prep started!")
    else:
        await update.message.reply_text(f"Failed: {result['message']}")


async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Test API connections."""
    if not is_authorized(update):
        await update.message.reply_text("Unauthorized.")
        return

    await update.message.reply_text("Running connection tests...")

    result = await trigger_workflow("test")

    if result["ok"]:
        await update.message.reply_text(
            "Test workflow triggered!\n"
            "Results will be sent via the automation bot."
        )
    else:
        await update.message.reply_text(f"Failed: {result['message']}")


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle unknown commands."""
    if not is_authorized(update):
        return

    await update.message.reply_text(
        "Unknown command. Use /help to see available commands."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular messages (not commands)."""
    if not is_authorized(update):
        return

    text = update.message.text.lower()

    # Simple keyword detection for convenience
    if "article" in text:
        await update.message.reply_text(
            "Want to generate an article? Use:\n"
            "/article [topic]\n\n"
            "Example: /article best sleep masks 2024"
        )
    elif "help" in text:
        await start(update, context)
    else:
        await update.message.reply_text(
            "I respond to commands. Use /help to see what I can do!"
        )


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    """Start the bot."""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set!")
        return

    if not GITHUB_TOKEN:
        logger.error("GITHUB_TOKEN not set!")
        return

    logger.info("Starting SleepWise Command Bot...")

    # Create application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("article", article_command))
    application.add_handler(CommandHandler("summary", summary_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("instagram", instagram_command))
    application.add_handler(CommandHandler("test", test_command))

    # Handle unknown commands
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    # Handle regular messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling
    logger.info("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
