"""
n8n Integration Module for SleepWise Reviews
Handles communication with n8n workflows for automation
"""

import os
import json
import requests
from typing import Dict, Any, Optional
from datetime import datetime


class N8NIntegration:
    """Helper class for triggering n8n workflows via webhooks"""

    def __init__(self):
        self.webhook_base = os.getenv('N8N_WEBHOOK_BASE')
        self.api_key = os.getenv('N8N_API_KEY', '')

    def trigger_pinterest_post(self, pin_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Trigger n8n workflow to post a pin to Pinterest

        Args:
            pin_data: Dictionary with pin info (title, description, link, image_url, etc.)

        Returns:
            Response from n8n webhook
        """
        webhook_url = f"{self.webhook_base}/post-pinterest"

        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "pin": pin_data
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

    def trigger_daily_report(self, stats: Dict[str, Any]) -> Dict[str, Any]:
        """
        Trigger n8n workflow to send daily analytics report

        Args:
            stats: Dictionary with daily statistics

        Returns:
            Response from n8n webhook
        """
        webhook_url = f"{self.webhook_base}/daily-report"

        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "stats": stats
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

    def trigger_instagram_reminder(self, content_path: str) -> Dict[str, Any]:
        """
        Trigger n8n workflow to send Instagram posting reminder

        Args:
            content_path: Path to Instagram content folder

        Returns:
            Response from n8n webhook
        """
        webhook_url = f"{self.webhook_base}/instagram-reminder"

        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "content_path": content_path
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
        Trigger n8n workflow to check content queue and alert if low

        Args:
            queue_length: Current number of items in queue

        Returns:
            Response from n8n webhook
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
        """Get headers for n8n API requests"""
        headers = {
            "Content-Type": "application/json"
        }

        if self.api_key:
            headers["X-N8N-API-KEY"] = self.api_key

        return headers

    def is_configured(self) -> bool:
        """Check if n8n integration is properly configured"""
        return bool(self.webhook_base)


# Example usage
if __name__ == "__main__":
    # Test n8n integration
    n8n = N8NIntegration()

    if not n8n.is_configured():
        print("❌ n8n not configured. Set N8N_WEBHOOK_BASE in .env")
    else:
        print(f"✅ n8n configured: {n8n.webhook_base}")

        # Test with dummy data
        test_pin = {
            "title": "Test Pin",
            "description": "Testing n8n integration",
            "link": "https://hanysharaf.github.io/sleepwisereviews/",
            "image_url": "https://via.placeholder.com/800x1200"
        }

        print("\nTesting Pinterest webhook...")
        result = n8n.trigger_pinterest_post(test_pin)
        print(f"Result: {json.dumps(result, indent=2)}")
