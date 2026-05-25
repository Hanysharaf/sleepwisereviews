import os

MARKER = 'class="related-guides"'


def make_related(links):
    items = '\n      '.join(
        f'<li><a href="{slug}.html" style="color:#93c5fd;text-decoration:none;font-size:.95rem;">{label}</a></li>'
        for slug, label in links
    )
    return (
        '\n<section class="related-guides" style="background:#111e33;border-top:2px solid #1e3a5f;padding:2rem 1.25rem;margin-top:2rem;">\n'
        '  <div style="max-width:820px;margin:0 auto;">\n'
        '    <h2 style="color:#c9a84c;font-size:1.05rem;letter-spacing:.04em;margin-bottom:1rem;text-transform:uppercase;">Related Guides</h2>\n'
        '    <ul style="list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:.6rem 1.5rem;">\n'
        f'      {items}\n'
        '    </ul>\n'
        '  </div>\n'
        '</section>\n'
    )


LINK_MAP = {
    'best-mattress-back-pain': [
        ('best-mattress-neck-pain',          'Best Mattress for Neck Pain'),
        ('best-mattress-hip-pain',           'Best Mattress for Hip Pain'),
        ('best-mattress-chronic-back-pain',  'Best Mattress for Chronic Back Pain'),
        ('best-mattress-side-sleepers',      'Best Mattress for Side Sleepers'),
    ],
    'best-mattress-side-sleepers': [
        ('best-mattress-back-pain',          'Best Mattress for Back Pain'),
        ('best-mattress-neck-pain',          'Best Mattress for Neck Pain'),
        ('best-mattress-hip-pain',           'Best Mattress for Hip Pain'),
        ('best-mattress-pressure-relief',    'Best Mattress for Pressure Relief'),
    ],
    'best-mattress-neck-pain': [
        ('best-mattress-back-pain',          'Best Mattress for Back Pain'),
        ('best-mattress-sciatica',           'Best Mattress for Sciatica'),
        ('best-mattress-side-sleepers',      'Best Mattress for Side Sleepers'),
        ('best-mattress-adjustable-base',    'Best Mattress for Adjustable Base'),
    ],
    'best-mattress-sciatica': [
        ('best-mattress-back-pain',          'Best Mattress for Back Pain'),
        ('best-mattress-hip-pain',           'Best Mattress for Hip Pain'),
        ('best-mattress-side-sleepers',      'Best Mattress for Side Sleepers'),
        ('best-mattress-chronic-back-pain',  'Best Mattress for Chronic Back Pain'),
    ],
    'best-mattress-chronic-back-pain': [
        ('best-mattress-back-pain',          'Best Mattress for Back Pain'),
        ('best-mattress-sciatica',           'Best Mattress for Sciatica'),
        ('best-mattress-hip-pain',           'Best Mattress for Hip Pain'),
        ('best-mattress-adjustable-base',    'Best Mattress for Adjustable Base'),
    ],
    'best-mattress-hip-pain': [
        ('best-mattress-back-pain',          'Best Mattress for Back Pain'),
        ('best-mattress-sciatica',           'Best Mattress for Sciatica'),
        ('best-mattress-side-sleepers',      'Best Mattress for Side Sleepers'),
        ('best-mattress-pressure-relief',    'Best Mattress for Pressure Relief'),
    ],
    'best-mattress-couples': [
        ('best-mattress-hot-sleepers',       'Best Mattress for Hot Sleepers'),
        ('best-king-mattress',               'Best King Size Mattress'),
        ('best-mattress-adjustable-base',    'Best Mattress for Adjustable Base'),
        ('best-mattress-side-sleepers',      'Best Mattress for Side Sleepers'),
    ],
    'best-mattress-hot-sleepers': [
        ('best-mattress-couples',            'Best Mattress for Couples'),
        ('best-mattress-side-sleepers',      'Best Mattress for Side Sleepers'),
        ('best-king-mattress',               'Best King Size Mattress'),
    ],
    'best-mattress-overweight': [
        ('best-mattress-back-pain',          'Best Mattress for Back Pain'),
        ('best-king-mattress',               'Best King Size Mattress'),
        ('best-mattress-couples',            'Best Mattress for Couples'),
    ],
    'best-mattress-scoliosis': [
        ('best-mattress-back-pain',          'Best Mattress for Back Pain'),
        ('best-mattress-sciatica',           'Best Mattress for Sciatica'),
        ('best-mattress-side-sleepers',      'Best Mattress for Side Sleepers'),
    ],
    'best-mattress-arthritis': [
        ('best-mattress-hip-pain',           'Best Mattress for Hip Pain'),
        ('best-mattress-pressure-relief',    'Best Mattress for Pressure Relief'),
        ('best-mattress-side-sleepers',      'Best Mattress for Side Sleepers'),
    ],
    'best-mattress-fibromyalgia': [
        ('best-mattress-pressure-relief',    'Best Mattress for Pressure Relief'),
        ('best-mattress-side-sleepers',      'Best Mattress for Side Sleepers'),
        ('best-mattress-arthritis',          'Best Mattress for Arthritis'),
    ],
    'best-mattress-stomach-sleepers-back-pain': [
        ('best-mattress-stomach-sleepers-lower-back-pain', 'Best Mattress for Stomach Sleepers (Lower Back Pain)'),
        ('best-mattress-back-pain',          'Best Mattress for Back Pain'),
        ('best-mattress-sciatica',           'Best Mattress for Sciatica'),
    ],
    'best-mattress-stomach-sleepers-lower-back-pain': [
        ('best-mattress-stomach-sleepers-back-pain', 'Best Mattress for Stomach Sleepers (Back Pain)'),
        ('best-mattress-back-pain',          'Best Mattress for Back Pain'),
        ('best-mattress-sciatica',           'Best Mattress for Sciatica'),
    ],
    'best-latex-mattress': [
        ('best-natural-latex-mattress',      'Best Natural Latex Mattress'),
        ('best-mattress-adjustable-base',    'Best Mattress for Adjustable Base'),
        ('best-mattress-back-pain',          'Best Mattress for Back Pain'),
    ],
    'best-natural-latex-mattress': [
        ('best-latex-mattress',              'Best Latex Mattress'),
        ('best-mattress-adjustable-base',    'Best Mattress for Adjustable Base'),
        ('best-mattress-back-pain',          'Best Mattress for Back Pain'),
    ],
    'best-king-mattress': [
        ('best-mattress-couples',            'Best Mattress for Couples'),
        ('best-mattress-adjustable-base',    'Best Mattress for Adjustable Base'),
        ('best-mattress-overweight',         'Best Mattress for Overweight Sleepers'),
    ],
    'best-mattress-adjustable-base': [
        ('best-mattress-back-pain',          'Best Mattress for Back Pain'),
        ('best-mattress-neck-pain',          'Best Mattress for Neck Pain'),
        ('best-mattress-sciatica',           'Best Mattress for Sciatica'),
        ('best-mattress-chronic-back-pain',  'Best Mattress for Chronic Back Pain'),
    ],
    'best-mattress-pressure-relief': [
        ('best-mattress-side-sleepers',      'Best Mattress for Side Sleepers'),
        ('best-mattress-hip-pain',           'Best Mattress for Hip Pain'),
        ('best-mattress-arthritis',          'Best Mattress for Arthritis'),
        ('best-mattress-fibromyalgia',       'Best Mattress for Fibromyalgia'),
    ],
}

patched = []
skipped_missing = []
skipped_already = []

for slug, links in LINK_MAP.items():
    path = f'posts/{slug}.html'
    if not os.path.exists(path):
        skipped_missing.append(slug)
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if MARKER in content:
        skipped_already.append(slug)
        continue
    block = make_related(links)
    new_content = content.replace('<footer', block + '<footer', 1)
    if new_content == content:
        print(f'WARNING: no footer found in {slug}')
        continue
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    patched.append(slug)

print(f'Patched ({len(patched)}):')
for s in patched:
    print(f'  + {s}')
print(f'\nSkipped - already has section ({len(skipped_already)}):')
for s in skipped_already:
    print(f'  ~ {s}')
print(f'\nSkipped - file missing ({len(skipped_missing)}):')
for s in skipped_missing:
    print(f'  X {s}')
