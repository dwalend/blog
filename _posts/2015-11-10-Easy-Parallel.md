---
layout: post
title: Parallel Disentangle
comments: True
---

<script type="text/javascript" src="../../../../disentangleParGraphs/js/d3.v3.js">
</script>

<script type="text/javascript" src="../../../../disentangleParGraphs/js/queue.js">
</script>

<script type="text/javascript" src="../../../../disentangleParGraphs/js/plot.js">
</script>

<style type="text/css">

    path {
    stroke-width: 2;
    fill: none;
    }

    .axis path,
    .axis line {
    fill: none;
    stroke: black;
    shape-rendering: crispEdges;
    }

    .axis text {
    font-family: sans-serif;
    font-size: 10px;
    }
</style>


TL/DR - I added parallel versions of Dijkstra's and Brandes' algorithms to Disentangle. Writing the code was easy. Consider using  parallel versions of these algorithms when you've got more than about 100 nodes in your graph and you have computational power to spare. Call them via

    val simpleShortPathLabelsFromPar = Dijkstra.parAllPairsShortestPaths(edges)

    val leastPathLabelsFromPar = Dijkstra.parAllPairsLeastPaths(edges,support,labelForEdge)

    val shortestPathsAndBetweennessFromPar = Brandes.parAllLeastPathsAndBetweenness(edges)

Pull in the latest snapshot with

    resolvers += "Sonatype OSS Snapshots" at "https://oss.sonatype.org/content/repositories/snapshots"

    libraryDependencies += "net.walend.disentangle" %% "graph" % "0.2.0-SNAPSHOT"


## Scala's Parallel Collections

Scala 2.9 provided [parallel versions of many of its standard collection classes](http://docs.scala-lang.org/overviews/parallel-collections/overview.html). Functional operations on these collections happen in parallel using a default compute pool. Dijkstra's and Brandes' algorithms can be run in parallel for each node. Aleksandar Prokopec provided some encouraging advice - all I needed to do was run the outermost functional operations on a parallel collection of nodes to use all the cores available. 

## Fifteen Minutes Later

I needed about ten minutes for the first pass, and five for a second pass ([Brandes' algorithm has an extra wrinkle](http://dl.acm.org/citation.cfm?id=2442521)) to get the algorithms running in parallel. Here's a code fragment from Dijkstra's algorithm:

    def parAllPairsLeastPaths[Node,EdgeLabel,Label,Key](edges: GenTraversable[(Node, Node, EdgeLabel)],
                                                        support: SemiringSupport[Label, Key],
                                                        labelForEdge: (Node, Node, EdgeLabel) => Label,
                                                        nodeOrder: GenSeq[Node] = ParSeq.empty):ParSeq[(Node, Node, Label)] = {
      val labelDigraph = createLabelDigraph(edges.par, support, labelForEdge, nodeOrder.par)

      //profiler blames both flatten and fold of IndexedSet as trouble
      labelDigraph.innerNodes.to[ParSeq].flatMap(source => dijkstraSingleSource(labelDigraph, support)(source))
    }

Making the edges collection parallel speeds up translating to the internal directed graph representation. The bigger benefit, running dijkstraSingleSource for each node in parallel, comes from putting the nodes in a parallel collection. This code was so straight-forward that I wrote it while bouncing on the T on my way home from work.

## Results on an AWS EC2 r3.8xlarge

I spun up an AWS EC2 r3.8xlarge instance to benchmark on a quiet, modern, multicore computer with a quarter-terabyte of ram. Running the benchmarks was easy. I spent most of my developer time tweaking these performance graphs in D3.
 
<div id="linearDijkstra" align="center"></div>
<script type="text/javascript">
plot3Results(false,"#linearDijkstra","../../../../disentangleParGraphs/results/dijkstra.csv","../../../../disentangleParGraphs/results/parDijkstra.csv","../../../../disentangleParGraphs/results/floydWarshall.csv")
</script>
 
The right half of this graph shows deviation from correct curves for Dijkstra's algorithm after about 4096 nodes. I think that's the garbage collector coming into play. (Lower is faster.) The r3.8xlarge let me use 238 GB for the JVM, which ran Dijkstra's algorithm on graphs with 16384 nodes before crashing into an out-of-memory error. I was expecting the parallel version of the algorithm to fill up memory faster than the serial version, but was pleasantly surprised that they ran out of memory on the same-sized graph. The parallel version found shortest paths for 16384 nodes in just over 15 minutes, about a 6X speedup over the serial version. 
 
(You'll notice the curve for the Floyd-Warshall algorithm arcing up quickly from the lower left. The Floyd-Warshall test didn't crash; I had a spare half-hour of compute time after one of the larger tests and stopped it after that.)  
 
<div id="logDijkstra" align="center"></div>
<script type="text/javascript">
plot3Results(true,"#logDijkstra","../../../../disentangleParGraphs/results/dijkstra.csv","../../../../disentangleParGraphs/results/parDijkstra.csv","../../../../disentangleParGraphs/results/floydWarshall.csv")
</script>

To examine what was happening in that lower left corner I plotted the results log/log. (A little lower is much faster.) As you can see, the crossover point where concurrency starts to pay off seems to be at about 90 nodes (on a quiet AWS r3.8xlarge with 32 cores and 244 GB ram - YMMV). The Floyd-Warshall algorithm was never better for graphs with 32 or more nodes.

I found similar results for Brandes algorithm.

<div id="linearBrandes" align="center"></div>
<script type="text/javascript">
plot2Results(false,"#linearBrandes","../../../../disentangleParGraphs/results/brandes.csv","../../../../disentangleParGraphs/results/parBrandes.csv")
</script>

<div id="logBrandes" align="center"></div>
<script type="text/javascript">
plot2Results(true,"#logBrandes","../../../../disentangleParGraphs/results/brandes.csv","../../../../disentangleParGraphs/results/parBrandes.csv")
</script>

You can see some inefficiency - maybe the JVM garbage collector - start to come into play after about 4096 nodes, but it was able to find all shortest paths and betweenness for every node in just over 15 minutes for 16384 nodes on an EC2 r3.8xlarge. That's about a 6X speed-up over non-parallel. Not bad for 15 minutes of effort with no regard for [Amdahl's law](https://en.wikipedia.org/wiki/Amdahl%27s_law).

## Try it out 

Pull it into an sbt project via

    resolvers += "Sonatype OSS Snapshots" at "https://oss.sonatype.org/content/repositories/snapshots"

    libraryDependencies += "net.walend.disentangle" %% "graph" % "0.2.0-SNAPSHOT"

Or clone the project and play in the console

    git clone https://github.com/dwalend/Disentangle.git
    cd Disentangle
    sbt console
