"""
SleepWise Automation Agent - Image Generator
Creates branded social media images using Pillow.
"""

import logging
from pathlib import Path
from typing import Optional, Tuple, List
from datetime import datetime
import textwrap

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Pillow not installed. Run: pip install Pillow")

import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import PROJECT_ROOT, DATA_DIR

logger = logging.getLogger(__name__)


# Brand colors
BRAND_COLORS = {
    "primary": "#1a1a2e",      # Dark navy
    "secondary": "#16213e",     # Darker blue
    "accent": "#d4af37",        # Gold
    "text_light": "#ffffff",    # White
    "text_muted": "#b8b8b8",    # Light gray
    "gradient_start": "#1a1a2e",
    "gradient_end": "#0f0f1a"
}

# Image dimensions
DIMENSIONS = {
    "instagram_square": (1080, 1080),
    "instagram_portrait": (1080, 1350),
    "instagram_story": (1080, 1920),
    "pinterest": (1000, 1500),
    "twitter": (1200, 675)
}


class ImageGenerator:
    """Generates branded social media images."""

    def __init__(self):
        """Initialize image generator."""
        self.output_dir = DATA_DIR / "images"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Font paths (will use default if not found)
        self.fonts_dir = PROJECT_ROOT / "assets" / "fonts"

        # Load fonts
        self._load_fonts()

    def _load_fonts(self):
        """Load or fallback to default fonts."""
        self.fonts = {}

        if not PIL_AVAILABLE:
            return

        try:
            # Try to load custom fonts
            font_files = {
                "title": "Montserrat-Bold.ttf",
                "subtitle": "Montserrat-SemiBold.ttf",
                "body": "OpenSans-Regular.ttf",
                "accent": "Montserrat-Medium.ttf"
            }

            for font_name, font_file in font_files.items():
                font_path = self.fonts_dir / font_file
                if font_path.exists():
                    self.fonts[font_name] = str(font_path)
                else:
                    self.fonts[font_name] = None  # Will use default

        except Exception as e:
            logger.warning(f"Could not load custom fonts: {e}")
            self.fonts = {k: None for k in ["title", "subtitle", "body", "accent"]}

    def _get_font(self, font_name: str, size: int) -> "ImageFont":
        """Get font with fallback to default."""
        if not PIL_AVAILABLE:
            return None

        font_path = self.fonts.get(font_name)

        try:
            if font_path:
                return ImageFont.truetype(font_path, size)
            else:
                # Try system fonts
                system_fonts = [
                    "arial.ttf",
                    "Arial.ttf",
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                    "C:/Windows/Fonts/arial.ttf"
                ]
                for sys_font in system_fonts:
                    try:
                        return ImageFont.truetype(sys_font, size)
                    except (OSError, IOError):
                        continue

                # Final fallback
                return ImageFont.load_default()

        except Exception:
            return ImageFont.load_default()

    def _create_gradient_background(self, size: Tuple[int, int],
                                    color1: str = None, color2: str = None) -> Image.Image:
        """Create gradient background."""
        if not PIL_AVAILABLE:
            return None

        width, height = size
        color1 = color1 or BRAND_COLORS["gradient_start"]
        color2 = color2 or BRAND_COLORS["gradient_end"]

        # Convert hex to RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        rgb1 = hex_to_rgb(color1)
        rgb2 = hex_to_rgb(color2)

        # Create gradient
        image = Image.new("RGB", size)
        pixels = image.load()

        for y in range(height):
            ratio = y / height
            r = int(rgb1[0] * (1 - ratio) + rgb2[0] * ratio)
            g = int(rgb1[1] * (1 - ratio) + rgb2[1] * ratio)
            b = int(rgb1[2] * (1 - ratio) + rgb2[2] * ratio)

            for x in range(width):
                pixels[x, y] = (r, g, b)

        return image

    def _wrap_text(self, text: str, max_chars: int = 30) -> List[str]:
        """Wrap text to fit in image."""
        return textwrap.wrap(text, width=max_chars)

    # ==========================================================================
    # Post Image Generators
    # ==========================================================================

    def create_quote_image(self, quote: str, author: str = "SleepWise",
                           size: str = "instagram_square",
                           output_name: str = None) -> Optional[str]:
        """
        Create a quote image with branded styling.

        Args:
            quote: The quote text
            author: Quote attribution
            size: Image size preset
            output_name: Custom output filename

        Returns:
            Path to generated image
        """
        if not PIL_AVAILABLE:
            logger.error("Pillow not installed")
            return None

        dimensions = DIMENSIONS.get(size, DIMENSIONS["instagram_square"])

        # Create background
        image = self._create_gradient_background(dimensions)
        draw = ImageDraw.Draw(image)

        width, height = dimensions

        # Add decorative elements
        accent_color = BRAND_COLORS["accent"]

        # Top accent line
        draw.rectangle(
            [(width * 0.1, height * 0.12), (width * 0.9, height * 0.125)],
            fill=accent_color
        )

        # Quote marks
        quote_font = self._get_font("accent", 120)
        draw.text((width * 0.1, height * 0.15), '"', font=quote_font, fill=accent_color)

        # Quote text
        title_font = self._get_font("title", 60)
        wrapped_quote = self._wrap_text(quote, max_chars=25)

        y_position = height * 0.3
        line_height = 80

        for line in wrapped_quote:
            # Center each line
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            x_position = (width - text_width) / 2

            draw.text((x_position, y_position), line,
                     font=title_font, fill=BRAND_COLORS["text_light"])
            y_position += line_height

        # Closing quote
        draw.text((width * 0.85, y_position - 40), '"',
                 font=quote_font, fill=accent_color)

        # Author
        author_font = self._get_font("subtitle", 36)
        author_text = f"- {author}"
        bbox = draw.textbbox((0, 0), author_text, font=author_font)
        author_width = bbox[2] - bbox[0]

        draw.text(((width - author_width) / 2, height * 0.75),
                 author_text, font=author_font, fill=BRAND_COLORS["text_muted"])

        # Bottom accent line
        draw.rectangle(
            [(width * 0.1, height * 0.88), (width * 0.9, height * 0.885)],
            fill=accent_color
        )

        # Branding
        brand_font = self._get_font("accent", 28)
        brand_text = "@sleepwisereviews"
        bbox = draw.textbbox((0, 0), brand_text, font=brand_font)
        brand_width = bbox[2] - bbox[0]

        draw.text(((width - brand_width) / 2, height * 0.92),
                 brand_text, font=brand_font, fill=BRAND_COLORS["text_muted"])

        # Save
        output_name = output_name or f"quote_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        output_path = self.output_dir / output_name
        image.save(output_path, "PNG", quality=95)

        logger.info(f"Created quote image: {output_path}")
        return str(output_path)

    def create_tip_image(self, tip_number: int, tip_text: str,
                         title: str = "Sleep Tip",
                         size: str = "instagram_square",
                         output_name: str = None) -> Optional[str]:
        """
        Create a numbered tip image.

        Args:
            tip_number: Tip number to display
            tip_text: The tip content
            title: Header title
            size: Image size preset
            output_name: Custom output filename

        Returns:
            Path to generated image
        """
        if not PIL_AVAILABLE:
            logger.error("Pillow not installed")
            return None

        dimensions = DIMENSIONS.get(size, DIMENSIONS["instagram_square"])
        image = self._create_gradient_background(dimensions)
        draw = ImageDraw.Draw(image)

        width, height = dimensions
        accent_color = BRAND_COLORS["accent"]

        # Header
        header_font = self._get_font("subtitle", 40)
        draw.text((width * 0.1, height * 0.08), title.upper(),
                 font=header_font, fill=accent_color)

        # Large tip number
        number_font = self._get_font("title", 200)
        number_text = f"#{tip_number:02d}"
        draw.text((width * 0.1, height * 0.15), number_text,
                 font=number_font, fill=BRAND_COLORS["text_light"])

        # Horizontal line
        draw.rectangle(
            [(width * 0.1, height * 0.45), (width * 0.9, height * 0.455)],
            fill=accent_color
        )

        # Tip text
        tip_font = self._get_font("body", 48)
        wrapped_tip = self._wrap_text(tip_text, max_chars=30)

        y_position = height * 0.5
        line_height = 65

        for line in wrapped_tip:
            draw.text((width * 0.1, y_position), line,
                     font=tip_font, fill=BRAND_COLORS["text_light"])
            y_position += line_height

        # Branding
        brand_font = self._get_font("accent", 28)
        brand_text = "sleepwisereviews.com"
        draw.text((width * 0.1, height * 0.9), brand_text,
                 font=brand_font, fill=BRAND_COLORS["text_muted"])

        # Moon emoji/icon area
        moon_font = self._get_font("title", 80)
        draw.text((width * 0.85, height * 0.88), "",
                 font=moon_font, fill=accent_color)

        # Save
        output_name = output_name or f"tip_{tip_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        output_path = self.output_dir / output_name
        image.save(output_path, "PNG", quality=95)

        logger.info(f"Created tip image: {output_path}")
        return str(output_path)

    def create_carousel_cover(self, title: str, subtitle: str = None,
                              slide_count: int = 5,
                              size: str = "instagram_square",
                              output_name: str = None) -> Optional[str]:
        """
        Create a carousel cover slide.

        Args:
            title: Main title
            subtitle: Optional subtitle
            slide_count: Number of slides to indicate
            size: Image size preset
            output_name: Custom output filename

        Returns:
            Path to generated image
        """
        if not PIL_AVAILABLE:
            logger.error("Pillow not installed")
            return None

        dimensions = DIMENSIONS.get(size, DIMENSIONS["instagram_square"])
        image = self._create_gradient_background(dimensions)
        draw = ImageDraw.Draw(image)

        width, height = dimensions
        accent_color = BRAND_COLORS["accent"]

        # Slide indicator dots
        dot_radius = 8
        dot_spacing = 30
        total_dots_width = (slide_count - 1) * dot_spacing + dot_radius * 2
        start_x = (width - total_dots_width) / 2

        for i in range(slide_count):
            x = start_x + i * dot_spacing
            color = accent_color if i == 0 else BRAND_COLORS["text_muted"]
            draw.ellipse(
                [(x - dot_radius, height * 0.1 - dot_radius),
                 (x + dot_radius, height * 0.1 + dot_radius)],
                fill=color
            )

        # Title
        title_font = self._get_font("title", 72)
        wrapped_title = self._wrap_text(title, max_chars=18)

        y_position = height * 0.35
        line_height = 90

        for line in wrapped_title:
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            x_position = (width - text_width) / 2

            draw.text((x_position, y_position), line,
                     font=title_font, fill=BRAND_COLORS["text_light"])
            y_position += line_height

        # Subtitle
        if subtitle:
            subtitle_font = self._get_font("subtitle", 36)
            bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
            subtitle_width = bbox[2] - bbox[0]

            draw.text(((width - subtitle_width) / 2, height * 0.7),
                     subtitle, font=subtitle_font, fill=BRAND_COLORS["text_muted"])

        # Swipe indicator
        swipe_font = self._get_font("body", 28)
        swipe_text = "Swipe to learn more"
        bbox = draw.textbbox((0, 0), swipe_text, font=swipe_font)
        swipe_width = bbox[2] - bbox[0]

        draw.text(((width - swipe_width) / 2, height * 0.85),
                 swipe_text, font=swipe_font, fill=accent_color)

        # Arrow
        draw.text(((width + swipe_width) / 2 + 20, height * 0.85),
                 ">", font=swipe_font, fill=accent_color)

        # Branding
        brand_font = self._get_font("accent", 24)
        brand_text = "@sleepwisereviews"
        bbox = draw.textbbox((0, 0), brand_text, font=brand_font)
        brand_width = bbox[2] - bbox[0]

        draw.text(((width - brand_width) / 2, height * 0.93),
                 brand_text, font=brand_font, fill=BRAND_COLORS["text_muted"])

        # Save
        output_name = output_name or f"carousel_cover_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        output_path = self.output_dir / output_name
        image.save(output_path, "PNG", quality=95)

        logger.info(f"Created carousel cover: {output_path}")
        return str(output_path)

    def create_stat_image(self, stat: str, description: str,
                          source: str = None,
                          size: str = "instagram_square",
                          output_name: str = None) -> Optional[str]:
        """
        Create a statistic/fact image.

        Args:
            stat: The statistic (e.g., "73%", "8 hours")
            description: What the stat means
            source: Optional source citation
            size: Image size preset
            output_name: Custom output filename

        Returns:
            Path to generated image
        """
        if not PIL_AVAILABLE:
            logger.error("Pillow not installed")
            return None

        dimensions = DIMENSIONS.get(size, DIMENSIONS["instagram_square"])
        image = self._create_gradient_background(dimensions)
        draw = ImageDraw.Draw(image)

        width, height = dimensions
        accent_color = BRAND_COLORS["accent"]

        # Large stat number
        stat_font = self._get_font("title", 180)
        bbox = draw.textbbox((0, 0), stat, font=stat_font)
        stat_width = bbox[2] - bbox[0]

        draw.text(((width - stat_width) / 2, height * 0.25), stat,
                 font=stat_font, fill=accent_color)

        # Description
        desc_font = self._get_font("subtitle", 44)
        wrapped_desc = self._wrap_text(description, max_chars=28)

        y_position = height * 0.55
        line_height = 60

        for line in wrapped_desc:
            bbox = draw.textbbox((0, 0), line, font=desc_font)
            text_width = bbox[2] - bbox[0]
            x_position = (width - text_width) / 2

            draw.text((x_position, y_position), line,
                     font=desc_font, fill=BRAND_COLORS["text_light"])
            y_position += line_height

        # Source
        if source:
            source_font = self._get_font("body", 24)
            source_text = f"Source: {source}"
            bbox = draw.textbbox((0, 0), source_text, font=source_font)
            source_width = bbox[2] - bbox[0]

            draw.text(((width - source_width) / 2, height * 0.82),
                     source_text, font=source_font, fill=BRAND_COLORS["text_muted"])

        # Branding
        brand_font = self._get_font("accent", 28)
        brand_text = "@sleepwisereviews"
        bbox = draw.textbbox((0, 0), brand_text, font=brand_font)
        brand_width = bbox[2] - bbox[0]

        draw.text(((width - brand_width) / 2, height * 0.92),
                 brand_text, font=brand_font, fill=BRAND_COLORS["text_muted"])

        # Save
        output_name = output_name or f"stat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        output_path = self.output_dir / output_name
        image.save(output_path, "PNG", quality=95)

        logger.info(f"Created stat image: {output_path}")
        return str(output_path)

    # ==========================================================================
    # Batch Generation
    # ==========================================================================

    def generate_weekly_images(self) -> List[str]:
        """
        Generate a week's worth of images.

        Returns:
            List of generated image paths
        """
        images = []

        # Quote images
        quotes = [
            ("Sleep is the best meditation.", "Dalai Lama"),
            ("A good laugh and a long sleep are the best cures.", "Irish Proverb"),
            ("Sleep is the golden chain that ties health and our bodies together.", "Thomas Dekker")
        ]

        for i, (quote, author) in enumerate(quotes):
            path = self.create_quote_image(quote, author, output_name=f"weekly_quote_{i+1}.png")
            if path:
                images.append(path)

        # Tip images
        tips = [
            "Keep your bedroom between 65-68F for optimal sleep",
            "Avoid screens 1 hour before bedtime",
            "Exercise daily, but finish 3+ hours before bed",
            "Use a weighted blanket to reduce anxiety"
        ]

        for i, tip in enumerate(tips, 1):
            path = self.create_tip_image(i, tip, output_name=f"weekly_tip_{i}.png")
            if path:
                images.append(path)

        # Stat images
        stats = [
            ("73%", "of people with weighted blankets report better sleep", "Journal of Sleep Medicine"),
            ("22 min", "faster sleep onset with proper bedroom temperature", "Sleep Foundation")
        ]

        for i, (stat, desc, source) in enumerate(stats, 1):
            path = self.create_stat_image(stat, desc, source, output_name=f"weekly_stat_{i}.png")
            if path:
                images.append(path)

        logger.info(f"Generated {len(images)} weekly images")
        return images


# =============================================================================
# Standalone test
# =============================================================================
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    if not PIL_AVAILABLE:
        print("Please install Pillow: pip install Pillow")
        exit(1)

    generator = ImageGenerator()

    print("Generating sample images...")

    # Test quote image
    quote_path = generator.create_quote_image(
        "Sleep is the best meditation",
        "Dalai Lama"
    )
    if quote_path:
        print(f"Quote image: {quote_path}")

    # Test tip image
    tip_path = generator.create_tip_image(
        1,
        "Keep your bedroom between 65-68F for optimal sleep quality"
    )
    if tip_path:
        print(f"Tip image: {tip_path}")

    # Test carousel cover
    carousel_path = generator.create_carousel_cover(
        "5 Sleep Tips You Need",
        "Backed by science"
    )
    if carousel_path:
        print(f"Carousel cover: {carousel_path}")

    # Test stat image
    stat_path = generator.create_stat_image(
        "73%",
        "of weighted blanket users report improved sleep quality",
        "Sleep Medicine Journal"
    )
    if stat_path:
        print(f"Stat image: {stat_path}")

    print(f"\nImages saved to: {generator.output_dir}")
