---
layout: post
title: Type Less and Type Later in Scala
---

Graphs, Now in Scala

Using my old JDigraph project, I did a lot of work with, unsurprisingly, directed graphs. I eventually hit the limit of Java's type system and [tried to punch through it.](https://weblogs.java.net/blog/dwalend/archive/2007/03/wild_winds_wres.html) I've been able to get a lot further with hardly any grief in Scala. The type system has what I need. It just worked, was fun, and (I hope) is pretty easy to explain.

I also found I could put off defining the specifics of a type until I was ready. Not having to predict the future perfectly from the outset is a huge win in object-oriented programming, and has really proven itself out over the last six months' hacking. That's something I could never do in Java.

A graph has a set of nodes and a set of edges. The edges define some kind of relationship between the nodes, but there are a lot of different possible rules for how those relationships work. [Wikipedia lists many of them](http://en.wikipedia.org/wiki/Graph_(mathematics)) . First I'll show the easy parts: I'll get to edges in a minute. A graph has a set of nodes.

trait Graph[Node] {

  def nodes:GenSet[Node]

  def nodeCount:Int

Note that I've only put in a parameter for the Node's type.  

I can get cleaner API if I use an internal representation of the nodes, similar to Java's [Map.Entry](http://docs.oracle.com/javase/8/docs/api/java/util/Map.Entry.html). This internal representation at least needs access to the node put into the graph.

  /**
   * An internal representation of nodes within the graph
   */
  trait InnerNodeTrait {
    def value:Node
  }

Here's where things get a bit interesting. I don't know what the type of that internal node is going to be. However, for a given implementation of Graph all of those internal nodes will be InnerNodeType, and they are all at least InnerNodeTraits. 

  /**
   * The type of InnerNodeTrait for this digraph representation
   */
  type InnerNodeType <: InnerNodeTrait

I'm not satisfied by the names InnerNodeTrait and InnerNodeType. Any suggestions for something better?

I'll want a way to return all the internal nodes, and get the internal node for an external node. I use the InnerNodeType in these definitions.

  /**
   * @return InnerNode representation of all of the nodes in the graph.
   */
  def innerNodes:Seq[InnerNodeType]

  /**
   * @param value a node that might be in this digraph
   * @return Some inner node if it exists in the digraph or None
   */
  def innerNode(value:Node):Option[InnerNodeType]

Defining edges is next. Someone using the API will pass in edges from the outside. Once the edges are in the Graph, it's convenient to hand back an internal representation for edges. It will eventually carry around references to inner nodes (as InnerNodeTypes.) However, I don't really know how the nodes will be related to each other yet. Therefore I declare both an OuterEdgeType and an InnerEdgeType. I don't define anything about them except that they exist. They'll have something to do with Node and InnerNodeType, but I can't say what in a way that will be useful.

  type OuterEdgeType

  type InnerEdgeType

Any help with naming? "type OuterEdgeType" is half a step from "object MyFirstScalaCode" .

I know I'll need to get back the edges, and I have just enough type information to do it.

  /**
   * @return A Traversable (usually something more specific) of the edges
   */
  def edges:GenTraversable[OuterEdgeType]

  /**
   * @return A Traversable (usually something more specific) of the edges as represented in the graph
   */
  def innerEdges:GenTraversable[InnerEdgeType]
}

I've managed to put off defining anything about edges except that edges exist, and they have an internal representation different from the external representation. The Graph class' API has committed to very little. Sub-traits can define undirected graphs with Set2[Node] for edges. directed graphs can have edges of type (Node,Node). Hypergraphs and directed hypergraphs can use Sets. Bipartite graphs can have edges just of nodes with different classes -- (Person,Job) for example. My favorite feature is that I don't have to code up any of those variations until I'm ready to use them for something.

Here's a labeled digraph example, where edges have labels:

trait LabelDigraph[Node,Label] extends Digraph[Node] {

  type OuterEdgeType = (Node,Node,Label)

  type InnerEdgeType = (InnerNodeType,InnerNodeType,Label)

  /**
   * @return the label to return when no edge exists. If Label is an Option, this will be None.
   */
  def noEdgeExistsLabel:Label

  /**
   * @return the Edge between start and end or noEdgeExistsValue if no edge connects start to end
   */
  def label(start:InnerNodeType,end:InnerNodeType):Label
}

For the first release, I settled on two implementations of LabelDigraph, MatrixLabelDigraph (to support the Floyd-Warshall algorithm) and AdjacencyLabelDigraph to support both Dijkstra's algorithm and Brandes' betweenness algorithm. 

I tried to make constructing a graph very easy, by supplying companion objects with apply methods that have default arguments:

  def apply[Node,Label](edges:GenTraversable[(Node,Node,Label)] = Seq.empty,
                       nodes:GenSeq[Node] = Seq.empty,
                       noEdgeExistsValue:Label = null) = {

So you can create a graph with a Vector of Tuple3s like this

  val yourGraph = AdjacencyLabelDigraph(edges = Vector(("A","B","ab"),("B","C","bc"),("C","A","ca"))

Download it and try it out. In sbt console, it's easy to just doodle around with graphs:

    libraryDependencies += "net.walend" %% "scalagraphminimizer" % "0.1.0"

Dave
