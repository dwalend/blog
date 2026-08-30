---
layout: post
title: "Whooshing Sounds"
date: 2006-09-09
permalink: /archive/2006/09/whooshing-sounds/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2006/09/whooshing_sound_1.html
javanetTopics:
  - J2SE
---

Back in May I [blogged](http://weblogs.java.net/blog/dwalend/archive/2006/05/tilting_at_the_1.html) about simplifying my generics code with dot accessors to the type parameters, to simplify code that currently looks like this:

```java
public class FloydWarshall<Node,
                            Edge,
                            Label,
                            BaseDigraph extends IndexedDigraph<Node,Edge>,
                            LabelDigraph extends IndexedMutableOverlayDigraph<Node,Label,Edge,BaseDigraph>,
                            SRing extends Semiring<Node,Edge,Label,BaseDigraph,LabelDigraph>>
```

into something more like this:

```java
public class FloydWarshall<SRing extends Semiring>
```

The [request for enhancement](http://bugs.sun.com/bugdatabase/view_bug.do?bug_id=6448707) made it into Sun's database. Seven of you voted for it in as many hours. Thanks.

I also had what I think was a revealing back-and-forth with a Sun engineer. I'm a bit disappointed it ended as quickly as it did, but I hope my suggestion planted some seeds for further thought about how the Generics language features can mature. I think the dialog in the RFE makes interesting reading.
