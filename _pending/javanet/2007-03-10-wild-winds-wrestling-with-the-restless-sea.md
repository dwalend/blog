---
layout: post
title: "Wild Winds Wrestling with the Restless Sea"
date: 2007-03-10
permalink: /archive/2007/03/wild-winds-wrestling-with-the-restless-sea/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2007/03/wild_winds_wres_1.html
---

I finally found some time to get back to the [generics saga](http://weblogs.java.net/blog/dwalend/archive/2006/05/tilting_at_the_1.html). A comment in the [feature request](http://bugs.sun.com/bugdatabase/view_bug.do?bug_id=6448707) says that wildcards should help make Semirings easier to use. This article describes what I was able to do with them, and the effect they have on the code someone using JDigraph would write. It was a bit of a disappointment. I could only use wildcards where my code did not use the type parameters. That limitation prevented them from helping with all but the simplest examples, and only eliminated the easy-to-grok type parameters. I could eliminate the type parameters a developer would understand best -- Nodes and Edges -- but left him trying to puzzle through monsters like MutableFastNodeOverlayDigraph&lt;TestBean, Boolean, IndexedMutableSimpleDigraph&lt;TestBean&gt;&gt; to make the system hang together.

Mads Torgersen & company's [JOT article](http://www.jot.fm/issues/issue_2004_12/article5/article5.pdf) gave me a good understanding of how wildcards worked. It might just be a matter of repetition, but I think I really needed to read what the compiler was up to to understand wildcard's use and limits. The core idea: if my code doesn't use a particular type parameter, I can leave it out. If my code has no warnings (and no dodgy `@SuppressWarnings("unchecked")` annotations), I can drop the type parameter and use a wildcard instead. The compiler knows enough to put the pieces together for me, or will tell me when I've blown it.

After some initial experiments, I set up a CVS branch (Subversion puts CVS to shame. Why'd we wait twenty years?) and cleaned out all of the warnings. That was no small undertaking; JDigraph's working code had eight warnings when I started, but the test code had about five hundred, mostly generics-related. My experiments had shown that warnings and wildcards don't mix at all. Cleaning out warnings ate my hobby code time for much of January.

**Algorithms First**

I started working from the end of the dependency chain forward. I started with the [Floyd-Warshall algorithm](https://jdigraph.dev.java.net/source/browse/jdigraph/v2/source/semiring/net/walend/semiring/FloydWarshall.java?rev=1.8.4.3&only_with_tag=wild&view=auto&content-type=text/vnd.viewcvs-markup) example I'd used in the bug report. Floyd-Warshall is about the simplest graph minimization algorithm there is. Initially, the class declaration looked like this:

```java
public class FloydWarshall<Node,
                                Edge,
                                Label,
                                BaseDigraph extends IndexedDigraph<Node,Edge>,
                                LabelDigraph extends IndexedMutableOverlayDigraph<Node,Label,Edge,BaseDigraph>,
                                SRing extends Semiring<Node,Edge,Label,BaseDigraph,LabelDigraph>>
```

and to use it in a test case, I had to type all of this:

```java
FloydWarshall<TestBean,
                      SimpleDigraph.SimpleEdge,
                      MostProbablePathLabel,
                      IndexedMutableSimpleDigraph<TestBean>,
                      NextStepDigraph<TestBean,MostProbablePathLabel,SimpleDigraph.SimpleEdge,
                             IndexedMutableSimpleDigraph<TestBean>>,
                      MostProbablePathSemiring<TestBean,
                                        SimpleDigraph.SimpleEdge,
                                        IndexedMutableSimpleDigraph<TestBean>>> floydWarshall
            = new FloydWarshall<TestBean,
                                  SimpleDigraph.SimpleEdge,
                                  MostProbablePathLabel,
                                  IndexedMutableSimpleDigraph<TestBean>,
                                  NextStepDigraph<TestBean,MostProbablePathLabel,SimpleDigraph.SimpleEdge,
                                      IndexedMutableSimpleDigraph<TestBean>>,
                                  MostProbablePathSemiring<TestBean,
                                                    SimpleDigraph.SimpleEdge,
                                                    IndexedMutableSimpleDigraph<TestBean>>>();
```

Floyd-Warshall should be very well suited for wildcards. It consists of three nested for loops to walk the Nodes. The loops don't use Node, Edge or Label. The algorithm just marches along the indices, calling the Semiring's relax() method.

Using wildcards, I was able to reduce the class declaration to:

public class FloydWarshall&lt;BaseDigraph extends IndexedDigraph&lt;?,?&gt;,LabelDigraph extends IndexedMutableOverlayDigraph&lt;?,?,?,BaseDigraph&gt;,SRing extends Semiring&lt;?,?,?,BaseDigraph,LabelDigraph&gt;&gt;

To use it in the test code, I had two fewer type parameters to specify:

```java
FloydWarshall<IndexedMutableSimpleDigraph<TestBean>,
                      NextStepDigraph<TestBean,MostProbablePathLabel,SimpleDigraph.SimpleEdge,
                                IndexedMutableSimpleDigraph<TestBean>>,
                      MostProbablePathSemiring<TestBean,
                                        SimpleDigraph.SimpleEdge,
                                        IndexedMutableSimpleDigraph<TestBean>>> floydWarshall
    = new FloydWarshall<IndexedMutableSimpleDigraph<TestBean>,
                          NextStepDigraph<TestBean,MostProbablePathLabel,SimpleDigraph.SimpleEdge,
                              IndexedMutableSimpleDigraph<TestBean>>,
                          MostProbablePathSemiring<TestBean,
                                            SimpleDigraph.SimpleEdge,
                                            IndexedMutableSimpleDigraph<TestBean>>>();
```

The Floyd-Warshall algorithm is pretty slow: O(nodes^3), not NP hard but like waiting for Santa. It solves general graph minimization problems, without taking advantage of any knowledge about the problem. Sometimes that's the best you can do.

However, in many problems a Semiring's summary() operator makes a choice between two paths. For those problems, Dijkstra's algorithm can do better -- O(edges +  nodes log (nodes)). In many real-world applications, O(edges) ~ O(nodes), so Dijkstra will run in O(nodes log (nodes)) time. In my implementation [Dijkstra's algorithm](https://jdigraph.dev.java.net/source/browse/jdigraph/v2/source/semiring/net/walend/semiring/Dijkstra.java?rev=1.6.4.3&only_with_tag=wild&view=auto&content-type=text/vnd.viewcvs-markup) keeps a [Fibonacci heap](https://jdigraph.dev.java.net/source/browse/jdigraph/v2/source/collection/net/walend/collection/FibHeap.java?rev=1.7&only_with_tag=wild&view=auto&content-type=text/vnd.viewcvs-markup) of Labels; the Labels can't be wildcarded away. My A* implementation hit a similar issue. The best I could do for these algorithms still had five type parameters.

```java
public class Dijkstra<Label,
                        BaseDigraph extends IndexedDigraph<?,?>,
                        LabelDigraph extends IndexedMutableOverlayDigraph<?,Label,?,BaseDigraph>,
                        Comp extends HeapComparator<Label>,
                        SRing extends PathSemiring<?,?,Label,BaseDigraph,LabelDigraph,Comp>>
```

I kept those changes in JDigraph's main branch.

**Semirings**

I was able remove Nodes and Edges from the Semiring interface. but I wasn't really happy about removing either. It's removing domain information from the Semiring, stripping away part of its mathematical definition. The code survives it because the algorithms, especially the relax method, use int indices to work with arrays inside IndexedDigraphs.

It worked for the Semiring interface and an abstract parent class, but then hit a dead end. Reachability is possibly the simplest Semiring. Its operators can determine if one Node can be reached from another. In the createLabelDigraph() method, it constructs a MutableFastNodeOverlayDigraph in which to build the solution:

```java
/**
Creates an initialized LabelDigraph. The LabelDigraph has BaseDigraph's
Nodes, initial Labels set to values from getInitialLabel().
    */
    public MutableFastNodeOverlayDigraph<?,Boolean,Edge,BaseDigraph> createLabelDigraph(BaseDigraph baseDigraph)
    {
        MutableFastNodeOverlayDigraph<?,Boolean,Edge,BaseDigraph> result
            = new MutableFastNodeOverlayDigraph<?,Boolean,Edge,BaseDigraph>(baseDigraph);
```

But you can't use a wildcard in a constructor. One fix would be to change MutableFastNodeOverlayDigraph so that the Node doesn't matter there. Unfortunately, MutableFastNodeOverlayDigraph implements Digraph&lt;Node,Edge&gt;, and implements demands real type specifiers, too. Another fix would be to pass in the MutableFastNodeOverlayDigraph in which to build the solution. That change would move this step from encapsulated inside the Semiring to outside in the developer's code. It misses the point.

However, I found a small step forward. In OverlayDigraph, the underlying Digraph's Edge's, UnderEdge, really shouldn't matter. For Reachability, that's fine. Removing Edge from Semiring and Reachability made the test code using FloydWarshall look like this:

```java
Reachability<TestBean,IndexedMutableSimpleDigraph<TestBean>> reachabilitySemiring
           = new Reachability<TestBean,IndexedMutableSimpleDigraph<TestBean>>();

        FloydWarshall<IndexedMutableSimpleDigraph<TestBean>,
                        MutableFastNodeOverlayDigraph<TestBean,Boolean,IndexedMutableSimpleDigraph<TestBean>>,
                        Reachability<TestBean,IndexedMutableSimpleDigraph<TestBean>>> floydWarshall
                        = new FloydWarshall<IndexedMutableSimpleDigraph<TestBean>,
                                            MutableFastNodeOverlayDigraph<TestBean,Boolean,IndexedMutableSimpleDigraph<TestBean>>,
                                            Reachability<TestBean,IndexedMutableSimpleDigraph<TestBean>>>();

        IndexedMutableDigraph<TestBean,Boolean> labels = floydWarshall.computeLabels(reachabilitySemiring,baseDigraph);
```

When I worked on slightly more complex semirings, where Labels are Path&lt;Node,Edge&gt;s, the Edges showed up again. LeastPathSemiring and MostProbablePathSemiring need to specify Nodes and Edges for their versions createLabelDigraph(). If that constructor hadn't caused problems, I'd have had a hard time measuring the cost to cross an Edge from one Node to another using a PathMeter that didn't know the type to use for Node or Edge.

The best I was able to do to use AStar using LeastPathSemiring using wildcards was this:

```java
LeastPathSemiring<TestBean,SimpleDigraph.SimpleEdge,IndexedMutableSimpleDigraph<TestBean>> shortestLabelsSemiring
            = new LeastPathSemiring<TestBean,SimpleDigraph.SimpleEdge,IndexedMutableSimpleDigraph<TestBean>>(new TestPathMeter());
        AStar<LeastPathLabel,
                      IndexedMutableSimpleDigraph<TestBean>,
                      NextStepDigraph<TestBean,LeastPathLabel,SimpleDigraph.SimpleEdge,IndexedMutableSimpleDigraph<TestBean>>,
                      LeastPathComparator,
                      LeastPathSemiring<TestBean,SimpleDigraph.SimpleEdge,IndexedMutableSimpleDigraph<TestBean>>> aStar
                        = new AStar<LeastPathLabel,
                                    IndexedMutableSimpleDigraph<TestBean>,
                                    NextStepDigraph<TestBean,LeastPathLabel,SimpleDigraph.SimpleEdge,IndexedMutableSimpleDigraph<TestBean>>,
                                    LeastPathComparator,
                                    LeastPathSemiring<TestBean,SimpleDigraph.SimpleEdge,IndexedMutableSimpleDigraph<TestBean>>>(new LeastPathEstimator());
```

Wildcards just don't make that much difference when a developer tries to use the generic algorithms. I really want a way to encapsulate all the complexity inside the Semiring, then pull it out inside the algorithm code. I want something like [this](http://weblogs.java.net/blog/dwalend/archive/2006/05/index.html).

There is some hope, though. Peter AhÃ©'s blogged that it's time to [erase erasure](http://blogs.sun.com/ahe/entry/reification). That effort might open up the type specifiers for use at compile time. My next stop is the [kitchen sink language project](https://ksl.dev.java.net/?redirect=SSL) to see what's in progress and maybe lend a hand. I've at least got a monster unit test for them.

In my ears (in my head at this point): Yuja Wang playing Tchaikovsky's Opus 23. Flat out amazing.
