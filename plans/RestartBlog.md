# Restarting the Blog

This file is the plan: what to do, what was decided, and what is still open.
**Everything retrospective lives in `RestartBlogJournal.md`** - notes from doing
the work, bugs hit and fixed, verification results. Write new history there, not
here, so this stays short enough to read before starting a task.

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

Source of truth moved to `master`, `.gitignore` rewritten, stale build output and
stale branches cleared. `gh-pages` was left in place to keep the site serving.

## Phase 1 - Eleventy skeleton  [DONE 2026-08-22]

Target layout:

```
blog/
├── package.json            # "type": "module", pinned deps, lockfile committed
├── eleventy.config.js
├── .github/workflows/pages.yml
├── src/
│   ├── _data/metadata.js       # replaces _config.yml
│   ├── _includes/              # layouts + partials (Liquid)
│   ├── posts/                  # published posts, one .md each
│   │   └── posts.json          # dir data: layout, tags, permalink
│   ├── drafts/                 # 2014-2024 drafts, excluded from build
│   ├── css/main.css
│   ├── feed.njk                # Nunjucks; see Phase 3
│   ├── feed.xsl.liquid
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
   - Single column, mobile-first. `--measure` for prose, `line-height: 1.6`.
     34rem to start; widened to 51rem on 2026-08-23.
   - Code blocks break out wider than the measure via a grid, so long Scala
     signatures do not wrap.
   - System font stack for prose and mono - no webfonts, no external requests.
   - A dark Prism theme for the build-time syntax highlighting.
7. Verify against the code-heaviest content: the centaur post's JSON blocks and
   `_posts/2016-06-13-Pimping-Config.md`'s Scala.

## Phase 3 - Feed and subscribing  [DONE 2026-08-22]

1. `src/feed.njk` using `@11ty/eleventy-plugin-rss` - Nunjucks, not Liquid,
   because the plugin's filters register only for Nunjucks. The 2016 `feed.xml`
   is a close model - same fields, same 10-item limit.
2. Emit **full post content** in the feed, not excerpts. Hashnode did full content
   in `content:encoded`; do not regress.
3. Confirm the autodiscovery `<link>` resolves, and that the feed validates.
4. Add a visible "Subscribe (RSS)" link in the footer as well - autodiscovery
   covers readers, a visible link covers humans.
5. `src/feed.xsl.liquid` -> `/feed.xsl`, so a browser shows the feed as a page
   instead of raw XML. Added 2026-08-23.
6. Optional later: an email option (Buttondown/Listmonk) fed from the RSS.

## Phase 4 - Deploy, without moving DNS  [DONE 2026-08-23]

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

## Phase 5 - Migrate the 10 published Jekyll posts  [DONE 2026-08-23]

See `MigrateOldBlogs.md`.

All ten live at `/YYYY/MM/slug/`, with 20 redirect stubs, 10 feed items, and 12
sitemap URLs. 49 code blocks that Eleventy had been flattening into prose were
recovered and fenced with languages. The old Jekyll tree is deleted. Nothing is
outstanding in this phase.

---

## Open questions

Three need your call. They have been sitting in the notes since Phase 2 and are
easy to lose track of.

1. **A social link in the footer, or none?** The 2016 footer linked
   `twitter_username: dwalend`; `metadata.js` does not, and Phase 11 says X is not
   coming back. Mastodon would pair with the deferred fediverse-comments idea.
   Doing nothing is a fine answer - it just needs to be a decision.
2. **`about.md` wants your pass.** The Jekyll original literally read "This blog
   uses the base Jekyll theme," so it was rewritten from scratch. The words are
   currently mine, not yours.
3. **Keep `src/style-guide.md`?** It renders at `/style-guide/` as a typography
   and code specimen for checking the theme, and is excluded from collections so
   it stays out of the post list. Useful while the CSS is moving; delete it once
   it settles.

Two things to check rather than decide:

4. **ANSWERED 2026-08-25 - it is `application/xml` in production.** The feed
   renders as a page, no `text/plain` regression. Original note follows.
   **The `.xsl` content type on GitHub Pages.** Eleventy serves it as
   `application/xml` and browsers accept that, but the content type in production
   comes from GitHub's server. If it lands as `text/plain` the transform silently
   does nothing and the feed goes back to raw XML. Look at the next deploy.
5. **Local Node is 21.7.2, EOL since June 2024.** CI is pinned to 24, so this only
   affects the laptop - upgrading would also silence the
   `ExperimentalWarning: Importing JSON modules` on every build.

## Where things stand

Phases 0-6 are done: `gh-pages` retired, Enforce HTTPS on, OpenGraph tags and
card shipped, `description:` on every post, and the four Hashnode posts migrated.
Fourteen posts live. **Phase 7 - giscus comments, and rescuing the 2015 Disqus
thread - is next.**

Two follow-ups below are not blockers, and neither is urgent. Do them when
convenient, or fold them into the Phase 9 cutover.

### Find a reliable source for the Grover pictures

The CQRS post runs a gag: Grover, escalating from taken-aback to pleading, trying
to stop you reading - the joke from *The Monster at the End of This Book*. Five
images. They are staying; they need a source that does not rot.

Right now each one hotlinks a stranger's CDN, grabbed from image search, and
**three of the five are already dead**: `handoff-cdn.appadvice.com` does not
resolve, `media.licdn.com` returns 403, and one `<img>` had no `src` at all in
Hashnode's own HTML - it currently sits in the Markdown as an HTML comment
holding its alt text. The two that still answer are a Walmart product photo
(1.2 MB) and a Google thumbnail, and neither is a promise about next year.

**Self-hosting is the only fix.** Any external URL breaks again eventually, and
the point of the migration was to stop depending on other people's servers. Put
them in `src/img/posts/` beside the Planck curve and the CQRS diagram.

That makes the real question where to get five good stills, not how to reference
them:

- The **book itself** is the strongest fit - the gag is a direct reference, so
  frames or cover art from *The Monster at the End of This Book* land better than
  arbitrary Grover photos, and there is a clean provenance story.
- **Muppet Wiki** has the best catalogue by far. Download, do not hotlink; it is
  a Fandom site and hotlinking is both against their terms and unreliable.
- Whatever the source, **write real alt text**. The current alt lines are good
  ("Famous blue muppet pleading with you to read no further") and should survive.

Worth being clear-eyed: Grover is Sesame Workshop's, and there is no free licence
for these. Small illustrative images used for commentary on a non-commercial blog
is the ordinary case people rely on, and the site is already CC BY for prose with
the images plainly not his. That is a judgement call, not something to look up -
make it deliberately rather than by default. If it feels wrong, the fallback is
to cut the images and keep the escalating section headings, which carry most of
the joke on their own.

One image is currently missing entirely, so this is also the moment the gag goes
back to five beats instead of four.

### Rename the OpenGraph card back  [DONE 2026-08-24]

Folded into the Phase 9 cutover, as this section said to do if the cutover came
first. `src/img/og-card-v2.png` is back to `src/img/og-default.png`, with the
reference updated in `src/_includes/head.liquid`, `README.md`, and the recipe in
the journal.

The `v2` existed for one reason: on 2026-08-23 LinkedIn had cached the first,
badly quantised card on its own media servers, and Post Inspector refreshes page
metadata without replacing a stored image, so a new URL was the only reliable way
to force a refetch. The name carried no meaning and read as though a `v3` should
follow.

No separate re-inspection is needed. Every preview cache keys on URL, and moving
to `blog.walend.net` gives clean caches anyway.

Two checks that can only be done against the live site, so they belong with the
next deploy rather than with a commit:

- The `.xsl` content type on GitHub Pages. If it lands as `text/plain` the feed
  silently goes back to raw XML in the browser.
- Link previews, via a private Discord channel and LinkedIn's Post Inspector.
  Both cache hard, so check before announcing anything.

## Phase 6 - Migrate the 4 Hashnode posts  [DONE 2026-08-23, one decision open]

See `MigrateOldBlogs.md`. Text came from the **published** RSS content, not the
raw `_pending` drafts, because the published versions were edited.

All four live at `/2024/MM/slug/` with flat-slug aliases, descriptions, and tags.
The site is now 14 posts. The superseded `_pending` drafts were deleted - they
stay in git history. See the journal.

**The Grover gag stays**, and needs a reliable source for its five images - see
"Find a reliable source for the Grover pictures" above. They still point at the
original hotlinked URLs, which is what Hashnode serves today, so nothing
regressed; three of the five are simply already broken.

## Phase 7 - Comments  [DONE 2026-08-24]

1. **Discussions enabled** on `dwalend/blog`. Comments use **Announcements**,
   which only maintainers can start discussions in - what giscus wants.
2. **giscus GitHub App installed**, scoped to the one repo. Verified against
   `giscus.app/api/discussions`, which answers "Discussion not found" for a term
   with no thread yet rather than "giscus is not installed" - so the repo,
   category, and app all resolve. The first comment creates the discussion.
3. **`src/_includes/comments.liquid`.** Mapped with `specific` + `page.url`, not
   `pathname` - see the journal; `pathname` would have split every post's
   comments across the Phase 9 cutover. Theme `preferred_color_scheme`.
4. **Gated on `{% if comments %}`.** All 14 posts; not `/about/` or
   `/style-guide/`.
5. **The 2015 Disqus thread is preserved.** All six real comments are in
   `src/_data/archivedComments.json` and render above giscus on
   `/2015/06/escape-from-inner-trait/`. **No Disqus export was needed** - the
   forum's public RSS feed still had them. See the journal.

**One consequence worth knowing.** giscus is the first external request this site
makes - there are no webfonts, and highlighting happens at build time. Post pages
now load `giscus.app/client.js` and an iframe from the same host, so giscus.app
sees the IP of anyone who reads a post. That does not undo the "no analytics, no
trackers" decision, but it is no longer literally zero third parties.
`data-loading="lazy"` holds the request until the reader scrolls that far.

**Still worth doing by hand:** post a comment on one page and confirm it lands in
Discussions, renders in both colour schemes, and that the archived 2015 thread
sits above it without the two looking like one conversation.

## Phase 8 - Publish the first new post  [DONE 2026-08-24]

1. **Draft finished** and reviewed.
2. **Front matter added**: `title: A Centaur's Gait`, `comments: True`, a
   `description:`, and tags `AI` / `Claude Code` / `SDLC` alongside `post`. The
   date comes from the filename, as it does for every other post - no `date:`
   key needed. The body's `# A Centaur's Gait` line was removed, so the page has
   one `h1` from `post.liquid` and six `h2`s.
3. **Moved to `src/posts/`**, live at `/2026/08/centaur-hoofbeats/`. Fifteen
   posts; it leads the index and the feed.
4. **Verified**: the JSON block highlights (`language-json`, real Prism tokens),
   its longest line is 68 characters so it scrolls inside its own `<pre>` on a
   phone rather than pushing the page sideways, and OpenGraph, giscus, and the
   `#boink` anchor all resolve.

**Note the date.** The filename says 2026-08-25 and the post is live now with
that date. Eleventy builds future-dated posts without complaint - there is no
`--future` flag to forget, the way Jekyll had. If it should read as the 24th,
rename the file; if the 25th is intended, nothing to do.

## Phase 9 - DNS cutover  [DONE 2026-08-25]

Everything Phases 1-8 gate is done and verified. What remains is the cutover
itself, which is deliberately not automated: the moment the DNS record changes,
every Hashnode URL dies.

### State after the cutover, 2026-08-25

| | |
| --- | --- |
| Live at | `https://blog.walend.net/` (Pages `build_type: workflow`, `cname: blog.walend.net`) |
| Posts / feed items / sitemap URLs / aliases | 15 / 10 / 17 / 24 |
| `blog.walend.net` | `CNAME dwalend.github.io`, TTL **300** |
| Route 53 hosted zone | `Z09976561DOUNYRCRMG2A` (`walend.net.`) |
| Certificate | Let's Encrypt, `CN=blog.walend.net`, to 2026-11-23 |
| Cutover commits | `30f4d34`, then the runbook commit; build `32862473920` is the first at `prefix '/'` |

**Post-cutover verification, over both http and https**: `bin/sweep.sh` checked
52 URLs with 0 failures and its sanity check returned 404. Feed self-links and
guids are on `https://blog.walend.net`, `/rss.xml` answers 200 for the Hashnode
subscribers, autodiscovery points at `/feed.xml`, and `/feed.xsl` comes back as
`application/xml`.

### What the state was before, 2026-08-24

**Pre-cutover verification passed with zero failures**: every core page
(`/`, `/about/`, `/feed.xml`, `/feed.xsl`, `/rss.xml`, `/robots.txt`,
`/sitemap.xml`, `/llms.txt`, the OG card), all 15 posts, and all 24 alias stubs
return 200. The checker was sanity-tested against a URL that should 404, so the
result is real rather than a broken loop reporting success.

### Committed, not yet pushed

`30f4d34 "Before DNS cutover."` carries all of it:

- `src/CNAME` containing `blog.walend.net`, plus its `addPassthroughCopy` in
  `eleventy.config.js` - it has no extension, so Eleventy skips it otherwise.
  **It turned out to be inert.** The artifact's CNAME does not register a custom
  domain for a custom Actions workflow, only for branch-based publishing; the
  domain had to be set over the API. The file is harmless and matches what the
  Pages settings say, so it stays, but the comment in `eleventy.config.js`
  claiming it "sets the custom domain" is wrong and should be corrected.
- `src/rss.njk` and `src/_includes/feed-body.njk`. **See the journal** - this one
  is not cosmetic, it is the difference between keeping and losing the existing
  Hashnode subscribers.
- The og-card rename, `og-card-v2.png` -> `og-default.png`, folded in here
  because every preview cache resets at the cutover anyway.

The predecessor commit, `446d936`, shipped `feed.njk` in its new one-line include
form without the three files it depends on, so Actions run #20 died with
`template not found: feed-body.njk` and wrote 0 files. That was fail-safe - the
artifact upload never ran, and Pages kept serving the previous deploy - but it
is why `master` sat red overnight. `30f4d34` is the fix.

`bin/` holds what the cutover needs: `sweep.sh`, and the three Route 53 change
batches as files rather than heredocs.

### The order, which is not the order this plan originally had

Two things force the sequence, and they pull against each other.

**DNS has to move before Pages settings.** GitHub validates the DNS record when a
custom domain is set, and it still points at Hashnode. That is why the original
step list - Pages settings, then DNS - fails.

**The build reads its base path from the Pages settings, not from `src/CNAME`.**
`actions/configure-pages` reports `base_path`, and the workflow passes it through
as `PATH_PREFIX`. The failed run on 2026-08-24 logged it plainly:

```
Building for https://dwalend.github.io (prefix '/blog')
```

So the first build after `src/CNAME` lands will *still* emit `/blog/...` URLs
while the site is being served at the root of `blog.walend.net`. CSS, images, and
all 24 aliases would 404. **The custom domain has to register before the build
that produces the final URLs**, which means a second run, not one.

So: cut DNS over first, let the domain register, then rebuild.

Every command below is meant to be copied out of this file rather than retyped.
The Route 53 change batches live in `bin/` as real files, so no command here
carries a multi-line quoted heredoc - that is what made the first attempt at
this fail on a mangled quote. **Run them from the repo root**; the `file://`
paths are relative to the working directory.

#### 1. Lower the TTL, then wait about ten minutes

```sh
aws route53 change-resource-record-sets \
  --hosted-zone-id Z09976561DOUNYRCRMG2A \
  --change-batch file://bin/route53-ttl60.json
```

Still pointing at Hashnode; only the TTL moves. The wait matters because
resolvers holding the old record keep it for up to the *old* 600 seconds. Watch
it drop, and go when it reads 60:

```sh
dig +noall +answer blog.walend.net @8.8.8.8
```

#### 2. Push, and wait for green

```sh
git push && sleep 10 && gh run watch
```

This build logs `prefix '/blog'`, which is correct at this point - DNS has not
moved and the site is still served at `dwalend.github.io/blog/`. **Do not go on
from a red run.**

#### 3. Route 53 cutover, immediately after

```sh
aws route53 change-resource-record-sets \
  --hosted-zone-id Z09976561DOUNYRCRMG2A \
  --change-batch file://bin/route53-cutover.json
```

Then wait for it to resolve. Want `dwalend.github.io.` and the four
`185.199.10[8-11].153` addresses:

```sh
dig +short blog.walend.net @8.8.8.8
```

**Rollback**, valid at any point from here on:

```sh
aws route53 change-resource-record-sets \
  --hosted-zone-id Z09976561DOUNYRCRMG2A \
  --change-batch file://bin/route53-rollback.json
```

#### 4. Set the custom domain

`src/CNAME` in the artifact **does not** register the domain for a custom Actions
workflow - confirmed on 2026-08-25, `cname` stayed `null` after a green deploy
carrying the file. Set it over the API:

```sh
gh api -X PUT repos/dwalend/blog/pages -f cname=blog.walend.net
```

Silent `204` is success. Confirm:

```sh
gh api repos/dwalend/blog/pages --jq '{cname,html_url,https_enforced}'
```

**Do not pass `https_enforced` here.** GitHub rejects that field outright while
no certificate exists, even setting it to `false`:

```
{"message": "The certificate does not exist yet", "status": "404"}
```

The whole request is refused, nothing partially applies, and GitHub flips
`https_enforced` to `false` on its own when the domain changes.

If the API refuses for some other reason, the UI path is: repo page ->
**Settings** (top nav, right end) -> **Pages** (left sidebar, under "Code and
automation") -> **Custom domain** field -> type `blog.walend.net` -> **Save**.

#### 5. Rebuild so the URLs come out at `/`  (always - this is not optional)

Setting the domain over the API **does not queue a rebuild.** The artifact still
in place was built with `prefix '/blog'` and is now being served at the root, so
between step 4 and this step the live site is up but unstyled - every asset and
alias 404s:

```
http://blog.walend.net/                    200
http://blog.walend.net/css/main.css        200   the file is there
page links                                 /blog/css/main.css
http://blog.walend.net/blog/css/main.css   404   but the HTML points here
```

Keep this window short:

```sh
gh workflow run pages.yml && sleep 20 && gh run watch
```

Confirm the prefix is gone rather than assuming it. Want `prefix '/'`:

```sh
gh run view --log | grep 'Building for'
curl -s http://blog.walend.net/ | grep -o 'href="[^"]*main.css"'
```

If it still says `/blog`, the domain had not registered when the build started.
Wait a minute and run it again.

#### 6. Wait for the certificate - usually already done

Check before waiting. On 2026-08-25 the certificate issued about twelve minutes
after step 4, so by the time step 5's rebuild was verified it was already live
and this step was a no-op:

```sh
curl -sI --max-time 10 https://blog.walend.net/ | head -1
```

`HTTP/2 200` means go straight to step 7. If it does not answer, GitHub retries
on its own - minutes to about an hour - and this waits it out:

```sh
until curl -sI --max-time 10 https://blog.walend.net/ >/dev/null 2>&1; do sleep 60; done; echo "HTTPS answering"
```

Note that Let's Encrypt backdates `notBefore` about an hour for clock skew, so a
certificate can look older than the moment you set the domain. That is normal
and not evidence of a stale certificate.

#### 7. Enforce HTTPS

```sh
gh api -X PUT repos/dwalend/blog/pages -F https_enforced=true
gh api repos/dwalend/blog/pages --jq '{cname,https_enforced}'
```

UI fallback: **Settings** -> **Pages** -> **Enforce HTTPS** checkbox, below the
custom domain field. It stays greyed out until the certificate exists.

#### 8. Full sweep

`bin/sweep.sh` checks every URL the local build produces against a live base URL,
and sanity-tests itself against a URL that must 404. Build first so the list is
current:

```sh
npx @11ty/eleventy && bin/sweep.sh https://blog.walend.net
```

Want `checked 52 URLs, 0 failures` and `sanity check (want 404): 404`. Run this
**after** step 5 - against a `/blog/`-prefixed build it passes every page and
fails every asset, which is a confusing way to find the problem.

Three things the sweep cannot check:

```sh
curl -sI https://blog.walend.net/feed.xsl | grep -i content-type
```

Want `application/xml` or `text/xsl`. If it lands as `text/plain` the transform
silently does nothing and the feed shows as raw XML in a browser.

Then subscribe to `https://blog.walend.net/feed.xml` in a real reader to confirm
autodiscovery, and paste a post link into a private Discord channel and
LinkedIn's Post Inspector for the card.

#### 9. Leave the Hashnode blog in place

Unpublished-to, not deleted. **The backstop is the DNS rollback, not the
subdomain.** `dwalend.hashnode.dev` returns 403 on every page after the cutover
- only its `/rss.xml` still answers - because Hashnode still holds
`blog.walend.net` as its custom domain and serves the free subdomain as a 403
while one is configured.

That same configuration is what makes `bin/route53-rollback.json` work, so
removing the custom domain in Hashnode's dashboard would restore the subdomain at
the cost of the rollback path. Bad trade. Leave it.

#### 10. Nothing to do about the TTL

The step 3 batch UPSERTs the whole record set, so the record comes back at TTL
300 with the new value. The 60 from step 1 does not survive and needs no reset.

### Every feed guid changes at this moment

Guids go from `https://dwalend.github.io/blog/...` to `https://blog.walend.net/...`.
A subscriber would re-see the entire back catalogue as new.

**This is harmless only because nobody is subscribed to the github.io feed** - it
was never announced. After the cutover the guids are stable for good. This is the
last moment that is free, which is a reason to cut over before Phase 11 tells
anyone the feed exists.

### Fold these in while the caches clear

Both are in "Where things stand" above, and every preview and DNS cache resets
here anyway:

- ~~Rename the OpenGraph card off its temporary `og-card-v2.png`.~~ Done.
- Source the Grover pictures properly.

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

### 1. OpenGraph tags  [DONE 2026-08-23]

`head.liquid` emits the full set, with `src/img/og-default.png` as a site-wide
card. See the journal. Two things still worth doing when this phase comes up:

- **Verify with the real scrapers** - paste a link into a private Discord
  channel, and run one through LinkedIn's Post Inspector. Neither can be checked
  from here, and both cache aggressively, so check before announcing rather than
  after.
- **Per-post cards, maybe.** One site-wide image is enough to start. A generated
  card per post would read better in a feed of links, but it is only worth it if
  the announcements turn out to matter.

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
