"""
Bonus Pins - Based on Analytics Insights
Weighted Blankets = TOP PERFORMER - Create more!
"""

from create_content import create_pinterest_pin, OUTPUT_DIR
from datetime import datetime
import os

# Bonus pins - Weighted Blanket variations (TOP PERFORMER!)
BONUS_PINS = [
    {
        "tip": "A weighted blanket should be 7-12% of your body weight. Too heavy and you'll feel trapped. Too light and you won't get the calming benefits.",
        "title": "Weighted Blanket Guide",
        "filename": "bonus-pin-weighted-blanket-guide.png",
        "pinterest_title": "How to Choose the Perfect Weighted Blanket Weight",
        "pinterest_desc": "Weighted blanket buying guide: Choose 7-12% of your body weight for best results. 150 lbs = 15 lb blanket. Too heavy feels trapped, too light won't calm you. Save this guide! #WeightedBlanket #SleepProducts #AnxietyRelief #DeepSleep #BetterSleep",
        "product_link": "https://www.amazon.com/s?k=weighted+blanket&tag=sleepwiserevi-20"
    },
    {
        "tip": "Weighted blankets use deep pressure therapy to boost serotonin and melatonin while reducing cortisol. It's like a calming hug all night long.",
        "title": "Weighted Blanket Science",
        "filename": "bonus-pin-weighted-blanket-science.png",
        "pinterest_title": "The Science Behind Weighted Blankets",
        "pinterest_desc": "Why weighted blankets work: Deep pressure therapy boosts serotonin (+28%) and melatonin while reducing cortisol (stress hormone). Like a calming hug all night! Save for better sleep! #WeightedBlanket #SleepScience #AnxietyRelief #DeepPressureTherapy #BetterSleep",
        "product_link": "https://www.amazon.com/s?k=weighted+blanket+anxiety&tag=sleepwiserevi-20"
    }
]


def main():
    today = datetime.now().strftime('%Y-%m-%d')
    output_folder = os.path.join(OUTPUT_DIR, "content", f"{today}-bonus")
    os.makedirs(output_folder, exist_ok=True)

    print("=" * 60)
    print("CREATING BONUS WEIGHTED BLANKET PINS")
    print("(Based on Analytics - Top Performer!)")
    print("=" * 60)

    # Create README for bonus pins
    readme_path = os.path.join(output_folder, "README.txt")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("SLEEPWISE - BONUS PINS (Weighted Blanket Focus)\n")
        f.write("=" * 50 + "\n\n")
        f.write("Based on analytics: Weighted Blankets = TOP PERFORMER\n")
        f.write("These pins should get high impressions!\n\n")

        for i, pin_data in enumerate(BONUS_PINS, 1):
            print(f"\nCreating bonus pin {i}...")

            # Create subfolder
            pin_folder = os.path.join(output_folder, "pinterest")
            os.makedirs(pin_folder, exist_ok=True)

            pin_path = create_pinterest_pin(
                tip_text=pin_data['tip'],
                title=pin_data['title'],
                filename=pin_data['filename']
            )

            # Move to correct folder
            new_path = os.path.join(pin_folder, pin_data['filename'])
            if os.path.exists(pin_path):
                os.rename(pin_path, new_path)

            f.write("-" * 50 + "\n")
            f.write(f"PIN {i}\n")
            f.write("-" * 50 + "\n")
            f.write(f"File: pinterest/{pin_data['filename']}\n\n")
            f.write(f"Title: {pin_data['pinterest_title']}\n\n")
            f.write(f"Description:\n{pin_data['pinterest_desc']}\n\n")
            f.write(f"Link: {pin_data['product_link']}\n\n")

    print("\n" + "=" * 60)
    print("BONUS PINS CREATED!")
    print("=" * 60)
    print(f"\nFolder: {output_folder}")
    print("\nThese are PRIORITY pins - post them soon!")
    print("Weighted blanket content gets 50%+ of your impressions!")


if __name__ == "__main__":
    main()
