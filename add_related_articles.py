"""Add Related Articles sections to the 20 posts that are missing them."""
import re, os

POSTS_DIR = os.path.join(os.path.dirname(__file__), 'posts')

# Build title map from all posts
title_map = {}
for fn in os.listdir(POSTS_DIR):
    if not fn.endswith('.html'):
        continue
    with open(os.path.join(POSTS_DIR, fn), encoding='utf-8') as f:
        html = f.read()
    m = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL)
    if m:
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        title = re.sub(r'\s*[|\-–]\s*(Sleep.*|SleepWise.*)$', '', title).strip()
        title_map[fn] = title

# Related articles map: post -> list of related filenames
RELATED = {
    'best-aromatherapy-sleep.html': [
        'sleep-environment-optimization.html', 'bedroom-plants-sleep.html',
        'natural-sleep-aids.html', 'wind-down-routine.html', 'best-sleep-supplements-guide.html',
    ],
    'best-grounding-sheets.html': [
        'sleep-environment-optimization.html', 'magnesium-deficiency-sleep.html',
        'sleep-and-pain.html', 'sleep-chronic-pain.html', 'best-sleep-supplements-guide.html',
    ],
    'best-humidifiers-sleep.html': [
        'bedroom-temperature-sleep.html', 'sleep-environment-optimization.html',
        'sleep-sanctuary-guide.html', 'best-blackout-curtains.html', 'bedroom-plants-sleep.html',
    ],
    'best-mattress-toppers.html': [
        'best-mattresses-back-pain.html', 'best-cooling-mattress-pads.html',
        'sleep-chronic-pain.html', 'sleep-and-pain.html', 'bedroom-temperature-sleep.html',
    ],
    'best-sleep-headphones.html': [
        'best-sleep-masks.html', 'sleep-environment-optimization.html',
        'article-white-noise-machines.html', 'best-blackout-curtains.html', 'sleep-sanctuary-guide.html',
    ],
    'best-sleep-monitors.html': [
        'best-sleep-tracking-rings.html', 'sleep-tracking-data.html',
        'sleep-tracking-worth-it.html', 'sleep-stages-explained.html', 'sleep-goal-setting.html',
    ],
    'jet-lag-guide.html': [
        'circadian-rhythm-basics.html', 'chronobiology-basics.html',
        'daylight-saving-sleep.html', 'sleep-travel-tips.html', 'reset-sleep-schedule.html',
    ],
    'sleep-and-alcohol-free.html': [
        'alcohol-sleep-quality.html', 'sleep-food-connection.html',
        'sleep-fasting.html', 'natural-sleep-aids.html', 'sleep-productivity.html',
    ],
    'sleep-apnea-warning-signs.html': [
        'sleep-apnea-diagnosis.html', 'best-cpap-alternatives.html',
        'snoring-causes-fixes.html', 'sleep-disorders-overview.html', 'sleep-heart-health.html',
    ],
    'sleep-athletic-performance.html': [
        'sleep-exercise-timing.html', 'sleep-productivity.html',
        'deep-sleep-benefits.html', 'rem-sleep-benefits.html', 'sleep-goal-setting.html',
    ],
    'sleep-chronic-pain.html': [
        'sleep-and-pain.html', 'sleep-fibromyalgia.html',
        'magnesium-deficiency-sleep.html', 'best-mattresses-back-pain.html', 'cbt-i-guide.html',
    ],
    'sleep-cortisol-stress.html': [
        'sleep-anxiety-techniques.html', 'sleep-mental-health.html',
        'wind-down-routine.html', 'sleep-immune-system.html', 'circadian-rhythm-basics.html',
    ],
    'sleep-mental-health.html': [
        'sleep-depression.html', 'sleep-anxiety-techniques.html',
        'sleep-cortisol-stress.html', 'sleep-ptsd.html', 'sleep-when-anxious.html',
    ],
    'sleep-productivity.html': [
        'sleep-goal-setting.html', 'sleep-athletic-performance.html',
        'morning-habits-sleep.html', 'power-nap-science.html', 'sleep-mental-performance.html',
    ],
    'sleep-sanctuary-guide.html': [
        'sleep-environment-optimization.html', 'bedroom-temperature-sleep.html',
        'best-blackout-curtains.html', 'best-sleep-masks.html', 'bedroom-plants-sleep.html',
    ],
    'sleep-tracking-data.html': [
        'best-sleep-tracking-rings.html', 'best-sleep-monitors.html',
        'sleep-tracking-worth-it.html', 'sleep-goal-setting.html', 'sleep-stages-explained.html',
    ],
    'sleep-travel-tips.html': [
        'jet-lag-guide.html', 'sleep-business-travel.html',
        'sleep-camping.html', 'daylight-saving-sleep.html', 'chronobiology-basics.html',
    ],
    'summer-sleep-guide.html': [
        'bedroom-temperature-sleep.html', 'best-cooling-pillows.html',
        'best-cooling-mattress-pads.html', 'sleep-environment-optimization.html', 'winter-sleep-guide.html',
    ],
    'teen-sleep-guide.html': [
        'kids-sleep-guide.html', 'sleep-stages-explained.html',
        'circadian-rhythm-basics.html', 'morning-habits-sleep.html', 'sleep-goal-setting.html',
    ],
    'weekend-sleep-mistake.html': [
        'sleep-consistency-importance.html', 'sleep-debt-accumulation.html',
        'sleep-debt-recovery.html', 'social-jetlag.html', 'circadian-rhythm-basics.html',
    ],
}

def make_related_block(related_files):
    items = []
    for fn in related_files:
        title = title_map.get(fn, fn.replace('.html', '').replace('-', ' ').title())
        items.append(f'        <li><a href="{fn}">{title}</a></li>')
    return (
        '\n    <div class="related-articles">\n'
        '      <h3>Related Articles</h3>\n'
        '      <ul>\n'
        + '\n'.join(items) + '\n'
        '      </ul>\n'
        '    </div>'
    )

INJECT_POINTS = ['</article>', '</main>', '<footer']

updated = 0
skipped = 0

for fname, related in RELATED.items():
    fpath = os.path.join(POSTS_DIR, fname)
    if not os.path.exists(fpath):
        print(f'MISSING: {fname}')
        skipped += 1
        continue

    with open(fpath, encoding='utf-8') as f:
        html = f.read()

    if 'Related Articles' in html or 'related-articles' in html:
        print(f'SKIP (already has related): {fname}')
        skipped += 1
        continue

    # Filter to only related files that exist
    valid_related = [r for r in related if os.path.exists(os.path.join(POSTS_DIR, r))]
    if not valid_related:
        print(f'SKIP (no valid related files): {fname}')
        skipped += 1
        continue

    block = make_related_block(valid_related)

    injected = False
    for point in INJECT_POINTS:
        if point in html:
            html = html.replace(point, block + '\n  ' + point, 1)
            injected = True
            break

    if not injected:
        print(f'SKIP (no injection point): {fname}')
        skipped += 1
        continue

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'OK: {fname} ({len(valid_related)} links)')
    updated += 1

print(f'\nUpdated: {updated}  Skipped: {skipped}')
