"""
Mass-apply Harry Soul EEAT byline block + Schema.org Person author upgrade.
Handles both template variants (newer chronic-sinusitis style + older fibromyalgia style).
Idempotent: skips posts that already have the byline.
"""
import os
import re
import glob

POSTS_DIR = r"O:\MyFiles\Projects\SleepReviewes\posts"

BYLINE_BLOCK = '''<div class="byline" style="margin-top:18px;padding:14px 18px;background:rgba(255,255,255,0.04);border-left:3px solid #c9a84c;border-radius:4px;display:flex;align-items:center;gap:14px;font-size:0.88rem;line-height:1.5;max-width:680px;">
<img src="/images/authors/harry-soul.svg" alt="Harry Soul" width="44" height="44" style="border-radius:50%;flex-shrink:0;" />
<div>
<div>By <a href="/pages/about.html" rel="author" style="color:#c9a84c;text-decoration:none;font-weight:600;">Harry Soul</a> &middot; Independent Sleep Reviewer</div>
<div style="opacity:0.75;font-size:0.82rem;margin-top:2px;">Reviewed for clinical accuracy by SleepWise Editorial Team &middot; Updated May 26, 2026</div>
<div style="opacity:0.65;font-size:0.78rem;margin-top:4px;font-style:italic;">Educational content only. Not medical advice. Consult your physician before changing sleep equipment that affects your condition.</div>
</div>
</div>
'''

# Author JSON-LD upgrades
AUTHOR_PERSON = '"author":{"@type":"Person","name":"Harry Soul","url":"https://sleepwisereviews.com/pages/about.html","jobTitle":"Independent Sleep Product Reviewer"},"reviewedBy":{"@type":"Organization","name":"SleepWise Editorial Team"},"publisher"'
AUTHOR_PERSON_SPACED_6 = '"author": {"@type": "Person", "name": "Harry Soul", "url": "https://sleepwisereviews.com/pages/about.html", "jobTitle": "Independent Sleep Product Reviewer"},\n      "reviewedBy": {"@type": "Organization", "name": "SleepWise Editorial Team"},\n      "publisher"'
AUTHOR_PERSON_SPACED_2 = '"author": {"@type": "Person", "name": "Harry Soul", "url": "https://sleepwisereviews.com/pages/about.html", "jobTitle": "Independent Sleep Product Reviewer"},\n  "reviewedBy": {"@type": "Organization", "name": "SleepWise Editorial Team"},\n  "publisher"'

# Patterns to replace
OLD_AUTHOR_COMPACT = '"author":{"@type":"Organization","name":"SleepWise Reviews"},"publisher"'
OLD_AUTHOR_SPACED_6 = '"author": {"@type": "Organization", "name": "SleepWise Reviews"},\n      "publisher"'
OLD_AUTHOR_SPACED_2 = '"author": {"@type": "Organization", "name": "SleepWiseReviews"},\n  "publisher"'

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    actions = []

    # Skip if byline already present
    if 'class="byline"' in content or 'rel="author"' in content:
        return None, "already has byline"

    # Update JSON-LD author -- try compact form first, then spaced forms
    if OLD_AUTHOR_COMPACT in content:
        content = content.replace(OLD_AUTHOR_COMPACT, AUTHOR_PERSON)
        actions.append("schema:compact")
    elif OLD_AUTHOR_SPACED_6 in content:
        content = content.replace(OLD_AUTHOR_SPACED_6, AUTHOR_PERSON_SPACED_6)
        actions.append("schema:spaced6")
    elif OLD_AUTHOR_SPACED_2 in content:
        content = content.replace(OLD_AUTHOR_SPACED_2, AUTHOR_PERSON_SPACED_2)
        actions.append("schema:spaced2")

    # Insert byline block
    # Newer template: <div class="meta">...</div> inside <div class="hero"> or <section class="hero">
    new_template_re = re.compile(r'(<div class="meta">[^<]*(?:<[^/][^>]*>[^<]*</[^>]+>[^<]*)*</div>\s*)\n(\s*)</(?:div|section)>\s*\n\s*<div class="container">', re.DOTALL)
    # Third variant: <p class="meta">[any byline text]</p> inside hero
    third_template_re = re.compile(r'(\s*)<p class="meta">(?:By |Reviewed by |Author: )?SleepWise[^<]*</p>', re.DOTALL)
    # Older template: <div class="hero-meta">...</div> ending </section>
    old_template_re = re.compile(r'(<div class="hero-meta">[\s\S]*?</div>)\s*\n(\s*</section>)', re.DOTALL)

    # Fourth variant: H1 + p.subtitle, no meta line — insert after subtitle
    subtitle_re = re.compile(r'(<p class="subtitle">[\s\S]*?</p>)', re.DOTALL)
    # Fifth variant: H1 + p.sub (older fibromyalgia-style without hero-meta)
    sub_re = re.compile(r'(<p class="sub">[\s\S]*?</p>)', re.DOTALL)

    m = new_template_re.search(content)
    if m:
        # Determine closing tag from match (preserve div or section)
        closing_tag = '</section>' if '</section>' in m.group(0) else '</div>'
        content = new_template_re.sub(r'\1\n' + BYLINE_BLOCK + closing_tag + r'\n\n<div class="container">', content, count=1)
        actions.append("byline:new-template")
    elif third_template_re.search(content):
        content = third_template_re.sub(r'\1' + BYLINE_BLOCK.rstrip(), content, count=1)
        actions.append("byline:third-template")
    elif old_template_re.search(content):
        content = old_template_re.sub(r'\1\n  ' + BYLINE_BLOCK + r'\2', content, count=1)
        actions.append("byline:old-template")
    elif subtitle_re.search(content):
        content = subtitle_re.sub(r'\1\n  ' + BYLINE_BLOCK, content, count=1)
        actions.append("byline:subtitle")
    elif sub_re.search(content):
        content = sub_re.sub(r'\1\n  ' + BYLINE_BLOCK, content, count=1)
        actions.append("byline:sub")
    else:
        # Catch-all fallback: insert after first <h1>...</h1> followed by first <p ...>...</p>
        fallback_re = re.compile(r'(<h1[^>]*>[\s\S]*?</h1>\s*\n\s*<p[^>]*>[\s\S]*?</p>)', re.DOTALL)
        m = fallback_re.search(content)
        if m:
            content = content[:m.end()] + '\n  ' + BYLINE_BLOCK + content[m.end():]
            actions.append("byline:fallback")

    if content == original:
        return None, "no patterns matched"

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path, ",".join(actions)


def main():
    files = sorted(glob.glob(os.path.join(POSTS_DIR, "best-mattress-*.html")))
    updated = 0
    skipped = 0
    no_match = 0
    results = {"updated": [], "skipped": [], "no_match": []}

    for path in files:
        result, msg = process_file(path)
        name = os.path.basename(path)
        if result:
            updated += 1
            results["updated"].append((name, msg))
        elif msg == "already has byline":
            skipped += 1
            results["skipped"].append(name)
        else:
            no_match += 1
            results["no_match"].append((name, msg))

    print(f"\n=== SUMMARY ===")
    print(f"Updated:   {updated}")
    print(f"Skipped:   {skipped} (already had byline)")
    print(f"No match:  {no_match}")
    print(f"Total:     {len(files)}")

    if results["no_match"]:
        print(f"\n=== NO MATCH (first 10) ===")
        for name, msg in results["no_match"][:10]:
            print(f"  {name}: {msg}")


if __name__ == "__main__":
    main()
