"""
SleepWise Automation Agent - Telegram Reporter
Sends notifications and reports to Telegram.
"""

import requests
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime, timezone

import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_TEMPLATES

logger = logging.getLogger(__name__)


class TelegramReporter:
    """Handles all Telegram bot interactions for reporting."""

    def __init__(self, bot_token: str = None, chat_id: str = None):
        """
        Initialize the Telegram reporter.

        Args:
            bot_token: Telegram bot token (defaults to env var)
            chat_id: Telegram chat ID (defaults to env var)
        """
        self.bot_token = bot_token or TELEGRAM_BOT_TOKEN
        self.chat_id = chat_id or TELEGRAM_CHAT_ID
        self.api_base = f"https://api.telegram.org/bot{self.bot_token}"

    def _make_request(self, method: str, data: dict = None, files: dict = None) -> dict:
        """
        Make a request to the Telegram API.

        Args:
            method: API method name
            data: Request data
            files: Files to upload

        Returns:
            API response as dict
        """
        url = f"{self.api_base}/{method}"
        try:
            if files:
                response = requests.post(url, data=data, files=files, timeout=30)
            else:
                response = requests.post(url, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Telegram API error: {e}")
            return {"ok": False, "error": str(e)}

    def send_message(self, text: str, parse_mode: str = "HTML") -> dict:
        """
        Send a text message to the configured chat.

        Args:
            text: Message text
            parse_mode: Parse mode (HTML, Markdown, MarkdownV2)

        Returns:
            API response
        """
        data = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        result = self._make_request("sendMessage", data)
        if result.get("ok"):
            logger.info("Telegram message sent successfully")
        else:
            logger.error(f"Failed to send Telegram message: {result}")
        return result

    def send_photo(self, photo_path: str, caption: str = None) -> dict:
        """
        Send a photo with optional caption.

        Args:
            photo_path: Path to the photo file
            caption: Optional caption text

        Returns:
            API response
        """
        data = {
            "chat_id": self.chat_id,
            "parse_mode": "HTML"
        }
        if caption:
            data["caption"] = caption[:1024]  # Telegram caption limit

        with open(photo_path, "rb") as photo:
            files = {"photo": photo}
            result = self._make_request("sendPhoto", data=data, files=files)

        if result.get("ok"):
            logger.info("Telegram photo sent successfully")
        else:
            logger.error(f"Failed to send Telegram photo: {result}")
        return result

    def send_document(self, doc_path: str, caption: str = None) -> dict:
        """
        Send a document file.

        Args:
            doc_path: Path to the document
            caption: Optional caption text

        Returns:
            API response
        """
        data = {
            "chat_id": self.chat_id,
            "parse_mode": "HTML"
        }
        if caption:
            data["caption"] = caption[:1024]

        with open(doc_path, "rb") as doc:
            files = {"document": doc}
            result = self._make_request("sendDocument", data=data, files=files)

        if result.get("ok"):
            logger.info("Telegram document sent successfully")
        else:
            logger.error(f"Failed to send Telegram document: {result}")
        return result

    # ==========================================================================
    # Report Methods
    # ==========================================================================

    def send_startup_report(self) -> dict:
        """Send agent startup notification."""
        text = (
            f"{TELEGRAM_TEMPLATES['header']}"
            f"🚀 Agent Started\n"
            f"⏰ Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n\n"
            f"Ready to process tasks..."
        )
        return self.send_message(text)

    def send_pinterest_success(self, title: str, board: str, url: str) -> dict:
        """Send Pinterest pin success notification."""
        text = (
            f"{TELEGRAM_TEMPLATES['header']}"
            f"✅ Pinterest Pin Posted!\n\n"
            f"📌 Title: {title}\n"
            f"📁 Board: {board}\n"
            f"🔗 Link: {url}\n\n"
            f"⏰ {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"
        )
        return self.send_message(text)

    def send_instagram_content(self, caption: str, image_path: str = None,
                                hashtags: list = None) -> dict:
        """
        Send Instagram content ready for manual posting.

        Args:
            caption: Post caption
            image_path: Path to image (optional)
            hashtags: List of hashtags
        """
        hashtag_text = " ".join([f"#{tag}" for tag in (hashtags or [])])
        full_caption = f"{caption}\n\n{hashtag_text}" if hashtags else caption

        message = (
            f"{TELEGRAM_TEMPLATES['header']}"
            f"📸 Instagram Content Ready!\n\n"
            f"📝 Caption:\n"
            f"━━━━━━━━━━━━━━━\n"
            f"{full_caption}\n"
            f"━━━━━━━━━━━━━━━\n\n"
            f"👆 Copy this to Meta Business Suite!\n\n"
            f"⏰ {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"
        )

        if image_path and Path(image_path).exists():
            return self.send_photo(image_path, message[:1024])
        return self.send_message(message)

    def send_daily_summary(self, stats: dict) -> dict:
        """
        Send daily summary report.

        Args:
            stats: Dictionary with daily statistics
        """
        text = (
            f"{TELEGRAM_TEMPLATES['header']}"
            f"📊 Daily Summary\n\n"
            f"📌 Pinterest pins today: {stats.get('pins_today', 0)}\n"
            f"📸 IG posts prepared: {stats.get('ig_prepared', 0)}\n"
            f"📝 Articles generated: {stats.get('articles_today', 0)}\n\n"
            f"📈 Weekly totals:\n"
            f"   • Total pins: {stats.get('pins_week', 0)}\n"
            f"   • Total IG content: {stats.get('ig_week', 0)}\n"
            f"   • New articles: {stats.get('articles_week', 0)}\n\n"
            f"⏰ {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"
        )
        return self.send_message(text)

    def send_weekly_summary(self, stats: dict) -> dict:
        """
        Send weekly summary report.

        Args:
            stats: Dictionary with weekly statistics
        """
        text = (
            f"{TELEGRAM_TEMPLATES['header']}"
            f"📈 Weekly Summary Report\n\n"
            f"🗓️ Week Ending: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}\n\n"
            f"📌 Pinterest:\n"
            f"   • Pins posted: {stats.get('total_pins', 0)}\n"
            f"   • Impressions: {stats.get('pin_impressions', 'N/A')}\n\n"
            f"📸 Instagram:\n"
            f"   • Content prepared: {stats.get('ig_content', 0)}\n\n"
            f"📝 Website:\n"
            f"   • New articles: {stats.get('new_articles', 0)}\n"
            f"   • Total articles: {stats.get('total_articles', 0)}\n\n"
            f"🎯 Next week goals:\n"
            f"   • Pinterest: {stats.get('next_pins_goal', 28)} pins\n"
            f"   • Articles: {stats.get('next_articles_goal', 1)} article\n\n"
            f"Keep up the great work! 🌙"
        )
        return self.send_message(text)

    def send_error_report(self, error: str, task: str = None) -> dict:
        """
        Send error notification.

        Args:
            error: Error message
            task: Task that failed (optional)
        """
        text = (
            f"{TELEGRAM_TEMPLATES['header']}"
            f"❌ Error Occurred\n\n"
            f"🔴 Task: {task or 'Unknown'}\n"
            f"📝 Error: {error}\n\n"
            f"⏰ {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"
        )
        return self.send_message(text)

    def send_engagement_tips(self) -> dict:
        """Send daily engagement tips."""
        tips = [
            "💡 Respond to all Pinterest comments within 24 hours",
            "💡 Save pins from others in your niche to your boards",
            "💡 Check Instagram DMs for potential collaborations",
            "💡 Review which pins are performing best this week",
            "💡 Update old article with fresh information",
            "💡 Cross-promote your latest article on all platforms"
        ]
        import random
        tip = random.choice(tips)

        text = (
            f"{TELEGRAM_TEMPLATES['header']}"
            f"🎯 Engagement Tip of the Day\n\n"
            f"{tip}\n\n"
            f"⏰ {datetime.now(timezone.utc).strftime('%H:%M UTC')}"
        )
        return self.send_message(text)

    def send_article_notification(self, title: str, url: str) -> dict:
        """
        Notify about new article generation.

        Args:
            title: Article title
            url: Article URL
        """
        text = (
            f"{TELEGRAM_TEMPLATES['header']}"
            f"📝 New Article Published!\n\n"
            f"📄 Title: {title}\n"
            f"🔗 URL: {url}\n\n"
            f"✅ Article is live on the website!\n\n"
            f"📌 Next steps:\n"
            f"   1. Create Pinterest pins for this article\n"
            f"   2. Share excerpt on Instagram\n"
            f"   3. Update internal links\n\n"
            f"⏰ {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"
        )
        return self.send_message(text)

    def test_connection(self) -> bool:
        """Test the Telegram bot connection."""
        result = self._make_request("getMe")
        if result.get("ok"):
            bot_name = result.get("result", {}).get("username", "Unknown")
            logger.info(f"Connected to Telegram bot: @{bot_name}")
            return True
        logger.error("Failed to connect to Telegram bot")
        return False

    # ==========================================================================
    # Two-Way Communication Methods
    # ==========================================================================

    def request_help(self, request_type: str, details: str, options: list = None) -> dict:
        """
        Request help from the user for something the bot needs.

        Args:
            request_type: Type of request (image, approval, input, etc.)
            details: What is needed and why
            options: Optional list of choices
        """
        emoji_map = {
            "image": "🖼️",
            "approval": "✅",
            "input": "📝",
            "review": "👀",
            "decision": "🤔",
            "upload": "📤"
        }
        emoji = emoji_map.get(request_type, "❓")

        text = (
            f"{TELEGRAM_TEMPLATES['header']}"
            f"{emoji} Help Needed\n\n"
            f"📋 Request: {request_type.title()}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"{details}\n"
            f"━━━━━━━━━━━━━━━\n"
        )

        if options:
            text += "\n🔘 Options:\n"
            for i, option in enumerate(options, 1):
                text += f"   {i}. {option}\n"

        text += (
            f"\n💬 Reply to this message with your response.\n\n"
            f"⏰ {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"
        )
        return self.send_message(text)

    def report_completed(self, task: str, summary: str, details: list = None,
                         next_steps: list = None) -> dict:
        """
        Report completed work to the user.

        Args:
            task: Name of the completed task
            summary: Brief summary of what was done
            details: List of specific actions taken
            next_steps: List of suggested next actions
        """
        text = (
            f"{TELEGRAM_TEMPLATES['header']}"
            f"✅ Task Completed\n\n"
            f"📌 Task: {task}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"{summary}\n"
            f"━━━━━━━━━━━━━━━\n"
        )

        if details:
            text += "\n📋 What was done:\n"
            for detail in details:
                text += f"   • {detail}\n"

        if next_steps:
            text += "\n🎯 Suggested next steps:\n"
            for i, step in enumerate(next_steps, 1):
                text += f"   {i}. {step}\n"

        text += f"\n⏰ {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"
        return self.send_message(text)

    def send_content_idea(self, topic: str, content_type: str,
                          outline: list = None, inspired_by: str = None) -> dict:
        """
        Send a content idea for approval before creating.

        Args:
            topic: The topic suggestion
            content_type: Type of content (article, post, etc.)
            outline: Optional content outline
            inspired_by: Book or source of inspiration
        """
        text = (
            f"{TELEGRAM_TEMPLATES['header']}"
            f"💡 Content Idea\n\n"
            f"📝 Topic: {topic}\n"
            f"📄 Type: {content_type}\n"
        )

        if inspired_by:
            text += f"📚 Inspired by: {inspired_by}\n"

        if outline:
            text += "\n📋 Proposed outline:\n"
            for i, point in enumerate(outline, 1):
                text += f"   {i}. {point}\n"

        text += (
            f"\n━━━━━━━━━━━━━━━\n"
            f"Reply with:\n"
            f"   ✅ 'yes' to approve\n"
            f"   ✏️ 'edit: [your changes]' to modify\n"
            f"   ❌ 'no' to reject\n\n"
            f"⏰ {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"
        )
        return self.send_message(text)


# =============================================================================
# Standalone test
# =============================================================================
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    reporter = TelegramReporter()

    if reporter.test_connection():
        print("✅ Telegram connection successful!")
        # Uncomment to test:
        # reporter.send_startup_report()
    else:
        print("❌ Failed to connect to Telegram")
