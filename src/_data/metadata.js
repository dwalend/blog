// Replaces Jekyll's _config.yml.
//
// SITE_URL is overridable so the pre-cutover builds at dwalend.github.io/blog
// emit correct absolute URLs in the feed. It defaults to the domain the site
// will live at once DNS moves.
export default {
  title: "Intuitive Counter",
  subtitle: "A blog about Scala, graphs, and coding",
  description: "David Walend's blog about Scala, graphs, and coding",
  url: process.env.SITE_URL || "https://blog.walend.net",
  language: "en",
  author: {
    name: "David Walend",
    email: "david@walend.net",
    github: "dwalend",
  },
  license: {
    content: {
      name: "CC BY 4.0",
      url: "https://creativecommons.org/licenses/by/4.0/",
    },
    samples: "public domain",
  },
};
