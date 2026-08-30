#!/usr/bin/env python3
"""Recover the 2003-2009 weblogs.java.net/blog/dwalend posts from Common Crawl.

Written because web.archive.org was unreachable for a full day in August 2026
while archive.org itself stayed up. Common Crawl's 2008-2009 and 2009-2010
indexes cover the tail of the java.net run and, as it turns out, hold snapshots
of the whole archive - the blog's own /archive/ pages were still linked, so the
crawler reached posts back to 2003.

Writes raw HTML into _archive-src/javanet/, one file per post, named
YYYY-MM-slug.html. Resumable: existing files are skipped.

    bin/fetch-javanet-cc.py --list    # inventory only, no downloads
    bin/fetch-javanet-cc.py           # fetch what is missing
"""
import gzip, html as html_mod, json, os, re, sys, time
import urllib.parse, urllib.request, urllib.error

# Every Common Crawl index from java.net's lifetime. The 2008-2010 crawls hold
# the whole 2003-2009 run because the blog's monthly /archive/ pages were still
# linked; the 2014-2015 crawls add alternate slugs and one extra post.
INDEX_YEARS = ("2008", "2009", "2010", "2012", "2013", "2014", "2015", "2016", "2017")

# today.java.net articles are a DIFFERENT SITE from the blog. They are listed on
# the author page, which is the only reliable way to enumerate them.
AUTHOR_PAGE = "today.java.net/pub/au/95*"
ARTICLES = "today.java.net/pub/a/today/*"
PATTERN = "weblogs.java.net/blog/dwalend/*"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "_archive-src", "javanet")
# /YYYY/MM/slug.html, but NOT /YYYY/MM/index.html - those are the
# monthly archive listings, not posts.
ARTICLE = re.compile(r"/(19|20)\d\d/\d\d/(?!index\.html$)[^/]+\.html$")
SLUG = re.compile(r"/((?:19|20)\d\d)/(\d\d)/([^/]+)\.html$")


def get(url, headers=None, tries=3):
    for n in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers or {})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except Exception as e:
            if n == tries - 1:
                raise
            print(f"    retry {n+1}: {e}", file=sys.stderr)
            time.sleep(5 * (n + 1))


def indexes():
    url = "https://index.commoncrawl.org/collinfo.json"
    ids = [c["id"] for c in json.loads(get(url).decode())]
    return [i for i in ids if any(y in i for y in INDEX_YEARS)]


def inventory(pattern=PATTERN, article_only=True):
    """Best snapshot per URL, preferring the largest capture."""
    best = {}
    for idx in indexes():
        url = (f"https://index.commoncrawl.org/{idx}-index"
               f"?url={urllib.parse.quote(pattern, safe='')}&output=json")
        try:
            raw = get(url, tries=1).decode("utf-8", "replace")
        except Exception:
            continue          # 404 = index has nothing; 5xx = try another index
        n = 0
        for line in raw.splitlines():
            if not line.startswith("{"):
                continue
            r = json.loads(line)
            # index rows are occasionally malformed - no length/offset
            if r.get("status") != "200" or "length" not in r or "offset" not in r:
                continue
            if article_only and not ARTICLE.search(r["url"]):
                continue
            n += 1
            prev = best.get(r["url"])
            if prev is None or int(r["length"]) > int(prev["length"]):
                best[r["url"]] = r
        if n:
            print(f"  {idx}: {n} rows")
    return best


def title_of(html):
    m = re.search(r"<title>(.*?)</title>", html.decode("utf-8", "replace"),
                  re.S | re.I)
    if not m:
        return None
    t = html_mod.unescape(m.group(1).strip())
    t = re.sub(r"^David Walend's Blog:\s*", "", t)
    return re.sub(r"\s*\|\s*Java\.net$", "", t)


def fetch(r):
    """Ranged read of one capture -> the HTTP response body."""
    off, ln = int(r["offset"]), int(r["length"])
    cc = f"https://data.commoncrawl.org/{r['filename']}"
    blob = gzip.decompress(get(cc, {"Range": f"bytes={off}-{off+ln-1}"}))
    return body_of(blob)


def slug_for(url):
    m = SLUG.search(url)
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"


def body_of(blob):
    """ARC record -> the HTTP response body."""
    # arc header line, then the HTTP response; headers end at the blank line
    return blob.split(b"\r\n\r\n", 1)[1]


def run(pattern, outdir, article_only, label):
    """Fetch a set of captures, skipping posts already on disk and any capture
    whose <title> duplicates one already written - Movable Type emitted two
    slugs for the same post (foo.html and foo_1.html), and counting slugs
    instead of titles inflates the total."""
    print(f"== {label} ==")
    best = inventory(pattern, article_only)
    print(f"unique URLs: {len(best)}")
    if "--list" in sys.argv:
        for u in sorted(best):
            print(f"  {u}")
        return 0

    os.makedirs(outdir, exist_ok=True)
    seen_titles = {}
    for f in sorted(os.listdir(outdir)):
        if f.endswith(".html"):
            with open(os.path.join(outdir, f), "rb") as fh:
                seen_titles[title_of(fh.read())] = f

    got = skipped = dup = failed = 0
    for u in sorted(best):
        dest = os.path.join(outdir, slug_for(u) + ".html")
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            skipped += 1
            continue
        try:
            html = fetch(best[u])
            if len(html) < 500:
                raise ValueError(f"suspiciously short: {len(html)} bytes")
            t = title_of(html)
            if t in seen_titles:
                dup += 1
                print(f"  dup  {slug_for(u)}  (same title as {seen_titles[t]})")
                continue
            with open(dest, "wb") as f:
                f.write(html)
            seen_titles[t] = os.path.basename(dest)
            got += 1
            print(f"  {slug_for(u)}  {len(html)}b  {t}")
        except Exception as e:
            failed += 1
            print(f"  FAIL {slug_for(u)}: {e}", file=sys.stderr)
            if os.path.exists(dest):
                os.remove(dest)
        time.sleep(0.4)
    print(f"-- fetched {got}, skipped {skipped}, dup titles {dup}, failed {failed}\n")
    return failed


def main():
    root = os.path.join(ROOT, "_archive-src")
    failed = run(PATTERN, os.path.join(root, "javanet"), True, "blog posts")

    # The articles live on a different site and cannot be guessed by URL
    # pattern. The author page lists them; parse it for /pub/a/ links.
    print("== today.java.net articles ==")
    au = inventory(AUTHOR_PAGE, article_only=False)
    links = set()
    for u in sorted(au, key=lambda x: -int(au[x]["length"])):
        try:
            page = fetch(au[u]).decode("utf-8", "replace")
        except Exception as e:
            print(f"  author page {u}: {e}", file=sys.stderr)
            continue
        links |= set(re.findall(r'href="(/pub/a/[^"]+\.html)"', page))
    print(f"articles listed on the author page: {len(links)}")

    outdir = os.path.join(root, "javanet-articles")
    os.makedirs(outdir, exist_ok=True)
    for href in sorted(links):
        full = "today.java.net" + href
        m = re.search(r"/(\d{4})/(\d{2})/(\d{2})/([^/]+)\.html$", href)
        name = f"{m.group(1)}-{m.group(2)}-{m.group(3)}-{m.group(4)}" if m \
            else href.strip("/").replace("/", "-")
        dest = os.path.join(outdir, name + ".html")
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            print(f"  have {name}")
            continue
        caps = inventory(full, article_only=False)
        if not caps:
            print(f"  NO CAPTURES {name}", file=sys.stderr)
            failed += 1
            continue
        r = max(caps.values(), key=lambda x: int(x["length"]))
        try:
            html = fetch(r)
            with open(dest, "wb") as f:
                f.write(html)
            print(f"  {name}  {len(html)}b  {title_of(html)}")
        except Exception as e:
            print(f"  FAIL {name}: {e}", file=sys.stderr)
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
