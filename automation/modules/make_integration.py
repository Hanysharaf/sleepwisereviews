"""
Make.com Integration Module for SleepWise Reviews
Handles communication with Make.com scenarios via webhooks
"""

import os
import json
import requests
from typing import Dict, Any
from datetime import datetime


class MakeIntegration:
    """Helper class for triggering Make.com scenarios via webhooks"""

    def __init__(self):
        self.webhook_base = os.getenv('MAKE_WEBHOOK_BASE')
        self.secret = os.getenv('MAKE_WEBHOOK_SECRET', '')

    def trigger_instagram_post(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Trigger Make.com scenario to post to Instagram

        Args:
            post_data: Dictionary with post info (caption, image_url, etc.)

        Returns:
            Response from Make.com webhook
        """
        webhook_url = f"{self.webhook_base}/instagram-post"

        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "post": post_data
        }

        try:
            response = requests.post(
                webhook_url,
                json=payload,
                headers=self._get_headers(),
                timeout=30
            )
            response.raise_for_status()
            return {
                "success": True,
                "data": response.json(),
                "status_code": response.status_code
            }
        except requests.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": getattr(e.response, 'status_code', None)
            }

    def check_content_queue(self, queue_length: int) -> Dict[str, Any]:
        """
        Trigger Make.com scenario to check content queue and alert if low

        Args:
            queue_length: Current number of items in queue

        Returns:
            Response from Make.com webhook
        """
        webhook_url = f"{self.webhook_base}/check-queue"

        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "queue_length": queue_length,
            "alert_threshold": 5
        }

        try:
            response = requests.post(
                webhook_url,
                json=payload,
                headers=self._get_headers(),
                timeout=30
            )
            response.raise_for_status()
            return {
                "success": True,
                "data": response.json(),
                "status_code": response.status_code
            }
        except requests.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": getattr(e.response, 'status_code', None)
            }

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json"
        }
        if self.secret:
            headers["X-Make-Secret"] = self.secret
        return headers

    def is_configured(self) -> bool:
        return bool(self.webhook_base)


if __name__ == "__main__":
    make = MakeIntegration()

    if not make.is_configured():
        print("Make.com not configured. Set MAKE_WEBHOOK_BASE in .env")
    else:
        print(f"Make.com configured: {make.webhook_base}")

        test_post = {
            "caption": "Test post from SleepWise Reviews",
            "image_url": "https://hanysharaf.github.io/sleepwisereviews/assets/test.jpg"
        }

        print("\nTesting Instagram webhook...")
        result = make.trigger_instagram_post(test_post)
        print(f"Result: {json.dumps(result, indent=2)}")
