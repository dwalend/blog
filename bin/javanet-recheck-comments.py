#!/usr/bin/env python3
"""Look for Movable-Type-era captures of the posts whose Drupal capture has no comments.

java.net's move from Movable Type to Drupal appears to have dropped the comment
threads on older posts, and bin/fetch-javanet-cc.py keeps only the *largest*
capture per URL - a bulky comment-free Drupal page can outweigh a lean MT page
that still has the thread. So for these URLs, fetch every capture rather than
the biggest one, and keep whichever has the most comments.

Writes better captures to _archive-src/javanet/ as SLUG.mt.html and leaves the
existing file alone, so the two can be compared before anything is replaced.
"""
import importlib.util, json, os, re, sys, time, urllib.parse

spec = importlib.util.spec_from_file_location("cc", os.path.join(os.path.dirname(os.path.abspath(__file__)), "fetch-javanet-cc.py"))
cc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cc)

# The Drupal-shape captures that carry no comments at all.
SLUGS = [
    "2003/09/design_for_reus", "2003/10/reviewing_the_j", "2004/01/coupling_in_sof",
    "2004/06/somnifugijms_fo_4", "2005/08/graphviz_class", "2006/05/no_giant_or_win_1",
    "2006/06/brilliant_appro", "2006/06/our_grass_is_gr", "2006/09/whooshing_sound_1",
    "2006/11/bad_things_in_a", "2007/03/wild_winds_wres_1", "2008/06/jmx_and_testdri_1",
]

COMMENT_MARKERS = (re.compile(r'<div id="c\d+">'), re.compile(r'class="comment comment-published'))


def count_comments(html):
    text = html.decode("utf-8", "replace")
    return max(len(p.findall(text)) for p in COMMENT_MARKERS)


def main():
    idxs = cc.indexes()
    print(f"{len(idxs)} indexes, {len(SLUGS)} URLs", file=sys.stderr)
    for slug in SLUGS:
        url = f"weblogs.java.net/blog/dwalend/archive/{slug}.html"
        rows, errors = {}, 0
        for idx in idxs:
            q = (f"https://index.commoncrawl.org/{idx}-index"
                 f"?url={urllib.parse.quote(url, safe='')}&output=json")
            try:
                raw = cc.get(q, tries=1).decode("utf-8", "replace")
            except Exception as e:
                # A 404 means the index genuinely has nothing. Anything else -
                # a 503, a refused connection - means we did not ask, and
                # counting that as "no captures" is how a rate limit turns into
                # a false finding. Count them and say so.
                if "404" not in str(e):
                    errors += 1
                continue
            time.sleep(1)     # index.commoncrawl.org blocks a fast caller outright
            for line in raw.splitlines():
                if not line.startswith("{"):
                    continue
                r = json.loads(line)
                if r.get("status") != "200" or "length" not in r or "offset" not in r:
                    continue
                rows[(r["filename"], r["offset"])] = r
        best, best_n = None, 0
        for r in rows.values():
            try:
                html = cc.fetch(r)
            except Exception as e:
                print(f"  {slug}: fetch failed {e}", file=sys.stderr)
                continue
            n = count_comments(html)
            if n > best_n:
                best, best_n = html, n
        name = slug.replace("/", "-", 1).replace("/", "-")
        note = f", {errors}/{len(idxs)} indexes UNREACHABLE - result not trustworthy" if errors else ""
        print(f"{name}: {len(rows)} captures, best comment count {best_n}{note}", flush=True)
        if best_n:
            open(os.path.join(cc.OUT, f"{name}.mt.html"), "wb").write(best)


if __name__ == "__main__":
    main()
