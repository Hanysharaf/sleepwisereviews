"""
SleepWise Telegram Command Bot
Receives commands via Telegram and triggers GitHub Actions workflows.
Includes LLM integration for text improvement.
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
import anthropic

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
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Initialize Anthropic client
claude_client = None
if ANTHROPIC_API_KEY:
    claude_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

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


async def process_with_llm(text: str, task: str = "improve") -> dict:
    """
    Process text with Claude LLM.

    Tasks:
    - improve: Fix grammar, spelling, and improve clarity
    - rewrite: Rewrite the text professionally
    - summarize: Summarize the text
    - translate: Translate to English if needed
    """
    if not claude_client:
        return {"ok": False, "message": "ANTHROPIC_API_KEY not configured"}

    prompts = {
        "improve": f"""Fix any grammar, spelling, and punctuation errors in this text.
Improve clarity while keeping the same meaning and tone.
Only return the fixed text, nothing else.

Text to fix:
{text}""",

        "rewrite": f"""Rewrite this text to be more professional and polished.
Keep the same meaning but improve the writing quality.
Only return the rewritten text, nothing else.

Text to rewrite:
{text}""",

        "summarize": f"""Summarize this text concisely.
Only return the summary, nothing else.

Text to summarize:
{text}""",

        "caption": f"""Create an engaging Instagram caption from this text.
Include relevant emojis and make it engaging.
Add 5-10 relevant hashtags at the end.
Only return the caption, nothing else.

Text:
{text}"""
    }

    prompt = prompts.get(task, prompts["improve"])

    try:
        message = claude_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        result_text = message.content[0].text
        return {"ok": True, "text": result_text}

    except Exception as e:
        logger.error(f"LLM processing error: {e}")
        return {"ok": False, "message": str(e)}


# =============================================================================
# Command Handlers
# =============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message with available commands."""
    if not is_authorized(update):
        await update.message.reply_text("Unauthorized. This bot is private.")
        return

    welcome = """🌙 Welcome to SleepWise Command Bot!

📝 **Text Processing (AI):**
Just send any text → I'll fix/improve it!
/fix [text] - Fix grammar & spelling
/rewrite [text] - Professional rewrite
/caption [text] - Create Instagram caption

📰 **Content Generation:**
/article [topic] - Generate article
/instagram [topic] - Prepare IG post

📊 **Status & Reports:**
/summary - Get daily summary
/status - Check automation status
/test - Test API connections

/help - Show this message

**Example:**
/article best pillows for side sleepers
/caption 5 tips for better sleep tonight
"""
    await update.message.reply_text(welcome, parse_mode="Markdown")


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

    llm_status = "✅ Active" if claude_client else "❌ Not configured"

    status_message = f"""
🌙 SleepWise Automation Status

🤖 Bot Status: Online
⏰ Time: {now.strftime('%Y-%m-%d %H:%M UTC')}

🔄 GitHub Actions: Active
📅 Schedule: Every 2 hours

🧠 LLM (Claude): {llm_status}

📋 Automated Tasks:
  • Content preparation
  • Daily summaries
  • Engagement tips
  • Article generation (Sunday)

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


async def fix_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fix/improve text using LLM."""
    if not is_authorized(update):
        await update.message.reply_text("Unauthorized.")
        return

    text = " ".join(context.args) if context.args else None

    if not text:
        await update.message.reply_text(
            "Please provide text to fix.\n"
            "Usage: /fix Your text here\n\n"
            "Or just send any text and I'll improve it!"
        )
        return

    await update.message.reply_text("Processing with AI...")

    result = await process_with_llm(text, "improve")

    if result["ok"]:
        await update.message.reply_text(f"✅ Fixed text:\n\n{result['text']}")
    else:
        await update.message.reply_text(f"❌ Error: {result['message']}")


async def rewrite_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Rewrite text professionally using LLM."""
    if not is_authorized(update):
        await update.message.reply_text("Unauthorized.")
        return

    text = " ".join(context.args) if context.args else None

    if not text:
        await update.message.reply_text(
            "Please provide text to rewrite.\n"
            "Usage: /rewrite Your text here"
        )
        return

    await update.message.reply_text("Rewriting with AI...")

    result = await process_with_llm(text, "rewrite")

    if result["ok"]:
        await update.message.reply_text(f"✅ Rewritten:\n\n{result['text']}")
    else:
        await update.message.reply_text(f"❌ Error: {result['message']}")


async def caption_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Create Instagram caption using LLM."""
    if not is_authorized(update):
        await update.message.reply_text("Unauthorized.")
        return

    text = " ".join(context.args) if context.args else None

    if not text:
        await update.message.reply_text(
            "Please provide text or topic for caption.\n"
            "Usage: /caption Your topic or text here"
        )
        return

    await update.message.reply_text("Creating caption with AI...")

    result = await process_with_llm(text, "caption")

    if result["ok"]:
        await update.message.reply_text(
            f"📸 Instagram Caption:\n\n{result['text']}\n\n"
            f"👆 Copy this to Instagram!"
        )
    else:
        await update.message.reply_text(f"❌ Error: {result['message']}")


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle unknown commands."""
    if not is_authorized(update):
        return

    await update.message.reply_text(
        "Unknown command. Use /help to see available commands."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular messages - automatically improve text with LLM."""
    if not is_authorized(update):
        return

    text = update.message.text

    # If text is short and looks like a question about commands
    if len(text) < 20 and ("help" in text.lower() or "?" in text):
        await start(update, context)
        return

    # Process any text with LLM automatically
    if len(text) >= 10:  # Only process texts with at least 10 characters
        await update.message.reply_text("🤖 Processing your text with AI...")

        result = await process_with_llm(text, "improve")

        if result["ok"]:
            await update.message.reply_text(
                f"✅ **Improved text:**\n\n{result['text']}\n\n"
                f"━━━━━━━━━━━━━━━\n"
                f"💡 Other options:\n"
                f"/rewrite - Professional rewrite\n"
                f"/caption - Instagram caption",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(
                f"❌ Could not process: {result['message']}\n\n"
                f"Make sure ANTHROPIC_API_KEY is set."
            )
    else:
        await update.message.reply_text(
            "Send me any text and I'll improve it!\n\n"
            "Or use /help to see all commands."
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
    application.add_handler(CommandHandler("fix", fix_command))
    application.add_handler(CommandHandler("rewrite", rewrite_command))
    application.add_handler(CommandHandler("caption", caption_command))

    # Handle unknown commands
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    # Handle regular messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling
    logger.info("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
