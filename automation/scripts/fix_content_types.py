"""
fix_content_types.py
Batch update rows where content_type == "Single Image" -> "Carousel".

Usage:
    python fix_content_types.py          # dry-run
    python fix_content_types.py --apply  # write to sheet
"""

import argparse
import gspread
from google.oauth2.service_account import Credentials

SHEET_ID = "1KeWK1xO5eiD2YbFe63Fx8sV9Vf6jUwi57h71fc8zb5o"
SHEET_NAME = "IG QUEUE"
SERVICE_ACCOUNT_PATH = (
    r"C:\Users\Hany\OneDrive - Petroleum Air Services"
    r"\Projects\SleepReviewes\automation\data\service_account.json"
)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]

COL_CONTENT_TYPE = 2  # 0-indexed → column C


def get_sheet():
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_PATH, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)


def main(apply: bool) -> None:
    sheet = get_sheet()
    all_values = sheet.get_all_values()

    # Row 0 is header; data starts at row 1 (sheet row 2)
    data_rows = all_values[1:]

    updates = []
    for i, row in enumerate(data_rows):
        content_type = row[COL_CONTENT_TYPE] if len(row) > COL_CONTENT_TYPE else ""
        if content_type.strip() == "Single Image":
            sheet_row = i + 2  # 1-indexed sheet row, +1 for header
            updates.append(sheet_row)
            print(f"  Row {sheet_row}: '{content_type}' -> 'Carousel'")

    if not updates:
        print("No rows found with content_type == 'Single Image'.")
        return

    if apply:
        # Build batch update payload: list of dicts {range, values}
        batch = [
            {
                "range": f"C{row}",
                "values": [["Carousel"]],
            }
            for row in updates
        ]
        sheet.batch_update(batch)
        print(f"\nAPPLIED: {len(updates)} rows updated.")
    else:
        print(f"\nDRY RUN: {len(updates)} rows would be updated. Pass --apply to write.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fix content_type: Single Image → Carousel")
    parser.add_argument("--apply", action="store_true", help="Write changes to sheet")
    args = parser.parse_args()
    main(apply=args.apply)
