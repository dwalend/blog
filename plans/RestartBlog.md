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

4. **The `.xsl` content type on GitHub Pages.** Eleventy serves it as
   `application/xml` and browsers accept that, but the content type in production
   comes from GitHub's server. If it lands as `text/plain` the transform silently
   does nothing and the feed goes back to raw XML. Look at the next deploy.
5. **Local Node is 21.7.2, EOL since June 2024.** CI is pinned to 24, so this only
   affects the laptop - upgrading would also silence the
   `ExperimentalWarning: Importing JSON modules` on every build.

## Where things stand

Phases 0-5 are done and the carry-over list is empty: `gh-pages` retired, Enforce
HTTPS on, OpenGraph tags and card shipped, `description:` written for all ten
posts. **Phase 6 is next.**

Two checks that can only be done against the live site, so they belong with the
next deploy rather than with a commit:

- The `.xsl` content type on GitHub Pages. If it lands as `text/plain` the feed
  silently goes back to raw XML in the browser.
- Link previews, via a private Discord channel and LinkedIn's Post Inspector.
  Both cache hard, so check before announcing anything.

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
