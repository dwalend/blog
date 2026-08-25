# Migrating the Old Blogs

Content-migration companion to `RestartBlog.md`. Four sources.

**Three of the four are done.** The blog went live at `https://blog.walend.net`
on 2026-08-25; everything time-boxed by the DNS cutover finished before it. Only
the java.net recovery is left, and it was never urgent.

| Source | Count | Status | Phase |
| --- | --- | --- | --- |
| Jekyll `_posts/` (2014-2016) | 10 | Done 2026-08-23 | Phase 5 |
| Hashnode (2024) | 4 | Done 2026-08-23 | Phase 6 |
| Disqus comments (2015) | 6 real | Done 2026-08-24 | Phase 7 |
| java.net via wayback (2003-2009) | ~37 pages | **Outstanding** | Phase 10 |

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

### Still to do

1. Convert the 33 HTML files to Markdown. Expect Movable Type markup, old
   entities, and dead outbound links.
2. Recover per-post dates. The filenames give `YYYY-MM`; the exact day is in the
   HTML as "Posted by dwalend on September 18, 2003 at 05:14 AM" but in more than
   one template shape across six years, so it needs a real parser rather than one
   regex.
3. **Decide about comments.** Several posts carry substantial threads - "Design
   For Exceptions" has 25, "Naming Generic Types" 16, "What Giants?" 14, "Better
   JavaDoc" 13. That is a real archive, the same judgement as the 2015 Disqus
   thread in section 3, and it is in the recovered HTML already.
4. Decide presentation - an `/archive/` prefix with a standing header rather than
   backdating 33 items into the main feed.
5. Then write the retrospective as a *new* post linking back into it. That is the
   actual goal; the recovery is in service of it.

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
