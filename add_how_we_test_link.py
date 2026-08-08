import glob

OLD = '<div class="author-role" style="color:#7A85A0;font-size:0.82rem;">Independent Sleep Researcher</div>'
NEW = ('<div class="author-role" style="color:#7A85A0;font-size:0.82rem;">'
       'Independent Sleep Researcher &middot; '
       '<a href="../pages/how-we-test.html" style="color:#7A85A0;text-decoration:underline;">How we test</a>'
       '</div>')

changed = []
skipped_no_match = []
skipped_already_linked = []

for path in glob.glob("posts/*.html"):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "how-we-test.html" in content:
        skipped_already_linked.append(path)
        continue

    if OLD not in content:
        skipped_no_match.append(path)
        continue

    count = content.count(OLD)
    if count != 1:
        skipped_no_match.append(path + f" (found {count}x, expected 1)")
        continue

    new_content = content.replace(OLD, NEW)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new_content)
    changed.append(path)

print(f"Changed: {len(changed)}")
print(f"Already linked (skipped): {len(skipped_already_linked)}")
print(f"No exact match (skipped): {len(skipped_no_match)}")
if skipped_no_match:
    print("\nFirst 10 no-match files:")
    for p in skipped_no_match[:10]:
        print(" -", p)
