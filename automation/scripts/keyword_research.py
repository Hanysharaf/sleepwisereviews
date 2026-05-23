"""
keyword_research.py — free Google autocomplete scraping, no API key needed.

Usage:
    python automation/scripts/keyword_research.py --seed "best ear plugs for sleeping"
"""

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent.parent / "data" / "keyword_results.json"

SLEEP_NICHE = {
    "ear plug", "sleep mask", "pillow", "white noise", "mattress topper",
    "weighted blanket", "melatonin", "magnesium", "blue light", "blackout curtain",
    "cooling pad", "cooling pillow", "sleep tracker", "aromatherapy", "sleep supplement",
    "sleep headphone", "cpap", "anti-snoring", "sleep monitor", "sunrise alarm",
}

BUYER_SIGNALS = {
    "best": 5, "top": 5, "review": 4, "vs": 4, "worth it": 4,
    "buy": 5, "cheap": 4, "affordable": 4, "under $": 4,
    "for sleeping": 4, "for sleep": 4, "for side sleeper": 4,
    "2025": 3, "2026": 3, "comparison": 4, "ranked": 4, "tested": 4,
}

QUERY_TEMPLATES = [
    "{seed}",
    "best {seed}",
    "{seed} review",
    "{seed} vs",
    "{seed} for sleeping",
    "{seed} 2026",
    "top {seed}",
    "cheap {seed}",
    "{seed} worth it",
]

CONTENT_TYPE_MAP = {
    "best": "buying_guide", "top": "buying_guide", "ranked": "buying_guide",
    "review": "product_review", "tested": "product_review",
    "vs": "comparison", "comparison": "comparison",
    "how to": "how_to", "tips": "how_to",
}


def google_autocomplete(query: str) -> list[str]:
    encoded = urllib.parse.quote(query)
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&hl=en&gl=us&q={encoded}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0)"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data[1] if len(data) > 1 else []
    except Exception:
        return []


def intent_score(keyword: str) -> int:
    kw = keyword.lower()
    score = 1
    for signal, pts in BUYER_SIGNALS.items():
        if signal in kw:
            score = max(score, pts)
    return score


def niche_match(keyword: str) -> bool:
    kw = keyword.lower()
    return any(term in kw for term in SLEEP_NICHE)


def infer_content_type(keyword: str) -> str:
    kw = keyword.lower()
    for signal, ctype in CONTENT_TYPE_MAP.items():
        if signal in kw:
            return ctype
    return "buying_guide"


def infer_difficulty(keyword: str) -> str:
    kw = keyword.lower()
    if any(x in kw for x in ["best ", "top ", "review"]):
        return "medium"
    if any(x in kw for x in ["cheap", "affordable", "under $", "2025", "2026"]):
        return "low"
    return "medium"


def build_brief(keyword: str) -> str:
    ct = infer_content_type(keyword)
    if ct == "buying_guide":
        return f"Roundup of the best options for '{keyword}' with affiliate product recommendations."
    if ct == "product_review":
        return f"In-depth review covering pros, cons, and who should buy for '{keyword}'."
    if ct == "comparison":
        return f"Side-by-side comparison helping readers decide between options for '{keyword}'."
    return f"Practical guide covering '{keyword}' with sleep science context."


def collect_keywords(seed: str) -> list[dict]:
    seen = set()
    candidates = []

    base = seed.strip().lower()
    for template in QUERY_TEMPLATES:
        query = template.format(seed=base)
        suggestions = google_autocomplete(query)
        time.sleep(0.3)

        for s in suggestions:
            s_clean = s.strip().lower()
            if s_clean in seen:
                continue
            seen.add(s_clean)

            score = intent_score(s_clean)
            if score < 3:
                continue
            if not niche_match(s_clean):
                continue

            candidates.append({
                "keyword": s_clean,
                "intent_score": score,
                "content_type": infer_content_type(s_clean),
                "estimated_difficulty": infer_difficulty(s_clean),
                "brief": build_brief(s_clean),
            })

    # Sort by intent_score desc, deduplicate, take top 10
    candidates.sort(key=lambda x: x["intent_score"], reverse=True)

    if not candidates:
        # Fallback: build synthetic keywords from seed when scraping returns nothing
        candidates = _fallback(seed)

    return candidates[:10]


def _fallback(seed: str) -> list[dict]:
    base = seed.strip().lower()
    templates = [
        ("best " + base, 5, "buying_guide"),
        (base + " review", 4, "product_review"),
        ("top " + base, 5, "buying_guide"),
        (base + " vs alternatives", 4, "comparison"),
        ("cheap " + base, 4, "buying_guide"),
        (base + " 2026", 3, "buying_guide"),
        ("best " + base + " for side sleepers", 5, "buying_guide"),
        (base + " worth it", 4, "product_review"),
        (base + " under $50", 4, "buying_guide"),
        ("best " + base + " for light sleepers", 5, "buying_guide"),
    ]
    return [
        {
            "keyword": kw,
            "intent_score": score,
            "content_type": ct,
            "estimated_difficulty": "medium",
            "brief": build_brief(kw),
        }
        for kw, score, ct in templates
    ]


def main():
    parser = argparse.ArgumentParser(description="Free keyword research — Google autocomplete")
    parser.add_argument("--seed", required=True, help='e.g. "best ear plugs for sleeping"')
    args = parser.parse_args()

    keywords = collect_keywords(args.seed)

    print(json.dumps(keywords, indent=2, ensure_ascii=False))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(keywords, indent=2, ensure_ascii=False))
    print(f"\nResults saved to: {OUTPUT_PATH}", file=sys.stderr)


if __name__ == "__main__":
    main()
