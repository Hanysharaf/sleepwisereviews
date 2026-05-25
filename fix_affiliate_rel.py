"""Add rel="nofollow noopener noreferrer" to Amazon affiliate links missing nofollow."""
import re, os

POSTS_DIR = os.path.join(os.path.dirname(__file__), 'posts')

def fix_amazon_link(match):
    tag = match.group(0)
    if 'nofollow' in tag:
        return tag
    # Check if rel attribute already exists
    rel_match = re.search(r'\brel="([^"]*)"', tag)
    if rel_match:
        existing = rel_match.group(1)
        parts = set(existing.split())
        parts.update(['nofollow', 'noopener', 'noreferrer'])
        new_rel = ' '.join(sorted(parts))
        return tag.replace(rel_match.group(0), f'rel="{new_rel}"')
    else:
        # Add rel before the closing >
        return tag[:-1] + ' rel="nofollow noopener noreferrer">'

updated = 0
total_fixed = 0

for fname in sorted(os.listdir(POSTS_DIR)):
    if not fname.endswith('.html'):
        continue

    fpath = os.path.join(POSTS_DIR, fname)
    with open(fpath, encoding='utf-8') as f:
        html = f.read()

    # Match all <a> tags pointing to amazon.com
    new_html, count = re.subn(
        r'<a\b[^>]+amazon\.com[^>]+>',
        fix_amazon_link,
        html
    )

    if count > 0 and new_html != html:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        updated += 1
        total_fixed += count

print(f'Files updated: {updated}')
print(f'Links fixed: {total_fixed}')
