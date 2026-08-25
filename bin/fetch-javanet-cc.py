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
import gzip, json, os, re, sys, time, urllib.request, urllib.error

INDEXES = ["CC-MAIN-2008-2009", "CC-MAIN-2009-2010"]
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


def inventory():
    """Best snapshot per article URL, preferring the largest capture."""
    best = {}
    for idx in INDEXES:
        url = (f"https://index.commoncrawl.org/{idx}-index"
               f"?url={urllib.parse.quote(PATTERN, safe='')}&output=json")
        print(f"querying {idx} ...")
        raw = get(url).decode("utf-8", "replace")
        for line in raw.splitlines():
            if not line.startswith("{"):
                continue
            r = json.loads(line)
            if r.get("status") != "200" or not ARTICLE.search(r["url"]):
                continue
            prev = best.get(r["url"])
            if prev is None or int(r["length"]) > int(prev["length"]):
                best[r["url"]] = r
    return best


def slug_for(url):
    m = SLUG.search(url)
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"


def body_of(blob):
    """ARC record -> the HTTP response body."""
    # arc header line, then the HTTP response; headers end at the blank line
    return blob.split(b"\r\n\r\n", 1)[1]


def main():
    import urllib.parse  # noqa: F401  (used via urllib.parse.quote above)
    best = inventory()
    print(f"unique articles: {len(best)}")
    if "--list" in sys.argv:
        for u in sorted(best):
            print(f"  {slug_for(u)}  {best[u]['length']:>7}b  {u}")
        return 0

    os.makedirs(OUT, exist_ok=True)
    got = skipped = failed = 0
    for u in sorted(best):
        r = best[u]
        dest = os.path.join(OUT, slug_for(u) + ".html")
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            skipped += 1
            continue
        off, ln = int(r["offset"]), int(r["length"])
        cc = f"https://data.commoncrawl.org/{r['filename']}"
        try:
            blob = gzip.decompress(get(cc, {"Range": f"bytes={off}-{off+ln-1}"}))
            html = body_of(blob)
            if len(html) < 500:
                raise ValueError(f"suspiciously short: {len(html)} bytes")
            with open(dest, "wb") as f:
                f.write(html)
            got += 1
            print(f"  {slug_for(u)}  {len(html)}b")
        except Exception as e:
            failed += 1
            print(f"  FAIL {slug_for(u)}: {e}", file=sys.stderr)
            if os.path.exists(dest):
                os.remove(dest)
        time.sleep(0.5)
    print(f"--- fetched {got}, skipped {skipped}, failed {failed} ---")
    print(f"raw HTML in {OUT}")
    return 1 if failed else 0


if __name__ == "__main__":
    import urllib.parse
    sys.exit(main())
