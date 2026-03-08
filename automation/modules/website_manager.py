"""
SleepWise Automation Agent - Website Manager
Handles article generation and website updates.
"""

import logging
import json
import re
import os
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime, timezone
from xml.etree import ElementTree as ET

import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import (
    PROJECT_ROOT, POSTS_DIR, PAGES_DIR, TEMPLATES_DIR,
    WEBSITE_CONFIG, DATA_DIR
)

logger = logging.getLogger(__name__)


class WebsiteManager:
    """Manages website content and updates."""

    def __init__(self):
        """Initialize the website manager."""
        self.posts_dir = POSTS_DIR
        self.pages_dir = PAGES_DIR
        self.templates_dir = TEMPLATES_DIR
        self.project_root = PROJECT_ROOT
        self.base_url = WEBSITE_CONFIG["base_url"]

        # Ensure directories exist
        self.posts_dir.mkdir(parents=True, exist_ok=True)
        self.pages_dir.mkdir(parents=True, exist_ok=True)

    # ==========================================================================
    # Article Management
    # ==========================================================================

    def create_article(self, article_data: dict, template: str = None) -> dict:
        """
        Create a new article HTML file.

        Args:
            article_data: Article content and metadata
            template: Optional custom template HTML

        Returns:
            Result with file path and URL
        """
        try:
            # Generate slug from title
            title = article_data.get("title", "Untitled Article")
            slug = self._generate_slug(title)

            # Get or load template
            if not template:
                template = self._load_template()

            # Generate HTML content
            html_content = self._render_article(article_data, template)

            # Save the file
            filename = f"{slug}.html"
            filepath = self.posts_dir / filename

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html_content)

            logger.info(f"Article created: {filepath}")

            # Update sitemap
            article_url = f"{self.base_url}/posts/{filename}"
            self.update_sitemap(article_url)

            return {
                "ok": True,
                "filepath": str(filepath),
                "filename": filename,
                "url": article_url,
                "slug": slug
            }

        except Exception as e:
            logger.error(f"Failed to create article: {e}")
            return {"ok": False, "error": str(e)}

    def _generate_slug(self, title: str) -> str:
        """Generate URL-friendly slug from title."""
        # Convert to lowercase and replace spaces with hyphens
        slug = title.lower().strip()
        # Remove special characters
        slug = re.sub(r'[^\w\s-]', '', slug)
        # Replace spaces with hyphens
        slug = re.sub(r'[\s_]+', '-', slug)
        # Remove multiple hyphens
        slug = re.sub(r'-+', '-', slug)
        # Add date prefix for uniqueness
        date_prefix = datetime.now().strftime("%Y-%m-%d")
        return f"{date_prefix}-{slug}"

    def _load_template(self) -> str:
        """Load the article template."""
        template_path = self.templates_dir / "article_template.html"

        if template_path.exists():
            with open(template_path, "r", encoding="utf-8") as f:
                return f.read()

        # Return a basic template if file doesn't exist
        return self._get_default_template()

    def _get_default_template(self) -> str:
        """Get default article template."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{{META_DESCRIPTION}}">
    <meta name="keywords" content="{{KEYWORDS}}">
    <title>{{TITLE}} | SleepWise Reviews</title>
    <link rel="canonical" href="{{CANONICAL_URL}}">

    <!-- Open Graph / Social Media -->
    <meta property="og:title" content="{{TITLE}}">
    <meta property="og:description" content="{{META_DESCRIPTION}}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{{CANONICAL_URL}}">

    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.7;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        header { margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 1px solid #eee; }
        h1 { font-size: 2.2rem; margin-bottom: 0.5rem; color: #1a1a2e; }
        .meta { color: #666; font-size: 0.9rem; }
        h2 { margin: 2rem 0 1rem; color: #1a1a2e; }
        h3 { margin: 1.5rem 0 0.75rem; color: #333; }
        p { margin-bottom: 1rem; }
        .faq { background: #f8f9fa; padding: 1.5rem; border-radius: 8px; margin: 2rem 0; }
        .faq h3 { margin-top: 0; }
        .faq-item { margin-bottom: 1rem; }
        .faq-item strong { color: #1a1a2e; }
        footer { margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #eee; color: #666; }
    </style>
</head>
<body>
    <header>
        <h1>{{TITLE}}</h1>
        <p class="meta">Published on {{DATE}} | {{READ_TIME}} min read</p>
    </header>

    <article>
        {{CONTENT}}
    </article>

    {{FAQ_SECTION}}

    <footer>
        <p>&copy; {{YEAR}} SleepWise Reviews. All rights reserved.</p>
    </footer>
</body>
</html>"""

    def _render_article(self, article_data: dict, template: str) -> str:
        """
        Render article data into HTML template.

        Args:
            article_data: Article content and metadata
            template: HTML template string

        Returns:
            Rendered HTML
        """
        # Extract data
        title = article_data.get("title", "Untitled")
        meta_desc = article_data.get("meta_description", "")
        keywords = article_data.get("keywords", [])
        introduction = article_data.get("introduction", "")
        sections = article_data.get("sections", [])
        conclusion = article_data.get("conclusion", "")
        faq = article_data.get("faq", [])

        # Build content HTML
        content_parts = []

        # Introduction
        if introduction:
            content_parts.append(f"<p>{introduction}</p>")

        # Sections
        for section in sections:
            content_parts.append(f"<h2>{section.get('heading', '')}</h2>")
            content_parts.append(f"<p>{section.get('content', '')}</p>")

            # Subsections
            for subsection in section.get("subsections", []):
                content_parts.append(f"<h3>{subsection.get('heading', '')}</h3>")
                content_parts.append(f"<p>{subsection.get('content', '')}</p>")

        # Conclusion
        if conclusion:
            content_parts.append("<h2>Conclusion</h2>")
            content_parts.append(f"<p>{conclusion}</p>")

        content_html = "\n".join(content_parts)

        # FAQ Section
        faq_html = ""
        if faq:
            faq_items = []
            for item in faq:
                faq_items.append(
                    f'<div class="faq-item">'
                    f'<strong>Q: {item.get("question", "")}</strong>'
                    f'<p>A: {item.get("answer", "")}</p>'
                    f'</div>'
                )
            faq_html = f'<div class="faq"><h2>Frequently Asked Questions</h2>{"".join(faq_items)}</div>'

        # Calculate read time (average 200 words per minute)
        word_count = len(content_html.split())
        read_time = max(1, round(word_count / 200))

        # Generate slug and URL
        slug = self._generate_slug(title)
        canonical_url = f"{self.base_url}/posts/{slug}.html"

        # Replace placeholders
        now = datetime.now()
        html = template
        replacements = {
            "{{TITLE}}": title,
            "{{META_DESCRIPTION}}": meta_desc,
            "{{KEYWORDS}}": ", ".join(keywords),
            "{{CANONICAL_URL}}": canonical_url,
            "{{DATE}}": now.strftime("%B %d, %Y"),
            "{{YEAR}}": str(now.year),
            "{{READ_TIME}}": str(read_time),
            "{{CONTENT}}": content_html,
            "{{FAQ_SECTION}}": faq_html
        }

        for placeholder, value in replacements.items():
            html = html.replace(placeholder, value)

        return html

    # ==========================================================================
    # Sitemap Management
    # ==========================================================================

    def update_sitemap(self, new_url: str = None) -> dict:
        """
        Update the sitemap with a new URL or regenerate completely.

        Args:
            new_url: Optional new URL to add

        Returns:
            Result of operation
        """
        sitemap_path = self.project_root / "sitemap.xml"

        try:
            # Load existing sitemap or create new
            if sitemap_path.exists():
                tree = ET.parse(sitemap_path)
                root = tree.getroot()
            else:
                root = ET.Element("urlset")
                root.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

            # Define namespace
            ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

            # Check if URL already exists
            if new_url:
                existing_urls = [
                    elem.text for elem in root.findall(".//sm:loc", ns)
                ] if root.findall(".//sm:loc", ns) else [
                    elem.text for elem in root.findall(".//loc")
                ]

                if new_url not in existing_urls:
                    url_elem = ET.SubElement(root, "url")
                    loc = ET.SubElement(url_elem, "loc")
                    loc.text = new_url
                    lastmod = ET.SubElement(url_elem, "lastmod")
                    lastmod.text = datetime.now().strftime("%Y-%m-%d")
                    changefreq = ET.SubElement(url_elem, "changefreq")
                    changefreq.text = "weekly"

            # Write sitemap
            tree = ET.ElementTree(root)
            with open(sitemap_path, "wb") as f:
                tree.write(f, encoding="utf-8", xml_declaration=True)

            logger.info(f"Sitemap updated: {sitemap_path}")
            return {"ok": True, "path": str(sitemap_path)}

        except Exception as e:
            logger.error(f"Failed to update sitemap: {e}")
            return {"ok": False, "error": str(e)}

    def regenerate_sitemap(self) -> dict:
        """Regenerate sitemap from all HTML files."""
        try:
            root = ET.Element("urlset")
            root.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

            # Add homepage
            self._add_sitemap_url(root, self.base_url, "daily", "1.0")

            # Add all posts
            if self.posts_dir.exists():
                for html_file in self.posts_dir.glob("*.html"):
                    url = f"{self.base_url}/posts/{html_file.name}"
                    self._add_sitemap_url(root, url, "weekly", "0.8")

            # Add all pages
            if self.pages_dir.exists():
                for html_file in self.pages_dir.glob("*.html"):
                    url = f"{self.base_url}/pages/{html_file.name}"
                    self._add_sitemap_url(root, url, "monthly", "0.6")

            # Write sitemap
            sitemap_path = self.project_root / "sitemap.xml"
            tree = ET.ElementTree(root)
            with open(sitemap_path, "wb") as f:
                tree.write(f, encoding="utf-8", xml_declaration=True)

            url_count = len(root.findall(".//url"))
            logger.info(f"Sitemap regenerated with {url_count} URLs")
            return {"ok": True, "url_count": url_count}

        except Exception as e:
            logger.error(f"Failed to regenerate sitemap: {e}")
            return {"ok": False, "error": str(e)}

    def _add_sitemap_url(self, root: ET.Element, url: str,
                         changefreq: str, priority: str):
        """Add a URL entry to sitemap."""
        url_elem = ET.SubElement(root, "url")
        loc = ET.SubElement(url_elem, "loc")
        loc.text = url
        lastmod = ET.SubElement(url_elem, "lastmod")
        lastmod.text = datetime.now().strftime("%Y-%m-%d")
        cf = ET.SubElement(url_elem, "changefreq")
        cf.text = changefreq
        prio = ET.SubElement(url_elem, "priority")
        prio.text = priority

    # ==========================================================================
    # Content Inventory
    # ==========================================================================

    def get_all_articles(self) -> List[dict]:
        """Get list of all articles with metadata."""
        articles = []

        if self.posts_dir.exists():
            for html_file in self.posts_dir.glob("*.html"):
                stat = html_file.stat()
                articles.append({
                    "filename": html_file.name,
                    "path": str(html_file),
                    "url": f"{self.base_url}/posts/{html_file.name}",
                    "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "size": stat.st_size
                })

        # Sort by modified date, newest first
        articles.sort(key=lambda x: x["modified"], reverse=True)
        return articles

    def get_article_count(self) -> int:
        """Get total number of articles."""
        if self.posts_dir.exists():
            return len(list(self.posts_dir.glob("*.html")))
        return 0

    def get_recent_articles(self, count: int = 5) -> List[dict]:
        """Get the most recent articles."""
        articles = self.get_all_articles()
        return articles[:count]

    # ==========================================================================
    # Image Management
    # ==========================================================================

    def get_available_images(self) -> List[dict]:
        """Get list of available images in the project."""
        images = []
        image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

        for ext in image_extensions:
            for img_path in self.project_root.glob(f"*{ext}"):
                images.append({
                    "filename": img_path.name,
                    "path": str(img_path),
                    "url": f"{self.base_url}/{img_path.name}"
                })

        return images

    def select_image_for_article(self, keywords: List[str]) -> Optional[str]:
        """
        Select an appropriate image based on keywords.

        Args:
            keywords: Article keywords

        Returns:
            Image URL or None
        """
        images = self.get_available_images()

        if not images:
            return None

        # Try to match keywords in image filenames
        for keyword in keywords:
            keyword_lower = keyword.lower().replace(" ", "-")
            for img in images:
                if keyword_lower in img["filename"].lower():
                    return img["url"]

        # Return first available image as fallback
        return images[0]["url"] if images else None


# =============================================================================
# Standalone test
# =============================================================================
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    manager = WebsiteManager()

    print(f"Posts directory: {manager.posts_dir}")
    print(f"Pages directory: {manager.pages_dir}")
    print(f"Article count: {manager.get_article_count()}")

    recent = manager.get_recent_articles(3)
    print(f"\nRecent articles:")
    for article in recent:
        print(f"  - {article['filename']}")
