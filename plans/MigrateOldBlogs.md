# Migrating the Old Blogs

Content-migration companion to `RestartBlog.md`. Four sources.

**Three of the four are done, and the fourth is staged.** The blog went live at
`https://blog.walend.net` on 2026-08-25; everything time-boxed by the DNS
cutover finished before it. The java.net recovery is converted and sitting in
`_pending/javanet/`, waiting on David to read it - nothing publishes before
that. Three loose ends still need a network archive; see the end of section 4.

| Source | Count | Status | Phase |
| --- | --- | --- | --- |
| Jekyll `_posts/` (2014-2016) | 10 | Done 2026-08-23 | Phase 5 |
| Hashnode (2024) | 4 | Done 2026-08-23 | Phase 6 |
| Disqus comments (2015) | 6 real | Done 2026-08-24 | Phase 7 |
| java.net via Common Crawl (2003-2009) | 36 pages | Converted 2026-08-26, **staged unread** | Phase 10 |

---

## 1. The 10 Jekyll posts (Phase 5)  [DONE 2026-08-23]

All ten live at `/YYYY/MM/slug/` with 20 redirect stubs. The old Jekyll tree is
deleted; it stays in git history.

| File | Title |
| --- | --- |
| `2014-09-01-back-in.md` | Back From the Break |
| `2014-09-10-graphs-in-scala.md` | Graphs, Now in Scala |
| `2014-10-05-Semirings.md` | Generics and Semirings and Tilting at Windmills |
| `2015-02-28-Enron-Thing.md` | Between People at Enron |
| `2015-06-08-escape-from-inner-trait.md` | Escape to an Inner Object |
| `2015-06-21-Test-With-TypeSafeConfig.md` | Testing With TypeSafe Config |
| `2015-11-03-Rename-to-Disentangle.md` | Renaming to Disentangle |
| `2015-11-10-Easy-Parallel.md` | Parallel Disentangle |
| `2016-05-20-Applying-Typesafe-Config.md` | Just apply(Config) |
| `2016-06-13-Pimping-Config.md` | Implicit Pimp Suspicion |

What it took, kept because the next migration will hit the same things:

1. Moving `_posts/*.md` -> `src/posts/` carried the dates for free - Eleventy
   reads the `YYYY-MM-DD-` filename prefix the same way Jekyll does.
2. Frontmatter was already compatible (`layout`, `title`, `comments`).
3. **Aliases.** Old URLs were `.../YYYY/MM/DD/Name.html`, new ones are
   `/YYYY/MM/slug/`. Both a `.html` and a trailing-slash variant were in
   circulation, so both are emitted - 20 stubs for 10 posts. They are
   meta-refresh + `<link rel="canonical">` stubs, not HTTP 301s; GitHub Pages
   cannot serve real redirects for a static site.
4. **49 code blocks** that Eleventy had been flattening into prose were recovered
   and fenced with languages. This was the expensive part, and it is the reason
   the journal keeps repeating that generated output must be parsed rather than
   read.

### The old github.io origin now redirects  [changed at the cutover]

This section used to warn that `dwalend.github.io/blog/...` was a *different
origin* from `blog.walend.net`, so stubs on the new domain could not help links
pointing at the old one, and that the fix was keeping the github.io site
reachable.

**That is no longer how it behaves, and the outcome is better than the warning
feared.** Setting the custom domain made GitHub serve the old origin as a
redirect to the new one, preserving the path. Verified 2026-08-25:

```
https://dwalend.github.io/blog/2015/11/10/Easy-Parallel.html
  -> 301 https://blog.walend.net/2015/11/10/Easy-Parallel.html
  -> 200 (the alias stub)
  -> the post
```

So an old github.io link lands on the right post through two hops, and no
separate provision is needed for that origin. Nothing to do here; recorded
because the old warning read as a live constraint.

## 2. The 4 Hashnode posts (Phase 6)  [DONE 2026-08-23]

Done before the DNS cutover, which is what made it possible - once
`blog.walend.net` left Hashnode on 2026-08-25 these source URLs stopped
resolving. The text came from the **published** RSS content, not the raw
`_pending` drafts, because the published versions had been edited.

| Published | Title | Hashnode slug |
| --- | --- | --- |
| 2024-03-28 | The New Hire Plan | `the-new-hire-plan` |
| 2024-04-12 | CQRS in a Relational Database via Slick | `cqrs-in-a-relational-database-via-slick` |
| 2024-04-16 | The 20-Minute Limit | `the-20-minute-limit` |
| 2024-04-30 | Bounding Complexity in Scala Projects | `bounding-complexity-in-scala-projects` |

**Source the text from the published RSS, not the `_pending` drafts.** The drafts
were edited before publishing - `_pending/2024-04-27-capping-complexity.md` is
222 lines of raw notes with a different title ("The Principle of Least Power:
Capping Complexity in Scala Projects") and bare URLs where the published version
has real links. The feed is the record of what actually shipped.

Steps:

1. Pull `https://blog.walend.net/rss.xml` (or `https://dwalend.hashnode.dev/rss.xml`,
   which survives the DNS move and is the safer long-term source).
2. Each `<item>` carries the full post body as HTML in `<content:encoded>`, plus
   title, `pubDate`, categories, and `dc:creator`. Nothing is truncated.
3. Convert that HTML back to Markdown. Watch for:
   - `<a target="_blank" href="...">` - drop the `target`.
   - Code blocks - confirm the language tag survives so Prism highlights them.
   - The CQRS post has heavy formatting; check it by eye.
4. Diff the result against the matching `_pending` draft. Where they differ, the
   published version wins, but the draft may hold paragraphs that were cut - worth
   a look before discarding.
5. Set frontmatter: title, `date` from `pubDate`, `comments: true`, tags from the
   `<category>` elements (`Scala`, `Scala-Basics`, ...).
6. **Alias each post to its flat Hashnode slug**, e.g. `/bounding-complexity-in-scala-projects`
   -> `/2024/04/bounding-complexity-in-scala-projects/`. This is what keeps existing
   inbound links and any search-engine results alive across the cutover.
7. Once migrated, the corresponding `_pending` drafts are superseded - move them out
   of the drafts folder so they are not published twice.

Leave the Hashnode blog itself in place, unpublished-to. `dwalend.hashnode.dev`
keeps working as a backstop even after `blog.walend.net` moves.

## 3. The Disqus comments (Phase 7)  [DONE 2026-08-24]

The `intuitivecounter` forum (created 2014-09-02) is still live and still holds
**9 comments**. Three are your own "Test disqus" posts. The remaining six are real,
and five of them form one substantive thread:

- **`2015-06-08-escape-from-inner-trait.md`** - June 2015, a real technical exchange
  with **Alexey Romanov** and **Jörg-Ulrich Wölfel** working through Scala inner
  trait types, including a working answer
  (`val innerThing: BeyondTrait#InnerTrait = bey...`).

That thread is worth more than the comment system it lives in.

How it actually went:

1. **No Disqus export was needed.** The plan said to export from Settings ->
   Export early, because it was "the only copy." It was not - the forum's public
   RSS feed still carried the comments, and that is where they came from. The
   export step was never run.
2. All six real comments live in `src/_data/archivedComments.json` and render as
   static HTML above giscus on `/2015/06/escape-from-inner-trait/`. Importing
   six comments into giscus was never worth it.
3. Commenters are credited by name with their original dates.
4. The forum's other ~25 threads hold 0 posts - duplicates from
   `127.0.0.1:4000` local previews and URL-scheme churn. Nothing else needed
   preserving.
5. The Disqus account can be abandoned. Worth doing deliberately rather than by
   neglect, since the data is now in the repo.

## 4. java.net, recovered from Common Crawl (Phase 10)  [FETCHED 2026-08-25]

**34 blog posts (2003-2009) in `_archive-src/javanet/`, plus 2 java.net articles
in `_archive-src/javanet-articles/`.** All from Common Crawl; the wayback machine
was never used.

### The articles were not blog posts

`today.java.net/pub/a/...` was a different site from `weblogs.java.net/blog/dwalend`,
which is why searching the blog archive never found them. This plan said
"article" and it was read as "blog post."

- **`2006-04-04-understanding-service-oriented-architecture.html`** - 62KB, the
  one the retrospective is for. Opens by going after the hype: *"By 2008, SOA will
  provide the basis for 80 percent of development projects." At JavaOne 2005, 82
  of the 168 technical session PDFs contained "SOA."*
- **`2008-05-08-jmx-for-unit-tests-in-tdd.html`** - a JavaOne 2008 session
  abstract, complete as captured but short. David expected only one article;
  there were two.

Found via the author page `today.java.net/pub/au/95`, which is linked from the
SOA article and lists everything he wrote there. **That is the trick worth
remembering**: an author page enumerates what a URL-pattern search cannot guess.

The URL itself came from a javawhat.com directory entry David found - a page with
no content on it, but with the exact link. A dead end that was not one.

| Year | Posts |
| --- | --- |
| 2003 | 4 |
| 2004 | 6 |
| 2005 | 5 |
| 2006 | 8 |
| 2007 | 4 |
| 2008 | 3 |
| 2009 | 1 |

### Why Common Crawl instead

`web.archive.org` refused every connection for a full day on 2026-08-25 - from
two machines, over ~75-second timeouts - while `archive.org` itself stayed up.
See the journal. Rather than wait it out, the question became which *other*
archive holds this material.

Checked: `arquivo.pt` (reachable, has nothing - it is a Portuguese national
archive), `archive.today` (reachable), `web.archive.org.bibalex.org` (down),
**Common Crawl (reachable, and has it)**.

Common Crawl's two oldest indexes, `CC-MAIN-2008-2009` and `CC-MAIN-2009-2010`,
cover the tail of the java.net run - but they hold snapshots of the *whole*
archive, back to 2003, because the blog's own monthly `/archive/` pages were
still linked when the crawler came through. That is the lucky part and it is
worth understanding: the crawl date bounds when the crawler visited, not how old
the content is.

### How it works

`bin/fetch-javanet-cc.py` queries both indexes, keeps the largest capture per
URL, does a ranged read against `data.commoncrawl.org`, unzips the ARC record,
and writes the HTTP body. Resumable; existing files are skipped.

```sh
bin/fetch-javanet-cc.py --list    # inventory only
bin/fetch-javanet-cc.py           # fetch what is missing
```

`bin/fetch-javanet.sh` (the wayback version) is kept. Common Crawl only has what
Common Crawl crawled; if the wayback machine comes back it is worth re-running to
see whether it holds anything Common Crawl missed. The plan's original figure was
~37 article pages against the 33 recovered here.

Two filter traps, both hit and both fixed - **articles live under `/archive/`**,
so excluding that path drops everything, and **`/YYYY/MM/index.html` matches the
article pattern** but is a monthly listing, not a post. Excluding those took the
count from 58 to 33.

### The SOA retrospective

The plan wanted "an especially good article on service-oriented architecture."
It is **`2004-01-coupling_in_sof.html`, "Coupling in Software Architecture"** -
a coupling spectrum running from dissociated ubiquitous services assembled by
discovery (UDDI, topic-based messaging) through known services assembled at run
time by configuration.

Note the date: January 2004. That makes it a **22-year** retrospective, not the
20 this plan has said since it was written.

The category index at `archive/web_services_and_xml/index.html` is **not** in
Common Crawl - no captures. If that grouping matters for the retrospective it
needs the wayback machine, or reconstructing from the posts themselves.

### The "7 known-missing posts" were never his  [CORRECTED 2026-08-30]

This section used to list seven slugs as posts linked from the monthly archive
pages with no Common Crawl capture, needing the wayback machine.

**All seven are other people's blogs.** They are outbound links David made, and
the scraper that built the list matched `weblogs.java.net/blog/*/archive/...`
without pinning the author to `dwalend`:

| Slug | Actually on |
| --- | --- |
| `2004-09-evolving_the_ja` | `/blog/kgh/` - Graham Hamilton |
| `2005-06-generics_consid_1` | `/blog/arnold/` - Ken Arnold, the "generics are a mistake" post |
| `2005-08-pumping_up_java` | `/blog/kohsuke/` - Kohsuke Kawaguchi |
| `2006-01-the_nonpublic_c` | `/blog/robogeek/` - David Herron |
| `2006-05-a_java_perspect` | `/blog/jonbruce/` |
| `2007-04-reserve_seats_a` | `/blog/webmink/` - Simon Phipps |
| `2008-06-tests_first_or` | `/blog/johnsmart/` - John Ferguson Smart |

One grep against the recovered HTML settles it, and it should have been run
before the slugs were written down as missing. **A URL pattern that omits the
part identifying the author will happily match every author.** Same family as
the `/YYYY/MM/index.html` trap and the `foo_1.html` duplicate-slug trap: a
pattern matching more than intended, producing a plausible number.

Note which direction this one goes. The earlier two *inflated* the count and
flattered the work; this one *invented a deficit* and made the recovery look
less complete than it was. Both survived because nobody checked, which is the
only thing the three have in common that matters.

**So there is no known-missing set.** 34 blog posts and 2 articles is the whole
of what the crawled index pages point to under `/blog/dwalend/`.

**That is still a floor, not a ceiling.** It is only what the crawled monthly
index pages happened to link; months whose index page was never crawled
contribute nothing at all. "All of them" remains a claim this recovery cannot
support - but the support for it is stronger than this plan has been saying.

### `bin/fetch-javanet-cc.py` is UNTESTED as it currently stands

The version that produced the 34 posts on disk queried only two indexes and knew
nothing about the articles - so it would **not** reproduce the current state from
a clean checkout. It was rewritten on 2026-08-25 to query all ~42 indexes from
java.net's lifetime, dedupe by `<title>` rather than by slug, and enumerate the
articles from the author page.

**That rewrite parses but has never been run end to end.** Verify it before
trusting it. A full run re-queries ~42 indexes across several URL patterns and
takes minutes, so start with `--list`.

The authoritative artifact is the recovered HTML in `_archive-src/`, not the
script. If the script disagrees with what is on disk, the disk is right.

### Two traps that cost real errors here

1. **Count titles, not slugs.** Movable Type emitted two URLs per post
   (`foo.html` and `foo_1.html`). Ten slugs that were "missing from disk" turned
   out to be nine duplicates and one genuine post. A slug you do not have is not
   the same as a post you do not have.
2. **`/YYYY/MM/index.html` matches the article pattern** but is a monthly
   listing. Including them inflated the count from 33 to 58.

Both produce a plausible larger number, which is exactly why they survive a
glance. **A count is not a check.**

### The conversion  [DONE 2026-08-25, staged unpublished]

All 36 pages are converted and staged in **`_pending/javanet/`** - out of the
Eleventy build, awaiting David's review before anything is published. Two
scripts do it, and both have been run end to end:

```sh
bin/javanet-extract.py --table                      # inventory: shape, date, title, counts
bin/javanet-extract.py | bin/javanet-to-markdown.py _pending/javanet
```

`javanet-extract.py` parses HTML to JSON; `javanet-to-markdown.py` turns that
JSON into Markdown plus `javanetComments.json`. The split matters: the
inventory is readable on its own, which is how the template surprises below
got caught.

**Five template shapes, not two.** The plan expected the articles to differ
from the posts. In fact the blog itself has three shapes, because java.net
moved it from Movable Type to Drupal in 2008 and kept the archive URLs, then
re-themed Drupal at least once. *Which shape a page has depends on when the
crawler visited, not on when the post was written* - the same fact that made a
2008 crawl yield 2003 posts. 20 pages are Movable Type, 14 Drupal (two themes),
plus one shape for each article.

**Dates: all 36 recovered, to the minute.** Both blog templates carry a full
"Posted by dwalend on October 06, 2003 at 04:57 AM"; the articles carry
`04/04/2006` and `Thu, 2008-05-08`. Every result was read against its page.

**Comments: 189, from 83 people**, 62 of them David's own replies. Kept as
static HTML in the shape `src/_data/archivedComments.json` already uses, keyed
by the new `/archive/...` URL - the same treatment as the six Disqus comments
in section 3.

### Presentation: `/archive/`, out of the feed, unpublished until reviewed

- URLs are `/archive/YYYY/MM/slug/`, set by an explicit `permalink`.
- No `tags: post`, so they stay out of the index and the RSS feed even after
  they move into `src/`.
- Front matter carries `archived: true` and `originalUrl:`, for a standing
  header noting the original date and source. **The header and the layout
  support for `archived` are not written yet.**
- They live in `_pending/javanet/` until David has read them.

### Three things the conversion turned up

1. **The original pages ate their own generics.** `<Elem>`, `<Node>`, `<Key>`
   and friends were written bare in prose, so browsers silently dropped them -
   readers in 2004 saw "I changed the Bag interface to Bag extending
   Collection." They are restored as escaped text. Note the second trap here:
   several *are* correctly escaped in the source, and a naive
   `html.unescape` turns those back into raw brackets that markdown-it then
   swallows. Escaping happens after every real tag is gone.
2. **Four content images are dead** and were never fetched -
   `bloggers.dev.java.net` is gone. Two source-directory diagrams in "Design
   for Reuse", two GraphViz class diagrams in "GraphViz Class Diagrams".
   **Decision 2026-08-26: recover them, do not cut them and add a note.** All
   four are reproducible from the posts if no archive has them - a directory
   tree and a GraphViz class diagram can both be redrawn. `bin/javanet-fetch-images.py`
   tries the wayback machine, then Common Crawl, and writes to `src/img/archive/`.
   The Markdown keeps the image references either way.
3. **Two dead embeds**, replaced with an italic note: the ZoomApplet in
   "Affine Frustration Transformed" and the JavaFX minesweeper launcher in
   "Event Based Programming in JavaFX".

### The comment gap - 12 posts, and why the fetch script may be at fault

**12 of the 36 pages carry zero comments, and that is probably not true.**
All 12 are Drupal-shape captures of pre-2008 posts. The Drupal-shape captures
that *do* have comments are the late ones (2008-07, 2009-07). The likely
reading is that the Movable Type -> Drupal migration dropped the older threads.

But there is a second possible cause, and it is ours: **`fetch-javanet-cc.py`
keeps the largest capture per URL**, and a bulky comment-free Drupal page can
outweigh a lean Movable Type page that still has the thread. If so, the
comments were in Common Crawl all along and the fetch threw them away.

`bin/javanet-recheck-comments.py` tests exactly this - for those 12 URLs it
fetches *every* capture rather than the biggest, counts comment blocks in each,
and writes any better one as `SLUG.mt.html` beside the existing file rather
than over it.

**Second run, 2026-08-30: the theory was right.** `coupling_in_sof` - the
retrospective's own subject - has **25 captures in Common Crawl, and the
Movable Type one carries 3 comments**: `ljnelson` twice and `ceperez`, January
2004. The bodies of the two captures are identical to the character. The only
difference is that the comment-free Drupal page is bulkier, so "keep the
largest" discarded the thread. Recovered as
`_archive-src/javanet/2004-01-coupling_in_sof.mt.html`.

That makes 192 comments across 24 posts.

**The two captures each kept something the other dropped** - Movable Type the
comments, Drupal the `Programming` topic tag - so `javanet-extract.py` now
folds `SLUG.mt.html` into `SLUG.html` and takes the best of each field rather
than picking a winner. Repeating the original mistake one level up would have
been an easy thing to do here.

**The run is only half done.** The 1s sleep was not enough; throttling returned
partway through and the last five URLs report `44/44 indexes UNREACHABLE`:

| Verdict | Posts |
| --- | --- |
| Genuinely no comments - 24 captures, clean run | `graphviz_class` |
| Probably none | `design_for_reus`, `reviewing_the_j`, `somnifugijms_fo_4`, `no_giant_or_win_1` |
| Weak - 23/44 indexes unreachable | `brilliant_appro` |
| **No data at all** | `our_grass_is_gr`, `whooshing_sound_1`, `bad_things_in_a`, `wild_winds_wres_1`, `jmx_and_testdri_1` |

Those five need another pass after a longer cooldown, with a bigger sleep.
`coupling_in_sof` is the argument for bothering.

**First run, 2026-08-26: inconclusive, and it took a fix to see that.** One
real result came back - `design_for_reus` has 4 captures and none of them carry
comments, so for that post the threads are genuinely gone. Then
`index.commoncrawl.org` stopped answering entirely (connection refused, not a
timeout), almost certainly a rate limit earned by querying 44 indexes for 12
URLs back to back. The script swallowed those failures and printed `0 captures`
for every remaining post, which reads exactly like a finding.

It now counts unreachable indexes separately, says so in its output, and sleeps
between queries. **An archive that will not answer is not an archive that has
nothing** - the second half of that sentence is what the first version wrote to
the log. Re-run after a cooldown.

The 12: `design_for_reus`, `reviewing_the_j`, **`coupling_in_sof`** (the
retrospective's own subject), `somnifugijms_fo_4`, `graphviz_class`,
`no_giant_or_win_1`, `brilliant_appro`, `our_grass_is_gr`, `whooshing_sound_1`,
`bad_things_in_a`, `wild_winds_wres_1`, `jmx_and_testdri_1`.

### Still to do

1. **David reads the 36 staged posts.** Nothing publishes before that.
2. **Layout support for `archived`** - the standing header, and keeping the
   archive out of the feed and sitemap.
3. **Wire `javanetComments.json` in** the way `archivedComments.json` is wired.
4. **Re-run `bin/javanet-recheck-comments.py`** for the five posts that got no
   data at all, after a longer cooldown and with a bigger sleep.
5. **Recover the four dead images** (`bin/javanet-fetch-images.py`). There is
   no seventh-post problem - see the correction above.
6. **Then write the retrospective** as a *new* post linking into the recovered
   material. That is the goal; the recovery serves it.

### Archive availability, 2026-08-30

**Common Crawl is back.** `index.commoncrawl.org/collinfo.json` answers 200 in
0.19s, four days after refusing connections. The recheck and image runs were
started against it; results below.

**`web.archive.org` is still down for us** - `/cdx/search/cdx` timed out at 30s
on 2026-08-30, as it has since 2026-08-25. Six days. `archive.org` is fine; it
is specifically the capture service. Nothing outstanding needs it any more now
that the seven "missing posts" turn out to be other people's.

The state it was in on 2026-08-26, kept because the endpoint trap is worth
remembering:

- **`web.archive.org` is still down for us** - `/cdx/search/cdx` times out at
  40s, as it did all of 2026-08-25. Note the trap: `archive.org/wayback/available`
  answers 200 in 1.3s, and that is a *different host*. Checking the wrong
  endpoint says wayback is back when it is not.
- **`index.commoncrawl.org` refuses connections** as of the recheck run above.
  `data.commoncrawl.org` was not retested.

**2026-08-30: the images are not in the wayback machine, and this time that is
a real answer.** The host is there and so are its neighbours - a CDX query for
`bloggers.dev.java.net/files/documents/84*` returns other people's images - but
**every one of them is a 301, 302 or 404, never a 200.** java.net's file server
redirected crawlers instead of serving bytes. A query for each of the four
returns `[]`: no captures at all.

Common Crawl was rate-limited from the comment recheck and refused connections
throughout, so it is still untested for the images. That is the one remaining
place to look. After that, redraw them - a directory tree and a GraphViz class
diagram are both reproducible from the posts, which is why the decision was to
keep the references rather than cut them.

Nothing that needs a network archive can proceed until one of them returns.
Everything staged in `_pending/javanet/` is already local and unaffected.

## 4b. Note for whichever post covers disentangleParGraphs

When that post gets brought up to speed, add a footnote crediting **d3 3.5.6** and
**queue.js** as Mike Bostock's, BSD-3-Clause. The vendored copies in
`disentangleParGraphs/js/` had their copyright headers stripped; Phase 1 restores
them in the JavaScript itself, and the post should say so in prose too.

## 5. private-duck-aligner blog-fodder (Phase 10+)

Not a migration - a backlog. Mine it for post ideas once the publishing habit is
re-established. Out of scope for the restart.

## 6. The drafts in `_pending/`

Staying drafts, per decision. Out of the build, in the repo. Thirteen files as of
2026-08-25:

`2014-09-02-blog-setup.md`, `2014-09-05-custom-collection.md`,
`2015-03-31-Progression.md`, `2015-06-01-Java-Pedantic.md`,
`2016-05-13-welcome-to-jekyll.markdown`, `2024-02-27-back-again.md`,
`2024-03-21-Daily-Loop.md`, `2024-04-26-horses.md`,
`2026-08-30-kill-at-thirty-percent.md`, `you-shouldnt-be-able-to.md`,
`remotely.md`, `blog_ideas.txt`, `NEScalaSymposiumDay1.txt`

Two are newer than this plan and are **not** part of the migration -
`2026-08-30-kill-at-thirty-percent.md` and `you-shouldnt-be-able-to.md` are new
writing, and `2026-08-30` is a future date of the same kind the centaur post
used. Eleventy builds future-dated posts without complaint, so a date is not a
guard; moving the file into `src/posts/` is what publishes it.

`2016-05-13-welcome-to-jekyll.markdown` is the stock Jekyll sample post and can
just be deleted.

The four drafts that corresponded to published Hashnode posts
(`2024-03-01-first-day-plan.md`, `2024-03-20-20-minute-limit.md`,
`2024-04-27-capping-complexity.md`, `CQRSWithRDMS.md`) were superseded by
section 2 and deleted; they stay in git history.
