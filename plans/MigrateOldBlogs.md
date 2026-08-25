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

## 4. java.net via the wayback machine (Phase 10)  [OUTSTANDING]

**The only migration left**, and the only one that was never time-boxed by the
cutover.

The old `weblogs.java.net/blog/dwalend/` blog is recoverable. A CDX query was
reported to return **84 archived URLs, of which ~37 are article pages**, spanning
**2003 through 2009**.

**The wayback machine was unreachable on 2026-08-25 - from archive.org's side.**
`web.archive.org` refused connections on both 80 and 443, from two different
machines, over ~75-second timeouts.

The first read of this was wrong. Seeing `archive.org` work while
`web.archive.org` failed, it looked like an egress policy on the agent's sandbox.
Running the same script from the laptop produced the identical failure, which
ruled that out. What it actually is:

- One A record, `207.241.237.3`, from every public resolver. No AAAA, so no
  IPv6-first stall.
- Connecting straight to that IP with SNI fails the same way, so nothing local is
  intercepting.
- `archive.org` lives on `207.241.224.2` - a different range - which is why one
  host answers and the other does not.
- The `wayback/available` API on `archive.org`, which answered normally twenty
  minutes earlier, started returning **`429 Too Many Requests`**.

A host refusing every connection while its sibling sheds load with 429s is the
archive under strain. Transient, most likely. **Retry later rather than
debugging the network** - and back off rather than hammering, since something
over there is already rate-limiting.

`bin/fetch-javanet.sh` is resumable precisely for this: re-running after a
failure re-queries CDX only if `cdx.txt` is missing, and skips every article
already on disk.

What could be confirmed, via the availability API on the reachable `archive.org`
host, is that **the material is still there**:

```sh
curl -s "https://archive.org/wayback/available?url=weblogs.java.net/blog/dwalend/"
# -> closest snapshot 20090531085525, status 200, available true
```

The CDX endpoint is not mirrored on that host (404), so the **84 archived URLs /
~37 article pages** figures remain as-recorded rather than as-confirmed. A CDX
timeout means try again; it does not mean anything is lost.

**`bin/fetch-javanet.sh` does the network half** - CDX query, filter to article
pages, fetch each with the `id_` suffix, write raw HTML into
`_archive-src/javanet/`. It is resumable, so an interrupted run costs nothing,
and it sleeps a second between fetches. Run it from a machine that can reach the
archive:

```sh
bin/fetch-javanet.sh --list    # show what would be fetched, no downloads
bin/fetch-javanet.sh           # fetch what is missing
```

Everything after that - HTML to Markdown, frontmatter, presentation - can be done
here from the local files.

One trap already found and fixed in that script: Movable Type puts articles under
`/archive/`, so filtering that path out drops **every** article. The
`YYYY/MM/slug.html` date pattern is what separates articles from the category
listings; nothing else needs excluding but `index.html` and the `%23comments`
artifacts.

**`_archive-src/` gets committed** (decided 2026-08-25). The wayback copy is the
only copy, and 20-year-old bytes are worth having twice. It is not in
`.gitignore`, so the fetched HTML lands in the working tree ready to commit -
that is deliberate, not an oversight.

Sample of what is there:

- `2003/09/defending_autob.html`, `design_for_reus.html`, `somnifugijms_fo_6.html`
- `2003/10/design_for_exce.html`, `reviewing_the_j.html`
- `2004/01/coupling_in_sof.html`, `2004/07/test_driving_ge.html`,
  `2004/08/moving_jdigraph.html`, `2004/12/naming_generic.html`
- `2005/03/better_javadoc.html`, `2005/08/graphviz_class.html`
- `2006/05/tilting_at_the_1.html`, `2006/12/pronouns_in_com.html`
- `2007/05/preparing_for_j.html`, `2007/06/salutafugijms_j_1.html`

There is also a category index at `archive/web_services_and_xml/index.html` -
**that is the thread to pull for the service-oriented-architecture retrospective.**

Steps:

1. Run the CDX query, filter to `statuscode:200`, drop `/index.html` archive pages
   and the `%23comments` artifacts.
2. For each article, fetch `http://web.archive.org/web/<timestamp>id_/<url>` - the
   `id_` suffix returns the original bytes without the wayback toolbar injection.
3. Convert the 2003-era HTML to Markdown. Expect Movable Type markup, old entities,
   and dead outbound links.
4. Decide presentation. Suggestion: publish under an `/archive/` prefix with a
   standing header noting the original date and source, rather than backdating them
   into the main feed - the feed should not suddenly emit 37 items from 2003.
5. Tag them so they are browsable but do not dominate the front page.
6. Then write the **SOA 20-year retrospective** as a *new* post that links back into
   the recovered `web_services_and_xml` material. That is the actual goal; the
   recovery is in service of it.

Timing note: these have survived in the archive for 20 years and are not at
immediate risk, but `weblogs.java.net` itself is long gone, so the wayback copy is
the only copy.

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
