---
layout: page.liquid
title: Style Guide
permalink: /style-guide/
eleventyExcludeFromCollections: true
description: Typography and code specimen used to check the theme.
---

A specimen page for checking the theme. Not listed in the post index or the feed.

## Prose

Body text sits at a 34rem measure so a line lands near 65 characters. A reader
who has explicitly asked for a light theme gets one; everyone else gets dark,
including anyone whose system is set to "no preference". Inline code such as
`Semiring[Label, Key, Node]` sits in the run of text, and a long unbroken
identifier like `net.walend.disentangle.graph.semiring.Dijkstra` should wrap
rather than push the page sideways.

> A blockquote, for the many posts here that lean on one.
> Tim Berners-Lee's "Principle of Least Power" turns up more than once.

### Lists

- First item
- Second item, longer, so it wraps onto a second line and the indentation of the
  continuation can be checked against the bullet
- Third

1. Ordered
2. Also ordered

## Scala

```scala
implicit class ConfigPimp(config: Config) {
  def getOption[T](path: String)(implicit reader: ConfigReader[T]): Option[T] =
    if (config.hasPath(path)) Some(reader.read(config, path)) else None
}

case class Digraph[Node, Label, Key](edges: Seq[(Node, Node, Label)]) {
  def shortestPaths(start: Node): Map[Node, Label] = ???
}
```

## JSON

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          { "type": "command", "command": "afplay /System/Library/Sounds/Glass.aiff &" }
        ]
      }
    ]
  }
}
```

## A very wide line

```scala
def parBrandes[Node, CoreLabel, Label, Key](labelDigraph: IndexedLabelDigraph[Node, Label], support: SemiringSupport[CoreLabel, Key]): (Seq[(Node, Node, Label)], Map[Node, Double]) = ???
```

## Table

| Source | Count | Phase |
| --- | --- | --- |
| Jekyll `_posts/` | 10 | 5 |
| Hashnode | 4 | 6 |
| java.net via wayback | ~37 | 10 |
