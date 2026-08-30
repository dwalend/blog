#!/usr/bin/env python3
"""Extract titles, dates, bodies, and comments from the recovered java.net HTML.

The recovered pages come in four shapes. Which shape a page has depends on when
Common Crawl visited it, not on when the post was written - java.net moved the
blog from Movable Type to Drupal in 2008, keeping the old archive URLs, so a
2003 post can arrive in either shape.

  mt      Movable Type: <h3> title, "Posted by <b>dwalend</b> on <date>",
          comments as <div id="cNNNN"> ending in <p class="posted">.
  drupal  <h2 class="title">, <div id="blog-submitted">, taxonomy links,
          comments as <div class="comment comment-published">.
  soa     today.java.net article template (one page).
  j1      java.net session-abstract template (one page).

Usage:
  bin/javanet-extract.py            # write the inventory JSON to stdout
  bin/javanet-extract.py --table    # one line per page, for reading
"""

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIRS = [ROOT / "_archive-src" / "javanet", ROOT / "_archive-src" / "javanet-articles"]

MONTHS = {
    m: i + 1
    for i, m in enumerate(
        "January February March April May June July August September "
        "October November December".split()
    )
}


def unent(s):
    return html.unescape(s or "").strip()


def strip_tags(s):
    return unent(re.sub(r"<[^>]+>", "", s))


def us_date(text):
    """'October 06, 2003 at 04:57 AM' -> ('2003-10-06', '04:57 AM')."""
    m = re.search(
        r"([A-Z][a-z]+)\s+(\d{1,2}),\s*(\d{4})(?:\s+at\s+(\d{1,2}:\d{2}\s*[AP]M))?", text
    )
    if not m:
        return None, None
    mon, day, year, time = m.groups()
    if mon not in MONTHS:
        return None, None
    return f"{int(year):04d}-{MONTHS[mon]:02d}-{int(day):02d}", (time or "").strip()


def between(text, start_pat, end_pats):
    """Text after the first match of start_pat, up to the earliest end pattern."""
    m = re.search(start_pat, text, re.S)
    if not m:
        return None
    rest = text[m.end() :]
    cut = len(rest)
    for pat in end_pats:
        e = re.search(pat, rest, re.S)
        if e:
            cut = min(cut, e.start())
    out = rest[:cut].strip()
    # The end markers sit outside the content div, so its closing tag rides along.
    return re.sub(r"(?:\s*(?:</div>|<p>|<br\s*/?>))+$", "", out).strip()


def detect(text):
    if re.search(r"<title>java\.net:", text):
        return "soa"
    if re.search(r"Posted by <b>dwalend</b> on", text):
        return "mt"
    if 'id="blog-submitted"' in text:
        return "drupal"
    if 'class="date-display-single"' in text:
        return "j1"
    return "unknown"


def parse_mt(text):
    title = strip_tags(re.search(r"<h3>(.*?)</h3>", text, re.S).group(1))
    posted = re.search(r"Posted by <b>dwalend</b> on ([^<|]+)", text).group(1)
    date, time = us_date(posted)
    body = between(
        text,
        r"Posted by <b>dwalend</b>.*?</span>\s*(?:<br\s*/?>\s*)*",
        [r'<div id="a\d+more"', r"<br\s*/?>\s*\nBookmark blog post:", r'<a name="comments">'],
    )
    comments = []
    for block in re.findall(r'<div id="c\d+">(.*?)</div>', text, re.S):
        p = re.search(
            r'<p class="posted">\s*<span[^>]*>Posted by:\s*(.*?)\s+on\s+([^<]+)</span>', block, re.S
        )
        if not p:
            continue
        cdate, ctime = us_date(p.group(2))
        comments.append(
            {
                "author": strip_tags(p.group(1)),
                "date": cdate,
                "time": ctime,
                "body": block[: p.start()].strip(),
            }
        )
    return title, date, time, body, comments, []


def parse_drupal(text):
    # Three Drupal themes ran over the blog's life. They differ in where the
    # title lives and in what follows the body, so each is a fallback chain
    # rather than a separate parser.
    t = (
        re.search(r'<h1 id="page-title">(.*?)</h1>', text, re.S)
        or re.search(r'<h2 class="title">(.*?)</h2>', text, re.S)
        or re.search(r"<title>(.*?)\s*\|\s*Java\.net</title>", text, re.S)
    )
    title = strip_tags(t.group(1))
    posted = re.search(r'<div id="blog-submitted">(.*?)</div>', text, re.S).group(1)
    date, time = us_date(strip_tags(posted))
    body = between(
        text,
        r'<div id="blog-submitted">.*?</div>\s*'
        r'(?:<div class="content">)?(?:<span class=.print-link.></span>)?',
        [
            r'<div class="links">&raquo;',
            r'<div class="taxonomy">',
            r'<div class="node-links">',
            r'<div id="comment-header">',
        ],
    )
    tax = re.search(r'<div class="taxonomy">(.*?)</div>\s*(?:</div>)?', text, re.S)
    tags = (
        [strip_tags(a) for a in re.findall(r'<a href="/(?:blogs/)?topic[/s]\S*?"[^>]*>(.*?)</a>', tax.group(1), re.S)]
        if tax
        else []
    )
    comments = []
    for block in re.findall(
        r'<div class="comment comment-published[^"]*">(.*?)<ul class="links">', text, re.S
    ):
        s = re.search(r'<div class="submitted">\s*Submitted by (.*?) on (.*?)\.\s*</div>', block, re.S)
        c = re.search(r'<div class="content">(.*?)</div>', block, re.S)
        if not (s and c):
            continue
        iso = re.search(r"(\d{4})-(\d{2})-(\d{2})\s+(\d{2}:\d{2})", s.group(2))
        comments.append(
            {
                "author": strip_tags(s.group(1)),
                "date": f"{iso.group(1)}-{iso.group(2)}-{iso.group(3)}" if iso else None,
                "time": iso.group(4) if iso else None,
                "body": c.group(1).strip(),
            }
        )
    return title, date, time, body, comments, tags


def parse_soa(text):
    # today.java.net articles: byline and an MM/DD/YYYY line, then the body up
    # to the "end content" comment. Comments are a flat list of <li> blocks.
    title = strip_tags(re.search(r"<title>java\.net:\s*(.*?)</title>", text, re.S).group(1))
    d = re.search(r'by <a href="/pub/au/\d+">[^<]*</a><br\s*/?>\s*(\d{2})/(\d{2})/(\d{4})', text, re.S)
    date = f"{d.group(3)}-{d.group(1)}-{d.group(2)}" if d else None
    # The byline is followed by a table-of-contents block; the body proper
    # starts after it and ends before the spacer rule above the talkback form.
    body = between(
        text,
        r"<!--\s*End TOC\s*-->",
        [r'<div class="pad3x0">', r"<!--\s*end content\s*-->"],
    )
    comments = []
    for block in re.findall(r'<li>\s*<a name="\d+"></a>(.*?)</li>', text, re.S):
        m = re.search(
            r"<b>(.*?)</b><br\s*/?>\s*(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}):\d{2}&nbsp;(\S+)", block, re.S
        )
        if not m:
            continue
        after = block[m.end() :]
        cut = re.search(r"\]\s*(?:</a>)?\s*(?:<br\s*/?>\s*)*", after)
        comments.append(
            {
                "author": strip_tags(m.group(4)),
                "date": m.group(2),
                "time": m.group(3),
                "subject": strip_tags(m.group(1)),
                "body": (after[cut.end() :] if cut else after).strip(),
            }
        )
    return title, date, None, body, comments, []


def parse_j1(text):
    title = strip_tags(re.search(r'<h2 class="title">(.*?)</h2>', text, re.S).group(1))
    d = re.search(r'<span class="date-display-single">.*?(\d{4})-(\d{2})-(\d{2})', text, re.S)
    date = f"{d.group(1)}-{d.group(2)}-{d.group(3)}" if d else None
    # The capture kept the CMS's own unexpanded template tags above the text.
    body = between(
        text,
        r"<cs_comment\s+sidebar ends -->",
        [r'<div class="links">&raquo;', r'<div class="taxonomy">', r'<div id="comment-header">'],
    )
    return title, date, None, body, [], []


PARSERS = {"mt": parse_mt, "drupal": parse_drupal, "soa": parse_soa, "j1": parse_j1}


def main():
    pages = []
    for d in DIRS:
        for path in sorted(d.glob("*.html")):
            text = path.read_text(encoding="utf-8", errors="replace")
            shape = detect(text)
            if shape not in PARSERS:
                pages.append({"file": str(path.relative_to(ROOT)), "shape": shape, "error": "unrecognized template"})
                continue
            title, date, time, body, comments, tags = PARSERS[shape](text)
            pages.append(
                {
                    "file": str(path.relative_to(ROOT)),
                    "shape": shape,
                    "title": title,
                    "date": date,
                    "time": time,
                    "tags": tags,
                    "comment_count": len(comments),
                    "body_chars": len(body or ""),
                    "body": body,
                    "comments": comments,
                }
            )

    if "--table" in sys.argv:
        for p in pages:
            print(
                f"{p['file'].split('/')[-1]:<40} {p['shape']:<7} {str(p.get('date')):<11} "
                f"{str(p.get('time') or ''):<9} c={p.get('comment_count', '?'):<3} "
                f"b={p.get('body_chars', 0):<6} {p.get('title') or p.get('error')}"
            )
    else:
        json.dump(pages, sys.stdout, indent=2, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
