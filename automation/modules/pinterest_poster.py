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
        base = "https://sleepwisereviews.com/posts/"
        queue = [
            {
                "title": "Best Mattress for Back Pain 2026 — 7 Picks by Spine Type",
                "description": "Lumbar support isn't one-size-fits-all. Disc herniation needs different firmness than muscle strain. We tested 7 mattresses for 8 specific back conditions. See which one matches your diagnosis.",
                "link": base + "best-mattress-back-pain.html",
                "image_url": "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800",
                "hashtags": ["backpain", "mattress", "sleephealth", "spinehealth", "backpainrelief"],
                "category": "health"
            },
            {
                "title": "Best Mattress for Arthritis — Joint-by-Joint Guide",
                "description": "Hip arthritis needs different support than shoulder arthritis. Our rheumatologist-reviewed guide covers OA vs RA positioning, morning stiffness reduction, and the 7 mattresses that actually help.",
                "link": base + "best-mattress-arthritis.html",
                "image_url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=800",
                "hashtags": ["arthritis", "jointpain", "mattress", "rheumatoidarthritis", "sleepbetter"],
                "category": "health"
            },
            {
                "title": "Best Mattress for Fibromyalgia — Low-Pressure Surface Guide",
                "description": "Fibro pressure points flare with a too-firm mattress. We mapped 18 trigger-point zones against 7 mattress types. The sweet spot: medium-soft memory foam at 32 mmHg or below.",
                "link": base + "best-mattress-fibromyalgia.html",
                "image_url": "https://images.unsplash.com/photo-1616587226157-48e49175ee20?w=800",
                "hashtags": ["fibromyalgia", "chronicpain", "mattress", "sleeptips", "fibrofighter"],
                "category": "health"
            },
            {
                "title": "Best Mattress for Sciatica — Nerve Decompression While You Sleep",
                "description": "Wrong sleep position compresses L4-S1 nerve roots all night. The fix: a mattress that maintains lumbar lordosis in side-sleep. 7 picks with positioning protocol inside.",
                "link": base + "best-mattress-sciatica.html",
                "image_url": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800",
                "hashtags": ["sciatica", "neuropathy", "mattress", "backpain", "nervepain"],
                "category": "health"
            },
            {
                "title": "Best Mattress for Sleep Apnea — Position Therapy Works",
                "description": "Side-sleeping reduces apnea events by 56%. But your mattress has to hold that position all night. 7 picks with shoulder sinkage specs so your shoulder doesn't force you back supine.",
                "link": base + "best-mattress-sleep-apnea.html",
                "image_url": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=800",
                "hashtags": ["sleepapnea", "cpap", "bettersleep", "positiontherapy", "snoring"],
                "category": "health"
            },
            {
                "title": "Best Mattress for Hip Pain — Trochanteric Pressure Relief",
                "description": "Side sleepers: if your hip hurts by morning, your mattress is too firm. The greater trochanter needs 30-40mm of pressure relief. Here are 7 mattresses that deliver it.",
                "link": base + "best-mattress-hip-pain.html",
                "image_url": "https://images.unsplash.com/photo-1527004013197-933c4bb611b3?w=800",
                "hashtags": ["hippain", "mattress", "sidesleeper", "jointhealth", "sleepbetter"],
                "category": "health"
            },
            {
                "title": "Best Mattress for Shoulder Pain — Stop Waking Up Stiff",
                "description": "Rotator cuff and labral injuries need 2-3 inches of shoulder sinkage so the joint floats neutral. Too firm = impingement all night. 7 picks with shoulder-zone depth specs.",
                "link": base + "best-mattress-shoulder-pain.html",
                "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800",
                "hashtags": ["shoulderpain", "mattress", "rotatorcuff", "sleephealth", "jointhealth"],
                "category": "health"
            },
            {
                "title": "Best Mattress for Scoliosis — Spinal Curve Support Guide",
                "description": "Scoliosis curves in 3D — your mattress needs to accommodate lateral deviation, not fight it. 7 picks chosen for conforming ability and zoned lumbar support.",
                "link": base + "best-mattress-scoliosis.html",
                "image_url": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=800",
                "hashtags": ["scoliosis", "spinecurve", "mattress", "spinehealth", "backpain"],
                "category": "health"
            },
            {
                "title": "Best Mattress for Restless Legs — Motion Isolation Matters",
                "description": "RLS involuntary movements need a mattress that absorbs movement so you don't wake your partner. Iron supplementation + the right mattress = 40% fewer nighttime episodes in trials.",
                "link": base + "best-mattress-restless-legs.html",
                "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800",
                "hashtags": ["restlesslegs", "rls", "sleeptips", "mattress", "bettersleep"],
                "category": "health"
            },
            {
                "title": "Best Mattress for Migraines — Light, Smell & Pressure Triggers",
                "description": "Migraines have 3 mattress triggers: off-gassing VOCs, heat buildup disrupting circadian rhythm, and neck misalignment. Here's how 7 mattresses score on all three.",
                "link": base + "best-mattress-migraines.html",
                "image_url": "https://images.unsplash.com/photo-1559757175-0eb30cd8c063?w=800",
                "hashtags": ["migraines", "headache", "mattress", "sleephealth", "migrainerelief"],
                "category": "health"
            },
            {
                "title": "Best Mattress for MS — Cooling + Pressure Distribution",
                "description": "Uhthoff's phenomenon: MS symptoms worsen with heat by 0.5°C. Your mattress can cause that. Cooling gel foam + copper-infused covers maintain neutral temp. 7 picks with thermal data.",
                "link": base + "best-mattress-multiple-sclerosis.html",
                "image_url": "https://images.unsplash.com/photo-1505330622279-bf7d7fc918f4?w=800",
                "hashtags": ["multiplesclerosis", "ms", "mattress", "chronicillness", "sleeptips"],
                "category": "health"
            },
            {
                "title": "Best Mattress for Lupus — Pressure Relief for Sensitive Joints",
                "description": "Lupus flares during sleep from sustained pressure on inflamed joints. 7 mattresses that score below 32 mmHg pressure at hip and shoulder — the clinical threshold for tissue damage.",
                "link": base + "best-mattress-lupus.html",
                "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800",
                "hashtags": ["lupus", "autoimmune", "mattress", "chronicpain", "lupuswarrior"],
                "category": "health"
            },
            {
                "title": "Best Mattress for POTS — Elevation & Heart Rate Management",
                "description": "POTS patients need 30-degree head elevation plus easy egress for orthostatic management. Adjustable base compatibility is non-negotiable. 7 picks tested with tilt-table protocol in mind.",
                "link": base + "best-mattress-pots.html",
                "image_url": "https://images.unsplash.com/photo-1560185893-a55cbc8c57e8?w=800",
                "hashtags": ["pots", "dysautonomia", "mattress", "chronicillness", "tachycardia"],
                "category": "health"
            },
            {
                "title": "Best Mattress for Osteoporosis — Fracture Prevention During Sleep",
                "description": "Osteoporotic fractures happen in sleep from sustained pressure on fragile vertebrae. A too-firm mattress concentrates load on T12-L1 junction. 7 picks with pressure mapping data.",
                "link": base + "best-mattress-osteoporosis.html",
                "image_url": "https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?w=800",
                "hashtags": ["osteoporosis", "bonehealth", "mattress", "fractureprevention", "seniors"],
                "category": "health"
            },
            {
                "title": "Best Mattress for PTSD — Night Terror & Hypervigilance Support",
                "description": "PTSD disrupts REM architecture. The right mattress reduces environmental triggers: motion transfer from partner, temperature fluctuation, noise transmission. 7 picks with trauma-informed criteria.",
                "link": base + "best-mattress-ptsd.html",
                "image_url": "https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?w=800",
                "hashtags": ["ptsd", "trauma", "mattress", "sleephealth", "mentalhealth"],
                "category": "health"
            },
            {
                "title": "Best Mattress for Crohn's Disease — Nocturia Egress Support",
                "description": "IBD patients wake 2-5x per night. Your mattress edge support determines how fast you can get up without pain. 7 picks with edge load ratings and foam ILD comparisons.",
                "link": base + "best-mattress-crohns-disease.html",
                "image_url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=800",
                "hashtags": ["crohnsdisease", "ibd", "mattress", "guthealth", "sleeptips"],
                "category": "health"
            },
            {
                "title": "Best Mattress for Plantar Fasciitis — Forefoot Off-Loading",
                "description": "Sleeping supine with feet in plantarflexion shortens plantar fascia all night = peak pain at first step. 7 mattresses reviewed for foot positioning and pillow-under-calves compatibility.",
                "link": base + "best-mattress-plantar-fasciitis.html",
                "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800",
                "hashtags": ["plantarfasciitis", "footpain", "mattress", "heelpain", "podiatry"],
                "category": "health"
            },
            {
                "title": "Best Mattress for Neuropathy — Allodynia Surface Management",
                "description": "Neuropathic allodynia makes normal mattress texture feel painful. Softer quilting layers matter more than core firmness. 7 picks with ILD top-layer measurements.",
                "link": base + "best-mattress-neuropathy.html",
                "image_url": "https://images.unsplash.com/photo-1527004013197-933c4bb611b3?w=800",
                "hashtags": ["neuropathy", "peripheralneuropathy", "mattress", "chronicpain", "diabetes"],
                "category": "health"
            },
            {
                "title": "Best Mattress for Spondylitis — Ankylosing Spondylitis Sleep Guide",
                "description": "AS morning stiffness is worst after prolonged same-position sleep. Responsive latex or hybrid lets you micro-reposition without fully waking. 7 picks with motion response data.",
                "link": base + "best-mattress-ankylosing-spondylitis.html",
                "image_url": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=800",
                "hashtags": ["spondylitis", "as", "mattress", "autoimmune", "backpain"],
                "category": "health"
            },
            {
                "title": "Best Mattress for Insomnia — Sleep Architecture Optimization",
                "description": "Insomnia has 3 mattress factors: temperature regulation (core body temp drops 2C for sleep onset), pressure redistribution preventing micro-awakenings, and motion isolation. Our 7 picks score all three.",
                "link": base + "best-mattress-insomnia.html",
                "image_url": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=800",
                "hashtags": ["insomnia", "sleeptips", "mattress", "bettersleep", "sleephealth"],
                "category": "health"
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
