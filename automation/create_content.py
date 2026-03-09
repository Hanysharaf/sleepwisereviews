"""
SleepWise Content Creator
Creates Pinterest pins and Instagram posts from tips
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os
from datetime import datetime

# Output directory
OUTPUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Colors - Nocturnal Serenity palette
DEEP_INDIGO = (26, 26, 64)
SOFT_LAVENDER = (147, 129, 186)
WARM_AMBER = (255, 191, 128)
LIGHT_AMBER = (255, 220, 180)
BRIGHT_AMBER = (255, 235, 200)
CREAM = (250, 248, 245)
MIDNIGHT = (15, 15, 35)
MUTED_LAVENDER = (100, 90, 130)


def load_font(name, size):
    """Load font with fallbacks."""
    windows_fonts = r"C:\Windows\Fonts"
    font_map = {
        "display": ["georgiab.ttf", "timesbd.ttf"],
        "subtitle": ["arialbd.ttf", "calibrib.ttf"],
        "body": ["arial.ttf", "calibri.ttf"],
        "accent": ["georgiai.ttf", "timesi.ttf"],
        "light": ["ariali.ttf", "calibrili.ttf"],
    }
    if name in font_map:
        for f in font_map[name]:
            try:
                return ImageFont.truetype(os.path.join(windows_fonts, f), size)
            except:
                continue
    return ImageFont.load_default()


def draw_glowing_crescent(img, center_x, center_y, radius):
    """Draw a clean crescent moon with strong glow."""
    moon_size = int(radius * 3)
    moon_img = Image.new('RGBA', (moon_size, moon_size), (0, 0, 0, 0))
    moon_draw = ImageDraw.Draw(moon_img)
    cx = moon_size // 2
    cy = moon_size // 2

    # Glow layers
    glow_colors = [
        (255, 220, 160, 8),
        (255, 210, 150, 15),
        (255, 200, 140, 25),
        (255, 195, 135, 35),
        (255, 190, 130, 50),
    ]

    for i, (r, g, b, a) in enumerate(glow_colors):
        glow_radius = radius + 80 - i * 15
        moon_draw.ellipse(
            [cx - glow_radius, cy - glow_radius, cx + glow_radius, cy + glow_radius],
            fill=(r, g, b, a)
        )

    # Moon body gradient
    for r in range(int(radius), 0, -1):
        ratio = r / radius
        color_r = int(WARM_AMBER[0] + (BRIGHT_AMBER[0] - WARM_AMBER[0]) * (1 - ratio))
        color_g = int(WARM_AMBER[1] + (BRIGHT_AMBER[1] - WARM_AMBER[1]) * (1 - ratio))
        color_b = int(WARM_AMBER[2] + (BRIGHT_AMBER[2] - WARM_AMBER[2]) * (1 - ratio))
        moon_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(color_r, color_g, color_b, 255))

    # Crescent cut
    shadow_offset_x = radius * 0.4
    shadow_radius = radius * 0.85
    moon_draw.ellipse(
        [cx + shadow_offset_x - shadow_radius, cy - shadow_radius,
         cx + shadow_offset_x + shadow_radius, cy + shadow_radius],
        fill=(26, 26, 64, 255)
    )

    # Blur for glow effect
    moon_img = moon_img.filter(ImageFilter.GaussianBlur(radius=1))
    paste_x = int(center_x - moon_size // 2)
    paste_y = int(center_y - moon_size // 2)
    img.paste(moon_img, (paste_x, paste_y), moon_img)


def draw_stars(draw, positions):
    """Draw glowing stars."""
    for x, y, size in positions:
        for i in range(4, 0, -1):
            glow_size = size + i * 2
            draw.ellipse([x - glow_size, y - glow_size, x + glow_size, y + glow_size], fill=(180, 180, 200))
        draw.ellipse([x - size, y - size, x + size, y + size], fill=CREAM)


def draw_rings(draw, center_x, center_y, start_radius, count):
    """Draw concentric rings."""
    for i in range(count):
        radius = start_radius + i * 32
        draw.ellipse(
            [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
            outline=(90, 80, 130), width=1
        )


def wrap_text(text, font, max_width, draw):
    """Wrap text to fit within max_width."""
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    return lines


def create_pinterest_pin(tip_text, title="Sleep Tip", filename=None):
    """Create a Pinterest pin (1000x1500px)."""
    WIDTH, HEIGHT = 1000, 1500

    img = Image.new('RGBA', (WIDTH, HEIGHT), MIDNIGHT)
    draw = ImageDraw.Draw(img)

    # Gradient background
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(DEEP_INDIGO[0] * (1 - ratio) + MIDNIGHT[0] * ratio)
        g = int(DEEP_INDIGO[1] * (1 - ratio) + MIDNIGHT[1] * ratio)
        b = int(DEEP_INDIGO[2] * (1 - ratio) + MIDNIGHT[2] * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b, 255))

    # Fonts
    title_font = load_font("display", 72)
    body_font = load_font("body", 42)
    brand_font = load_font("subtitle", 36)
    tagline_font = load_font("accent", 28)

    moon_y = 280

    # Rings and moon
    draw_rings(draw, WIDTH // 2, moon_y, 160, 5)
    draw_glowing_crescent(img, WIDTH // 2, moon_y, 120)
    draw = ImageDraw.Draw(img)

    # Stars
    stars = [
        (80, 60, 3), (150, 140, 2), (60, 220, 2),
        (900, 80, 3), (940, 180, 2), (820, 50, 2),
        (100, 380, 2), (910, 360, 3),
    ]
    draw_stars(draw, stars)

    # Title
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - title_width) // 2, 480), title, font=title_font, fill=WARM_AMBER)

    # Decorative line
    draw.line([(200, 570), (800, 570)], fill=MUTED_LAVENDER, width=2)

    # Tip text - wrapped
    lines = wrap_text(tip_text, body_font, WIDTH - 120, draw)
    y_pos = 620
    line_height = 60

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=body_font)
        line_width = bbox[2] - bbox[0]
        draw.text(((WIDTH - line_width) // 2, y_pos), line, font=body_font, fill=CREAM)
        y_pos += line_height

    # Icon - thermometer representation (simple)
    icon_y = y_pos + 60
    # Draw temperature indicator
    draw.rounded_rectangle([WIDTH//2 - 30, icon_y, WIDTH//2 + 30, icon_y + 120], radius=15, fill=SOFT_LAVENDER)
    draw.ellipse([WIDTH//2 - 45, icon_y + 90, WIDTH//2 + 45, icon_y + 180], fill=WARM_AMBER)
    draw.rounded_rectangle([WIDTH//2 - 20, icon_y + 30, WIDTH//2 + 20, icon_y + 100], radius=10, fill=WARM_AMBER)

    # Temperature text
    temp_text = "65-68°F"
    temp_font = load_font("display", 56)
    bbox = draw.textbbox((0, 0), temp_text, font=temp_font)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, icon_y + 200), temp_text, font=temp_font, fill=WARM_AMBER)

    temp_c = "18-20°C"
    bbox = draw.textbbox((0, 0), temp_c, font=tagline_font)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, icon_y + 270), temp_c, font=tagline_font, fill=SOFT_LAVENDER)

    # Bottom section
    draw.line([(100, 1280), (WIDTH - 100, 1280)], fill=MUTED_LAVENDER, width=2)

    # CTA
    cta = "Save for better sleep tonight"
    bbox = draw.textbbox((0, 0), cta, font=tagline_font)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, 1320), cta, font=tagline_font, fill=SOFT_LAVENDER)

    # Brand
    brand = "SLEEPWISE"
    bbox = draw.textbbox((0, 0), brand, font=brand_font)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, 1380), brand, font=brand_font, fill=CREAM)

    # Mini moon
    draw.ellipse([WIDTH//2 - 10, 1440, WIDTH//2 + 10, 1460], fill=WARM_AMBER)
    draw.ellipse([WIDTH//2 - 4, 1438, WIDTH//2 + 12, 1458], fill=MIDNIGHT)

    # Save in dated folder
    today = datetime.now().strftime('%Y-%m-%d')
    if filename is None:
        filename = f"pinterest-pin-{datetime.now().strftime('%H%M%S')}.png"

    output_folder = os.path.join(OUTPUT_DIR, "content", today)
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, filename)

    final = img.convert('RGB')
    final.save(output_path, "PNG", quality=100)
    print(f"Pinterest pin saved: {output_path}")
    return output_path


def create_instagram_post(tip_text, title="Sleep Tip", filename=None):
    """Create an Instagram post (1080x1080px)."""
    WIDTH, HEIGHT = 1080, 1080

    img = Image.new('RGBA', (WIDTH, HEIGHT), MIDNIGHT)
    draw = ImageDraw.Draw(img)

    # Gradient background
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(DEEP_INDIGO[0] * (1 - ratio) + MIDNIGHT[0] * ratio)
        g = int(DEEP_INDIGO[1] * (1 - ratio) + MIDNIGHT[1] * ratio)
        b = int(DEEP_INDIGO[2] * (1 - ratio) + MIDNIGHT[2] * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b, 255))

    # Fonts
    title_font = load_font("display", 64)
    body_font = load_font("body", 38)
    brand_font = load_font("subtitle", 32)
    accent_font = load_font("accent", 28)

    moon_y = 200

    # Rings and moon (smaller for IG)
    draw_rings(draw, WIDTH // 2, moon_y, 120, 4)
    draw_glowing_crescent(img, WIDTH // 2, moon_y, 90)
    draw = ImageDraw.Draw(img)

    # Stars
    stars = [
        (70, 50, 2), (130, 120, 2), (950, 60, 2),
        (1000, 150, 2), (80, 300, 2), (1000, 280, 2),
    ]
    draw_stars(draw, stars)

    # Title
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - title_width) // 2, 350), title, font=title_font, fill=WARM_AMBER)

    # Decorative dots
    for i in range(3):
        x = WIDTH // 2 - 40 + i * 40
        draw.ellipse([x - 5, 430, x + 5, 440], fill=SOFT_LAVENDER)

    # Tip text - wrapped
    lines = wrap_text(tip_text, body_font, WIDTH - 100, draw)
    y_pos = 480
    line_height = 52

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=body_font)
        line_width = bbox[2] - bbox[0]
        draw.text(((WIDTH - line_width) // 2, y_pos), line, font=body_font, fill=CREAM)
        y_pos += line_height

    # Temperature highlight
    temp_y = y_pos + 40
    temp_text = "65-68°F / 18-20°C"
    temp_font = load_font("display", 48)
    bbox = draw.textbbox((0, 0), temp_text, font=temp_font)

    # Background pill for temperature
    pill_padding = 30
    pill_left = (WIDTH - (bbox[2] - bbox[0])) // 2 - pill_padding
    pill_right = (WIDTH + (bbox[2] - bbox[0])) // 2 + pill_padding
    draw.rounded_rectangle([pill_left, temp_y - 10, pill_right, temp_y + 70], radius=35, fill=WARM_AMBER)

    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, temp_y), temp_text, font=temp_font, fill=MIDNIGHT)

    # Bottom brand
    draw.line([(150, 950), (WIDTH - 150, 950)], fill=MUTED_LAVENDER, width=1)

    brand = "SLEEPWISE"
    bbox = draw.textbbox((0, 0), brand, font=brand_font)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, 980), brand, font=brand_font, fill=CREAM)

    # Mini moon
    draw.ellipse([WIDTH//2 - 8, 1030, WIDTH//2 + 8, 1046], fill=WARM_AMBER)
    draw.ellipse([WIDTH//2 - 3, 1028, WIDTH//2 + 10, 1044], fill=MIDNIGHT)

    # Save in dated folder
    today = datetime.now().strftime('%Y-%m-%d')
    if filename is None:
        filename = f"instagram-post-{datetime.now().strftime('%H%M%S')}.png"

    output_folder = os.path.join(OUTPUT_DIR, "content", today)
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, filename)

    final = img.convert('RGB')
    final.save(output_path, "PNG", quality=100)
    print(f"Instagram post saved: {output_path}")
    return output_path


def create_readme(folder_path, content_data):
    """Create a README with copy-paste content."""
    readme_path = os.path.join(folder_path, "README.txt")

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("SLEEPWISE CONTENT - " + datetime.now().strftime('%Y-%m-%d') + "\n")
        f.write("=" * 60 + "\n\n")

        # Pinterest section
        f.write("-" * 40 + "\n")
        f.write("PINTEREST\n")
        f.write("-" * 40 + "\n")
        f.write(f"File: {content_data['pinterest_file']}\n\n")
        f.write(f"Title: {content_data['pinterest_title']}\n\n")
        f.write(f"Description:\n{content_data['pinterest_desc']}\n\n")
        f.write(f"Board: Sleep Tips\n\n")
        f.write(f"Link: {content_data['product_link']}\n\n")

        # Instagram section
        f.write("-" * 40 + "\n")
        f.write("INSTAGRAM\n")
        f.write("-" * 40 + "\n")
        f.write(f"File: {content_data['instagram_file']}\n\n")
        f.write("Caption:\n")
        f.write(content_data['instagram_caption'] + "\n\n")
        f.write("Hashtags (paste in first comment):\n")
        f.write(content_data['hashtags'] + "\n\n")
        f.write(f"Bio Link: {content_data['product_link']}\n\n")

        # Checklist
        f.write("-" * 40 + "\n")
        f.write("CHECKLIST\n")
        f.write("-" * 40 + "\n")
        f.write("[ ] Upload Pinterest pin\n")
        f.write("[ ] Post to Instagram\n")
        f.write("[ ] Update bio link (if needed)\n")
        f.write("[ ] Reply to any comments\n")

    print(f"README created: {readme_path}")
    return readme_path


if __name__ == "__main__":
    # Today's content - Temperature tip
    tip = "Keep your bedroom at 65-68°F (18-20°C) for optimal sleep. Your body temperature needs to drop for quality rest."

    # Content data
    content_data = {
        'pinterest_title': 'Sleep Tip: Ideal Bedroom Temperature',
        'pinterest_desc': 'Keep your bedroom at 65-68°F (18-20°C) for optimal sleep. Your body temperature needs to drop for quality rest. Cool room = deeper sleep! #SleepTips #BetterSleep #SleepHacks',
        'instagram_caption': '''Did you know the ideal bedroom temperature for sleep is 65-68°F (18-20°C)?

Your body needs to cool down to fall asleep! Try lowering your thermostat tonight and see the difference.

The science: Your core body temperature naturally drops at night. A cool room helps this process, leading to deeper, more restful sleep.

Quick tips:
- Set thermostat to 65-68°F
- Use breathable bedding
- Consider a cooling mattress pad

Save this for better sleep tonight!''',
        'hashtags': '#SleepTips #BetterSleep #SleepScience #HealthySleep #SleepWell #RestfulNights #SleepHacks #WellnessJourney #SelfCare #NightRoutine #SleepBetter #HealthyLifestyle #BedroomGoals #SleepQuality #GoodNight',
        'product_link': 'https://www.amazon.com/s?k=cooling+mattress+pad&tag=sleepwiserevi-20',
        'pinterest_file': '',
        'instagram_file': ''
    }

    # Create Pinterest pin
    pin_path = create_pinterest_pin(tip, title="Sleep Tip", filename="01-pinterest-temperature-tip.png")
    content_data['pinterest_file'] = os.path.basename(pin_path)

    # Create Instagram post
    ig_path = create_instagram_post(tip, title="Sleep Tip", filename="02-instagram-temperature-tip.png")
    content_data['instagram_file'] = os.path.basename(ig_path)

    # Create README with copy-paste content
    today_folder = os.path.dirname(pin_path)
    readme_path = create_readme(today_folder, content_data)

    print("\n" + "=" * 50)
    print("CONTENT CREATED SUCCESSFULLY!")
    print("=" * 50)
    print(f"\nFolder: {today_folder}")
    print(f"\nFiles:")
    print(f"  1. {content_data['pinterest_file']} - Upload to Pinterest")
    print(f"  2. {content_data['instagram_file']} - Post to Instagram")
    print(f"  3. README.txt - Copy-paste captions & hashtags")
    print("\nOpen the folder and follow README.txt instructions!")
