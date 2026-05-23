import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv
import os
import anthropic

ENV_PATH = Path(__file__).parent.parent / ".env"
OUTPUT_PATH = Path(__file__).parent.parent / "data" / "keyword_results.json"

SYSTEM_PROMPT = (
    "You are an SEO specialist for SleepWiseReviews, an affiliate blog targeting USA buyers "
    "in the sleep products niche. "
    "Generate buyer-intent keyword ideas that rank well on Google and convert to Amazon affiliate purchases. "
    "Focus on: ear plugs, sleep masks, pillows, white noise machines, mattress toppers, weighted blankets, "
    "sleep supplements, blue light glasses, blackout curtains, cooling pads, sleep trackers."
)

USER_PROMPT_TEMPLATE = """\
Seed topic: {seed}

Generate exactly 10 keyword ideas in this JSON format:
{{
  "keywords": [
    {{
      "keyword": "exact phrase to target",
      "intent_score": 5,
      "content_type": "buying_guide",
      "estimated_difficulty": "low",
      "brief": "One sentence describing what the article covers"
    }}
  ]
}}

Intent score 1-5: 5 = strong purchase intent ("best X for Y"), 1 = informational only.
Prioritize keywords with intent_score >= 3.
Sort by intent_score descending.
"""


def load_api_key() -> str:
    load_dotenv(ENV_PATH)
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        print(f"ERROR: ANTHROPIC_API_KEY not found in {ENV_PATH}")
        sys.exit(1)
    return key


def call_claude(seed: str, api_key: str) -> list[dict]:
    client = anthropic.Anthropic(api_key=api_key)

    user_prompt = USER_PROMPT_TEMPLATE.format(seed=seed)

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )
    except anthropic.APIError as e:
        print(f"ERROR: API call failed: {e}")
        sys.exit(1)

    raw = message.content[0].text

    try:
        data = json.loads(raw)
        return data["keywords"]
    except (json.JSONDecodeError, KeyError):
        # Claude sometimes wraps JSON in a markdown block
        import re
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(1))
                return data["keywords"]
            except (json.JSONDecodeError, KeyError):
                pass
        print("ERROR: Could not parse JSON from response. Raw output:")
        print(raw)
        sys.exit(1)


def save_results(keywords: list[dict]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(keywords, indent=2, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword research for SleepWiseReviews")
    parser.add_argument("--seed", required=True, help='Seed topic, e.g. "best ear plugs for sleeping"')
    args = parser.parse_args()

    api_key = load_api_key()
    keywords = call_claude(args.seed, api_key)

    print(json.dumps(keywords, indent=2, ensure_ascii=False))

    save_results(keywords)
    print(f"\nResults saved to: {OUTPUT_PATH}", file=sys.stderr)


if __name__ == "__main__":
    main()
