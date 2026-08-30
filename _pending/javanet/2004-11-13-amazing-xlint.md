---
layout: post
title: "Amazing -Xlint"
date: 2004-11-13
permalink: /archive/2004/11/amazing-xlint/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2004/11/amazing_xlint.html
---

I've been reorganizing JDigraph to take advantage of generics. I've been able to implement generic versions of Floyd-Warshall and Dijkstra's algorithms -- hopefully using generics means doing this for the last time. I want to highlight -Xlint, a JDK 5 feature that's saved me a lot of grueling code reads as I've learned generics. I wish I'd found it sooner.

My common-build.xml file's javac task now looks like

```java
<javac srcdir="${src}" excludes="**/test/**" destdir="${assembly}" deprecation="yes" debug="yes" >
   <compilerarg value="-Xlint" />
   <classpath>
     <path refid="compile-classpath"/>
   </classpath>
  </javac>
```

. The output looks like this:  

```java
    [javac] /Users/dwalend/projects/opensource/jdigraph/v2/source/grid/net/walend

/grid/AbstractArrayGrid2D.java:46: warning: [unchecked] unchecked cast

    [javac] found   : java.lang.Object[][]

    [javac] required: Elem[][]

    [javac]         array = (Elem[][])new Object[sizeI][sizeJ];

    [javac]                           ^
```

The feature pointed out a few hundred spots where I hadn't specified types on my first "make it work" pass. lint made short work of the clean-up pass. Further, lint pointed out places that needed some more thought, and helped keep me honest. I've fielded a lot of questions about generics over the last six weeks; none of the people asking had found -Xlint. Try it out. I found it more useful than any of the tutorials.
