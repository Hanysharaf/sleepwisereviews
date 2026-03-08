"""
SleepWise Automation Agent - Pinterest Manager
Handles Pinterest API interactions for posting pins.
"""

import requests
import logging
import json
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime, timezone

import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import PINTEREST_ACCESS_TOKEN, PINTEREST_CONFIG, WEBSITE_CONFIG

logger = logging.getLogger(__name__)


class PinterestManager:
    """Handles Pinterest API v5 interactions."""

    def __init__(self, access_token: str = None):
        """
        Initialize the Pinterest manager.

        Args:
            access_token: Pinterest API access token (defaults to env var)
        """
        self.access_token = access_token or PINTEREST_ACCESS_TOKEN
        self.api_base = PINTEREST_CONFIG["api_base_url"]
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def _make_request(self, method: str, endpoint: str,
                      data: dict = None, params: dict = None) -> dict:
        """
        Make a request to the Pinterest API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            data: Request body data
            params: Query parameters

        Returns:
            API response as dict
        """
        url = f"{self.api_base}/{endpoint}"
        try:
            response = requests.request(
                method,
                url,
                headers=self.headers,
                json=data,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return {"ok": True, "data": response.json()}
        except requests.exceptions.HTTPError as e:
            error_detail = ""
            try:
                error_detail = response.json()
            except:
                error_detail = response.text
            logger.error(f"Pinterest API HTTP error: {e} - {error_detail}")
            return {"ok": False, "error": str(e), "detail": error_detail}
        except requests.RequestException as e:
            logger.error(f"Pinterest API request error: {e}")
            return {"ok": False, "error": str(e)}

    # ==========================================================================
    # User & Board Management
    # ==========================================================================

    def get_user_account(self) -> dict:
        """Get the authenticated user's account info."""
        return self._make_request("GET", "user_account")

    def get_boards(self) -> dict:
        """Get all boards for the authenticated user."""
        return self._make_request("GET", "boards")

    def get_board(self, board_id: str) -> dict:
        """
        Get a specific board by ID.

        Args:
            board_id: Pinterest board ID
        """
        return self._make_request("GET", f"boards/{board_id}")

    def create_board(self, name: str, description: str = "",
                     privacy: str = "PUBLIC") -> dict:
        """
        Create a new board.

        Args:
            name: Board name
            description: Board description
            privacy: PUBLIC or PROTECTED
        """
        data = {
            "name": name,
            "description": description,
            "privacy": privacy
        }
        return self._make_request("POST", "boards", data=data)

    # ==========================================================================
    # Pin Management
    # ==========================================================================

    def create_pin(self, board_id: str, title: str, description: str,
                   link: str, media_source: dict, alt_text: str = None) -> dict:
        """
        Create a new pin.

        Args:
            board_id: Board ID to pin to
            title: Pin title (max 100 chars)
            description: Pin description (max 500 chars)
            link: Destination URL when pin is clicked
            media_source: Media source dict (url, base64, or media_id)
            alt_text: Alt text for accessibility

        Returns:
            API response with pin data
        """
        data = {
            "board_id": board_id,
            "title": title[:100],  # Pinterest limit
            "description": description[:500],  # Pinterest limit
            "link": link,
            "media_source": media_source
        }

        if alt_text:
            data["alt_text"] = alt_text[:500]

        result = self._make_request("POST", "pins", data=data)

        if result.get("ok"):
            logger.info(f"Pin created successfully: {title}")
        else:
            logger.error(f"Failed to create pin: {result.get('error')}")

        return result

    def create_pin_from_url(self, board_id: str, title: str, description: str,
                            link: str, image_url: str, alt_text: str = None) -> dict:
        """
        Create a pin using an image URL.

        Args:
            board_id: Board ID to pin to
            title: Pin title
            description: Pin description
            link: Destination URL
            image_url: URL of the image to pin
            alt_text: Alt text for accessibility
        """
        media_source = {
            "source_type": "image_url",
            "url": image_url
        }
        return self.create_pin(board_id, title, description, link,
                               media_source, alt_text)

    def get_pins(self, board_id: str = None, page_size: int = 25) -> dict:
        """
        Get pins, optionally filtered by board.

        Args:
            board_id: Filter by board (optional)
            page_size: Number of pins to return (max 250)
        """
        if board_id:
            return self._make_request(
                "GET",
                f"boards/{board_id}/pins",
                params={"page_size": min(page_size, 250)}
            )
        return self._make_request(
            "GET",
            "pins",
            params={"page_size": min(page_size, 250)}
        )

    def delete_pin(self, pin_id: str) -> dict:
        """
        Delete a pin.

        Args:
            pin_id: ID of the pin to delete
        """
        return self._make_request("DELETE", f"pins/{pin_id}")

    # ==========================================================================
    # Analytics
    # ==========================================================================

    def get_pin_analytics(self, pin_id: str, start_date: str,
                          end_date: str, metric_types: List[str] = None) -> dict:
        """
        Get analytics for a specific pin.

        Args:
            pin_id: Pin ID
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            metric_types: List of metrics (IMPRESSION, PIN_CLICK, etc.)
        """
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "metric_types": ",".join(metric_types or ["IMPRESSION", "PIN_CLICK"])
        }
        return self._make_request("GET", f"pins/{pin_id}/analytics", params=params)

    def get_user_analytics(self, start_date: str, end_date: str) -> dict:
        """
        Get account-level analytics.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
        """
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "metric_types": "IMPRESSION,PIN_CLICK,OUTBOUND_CLICK,SAVE"
        }
        return self._make_request("GET", "user_account/analytics", params=params)

    # ==========================================================================
    # Helper Methods
    # ==========================================================================

    def generate_description(self, title: str, keywords: List[str],
                             article_url: str = None) -> str:
        """
        Generate a Pinterest-optimized description.

        Args:
            title: Pin title
            keywords: List of relevant keywords
            article_url: Optional article URL for CTA
        """
        # Pinterest descriptions should be 150-300 characters
        base_description = title

        # Add keywords as natural text
        if keywords:
            keyword_text = ", ".join(keywords[:5])
            base_description += f". Learn about {keyword_text}."

        # Add call to action
        if article_url:
            base_description += " Click to read the full guide!"

        # Add hashtags (Pinterest supports them)
        hashtags = " ".join([f"#{kw.replace(' ', '')}" for kw in keywords[:3]])
        full_description = f"{base_description} {hashtags}"

        return full_description[:500]  # Pinterest limit

    def select_board(self, content_type: str = None) -> str:
        """
        Select appropriate board based on content type.

        Args:
            content_type: Type of content (product_review, tips, science, etc.)

        Returns:
            Board ID
        """
        boards = PINTEREST_CONFIG["boards"]

        if content_type == "product_review":
            return boards.get("product_reviews", list(boards.values())[0])
        elif content_type == "science":
            return boards.get("sleep_science", list(boards.values())[0])
        else:
            return boards.get("sleep_tips", list(boards.values())[0])

    def test_connection(self) -> bool:
        """Test the Pinterest API connection."""
        result = self.get_user_account()
        if result.get("ok"):
            username = result.get("data", {}).get("username", "Unknown")
            logger.info(f"Connected to Pinterest account: {username}")
            return True
        logger.error("Failed to connect to Pinterest API")
        return False

    def post_article_pin(self, article: dict, board_id: str = None) -> dict:
        """
        Create a pin for a website article.

        Args:
            article: Article data dict with title, description, url, image_url
            board_id: Specific board ID (optional, auto-selects if not provided)

        Returns:
            Result of pin creation
        """
        if not board_id:
            board_id = self.select_board(article.get("content_type"))

        title = article.get("title", "Sleep Tips")
        description = self.generate_description(
            title,
            article.get("keywords", []),
            article.get("url")
        )

        return self.create_pin_from_url(
            board_id=board_id,
            title=title,
            description=description,
            link=article.get("url", WEBSITE_CONFIG["base_url"]),
            image_url=article.get("image_url", ""),
            alt_text=article.get("alt_text", title)
        )


# =============================================================================
# Standalone test
# =============================================================================
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    manager = PinterestManager()

    if manager.test_connection():
        print("✅ Pinterest connection successful!")

        # Get boards
        boards_result = manager.get_boards()
        if boards_result.get("ok"):
            boards = boards_result.get("data", {}).get("items", [])
            print(f"Found {len(boards)} boards:")
            for board in boards:
                print(f"  - {board.get('name')} (ID: {board.get('id')})")
    else:
        print("❌ Failed to connect to Pinterest")
