---
layout: post
title: Renaming to Disentangle
comments: True
---

TLDR - I renamed ScalaGraphMinimizer to [Disentangle](https://github.com/dwalend/Disentangle), which better matches what the library is about. Pull in the latest snapshot with

    resolvers += "Sonatype OSS Snapshots" at "https://oss.sonatype.org/content/repositories/snapshots"

    libraryDependencies += "net.walend.disentangle" %% "graph" % "0.2.0-SNAPSHOT"

#Disentagle

I renamed ScalaGraphMinimizer to [Disentangle](https://github.com/dwalend/Disentangle). I wanted to change the name for a while. ScalaGraphMinimizer is internet-unique, but I realized during a presentation this spring that it was nearly impossible to say using a human mouth. My work with semiring-based minimization algorithms is pretty mature at this point and I'd like project to grow in new directions. While working on parallel versions of algorithms this fall I realized ScalaGraphMinimizer had outgrown its name.

I picked the name Disentangle to provide a double-meaning of optimism of purpose and guidance for the code. 

On its surface, Disentangle is a library of algorithms to help provide human insight for complex graph structures. In my day job too often I've projected a picture of a hairball of a graph on a screen in a dark room, narrating it with words like, "This graph is really complicated, but - next slide please - I found these interesting things that you may care about." Disentangle has already helped tell some stories and I plan to keep grown the library that way.

The second meaning is guidance for me creating the library and a promise to people using it. I want Disentangle to be a non-invasive library used via clean method calls, not a project-defining framework. It uses some of Scala's common-currency parts - collections and tuples - as the core of its API. Specifically it does not provide a domain-specific language or require developers to extend its internal structures.
 
The above differentiates Disentangle from its predecessors. Some structures, like lists, sets, and maps, are ubiquitus and having them in a common core library makes sense. Other structures like a [master-and-servant set of queues of AtomicMarkedReferences](https://java.net/projects/somnifugijms/sources/svn/content/trunk/source/somnifugi/net/walend/somnifugi/juc/MessageSelectingPriorityBlockingQueue.java?rev=287) are purpose-built for their specialized tasks. Graphs fall in a gap between these extremes because graphs have [a lot of lot of commonality and a lot of variation.](https://en.wikipedia.org/wiki/Graph_(mathematics)) Other graph frameworks require developers to begin by supplying graphs defined in that framework's structures. Developers who attempt to use those frameworks frequently give up when the framework doesn't meet their needs. They either rip out the old work (or - far worse - leave it gumming up the works) and replace it with something exactly customized to their own needs. 

#Graphs, Collections, and Tuples

Computers are pretty good at graphs, at least directed graphs. A general-purpose programming language with Scala's rich type system ought to provide a good starting point for general-purpose graph algorithms without demanding too much of developers. Scala - as a better Java - provides a lot of easily-accessible features through its type system. I chose those features for Disentangle's surface API. Disentangle's starting point is a collection of Tuples and a simple, single API call. It looks like this:

    /**
     * Edges are just a Seq of Tuple3[Node,Node,Edge]
     */
    val edges: Seq[(String, String, String)] = Seq(
                                                  ("A","B","ab"),
                                                  ("B","C","bc"),
                                                  ("C","D","cd"),
                                                  ("D","E","de"),
                                                  ("E","F","ef"),
                                                  ("E","B","eb"),
                                                  ("E","H","eh"),
                                                  ("H","C","hc")
                                                )
    
    import net.walend.disentangle.graph.semiring.{Dijkstra,FirstStepsTrait,AllPathsFirstSteps,LeastWeights}
    /**
     * Generate all the shortest paths in the graph
     */
    val simpleShortPathLabels: Seq[(String, String, Option[FirstStepsTrait[String, Int]])] = Dijkstra.allPairsShortestPaths(edges)

FirstStepsTrait has a Set of possible first steps to take on shortest paths, and the weight of those paths.  
  
#Semirings Inside  
  
Other frameworks get into trouble when you want to supply something beyond exactly what their algorithms can solve for. It's extremely difficult to modify what the code will do. Disentangle's implementations of the Floyd-Warshall algorithm, Dijkstra's algorithm, and Brandes' algorithm are semiring based. You can supply a different semiring. Dijkstra.allPairsShortestPaths() is a wrapper method around allPairsLeastPaths(), which takes a SemiringSupport object. The default version finds paths with the fewest nodes. Here's a code snippet from inside of object Dijkstra.

    def defaultSupport[Node] = AllPathsFirstSteps[Node,Int,Int](FewestNodes)

    def allPairsShortestPaths[Node,EdgeLabel](edges:GenTraversable[(Node,Node,EdgeLabel)],
                                          nodeOrder:GenSeq[Node] = Seq.empty
                                        ):Seq[(Node,Node,Option[FirstStepsTrait[Node, Int]])] = {
      val support = defaultSupport[Node]
      allPairsLeastPaths(edges, support, support.convertEdgeToLabel(FewestNodes.convertEdgeToLabel), nodeOrder)
    }
    
#Weights via Semirings    
    
A more specific complaint I've had with other frameworks is their baked-in selection of what to use for weights. They usually pick Doubles for weights, which is as good a choice as you can make. In contrast, Disentangle is semiring-based; you can supply the semiring, so you can use a weight that matches your needs. I created a straight-forward double-based semiring - LeastWeights - to provide traditional Double weights. It's easy to [copy and bend to your needs](https://github.com/dwalend/Disentangle/blob/to0.1.2/graph/src/main/scala/net/walend/disentangle/graph/semiring/LeastWeights.scala).

    val support: AllPathsFirstSteps[String, Double, Double] = new AllPathsFirstSteps(LeastWeights)
    
If the edges aren't Doubles already you'll need to supply some function to convert your edges to Doubles. I wrote this cheezy hack as an example.

    def stringToDouble(fromNode:String,toNode:String,edge:String):Double = edge.map(_.hashCode().toDouble).product
    
Instead of calling allPairsShortestPaths() call allPairsLeastPaths() to generate all the shortest paths.

    val leastPathLabels: Seq[(String, String, support.Label)] = Dijkstra.allPairsLeastPaths(edges,
                                                                                            support,
                                                                                            support.convertEdgeToLabel[String](stringToDouble))

Because Disentangle is semiring-based, it's possible to create your own semirings to drive the algorithms. For example, here's one for [most probable paths](https://github.com/dwalend/Disentangle/blob/to0.1.2/graph/src/main/scala/net/walend/disentangle/graph/semiring/MostProbable.scala). 

#Try it out 

Pull it into an sbt project via

    resolvers += "Sonatype OSS Snapshots" at "https://oss.sonatype.org/content/repositories/snapshots"

    libraryDependencies += "net.walend.disentangle" %% "graph" % "0.2.0-SNAPSHOT"

Or clone the project and play in the console

    git clone https://github.com/dwalend/Disentangle.git
    cd Disentangle
    sbt console
