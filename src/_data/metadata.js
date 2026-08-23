// SITE_URL overrides the absolute base URL used in the feed, sitemap, and
// llms.txt, for builds served from somewhere other than the production domain.
export default {
  title: "Intuitive Counter",
  subtitle: "A blog about Scala, AI, graphs, and coding",
  description: "David Walend's blog about Scala, AI, graphs, and coding",
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
