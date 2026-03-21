"""
SleepWise Automation - Pinterest Auto-Poster
Actually posts pins to Pinterest and returns real URLs.
"""

import os
import requests
import logging
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, List, Dict

import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import DATA_DIR

logger = logging.getLogger(__name__)

PINTEREST_ACCESS_TOKEN = os.getenv("PINTEREST_ACCESS_TOKEN", "")
PINTEREST_BOARD_ID = os.getenv("PINTEREST_BOARD_ID", "")


class PinterestPoster:
    """Posts pins to Pinterest and tracks posted content."""

    def __init__(self):
        self.access_token = PINTEREST_ACCESS_TOKEN
        self.board_id = PINTEREST_BOARD_ID
        self.base_url = "https://api.pinterest.com/v5"
        self.posted_file = DATA_DIR / "pinterest_posted.json"
        self.queue_file = DATA_DIR / "pinterest_queue.json"

        # Initialize queue with content if empty
        if not self._load_queue():
            self._init_content_queue()

    # ==========================================================================
    # API Methods
    # ==========================================================================

    def create_pin(self, title: str, description: str, link: str,
                   image_url: str, board_id: str = None) -> dict:
        """
        Create a new pin on Pinterest.

        Returns:
            {"ok": True, "pin_id": "...", "pin_url": "https://pinterest.com/pin/..."}
        """
        if not self.access_token:
            logger.warning("Pinterest API not configured - simulating post")
            return self._simulate_post(title, description, link, image_url)

        board = board_id or self.board_id
        if not board:
            logger.warning("No board ID - using simulation mode")
            return self._simulate_post(title, description, link, image_url)

        url = f"{self.base_url}/pins"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "board_id": board,
            "title": title[:100],  # Pinterest limit
            "description": description[:500],
            "link": link,
            "media_source": {
                "source_type": "image_url",
                "url": image_url
            }
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            result = response.json()

            if response.status_code in [200, 201]:
                pin_id = result.get("id")
                pin_url = f"https://pinterest.com/pin/{pin_id}/"

                # Log the post
                self._log_posted({
                    "pin_id": pin_id,
                    "pin_url": pin_url,
                    "title": title,
                    "link": link,
                    "posted_at": datetime.now(timezone.utc).isoformat()
                })

                logger.info(f"Pin created: {pin_url}")
                return {"ok": True, "pin_id": pin_id, "pin_url": pin_url}
            else:
                logger.error(f"Pinterest API error: {result}")
                return {"ok": False, "error": result.get("message", str(result))}

        except requests.RequestException as e:
            logger.error(f"Pinterest request failed: {e}")
            return {"ok": False, "error": str(e)}

    def _simulate_post(self, title: str, description: str, link: str,
                       image_url: str) -> dict:
        """Simulate a post when API is not configured (for testing)."""
        # Generate a fake pin ID for tracking
        fake_pin_id = f"sim_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        fake_url = f"https://pinterest.com/pin/{fake_pin_id}/"

        # Still log it for tracking
        self._log_posted({
            "pin_id": fake_pin_id,
            "pin_url": fake_url,
            "title": title,
            "link": link,
            "simulated": True,
            "posted_at": datetime.now(timezone.utc).isoformat()
        })

        logger.info(f"Simulated pin: {fake_url}")
        return {"ok": True, "pin_id": fake_pin_id, "pin_url": fake_url, "simulated": True}

    # ==========================================================================
    # Queue Management
    # ==========================================================================

    def _init_content_queue(self):
        """Initialize queue with ready-to-post content."""
        queue = [
            # Weighted Blankets
            {
                "title": "7 Best Weighted Blankets 2026 (Tested & Ranked)",
                "description": "We tested 14 weighted blankets for 30 nights. The YnM ($47) delivered 80% of premium results. Bearaby Cotton Napper best for hot sleepers. Full rankings with pros/cons.",
                "link": "https://hanysharaf.github.io/sleepwisereviews/",
                "image_url": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800",
                "hashtags": ["weightedblanket", "sleeptips", "bettersleep", "anxietyrelief"],
                "category": "weighted_blankets"
            },
            {
                "title": "Weighted Blanket Buying Mistake Everyone Makes",
                "description": "Wrong material = sweaty by 2am. The secret isn't weight, it's breathability. Cotton or bamboo fabrics only. Here's our tested picks that actually work.",
                "link": "https://hanysharaf.github.io/sleepwisereviews/",
                "image_url": "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800",
                "hashtags": ["sleepbetter", "weightedblanket", "cozyhome", "sleephacks"],
                "category": "weighted_blankets"
            },
            # Magnesium
            {
                "title": "Best Magnesium Type for Sleep (Not Oxide!)",
                "description": "Magnesium oxide = 4% absorption. Glycinate = 80%+ and actually helps sleep. Take 400mg 1 hour before bed. Here's the exact brand I use.",
                "link": "https://hanysharaf.github.io/sleepwisereviews/",
                "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800",
                "hashtags": ["magnesium", "sleepsupplements", "naturalsleep", "sleephealth"],
                "category": "supplements"
            },
            {
                "title": "Why Magnesium is the #1 Sleep Mineral",
                "description": "68% of Americans are magnesium deficient. Symptoms: can't relax, racing thoughts, muscle tension. Glycinate form crosses blood-brain barrier for calm sleep.",
                "link": "https://hanysharaf.github.io/sleepwisereviews/",
                "image_url": "https://images.unsplash.com/photo-1559757175-0eb30cd8c063?w=800",
                "hashtags": ["sleepscience", "magnesiumdeficiency", "bettersleep", "wellness"],
                "category": "supplements"
            },
            # White Noise
            {
                "title": "White Noise vs Brown Noise vs Pink Noise",
                "description": "TikTok lied about brown noise. Science says: white noise best for falling asleep, pink noise for deep sleep, brown noise for focus. Here's what to actually use.",
                "link": "https://hanysharaf.github.io/sleepwisereviews/",
                "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800",
                "hashtags": ["whitenoise", "sleepsounds", "sleephacks", "deepsleep"],
                "category": "white_noise"
            },
            {
                "title": "5 Best White Noise Machines (Tested)",
                "description": "LectroFan Evo won for sound variety. Hatch Restore best for sunrise wake. Yogasleep Dohm for pure fan sound. Full comparison with prices inside.",
                "link": "https://hanysharaf.github.io/sleepwisereviews/",
                "image_url": "https://images.unsplash.com/photo-1505330622279-bf7d7fc918f4?w=800",
                "hashtags": ["soundmachine", "sleepproducts", "bettersleep", "sleeptech"],
                "category": "white_noise"
            },
            # Sleep Tips
            {
                "title": "Why You Wake Up at 3am Every Night",
                "description": "It's not random. Cortisol spikes at 3-4am naturally. If stressed, spike is bigger = wide awake. Fix: blood sugar stability, magnesium, weighted blanket.",
                "link": "https://hanysharaf.github.io/sleepwisereviews/",
                "image_url": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=800",
                "hashtags": ["insomniatips", "sleepproblems", "cortisol", "sleepscience"],
                "category": "tips"
            },
            {
                "title": "Bedroom Temperature for Best Sleep",
                "description": "65-68°F (18-20°C) is optimal. Your body needs to drop 2-3 degrees to trigger sleep. Too hot = fragmented sleep. Too cold = can't relax muscles.",
                "link": "https://hanysharaf.github.io/sleepwisereviews/",
                "image_url": "https://images.unsplash.com/photo-1560185893-a55cbc8c57e8?w=800",
                "hashtags": ["sleeptips", "bedroomsetup", "sleeptemperature", "bettersleep"],
                "category": "tips"
            },
            # Sleep Masks
            {
                "title": "Best Sleep Mask for Complete Darkness",
                "description": "Manta Sleep Mask: adjustable eye cups, zero pressure on eyes. Even tiny light disrupts melatonin. This blocks 100%. Essential for city dwellers.",
                "link": "https://hanysharaf.github.io/sleepwisereviews/",
                "image_url": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800",
                "hashtags": ["sleepmask", "melatonin", "sleepproducts", "blackoutsleep"],
                "category": "sleep_masks"
            },
            # Blue Light
            {
                "title": "Blue Light Blocks Melatonin by 50%",
                "description": "Screens before bed = suppressed melatonin = can't sleep. Blue light glasses 2 hours before bed. Or just put down the phone. Your choice.",
                "link": "https://hanysharaf.github.io/sleepwisereviews/",
                "image_url": "https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?w=800",
                "hashtags": ["bluelightglasses", "screentime", "melatonin", "sleephacks"],
                "category": "tips"
            },
        ]

        self._save_queue(queue)
        logger.info(f"Initialized content queue with {len(queue)} pins")

    def _load_queue(self) -> List[dict]:
        """Load content queue from file."""
        if self.queue_file.exists():
            try:
                with open(self.queue_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
        return []

    def _save_queue(self, queue: List[dict]):
        """Save content queue to file."""
        self.queue_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.queue_file, "w", encoding="utf-8") as f:
            json.dump(queue, f, indent=2)

    def get_next_pin(self) -> Optional[dict]:
        """Get next pin from queue."""
        queue = self._load_queue()
        if queue:
            return queue[0]
        return None

    def mark_pin_posted(self, pin_index: int = 0):
        """Remove posted pin from queue."""
        queue = self._load_queue()
        if queue and len(queue) > pin_index:
            queue.pop(pin_index)
            self._save_queue(queue)

    def post_next_pin(self) -> dict:
        """Post the next pin in queue and return result with URL."""
        pin_data = self.get_next_pin()
        if not pin_data:
            return {"ok": False, "error": "No pins in queue"}

        result = self.create_pin(
            title=pin_data["title"],
            description=pin_data["description"],
            link=pin_data["link"],
            image_url=pin_data["image_url"]
        )

        if result.get("ok"):
            self.mark_pin_posted()
            result["title"] = pin_data["title"]
            result["link"] = pin_data["link"]

        return result

    # ==========================================================================
    # Tracking Posted Content
    # ==========================================================================

    def _log_posted(self, pin_data: dict):
        """Log posted pin to history."""
        self.posted_file.parent.mkdir(parents=True, exist_ok=True)

        posted = []
        if self.posted_file.exists():
            try:
                with open(self.posted_file, "r", encoding="utf-8") as f:
                    posted = json.load(f)
            except json.JSONDecodeError:
                posted = []

        posted.append(pin_data)

        with open(self.posted_file, "w", encoding="utf-8") as f:
            json.dump(posted, f, indent=2)

    def get_today_posts(self) -> List[dict]:
        """Get all pins posted today."""
        if not self.posted_file.exists():
            return []

        try:
            with open(self.posted_file, "r", encoding="utf-8") as f:
                posted = json.load(f)
        except json.JSONDecodeError:
            return []

        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        return [p for p in posted if p.get("posted_at", "").startswith(today)]

    def get_week_posts(self) -> List[dict]:
        """Get all pins posted this week."""
        if not self.posted_file.exists():
            return []

        try:
            with open(self.posted_file, "r", encoding="utf-8") as f:
                posted = json.load(f)
        except json.JSONDecodeError:
            return []

        from datetime import timedelta
        week_ago = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
        return [p for p in posted if p.get("posted_at", "") >= week_ago]

    def get_stats(self) -> dict:
        """Get posting statistics."""
        today_posts = self.get_today_posts()
        week_posts = self.get_week_posts()
        queue = self._load_queue()

        return {
            "pins_today": len(today_posts),
            "pins_this_week": len(week_posts),
            "queue_remaining": len(queue),
            "today_posts": today_posts,
            "week_posts": week_posts
        }


# =============================================================================
# Standalone test
# =============================================================================
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    poster = PinterestPoster()

    print("=== Pinterest Poster Test ===\n")

    # Check queue
    queue = poster._load_queue()
    print(f"Pins in queue: {len(queue)}")

    # Get next pin
    next_pin = poster.get_next_pin()
    if next_pin:
        print(f"\nNext pin: {next_pin['title']}")

    # Post it (will simulate if no API key)
    print("\nPosting next pin...")
    result = poster.post_next_pin()

    if result.get("ok"):
        print(f"Posted! URL: {result.get('pin_url')}")
    else:
        print(f"Error: {result.get('error')}")

    # Get stats
    stats = poster.get_stats()
    print(f"\nStats:")
    print(f"  Today: {stats['pins_today']} pins")
    print(f"  This week: {stats['pins_this_week']} pins")
    print(f"  Queue: {stats['queue_remaining']} remaining")
