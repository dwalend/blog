---
layout: post
title: "What Giants? - Vote For My Generics RFE"
date: 2006-07-18
permalink: /archive/2006/07/what-giants-vote-for-my-generics-rfe/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2006/07/they_might_be_g.html
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

The [request for enhancement](http://bugs.sun.com/bugdatabase/view_bug.do?bug_id=6448707) made it into Sun's database. That whooshing sound may not be a windmill after all.

If you can spare a bug vote, please [vote for this RFE](http://bugs.sun.com/bugdatabase/view_bug.do?bug_id=6448707). Judging by the evaluation from Sun's engineer, this RFE needs some votes raising it up so the Sun language giants might spot it.

The RFE will also need some good rational discussion. I held back my irrelevant knee-jerk reaction -- "Didn't we all out-grow one-letter-variables when we traded our PETs for C-64s?" I could send a link to [an old blog](http://weblogs.java.net/blog/dwalend/archive/2004/12/naming_generic_1.html), but even that might distract from the cause.
Please keep in mind that we want these folks to do us a favor. I'm working on a response that frames the RFE as "encapsulation vs. exposure," to dispel the "inference vs. explicitness" suggestion.
