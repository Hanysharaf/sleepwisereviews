"""
SleepWise Automation Agent - Telegram Bot Integration
Sends notifications and reports to Telegram.
"""

import requests
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, List, Dict
import json

import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_TEMPLATES, DATA_DIR

logger = logging.getLogger(__name__)


class TelegramBot:
    """Handles all Telegram notifications and reporting."""

    def __init__(self, bot_token: str = None, chat_id: str = None):
        """
        Initialize Telegram bot.

        Args:
            bot_token: Telegram bot token (from @BotFather)
            chat_id: Your Telegram chat ID
        """
        self.bot_token = bot_token or TELEGRAM_BOT_TOKEN
        self.chat_id = chat_id or TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        self.history_file = DATA_DIR / "telegram_history.json"

    # ==========================================================================
    # Core Messaging
    # ==========================================================================

    def send_message(self, text: str, parse_mode: str = "HTML",
                     disable_preview: bool = True) -> dict:
        """
        Send a text message to Telegram.

        Args:
            text: Message text (supports HTML formatting)
            parse_mode: HTML or Markdown
            disable_preview: Disable link previews

        Returns:
            API response
        """
        if not self.bot_token or not self.chat_id:
            logger.error("Telegram credentials not configured")
            return {"ok": False, "error": "Credentials not configured"}

        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": disable_preview
        }

        try:
            response = requests.post(url, json=payload, timeout=30)
            result = response.json()

            if result.get("ok"):
                self._log_message(text, "sent")
                logger.info("Telegram message sent successfully")
            else:
                logger.error(f"Telegram API error: {result.get('description')}")

            return result

        except requests.RequestException as e:
            logger.error(f"Telegram request failed: {e}")
            return {"ok": False, "error": str(e)}

    def send_photo(self, photo_path: str, caption: str = None) -> dict:
        """
        Send a photo to Telegram.

        Args:
            photo_path: Path to image file
            caption: Optional caption (max 1024 chars)

        Returns:
            API response
        """
        if not self.bot_token or not self.chat_id:
            return {"ok": False, "error": "Credentials not configured"}

        url = f"{self.base_url}/sendPhoto"

        try:
            with open(photo_path, "rb") as photo:
                files = {"photo": photo}
                data = {
                    "chat_id": self.chat_id,
                    "parse_mode": "HTML"
                }
                if caption:
                    data["caption"] = caption[:1024]

                response = requests.post(url, data=data, files=files, timeout=60)
                return response.json()

        except FileNotFoundError:
            return {"ok": False, "error": f"Photo not found: {photo_path}"}
        except requests.RequestException as e:
            return {"ok": False, "error": str(e)}

    def send_document(self, document_path: str, caption: str = None) -> dict:
        """Send a document/file to Telegram."""
        if not self.bot_token or not self.chat_id:
            return {"ok": False, "error": "Credentials not configured"}

        url = f"{self.base_url}/sendDocument"

        try:
            with open(document_path, "rb") as doc:
                files = {"document": doc}
                data = {"chat_id": self.chat_id}
                if caption:
                    data["caption"] = caption[:1024]

                response = requests.post(url, data=data, files=files, timeout=60)
                return response.json()

        except FileNotFoundError:
            return {"ok": False, "error": f"Document not found: {document_path}"}
        except requests.RequestException as e:
            return {"ok": False, "error": str(e)}

    # ==========================================================================
    # Notification Types
    # ==========================================================================

    def notify_post_created(self, platform: str, content: dict) -> dict:
        """
        Notify when a post is created/scheduled.

        Args:
            platform: instagram, pinterest, etc.
            content: Post content data
        """
        icons = {
            "instagram": "Instagram",
            "pinterest": "Pinterest",
            "twitter": "Twitter/X"
        }

        message = (
            f"{TELEGRAM_TEMPLATES['header']}"
            f"<b>New Post Created</b>\n\n"
            f"Platform: {icons.get(platform, platform)}\n"
            f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        )

        if content.get("caption"):
            caption_preview = content["caption"][:200]
            if len(content["caption"]) > 200:
                caption_preview += "..."
            message += f"<b>Caption Preview:</b>\n<code>{caption_preview}</code>\n\n"

        if content.get("hashtags"):
            message += f"<b>Hashtags:</b> {len(content['hashtags'])} tags\n"

        if content.get("scheduled_time"):
            message += f"<b>Scheduled:</b> {content['scheduled_time']}\n"

        if content.get("status"):
            status_icons = {"pending": "Pending", "scheduled": "Scheduled", "posted": "Posted"}
            message += f"<b>Status:</b> {status_icons.get(content['status'], content['status'])}\n"

        return self.send_message(message)

    def notify_post_published(self, platform: str, post_url: str = None) -> dict:
        """Notify when a post is successfully published."""
        message = (
            f"{TELEGRAM_TEMPLATES['header']}"
            f"<b>Post Published!</b>\n\n"
            f"Platform: {platform}\n"
            f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        )

        if post_url:
            message += f"Link: {post_url}\n"

        message += "\n<b>Keep growing!</b>"

        return self.send_message(message)

    def notify_pin_posted(self, pin_data: dict) -> dict:
        """
        Notify when a Pinterest pin is actually posted.
        Includes the real pin URL.
        """
        message = (
            f"<b>Pinterest Pin Posted!</b>\n\n"
            f"<b>{pin_data.get('title', 'New Pin')}</b>\n\n"
        )

        if pin_data.get("pin_url"):
            message += f"<b>View Pin:</b>\n{pin_data['pin_url']}\n\n"

        if pin_data.get("link"):
            message += f"<b>Links to:</b>\n{pin_data['link']}\n\n"

        message += f"<i>{datetime.now().strftime('%Y-%m-%d %H:%M')}</i>"

        return self.send_message(message, disable_preview=False)

    def notify_instagram_posted(self, post_data: dict) -> dict:
        """
        Notify when Instagram content is posted.
        """
        message = (
            f"<b>Instagram Posted!</b>\n\n"
        )

        if post_data.get("caption"):
            caption_preview = post_data["caption"][:100]
            message += f"<b>Caption:</b>\n{caption_preview}...\n\n"

        if post_data.get("post_url"):
            message += f"<b>View Post:</b>\n{post_data['post_url']}\n\n"

        if post_data.get("hashtags"):
            message += f"<b>Hashtags:</b> {len(post_data['hashtags'])} tags\n"

        message += f"\n<i>{datetime.now().strftime('%Y-%m-%d %H:%M')}</i>"

        return self.send_message(message, disable_preview=False)

    def notify_error(self, error_type: str, error_message: str,
                     details: str = None) -> dict:
        """Notify about an error."""
        message = (
            f"<b>Error Alert</b>\n\n"
            f"<b>Type:</b> {error_type}\n"
            f"<b>Message:</b> {error_message}\n"
        )

        if details:
            message += f"<b>Details:</b>\n<code>{details[:500]}</code>\n"

        message += f"\n<i>Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>"

        return self.send_message(message)

    def notify_daily_tip(self, tip: str) -> dict:
        """Send the daily sleep tip."""
        message = (
            f"<b>Daily Sleep Tip</b>\n\n"
            f"{tip}\n\n"
            f"<i>Share this with someone who needs better sleep!</i>"
        )
        return self.send_message(message)

    # ==========================================================================
    # Reports
    # ==========================================================================

    def send_daily_report_with_links(self, stats: dict) -> dict:
        """
        Send daily summary report WITH actual links to posted content.

        Args:
            stats: Dictionary with daily statistics including posted URLs
        """
        message = (
            f"{TELEGRAM_TEMPLATES['header']}"
            f"<b>Daily Report - {datetime.now().strftime('%B %d, %Y')}</b>\n\n"
        )

        # Pinterest pins posted today
        pinterest_posts = stats.get("pinterest_today", [])
        if pinterest_posts:
            message += f"<b>Pinterest Pins Posted: {len(pinterest_posts)}</b>\n"
            for pin in pinterest_posts[:5]:  # Show max 5
                title = pin.get("title", "Pin")[:40]
                url = pin.get("pin_url", "")
                message += f"  {title}\n  {url}\n\n"
        else:
            message += "<b>Pinterest:</b> No pins today\n\n"

        # Instagram posts
        instagram_posts = stats.get("instagram_today", [])
        if instagram_posts:
            message += f"<b>Instagram Posts: {len(instagram_posts)}</b>\n"
            for post in instagram_posts[:5]:
                caption = post.get("caption", "")[:40]
                url = post.get("post_url", "")
                message += f"  {caption}...\n"
                if url:
                    message += f"  {url}\n\n"
        else:
            message += "<b>Instagram:</b> No posts today\n\n"

        # Weekly totals
        message += f"<b>Weekly Totals:</b>\n"
        message += f"  Pinterest pins: {stats.get('pinterest_week_count', 0)}\n"
        message += f"  Instagram posts: {stats.get('instagram_week_count', 0)}\n"
        message += f"  Articles: {stats.get('articles_week_count', 0)}\n\n"

        # Queue status
        message += f"<b>Content Queue:</b>\n"
        message += f"  Pinterest: {stats.get('pinterest_queue', 0)} pins ready\n"
        message += f"  Instagram: {stats.get('instagram_queue', 0)} posts ready\n\n"

        # Links to your pages
        message += f"<b>Your Pages:</b>\n"
        message += f"  Website: https://hanysharaf.github.io/sleepwisereviews/\n"
        message += f"  Pinterest: https://pinterest.com/sleepwisereviews/\n"

        message += f"\n{datetime.now().strftime('%Y-%m-%d %H:%M')} UTC"

        return self.send_message(message)

    def send_daily_report(self, stats: dict) -> dict:
        """
        Send daily summary report.

        Args:
            stats: Dictionary with daily statistics
        """
        message = (
            f"{TELEGRAM_TEMPLATES['header']}"
            f"<b>Daily Report - {datetime.now().strftime('%B %d, %Y')}</b>\n\n"
            f"<b>Today's Activity:</b>\n"
            f"Posts created: {stats.get('posts_created', 0)}\n"
            f"Posts published: {stats.get('posts_published', 0)}\n"
            f"Pending posts: {stats.get('pending_posts', 0)}\n\n"
        )

        if stats.get("platforms"):
            message += "<b>By Platform:</b>\n"
            for platform, count in stats["platforms"].items():
                message += f"  {platform}: {count}\n"
            message += "\n"

        if stats.get("tomorrow_scheduled"):
            message += f"<b>Scheduled for Tomorrow:</b> {stats['tomorrow_scheduled']} posts\n\n"

        if stats.get("content_queue"):
            message += f"<b>Content Queue:</b> {stats['content_queue']} items ready\n"

        message += "\n<i>Keep up the great work!</i>"

        return self.send_message(message)

    def send_weekly_report(self, stats: dict) -> dict:
        """Send weekly summary report."""
        message = (
            f"{TELEGRAM_TEMPLATES['header']}"
            f"<b>Weekly Report</b>\n"
            f"<i>Week of {datetime.now().strftime('%B %d, %Y')}</i>\n\n"
            f"<b>This Week:</b>\n"
            f"Total posts: {stats.get('total_posts', 0)}\n"
            f"Instagram: {stats.get('instagram_posts', 0)}\n"
            f"Pinterest: {stats.get('pinterest_posts', 0)}\n\n"
        )

        if stats.get("top_content"):
            message += f"<b>Best Performing:</b>\n{stats['top_content']}\n\n"

        if stats.get("next_week_planned"):
            message += f"<b>Next Week:</b> {stats['next_week_planned']} posts planned\n"

        message += "\n<b>Revenue Update:</b>\n"
        message += f"Affiliate clicks: {stats.get('affiliate_clicks', 'N/A')}\n"
        message += f"Estimated earnings: ${stats.get('estimated_earnings', '0.00')}\n"

        return self.send_message(message)

    def send_instagram_ready(self, post_data: dict) -> dict:
        """
        Send Instagram post content ready for manual posting.

        Args:
            post_data: Post data including caption, hashtags, etc.
        """
        message = (
            f"<b>Instagram Post Ready!</b>\n\n"
            f"<b>Copy this caption:</b>\n"
            f"<code>{post_data.get('full_caption', post_data.get('caption', ''))}</code>\n\n"
        )

        if post_data.get("suggested_time"):
            message += f"<b>Best time to post:</b> {post_data['suggested_time']}\n"

        if post_data.get("article_url"):
            message += f"<b>Update link in bio to:</b>\n{post_data['article_url']}\n"

        message += (
            f"\n<b>Instructions:</b>\n"
            f"1. Open Meta Business Suite\n"
            f"2. Create new post\n"
            f"3. Paste caption above\n"
            f"4. Add your image\n"
            f"5. Schedule or post now\n"
        )

        return self.send_message(message)

    # ==========================================================================
    # Task Notifications
    # ==========================================================================

    def notify_task_started(self, task_name: str) -> dict:
        """Notify that a scheduled task has started."""
        message = (
            f"<b>Task Started</b>\n\n"
            f"Task: {task_name}\n"
            f"Time: {datetime.now().strftime('%H:%M:%S')}\n"
        )
        return self.send_message(message)

    def notify_task_completed(self, task_name: str, result: str = None) -> dict:
        """Notify that a task has completed."""
        message = (
            f"<b>Task Completed</b>\n\n"
            f"Task: {task_name}\n"
            f"Status: Success\n"
        )
        if result:
            message += f"Result: {result}\n"

        message += f"Time: {datetime.now().strftime('%H:%M:%S')}"

        return self.send_message(message)

    def notify_scheduler_status(self, status: str, next_tasks: List[dict] = None) -> dict:
        """Send scheduler status update."""
        message = (
            f"{TELEGRAM_TEMPLATES['header']}"
            f"<b>Scheduler Status</b>\n\n"
            f"Status: {status}\n"
            f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        )

        if next_tasks:
            message += "<b>Upcoming Tasks:</b>\n"
            for task in next_tasks[:5]:
                message += f"  {task.get('time', 'N/A')} - {task.get('name', 'Unknown')}\n"

        return self.send_message(message)

    # ==========================================================================
    # Utility Methods
    # ==========================================================================

    def _log_message(self, message: str, status: str):
        """Log sent message to history file."""
        self.history_file.parent.mkdir(parents=True, exist_ok=True)

        history = []
        if self.history_file.exists():
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except json.JSONDecodeError:
                history = []

        history.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": message[:500],  # Truncate for storage
            "status": status
        })

        # Keep last 100 messages
        history = history[-100:]

        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)

    def test_connection(self) -> bool:
        """Test the Telegram bot connection."""
        result = self.send_message(
            "<b>SleepWise Bot Connected!</b>\n\n"
            "Automation system is now active.\n"
            f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        return result.get("ok", False)

    def get_me(self) -> dict:
        """Get bot information."""
        url = f"{self.base_url}/getMe"
        try:
            response = requests.get(url, timeout=10)
            return response.json()
        except requests.RequestException as e:
            return {"ok": False, "error": str(e)}


# =============================================================================
# Standalone test
# =============================================================================
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    bot = TelegramBot()

    # Test connection
    print("Testing Telegram connection...")
    bot_info = bot.get_me()

    if bot_info.get("ok"):
        print(f"Bot name: {bot_info['result']['first_name']}")
        print(f"Username: @{bot_info['result']['username']}")

        # Send test message
        if bot.test_connection():
            print("Test message sent successfully!")
        else:
            print("Failed to send test message")
    else:
        print(f"Failed to connect: {bot_info.get('error', 'Unknown error')}")
        print("Make sure TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are set in .env")
