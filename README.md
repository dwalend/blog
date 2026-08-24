# Intuitive Counter

David Walend's blog about Scala, AI, graphs, and coding — <https://blog.walend.net>

## Stack

[Eleventy](https://www.11ty.dev/) 3.x, building Markdown and Liquid into static
HTML, deployed to GitHub Pages. Syntax highlighting runs at build time through
Prism, so no JavaScript is shipped to the browser for it.

## Building

```sh
npm ci
npm run serve     # local preview with live reload
npm run build     # one-shot build into _site/
```

Two environment variables control where the site thinks it lives:

| Variable | Default | Use |
| --- | --- | --- |
| `SITE_URL` | `https://blog.walend.net` | Absolute URLs in the feed, sitemap, and llms.txt |
| `PATH_PREFIX` | `/` | Set to `/blog/` when deploying to `dwalend.github.io/blog` |

```sh
PATH_PREFIX=/blog/ SITE_URL=https://dwalend.github.io npm run build
```

## Layout

```
src/
├── _data/metadata.js   site metadata (replaces Jekyll's _config.yml)
├── _includes/          layouts and partials, in Liquid
├── posts/              published posts; posts.json sets their shared defaults
├── css/main.css
├── img/og-card-v2.png  the site-wide OpenGraph card
├── index.liquid
├── feed.njk            RSS; the one Nunjucks template, for the RSS plugin's filters
├── feed.xsl.liquid     XSLT so browsers show the feed as a page, not raw XML
├── robots.txt.liquid   generated
├── sitemap.xml.liquid  generated
└── llms.txt.liquid     generated from the post list
_pending/               drafts, not built
disentangleParGraphs/   d3 plots from the 2015 Disentangle posts
plans/                  the restart and migration plans
```

Posts get permalinks of the form `/YYYY/MM/slug/`. Older URLs from the 2014–2016
Jekyll site and the 2024 Hashnode site are preserved with redirect stubs.

## Deploying

GitHub Actions builds and deploys to GitHub Pages on push to `master`. The
workflow reads `PATH_PREFIX` and `SITE_URL` from the Pages configuration, so it
works unchanged at `dwalend.github.io/blog` and at the custom domain later.

## License

Three different things live here, under three different terms:

- **Posts and prose** — [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
  Quote, translate, mirror, and syndicate freely; attribution is all that is asked.
  The RSS feed carries full post text precisely so that this is easy.
- **Code samples inside posts** — public domain. Copy them into your own work with
  no attribution and no obligation.
- **The site's own machinery** — Eleventy config, templates, CSS — [MIT](LICENSE).

Crawlers are welcome, AI systems included. See [`src/robots.txt.liquid`](src/robots.txt.liquid).

### Third-party code

`disentangleParGraphs/js/` vendors two of Mike Bostock's libraries, both
BSD-3-Clause, with their license headers restored in the files themselves:

- [d3](https://d3js.org/) 3.5.6 — Copyright (c) 2010-2015, Michael Bostock
- [d3-queue](https://github.com/d3/d3-queue) 1.0.7 — Copyright (c) 2012-2016, Michael Bostock
