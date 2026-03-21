"""
SleepWise Automation Agent - Buffer Integration
Auto-posts to social media via Buffer API.

Buffer Pricing: $6/month (Essentials) - 1 channel, unlimited posts
Alternative: Use free tier with manual queue management
"""

import requests
import logging
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict

import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import DATA_DIR

logger = logging.getLogger(__name__)

# Get Buffer token from environment
import os
BUFFER_ACCESS_TOKEN = os.getenv("BUFFER_ACCESS_TOKEN", "")


class BufferIntegration:
    """Handles auto-posting via Buffer API."""

    def __init__(self, access_token: str = None):
        """
        Initialize Buffer integration.

        Args:
            access_token: Buffer API access token
        """
        self.access_token = access_token or BUFFER_ACCESS_TOKEN
        self.base_url = "https://api.bufferapp.com/1"
        self.profiles = {}
        self.queue_file = DATA_DIR / "buffer_queue.json"

    # ==========================================================================
    # Authentication & Setup
    # ==========================================================================

    def get_profiles(self) -> dict:
        """
        Get all connected social media profiles.

        Returns:
            List of profile data
        """
        if not self.access_token:
            return {"ok": False, "error": "Buffer access token not configured"}

        url = f"{self.base_url}/profiles.json"
        params = {"access_token": self.access_token}

        try:
            response = requests.get(url, params=params, timeout=30)
            result = response.json()

            if isinstance(result, list):
                self.profiles = {p["service"]: p for p in result}
                return {"ok": True, "profiles": result}
            else:
                return {"ok": False, "error": result.get("error", "Unknown error")}

        except requests.RequestException as e:
            logger.error(f"Buffer API error: {e}")
            return {"ok": False, "error": str(e)}

    def get_profile_id(self, service: str) -> Optional[str]:
        """Get profile ID for a specific service (instagram, pinterest, etc.)."""
        if not self.profiles:
            self.get_profiles()
        profile = self.profiles.get(service)
        return profile["id"] if profile else None

    # ==========================================================================
    # Posting
    # ==========================================================================

    def create_update(self, profile_ids: List[str], text: str,
                      media: List[dict] = None, scheduled_at: datetime = None,
                      now: bool = False) -> dict:
        """
        Create a new post/update.

        Args:
            profile_ids: List of Buffer profile IDs to post to
            text: Post text/caption
            media: List of media objects [{"link": "url", "photo": "url"}]
            scheduled_at: When to post (None = add to queue)
            now: Post immediately if True

        Returns:
            API response
        """
        if not self.access_token:
            return {"ok": False, "error": "Buffer access token not configured"}

        url = f"{self.base_url}/updates/create.json"

        data = {
            "access_token": self.access_token,
            "text": text,
            "profile_ids[]": profile_ids
        }

        if media:
            for i, m in enumerate(media):
                if m.get("link"):
                    data[f"media[link]"] = m["link"]
                if m.get("photo"):
                    data[f"media[photo]"] = m["photo"]
                if m.get("thumbnail"):
                    data[f"media[thumbnail]"] = m["thumbnail"]

        if now:
            data["now"] = "true"
        elif scheduled_at:
            data["scheduled_at"] = int(scheduled_at.timestamp())

        try:
            response = requests.post(url, data=data, timeout=30)
            result = response.json()

            if result.get("success"):
                logger.info(f"Buffer update created: {result.get('updates', [{}])[0].get('id')}")
                return {"ok": True, "updates": result.get("updates", [])}
            else:
                logger.error(f"Buffer error: {result.get('message')}")
                return {"ok": False, "error": result.get("message", "Unknown error")}

        except requests.RequestException as e:
            logger.error(f"Buffer request failed: {e}")
            return {"ok": False, "error": str(e)}

    def schedule_instagram_post(self, caption: str, image_url: str,
                                scheduled_at: datetime = None) -> dict:
        """
        Schedule an Instagram post.

        Args:
            caption: Post caption with hashtags
            image_url: URL to the image (must be publicly accessible)
            scheduled_at: When to post

        Returns:
            API response
        """
        profile_id = self.get_profile_id("instagram")
        if not profile_id:
            return {"ok": False, "error": "Instagram profile not connected to Buffer"}

        media = [{"photo": image_url}]

        return self.create_update(
            profile_ids=[profile_id],
            text=caption,
            media=media,
            scheduled_at=scheduled_at
        )

    def schedule_pinterest_pin(self, description: str, image_url: str,
                               link_url: str, board_id: str = None,
                               scheduled_at: datetime = None) -> dict:
        """
        Schedule a Pinterest pin.

        Args:
            description: Pin description
            image_url: URL to the pin image
            link_url: Link when pin is clicked
            board_id: Pinterest board ID (optional)
            scheduled_at: When to post

        Returns:
            API response
        """
        profile_id = self.get_profile_id("pinterest")
        if not profile_id:
            return {"ok": False, "error": "Pinterest profile not connected to Buffer"}

        media = [{"photo": image_url, "link": link_url}]

        return self.create_update(
            profile_ids=[profile_id],
            text=description,
            media=media,
            scheduled_at=scheduled_at
        )

    # ==========================================================================
    # Queue Management
    # ==========================================================================

    def get_pending_updates(self, profile_id: str) -> dict:
        """Get all pending (queued) updates for a profile."""
        if not self.access_token:
            return {"ok": False, "error": "Buffer access token not configured"}

        url = f"{self.base_url}/profiles/{profile_id}/updates/pending.json"
        params = {"access_token": self.access_token}

        try:
            response = requests.get(url, params=params, timeout=30)
            result = response.json()

            if "updates" in result:
                return {"ok": True, "updates": result["updates"], "total": result.get("total", 0)}
            else:
                return {"ok": False, "error": result.get("error", "Unknown error")}

        except requests.RequestException as e:
            return {"ok": False, "error": str(e)}

    def get_sent_updates(self, profile_id: str, count: int = 10) -> dict:
        """Get recently sent updates for a profile."""
        if not self.access_token:
            return {"ok": False, "error": "Buffer access token not configured"}

        url = f"{self.base_url}/profiles/{profile_id}/updates/sent.json"
        params = {"access_token": self.access_token, "count": count}

        try:
            response = requests.get(url, params=params, timeout=30)
            result = response.json()

            if "updates" in result:
                return {"ok": True, "updates": result["updates"]}
            else:
                return {"ok": False, "error": result.get("error", "Unknown error")}

        except requests.RequestException as e:
            return {"ok": False, "error": str(e)}

    def shuffle_queue(self, profile_id: str) -> dict:
        """Shuffle the order of queued updates."""
        if not self.access_token:
            return {"ok": False, "error": "Buffer access token not configured"}

        url = f"{self.base_url}/profiles/{profile_id}/updates/shuffle.json"
        data = {"access_token": self.access_token}

        try:
            response = requests.post(url, data=data, timeout=30)
            return response.json()
        except requests.RequestException as e:
            return {"ok": False, "error": str(e)}

    # ==========================================================================
    # Update Management
    # ==========================================================================

    def delete_update(self, update_id: str) -> dict:
        """Delete a pending update."""
        if not self.access_token:
            return {"ok": False, "error": "Buffer access token not configured"}

        url = f"{self.base_url}/updates/{update_id}/destroy.json"
        data = {"access_token": self.access_token}

        try:
            response = requests.post(url, data=data, timeout=30)
            return response.json()
        except requests.RequestException as e:
            return {"ok": False, "error": str(e)}

    def share_now(self, update_id: str) -> dict:
        """Share an update immediately."""
        if not self.access_token:
            return {"ok": False, "error": "Buffer access token not configured"}

        url = f"{self.base_url}/updates/{update_id}/share.json"
        data = {"access_token": self.access_token}

        try:
            response = requests.post(url, data=data, timeout=30)
            result = response.json()

            if result.get("success"):
                logger.info(f"Update shared immediately: {update_id}")
                return {"ok": True}
            else:
                return {"ok": False, "error": result.get("message", "Unknown error")}

        except requests.RequestException as e:
            return {"ok": False, "error": str(e)}

    # ==========================================================================
    # Statistics
    # ==========================================================================

    def get_update_stats(self, update_id: str) -> dict:
        """Get analytics for a specific update."""
        if not self.access_token:
            return {"ok": False, "error": "Buffer access token not configured"}

        url = f"{self.base_url}/updates/{update_id}.json"
        params = {"access_token": self.access_token}

        try:
            response = requests.get(url, params=params, timeout=30)
            result = response.json()

            if "statistics" in result:
                return {"ok": True, "stats": result["statistics"]}
            else:
                return {"ok": False, "error": "No statistics available"}

        except requests.RequestException as e:
            return {"ok": False, "error": str(e)}

    # ==========================================================================
    # Local Queue (Fallback when Buffer not available)
    # ==========================================================================

    def add_to_local_queue(self, post_data: dict) -> dict:
        """
        Add post to local queue (for when Buffer is not available).
        Posts will be uploaded when Buffer becomes available.
        """
        queue = self._load_local_queue()

        post_data["id"] = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        post_data["created_at"] = datetime.now(timezone.utc).isoformat()
        post_data["status"] = "queued"

        queue.append(post_data)
        self._save_local_queue(queue)

        logger.info(f"Added to local queue: {post_data['id']}")
        return {"ok": True, "id": post_data["id"]}

    def sync_local_queue(self) -> dict:
        """
        Sync local queue to Buffer.
        Call this when Buffer becomes available.
        """
        if not self.access_token:
            return {"ok": False, "error": "Buffer not configured"}

        queue = self._load_local_queue()
        synced = 0
        failed = 0

        for post in queue:
            if post.get("status") == "queued":
                platform = post.get("platform", "instagram")

                if platform == "instagram":
                    result = self.schedule_instagram_post(
                        caption=post.get("caption", ""),
                        image_url=post.get("image_url", ""),
                        scheduled_at=post.get("scheduled_at")
                    )
                elif platform == "pinterest":
                    result = self.schedule_pinterest_pin(
                        description=post.get("description", ""),
                        image_url=post.get("image_url", ""),
                        link_url=post.get("link_url", "")
                    )
                else:
                    continue

                if result.get("ok"):
                    post["status"] = "synced"
                    synced += 1
                else:
                    post["error"] = result.get("error")
                    failed += 1

        self._save_local_queue(queue)

        return {"ok": True, "synced": synced, "failed": failed}

    def _load_local_queue(self) -> List[dict]:
        """Load local queue from file."""
        if self.queue_file.exists():
            try:
                with open(self.queue_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def _save_local_queue(self, queue: List[dict]):
        """Save local queue to file."""
        self.queue_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.queue_file, "w", encoding="utf-8") as f:
            json.dump(queue, f, indent=2)

    # ==========================================================================
    # Utility
    # ==========================================================================

    def test_connection(self) -> bool:
        """Test Buffer API connection."""
        result = self.get_profiles()
        return result.get("ok", False)

    def get_status(self) -> dict:
        """Get current Buffer status and quota."""
        profiles = self.get_profiles()

        if not profiles.get("ok"):
            return {"ok": False, "error": profiles.get("error")}

        status = {
            "ok": True,
            "connected_profiles": len(profiles.get("profiles", [])),
            "profiles": []
        }

        for profile in profiles.get("profiles", []):
            pending = self.get_pending_updates(profile["id"])
            status["profiles"].append({
                "service": profile["service"],
                "name": profile.get("formatted_username", profile.get("service_username")),
                "pending_posts": pending.get("total", 0) if pending.get("ok") else "N/A"
            })

        return status


# =============================================================================
# Alternative: Make.com / Zapier Integration (Free tier available)
# =============================================================================

class MakeWebhook:
    """
    Integration with Make.com (formerly Integromat) webhooks.
    Free tier: 1,000 operations/month

    Setup:
    1. Create Make.com account
    2. Create scenario with Webhook trigger
    3. Add Instagram/Pinterest modules
    4. Copy webhook URL
    """

    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url or os.getenv("MAKE_WEBHOOK_URL", "")

    def trigger_post(self, data: dict) -> dict:
        """
        Trigger Make.com scenario to post content.

        Args:
            data: Post data to send to webhook
        """
        if not self.webhook_url:
            return {"ok": False, "error": "Make webhook URL not configured"}

        try:
            response = requests.post(self.webhook_url, json=data, timeout=30)

            if response.status_code == 200:
                logger.info("Make.com webhook triggered successfully")
                return {"ok": True}
            else:
                return {"ok": False, "error": f"Webhook returned {response.status_code}"}

        except requests.RequestException as e:
            return {"ok": False, "error": str(e)}


# =============================================================================
# Standalone test
# =============================================================================
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    buffer = BufferIntegration()

    print("Testing Buffer connection...")
    status = buffer.get_status()

    if status.get("ok"):
        print(f"Connected profiles: {status['connected_profiles']}")
        for profile in status["profiles"]:
            print(f"  - {profile['service']}: {profile['name']} ({profile['pending_posts']} pending)")
    else:
        print(f"Buffer not configured or error: {status.get('error')}")
        print("\nTo set up Buffer:")
        print("1. Go to https://buffer.com and sign up (free tier available)")
        print("2. Connect your Instagram/Pinterest accounts")
        print("3. Get your access token from Settings > Apps & Extras")
        print("4. Set BUFFER_ACCESS_TOKEN in your .env file")
