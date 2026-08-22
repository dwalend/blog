# Migrating the Old Blogs

Content-migration companion to `RestartBlog.md`. Four sources, in descending
order of urgency.

| Source | Count | Urgency | Phase |
| --- | --- | --- | --- |
| Jekyll `_posts/` (2014-2016) | 10 | Already in the repo | Phase 5 |
| Hashnode (2024) | 4 | **Before DNS cutover** | Phase 6 |
| Disqus comments (2015) | 6 real | Before Disqus rots further | Phase 7 |
| java.net via wayback (2003-2009) | ~37 pages | After launch | Phase 10 |

---

## 1. The 10 Jekyll posts (Phase 5)

Already in `_posts/` with Jekyll frontmatter. Low risk - mostly a move plus an alias.

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

Steps:

1. Move `_posts/*.md` -> `src/posts/`. Eleventy reads the `YYYY-MM-DD-` filename
   prefix for the date the same way Jekyll does, so dates carry over for free.
2. Frontmatter is already compatible (`layout`, `title`, `comments`). `layout: post`
   resolves to `src/_includes/post.liquid`.
3. **Aliases.** Old URLs were `https://dwalend.github.io/blog/YYYY/MM/DD/Name.html`.
   New URLs are `https://blog.walend.net/YYYY/MM/slug/`. Generate a redirect stub
   per old path. Both a `.html` and a trailing-slash variant were in circulation
   (the Disqus thread list shows both `/Easy-Parallel.html` and `/Easy-Parallel/`),
   so emit both.
   - These are meta-refresh + `<link rel="canonical">` stubs, not HTTP 301s.
     GitHub Pages cannot serve real redirects on a static site.
   - Note the old host was `dwalend.github.io/blog/...`, a *different origin* from
     `blog.walend.net`. Stubs on the new domain only help links that already point
     at the new domain. Keeping the repo's Pages site reachable at
     `dwalend.github.io/blog/` preserves the rest.
4. Check the body of each for Jekyll-isms: `{% highlight scala %}` blocks need to
   become fenced ```` ```scala ```` blocks for the syntax-highlight plugin, and
   `{{ site.baseurl }}` references need updating.
5. Spot-check internal cross-links between posts - several reference each other.

## 2. The 4 Hashnode posts (Phase 6)

**Do this before the DNS cutover.** Once `blog.walend.net` leaves Hashnode these
URLs stop resolving.

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

## 3. The Disqus comments (Phase 7)

The `intuitivecounter` forum (created 2014-09-02) is still live and still holds
**9 comments**. Three are your own "Test disqus" posts. The remaining six are real,
and five of them form one substantive thread:

- **`2015-06-08-escape-from-inner-trait.md`** - June 2015, a real technical exchange
  with **Alexey Romanov** and **Jörg-Ulrich Wölfel** working through Scala inner
  trait types, including a working answer
  (`val innerThing: BeyondTrait#InnerTrait = bey...`).

That thread is worth more than the comment system it lives in.

Steps:

1. Export from Disqus admin: Settings -> Export. It emails a WXR/XML archive.
   Do this early - it is the only copy.
2. Because it is six comments on one post, **do not** try to import them into
   giscus. Render them as static HTML at the foot of that one post: name, date,
   body, in a `<section class="archived-comments">`.
3. Credit the commenters by name and keep their original dates.
4. Note the forum has ~25 threads but 0 posts on all of them except this one -
   many are duplicates from `127.0.0.1:4000` local previews and from URL-scheme
   churn. Nothing else needs preserving.
5. After export, the Disqus account can be abandoned.

## 4. java.net via the wayback machine (Phase 10)

The old `weblogs.java.net/blog/dwalend/` blog is recoverable. A CDX query returns
**84 archived URLs, of which ~37 are article pages**, spanning **2003 through 2009**.

```
http://web.archive.org/cdx/search/cdx?url=weblogs.java.net/blog/dwalend*&output=text&fl=original,timestamp,statuscode&collapse=urlkey&filter=statuscode:200
```

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

## 6. The 2014-2024 drafts

Staying drafts, per decision. Keep them out of the build but in the repo:

`2014-09-02-blog-setup.md`, `2014-09-05-custom-collection.md`,
`2015-03-31-Progression.md`, `2015-06-01-Java-Pedantic.md`,
`2016-05-13-welcome-to-jekyll.markdown`, `2024-02-27-back-again.md`,
`2024-03-21-Daily-Loop.md`, `2024-04-26-horses.md`, `remotely.md`,
`blog_ideas.txt`, `NEScalaSymposiumDay1.txt`

Note `2016-05-13-welcome-to-jekyll.markdown` is the stock Jekyll sample post and can
just be deleted. The four drafts that correspond to published Hashnode posts
(`2024-03-01-first-day-plan.md`, `2024-03-20-20-minute-limit.md`,
`2024-04-27-capping-complexity.md`, `CQRSWithRDMS.md`) are superseded by section 2.
