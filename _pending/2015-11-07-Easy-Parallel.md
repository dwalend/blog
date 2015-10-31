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

Scala 2.?? provided [parallel versions of many of its standard collection classes](http://docs.scala-lang.org/overviews/parallel-collections/overview.html). Functional operations on these collections happen in parallel using a default compute pool ??? . Dijkstra's and Brandes' algorithms can be run in parallel for each node. All I needed to do was run functional operations on a parallel collection of nodes to use all the cores available.

#Fifteen Minutes Later

I needed about ten minutes for the first pass, and five for a second pass (Brandes' has an extra wrinkle), while riding on the T, to get the algorithms running in parallel. Here's a code fragment from Dijkstra's algorithm:

    def parAllPairsLeastPaths[Node,EdgeLabel,Label,Key](edges: GenTraversable[(Node, Node, EdgeLabel)],
                                                        support: SemiringSupport[Label, Key],
                                                        labelForEdge: (Node, Node, EdgeLabel) => Label,
                                                        nodeOrder: GenSeq[Node] = ParSeq.empty):ParSeq[(Node, Node, Label)] = {
      val labelDigraph = createLabelDigraph(edges.par, support, labelForEdge, nodeOrder.par)

      //profiler blames both flatten and fold of IndexedSet as trouble
      labelDigraph.innerNodes.to[ParSeq].flatMap(source => dijkstraSingleSource(labelDigraph, support)(source))
    }

Making the edges collection parallel speeds up translating to the internal directed graph representation. The bigger benefit, running dijkstraSingleSource in parallel, comes from making the nodes parallel. 

#Results on an EC2 R3

I spun up an AWS EC2 R3 instance to benchmark on modern multicore hardware. (A quick experiment on an AWS E2 C4 showed that the system was memory-bound.) That part was easy. Drawing nice graphs in D3 proved to be much more challenging.
 
TODO graphs 
 
As you can see, the crossover point where concurrency starts to pay off seems to be at about 100 nodes. I've also plotted the results of the Floyd-Warshall algorithm to compare with the cost of setting up and running Dijkstra's algorithm's structures. The Floyd-Warshall algorithm is better for graphs of less than ??? nodes.

I had similar results for Brandes algorithm.

TODO

#Try it out 

Pull it into an sbt project via

    resolvers += "Sonatype OSS Snapshots" at "https://oss.sonatype.org/content/repositories/snapshots"

    libraryDependencies += "net.walend.disentangle" %% "graph" % "0.2.0-SNAPSHOT"

Or clone the project and play in the console

    git clone https://github.com/dwalend/Disentangle.git
    cd Disentangle
    sbt console
