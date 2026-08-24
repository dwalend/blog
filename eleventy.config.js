import pluginRss from "@11ty/eleventy-plugin-rss";
import pluginSyntaxHighlight from "@11ty/eleventy-plugin-syntaxhighlight";

export default function (eleventyConfig) {
  // Prism at build time. No syntax-highlighting JavaScript reaches the browser.
  eleventyConfig.addPlugin(pluginSyntaxHighlight);

  // Eleventy disables markdown-it's indented code blocks by default. The posts
  // migrated from Jekyll use them throughout, and without this their code
  // renders as paragraphs.
  eleventyConfig.amendLibrary("md", (md) => {
    md.enable("code");

    // Slugged ids on every heading, so a post can link to its own sections.
    // markdown-it exposes the renderer rule directly, so this needs no plugin.
    // The slug comes from the heading's rendered text, not its source, or a
    // heading like `## [SHRINE](https://...)` would drag the URL into the id.
    md.renderer.rules.heading_open = (tokens, idx, options, env, self) => {
      const text = (tokens[idx + 1].children || [])
        .filter((t) => t.type === "text" || t.type === "code_inline")
        .map((t) => t.content)
        .join("");
      const base =
        text
          .toLowerCase()
          .trim()
          .replace(/[^\p{L}\p{N}\s-]/gu, "")
          .replace(/\s+/g, "-") || "section";
      const seen = (env.headingSlugs = env.headingSlugs || new Map());
      const n = seen.get(base) || 0;
      seen.set(base, n + 1);
      tokens[idx].attrSet("id", n ? `${base}-${n}` : base);
      return self.renderToken(tokens, idx, options);
    };
  });
  // The RSS plugin pulls in the HTML base plugin, which rewrites root-relative
  // URLs in HTML output. Templates already apply the pathPrefix with the `url`
  // filter, so leave its base at "/" and let it pass those through untouched.
  eleventyConfig.addPlugin(pluginRss, { htmlBasePluginOptions: { baseHref: "/" } });

  // Render dates in UTC. Eleventy reads the date from the filename as UTC
  // midnight, so rendering in local time moves a post back a day, and across a
  // month boundary that puts the permalink in the wrong month.
  eleventyConfig.setLiquidOptions({ timezoneOffset: 0 });

  // One entry per old URL that should still resolve, flattened from the
  // `aliases` list in each post's front matter.
  eleventyConfig.addCollection("aliases", (api) =>
    api
      .getFilteredByTag("post")
      .flatMap((post) =>
        (post.data.aliases || []).map((from) => ({
          from,
          to: post.url,
          title: post.data.title,
        })),
      ),
  );

  eleventyConfig.addPassthroughCopy({ disentangleParGraphs: "disentangleParGraphs" });
  eleventyConfig.addPassthroughCopy("src/css");
  eleventyConfig.addPassthroughCopy("src/img");

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data",
    },
    // Set PATH_PREFIX when the site is served from a subdirectory.
    pathPrefix: process.env.PATH_PREFIX || "/",
    markdownTemplateEngine: "liquid",
    htmlTemplateEngine: "liquid",
    templateFormats: ["md", "liquid", "njk", "html"],
  };
}
