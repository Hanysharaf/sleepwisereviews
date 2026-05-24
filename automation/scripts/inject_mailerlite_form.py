"""
inject_mailerlite_form.py
Injects MailerLite signup form into the 7-day-sleep-reset.html page
and optionally into high-traffic post pages.

Usage:
    python automation/scripts/inject_mailerlite_form.py --form-id YOUR_FORM_ID
    python automation/scripts/inject_mailerlite_form.py --form-id abc123 --all-posts

Hany: Get your form ID from MailerLite -> Forms -> Embedded Forms -> Copy code
The ID is in the data-form="..." attribute of the embed script.
"""

import argparse
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# High-traffic posts to inject form (based on Search Console top pages)
HIGH_TRAFFIC_POSTS = [
    "posts/best-pillow-side-sleepers.html",
    "posts/article-magnesium-sleep.html",
    "posts/best-white-noise-machines-sleeping.html",
    "posts/waking-at-3am.html",
    "posts/sleep-hygiene-checklist.html",
    "posts/best-sleep-supplements-guide.html",
    "posts/article-weighted-blanket.html",
    "7-day-sleep-reset.html",
]

FORM_HTML_TEMPLATE = """
<!-- MailerLite signup form -->
<div class="email-signup-section" style="background:linear-gradient(135deg,#1a1a40,#0d0d2b);border:1px solid rgba(255,191,128,.2);border-radius:12px;padding:2rem;margin:2rem 0;text-align:center">
  <p style="color:#ffbf80;font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;margin:0 0 .75rem">Free Guide</p>
  <h3 style="color:#f0e6c8;font-family:'Georgia',serif;font-size:1.5rem;margin:0 0 .75rem;font-weight:600">7-Day Sleep Reset Guide</h3>
  <p style="color:#b8c8e8;font-size:.95rem;margin:0 0 1.5rem;max-width:400px;display:inline-block">Evidence-based protocol. Day-by-day. No supplements required for Week 1.</p>
  <div class="ml-embedded" data-form="{FORM_ID}"></div>
</div>
<script>
  (function(w,d,e,u,f,l,n){{w[f]=w[f]||function(){{(w[f].q=w[f].q||[]).push(arguments);}},l=d.createElement(e),l.async=1,l.src=u,n=d.getElementsByTagName(e)[0],n.parentNode.insertBefore(l,n);}})
  (window,document,'script','https://assets.mailerlite.com/js/universal.js','ml');
  ml('account', '{ACCOUNT_ID}');
</script>
<!-- End MailerLite -->
"""

INJECT_BEFORE = "</main>"  # Inject before closing main tag


def inject_form(html_path: Path, form_id: str, account_id: str) -> bool:
    content = html_path.read_text(encoding="utf-8")
    form_html = FORM_HTML_TEMPLATE.replace("{FORM_ID}", form_id).replace("{ACCOUNT_ID}", account_id)

    if "ml-embedded" in content:
        print(f"  SKIP {html_path.name} — form already injected")
        return False

    if INJECT_BEFORE not in content:
        print(f"  SKIP {html_path.name} — no {INJECT_BEFORE!r} anchor found")
        return False

    new_content = content.replace(INJECT_BEFORE, form_html + INJECT_BEFORE, 1)
    html_path.write_text(new_content, encoding="utf-8")
    print(f"  OK   {html_path.name}")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--form-id", required=True, help="MailerLite form ID (from embed code)")
    parser.add_argument("--account-id", default="", help="MailerLite account ID (optional)")
    parser.add_argument("--all-posts", action="store_true", help="Inject into all high-traffic posts")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    targets = ["7-day-sleep-reset.html"]
    if args.all_posts:
        targets = HIGH_TRAFFIC_POSTS

    print(f"Injecting MailerLite form {args.form_id!r} into {len(targets)} pages...")

    done = 0
    for rel_path in targets:
        html_path = BASE_DIR / rel_path
        if not html_path.exists():
            print(f"  MISS {rel_path} — file not found")
            continue
        if args.dry_run:
            print(f"  DRY  {html_path.name}")
            continue
        if inject_form(html_path, args.form_id, args.account_id):
            done += 1

    print(f"\nDone: {done} pages updated")
    if done:
        print("Next step: git add -p; git commit -m 'feat: inject MailerLite signup form'; git push")


if __name__ == "__main__":
    main()
