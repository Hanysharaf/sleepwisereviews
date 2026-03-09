"""
SleepWise Automation Agent - Queue Sender
Sends pre-written content from the queue without needing API credits.
Content is generated using Claude Code sessions and stored in content_queue.json.
"""

import json
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, List

import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import DATA_DIR, TELEGRAM_TEMPLATES

logger = logging.getLogger(__name__)

QUEUE_FILE = DATA_DIR / "content_queue.json"


class QueueSender:
    """Sends pre-written content from the queue file."""

    def __init__(self, telegram_reporter=None):
        """
        Initialize the queue sender.

        Args:
            telegram_reporter: TelegramReporter instance for sending messages
        """
        self.telegram = telegram_reporter
        self.queue = self._load_queue()

    def _load_queue(self) -> dict:
        """Load the content queue from file."""
        if QUEUE_FILE.exists():
            try:
                with open(QUEUE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.error("Could not parse queue file")
                return self._get_empty_queue()
        return self._get_empty_queue()

    def _get_empty_queue(self) -> dict:
        """Return empty queue structure."""
        return {
            "version": "1.0",
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "daily_tips": [],
            "instagram_captions": [],
            "engagement_messages": [],
            "weekly_tasks": []
        }

    def _save_queue(self):
        """Save the queue back to file."""
        self.queue["last_updated"] = datetime.now(timezone.utc).isoformat()
        with open(QUEUE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.queue, f, indent=2, ensure_ascii=False)
        logger.info("Queue saved")

    def _get_next_unsent(self, queue_name: str) -> Optional[dict]:
        """
        Get the next unsent item from a queue.

        Args:
            queue_name: Name of the queue (daily_tips, instagram_captions, etc.)

        Returns:
            Next unsent item or None
        """
        items = self.queue.get(queue_name, [])
        for item in items:
            if not item.get("sent", False):
                return item
        return None

    def _mark_as_sent(self, queue_name: str, item_id: str):
        """
        Mark an item as sent.

        Args:
            queue_name: Name of the queue
            item_id: ID of the item to mark
        """
        items = self.queue.get(queue_name, [])
        for item in items:
            if item.get("id") == item_id:
                item["sent"] = True
                item["sent_at"] = datetime.now(timezone.utc).isoformat()
                break
        self._save_queue()

    def reset_queue(self, queue_name: str = None):
        """
        Reset sent status for all items in a queue (or all queues).

        Args:
            queue_name: Specific queue to reset, or None for all
        """
        queues = [queue_name] if queue_name else ["daily_tips", "instagram_captions", "engagement_messages"]

        for qname in queues:
            items = self.queue.get(qname, [])
            for item in items:
                item["sent"] = False
                item.pop("sent_at", None)

        self._save_queue()
        logger.info(f"Queue(s) reset: {queues}")

    # =========================================================================
    # Send Methods
    # =========================================================================

    def send_daily_tip(self) -> dict:
        """Send the next daily tip via Telegram."""
        tip = self._get_next_unsent("daily_tips")

        if not tip:
            logger.info("No unsent daily tips - resetting queue")
            self.reset_queue("daily_tips")
            tip = self._get_next_unsent("daily_tips")

            if not tip:
                return {"ok": False, "error": "No tips in queue"}

        message = (
            f"{TELEGRAM_TEMPLATES['header']}"
            f"Sleep Tip of the Day\n\n"
            f"{tip['content']}\n\n"
            f"---\n"
            f"Add more tips using Claude Code!"
        )

        if self.telegram:
            result = self.telegram.send_message(message)
            if result.get("ok"):
                self._mark_as_sent("daily_tips", tip["id"])
                return {"ok": True, "tip_id": tip["id"]}
            return {"ok": False, "error": "Failed to send"}

        return {"ok": True, "tip": tip, "message": "No Telegram - preview mode"}

    def send_instagram_content(self) -> dict:
        """Send the next Instagram caption via Telegram."""
        caption = self._get_next_unsent("instagram_captions")

        if not caption:
            logger.info("No unsent Instagram captions - resetting queue")
            self.reset_queue("instagram_captions")
            caption = self._get_next_unsent("instagram_captions")

            if not caption:
                return {"ok": False, "error": "No captions in queue"}

        hashtags = " ".join(caption.get("hashtags", []))

        message = (
            f"{TELEGRAM_TEMPLATES['header']}"
            f"Instagram Content Ready!\n\n"
            f"Topic: {caption.get('topic', 'Sleep Tips')}\n"
            f"---\n"
            f"{caption['caption']}\n\n"
            f"{hashtags}\n"
            f"---\n"
            f"Product Link: {caption.get('product_link', 'N/A')}\n\n"
            f"Copy this to Instagram!"
        )

        if self.telegram:
            result = self.telegram.send_message(message)
            if result.get("ok"):
                self._mark_as_sent("instagram_captions", caption["id"])
                return {"ok": True, "caption_id": caption["id"]}
            return {"ok": False, "error": "Failed to send"}

        return {"ok": True, "caption": caption, "message": "No Telegram - preview mode"}

    def send_engagement_reminder(self) -> dict:
        """Send the next engagement reminder via Telegram."""
        reminder = self._get_next_unsent("engagement_messages")

        if not reminder:
            logger.info("No unsent engagement reminders - resetting queue")
            self.reset_queue("engagement_messages")
            reminder = self._get_next_unsent("engagement_messages")

            if not reminder:
                return {"ok": False, "error": "No reminders in queue"}

        message = (
            f"{TELEGRAM_TEMPLATES['header']}"
            f"Engagement Reminder\n\n"
            f"{reminder['message']}\n\n"
            f"Small daily actions = big results!"
        )

        if self.telegram:
            result = self.telegram.send_message(message)
            if result.get("ok"):
                self._mark_as_sent("engagement_messages", reminder["id"])
                return {"ok": True, "reminder_id": reminder["id"]}
            return {"ok": False, "error": "Failed to send"}

        return {"ok": True, "reminder": reminder, "message": "No Telegram - preview mode"}

    def send_weekly_task(self) -> dict:
        """Send today's weekly task if there is one."""
        today = datetime.now(timezone.utc).strftime("%A").lower()

        tasks = self.queue.get("weekly_tasks", [])
        for task in tasks:
            if task.get("day", "").lower() == today:
                message = (
                    f"{TELEGRAM_TEMPLATES['header']}"
                    f"Weekly Task: {today.title()}\n\n"
                    f"Task: {task['task']}\n\n"
                    f"Details: {task.get('details', 'No details')}\n\n"
                    f"Let's make this week count!"
                )

                if self.telegram:
                    return self.telegram.send_message(message)
                return {"ok": True, "task": task, "message": "No Telegram - preview mode"}

        return {"ok": True, "message": f"No weekly task for {today}"}

    # =========================================================================
    # Queue Management
    # =========================================================================

    def get_queue_status(self) -> dict:
        """Get status of all queues."""
        status = {}

        for queue_name in ["daily_tips", "instagram_captions", "engagement_messages"]:
            items = self.queue.get(queue_name, [])
            sent = sum(1 for item in items if item.get("sent", False))
            total = len(items)
            status[queue_name] = {
                "total": total,
                "sent": sent,
                "remaining": total - sent
            }

        return status

    def add_content(self, queue_name: str, content: dict) -> dict:
        """
        Add new content to a queue.

        Args:
            queue_name: Name of the queue
            content: Content dict with required fields

        Returns:
            Result dict
        """
        if queue_name not in self.queue:
            return {"ok": False, "error": f"Unknown queue: {queue_name}"}

        # Generate ID
        existing_ids = [item.get("id", "") for item in self.queue[queue_name]]
        prefix = queue_name[:3]
        new_id = f"{prefix}_{len(existing_ids) + 1:03d}"

        content["id"] = new_id
        content["sent"] = False

        self.queue[queue_name].append(content)
        self._save_queue()

        return {"ok": True, "id": new_id}


# =============================================================================
# Standalone test
# =============================================================================
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    sender = QueueSender()

    print("Queue Status:")
    print(json.dumps(sender.get_queue_status(), indent=2))

    print("\nNext daily tip (preview):")
    result = sender.send_daily_tip()
    print(json.dumps(result, indent=2))
