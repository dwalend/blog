import pluginRss from "@11ty/eleventy-plugin-rss";
import pluginSyntaxHighlight from "@11ty/eleventy-plugin-syntaxhighlight";

export default function (eleventyConfig) {
  // Prism at build time. No syntax-highlighting JavaScript reaches the browser.
  eleventyConfig.addPlugin(pluginSyntaxHighlight);

  // Eleventy disables markdown-it's indented code blocks by default. The posts
  // migrated from Jekyll use them throughout, and without this their code
  // renders as paragraphs.
  eleventyConfig.amendLibrary("md", (md) => md.enable("code"));
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
