"""
SleepWise - Create Week's Instagram Posts
Generates Instagram images for Tuesday-Sunday
"""

from create_content import create_instagram_post, OUTPUT_DIR
from datetime import datetime, timedelta
import os

# This week's Instagram posts (Tue-Sun)
WEEKLY_POSTS = [
    {
        "day": "tuesday",
        "date_offset": 1,  # Days from Monday
        "tip": "That 3pm coffee might be ruining your sleep! Caffeine has a half-life of 5-6 hours. Cut off by 2pm for better rest.",
        "title": "Caffeine & Sleep",
        "filename": "instagram-caffeine.png"
    },
    {
        "day": "wednesday",
        "date_offset": 2,
        "tip": "Blue light from screens suppresses melatonin by up to 50%. Use night mode or stop screens 1 hour before bed.",
        "title": "Blue Light",
        "filename": "instagram-bluelight.png"
    },
    {
        "day": "thursday",
        "date_offset": 3,
        "tip": "Exercise improves sleep quality, but finish workouts 3-4 hours before bed. Morning exercise is ideal!",
        "title": "Exercise & Sleep",
        "filename": "instagram-exercise.png"
    },
    {
        "day": "friday",
        "date_offset": 4,
        "tip": "Same bedtime + same wake time = better sleep! Your circadian rhythm needs consistency, even on weekends.",
        "title": "Sleep Schedule",
        "filename": "instagram-schedule.png"
    },
    {
        "day": "saturday",
        "date_offset": 5,
        "tip": "Weighted blankets use deep pressure therapy to calm your nervous system. Choose 7-12% of your body weight.",
        "title": "Weighted Blankets",
        "filename": "instagram-weighted.png"
    },
    {
        "day": "sunday",
        "date_offset": 6,
        "tip": "White noise masks sudden sounds that wake you up. Perfect for light sleepers in noisy environments!",
        "title": "White Noise",
        "filename": "instagram-whitenoise.png"
    }
]


def main():
    # Start from Monday of this week
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())

    print("=" * 60)
    print("CREATING THIS WEEK'S INSTAGRAM POSTS")
    print("=" * 60)

    for post_data in WEEKLY_POSTS:
        # Calculate the date for this post
        post_date = monday + timedelta(days=post_data['date_offset'])
        date_str = post_date.strftime('%Y-%m-%d')
        day_name = post_data['day']

        # Create folder for that day
        folder_name = f"{date_str}-{day_name}"
        output_folder = os.path.join(OUTPUT_DIR, "content", folder_name, "instagram")
        os.makedirs(output_folder, exist_ok=True)

        print(f"\nCreating {day_name.title()} Instagram post...")
        print(f"  Folder: {folder_name}")

        # Create the Instagram post
        ig_path = create_instagram_post(
            tip_text=post_data['tip'],
            title=post_data['title'],
            filename=post_data['filename']
        )

        # Move to correct folder if needed
        if ig_path:
            target_path = os.path.join(output_folder, post_data['filename'])
            if os.path.exists(ig_path) and ig_path != target_path:
                import shutil
                shutil.move(ig_path, target_path)
                print(f"  Saved: {target_path}")

    print("\n" + "=" * 60)
    print("INSTAGRAM POSTS CREATED!")
    print("=" * 60)
    print("\nCheck each day's folder under content/")
    print("Each folder now has pinterest/ and instagram/ subfolders")


if __name__ == "__main__":
    main()
