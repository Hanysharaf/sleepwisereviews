"""
Fix homepage issues:
1. Wrap floating article cards in a CSS grid container
2. Add CSS to make all card formats visually consistent
"""

content = open('index.html', encoding='utf-8').read()
original = content

# ── CSS to inject ──────────────────────────────────────────────────────────────
new_css = '''
    /* REVIEWS ARCHIVE GRID */
    .reviews-archive-section { padding: 1rem 0 4rem; }
    .reviews-archive-section .section-inner { padding-top: 1.5rem; }
    .reviews-archive-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 1.5rem;
    }
    /* Normalize ALL article-card variants inside grid */
    .reviews-archive-grid .article-card {
      min-width: 0 !important;
      max-width: none !important;
      width: 100%;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      overflow: hidden;
      text-decoration: none;
      color: var(--text);
      display: flex;
      flex-direction: column;
      padding: 1.3rem;
      transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
    }
    .reviews-archive-grid .article-card:hover {
      border-color: rgba(201,168,76,0.4);
      transform: translateY(-3px);
      box-shadow: 0 12px 32px rgba(0,0,0,0.3);
    }
    /* Unified category tag — covers card-cat, card-badge, article-tag, category-tag, card-tag */
    .reviews-archive-grid .article-card .card-cat,
    .reviews-archive-grid .article-card .card-badge,
    .reviews-archive-grid .article-card .article-tag,
    .reviews-archive-grid .article-card .category-tag,
    .reviews-archive-grid .article-card .card-tag {
      display: inline-block;
      font-size: 0.72rem;
      font-family: sans-serif;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      color: var(--gold);
      background: rgba(201,168,76,0.1);
      border: 1px solid rgba(201,168,76,0.25);
      border-radius: 20px;
      padding: 0.2rem 0.65rem;
      margin-bottom: 0.6rem;
    }
    /* Unified title — covers h2, h3, .article-title, .card-title, .article-card-title */
    .reviews-archive-grid .article-card h2,
    .reviews-archive-grid .article-card h3,
    .reviews-archive-grid .article-card .article-title,
    .reviews-archive-grid .article-card .card-title,
    .reviews-archive-grid .article-card .article-card-title {
      font-size: 0.97rem;
      font-weight: 700;
      line-height: 1.35;
      color: #f0e6c8;
      margin-bottom: 0.5rem;
      font-family: 'Outfit', 'Georgia', sans-serif;
    }
    /* Unified excerpt — covers p, .article-excerpt, .card-desc */
    .reviews-archive-grid .article-card p,
    .reviews-archive-grid .article-card .article-excerpt,
    .reviews-archive-grid .article-card .card-desc {
      font-size: 0.83rem;
      color: var(--muted);
      line-height: 1.55;
      margin-bottom: 0.6rem;
      flex-grow: 1;
    }
    /* Unified meta/CTA */
    .reviews-archive-grid .article-card .card-meta,
    .reviews-archive-grid .article-card .article-card-meta {
      font-size: 0.75rem;
      color: var(--muted);
      font-family: sans-serif;
      margin-top: auto;
    }
    .reviews-archive-grid .article-card .card-meta span { margin-right: 0.75rem; }
    .reviews-archive-grid .article-card .read-more,
    .reviews-archive-grid .article-card .card-cta {
      font-size: 0.8rem;
      color: var(--gold);
      font-family: sans-serif;
      margin-top: auto;
    }
    /* Hide card-img-wrap images (no images uploaded yet) */
    .reviews-archive-grid .article-card .card-img-wrap,
    .reviews-archive-grid .article-card .article-thumb { display: none; }
    /* article-body: unwrap it */
    .reviews-archive-grid .article-card .article-body,
    .reviews-archive-grid .article-card .card-body { display: contents; }
    @media (max-width: 900px) { .reviews-archive-grid { grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 1rem; } }
    @media (max-width: 500px) { .reviews-archive-grid { grid-template-columns: 1fr; } }
'''

# Inject CSS before </style>
content = content.replace('  </style>\n</head>', new_css + '  </style>\n</head>', 1)

# ── Find injection points ──────────────────────────────────────────────────────
# After carousel and section-inner close, before floating cards
# Pattern: the </div> at line 1980 is followed by a blank line then the first floating card
# More precisely: after the carousel-wrapper closing, section-inner closing, there are floating cards

# The text after carousel/section-inner closes:
floating_start_marker = '        </div>\n      \n              <a class="article-card"'
floating_start_wrap_open = (
    '        </div>\n'
    '      \n'
    '      <!-- ALL REVIEWS GRID -->\n'
    '      <div class="reviews-archive-section">\n'
    '        <div class="section-inner">\n'
    '          <div class="label">All reviews</div>\n'
    '          <div class="section-title" style="margin-bottom:1.5rem;">Every Guide We\'ve Published</div>\n'
    '          <div class="reviews-archive-grid">\n'
    '              <a class="article-card"'
)

if floating_start_marker in content:
    content = content.replace(floating_start_marker, floating_start_wrap_open, 1)
    print('Injected grid wrapper open')
else:
    print('ERROR: floating_start_marker not found')
    print('Looking for alternative...')
    # Try to find it with different whitespace
    idx = content.find('        </div>\n      ')
    if idx != -1:
        print(f'Found potential match at char {idx}')
        print(repr(content[idx:idx+120]))

# The floating cards end before </section>\n\n      <!-- TOP PICKS -->
floating_end_marker = '</section>\n\n      <!-- TOP PICKS -->'
floating_end_wrap_close = (
    '          </div><!-- /reviews-archive-grid -->\n'
    '        </div><!-- /section-inner -->\n'
    '      </div><!-- /reviews-archive-section -->\n'
    '      </section>\n\n      <!-- TOP PICKS -->'
)

if floating_end_marker in content:
    content = content.replace(floating_end_marker, floating_end_wrap_close, 1)
    print('Injected grid wrapper close')
else:
    print('ERROR: floating_end_marker not found')
    idx = content.find('</section>')
    print(f'First </section> at char {idx}')

if content != original:
    open('index.html', 'w', encoding='utf-8').write(content)
    print('Saved index.html')
else:
    print('No changes made')
