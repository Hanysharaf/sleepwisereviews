"""
SleepWise Automation Agent - Instagram Prep
Prepares Instagram content for manual posting via Meta Business Suite.
"""

import logging
import json
import random
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime, timezone

import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import (
    INSTAGRAM_CONFIG, PROJECT_ROOT, DATA_DIR,
    CONTENT_CONFIG, WEBSITE_CONFIG
)

logger = logging.getLogger(__name__)


class InstagramPrep:
    """Prepares Instagram content for manual posting."""

    def __init__(self):
        """Initialize Instagram prep module."""
        self.max_hashtags = INSTAGRAM_CONFIG["max_hashtags"]
        self.default_hashtags = INSTAGRAM_CONFIG["default_hashtags"]
        self.best_times = INSTAGRAM_CONFIG["best_posting_times"]
        self.project_root = PROJECT_ROOT
        self.prepared_content_file = DATA_DIR / "instagram_queue.json"

    # ==========================================================================
    # Content Preparation
    # ==========================================================================

    def prepare_post(self, caption: str, image_path: str = None,
                     hashtags: List[str] = None, article_url: str = None) -> dict:
        """
        Prepare an Instagram post for manual publishing.

        Args:
            caption: Post caption
            image_path: Path to image file
            hashtags: List of hashtags (without #)
            article_url: Related article URL (for link in bio)

        Returns:
            Prepared post data
        """
        # Process hashtags
        all_hashtags = self._prepare_hashtags(hashtags)
        hashtag_text = " ".join([f"#{tag}" for tag in all_hashtags])

        # Format caption with hashtags
        full_caption = f"{caption}\n\n.\n.\n.\n\n{hashtag_text}"

        # Get suggested posting time
        suggested_time = self._get_best_posting_time()

        post_data = {
            "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "caption": caption,
            "hashtags": all_hashtags,
            "full_caption": full_caption,
            "image_path": image_path,
            "article_url": article_url,
            "suggested_time": suggested_time,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": "pending",
            "character_count": len(full_caption)
        }

        # Validate caption length
        if len(full_caption) > 2200:
            logger.warning(f"Caption exceeds Instagram limit: {len(full_caption)} chars")
            post_data["warning"] = "Caption exceeds 2200 character limit"

        # Save to queue
        self._add_to_queue(post_data)

        logger.info(f"Instagram post prepared: {post_data['id']}")
        return {"ok": True, "post": post_data}

    def _prepare_hashtags(self, custom_hashtags: List[str] = None) -> List[str]:
        """
        Prepare hashtag list, combining custom and default.

        Args:
            custom_hashtags: Custom hashtags for this post

        Returns:
            Combined list of hashtags (max 30)
        """
        hashtags = []

        # Add custom hashtags first
        if custom_hashtags:
            hashtags.extend([tag.lower().replace("#", "").replace(" ", "")
                           for tag in custom_hashtags])

        # Add default hashtags to fill remaining slots
        remaining = self.max_hashtags - len(hashtags)
        if remaining > 0:
            available_defaults = [h for h in self.default_hashtags
                                 if h not in hashtags]
            random.shuffle(available_defaults)
            hashtags.extend(available_defaults[:remaining])

        return hashtags[:self.max_hashtags]

    def _get_best_posting_time(self) -> str:
        """Get the next best posting time."""
        now = datetime.now()
        current_time = now.strftime("%H:%M")

        for time in self.best_times:
            if time > current_time:
                return time

        # If past all times today, return first time tomorrow
        return self.best_times[0]

    # ==========================================================================
    # Queue Management
    # ==========================================================================

    def _add_to_queue(self, post_data: dict):
        """Add post to the prepared content queue."""
        queue = self._load_queue()
        queue.append(post_data)
        self._save_queue(queue)

    def _load_queue(self) -> List[dict]:
        """Load the content queue from file."""
        if self.prepared_content_file.exists():
            try:
                with open(self.prepared_content_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def _save_queue(self, queue: List[dict]):
        """Save the content queue to file."""
        self.prepared_content_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.prepared_content_file, "w", encoding="utf-8") as f:
            json.dump(queue, f, indent=2)

    def get_pending_posts(self) -> List[dict]:
        """Get all pending posts."""
        queue = self._load_queue()
        return [p for p in queue if p.get("status") == "pending"]

    def get_all_posts(self) -> List[dict]:
        """Get all prepared posts."""
        return self._load_queue()

    def mark_posted(self, post_id: str) -> dict:
        """
        Mark a post as published.

        Args:
            post_id: ID of the post to mark

        Returns:
            Updated post data
        """
        queue = self._load_queue()

        for post in queue:
            if post.get("id") == post_id:
                post["status"] = "posted"
                post["posted_at"] = datetime.now(timezone.utc).isoformat()
                self._save_queue(queue)
                logger.info(f"Instagram post marked as posted: {post_id}")
                return {"ok": True, "post": post}

        return {"ok": False, "error": "Post not found"}

    def delete_post(self, post_id: str) -> dict:
        """
        Delete a prepared post from queue.

        Args:
            post_id: ID of the post to delete

        Returns:
            Result of deletion
        """
        queue = self._load_queue()
        original_length = len(queue)

        queue = [p for p in queue if p.get("id") != post_id]

        if len(queue) < original_length:
            self._save_queue(queue)
            logger.info(f"Instagram post deleted: {post_id}")
            return {"ok": True}

        return {"ok": False, "error": "Post not found"}

    def clear_posted(self) -> dict:
        """Clear all posted items from queue."""
        queue = self._load_queue()
        queue = [p for p in queue if p.get("status") != "posted"]
        self._save_queue(queue)
        return {"ok": True, "remaining": len(queue)}

    # ==========================================================================
    # Content Generation Helpers
    # ==========================================================================

    def prepare_from_article(self, article: dict) -> dict:
        """
        Prepare Instagram post from article data.

        Args:
            article: Article data with title, excerpt, keywords, etc.

        Returns:
            Prepared post data
        """
        title = article.get("title", "")
        excerpt = article.get("introduction", article.get("excerpt", ""))
        keywords = article.get("keywords", [])
        url = article.get("url", WEBSITE_CONFIG["base_url"])

        # Create engaging caption from article
        caption = self._create_article_caption(title, excerpt)

        # Convert keywords to hashtags
        hashtags = [kw.lower().replace(" ", "") for kw in keywords[:10]]

        # Find related image
        image_path = self._find_related_image(keywords)

        return self.prepare_post(
            caption=caption,
            image_path=image_path,
            hashtags=hashtags,
            article_url=url
        )

    def _create_article_caption(self, title: str, excerpt: str) -> str:
        """Create an engaging Instagram caption from article content."""
        # Create hook
        hooks = [
            "🌙 ",
            "💤 ",
            "✨ ",
            "Did you know? ",
            "Sleep better tonight! ",
            "The secret to great sleep: "
        ]

        hook = random.choice(hooks)

        # Truncate excerpt if too long
        max_excerpt = 800
        if len(excerpt) > max_excerpt:
            excerpt = excerpt[:max_excerpt].rsplit(" ", 1)[0] + "..."

        caption = f"{hook}{title}\n\n{excerpt}\n\n📖 Link in bio for the full article!"

        return caption

    def _find_related_image(self, keywords: List[str]) -> Optional[str]:
        """Find a related image based on keywords."""
        image_extensions = {".jpg", ".jpeg", ".png", ".webp"}

        for keyword in keywords:
            keyword_lower = keyword.lower().replace(" ", "-")
            for ext in image_extensions:
                for img_path in self.project_root.glob(f"*{ext}"):
                    if keyword_lower in img_path.name.lower():
                        return str(img_path)

        # Return any available image
        for ext in image_extensions:
            images = list(self.project_root.glob(f"*{ext}"))
            if images:
                return str(images[0])

        return None

    # ==========================================================================
    # Formatting Utilities
    # ==========================================================================

    def format_for_telegram(self, post: dict) -> str:
        """
        Format post data for Telegram notification.

        Args:
            post: Post data dict

        Returns:
            Formatted message for Telegram
        """
        message = (
            f"📸 <b>Instagram Post Ready!</b>\n\n"
            f"📝 <b>Caption:</b>\n"
            f"<code>{post.get('full_caption', post.get('caption', ''))}</code>\n\n"
        )

        if post.get("image_path"):
            message += f"🖼️ Image: {Path(post['image_path']).name}\n"

        if post.get("article_url"):
            message += f"🔗 Article: {post['article_url']}\n"

        message += (
            f"\n⏰ Suggested posting time: {post.get('suggested_time', 'N/A')}\n"
            f"📊 Character count: {post.get('character_count', 'N/A')}/2200\n\n"
            f"👆 <b>Copy the caption above to Meta Business Suite!</b>"
        )

        return message

    def get_posting_stats(self) -> dict:
        """Get statistics about prepared content."""
        queue = self._load_queue()

        pending = [p for p in queue if p.get("status") == "pending"]
        posted = [p for p in queue if p.get("status") == "posted"]

        # Calculate posts this week
        week_ago = datetime.now(timezone.utc).timestamp() - (7 * 24 * 60 * 60)
        posted_this_week = [
            p for p in posted
            if datetime.fromisoformat(p.get("posted_at", "1970-01-01")).timestamp() > week_ago
        ]

        return {
            "pending_count": len(pending),
            "posted_total": len(posted),
            "posted_this_week": len(posted_this_week),
            "queue_size": len(queue)
        }


# =============================================================================
# Standalone test
# =============================================================================
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    prep = InstagramPrep()

    # Test preparing a post
    result = prep.prepare_post(
        caption="🌙 Getting better sleep starts with the right environment. Here are 5 tips to transform your bedroom into a sleep sanctuary...",
        hashtags=["sleeptips", "bettersleep", "sleepsanctuary"]
    )

    if result.get("ok"):
        print("✅ Post prepared successfully!")
        print(f"Post ID: {result['post']['id']}")
        print(f"Caption length: {result['post']['character_count']} chars")
        print(f"Suggested time: {result['post']['suggested_time']}")
    else:
        print(f"❌ Failed to prepare post: {result.get('error')}")

    # Show stats
    stats = prep.get_posting_stats()
    print(f"\nQueue stats:")
    print(f"  Pending: {stats['pending_count']}")
    print(f"  Posted this week: {stats['posted_this_week']}")
