# Restarting the Blog

## Goals

Start the new blog and migrate the old blogs.

- Most of a first new entry is written in `_pending/2026-08-25-centaur-hoofbeats.md`.
- Need to show that first entry and future entries.
- Self-host on GitHub at `http://blog.walend.net`.
- Readers should be able to subscribe for updates - probably via RSS.
- Old blog entries exist on hashnode; `blog.walend.net` currently points there.
- More old entries exist in the wayback machine from java.net. There's an especially
  good article on service-oriented architecture worth capturing and writing a
  20-year retrospective about.
- `private-duck-aligner` has a massive collection under `blog-fodder` for future work.

See `MigrateOldBlogs.md` for the content-migration half of this.

## Decisions (2026-08-22)

| Question | Decision | Why |
| --- | --- | --- |
| Static site generator | **Eleventy 3.x** | Speaks Liquid, so the existing `_layouts` / `_includes` port with small edits. Markdown content stays portable. |
| Host | GitHub Pages, `dwalend/blog`, built by GitHub Actions | Source in git; Node pinned in CI, not on the laptop. |
| Domain | `blog.walend.net` (Route 53) | Already owned. Currently CNAME -> `hashnode.network`. |
| Permalinks | `/YYYY/MM/slug/` + aliases for old URLs | No slug collisions across 20+ years; aliases keep old links alive. |
| Feed | RSS at `/feed.xml` **with `<link rel="alternate">` autodiscovery** | Autodiscovery is the thing that was missing on Hashnode. |
| Comments | **giscus** (GitHub Discussions) | No server, no ads, no trackers, data stays in the repo. |
| Title | "Intuitive Counter" | Unchanged. |
| Styling | Hand-rolled CSS, ~200 lines, dark by default, single column | Whole design surface is small; avoids a framework dependency. |
| Analytics | None | Old UA property is dead; not re-adding tracking. |
| 2014-2024 unpublished drafts | Stay drafts | May be updated and published someday. |
| Content license | **CC BY 4.0** | The feed emits full post bodies, so readers, aggregators, and mirrors reproduce them wholesale. CC BY makes that unambiguously fine. Rejected BY-NC (ambiguous), BY-SA (viral), BY-ND (blocks translation). |
| Site code license | **MIT** | Conventional, and GitHub displays it. Covers the Eleventy config, templates, CSS. |
| Code samples in posts | **CC0 / public domain** | The first post's whole payload is a `settings.json` block meant to be pasted. Requiring attribution in someone's dotfiles is absurd. |
| Crawlers, AI included | **Welcome** | "Robots Welcome, too." Explicitly permissive `robots.txt`; no interest in blocking AI training. |

### Deliberately deferred

- **Rebuild in Laika** (Scala). Someday-maybe, and blog fodder in its own right.
  Not on the critical path - a hand-rolled Scala build is more to rot, and the
  goal here is to publish.
- **Scala.js for graph figures.** Cross-compile Disentangle to Scala.js and call it
  from an Eleventy shortcode to compute and emit SVG graph figures at build time.
  Good fit because it writes about the language it is written in, and because when
  it breaks only the figures break - the blog still builds and still publishes.
  Do this *after* the blog is up. See `disentangleParGraphs/` for prior art.
- **Fediverse comments.** Post each article to Mastodon, put the toot id in
  frontmatter, render replies alongside giscus. Still open - no objection to
  Mastodon, just no expectation of much traffic there, and possibly little
  traffic *because* it is not somewhere you currently spend time. That is a real
  chicken-and-egg and not an argument either way. giscus does not depend on it, so
  this can wait until there is a reason. See Phase 11.

## Sequencing principle

**Do not touch DNS until the new site is complete and verified.** The moment
`blog.walend.net` moves off Hashnode, every Hashnode URL dies. Build and verify
everything at `https://dwalend.github.io/blog/` first, with the Hashnode site still
serving readers. DNS is the last step, and it is a single Route 53 record change.

---

## Phase 0 - Repo hygiene  [DONE 2026-08-22]

1. **Source of truth moved to `master`.** `master` was a strict ancestor of
   `gh-pages` (100 commits behind, zero divergent), so this was a clean
   `git merge --ff-only gh-pages`. `origin/HEAD` already points at `master`, so
   the default branch needed no change.
   - The fast-forward dropped `LICENSE` and `README.md`, which existed on the old
     `master` initial commit and had been deleted on `gh-pages`. Worth adding a
     README back at some point.
2. **`gh-pages` stays, for now.** It is still serving `dwalend.github.io/blog`
   through the legacy Pages build (`build_type: legacy`, `source: gh-pages`).
   Retire it in Phase 4, once the Actions workflow is deploying. Switching the
   Pages source before a workflow exists would take the live site down - that
   step lives in Phase 4, not here.
3. **`.gitignore` rewritten.** Added `node_modules/` and `.eleventy-cache/` for the
   incoming Eleventy build, plus `.DS_Store`. Directories now carry trailing
   slashes, entries are grouped, and the missing newline at end of file is fixed.
   - Correction to an earlier draft of this plan: `_site/`, `.sass-cache/`,
     `.jekyll-cache/`, `.idea/`, and `.DS_Store` were **never tracked** - only 57
     files are in the index. There was no checked-in build output and nothing to
     `git rm --cached`.
4. **Stale build output removed from the working tree**: `_site/`, `.sass-cache/`,
   `.jekyll-cache/`. All ignored, all derived - every one of the 23 files in
   `_site` mapped onto the 10 posts plus `about.md`, `css/`, `disentangleParGraphs/`,
   `feed.xml`, and `index.html`.
5. **Stale branches.** `toJekyll3`, `origin/pending`, and `origin/setup` all have
   **zero commits not reachable from `master`**, so deleting them loses nothing.
6. Kept: `_posts/`, `_layouts/`, `_includes/`, `_sass/`, `disentangleParGraphs/`,
   `about.md`, and `_pending/` as the drafts folder.

## Phase 1 - Eleventy skeleton  [DONE 2026-08-22, except item 11]

Target layout:

```
blog/
├── package.json            # "type": "module", pinned deps, lockfile committed
├── eleventy.config.js
├── .github/workflows/pages.yml
├── src/
│   ├── _data/metadata.json     # replaces _config.yml
│   ├── _includes/              # layouts + partials (Liquid)
│   ├── posts/                  # published posts, one .md each
│   │   └── posts.json          # dir data: layout, tags, permalink
│   ├── drafts/                 # 2014-2024 drafts, excluded from build
│   ├── css/main.css
│   ├── feed.xml.liquid
│   ├── index.liquid
│   ├── about.md
│   └── CNAME                   # blog.walend.net  (add at Phase 9, not before)
└── disentangleParGraphs/       # passthrough copy
```

1. `npm init`, set `"type": "module"`, install pinned:
   - `@11ty/eleventy@3.1.6`
   - `@11ty/eleventy-plugin-rss@3.0.0`
   - `@11ty/eleventy-plugin-syntaxhighlight@5.0.2`
   Commit `package-lock.json`.
2. `eleventy.config.js`: input `src`, output `_site`, Liquid as the template engine,
   register the three plugins, add a passthrough copy for `disentangleParGraphs/`
   and `css/`.
3. `src/_data/metadata.json` carries what `_config.yml` used to:
   title "Intuitive Counter", description, author email, url `https://blog.walend.net`,
   github/social handles. Note `baseurl` disappears - with a custom domain on a
   project repo the site serves from `/`, not `/blog/`.
4. `src/posts/posts.json` sets the defaults for every post:
   `{"layout": "post", "tags": "post", "permalink": "/{{ page.date | date: '%Y/%m' }}/{{ page.fileSlug }}/"}`
5. Exclude `src/drafts/` from the build (`eleventyExcludeFromCollections`, or just
   keep drafts outside `src/`).
6. Verify: `npx @11ty/eleventy --serve` renders a stub index.
7. `LICENSE` - MIT, covering the site code.
8. `README.md` - written now that there is a real build to describe: what the
   stack is, `npm ci && npx @11ty/eleventy`, where posts and drafts live, and a
   `## License` section spelling out the three-way split (prose CC BY 4.0, site
   code MIT, in-post snippets CC0).
9. `src/robots.txt` - permissive, with a `Sitemap:` line. Name the AI crawlers
   with an explicit `Allow` rather than relying on the default, so the intent is
   on the record. Check whether `llms.txt` is worth adding alongside it.
10. Restore the stripped BSD-3-Clause copyright headers to
    `disentangleParGraphs/js/d3.v3.js` (d3 3.5.6) and `.../queue.js`. Both are
    Mike Bostock's and both are redistributed from the site.
11. Footer line, since it is the only license text a reader will ever see:
    "Words (c) David Walend, CC BY 4.0. Code samples: public domain."
    **Deferred to Phase 2** - there is no footer template yet.

Notes from doing this:

- `SITE_URL` and `PATH_PREFIX` are both overridable, and both were verified:
  `PATH_PREFIX=/blog/ SITE_URL=https://dwalend.github.io` correctly yields
  `https://dwalend.github.io/blog/sitemap.xml`. Phase 4 needs those set.
- `llms.txt` is generated from the post collection rather than hand-maintained.
  Adoption is around 8.7% of the top 1,000 sites with a W3C proposal as of
  June 2026 and no demonstrated ranking benefit, but IDE agents do fetch it and
  generating it costs nothing.
- **Local Node is v21.7.2, which went EOL in June 2024.** Eleventy needs >= 18 so
  it runs, but pin CI to an LTS (22 or 24) in Phase 4, and upgrading locally
  would also silence the `ExperimentalWarning: Importing JSON modules` on
  every build.
- `node --check` reports a syntax error in the vendored `queue.js` only because
  `package.json` declares `"type": "module"`, which makes node parse it as ESM
  where d3-queue's `await = noop` variable is a reserved word. It loads as a
  classic script in the browser and Eleventy only copies it. Not a problem.


## Phase 2 - Templates and theme  [DONE 2026-08-22]

1. Port `_layouts/default.html` -> `src/_includes/base.liquid`. Mostly mechanical:
   `site.foo` -> `metadata.foo`, `{% include head.html %}` -> `{% include "head.liquid" %}`.
2. Port `_layouts/post.html` and `_layouts/page.html`.
3. Port `_includes/head.html`. **Keep the `<link rel="alternate" type="application/rss+xml">`
   tag** - it is already correct in the 2016 file and it is precisely what Hashnode
   lacks.
4. Drop `_includes/google_analytics.html` entirely.
5. Replace `_includes/comments.html` (Disqus) with a giscus include - Phase 7.
6. New `src/css/main.css`, replacing `_sass/`:
   - `:root { color-scheme: dark light; }`
   - Palette as custom properties on `:root` (dark), overridden in
     `@media (prefers-color-scheme: light)`.
   - Single column, mobile-first. `max-width: 34rem` for prose, `line-height: 1.6`.
   - Code blocks break out wider than the measure via a grid, so long Scala
     signatures do not wrap.
   - System font stack for prose and mono - no webfonts, no external requests.
   - A dark Prism theme for the build-time syntax highlighting.
7. Verify against the code-heaviest content: the centaur post's JSON blocks and
   `_posts/2016-06-13-Pimping-Config.md`'s Scala.

Notes from doing this:

- Layouts live in `src/_includes/`: `base.liquid` (was `default.html`), plus
  `post.liquid`, `page.liquid`, `head.liquid`, `header.liquid`, `footer.liquid`.
- The old header's hamburger menu and `site.pages` loop are gone. One column does
  not need a collapsing nav - Posts / About / RSS as plain links.
- The footer carries the license line, which closes Phase 1 item 11.
- **Twitter is not carried over.** The 2016 footer linked `twitter_username:
  dwalend` and `metadata.js` does not. Say if it should come back, and whether as
  X or as Mastodon (which pairs with the deferred fediverse-comments idea).
- `about.md` was Jekyll boilerplate - it literally read "This blog uses the base
  Jekyll theme." Rewritten from scratch, and worth your own pass.
- `src/style-guide.md` at `/style-guide/` is a typography and code specimen for
  checking the theme. Excluded from collections, so it is not in the post list.
  Delete it if it is not wanted.
- Code breaks out past the 34rem prose measure to a 52rem band via a three-column
  grid on `.post-content`, so long Scala signatures have room. Wide code scrolls
  inside its own `<pre>`; the page body never scrolls sideways.
- Contrast was checked programmatically against WCAG AA for both palettes. One
  failure found and fixed: the light-theme comment token was 4.40:1, now 5.02:1.
  Everything else ranges 4.5:1 to 17.8:1.
- Dropped `_includes/google_analytics.html`, which carried `UA-54450354-1`.
- **The feed is a dangling link until Phase 3.** `head.liquid` emits the
  autodiscovery tag and the header and footer link `/feed.xml`, but nothing
  generates it yet. That is Phase 3's first item.
- The rest of the old Jekyll tree (`_layouts/`, `_includes/`, `_sass/`,
  `css/main.scss`, root `index.html`, `feed.xml`, `about.md`) is now superseded
  but still present. Sweep it in Phase 5 with the post migration, in one go.

## Phase 3 - Feed and subscribing  [DONE 2026-08-22]

1. `src/feed.xml.liquid` using `@11ty/eleventy-plugin-rss`. The 2016 `feed.xml`
   is a close model - same fields, same 10-item limit.
2. Emit **full post content** in the feed, not excerpts. Hashnode did full content
   in `content:encoded`; do not regress.
3. Confirm the autodiscovery `<link>` resolves, and that the feed validates.
4. Add a visible "Subscribe (RSS)" link in the footer as well - autodiscovery
   covers readers, a visible link covers humans.
5. Optional later: an email option (Buttondown/Listmonk) fed from the RSS.

Notes from doing this:

- The feed is **`src/feed.njk`, not `.liquid`**. Every filter
  `@11ty/eleventy-plugin-rss` 3.0.0 registers is Nunjucks-only
  (`addNunjucksFilter`), and this site is Liquid, so a Liquid feed would have had
  no `dateToRfc822`. `njk` is in `templateFormats` for this one file.
- The plugin's own built-in RSS virtual template was **not** used: it emits
  `<content:encoded>` while declaring only `xmlns:dc` and `xmlns:atom` on the
  `<rss>` root, with no `xmlns:content`, which is not well-formed XML. The
  hand-written template declares all three.
- `eleventyFeedHead` is registered by the plugin's virtual-template module, not
  the base plugin, so the 10-item limit is a `loop.index0` guard instead.
- `description` is `post.data.description` if a post sets one, otherwise a
  220-character auto-excerpt. `content:encoded` carries the full post. Worth
  setting `description` in frontmatter during Phases 5 and 6 - the auto-excerpt
  just takes the opening words.

### Two bugs found and fixed while verifying

- **Dates were a day early, and permalinks landed in the wrong month.** Eleventy
  reads the date from the filename as UTC midnight; Liquid and `dateRfc822` both
  rendered it in local time (EDT), moving it back four hours. A probe post named
  `2026-09-01-*` published at `/2026/09/` only after the fix - before it, it went
  to **`/2026/08/`**. Fixed with `setLiquidOptions({ timezoneOffset: 0 })` and by
  passing `"UTC"` to `dateToRfc822`. This mattered: the alias scheme in Phases 5
  and 6 is built on these permalinks.
- **The path prefix was applied twice**, giving `href="/blog/blog/feed.xml"` in
  the nav and footer. The RSS plugin force-adds Eleventy's HTML base plugin,
  which rewrites root-relative URLs, and the templates already do that with the
  `url` filter. Fixed by passing `htmlBasePluginOptions: { baseHref: "/" }` so
  the transform passes those through. Absolute URLs were never affected, which is
  why the autodiscovery tag looked correct. **This only shows up under
  `PATH_PREFIX`, which is exactly the Phase 4 deploy.**

Verified: XML well-formed with all three namespaces resolving, excerpt in
`description` against full text in `content:encoded`, no relative URLs left
inside the content, empty-collection build omits `lastBuildDate` and still parses,
and both the production and `PATH_PREFIX=/blog/` builds emit correct links.

## Phase 4 - Deploy, without moving DNS  [DONE 2026-08-23; gh-pages still to retire]

1. `.github/workflows/pages.yml`: `actions/checkout` -> `actions/setup-node` with a
   pinned Node version and npm cache -> `npm ci` -> `npx @11ty/eleventy` ->
   `actions/upload-pages-artifact` -> `actions/deploy-pages`.
2. Repo Settings -> Pages -> Source = **GitHub Actions**. This is the step that
   moves the site off the legacy `gh-pages` build - do it only once the workflow
   above is green, since it takes the legacy build offline.
3. Once the Actions deploy is verified, retire the `gh-pages` branch (local and
   `origin`). It is fully contained in `master`, so nothing is lost.
4. **Do not add `src/CNAME` yet.** Site publishes to `https://dwalend.github.io/blog/`.
5. Verify there: pages render, CSS loads, feed validates, links resolve.
   Note the `/blog/` path prefix here versus `/` after the custom domain - use
   Eleventy's url filter everywhere so both work.

Notes from doing this:

- `.github/workflows/pages.yml` written. Action versions were checked rather than
  assumed, and they have moved a long way: `checkout@v7`, `setup-node@v7`,
  `configure-pages@v6`, `upload-pages-artifact@v5`, `deploy-pages@v5`.
- Node pinned to **24**, the current Active LTS (Krypton). Node 22 (Jod) is in
  maintenance; the laptop's 21 went EOL in 2024.
- **The workflow needs no edit at Phase 9.** `PATH_PREFIX` and `SITE_URL` come
  from `configure-pages` outputs (`base_path` and `origin`), which Pages fills in
  from its own configuration - so it yields `dwalend.github.io` + `/blog` now and
  `blog.walend.net` + `/` once the custom domain is set. Both cases were built
  locally and produce correct links, including `base_path` with no trailing slash
  and an empty `base_path`.
- `npm run build` now runs `clean` first. Eleventy does not remove stale output,
  and leftover files from deleted posts sat in `_site` until this was noticed.
  CI is unaffected - it always builds from a fresh checkout.
- Careful with `npm ci --dry-run`: it removes `node_modules` before doing
  anything, dry run or not.

### What is left, and why it is not mine to do

`git push` and `git commit` are denied, and flipping the Pages source changes what
the public site serves. In order:

1. **You push** `master`. Nothing happens yet - Pages is still on the legacy
   `gh-pages` build, and the workflow will run but its deploy step will fail or
   no-op until step 2.
2. **You flip** Settings -> Pages -> Source to **GitHub Actions**. This is the
   moment the site stops coming from `gh-pages`. The last legacy build usually
   keeps serving until the first Actions deployment replaces it.
3. **Re-run the workflow** if step 1 ran before step 2.
4. **Verify** at `https://dwalend.github.io/blog/`: the page renders with styling,
   `/blog/feed.xml` parses, `/blog/robots.txt` and `/blog/sitemap.xml` resolve,
   and the nav links go to `/blog/...` rather than `/blog/blog/...`.
5. **Then** retire `gh-pages`, local and origin. It is fully contained in
   `master`.

Do not add `src/CNAME` yet - that is Phase 9.

### Outcome

Deployed and verified live at `https://dwalend.github.io/blog/`. All of `/`,
`/about/`, `/style-guide/`, `/css/main.css`, `/feed.xml`, `/robots.txt`,
`/sitemap.xml`, `/llms.txt`, and the vendored d3 return 200. Nav links read
`/blog/about/` and not `/blog/blog/about/`, which confirms the Phase 3
double-prefix fix in production - the only place it could have shown.

The first two runs failed at the deploy step: *Branch "master" is not allowed to
deploy to github-pages due to environment protection rules.* The `github-pages`
environment had a branch policy left over from the legacy build that allowed only
`gh-pages`. Adding `master` to Settings -> Environments -> github-pages fixed it.
Note the build job succeeded throughout; only the deploy gate rejected it.

### One fix that matters before Phase 5

Everything absolute came out **`http://`**, not https: the autodiscovery tag, the
feed's channel link and self link, and the `Sitemap:` line. `configure-pages`
reports `origin` from the Pages config, and this repo has `https_enforced: false`
with no certificate, so `html_url` is `http://...`.

Harmless with zero posts. Not harmless once posts exist: RSS readers key on
`<guid>`. Publishing with `http://` guids and later flipping to `https://` makes
every subscriber re-see the entire back catalogue as new.

The workflow now forces https itself (`https://${PAGES_ORIGIN#*://}`), so it holds
whatever the Pages setting says, at either domain. **Also worth turning on
Settings -> Pages -> Enforce HTTPS**, which will additionally fix `html_url`.

### Still to do

Retire `gh-pages`, local and origin. It is fully contained in `master`. Note the
Pages config still reports `source: {branch: gh-pages}` next to
`build_type: workflow` - that field is vestigial once the build type is Actions,
so ignore it rather than setting it back.

## Phase 5 - Migrate the 10 published Jekyll posts  [DONE 2026-08-23]

See `MigrateOldBlogs.md`.

All ten moved to `src/posts/`, live at `/YYYY/MM/slug/`, with 20 redirect stubs,
10 feed items, and 12 sitemap URLs (stubs correctly excluded).

### The one that mattered: 49 code blocks were rendering as prose

Eleventy disables markdown-it's indented code blocks by default -
`this.mdLib.disable("code")`, its Issue #2438. Eight of the ten posts use
four-space indented code throughout, which kramdown rendered as code and Eleventy
was silently flattening into paragraphs. Every Scala sample in those posts was
running together as body text.

Fixed with `eleventyConfig.amendLibrary("md", (md) => md.enable("code"))`.
That recovered **49 code blocks**, in the pages and in the feed. Worth knowing
this is a rendering-engine difference, not an authoring choice - the posts were
always correct.

### Aliases

`aliases:` in each post's front matter lists the old URLs; a collection in
`eleventy.config.js` flattens them and `src/alias.liquid` paginates one stub per
entry, with `rel=canonical` plus a meta refresh. Both shapes that were in
circulation are covered - `/2016/06/13/Pimping-Config.html` and
`/2016/06/13/Pimping-Config/`. The same mechanism carries Phase 6's Hashnode
slugs, which is why it is front matter rather than derived from filenames.

### Other repairs

- **CRLF line endings** in `2014-09-01-back-in.md` and
  `2014-09-10-graphs-in-scala.md`, normalised to LF. They had been breaking
  front-matter parsing in tooling that expects `^---$`.
- **Fence tags**: five ```` ```Scala ```` (capital S) would not have matched
  Prism's lowercase language classes. Now nine ```` ```scala ```` and one
  ```` ```bash ````.
- **Three cross-links between posts** pointed at absolute
  `dwalend.github.io/blog/YYYY/MM/DD/...` URLs. Rewritten relative and to the new
  scheme, so they work on either domain. The two remaining `dwalend.github.io`
  links are Disentangle scaladoc, correctly left alone.
- No `{% highlight %}` blocks, no `site.baseurl`, no Liquid at all in the bodies -
  the plan anticipated those and none existed.

### Code blocks converted to fenced, with languages

The recovered blocks were `<pre><code>` with no language. All 50 indented blocks
across seven posts are now fenced and labelled, judged block by block:

**51 scala, 3 bash, 1 java, 4 deliberately unlabelled.**

- The `java` block is in `Semirings` - angle-bracket generics and
  `new Dijkstra<...>()`, a Java comparison against the Scala version.
- The `bash` blocks are `git clone` / `cd` sequences.
- The four unlabelled ones are all in `Enron-Thing`: two `scala>` REPL
  transcripts and two blocks of raw result data. A language tag would have
  highlighted the prompts and stack traces as if they were source.
- `sbt` fragments (`libraryDependencies +=`, `resolvers +=`) are tagged `scala`,
  which is what they are.

Two mistakes made and corrected while doing this, both worth remembering:

- **The first block detector ignored existing fences**, so in the two posts that
  already used ```` ``` ```` it inserted new fences *inside* open blocks, breaking
  the pairing. The detector now tracks fence state - and with that fix, those two
  posts turn out to have no loose indented blocks at all.
- **One "CSS block" was live CSS**, not a sample: `Easy-Parallel` embeds a d3
  chart, and its `<style type="text/css">` contents got wrapped in a fence.
  Unwrapped. It is the only post carrying live HTML.

Verified afterwards: fences balanced in all ten posts, prose and code identical to
`HEAD` apart from the intended cross-link rewrites, and the chart's relative
`../../../disentangleParGraphs/js/plot.js` still resolves - the old permalink had
three path segments plus a filename, the new one has three directory segments, so
the depth happens to match.

Feed `description` still falls back to an auto-excerpt; setting `description` in
front matter per post would read better in readers.

## Phase 6 - Migrate the 4 Hashnode posts

See `MigrateOldBlogs.md`. Text comes from the **published** RSS content, not the
raw `_pending` drafts, because the published versions were edited.

## Phase 7 - Comments

1. Enable Discussions on `dwalend/blog`, create an "Announcements"-style category
   for comments.
2. Install the giscus GitHub App, scoped to the one repo.
3. Add `src/_includes/comments.liquid` with the giscus script, mapped by pathname,
   theme wired to the page palette (`preferred_color_scheme` or a fixed dark theme).
4. Gate on frontmatter the way the old Disqus include did - `{% if comments %}`.
5. Preserve the 2015 Disqus thread as static HTML - see `MigrateOldBlogs.md`.

## Phase 8 - Publish the first new post

1. Finish `_pending/2026-08-25-centaur-hoofbeats.md`.
2. Add frontmatter: `title: A Centaur's Gait`, `date: 2026-08-25`, `comments: true`,
   tags. The body currently starts with a bare `A Centaur's Gait` title line -
   that moves into frontmatter.
3. Move to `src/posts/`.
4. Verify the JSON code blocks highlight correctly and do not overflow on a phone.

## Phase 9 - DNS cutover

Only once Phases 1-8 are verified on `dwalend.github.io/blog`.

1. Add `src/CNAME` containing `blog.walend.net`. Push, let Actions deploy.
2. Repo Settings -> Pages -> Custom domain = `blog.walend.net`.
3. Route 53: change the `blog.walend.net` record from `CNAME hashnode.network`
   to `CNAME dwalend.github.io`. (Subdomain, so CNAME is correct - the four
   `185.199.10x.153` A records are only needed for an apex domain.)
4. Wait for GitHub to provision the Let's Encrypt cert, then enable **Enforce HTTPS**.
5. Verify: every alias from Phases 5-6 resolves, feed is reachable at the new
   host, autodiscovery works from a real feed reader.
6. Leave the Hashnode blog in place but stop posting to it. Its
   `dwalend.hashnode.dev` URLs keep working as a backstop.

## Phase 10 - After launch

- java.net / wayback recovery and the SOA 20-year retrospective (`MigrateOldBlogs.md`).
- Scala.js graph figures.
- Mine `private-duck-aligner`'s `blog-fodder`.
- Revisit Laika.

## Phase 11 - Distribution and social

Runs after Phase 9. Independent of Phase 10 - do it as soon as the site is live,
rather than waiting on the wayback archaeology.

The channels that matter are **LinkedIn** and **Discord**. Not Twitter/X - the
new site does not link it and it is not coming back. Mastodon stays an open
question rather than a no; see the deferred list.

### 1. OpenGraph tags first - this is a prerequisite, not a nicety

LinkedIn, Discord, and Slack all build their link previews from OpenGraph meta
tags. `src/_includes/head.liquid` has none today, so a pasted link renders as a
bare URL or a title-only card. Add to `head.liquid`:

- `og:title`, `og:description`, `og:url`, `og:type` (`article` for posts,
  `website` elsewhere), `og:site_name`
- `article:published_time` on posts
- `twitter:card` set to `summary_large_image` - despite the name, Discord and
  several others read these tags too
- `og:image` - needs an actual image. Options: a simple generated card per post,
  or one site-wide fallback. A site-wide fallback is enough to start.

Cheap, and it can land any time - it does not need to wait for the rest of this
phase. Verify with Discord's own preview (paste into a private channel) and
LinkedIn's Post Inspector.

### 2. LinkedIn

- Posts with outbound links get less reach than native text. The usual workaround
  is a substantive summary as the post body with the link in the first comment.
  Worth trying both and seeing whether it actually matters at this scale.
- Do **not** paste full post text as a LinkedIn article. It creates a duplicate
  with no reliable canonical back to `blog.walend.net`. Teaser plus link.

### 3. Discord

- Decide which servers. Scala's official Discord and Typelevel's are the obvious
  fits for the Scala and graph posts; the LLM-workflow posts suit somewhere else
  entirely.
- Read each server's self-promotion rules before posting. Most have a designated
  channel and dislike drive-by links.

### 4. Announcement routine

- Write down the actual steps for shipping a post, so it is a checklist and not a
  decision each time: publish -> verify the feed updated -> LinkedIn -> Discord.
- Consider whether any of it is worth automating from the RSS feed later. At a
  post every week or two, by hand is probably correct.

### 5. Relaunch post

One "the blog is back, here is where it lives, here is the feed" note on both
channels once Phase 9 is verified. Point at `/feed.xml` explicitly - the whole
reason for leaving Hashnode was that the feed had become undiscoverable.
