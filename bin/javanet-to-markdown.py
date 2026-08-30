#!/usr/bin/env python3
"""Convert the recovered java.net HTML into Markdown posts.

Reads the inventory that bin/javanet-extract.py produces and writes one
Markdown file per page, plus a JSON file of the comments keyed by post URL in
the shape src/_data/archivedComments.json already uses.

Usage:
  bin/javanet-extract.py | bin/javanet-to-markdown.py OUTDIR
"""

import html
import json
import re
import sys
from pathlib import Path

# The blog ran on Movable Type at this path; the Drupal era kept the same URLs.
BLOG_URL = "http://weblogs.java.net/blog/dwalend/archive/{year}/{month}/{slug}.html"
ARTICLE_URL = "http://today.java.net/pub/a/today/{year}/{month}/{day}/{slug}.html"


def slugify(title):
    s = re.sub(r"[^\w\s-]", "", title.lower())
    return re.sub(r"-+", "-", re.sub(r"[\s_]+", "-", s)).strip("-")


def code_language(source):
    """Guess a fence language. Everything here is Java unless it says otherwise."""
    s = source.strip()
    if s.startswith("<?xml") or re.match(r"<(project|beans|configuration|\w+:)", s):
        return "xml"
    if re.search(r"^\s*[\$>]\s|\bant\b\s+\w|^\s*java\s+-", s[:200]):
        return "sh"
    # The 2009 JavaFX Script blocks get no language: Prism has no grammar for
    # it, and labelling them "js" would highlight the wrong keywords.
    if re.search(r"\b(var|def)\s+\w+\s*:", s) and "public class" not in s:
        return ""
    return "java"


# Tag names the recovered pages actually use. Anything else inside angle
# brackets is prose the original author never escaped - almost always a Java
# type parameter like <Elem>. The 2003-era browsers silently dropped those, so
# restoring them is a repair, not a change.
HTML_TAGS = {
    "a", "abbr", "applet", "b", "big", "blockquote", "br", "center", "cite", "code",
    "dd", "div", "dl", "dt", "em", "embed", "font", "form", "h1", "h2", "h3", "h4",
    "h5", "h6", "hr", "i", "iframe", "img", "input", "li", "link", "meta", "nobr",
    "object", "ol", "p", "param", "pre", "q", "s", "script", "small", "span",
    "strike", "strong", "style", "sub", "sup", "table", "tbody", "td", "th", "tr",
    "tt", "u", "ul",
}
LT, GT = "\x01", "\x02"


def guard_pseudo_tags(s):
    def repl(m):
        if m.group(2).lower() in HTML_TAGS:
            return m.group(0)
        return LT + m.group(1) + m.group(2) + m.group(3) + GT

    return re.sub(r"<(/?)([A-Za-z][\w.:-]*)((?:\s[^>]*)?)>", repl, s)


def untag(s):
    return re.sub(r"<[^>]+>", "", s)


def inline(s):
    """Inline HTML -> Markdown. Runs after block structure is resolved."""
    s = guard_pseudo_tags(s)
    s = re.sub(r"<a\b[^>]*?href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", r"[\2](\1)", s, flags=re.S | re.I)
    s = re.sub(r"<img\b[^>]*?src=[\"']([^\"']+)[\"'][^>]*?alt=[\"']([^\"']*)[\"'][^>]*>", r"![\2](\1)", s, flags=re.I)
    s = re.sub(r"<img\b[^>]*?src=[\"']([^\"']+)[\"'][^>]*>", r"![](\1)", s, flags=re.I)
    s = re.sub(r"</?(b|strong)>", "**", s, flags=re.I)
    s = re.sub(r"</?(i|em)>", "*", s, flags=re.I)
    s = re.sub(r"<code>(.*?)</code>", lambda m: "`" + untag(m.group(1)).strip() + "`", s, flags=re.S | re.I)
    s = re.sub(r"<br\s*/?>", "  \n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    # Every real tag is gone by now, so any angle bracket left is prose - a Java
    # type parameter like <Elem>, which markdown-it would otherwise swallow as
    # an unknown HTML tag. That includes the ones the source escaped correctly
    # and html.unescape just turned back into raw brackets.
    s = s.replace("<", "&lt;").replace(">", "&gt;")
    s = s.replace(LT, "&lt;").replace(GT, "&gt;")
    # Collapse the runs of spaces the old templates left behind, but keep the
    # two-space line breaks Markdown needs.
    s = re.sub(r"[ \t]{3,}", " ", s)
    return s.strip()


def convert(body):
    """Block-level HTML -> Markdown. Code blocks are pulled out first so no
    inline rule can touch the generics inside them."""
    blocks = []

    def stash(m):
        raw = m.group(0)
        inner = re.search(r"<pre[^>]*>(.*?)</pre>", raw, re.S | re.I).group(1)
        inner = re.sub(r"</?code[^>]*>", "", inner, flags=re.I)
        inner = re.sub(r"<br\s*/?>", "\n", inner, flags=re.I)
        inner = untag(inner)
        inner = html.unescape(inner).replace("\xa0", " ").strip("\n")
        inner = "\n".join(line.rstrip() for line in inner.split("\n"))
        blocks.append(f"```{code_language(inner)}\n{inner}\n```")
        return f"\x00{len(blocks) - 1}\x00"

    # <code><pre> (Movable Type), <pre><code> (Drupal), and in a few captures
    # <pre><code><pre> all wrap the same thing. Flatten to a single <pre> so one
    # rule catches them all - otherwise the inner block gets stashed first and
    # the outer one fences its own placeholder.
    body = re.sub(r"(?:<(?:pre|code)[^>]*>\s*){2,}", "<pre>", body, flags=re.I)
    body = re.sub(r"(?:</(?:pre|code)>\s*){2,}", "</pre>", body, flags=re.I)
    body = re.sub(r"<pre[^>]*>.*?</pre>", stash, body, flags=re.S | re.I)

    # <quote> is this blog's own tag for a pull quote; it is not HTML.
    body = re.sub(r"<quote>(.*?)</quote>", lambda m: "\n\n> " + inline(m.group(1)).replace("\n", "\n> ") + "\n\n", body, flags=re.S | re.I)
    body = re.sub(r"<blockquote>(.*?)</blockquote>", lambda m: "\n\n> " + inline(m.group(1)).replace("\n", "\n> ") + "\n\n", body, flags=re.S | re.I)

    # Dead embeds. The applet and the JavaFX launcher cannot run anywhere now.
    body = re.sub(r"<applet\b.*?</applet>", "\n\n*[Java applet, no longer runnable]*\n\n", body, flags=re.S | re.I)
    body = re.sub(r"<script\b.*?</script>", "\n\n*[JavaFX applet, no longer runnable]*\n\n", body, flags=re.S | re.I)
    body = re.sub(r"<cs(include|field|_comment)\b[^>]*>", "", body, flags=re.I)

    body = re.sub(r"<h([1-6])[^>]*>(.*?)</h\1>", lambda m: f"\n\n{'#' * max(2, int(m.group(1)))} {inline(m.group(2))}\n\n", body, flags=re.S | re.I)
    body = re.sub(r"<li[^>]*>(.*?)</li>", lambda m: f"\n- {inline(m.group(1))}", body, flags=re.S | re.I)
    body = re.sub(r"</?(ul|ol)[^>]*>", "\n\n", body, flags=re.I)

    # These pages use a bare <p> as a separator far more often than as a
    # container, so split on every <p> or </p> and treat the pieces as blocks.
    parts = [inline(part) for part in re.split(r"</?p[^>]*>", body, flags=re.I)]
    md = "\n\n".join(p for p in parts if p)
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = re.sub(r"\x00(\d+)\x00", lambda m: "\n\n" + blocks[int(m.group(1))] + "\n\n", md)
    return re.sub(r"\n{3,}", "\n\n", md).strip() + "\n"


def main():
    outdir = Path(sys.argv[1])
    outdir.mkdir(parents=True, exist_ok=True)
    pages = json.load(sys.stdin)
    comments = {}
    for p in pages:
        name = Path(p["file"]).name
        slug = slugify(p["title"])
        date = p["date"]
        year, month, _ = date.split("-")
        article = "javanet-articles" in p["file"]
        if article:
            original = ARTICLE_URL.format(year=year, month=month, day=date.split("-")[2], slug=name[11:-5])
        else:
            original = BLOG_URL.format(year=year, month=month, slug=name[8:-5])

        url = f"/archive/{year}/{month}/{slug}/"
        # No `tags: post`, so these stay out of the index and the feed even once
        # they move into src/. The permalink is explicit because they will not
        # live under src/posts/, which is where the /YYYY/MM/ rule comes from.
        front = [
            "---",
            "layout: post",
            f"title: {json.dumps(p['title'])}",
            f"date: {date}",
            f"permalink: {url}",
            "archived: true",
            f"originalUrl: {original}",
        ]
        if p["tags"]:
            front.append("javanetTopics:")
            front += [f"  - {t}" for t in p["tags"]]
        front.append("---")

        (outdir / f"{date}-{slug}.md").write_text(
            "\n".join(front) + "\n\n" + convert(p["body"]), encoding="utf-8"
        )

        if p["comments"]:
            comments[url] = [
                {
                    "author": c["author"],
                    "date": c["date"],
                    **({"subject": c["subject"]} if c.get("subject") else {}),
                    "body": convert(c["body"]),
                }
                for c in p["comments"]
            ]

    (outdir / "javanetComments.json").write_text(
        json.dumps(comments, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"wrote {len(pages)} posts and comments for {len(comments)} of them to {outdir}", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
