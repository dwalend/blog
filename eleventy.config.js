import pluginRss from "@11ty/eleventy-plugin-rss";
import pluginSyntaxHighlight from "@11ty/eleventy-plugin-syntaxhighlight";

export default function (eleventyConfig) {
  // Prism at build time. No syntax-highlighting JavaScript reaches the browser.
  eleventyConfig.addPlugin(pluginSyntaxHighlight);
  eleventyConfig.addPlugin(pluginRss);

  // The d3 plots from the 2015 Disentangle posts, copied as they are.
  eleventyConfig.addPassthroughCopy({ disentangleParGraphs: "disentangleParGraphs" });
  eleventyConfig.addPassthroughCopy("src/css");

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data",
    },
    // "/" once blog.walend.net is live. The interim deploy at
    // dwalend.github.io/blog needs PATH_PREFIX=/blog/ instead.
    pathPrefix: process.env.PATH_PREFIX || "/",
    markdownTemplateEngine: "liquid",
    htmlTemplateEngine: "liquid",
    templateFormats: ["md", "liquid", "html"],
  };
}
