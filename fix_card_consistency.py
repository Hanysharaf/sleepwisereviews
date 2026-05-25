import re

path = 'index.html'
content = open(path, encoding='utf-8').read()
original = content

fixes = [
    (
        '        <a class="article-card" href="posts/best-firm-mattress.html">\n'
        '          <div class="card-badge">Mattresses</div>\n'
        '          <h3>Best Firm Mattress 2025</h3>\n'
        '          <p>For back sleepers, stomach sleepers, and heavy builds -- 7 firm mattresses tested over 12 months. Saatva, WinkBed, Brooklyn Titan, and more ranked.</p>\n'
        '        </a>',
        '        <a class="article-card" href="posts/best-firm-mattress.html">\n'
        '          <div class="card-cat">Mattresses &amp; Bedding</div>\n'
        '          <h3>Best Firm Mattress 2025</h3>\n'
        '          <p>For back sleepers, stomach sleepers, and heavy builds -- 7 firm mattresses tested over 12 months. Saatva, WinkBed, Brooklyn Titan, and more ranked.</p>\n'
        '          <div class="card-meta"><span>7 Products Reviewed</span><span>May 2025</span></div>\n'
        '        </a>'
    ),
    (
        '        <a class="article-card" href="posts/best-king-size-mattress.html">\n'
        '          <div class="card-badge">Mattresses</div>\n'
        '          <h3>Best King Size Mattress 2025</h3>\n'
        '          <p>14-month test of 16 king mattresses for couples. Motion isolation, edge support, and temperature regulation -- Saatva, Purple, WinkBed, Helix ranked.</p>\n'
        '        </a>',
        '        <a class="article-card" href="posts/best-king-size-mattress.html">\n'
        '          <div class="card-cat">Mattresses &amp; Bedding</div>\n'
        '          <h3>Best King Size Mattress 2025</h3>\n'
        '          <p>14-month test of 16 king mattresses for couples. Motion isolation, edge support, and temperature regulation -- Saatva, Purple, WinkBed, Helix ranked.</p>\n'
        '          <div class="card-meta"><span>7 Products Reviewed</span><span>May 2025</span></div>\n'
        '        </a>'
    ),
    (
        '        <a class="article-card" href="posts/best-latex-mattress.html">\n'
        '          <div class="card-badge">Mattresses</div>\n'
        '          <h3>Best Latex Mattress 2025</h3>\n'
        '          <p>Organic Talalay and Dunlop latex mattresses ranked for durability, certifications, and value. GOLS-certified picks from Saatva, Avocado, PlushBeds, and more.</p>\n'
        '        </a>',
        '        <a class="article-card" href="posts/best-latex-mattress.html">\n'
        '          <div class="card-cat">Mattresses &amp; Bedding</div>\n'
        '          <h3>Best Latex Mattress 2025</h3>\n'
        '          <p>Organic Talalay and Dunlop latex mattresses ranked for durability, certifications, and value. GOLS-certified picks from Saatva, Avocado, PlushBeds, and more.</p>\n'
        '          <div class="card-meta"><span>7 Products Reviewed</span><span>May 2025</span></div>\n'
        '        </a>'
    ),
    (
        '        <a class="article-card" href="posts/best-sleep-mask.html">\n'
        '          <div class="card-badge">Sleep Products</div>\n'
        '          <h3>Best Sleep Masks 2025</h3>\n'
        '          <p>Tested for total blackout, eye comfort, and side-sleeper fit. Manta, Alaska Bear, Bucky, and more — ranked by 90 nights of real testing.</p>\n'
        '        </a>',
        '        <a class="article-card" href="posts/best-sleep-mask.html">\n'
        '          <div class="card-cat">Sleep Products</div>\n'
        '          <h3>Best Sleep Masks 2025</h3>\n'
        '          <p>Tested for total blackout, eye comfort, and side-sleeper fit. Manta, Alaska Bear, Bucky, and more — ranked by 90 nights of real testing.</p>\n'
        '          <div class="card-meta"><span>7 Products Reviewed</span><span>May 2025</span></div>\n'
        '        </a>'
    ),
    (
        '        <a class="article-card" href="posts/best-cooling-pillow.html">\n'
        '          <div class="card-badge">Bedding</div>\n'
        '          <h3>Best Cooling Pillows 2025</h3>\n'
        '          <p>Science-backed picks that sleep cold all night — PCM tech, gel foam, and natural latex options for hot sleepers.</p>\n'
        '        </a>',
        '        <a class="article-card" href="posts/best-cooling-pillow.html">\n'
        '          <div class="card-cat">Mattresses &amp; Bedding</div>\n'
        '          <h3>Best Cooling Pillows 2025</h3>\n'
        '          <p>Science-backed picks that sleep cold all night — PCM tech, gel foam, and natural latex options for hot sleepers.</p>\n'
        '          <div class="card-meta"><span>7 Products Reviewed</span><span>May 2025</span></div>\n'
        '        </a>'
    ),
]

for old, new in fixes:
    if old in content:
        content = content.replace(old, new)
        print(f'Fixed: {old[:60].strip()}')
    else:
        print(f'NOT FOUND: {old[:60].strip()}')

if content != original:
    open(path, 'w', encoding='utf-8').write(content)
    print('Saved.')
else:
    print('No changes made.')
