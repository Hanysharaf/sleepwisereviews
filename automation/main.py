"""
SleepWise Automation Agent - Main Entry Point
Orchestrates all automation tasks based on schedule.
"""

import logging
import json
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, List

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import (
    SCHEDULE_CONFIG, STATE_FILE, HISTORY_FILE, DATA_DIR,
    validate_config, get_current_hour, get_current_day,
    is_github_actions
)
from modules import (
    TelegramReporter,
    ContentGenerator,
    WebsiteManager,
    InstagramPrep,
    QueueSender,
    PinterestPoster
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("SleepWiseAgent")


class SleepWiseAgent:
    """Main automation agent that orchestrates all tasks."""

    def __init__(self):
        """Initialize the agent and all modules."""
        logger.info("Initializing SleepWise Agent...")

        # Initialize modules
        self.telegram = TelegramReporter()
        self.content = ContentGenerator()
        self.website = WebsiteManager()
        self.instagram = InstagramPrep()
        self.pinterest = PinterestPoster()

        # Initialize queue sender (NO API credits needed!)
        self.queue = QueueSender(telegram_reporter=self.telegram)

        # Load state
        self.state = self._load_state()
        self.history = self._load_history()

        # Ensure data directory exists
        DATA_DIR.mkdir(parents=True, exist_ok=True)

    # ==========================================================================
    # State Management
    # ==========================================================================

    def _load_state(self) -> dict:
        """Load agent state from file."""
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.warning("Could not parse state file, using defaults")

        return {
            "last_run": None,
            "pins_today": 0,
            "pins_this_week": 0,
            "articles_this_week": 0,
            "ig_posts_prepared": 0,
            "last_article_date": None,
            "last_pin_date": None,
            "errors_today": 0,
            "week_start": datetime.now(timezone.utc).strftime("%Y-%m-%d")
        }

    def _save_state(self):
        """Save agent state to file."""
        self.state["last_run"] = datetime.now(timezone.utc).isoformat()
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2)
        logger.debug("State saved")

    def _load_history(self) -> List[dict]:
        """Load task history from file."""
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def _add_to_history(self, task: str, result: dict):
        """Add task execution to history."""
        self.history.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "task": task,
            "success": result.get("ok", False),
            "details": result.get("details", "")
        })

        # Keep only last 100 entries
        self.history = self.history[-100:]

        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=2)

    def _reset_daily_counters(self):
        """Reset daily counters if it's a new day."""
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        last_run = self.state.get("last_run", "")

        if last_run and not last_run.startswith(today):
            logger.info("New day detected, resetting daily counters")
            self.state["pins_today"] = 0
            self.state["errors_today"] = 0

    def _reset_weekly_counters(self):
        """Reset weekly counters if it's a new week."""
        today = datetime.now(timezone.utc)
        week_start = self.state.get("week_start", "")

        if today.weekday() == 0:  # Monday
            if week_start != today.strftime("%Y-%m-%d"):
                logger.info("New week detected, resetting weekly counters")
                self.state["pins_this_week"] = 0
                self.state["articles_this_week"] = 0
                self.state["week_start"] = today.strftime("%Y-%m-%d")

    # ==========================================================================
    # Task Execution
    # ==========================================================================

    def run(self):
        """Main entry point - determine and execute current task."""
        logger.info("=" * 50)
        logger.info("SleepWise Agent Starting")
        logger.info("=" * 50)

        # Validate configuration
        config_check = validate_config()
        if not config_check["valid"]:
            logger.error(f"Configuration issues: {config_check['issues']}")
            self.telegram.send_error_report(
                f"Configuration issues: {', '.join(config_check['issues'])}",
                "startup"
            )
            return

        # Reset counters if needed
        self._reset_daily_counters()
        self._reset_weekly_counters()

        # Determine current task
        current_hour = get_current_hour()
        current_day = get_current_day()

        logger.info(f"Current time: {current_hour}:00 UTC, Day: {current_day}")

        # Map hour to task
        hour_key = f"{current_hour:02d}:00"
        task = SCHEDULE_CONFIG["tasks"].get(hour_key)

        # Check for weekly tasks
        weekly_tasks = SCHEDULE_CONFIG["weekly_tasks"].get(current_day, [])

        # Execute scheduled task
        if task:
            logger.info(f"Executing scheduled task: {task}")
            self._execute_task(task)

        # Execute weekly tasks (on Sundays at specific hours)
        if current_day == "sunday" and current_hour == 12:
            for weekly_task in weekly_tasks:
                logger.info(f"Executing weekly task: {weekly_task}")
                self._execute_task(weekly_task)

        # Save state
        self._save_state()

        logger.info("=" * 50)
        logger.info("SleepWise Agent Complete")
        logger.info("=" * 50)

    def _execute_task(self, task: str):
        """
        Execute a specific task.

        Args:
            task: Task identifier
        """
        try:
            if task == "pinterest_pin":
                # Actually post to Pinterest and track URLs
                result = self._task_post_pinterest()
            elif task == "content_prep":
                # Use queue-based content (NO API credits needed!)
                result = self._task_content_prep_from_queue()
            elif task == "instagram_notify":
                # Use queue-based Instagram content (NO API credits needed!)
                result = self._task_instagram_from_queue()
            elif task == "engagement_tips":
                # Use queue-based engagement tips (NO API credits needed!)
                result = self._task_engagement_from_queue()
            elif task == "daily_summary":
                result = self._task_daily_summary()
            elif task == "daily_tip":
                # Send daily tip from queue
                result = self._task_daily_tip_from_queue()
            elif task == "weekly_task":
                # Send weekly task reminder
                result = self._task_weekly_from_queue()
            elif task == "generate_article":
                result = self._task_generate_article()
            else:
                logger.warning(f"Unknown task: {task}")
                result = {"ok": False, "error": f"Unknown task: {task}"}

            self._add_to_history(task, result)

        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            self.state["errors_today"] += 1
            self.telegram.send_error_report(str(e), task)
            self._add_to_history(task, {"ok": False, "error": str(e)})

    # ==========================================================================
    # Individual Tasks
    # ==========================================================================

    def _task_content_prep(self) -> dict:
        """Prepare content for social media."""
        logger.info("Executing content preparation task")

        # Generate Instagram caption for upcoming post
        topic = self.content.select_random_topic()
        result = self.content.generate_instagram_caption(
            topic=topic,
            style="engaging"
        )

        if result.get("ok"):
            caption_data = result.get("caption_data", {})

            # Prepare Instagram post
            self.instagram.prepare_post(
                caption=caption_data.get("caption", ""),
                hashtags=caption_data.get("suggested_hashtags", [])
            )

            self.state["ig_posts_prepared"] += 1

            return {
                "ok": True,
                "details": f"Content prepared for topic: {topic}"
            }

        return {"ok": False, "error": "Failed to generate content"}

    def _task_instagram_notify(self) -> dict:
        """Send notification about ready Instagram content."""
        logger.info("Executing Instagram notification task")

        # Get pending posts
        pending = self.instagram.get_pending_posts()

        if not pending:
            logger.info("No pending Instagram posts")
            return {"ok": True, "details": "No pending posts"}

        # Send the first pending post
        post = pending[0]
        message = self.instagram.format_for_telegram(post)

        # Send with image if available
        if post.get("image_path") and Path(post["image_path"]).exists():
            self.telegram.send_photo(post["image_path"], message[:1024])
        else:
            self.telegram.send_message(message)

        return {
            "ok": True,
            "details": f"Instagram notification sent for post {post.get('id')}"
        }

    def _task_engagement_tips(self) -> dict:
        """Send engagement tips via Telegram."""
        logger.info("Executing engagement tips task")

        result = self.telegram.send_engagement_tips()
        return {
            "ok": result.get("ok", False),
            "details": "Engagement tips sent"
        }

    # ==========================================================================
    # Queue-Based Tasks (NO API CREDITS NEEDED!)
    # Content is pre-written using Claude Code sessions
    # ==========================================================================

    def _task_content_prep_from_queue(self) -> dict:
        """Send content from the pre-written queue."""
        logger.info("Executing queue-based content prep (no API needed)")

        # Send daily tip
        result = self.queue.send_daily_tip()
        return {
            "ok": result.get("ok", False),
            "details": f"Daily tip sent from queue: {result.get('tip_id', 'N/A')}"
        }

    def _task_instagram_from_queue(self) -> dict:
        """Send Instagram content from the pre-written queue."""
        logger.info("Executing queue-based Instagram content (no API needed)")

        result = self.queue.send_instagram_content()
        return {
            "ok": result.get("ok", False),
            "details": f"Instagram content sent: {result.get('caption_id', 'N/A')}"
        }

    def _task_engagement_from_queue(self) -> dict:
        """Send engagement reminder from the pre-written queue."""
        logger.info("Executing queue-based engagement tips (no API needed)")

        result = self.queue.send_engagement_reminder()
        return {
            "ok": result.get("ok", False),
            "details": f"Engagement reminder sent: {result.get('reminder_id', 'N/A')}"
        }

    def _task_daily_tip_from_queue(self) -> dict:
        """Send daily sleep tip from queue."""
        logger.info("Executing daily tip from queue (no API needed)")

        result = self.queue.send_daily_tip()
        return {
            "ok": result.get("ok", False),
            "details": f"Daily tip sent: {result.get('tip_id', 'N/A')}"
        }

    def _task_weekly_from_queue(self) -> dict:
        """Send weekly task reminder from queue."""
        logger.info("Executing weekly task from queue (no API needed)")

        result = self.queue.send_weekly_task()
        return {
            "ok": result.get("ok", False),
            "details": "Weekly task sent"
        }

    def _task_post_pinterest(self, count: int = 2) -> dict:
        """Actually post pins to Pinterest and notify via Telegram."""
        logger.info(f"Executing Pinterest posting task ({count} pins)")

        results = []
        for i in range(count):
            result = self.pinterest.post_next_pin()

            if result.get("ok"):
                # Notify via Telegram with real URL
                self.telegram.send_pin_posted(result)

                # Update state
                self.state["pins_today"] = self.state.get("pins_today", 0) + 1
                self.state["pins_this_week"] = self.state.get("pins_this_week", 0) + 1
                self.state["last_pin_date"] = datetime.now(timezone.utc).isoformat()

                results.append(result)
                logger.info(f"Posted pin: {result.get('pin_url')}")
            else:
                logger.warning(f"Failed to post pin: {result.get('error')}")
                break

        return {
            "ok": len(results) > 0,
            "details": f"Posted {len(results)} pins to Pinterest",
            "pins": results
        }

    def _task_daily_summary(self) -> dict:
        """Send daily summary report WITH actual posted links."""
        logger.info("Executing daily summary task")

        # Get Pinterest stats with actual posted URLs
        pinterest_stats = self.pinterest.get_stats()

        stats = {
            # Pinterest - with actual URLs
            "pinterest_today": pinterest_stats.get("today_posts", []),
            "pins_today": len(pinterest_stats.get("today_posts", [])),
            "pinterest_queue": pinterest_stats.get("queue_remaining", 0),

            # Instagram
            "ig_prepared": self.state.get("ig_posts_prepared", 0),
            "ig_week": self.instagram.get_posting_stats().get("posted_this_week", 0),

            # Articles
            "articles_today": 0,
            "pins_week": self.state.get("pins_this_week", 0),
            "articles_week": self.state.get("articles_this_week", 0)
        }

        # Use the new method that includes actual links
        result = self.telegram.send_daily_summary_with_links(stats)
        return {
            "ok": result.get("ok", False),
            "details": "Daily summary with links sent"
        }

    def _task_generate_article(self) -> dict:
        """Generate a new article for the website."""
        logger.info("Executing article generation task")

        # Select topic and type
        topic = self.content.select_random_topic()
        content_type = self.content.select_random_content_type()

        logger.info(f"Generating {content_type} article about: {topic}")

        # Generate article
        result = self.content.generate_article(topic, content_type)

        if not result.get("ok"):
            return {"ok": False, "error": "Failed to generate article content"}

        article_data = result.get("article", {})

        if not article_data or "title" not in article_data:
            return {"ok": False, "error": "Invalid article data generated"}

        # Create the article file
        create_result = self.website.create_article(article_data)

        if create_result.get("ok"):
            self.state["articles_this_week"] += 1
            self.state["last_article_date"] = datetime.now(timezone.utc).isoformat()

            # Notify via Telegram
            self.telegram.send_article_notification(
                title=article_data.get("title", "New Article"),
                url=create_result.get("url", "")
            )

            # Prepare Instagram post from article
            self.instagram.prepare_from_article({
                "title": article_data.get("title"),
                "introduction": article_data.get("introduction"),
                "keywords": article_data.get("keywords", []),
                "url": create_result.get("url")
            })

            return {
                "ok": True,
                "details": f"Article created: {article_data.get('title')}"
            }

        return create_result

    # ==========================================================================
    # Manual Triggers
    # ==========================================================================

    def manual_generate_article(self, topic: str = None) -> dict:
        """Manually trigger article generation."""
        if topic:
            # Use provided topic
            result = self.content.generate_article(topic)
            if result.get("ok"):
                article_data = result.get("article", {})
                return self.website.create_article(article_data)
        return self._task_generate_article()

    def test_connections(self) -> dict:
        """Test all API connections."""
        results = {
            "telegram": self.telegram.test_connection(),
            "claude": self.content.test_connection()
        }

        all_ok = all(results.values())
        logger.info(f"Connection tests: {results}")

        if all_ok:
            self.telegram.send_startup_report()

        return {"ok": all_ok, "results": results}


# =============================================================================
# Entry Point
# =============================================================================

def main():
    """Main entry point for the automation agent."""
    agent = SleepWiseAgent()

    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "test":
            results = agent.test_connections()
            print(f"Connection test results: {results}")

        elif command == "article":
            # Check environment variable first (from Telegram bot), then command line
            import os
            topic = os.getenv("ARTICLE_TOPIC") or (sys.argv[2] if len(sys.argv) > 2 else None)
            if topic:
                logger.info(f"Generating article with topic: {topic}")
            result = agent.manual_generate_article(topic)
            print(f"Article generation result: {result}")

        elif command == "summary":
            result = agent._task_daily_summary()
            print(f"Summary sent: {result}")

        elif command == "content_prep":
            result = agent._task_content_prep()
            print(f"Content prep result: {result}")

        elif command == "instagram_notify":
            result = agent._task_instagram_notify()
            print(f"Instagram notify result: {result}")

        elif command == "engagement_tips":
            result = agent._task_engagement_tips()
            print(f"Engagement tips result: {result}")

        else:
            print(f"Unknown command: {command}")
            print("Available commands: test, article, summary, content_prep, instagram_notify, engagement_tips")
    else:
        # Normal scheduled run
        agent.run()


if __name__ == "__main__":
    main()
