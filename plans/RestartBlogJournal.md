# Restarting the Blog - Journal

What actually happened, in order. `RestartBlog.md` says what to do next; this
says what was done, what broke, and why each fix is the shape it is.

Nothing here is required reading to pick up the next task. It is here for when
something behaves oddly and the answer is "we already hit that."

Append new entries at the bottom.

---

## 2026-08-22 - Phase 0: repo hygiene

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

## 2026-08-22 - Phase 1: Eleventy skeleton

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

## 2026-08-22 - Phase 2: templates and theme

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

## 2026-08-22 - Phase 3: feed and subscribing

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

#### Two bugs found and fixed while verifying

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

## 2026-08-23 - Phase 4: deploy, without moving DNS

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

#### What is left, and why it is not mine to do

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

#### Outcome

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

#### One fix that matters before Phase 5

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

#### Left open at the end of the phase

Retire `gh-pages`, local and origin. It is fully contained in `master`. Note the
Pages config still reports `source: {branch: gh-pages}` next to
`build_type: workflow` - that field is vestigial once the build type is Actions,
so ignore it rather than setting it back.

## 2026-08-23 - Phase 5: migrating the 10 Jekyll posts

All ten moved to `src/posts/`, live at `/YYYY/MM/slug/`, with 20 redirect stubs,
10 feed items, and 12 sitemap URLs (stubs correctly excluded).

#### The one that mattered: 49 code blocks were rendering as prose

Eleventy disables markdown-it's indented code blocks by default -
`this.mdLib.disable("code")`, its Issue #2438. Eight of the ten posts use
four-space indented code throughout, which kramdown rendered as code and Eleventy
was silently flattening into paragraphs. Every Scala sample in those posts was
running together as body text.

Fixed with `eleventyConfig.amendLibrary("md", (md) => md.enable("code"))`.
That recovered **49 code blocks**, in the pages and in the feed. Worth knowing
this is a rendering-engine difference, not an authoring choice - the posts were
always correct.

#### Aliases

`aliases:` in each post's front matter lists the old URLs; a collection in
`eleventy.config.js` flattens them and `src/alias.liquid` paginates one stub per
entry, with `rel=canonical` plus a meta refresh. Both shapes that were in
circulation are covered - `/2016/06/13/Pimping-Config.html` and
`/2016/06/13/Pimping-Config/`. The same mechanism carries Phase 6's Hashnode
slugs, which is why it is front matter rather than derived from filenames.

#### Other repairs

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

#### Code blocks converted to fenced, with languages

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

#### The Jekyll tree is gone

Phase 2 deferred this sweep to Phase 5 and it did not happen then. Done now: 19
tracked files deleted - `_config.yml`, `_includes/` (8), `_layouts/` (3),
`_sass/` (3), `css/main.scss`, and the root `index.html`, `feed.xml`, and
`about.md`. The empty `_posts/` went with them.

All superseded by `src/`. Nothing in `src/`, `.github/`, or the Eleventy config
referenced any of it - the only surviving mentions are prose, in `README.md` and
`src/style-guide.md`. `_config.yml` is inert now that Pages builds from Actions
rather than Jekyll. `_pending/`, `disentangleParGraphs/`, and `plans/` stay.

The one fact worth rescuing from the deleted tree was the Disqus shortname,
`intuitivecounter`, in `_includes/comments.html`. It is already written down in
`MigrateOldBlogs.md`, so Phase 7 loses nothing.

## 2026-08-23 - Width, revisited

`--measure` 34rem -> **51rem**, `--wide` 52rem -> **78rem** - 150% of the
original, and the header, footer, and post list follow `--measure` with it.
34rem used about a third of a 16" screen and left code cramped enough to be hard
to scan.

At 51rem prose runs roughly 110 characters, which is longer than the usual
advice. Read against real posts and kept anyway: the code is what this blog is
for. If body text ever feels like a slog to track back to the left margin, widen
only `--wide` and pull `--measure` back toward 40rem.

Code went from about 90 columns to about 136. Of the 611 code lines across the
ten posts, **550 fit before and 600 fit now**. The 11 that still scroll are 140
to 225 characters - the long signatures in `Semirings` and `Pimping-Config` -
and no plausible measure would have held them.

## 2026-08-23 - An XSLT stylesheet for the feed

`/feed.xml` rendered as a wall of raw XML, which is correct and useless to a
human who clicks "RSS" in the nav. Browsers stopped rendering feeds years ago
(Firefox 64, Safari 6), so this needs solving on the site's side.

`src/feed.xsl.liquid` -> `/feed.xsl`, pulled in by an `<?xml-stylesheet?>`
processing instruction at the top of `feed.njk`. A browser applies it and gets a
page: what a feed is, the URL to copy, a few readers worth trying, and the ten
recent posts. Feed readers ignore the PI entirely and parse the RSS underneath,
byte for byte what it was.

- It links `css/main.css` rather than carrying its own styles, so it tracks the
  palette and dark mode for free. Only `.feed-notice`, `.feed-url`, and
  `.feed-help` were added - about 15 lines.
- `doctype-system="about:legacy-compat"` on `xsl:output` is load-bearing.
  Without it the transform emits no doctype at all and the browser lays the page
  out in quirks mode, which breaks the CSS.
- XSLT attribute value templates use single braces (`href="{link}"`), which
  Liquid passes through untouched. No `{% raw %}` needed.
- Both files serve as `application/xml`, which browsers accept for a stylesheet.
  **Re-verify this on GitHub Pages** - the content type comes from its server,
  not Eleventy's, and a `text/plain` would silently disable the transform.
- Verified with `xsltproc _site/feed.xsl _site/feed.xml`, and under
  `PATH_PREFIX=/blog/`, where the PI and the CSS link both come out `/blog/...`.

**Chrome has announced it intends to remove XSLT support.** When that lands the
feed degrades to exactly today's behaviour - raw XML - and nothing breaks for
subscribers; the explanatory page just stops appearing. The replacement, if it
comes to that, is an ordinary `/subscribe/` page with the nav pointing there
instead of at the feed.

## 2026-08-23 - Phase 4 loose ends closed

- **`gh-pages` retired**, local and origin (`3ab7184`). It was fully contained in
  `master`.
- **Enforce HTTPS turned on** in Settings -> Pages.

## 2026-08-23 - OpenGraph tags

`head.liquid` had none, so a link pasted into LinkedIn or Discord rendered as a
bare URL. It now emits `og:site_name`, `og:title`, `og:description`, `og:url`,
`og:type`, `og:image` with `:width` / `:height` / `:alt`, plus
`article:published_time` and `article:author` on posts and
`twitter:card = summary_large_image` everywhere.

- **Title, description, and URL are resolved once at the top** with `assign` and
  the `default` filter, then reused by `<title>`, the meta description, and the
  og tags. They had been computed inline twice already; three more copies would
  have been the point where they drifted apart.
- **`og:type` keys off `{% if tags contains "post" %}`.** `posts.json` sets
  `tags: "post"`, and Liquid's `contains` matches both a bare string and an
  array, so this holds whichever shape Eleventy hands over. Verified: posts get
  `article`, `/about/` and `/` get `website`.
- **Every og URL is absolute**, built as `metadata.url` + `page.url | url`. A
  scraper has no document to resolve a relative URL against.
  - The first cut wrote `metadata.url | append: page.url | url`, which runs the
    `url` filter over the whole absolute string rather than over the path. It
    happened to look right at `PATH_PREFIX=/`. Split into two `assign`s.
- **Alias stubs emit no og tags**, because `alias.liquid` writes its own `<head>`
  rather than including `head.liquid`. That is correct - they are `noindex`
  redirects.
- `article:published_time` comes out as `2016-06-13T00:00:00Z`, matching the
  filename. That is the Phase 3 `timezoneOffset: 0` fix still holding.

### The card

`src/img/og-default.png`, 1200x630, generated with ImageMagick from the site
palette - `#14161a` ground, `#f0f3f7` title, `#98a1af` subtitle, a `#83b4ff`
left bar and hostname. 11.7 KB at 8-bit. `src/img/` needed a new
`addPassthroughCopy` in `eleventy.config.js`.

Regenerating it, should the wording change:

```sh
magick -size 2400x1260 xc:'#14161a' \
  -fill '#83b4ff' -draw 'rectangle 0,0 28,1260' \
  -font '/System/Library/Fonts/Supplemental/Arial Bold.ttf' -pointsize 184 -fill '#f0f3f7' \
  -annotate +180+620 'Intuitive Counter' \
  -font '/System/Library/Fonts/Supplemental/Arial.ttf' -pointsize 84 -fill '#98a1af' \
  -annotate +180+760 'A blog about Scala, AI, graphs, and coding' \
  -font '/System/Library/Fonts/Supplemental/Arial.ttf' -pointsize 68 -fill '#83b4ff' \
  -annotate +180+1090 'blog.walend.net' \
  -background '#14161a' -alpha remove -alpha off -depth 8 -strip \
  src/img/og-card-v2.png
```

**Do not add `PNG8:` to that.** See below.

ImageMagick has no `rsvg-convert` delegate on this laptop, so an SVG source
would have fallen back to its own limited renderer. Drawing directly avoids the
question.

### The subtitle was missing AI

The card came out reading "A blog about Scala, graphs, and coding". `about.md`
had said "Scala, **AI**, graphs, and coding" since it was rewritten in Phase 2,
but `metadata.js` was never updated to match, so the two had been disagreeing
about what the blog is about.

Fixed in `metadata.js` (`subtitle` and `description`), and in `package.json` and
`README.md`, which each carried their own copy of the same sentence. One string
in `metadata.description` now reaches the page meta description, `og:description`,
the feed's channel `<description>`, and `llms.txt`; `metadata.subtitle` reaches
`og:image:alt` and the card. Card regenerated.

Four hand-maintained copies of one sentence is three too many, but `package.json`
and `README.md` cannot read `metadata.js`, so this is the floor without more
machinery than it is worth.

### A path-prefix bug found while verifying, in four content links

Checking the `PATH_PREFIX=/blog/` build turned up four root-relative links in
content that never went through the `url` filter, so they pointed at `/...`
instead of `/blog/...` and **404ed on the live site**:

- `src/about.md` - "Subscribe via RSS" -> `/feed.xml`
- `2016-06-13-Pimping-Config.md` -> `/2016/05/Applying-Typesafe-Config/`
- `2016-05-20-Applying-Typesafe-Config.md` -> `/2015/06/Test-With-TypeSafeConfig/`
- `2014-10-05-Semirings.md` -> `/2014/09/graphs-in-scala/`

The last three are the cross-links Phase 5 rewrote. The journal entry there says
they were "rewritten relative"; they were rewritten to the new *scheme* but left
root-relative, which is a different thing and only breaks under a path prefix.

All four now read `{{ '/path/' | url }}`. Markdown bodies render through Liquid,
so the filter works inline. After the fix a `/blog/` build has **zero** unprefixed
root-relative `href` or `src` attributes anywhere in `_site`.

Worth remembering as a rule: **no bare root-relative URL in content or
templates.** It works in production and only in production, which is the worst
place for a bug to hide.

## 2026-08-23 - `description:` for all ten posts

One string per post now feeds three places: the page `<meta name="description">`,
`og:description`, and the feed's `<description>`. Both defects the auto-excerpt
was causing are gone - `_site/feed.xml` has zero `&amp;quot;` and zero items with
the d3 chart's CSS in the description.

**Five were lifts, not drafts.** Those posts open with a `TL/DR -` line written
for exactly this purpose, and stripped of their markdown links they came out at
93 to 157 characters - already the right size. `Easy-Parallel`'s ran long and was
compressed; `Test-With-TypeSafeConfig` and `Applying-Typesafe-Config` had the
library name capitalised as "TypeSafe Config" to match the post titles, since the
body had it as link text in lower case.

**Five had no TL/DR and were drafted**, and are the ones worth a second read:
`back-in`, `graphs-in-scala`, `Semirings`, `Enron-Thing`, and
`escape-from-inner-trait`. They are a stranger's summary of your own posts until
you have looked at them.

All ten land between 93 and 158 characters. Roughly 155 is where Google starts
truncating a meta description and LinkedIn shows less than that, so anything much
longer gets cut mid-sentence in the place it matters most.

Posts still needing this treatment: the four from Phase 6.

## 2026-08-23 - The card was blurry on LinkedIn

Discord rendered the card correctly. LinkedIn rendered it badly, and the cause
was an optimisation I made when the card was first generated.

The first version was written through `PNG8:`, which quantises to a palette. It
took the image from 55 KB to 11.9 KB - and from thousands of colours to **73**.
Light antialiased text on a dark ground is almost entirely intermediate greys;
73 colours across the whole image leaves the glyph edges stepped rather than
smooth. On a page at full size that is hard to see. After a platform downscales
it and re-encodes it as JPEG, the stepping becomes mush.

Saving 43 KB on an image that is fetched once per shared link and cached was
never worth anything. It was optimising the wrong axis.

The replacement is rendered at **2400x1260** - twice the linear size, so a
platform that downscales has real pixels to work from - in full 24-bit colour.
734 colours, 64 KB. Alpha is removed as well (`-alpha remove -alpha off`): the
render came out `TrueColorAlpha`, and a transparent channel is a known way to get
odd results out of a scraper that flattens to JPEG.

`og:image:width` and `og:image:height` in `head.liquid` were updated to match.
They have to describe the actual file or scrapers reserve the wrong space.

### Vector is not an option here

The obvious thought is to ship an SVG and let each platform rasterise at whatever
size it needs. No scraper does this. LinkedIn, Discord, Facebook, and X all
require a raster `og:image` and will ignore or fail on an SVG. The nearest
equivalent is what is done above: keep the source resolution high enough that
their downscale is the only resampling step.

If it is still soft in the LinkedIn feed after this, the next lever is type size
rather than resolution - the card renders small there, and 84px of subtitle at
2400 wide is about 19px once LinkedIn is done with it.

## 2026-08-23 - Renamed the card to bust LinkedIn's media cache

The 2400x1260 card deployed and was verified live - `curl` on
`/blog/img/og-default.png` returned the new file, 734 colours, TrueColor, 64 KB,
with `og:image:width` / `:height` on the page declaring 2400 and 1260 to match.
LinkedIn still showed the blurry one.

So the stale image was on LinkedIn's side. Post Inspector re-scrapes a page's
metadata, but the image itself was copied to `media.licdn.com` when it first
fetched the 73-colour version, and re-inspecting does not replace that stored
asset.

Renamed `og-default.png` -> `og-card-v2.png`, which makes it a new asset to them.
References updated in `head.liquid`, `README.md`, this file's recipe, and the
plan's Phase 11 entry.

**This name is temporary.** There is a note at the tail of the plan to change it
back, and the reason it exists at all is a cache on someone else's server rather
than anything about the file. Left alone, `v2` invites a `v3`.

No TTL is published for that cache, which is why the rename was worth doing
rather than waiting it out. Note also that Phase 9 moves the site to
`blog.walend.net` - every preview cache keys on URL, so the cutover clears all of
this regardless.
