#!/usr/bin/env python3
"""Recover the four images the java.net posts point at.

bloggers.dev.java.net is gone, so both surviving posts that use images render
broken. These are worth recovering rather than cutting: two are source-directory
diagrams in "Design for Reuse", two are GraphViz class diagrams in "GraphViz
Class Diagrams", and all four could be redrawn from the posts if no archive has
them.

Tries the wayback machine first - it holds far more than Common Crawl - and
falls back to Common Crawl. Writes into src/img/archive/. Resumable.

Reports unreachable archives as unreachable. An archive that will not answer is
not an archive that has nothing.
"""
import importlib.util, json, os, sys, time, urllib.error, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("cc", os.path.join(HERE, "fetch-javanet-cc.py"))
cc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cc)

OUT = os.path.join(os.path.dirname(HERE), "src", "img", "archive")
BASE = "bloggers.dev.java.net/files/documents/84"
IMAGES = [
    (f"{BASE}/1073/projects-first-way.jpg", "projects-first-way.jpg"),
    (f"{BASE}/1074/projects-second-way.jpg", "projects-second-way.jpg"),
    (f"{BASE}/18669/classDigraph.gif", "classDigraph.gif"),
    (f"{BASE}/18670/classDigraph.svg", "classDigraph.svg"),
]


def from_wayback(url, tries=4):
    # web.archive.org answers 429 under load rather than failing outright, so
    # back off and ask again instead of treating a throttle as an absence.
    for n in range(tries):
        try:
            return _wayback(url)
        except urllib.error.HTTPError as e:
            if e.code != 429 or n == tries - 1:
                raise
            wait = 20 * (n + 1)
            print(f"    wayback 429, waiting {wait}s")
            time.sleep(wait)


def _wayback(url):
    cdx = ("https://web.archive.org/cdx/search/cdx?"
           f"url={urllib.parse.quote(url, safe='')}&output=json&filter=statuscode:200&limit=5")
    rows = json.loads(cc.get(cdx, tries=1).decode("utf-8", "replace") or "[]")
    if len(rows) < 2:
        return None
    fields = rows[0]
    stamp = rows[1][fields.index("timestamp")]
    # id_ asks for the original bytes, without the wayback toolbar rewrite.
    return cc.get(f"https://web.archive.org/web/{stamp}id_/https://{url}", tries=1)


def from_commoncrawl(url):
    for idx in cc.indexes():
        q = (f"https://index.commoncrawl.org/{idx}-index"
             f"?url={urllib.parse.quote(url, safe='')}&output=json")
        try:
            raw = cc.get(q, tries=1).decode("utf-8", "replace")
        except Exception:
            continue
        for line in raw.splitlines():
            if not line.startswith("{"):
                continue
            r = json.loads(line)
            if r.get("status") == "200" and "offset" in r:
                return cc.fetch(r)
    return None


def main():
    os.makedirs(OUT, exist_ok=True)
    missing = []
    for url, name in IMAGES:
        dest = os.path.join(OUT, name)
        if os.path.exists(dest):
            print(f"  have {name}")
            continue
        for source, fn in (("wayback", from_wayback), ("commoncrawl", from_commoncrawl)):
            try:
                blob = fn(url)
            except Exception as e:
                print(f"  {name}: {source} UNREACHABLE ({e})")
                continue
            if blob:
                open(dest, "wb").write(blob)
                time.sleep(5)
                print(f"  {name}: {len(blob)} bytes from {source}")
                break
        else:
            missing.append(name)
            print(f"  {name}: not found")
    if missing:
        print("\nstill missing:", ", ".join(missing))
        print("All four are reproducible from the posts if no archive has them.")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
