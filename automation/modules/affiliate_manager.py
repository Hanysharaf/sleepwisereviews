"""
SleepWise Automation Agent - Affiliate Link Manager
Manages affiliate products, links, and seasonal campaigns.
Scalable system for adding new products based on market needs.
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, List, Dict
from urllib.parse import urlencode, quote_plus

import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import DATA_DIR, PROJECT_ROOT

logger = logging.getLogger(__name__)

# Environment variables
AMAZON_TAG = os.getenv("AMAZON_AFFILIATE_TAG", "sleepwise-20")
CLICKBANK_NICKNAME = os.getenv("CLICKBANK_NICKNAME", "")


class AffiliateManager:
    """
    Manages affiliate products, links, and campaigns.
    Supports seasonal content and easy product additions.
    """

    def __init__(self):
        """Initialize affiliate manager."""
        self.products_file = DATA_DIR / "affiliate_products.json"
        self.campaigns_file = DATA_DIR / "seasonal_campaigns.json"
        self.stats_file = DATA_DIR / "affiliate_stats.json"

        # Load data
        self.products = self._load_products()
        self.campaigns = self._load_campaigns()

        # Initialize with default products if empty
        if not self.products:
            self._init_default_products()

    # ==========================================================================
    # Data Loading
    # ==========================================================================

    def _load_products(self) -> Dict:
        """Load products from file."""
        if self.products_file.exists():
            try:
                with open(self.products_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
        return {}

    def _save_products(self):
        """Save products to file."""
        self.products_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.products_file, "w", encoding="utf-8") as f:
            json.dump(self.products, f, indent=2)

    def _load_campaigns(self) -> Dict:
        """Load seasonal campaigns from file."""
        if self.campaigns_file.exists():
            try:
                with open(self.campaigns_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
        return self._default_campaigns()

    def _save_campaigns(self):
        """Save campaigns to file."""
        self.campaigns_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.campaigns_file, "w", encoding="utf-8") as f:
            json.dump(self.campaigns, f, indent=2)

    # ==========================================================================
    # Default Data
    # ==========================================================================

    def _init_default_products(self):
        """Initialize with default sleep products."""
        self.products = {
            # Weighted Blankets
            "bearaby-cotton-napper": {
                "name": "Bearaby Cotton Napper",
                "category": "weighted_blankets",
                "asin": "B07RWLR8FV",
                "price_range": "$199-$279",
                "commission": "4%",
                "rating": 4.7,
                "reviews": 5000,
                "keywords": ["weighted blanket", "cotton", "breathable", "anxiety"],
                "best_for": ["hot sleepers", "anxiety", "premium"],
                "season": ["all"],
                "active": True
            },
            "ynm-weighted-blanket": {
                "name": "YnM Weighted Blanket",
                "category": "weighted_blankets",
                "asin": "B073429DV2",
                "price_range": "$39-$69",
                "commission": "4%",
                "rating": 4.5,
                "reviews": 50000,
                "keywords": ["weighted blanket", "budget", "cooling"],
                "best_for": ["budget", "beginners"],
                "season": ["all"],
                "active": True
            },
            "gravity-blanket": {
                "name": "Gravity Blanket",
                "category": "weighted_blankets",
                "asin": "B07B2TT3FQ",
                "price_range": "$189-$249",
                "commission": "4%",
                "rating": 4.5,
                "reviews": 8000,
                "keywords": ["weighted blanket", "original", "anxiety", "stress"],
                "best_for": ["anxiety", "stress relief"],
                "season": ["all"],
                "active": True
            },
            # White Noise Machines
            "lectrofan-evo": {
                "name": "LectroFan Evo",
                "category": "white_noise",
                "asin": "B07MFZZQ13",
                "price_range": "$49-$59",
                "commission": "4%",
                "rating": 4.7,
                "reviews": 20000,
                "keywords": ["white noise", "fan sounds", "sleep machine"],
                "best_for": ["light sleepers", "apartments"],
                "season": ["all"],
                "active": True
            },
            "hatch-restore": {
                "name": "Hatch Restore",
                "category": "white_noise",
                "asin": "B08635Q4SB",
                "price_range": "$129-$149",
                "commission": "4%",
                "rating": 4.6,
                "reviews": 15000,
                "keywords": ["sunrise alarm", "sound machine", "smart"],
                "best_for": ["tech lovers", "morning routine"],
                "season": ["all"],
                "active": True
            },
            # Sleep Supplements
            "magnesium-glycinate": {
                "name": "Pure Encapsulations Magnesium Glycinate",
                "category": "supplements",
                "asin": "B000GHJRV4",
                "price_range": "$22-$35",
                "commission": "4%",
                "rating": 4.7,
                "reviews": 12000,
                "keywords": ["magnesium", "sleep supplement", "natural"],
                "best_for": ["muscle relaxation", "natural sleep"],
                "season": ["all"],
                "active": True
            },
            # Sleep Masks
            "manta-sleep-mask": {
                "name": "Manta Sleep Mask",
                "category": "sleep_masks",
                "asin": "B07PRG2CQB",
                "price_range": "$30-$40",
                "commission": "4%",
                "rating": 4.5,
                "reviews": 25000,
                "keywords": ["sleep mask", "blackout", "adjustable"],
                "best_for": ["light sensitivity", "travel"],
                "season": ["all"],
                "active": True
            },
            # Cooling Products (Summer)
            "chilipad-cube": {
                "name": "ChiliPad Cube Sleep System",
                "category": "cooling",
                "asin": "B07L3YM8JG",
                "price_range": "$399-$699",
                "commission": "4%",
                "rating": 4.3,
                "reviews": 3000,
                "keywords": ["cooling mattress pad", "temperature control"],
                "best_for": ["hot sleepers", "night sweats", "menopause"],
                "season": ["summer", "spring"],
                "active": True
            },
            # Cozy Products (Winter)
            "heated-blanket": {
                "name": "Sunbeam Heated Blanket",
                "category": "heated",
                "asin": "B00JMQG0U4",
                "price_range": "$50-$80",
                "commission": "4%",
                "rating": 4.6,
                "reviews": 30000,
                "keywords": ["heated blanket", "electric blanket", "warm"],
                "best_for": ["cold sleepers", "winter"],
                "season": ["winter", "fall"],
                "active": True
            }
        }

        # ClickBank products (higher commission)
        if CLICKBANK_NICKNAME:
            self.products["resurge-supplement"] = {
                "name": "Resurge Deep Sleep Support",
                "category": "supplements",
                "platform": "clickbank",
                "vendor": "resurge",
                "price_range": "$49-$147",
                "commission": "75%",
                "keywords": ["deep sleep", "weight loss", "metabolism"],
                "best_for": ["weight loss", "deep sleep"],
                "season": ["all"],
                "active": True
            }

        self._save_products()
        logger.info(f"Initialized {len(self.products)} default products")

    def _default_campaigns(self) -> Dict:
        """Default seasonal campaigns."""
        return {
            "spring": {
                "name": "Spring Sleep Refresh",
                "months": [3, 4, 5],
                "themes": ["allergy-free sleep", "spring cleaning bedroom", "daylight saving"],
                "featured_categories": ["cooling", "supplements", "white_noise"],
                "hooks": [
                    "Spring allergies ruining your sleep?",
                    "Time to refresh your sleep setup!",
                    "Daylight saving got you tired?"
                ]
            },
            "summer": {
                "name": "Cool Sleep Summer",
                "months": [6, 7, 8],
                "themes": ["cooling products", "hot sleeper solutions", "vacation sleep"],
                "featured_categories": ["cooling", "sleep_masks", "white_noise"],
                "hooks": [
                    "Too hot to sleep?",
                    "Beat the summer heat in bed",
                    "Stay cool all night long"
                ]
            },
            "fall": {
                "name": "Cozy Sleep Season",
                "months": [9, 10, 11],
                "themes": ["cozy bedroom", "back to routine", "weighted blankets"],
                "featured_categories": ["weighted_blankets", "heated", "supplements"],
                "hooks": [
                    "Get cozy this fall",
                    "Back to school = back to sleep routine",
                    "The perfect weighted blanket weather"
                ]
            },
            "winter": {
                "name": "Winter Sleep Wellness",
                "months": [12, 1, 2],
                "themes": ["holiday stress", "new year sleep goals", "cozy essentials"],
                "featured_categories": ["weighted_blankets", "heated", "supplements"],
                "hooks": [
                    "Sleep through the holidays stress-free",
                    "New year, better sleep",
                    "Winter wellness starts with sleep"
                ]
            },
            # Special campaigns
            "black_friday": {
                "name": "Black Friday Sleep Deals",
                "months": [11],
                "days": [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
                "themes": ["deals", "discounts", "best prices"],
                "featured_categories": ["all"],
                "hooks": [
                    "BIGGEST sleep deals of the year!",
                    "Black Friday: Save big on sleep",
                    "Don't sleep on these deals"
                ]
            },
            "prime_day": {
                "name": "Prime Day Sleep Deals",
                "months": [7, 10],
                "themes": ["prime deals", "amazon exclusive"],
                "featured_categories": ["all"],
                "hooks": [
                    "Prime Day sleep essentials",
                    "Exclusive deals for better sleep"
                ]
            }
        }

    # ==========================================================================
    # Product Management
    # ==========================================================================

    def add_product(self, product_id: str, product_data: Dict) -> dict:
        """
        Add a new affiliate product.

        Args:
            product_id: Unique product identifier
            product_data: Product information dict

        Returns:
            Result dict
        """
        required_fields = ["name", "category"]
        for field in required_fields:
            if field not in product_data:
                return {"ok": False, "error": f"Missing required field: {field}"}

        # Set defaults
        product_data.setdefault("active", True)
        product_data.setdefault("season", ["all"])
        product_data.setdefault("added_at", datetime.now(timezone.utc).isoformat())

        self.products[product_id] = product_data
        self._save_products()

        logger.info(f"Added product: {product_id}")
        return {"ok": True, "product_id": product_id}

    def update_product(self, product_id: str, updates: Dict) -> dict:
        """Update an existing product."""
        if product_id not in self.products:
            return {"ok": False, "error": "Product not found"}

        self.products[product_id].update(updates)
        self.products[product_id]["updated_at"] = datetime.now(timezone.utc).isoformat()
        self._save_products()

        return {"ok": True}

    def deactivate_product(self, product_id: str) -> dict:
        """Deactivate a product (don't delete, just hide)."""
        if product_id not in self.products:
            return {"ok": False, "error": "Product not found"}

        self.products[product_id]["active"] = False
        self._save_products()

        return {"ok": True}

    def get_products_by_category(self, category: str, active_only: bool = True) -> List[Dict]:
        """Get all products in a category."""
        products = []
        for pid, pdata in self.products.items():
            if pdata.get("category") == category:
                if not active_only or pdata.get("active", True):
                    products.append({"id": pid, **pdata})
        return products

    def get_seasonal_products(self, season: str = None) -> List[Dict]:
        """Get products for current or specified season."""
        if not season:
            month = datetime.now().month
            if month in [3, 4, 5]:
                season = "spring"
            elif month in [6, 7, 8]:
                season = "summer"
            elif month in [9, 10, 11]:
                season = "fall"
            else:
                season = "winter"

        products = []
        for pid, pdata in self.products.items():
            if pdata.get("active", True):
                if "all" in pdata.get("season", []) or season in pdata.get("season", []):
                    products.append({"id": pid, **pdata})

        return products

    # ==========================================================================
    # Link Generation
    # ==========================================================================

    def get_amazon_link(self, product_id: str = None, asin: str = None,
                        search_term: str = None) -> str:
        """
        Generate Amazon affiliate link.

        Args:
            product_id: Product ID from our database
            asin: Direct ASIN
            search_term: Search query for Amazon

        Returns:
            Affiliate link
        """
        if product_id and product_id in self.products:
            asin = self.products[product_id].get("asin")

        if asin:
            return f"https://www.amazon.com/dp/{asin}?tag={AMAZON_TAG}"

        if search_term:
            encoded_term = quote_plus(search_term)
            return f"https://www.amazon.com/s?k={encoded_term}&tag={AMAZON_TAG}"

        return f"https://www.amazon.com?tag={AMAZON_TAG}"

    def get_clickbank_link(self, vendor: str, product_id: str = None) -> str:
        """Generate ClickBank affiliate link."""
        if not CLICKBANK_NICKNAME:
            logger.warning("ClickBank nickname not configured")
            return ""

        return f"https://{CLICKBANK_NICKNAME}.{vendor}.hop.clickbank.net"

    def get_product_link(self, product_id: str) -> str:
        """Get the appropriate affiliate link for a product."""
        if product_id not in self.products:
            return ""

        product = self.products[product_id]
        platform = product.get("platform", "amazon")

        if platform == "amazon":
            return self.get_amazon_link(product_id=product_id)
        elif platform == "clickbank":
            return self.get_clickbank_link(product.get("vendor", ""))

        return ""

    # ==========================================================================
    # Campaign Management
    # ==========================================================================

    def get_current_campaign(self) -> Optional[Dict]:
        """Get the current active campaign based on date."""
        now = datetime.now()
        month = now.month
        day = now.day

        # Check special campaigns first (like Black Friday)
        for campaign_id, campaign in self.campaigns.items():
            if "days" in campaign:
                if month in campaign.get("months", []) and day in campaign.get("days", []):
                    return {"id": campaign_id, **campaign}

        # Check seasonal campaigns
        for campaign_id, campaign in self.campaigns.items():
            if "days" not in campaign:  # Not a special campaign
                if month in campaign.get("months", []):
                    return {"id": campaign_id, **campaign}

        return None

    def get_campaign_products(self, campaign_id: str = None) -> List[Dict]:
        """Get products featured in a campaign."""
        if not campaign_id:
            campaign = self.get_current_campaign()
            if not campaign:
                return self.get_seasonal_products()
            campaign_id = campaign["id"]

        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            return []

        featured_categories = campaign.get("featured_categories", ["all"])

        if "all" in featured_categories:
            return [{"id": pid, **pdata}
                   for pid, pdata in self.products.items()
                   if pdata.get("active", True)]

        products = []
        for pid, pdata in self.products.items():
            if pdata.get("active", True):
                if pdata.get("category") in featured_categories:
                    products.append({"id": pid, **pdata})

        return products

    def get_campaign_hook(self, campaign_id: str = None) -> str:
        """Get a random hook for the current campaign."""
        import random

        if not campaign_id:
            campaign = self.get_current_campaign()
            if not campaign:
                return "Improve your sleep tonight!"
            campaign_id = campaign["id"]

        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            return "Improve your sleep tonight!"

        hooks = campaign.get("hooks", ["Improve your sleep tonight!"])
        return random.choice(hooks)

    # ==========================================================================
    # Content Generation Helpers
    # ==========================================================================

    def get_product_content_block(self, product_id: str) -> str:
        """
        Generate a content block for a product (for articles/posts).

        Returns:
            Formatted product recommendation text
        """
        if product_id not in self.products:
            return ""

        product = self.products[product_id]
        link = self.get_product_link(product_id)

        content = f"""
**{product['name']}** - {product.get('price_range', 'Check price')}

{', '.join(product.get('best_for', []))}

Rating: {'*' * int(product.get('rating', 4.5))} ({product.get('reviews', 0):,} reviews)

[Check Current Price]({link})
"""
        return content.strip()

    def get_comparison_table(self, product_ids: List[str]) -> str:
        """
        Generate a comparison table for multiple products.

        Returns:
            Markdown table
        """
        if not product_ids:
            return ""

        headers = ["Product", "Price", "Rating", "Best For", "Link"]
        rows = []

        for pid in product_ids:
            if pid not in self.products:
                continue

            p = self.products[pid]
            link = self.get_product_link(pid)
            rows.append([
                p["name"],
                p.get("price_range", "N/A"),
                f"{p.get('rating', 'N/A')}/5",
                ", ".join(p.get("best_for", [])[:2]),
                f"[View]({link})"
            ])

        if not rows:
            return ""

        # Build table
        table = "| " + " | ".join(headers) + " |\n"
        table += "| " + " | ".join(["---"] * len(headers)) + " |\n"
        for row in rows:
            table += "| " + " | ".join(row) + " |\n"

        return table

    # ==========================================================================
    # Statistics
    # ==========================================================================

    def log_click(self, product_id: str, source: str = "unknown"):
        """Log an affiliate link click."""
        stats = self._load_stats()

        today = datetime.now().strftime("%Y-%m-%d")

        if today not in stats:
            stats[today] = {}

        if product_id not in stats[today]:
            stats[today][product_id] = {"clicks": 0, "sources": {}}

        stats[today][product_id]["clicks"] += 1
        stats[today][product_id]["sources"][source] = \
            stats[today][product_id]["sources"].get(source, 0) + 1

        self._save_stats(stats)

    def _load_stats(self) -> Dict:
        """Load click statistics."""
        if self.stats_file.exists():
            try:
                with open(self.stats_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
        return {}

    def _save_stats(self, stats: Dict):
        """Save click statistics."""
        self.stats_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.stats_file, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2)

    def get_stats_summary(self, days: int = 7) -> Dict:
        """Get statistics summary for the last N days."""
        stats = self._load_stats()

        from datetime import timedelta
        summary = {
            "total_clicks": 0,
            "top_products": {},
            "by_source": {}
        }

        cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        for date, products in stats.items():
            if date >= cutoff:
                for product_id, data in products.items():
                    clicks = data.get("clicks", 0)
                    summary["total_clicks"] += clicks

                    if product_id not in summary["top_products"]:
                        summary["top_products"][product_id] = 0
                    summary["top_products"][product_id] += clicks

                    for source, count in data.get("sources", {}).items():
                        if source not in summary["by_source"]:
                            summary["by_source"][source] = 0
                        summary["by_source"][source] += count

        # Sort top products
        summary["top_products"] = dict(
            sorted(summary["top_products"].items(),
                   key=lambda x: x[1], reverse=True)[:10]
        )

        return summary


# =============================================================================
# Standalone test
# =============================================================================
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    manager = AffiliateManager()

    print("\n=== Affiliate Manager ===\n")

    # Show product count
    print(f"Total products: {len(manager.products)}")

    # Get current campaign
    campaign = manager.get_current_campaign()
    if campaign:
        print(f"\nCurrent campaign: {campaign['name']}")
        print(f"Hook: {manager.get_campaign_hook()}")

    # Show seasonal products
    products = manager.get_seasonal_products()
    print(f"\nSeasonal products: {len(products)}")

    # Show sample links
    print("\n=== Sample Links ===")
    for pid in list(manager.products.keys())[:3]:
        print(f"{manager.products[pid]['name']}")
        print(f"  Link: {manager.get_product_link(pid)}")
        print()

    # Show comparison table
    print("\n=== Comparison Table ===")
    weighted_blankets = [p["id"] for p in manager.get_products_by_category("weighted_blankets")]
    print(manager.get_comparison_table(weighted_blankets))
