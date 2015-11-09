---
layout: post
title: Parallel Disentangle
comments: True
---

TLDR - I added parallel versions of Dijkstra's and Brandes' algorithms to Disentangle. Writing the code was easy. Consider using the parallel versions when you've got more than about 100 nodes in your graph. Call them via

    val simpleShortPathLabelsFromPar = Dijkstra.parAllPairsShortestPaths(edges)

    val leastPathLabelsFromPar = Dijkstra.parAllPairsLeastPaths(edges,support,labelForEdge)

    val shortestPathsAndBetweennessFromPar = Brandes.parAllLeastPathsAndBetweenness(edges,nodeOrder)

Pull in the latest snapshot with

    resolvers += "Sonatype OSS Snapshots" at "https://oss.sonatype.org/content/repositories/snapshots"

    libraryDependencies += "net.walend.disentangle" %% "graph" % "0.2.0-SNAPSHOT"


#Scala's Parallel Collections

Scala 2.9 provided [parallel versions of many of its standard collection classes](http://docs.scala-lang.org/overviews/parallel-collections/overview.html). Functional operations on these collections happen in parallel using a default compute pool. Dijkstra's and Brandes' algorithms can be run in parallel for each node. All I needed to do was run functional operations on a parallel collection of nodes to use all the cores available.

#Fifteen Minutes Later

I needed about ten minutes for the first pass, and five for a second pass (Brandes' has an extra wrinkle) to get the algorithms running in parallel. Here's a code fragment from Dijkstra's algorithm:

    def parAllPairsLeastPaths[Node,EdgeLabel,Label,Key](edges: GenTraversable[(Node, Node, EdgeLabel)],
                                                        support: SemiringSupport[Label, Key],
                                                        labelForEdge: (Node, Node, EdgeLabel) => Label,
                                                        nodeOrder: GenSeq[Node] = ParSeq.empty):ParSeq[(Node, Node, Label)] = {
      val labelDigraph = createLabelDigraph(edges.par, support, labelForEdge, nodeOrder.par)

      //profiler blames both flatten and fold of IndexedSet as trouble
      labelDigraph.innerNodes.to[ParSeq].flatMap(source => dijkstraSingleSource(labelDigraph, support)(source))
    }

Making the edges collection parallel speeds up translating to the internal directed graph representation. The bigger benefit, running dijkstraSingleSource in parallel, comes from making the nodes parallel. This code is so simple I wrote it on the T on my way home from work.

#Results on an EC2 R3

I spun up an AWS EC2 r3.8xlarge instance to benchmark on modern multicore hardware. (A quick experiment on an AWS E2 C4 showed that the system was memory-bound.) That part was easy. I spent a lot more time tweaking graphs in D3.
 
TODO linear graph
 
The right edge of this graph shows deviation from correct curves for Dijkstra's algorithm after 4096 nodes. I think that's the garbage collector coming in to play. The r3.8xlarge let me use 238 GB for the JVM, which ran on graphs with 16384 nodes before crashing with an out-of-memory error. You'll notice the curve for the Floyd-Warshall algorithm arcing up quickly from the lower left. (The Floyd-Warshall test didn't crash. As expected it was really slow so I stopped it once I had values for the smaller graphs.) I was expecting the parallel version of the algorithm to fill up memory faster than the serial version. I was pleasantly surprised that they failed at the same stage. The parallel version found shortest paths for 16384 nodes in just over 15 minutes, a 6X speedup over the serial version. 
 
TODO log/log graph
 
To examine what was happening in that lower left corner I plotted the results log/log. As you can see, the crossover point where concurrency starts to pay off seems to be at about 90 nodes (on a quiet 32-core r3.8xlarge - YMMV). The Floyd-Warshall algorithm was never better for graphs with 32 or more nodes.

I had similar results for Brandes algorithm.

TODO Brandes graphs

You can see the JVM garbage collector start to come into play at about 10000 nodes, but I was able to fit a graph with 16384 nodes on an EC2 r3.8xlarge, and find all shortest paths in just over 15 minutes, a 6X speed-up over non-parallel. Not bad for 15 minutes of effort with no regard for [Amdahl's law](https://en.wikipedia.org/wiki/Amdahl%27s_law).

#Try it out 

Pull it into an sbt project via

    resolvers += "Sonatype OSS Snapshots" at "https://oss.sonatype.org/content/repositories/snapshots"

    libraryDependencies += "net.walend.disentangle" %% "graph" % "0.2.0-SNAPSHOT"

Or clone the project and play in the console

    git clone https://github.com/dwalend/Disentangle.git
    cd Disentangle
    sbt console
