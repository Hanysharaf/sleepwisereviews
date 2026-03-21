"""
SleepWise - Create Week's Pinterest Pins
Generates 6 pins for Tuesday-Sunday
"""

from create_content import create_pinterest_pin, create_readme, OUTPUT_DIR
from datetime import datetime
import os

# This week's pins (Tue-Sun)
WEEKLY_PINS = [
    {
        "day": "Tuesday",
        "tip": "Stop caffeine 8-10 hours before bed. That afternoon coffee might be why you can't fall asleep!",
        "title": "Caffeine & Sleep",
        "filename": "03-pin-tuesday-caffeine.png",
        "pinterest_title": "When to Stop Caffeine for Better Sleep",
        "pinterest_desc": "Stop caffeine 8-10 hours before bed! That 3pm coffee has a half-life of 5-6 hours, keeping you awake at night. Switch to herbal tea in the afternoon. #SleepTips #CaffeineFree #BetterSleep #SleepHacks",
        "product_link": "https://www.amazon.com/s?k=herbal+sleep+tea&tag=sleepwiserevi-20"
    },
    {
        "day": "Wednesday",
        "tip": "Blue light from screens suppresses melatonin. Use night mode or stop screens 1 hour before bed.",
        "title": "Blue Light & Sleep",
        "filename": "04-pin-wednesday-bluelight.png",
        "pinterest_title": "Blue Light is Ruining Your Sleep",
        "pinterest_desc": "Blue light from phones & laptops suppresses melatonin by up to 50%! Use night mode or wear blue light blocking glasses 2 hours before bed. #BlueLightGlasses #SleepScience #BetterSleep #Melatonin",
        "product_link": "https://www.amazon.com/s?k=blue+light+blocking+glasses&tag=sleepwiserevi-20"
    },
    {
        "day": "Thursday",
        "tip": "Exercise improves sleep quality, but finish workouts 3-4 hours before bed to avoid being too energized.",
        "title": "Exercise & Sleep",
        "filename": "05-pin-thursday-exercise.png",
        "pinterest_title": "Best Time to Exercise for Better Sleep",
        "pinterest_desc": "Exercise improves sleep quality - but timing matters! Finish workouts 3-4 hours before bed. Morning or afternoon exercise is ideal for deep sleep. #SleepTips #ExerciseTips #HealthyLifestyle #BetterSleep",
        "product_link": "https://www.amazon.com/s?k=sleep+tracker&tag=sleepwiserevi-20"
    },
    {
        "day": "Friday",
        "tip": "Consistent sleep schedule is key! Go to bed and wake up at the same time, even on weekends.",
        "title": "Sleep Schedule",
        "filename": "06-pin-friday-schedule.png",
        "pinterest_title": "The #1 Sleep Habit You're Missing",
        "pinterest_desc": "Same bedtime + same wake time = better sleep! Even on weekends. Your body's circadian rhythm needs consistency. This simple habit beats any sleep supplement. #SleepSchedule #CircadianRhythm #SleepTips",
        "product_link": "https://www.amazon.com/s?k=sunrise+alarm+clock&tag=sleepwiserevi-20"
    },
    {
        "day": "Saturday",
        "tip": "Weighted blankets (7-12% of body weight) can reduce anxiety and improve sleep quality through deep pressure therapy.",
        "title": "Weighted Blankets",
        "filename": "07-pin-saturday-weighted.png",
        "pinterest_title": "Why Weighted Blankets Help You Sleep",
        "pinterest_desc": "Weighted blankets use deep pressure therapy to calm your nervous system. Choose 7-12% of your body weight for best results. Game changer for anxious sleepers! #WeightedBlanket #AnxietyRelief #DeepSleep #SleepProducts",
        "product_link": "https://www.amazon.com/s?k=weighted+blanket&tag=sleepwiserevi-20"
    },
    {
        "day": "Sunday",
        "tip": "White noise masks disruptive sounds and creates a consistent audio environment for better sleep.",
        "title": "White Noise",
        "filename": "08-pin-sunday-whitenoise.png",
        "pinterest_title": "White Noise: The Secret to Uninterrupted Sleep",
        "pinterest_desc": "White noise masks sudden sounds that wake you up - traffic, neighbors, pets. Your brain stays in deep sleep longer. Perfect for light sleepers! #WhiteNoise #SleepSounds #LightSleeper #BetterSleep",
        "product_link": "https://www.amazon.com/s?k=white+noise+machine&tag=sleepwiserevi-20"
    }
]


def main():
    today = datetime.now().strftime('%Y-%m-%d')
    output_folder = os.path.join(OUTPUT_DIR, "content", today)
    os.makedirs(output_folder, exist_ok=True)

    print("=" * 60)
    print("CREATING THIS WEEK'S PINTEREST PINS")
    print("=" * 60)

    created_pins = []

    for pin_data in WEEKLY_PINS:
        print(f"\nCreating {pin_data['day']} pin...")

        pin_path = create_pinterest_pin(
            tip_text=pin_data['tip'],
            title=pin_data['title'],
            filename=pin_data['filename']
        )

        created_pins.append({
            'day': pin_data['day'],
            'filename': pin_data['filename'],
            'title': pin_data['pinterest_title'],
            'desc': pin_data['pinterest_desc'],
            'link': pin_data['product_link']
        })

    # Create schedule README
    schedule_path = os.path.join(output_folder, "WEEK-SCHEDULE.txt")
    with open(schedule_path, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("SLEEPWISE - PINTEREST SCHEDULE FOR THIS WEEK\n")
        f.write("=" * 60 + "\n\n")
        f.write("Post 1 pin per day. Copy title & description below.\n\n")

        for pin in created_pins:
            f.write("-" * 50 + "\n")
            f.write(f"{pin['day'].upper()}\n")
            f.write("-" * 50 + "\n")
            f.write(f"File: {pin['filename']}\n\n")
            f.write(f"Title: {pin['title']}\n\n")
            f.write(f"Description:\n{pin['desc']}\n\n")
            f.write(f"Board: Sleep Tips\n")
            f.write(f"Link: {pin['link']}\n\n")

    print("\n" + "=" * 60)
    print("WEEK'S PINS CREATED!")
    print("=" * 60)
    print(f"\nFolder: {output_folder}")
    print(f"\nFiles created:")
    print(f"  - 01-pinterest-temperature-tip.png (Monday - DONE)")
    for pin in created_pins:
        print(f"  - {pin['filename']} ({pin['day']})")
    print(f"  - WEEK-SCHEDULE.txt (copy-paste guide)")
    print("\nOpen Pinterest → Scheduler → Upload pins → Set dates!")


if __name__ == "__main__":
    main()
