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
  frontmatter, render replies alongside giscus. Doubles as distribution. Phase 2.

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

## Phase 1 - Eleventy skeleton

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

## Phase 2 - Templates and theme

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

## Phase 3 - Feed and subscribing

1. `src/feed.xml.liquid` using `@11ty/eleventy-plugin-rss`. The 2016 `feed.xml`
   is a close model - same fields, same 10-item limit.
2. Emit **full post content** in the feed, not excerpts. Hashnode did full content
   in `content:encoded`; do not regress.
3. Confirm the autodiscovery `<link>` resolves, and that the feed validates.
4. Add a visible "Subscribe (RSS)" link in the footer as well - autodiscovery
   covers readers, a visible link covers humans.
5. Optional later: an email option (Buttondown/Listmonk) fed from the RSS.

## Phase 4 - Deploy, without moving DNS

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

## Phase 5 - Migrate the 10 published Jekyll posts

See `MigrateOldBlogs.md`.

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
