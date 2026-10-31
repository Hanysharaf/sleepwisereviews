"""Nightly SWR audit, REPORT ONLY. Standard library only. Counts per class, no fixes.

Usage: python automation/audit_nightly.py [--date YYYY-MM-DD] [--out reports/audit]
Writes <out>/<date>.md. Reads files in the repo; the only network call is the GitHub
Actions API for class 1, and only when GITHUB_TOKEN and GITHUB_REPOSITORY are set.
Same repo state -> same report (no clock values are written into the file).
"""
import argparse
import ast
import html as htmllib
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://sleepwisereviews.com"
TAG = "sleepwiserevi-20"
IG = "instagram.com/sleepwise.reviews"
NA = "needs secret / not available"

AMAZON_A = re.compile(r'<a\b[^>]*href="(https?://(?:www\.)?amazon\.com[^"]*)"[^>]*>', re.I)
HREF = re.compile(r'<a\b[^>]*?\bhref="([^"]*)"', re.I)
JSONLD = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)


def read(p):
    return p.read_text(encoding="utf-8", errors="replace")


def is_stub(t):
    return bool(re.search(r'<meta name="robots" content="[^"]*noindex', t)) or "This guide has moved" in t


def visible(t):
    t = re.sub(r"<script.*?</script>|<style.*?</style>|<head>.*?</head>", " ", t, flags=re.S)
    t = htmllib.unescape(re.sub(r"<[^>]+>", " ", t))
    return re.sub(r"\s+", " ", t).strip().lower()


def norm(s):
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", s))).strip().lower()


def url_to_path(u):
    if not u.startswith(BASE):
        return None
    rel = u[len(BASE):].split("#")[0].split("?")[0].lstrip("/")
    if rel == "" or rel.endswith("/"):
        rel += "index.html"
    return ROOT / rel


def load_files():
    pub = {}
    for p in sorted(ROOT.glob("*.html")):
        pub[p] = "root"
    for p in sorted((ROOT / "pages").glob("*.html")):
        pub[p] = "pages"
    for p in sorted((ROOT / "posts").glob("*.html")):
        pub[p] = "posts"
    for p in sorted((ROOT / "posts" / "category").glob("*.html")):
        pub[p] = "category"
    return pub


def broken_links(path, t, base_dir):
    n = 0
    for h in HREF.findall(t):
        h = htmllib.unescape(h).strip()
        if not h or h.startswith(("#", "mailto:", "tel:", "javascript:", "data:", "//")):
            continue
        if re.match(r"^[a-z][a-z0-9+.-]*:", h, re.I):
            if not h.startswith(BASE):
                continue
            target = url_to_path(h)
        else:
            clean = h.split("#")[0].split("?")[0]
            if clean == "":
                continue
            target = (base_dir / clean) if not clean.startswith("/") else ROOT / clean.lstrip("/")
        if target is None:
            continue
        if target.is_dir():
            target = target / "index.html"
        if not target.exists():
            n += 1
    return n


def check_html(t, base_dir, path):
    """Per-file measurements shared by published files and the queue."""
    r = {}
    r["broken_links"] = broken_links(path, t, base_dir)
    r["no_canonical"] = 'rel="canonical"' not in t
    for p in ("og:title", "og:description", "og:url", "og:image"):
        r["no_" + p] = ('property="%s"' % p) not in t
    m = re.search(r'property="og:image" content="([^"]*)"', t)
    r["og_image_missing_file"] = False
    if m:
        tp = url_to_path(m.group(1))
        r["og_image_missing_file"] = tp is not None and not tp.exists()
    amz = AMAZON_A.findall(t)
    r["amz_links"] = len(amz)
    notag = norel = 0
    for a in AMAZON_A.finditer(t):
        url = a.group(1)
        if re.search(r"amazon\.com/shop/", url):
            continue
        if "tag=" + TAG not in url:
            notag += 1
        rel = re.search(r'\srel="([^"]*)"', a.group(0))
        toks = rel.group(1).split() if rel else []
        if not ("sponsored" in toks and "nofollow" in toks):
            norel += 1
    r["amz_notag"] = notag
    r["amz_norel"] = norel
    r["no_ig"] = IG not in t
    return r


def faq(t):
    """(has_faq_schema, schema_questions, zero_visible, partly_missing, parse_errors)"""
    qs = []
    errs = 0
    for blk in JSONLD.findall(t):
        try:
            data = json.loads(blk)
        except Exception:
            errs += 1
            continue
        items = data if isinstance(data, list) else [data]
        flat = []
        for d in items:
            flat += d.get("@graph", [d]) if isinstance(d, dict) else []
        for d in flat:
            if isinstance(d, dict) and d.get("@type") == "FAQPage":
                for q in d.get("mainEntity", []) or []:
                    ans = (q.get("acceptedAnswer") or {}).get("text", "")
                    qs.append((norm(q.get("name", "")), norm(ans)[:80]))
    if not qs:
        return False, 0, False, False, errs
    vis = visible(t)
    found_q = sum(1 for q, a in qs if q and q in vis)
    ok = sum(1 for q, a in qs if q and q in vis and a and a in vis)
    return True, len(qs), found_q == 0, ok < len(qs), errs


def load_categories():
    src = (ROOT / "generate_posts_index.py")
    if not src.exists():
        return None
    for node in ast.parse(read(src)).body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "CATEGORIES":
            return ast.literal_eval(node.value)
    return None


def gh_api(path):
    req = urllib.request.Request(
        "https://api.github.com" + path,
        headers={"Authorization": "Bearer " + os.environ["GITHUB_TOKEN"],
                 "Accept": "application/vnd.github+json", "User-Agent": "swr-audit"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)


def class_workflows():
    if not (os.environ.get("GITHUB_TOKEN") and os.environ.get("GITHUB_REPOSITORY")):
        return None, NA + " (no GITHUB_TOKEN here)"
    repo = os.environ["GITHUB_REPOSITORY"]
    try:
        wfs = gh_api("/repos/%s/actions/workflows" % repo)["workflows"]
        bad = checked = 0
        for w in wfs:
            if w["path"].endswith("nightly-audit.yml") or w["state"] != "active" or not w["path"].startswith(".github/"):
                continue
            runs = gh_api("/repos/%s/actions/workflows/%d/runs?per_page=1&status=completed" % (repo, w["id"]))["workflow_runs"]
            if not runs:
                continue
            checked += 1
            if runs[0]["conclusion"] != "success":
                bad += 1
        return bad, "%d workflows with a last completed run, %d not success" % (checked, bad)
    except Exception as e:
        return None, "API error: %s" % type(e).__name__


def main():
    ap = argparse.ArgumentParser()
    cairo_today = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime("%Y-%m-%d")
    ap.add_argument("--date", default=cairo_today)
    ap.add_argument("--out", default="reports/audit")
    args = ap.parse_args()

    pub = load_files()
    rows = []  # (n, class, count or None, detail)

    # --- per-file pass over published files ---
    agg = {k: 0 for k in ("broken_links", "broken_files", "no_canonical", "no_og:title", "no_og:description",
                          "no_og:url", "no_og:image", "og_image_missing_file", "amz_links", "amz_notag",
                          "amz_notag_files", "amz_norel", "amz_norel_files", "no_ig_posts", "handle_files",
                          "faq_pages", "faq_zero_visible", "faq_partial", "jsonld_errors", "stale_titles",
                          "sleepbuds_files")}
    posts = {}
    titles, descs = {}, {}
    sitemap_text = read(ROOT / "sitemap.xml") if (ROOT / "sitemap.xml").exists() else ""
    for p, kind in pub.items():
        t = read(p)
        r = check_html(t, p.parent, p)
        stub = is_stub(t)
        agg["broken_links"] += r["broken_links"]
        agg["broken_files"] += 1 if r["broken_links"] else 0
        if not stub:  # noindex stubs and 404 pages are not checked for canonical/OG
            agg["no_canonical"] += r["no_canonical"]
            for k in ("no_og:title", "no_og:description", "no_og:url", "no_og:image", "og_image_missing_file"):
                agg[k] += r[k]
        agg["amz_links"] += r["amz_links"]
        agg["amz_notag"] += r["amz_notag"]
        agg["amz_norel"] += r["amz_norel"]
        agg["amz_notag_files"] += 1 if r["amz_notag"] else 0
        agg["amz_norel_files"] += 1 if r["amz_norel"] else 0
        if re.search(r"@sleepwisereviews(?![.\w])|instagram\.com/sleepwisereviews", t, re.I):
            agg["handle_files"] += 1
        has, nq, zero, partial, errs = faq(t)
        agg["jsonld_errors"] += errs
        if has:
            agg["faq_pages"] += 1
            agg["faq_zero_visible"] += zero
            agg["faq_partial"] += (partial and not zero)
        if kind == "posts" and p.name != "index.html":
            if not stub:
                posts[p.stem] = t
                agg["no_ig_posts"] += r["no_ig"]
                tm = re.search(r"<title>(.*?)</title>", t, re.S)
                title = norm(tm.group(1)) if tm else ""
                if re.search(r"\b(2023|2024|2025)\b", title):
                    agg["stale_titles"] += 1
                titles.setdefault(title, []).append(p.stem)
                dm = re.search(r'<meta name="description" content="([^"]*)"', t)
                if dm:
                    descs.setdefault(norm(dm.group(1)), []).append(p.stem)
                if re.search(r"sleepbuds", t, re.I):
                    agg["sleepbuds_files"] += 1
    n_ind = len(posts)

    # 1 workflow health
    c, d = class_workflows()
    rows.append((1, "Workflow health", c, d))

    # 2 sitemap
    try:
        root = ET.fromstring(sitemap_text)
        ns_ok = root.tag == "{http://www.sitemaps.org/schemas/sitemap/0.9}urlset"
        locs = [e.text.strip() for e in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    except Exception:
        ns_ok, locs = False, []
    dup = len(locs) - len(set(locs))
    nofile = sum(1 for u in locs if (url_to_path(u) is None or not url_to_path(u).exists()))
    stub_listed = sum(1 for u in locs if url_to_path(u) and url_to_path(u).exists() and is_stub(read(url_to_path(u))))
    locset = set(locs)
    missing = sum(1 for s in posts if "%s/posts/%s.html" % (BASE, s) not in locset)
    s_prob = (0 if ns_ok else 1) + dup + nofile + stub_listed + missing
    rows.append((2, "Sitemap", s_prob, "xmlns valid=%s; %d URLs; duplicates %d; URLs without file %d; stubs listed %d; indexable posts missing %d"
                 % (ns_ok, len(locs), dup, nofile, stub_listed, missing)))

    # 3 broken internal links
    rows.append((3, "Broken internal links", agg["broken_links"], "%d links in %d published files" % (agg["broken_links"], agg["broken_files"])))

    # 4 canonical / OG / og:image
    n4 = agg["no_canonical"] + agg["no_og:title"] + agg["no_og:description"] + agg["no_og:url"] + agg["no_og:image"] + agg["og_image_missing_file"]
    rows.append((4, "Canonical / OG / og:image", n4,
                 "canonical missing %d; og:title %d; og:description %d; og:url %d; og:image %d; og:image file missing %d (live HTTP status of og:image not checked)"
                 % (agg["no_canonical"], agg["no_og:title"], agg["no_og:description"], agg["no_og:url"], agg["no_og:image"], agg["og_image_missing_file"])))

    # 5 affiliate
    rows.append((5, "Affiliate links", agg["amz_notag"] + agg["amz_norel"],
                 "%d amazon links; without tag %s: %d in %d files; without rel sponsored+nofollow: %d in %d files"
                 % (agg["amz_links"], TAG, agg["amz_notag"], agg["amz_notag_files"], agg["amz_norel"], agg["amz_norel_files"])))

    # 6 handle drift
    rows.append((6, "Handle / brand drift", agg["handle_files"], "published html files with @sleepwisereviews (no dot)"))

    # 7 IG CTA
    rows.append((7, "IG CTA", agg["no_ig_posts"], "of %d indexable posts" % n_ind))

    # 8 FAQ schema
    rows.append((8, "FAQ schema vs visible", agg["faq_zero_visible"] + agg["faq_partial"] + agg["jsonld_errors"],
                 "%d pages with FAQPage JSON-LD; zero visible FAQ %d; reworded or partly missing %d (heuristic, upper bound); JSON-LD parse errors %d"
                 % (agg["faq_pages"], agg["faq_zero_visible"], agg["faq_partial"], agg["jsonld_errors"])))

    # 9 uncategorised / duplicate
    cats = load_categories()
    if cats is None:
        rows.append((9, "Uncategorised or duplicate posts", None, "generate_posts_index.py CATEGORIES not readable"))
    else:
        seen = {}
        for cname, slugs in cats.items():
            for s in slugs:
                seen.setdefault(s, []).append(cname)
        unc = sum(1 for s in posts if s not in seen)
        two = sum(1 for s, v in seen.items() if len(set(v)) > 1)
        gone = sum(1 for s in seen if not (ROOT / "posts" / (s + ".html")).exists())
        dt = sum(1 for v in titles.values() if len(v) > 1)
        dd = sum(1 for v in descs.values() if len(v) > 1)
        rows.append((9, "Uncategorised or duplicate posts", unc + two + dt + dd,
                     "uncategorised %d; in two categories %d; listed but file missing %d (not counted); duplicate title groups %d; duplicate description groups %d"
                     % (unc, two, gone, dt, dd)))

    # 10 stale
    rows.append((10, "Stale / discontinued", agg["stale_titles"] + agg["sleepbuds_files"],
                 "indexable posts with 2023/2024/2025 in title %d; posts mentioning Bose Sleepbuds %d (list only)"
                 % (agg["stale_titles"], agg["sleepbuds_files"])))

    # 11, 12 need credentials
    rows.append((11, "Instagram queue", None, NA + " (Google Sheets service account)"))
    rows.append((12, "Indexing trend", None, NA + " (Search Console)"))

    # queue (scheduled/, not _published): classes 3, 4, 5, 7 on files that will be published next
    q = {"files": 0, "broken_cat": 0, "no_ig": 0, "no_og": 0, "norel": 0, "notag": 0}
    for p in sorted((ROOT / "scheduled").glob("*.html")):
        t = read(p)
        r = check_html(t, ROOT / "posts", p)  # links resolve as they will from posts/
        q["files"] += 1
        q["broken_cat"] += 1 if any(not (ROOT / "pages" / m).exists() for m in re.findall(r'href="\.\./pages/(category-[^"]+)"', t)) else 0
        q["no_ig"] += r["no_ig"]
        q["no_og"] += 1 if (r["no_og:title"] or r["no_og:image"] or r["no_og:description"] or r["no_og:url"]) else 0
        q["norel"] += r["amz_norel"]
        q["notag"] += r["amz_notag"]

    lines = ["# SWR nightly audit %s" % args.date, "",
             "Report only. Counts only. No file was changed by this run except this report.", "",
             "Population: %d published html files (%d indexable posts, %d noindex stubs/moved), %d files in scheduled/ queue."
             % (len(pub), n_ind, sum(1 for p, k in pub.items() if k == "posts" and p.name != "index.html") - n_ind, q["files"]), "",
             "| # | Class | Problems | Detail |", "|---|---|---|---|"]
    for n, name, c, d in rows:
        lines.append("| %d | %s | %s | %s |" % (n, name, "n/a" if c is None else c, d))
    lines += ["", "## Queue (scheduled/), published next by publish_scheduler", "",
              "| Check | Count |", "|---|---|",
              "| files in queue | %d |" % q["files"],
              "| files linking to a missing category page | %d |" % q["broken_cat"],
              "| files without Instagram CTA | %d |" % q["no_ig"],
              "| files missing an og tag | %d |" % q["no_og"],
              "| amazon links without rel sponsored+nofollow | %d |" % q["norel"],
              "| amazon links without tag %s | %d |" % (TAG, q["notag"]), ""]
    out = ROOT / args.out
    out.mkdir(parents=True, exist_ok=True)
    f = out / (args.date + ".md")
    f.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print("\n".join(lines))
    print("wrote", f.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
