---
layout: post
title: "GraphViz Class Diagrams"
date: 2005-08-11
permalink: /archive/2005/08/graphviz-class-diagrams/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2005/08/graphviz_class.html
javanetTopics:
  - Tools
---

Last week, [Kohsuke Kawaguchi suggested](http://weblogs.java.net/blog/kohsuke/archive/2005/08/pumping_up_java.html) that we could use [GraphViz](http://graphviz.org/) to generate class diagrams automatically. This idea caught my imagination. I've been looking for a readily-available set of test data a for JDigraph, plus an excuse to invest time in digraph visualization for another project that uses SVG. Class diagrams are a great fit.

I used methods on Class to populate a [Digraph](https://jdigraph.dev.java.net/nonav/alpha-0-9-0/api/net/walend/digraph/Digraph.html) with Classes as nodes and their relationships ("extended by" and "implemented by") as edges. I used digraph iterators to cover the graph and create a [dot-formatted](http://graphviz.org/Documentation/dotguide.pdf) String. I pass the String into GraphViz' dot utility to produce an SVG picture. In the test code, I use [SVGSalamander](https://svgsalamander.dev.java.net/) to display the picture.

The project came together in three evenings. It deserves a weekend day to refactor some test code into more permanent parts, and maybe another evening or two to put it into a doclet. I hit a few snags that are worth their own blog entries, but I wanted to show the picture now. The effort is on its way to becoming a new project (under [Java Tools](http://community.java.net/javatools/) as soon as I think of a good name). The [test code](https://jdigraph.dev.java.net/source/browse/jdigraph/v2/source/tographviz/net/walend/tographviz/test/) is alive in JDigraph already. It's a work in progress, but here's what one of the first class diagrams looks like:

![](https://bloggers.dev.java.net/files/documents/84/18670/classDigraph.svg)

Here's what it looks like as a gif (a little lumpy) if your browser doesn't support SVG:

![](https://bloggers.dev.java.net/files/documents/84/18669/classDigraph.gif)
