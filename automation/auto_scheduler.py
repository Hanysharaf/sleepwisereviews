"""
SleepWise Automation Agent - Main Auto Scheduler
Actually posts content and reports real links to Telegram.

Run modes:
- Post now: python auto_scheduler.py --post-pinterest
- Daily report: python auto_scheduler.py --daily-report
- Full auto: python auto_scheduler.py --run-now
- Continuous: python auto_scheduler.py --continuous
"""

import os
import sys
import json
import logging
import argparse
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict
import random

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from config import (
    SCHEDULE_CONFIG, DATA_DIR, CONTENT_CONFIG, TELEGRAM_TEMPLATES,
    PROJECT_ROOT, QUEUE_FILE, STATE_FILE, HISTORY_FILE
)
from modules.telegram_bot import TelegramBot
from modules.content_generator import ContentGenerator
from modules.instagram_prep import InstagramPrep
from modules.pinterest_poster import PinterestPoster
from modules.buffer_integration import BufferIntegration, MakeWebhook

# Configure logging
DATA_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(DATA_DIR / "automation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AutoScheduler:
    """Main automation scheduler that ACTUALLY posts and reports."""

    def __init__(self):
        """Initialize the scheduler with all modules."""
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        # Initialize modules
        self.telegram = TelegramBot()
        self.content_gen = ContentGenerator()
        self.instagram = InstagramPrep()
        self.pinterest = PinterestPoster()
        self.buffer = BufferIntegration()
        self.make = MakeWebhook()

        # Load state
        self.state = self._load_state()

    # ==========================================================================
    # State Management
    # ==========================================================================

    def _load_state(self) -> dict:
        """Load scheduler state from file."""
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
        return {
            "last_run": None,
            "posts_today": 0,
            "last_post_date": None,
            "total_posts": 0,
            "pinterest_posts": 0,
            "instagram_posts": 0
        }

    def _save_state(self):
        """Save scheduler state to file."""
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        self.state["last_run"] = datetime.now(timezone.utc).isoformat()
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2)

    def _log_task(self, task_name: str, result: dict):
        """Log task execution to history file."""
        history = []
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except json.JSONDecodeError:
                pass

        history.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "task": task_name,
            "success": result.get("ok", False),
            "details": result.get("details", ""),
            "url": result.get("pin_url") or result.get("post_url", "")
        })

        # Keep last 500 entries
        history = history[-500:]

        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)

    # ==========================================================================
    # ACTUAL POSTING TASKS
    # ==========================================================================

    def task_post_pinterest(self, count: int = 1) -> dict:
        """
        Actually post pins to Pinterest.
        Returns the real pin URLs.
        """
        results = []

        for i in range(count):
            result = self.pinterest.post_next_pin()

            if result.get("ok"):
                # Notify via Telegram with real URL
                self.telegram.notify_pin_posted(result)

                # Update state
                today = datetime.now().strftime("%Y-%m-%d")
                if self.state.get("last_post_date") != today:
                    self.state["posts_today"] = 0
                    self.state["last_post_date"] = today

                self.state["posts_today"] += 1
                self.state["total_posts"] += 1
                self.state["pinterest_posts"] = self.state.get("pinterest_posts", 0) + 1

                results.append(result)
                logger.info(f"Posted pin: {result.get('pin_url')}")
            else:
                logger.error(f"Failed to post pin: {result.get('error')}")
                break

            # Small delay between posts
            if i < count - 1:
                time.sleep(2)

        self._save_state()
        self._log_task("post_pinterest", {
            "ok": len(results) > 0,
            "details": f"Posted {len(results)} pins",
            "pins": results
        })

        return {"ok": len(results) > 0, "pins": results, "count": len(results)}

    def task_post_instagram(self) -> dict:
        """
        Post to Instagram via Buffer or prepare for manual posting.
        """
        pending = self.instagram.get_pending_posts()
        if not pending:
            # Generate new content
            result = self.task_generate_instagram_post()
            if not result.get("ok"):
                return {"ok": False, "error": "No content to post"}
            pending = self.instagram.get_pending_posts()

        if not pending:
            return {"ok": False, "error": "No content available"}

        post = pending[0]

        # Try Buffer first
        if self.buffer.access_token:
            # Need image URL for Buffer
            image_url = post.get("image_url", "")
            if image_url:
                result = self.buffer.schedule_instagram_post(
                    caption=post.get("full_caption", post.get("caption", "")),
                    image_url=image_url
                )
                if result.get("ok"):
                    self.instagram.mark_posted(post["id"])
                    self.telegram.notify_instagram_posted(post)
                    return {"ok": True, "post": post}

        # Fallback: Send to Telegram for manual posting
        self.telegram.send_instagram_ready(post)
        return {"ok": True, "post": post, "manual": True}

    def task_generate_instagram_post(self, topic: str = None) -> dict:
        """Generate new Instagram content."""
        if not self.content_gen.client:
            # Use pre-written content
            topics = [
                "weighted blankets help reduce anxiety",
                "magnesium glycinate for better sleep",
                "optimal bedroom temperature is 65-68F",
                "blue light blocks melatonin production",
                "white noise machines for deeper sleep"
            ]
            topic = random.choice(topics)

            caption = f"Sleep tip: {topic}\n\nFollow @sleepwisereviews for more tips!"
            hashtags = ["sleeptips", "bettersleep", "sleephealth", "wellness", "healthysleep"]

            result = self.instagram.prepare_post(caption=caption, hashtags=hashtags)
            return result

        # Use Claude API
        topic = topic or random.choice(CONTENT_CONFIG["topics"])
        result = self.content_gen.generate_instagram_caption(topic, style="engaging")

        if result.get("ok"):
            caption_data = result.get("caption_data", {})
            prep_result = self.instagram.prepare_post(
                caption=caption_data.get("caption", result.get("content", "")),
                hashtags=caption_data.get("suggested_hashtags", [])
            )
            return prep_result

        return {"ok": False, "error": "Failed to generate content"}

    # ==========================================================================
    # REPORTING TASKS - WITH REAL LINKS
    # ==========================================================================

    def task_daily_report(self) -> dict:
        """
        Send daily report with ACTUAL posted links.
        """
        # Get Pinterest stats with actual posts
        pinterest_stats = self.pinterest.get_stats()

        # Get Instagram stats
        ig_stats = self.instagram.get_posting_stats()

        stats = {
            # Pinterest - actual posts with URLs
            "pinterest_today": pinterest_stats.get("today_posts", []),
            "pinterest_week_count": pinterest_stats.get("pins_this_week", 0),
            "pinterest_queue": pinterest_stats.get("queue_remaining", 0),

            # Instagram
            "instagram_today": [],  # Will be populated when IG posting works
            "instagram_week_count": ig_stats.get("posted_this_week", 0),
            "instagram_queue": ig_stats.get("pending_count", 0),

            # Articles
            "articles_week_count": 0
        }

        result = self.telegram.send_daily_report_with_links(stats)
        self._log_task("daily_report", {"ok": result.get("ok"), "details": "Report sent"})

        return result

    def task_daily_tip(self) -> dict:
        """Send daily sleep tip."""
        tips = [
            "Keep your bedroom between 65-68F (18-20C) for optimal sleep.",
            "Stop using screens 1 hour before bed - blue light blocks melatonin by 50%.",
            "Try the 4-7-8 breathing: inhale 4s, hold 7s, exhale 8s. Repeat 4 times.",
            "No caffeine after 2pm - it has a 6-hour half-life in your system.",
            "Weighted blankets (10% body weight) reduce anxiety and improve sleep.",
            "Magnesium glycinate taken 1 hour before bed helps muscle relaxation.",
            "Consistent sleep schedule - same time daily, even weekends.",
            "Complete darkness is crucial. Even small lights disrupt melatonin.",
            "Cool shower before bed helps your body temperature drop for sleep.",
            "Exercise improves sleep, but finish 3+ hours before bedtime."
        ]

        day_of_year = datetime.now().timetuple().tm_yday
        tip = tips[day_of_year % len(tips)]

        result = self.telegram.notify_daily_tip(tip)
        self._log_task("daily_tip", {"ok": result.get("ok"), "details": tip[:50]})

        return result

    # ==========================================================================
    # MAIN AUTOMATION
    # ==========================================================================

    def run_full_automation(self) -> dict:
        """
        Run complete automation cycle:
        1. Post to Pinterest
        2. Prepare Instagram content
        3. Send daily report with links
        """
        results = {
            "pinterest": None,
            "instagram": None,
            "report": None
        }

        # Post 2-3 Pinterest pins
        pin_count = random.randint(2, 3)
        logger.info(f"Posting {pin_count} Pinterest pins...")
        results["pinterest"] = self.task_post_pinterest(count=pin_count)

        # Prepare Instagram content
        logger.info("Preparing Instagram content...")
        results["instagram"] = self.task_post_instagram()

        # Send daily report with actual links
        logger.info("Sending daily report...")
        results["report"] = self.task_daily_report()

        return results

    def run_scheduled_tasks(self) -> dict:
        """Run tasks for the current hour."""
        current_hour = datetime.now().strftime("%H:00")

        tasks_map = {
            "06:00": self.task_daily_tip,
            "08:00": lambda: self.task_post_pinterest(count=2),
            "12:00": self.task_post_instagram,
            "14:00": lambda: self.task_post_pinterest(count=2),
            "18:00": lambda: self.task_post_pinterest(count=1),
            "20:00": self.task_daily_report
        }

        task_func = tasks_map.get(current_hour)
        if task_func:
            logger.info(f"Running scheduled task for {current_hour}")
            return task_func()

        return {"ok": True, "message": f"No tasks scheduled for {current_hour}"}

    def run_continuous(self, interval_minutes: int = 60):
        """Run scheduler continuously."""
        logger.info(f"Starting continuous scheduler (interval: {interval_minutes} min)")

        self.telegram.send_message(
            "<b>SleepWise Automation Started!</b>\n\n"
            "Now running continuously.\n"
            "Will post Pinterest pins and send reports automatically."
        )

        last_hour_run = None

        try:
            while True:
                current_hour = datetime.now().strftime("%H:00")

                if current_hour != last_hour_run:
                    result = self.run_scheduled_tasks()
                    last_hour_run = current_hour
                    logger.info(f"Hour {current_hour} tasks completed")

                time.sleep(interval_minutes * 60)

        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
            self.telegram.send_message("<b>SleepWise Automation Stopped</b>")

    def get_status(self) -> dict:
        """Get current status."""
        pinterest_stats = self.pinterest.get_stats()
        ig_stats = self.instagram.get_posting_stats()

        return {
            "last_run": self.state.get("last_run"),
            "total_posts": self.state.get("total_posts", 0),
            "pinterest_posts": self.state.get("pinterest_posts", 0),
            "pinterest_today": pinterest_stats.get("pins_today", 0),
            "pinterest_queue": pinterest_stats.get("queue_remaining", 0),
            "instagram_pending": ig_stats.get("pending_count", 0),
            "telegram_configured": bool(self.telegram.bot_token),
            "claude_configured": bool(self.content_gen.client),
            "pinterest_api_configured": bool(self.pinterest.access_token)
        }


# =============================================================================
# CLI Interface
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="SleepWise Auto Scheduler")
    parser.add_argument("--post-pinterest", type=int, metavar="N",
                        help="Post N pins to Pinterest now")
    parser.add_argument("--post-instagram", action="store_true",
                        help="Prepare/post Instagram content")
    parser.add_argument("--daily-report", action="store_true",
                        help="Send daily report with links")
    parser.add_argument("--run-now", action="store_true",
                        help="Run full automation cycle")
    parser.add_argument("--continuous", action="store_true",
                        help="Run scheduler continuously")
    parser.add_argument("--interval", type=int, default=60,
                        help="Check interval in minutes")
    parser.add_argument("--status", action="store_true",
                        help="Show current status")
    parser.add_argument("--test-telegram", action="store_true",
                        help="Test Telegram connection")

    args = parser.parse_args()

    scheduler = AutoScheduler()

    if args.status:
        status = scheduler.get_status()
        print("\n=== SleepWise Automation Status ===")
        print(f"Last run: {status['last_run'] or 'Never'}")
        print(f"Total posts: {status['total_posts']}")
        print(f"Pinterest posts: {status['pinterest_posts']}")
        print(f"Pinterest today: {status['pinterest_today']}")
        print(f"Pinterest queue: {status['pinterest_queue']} pins ready")
        print(f"Instagram pending: {status['instagram_pending']}")
        print(f"\nIntegrations:")
        print(f"  Telegram: {'OK' if status['telegram_configured'] else 'NOT CONFIGURED'}")
        print(f"  Claude API: {'OK' if status['claude_configured'] else 'NOT CONFIGURED'}")
        print(f"  Pinterest API: {'OK' if status['pinterest_api_configured'] else 'Simulated'}")
        return

    if args.test_telegram:
        print("Testing Telegram connection...")
        if scheduler.telegram.test_connection():
            print("SUCCESS! Check Telegram for message.")
        else:
            print("FAILED. Check your .env file.")
        return

    if args.post_pinterest:
        print(f"Posting {args.post_pinterest} pins to Pinterest...")
        result = scheduler.task_post_pinterest(count=args.post_pinterest)
        if result.get("ok"):
            print(f"SUCCESS! Posted {result['count']} pins")
            for pin in result.get("pins", []):
                print(f"  - {pin.get('pin_url')}")
        else:
            print(f"Failed: {result.get('error')}")
        return

    if args.post_instagram:
        print("Preparing Instagram content...")
        result = scheduler.task_post_instagram()
        if result.get("ok"):
            print("SUCCESS! Check Telegram for content.")
        else:
            print(f"Failed: {result.get('error')}")
        return

    if args.daily_report:
        print("Sending daily report...")
        result = scheduler.task_daily_report()
        if result.get("ok"):
            print("SUCCESS! Check Telegram for report.")
        else:
            print(f"Failed: {result.get('error')}")
        return

    if args.run_now:
        print("Running full automation cycle...")
        results = scheduler.run_full_automation()
        print("\n=== Results ===")
        if results["pinterest"].get("ok"):
            print(f"Pinterest: Posted {results['pinterest']['count']} pins")
        if results["instagram"].get("ok"):
            print(f"Instagram: Content prepared")
        if results["report"].get("ok"):
            print(f"Report: Sent to Telegram")
        return

    if args.continuous:
        scheduler.run_continuous(args.interval)
        return

    # Default: run scheduled tasks for current hour
    print(f"Running scheduled tasks for {datetime.now().strftime('%H:00')}...")
    result = scheduler.run_scheduled_tasks()
    print(f"Result: {result.get('message', 'Tasks completed')}")


if __name__ == "__main__":
    main()
