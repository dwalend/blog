---
layout: post
title: Overcoming My Implicit Suspicions
comments: True
---

TL/DR - I'm very suspicious of Scala's implicits and the pimp pattern. I pimped Typesafe Config's Config class to handle case class apply() constructors and Options. I pimped my undirected graph class to correct results for Brandes' algorithm. Maybe I'm getting over it. 

# Explicit Implicit

Before I read Pragmatic Programmer I knew I wanted to make my programs transparent and easy to understand. Thomas and Hunt have a section devoted to ["Explicit Programming,"](https://pragprog.com/the-pragmatic-programmer/extracts/coincidence) the idea of making a piece of code as clear and non-magical possible. Scala's implicits seem like an anathema of that goal. I've mostly avoided implicits, and mostly regretted it when I haven't.

# I Wish Typesafe Config Knew About Scala

I like Typesafe Config. However, it's in Java so the API is awkwardly broad. Config was pulled out of Akka; it shouldn't seem so alien. To support primitives the Config object has a herd of narrowly-typed get*() methods. To use Config I'm expected to pull out ints and booleans and Strings, and, piece-by-piece, collect little parts. I wish it had more of a Scala-style API, something that would let me hand in a higher order function and give me back a finished whole instance of things I do care about. 

I could use the pimp pattern to get what I want.

# Pimp Pattern

Scala offers the [Pimp Pattern](https://coderwall.com/p/k_1jzw/scala-s-pimp-my-library-pattern-example) to add API to classes we don't control. I was suspicious. One thing I like in Scala is that I don't need the [Gang-of-Four Pattern Book](http://alvinalexander.com/scala/how-scala-killed-oop-strategy-design-pattern#What_about_those_other_OOP_design_patterns); after 20 years of Java I've had enough patterns. [Pimps are comic bad guys in B movies](https://en.wikipedia.org/wiki/Doctor_Detroit). The Pimp Pattern relies on [implicits](http://twitter.github.io/effectivescala/#Types and Generics-Implicits), which seem like a good way to make spaghetti code, far from my explicit ideals. That's three bad smells before I've even started.

I tried it despite my misgivings. I pimped Config. I added higher order functions to make getters to give me the actual parts I care about instead of just primitives. To use it I still explicitly import the parts. The rest just works:

    import net.shrine.config.ConfigExtensions
    ...
    val config: Config = ConfigFactory.load("shrine")
    val keyStoreDescriptor = config.getConfigured("shrine.keystore",KeyStoreDescriptor(_))

KeyStoreDescriptor's companion object has an [apply(Config)](http://dwalend.github.io/blog/2016/05/20/Applying-Typesafe-Config.html) method that makes a KeyStoreDescriptor. I ask Config for what I want through very clean, very intuitive code. 

Here's the code for ConfigExtensions:

    package net.shrine
    
    import com.typesafe.config.Config
    
    package object config {
    
      implicit class ConfigExtensions(self: Config) {
    
        def get[T](key:String,construct:String => T):T = construct(self.getString(key))
    
        def getConfigured[T](key: String, constructor: Config => T): T = constructor(self.getConfig(key))
        ...
      }

The implicit class has to exist inside another class or object definition or else the compiler growls about an `implicit' modifier cannot be used for top-level objects'. However, the package object works fine and gets the class into a natural namespace, only one step from explicitly having ConfigExtensions in its own file. (Other people seem to use a class or a trait as a namespace to hold the implicit class. The class approach tempts coders into using a wildcard import, hiding the magical pimp behind more smoke and another mirror. Extending the trait to get access to methods in a class' context seems to make the class claim to essentially be something it isn't, inviting an OO tangle.) 

I'm half-tempted to suggest a Scala language fix to let the implicit class just be part of a package instead of junking up my package object. I want a better understanding of why things are done this way first.

# Code Caught Between

For a directed graph [Brandes' Algorithm](http://dwalend.github.io/Disentangle/v0.2.1/#net.walend.disentangle.graph.semiring.Brandes$) counts how many times a node appears in the shortest path from one node to another. To run Brande's Algorithm on an undirected graph, convert each undirected edge into two directed edges (one each way), run the calculation, then divide the counts by two - because the algorithm finds two paths in the directed graph for every path that exists in the undirected graph. 

In [Disentangle](http://dwalend.github.io/Disentangle) the [algorithm code](http://dwalend.github.io/Disentangle/v0.2.1/#net.walend.disentangle.graph.semiring.package) is decoupled from the [graph structures](http://dwalend.github.io/Disentangle/v0.2.1/#net.walend.disentangle.graph.package). The parameters for algorithms are collections of edges and nodes, not graphs. Up until Brandes' algorithm on undirected graphs I was comfortable writing explicit, simple glue code to access lists of edges to feed the algorithms. I didn't want to force my users to convert to Disentangle's graph structures in order to access the algorithms, and didn't want parts of my algorithms escaping into the graph code. 

I trust people to convert from undirected to directed graphs; mistakes will give spectacular wrong answers. However, Brandes' "finally divide the results by two" would be easy to leave out; betweenness would still just be a big Map from nodes to unintuitive numbers. I had no good place to hang the divide-by-two correction.

# Return of the Pimp

That pimp pattern let me inject a new method on the undirected graph trait; using Brandes' algorithm looks like just another method call:

    package net.walend.disentangle.examples

    import net.walend.disentangle.graph.semiring.Brandes.BrandesSteps
    import net.walend.disentangle.graph.semiring.LabelUndigraphSemiringAlgorithms
    import net.walend.disentangle.graph.{AdjacencyLabelUndigraph, NodePair}

    object BrandesImplicitsExample {
      val edges: Seq[(NodePair[String], String)] = Seq(
        (NodePair("A","B"),"ab"),
        ...
        )

      val nodeOrder = Array("A","B","C","D","E","F","H")

      val graph = AdjacencyLabelUndigraph(edges,nodeOrder)

      val brandesResults = graph.allLeastPathsAndBetweenness()
      ...
      val betweennessValues: Map[String, Double] = brandesResults._2
    }

The [code](https://github.com/dwalend/Disentangle/blob/master/graph/src/main/scala/net/walend/disentangle/graph/semiring/package.scala) looks like this:

    package object semiring {
    ...
    
      implicit class LabelUndigraphSemiringAlgorithms[Node,Label](self: LabelUndigraph[Node,Label]) {
        ...
        def allLeastPathsAndBetweenness[CoreLabel, Key]( coreSupport: SemiringSupport[CoreLabel, Key] = FewestNodes,
                                                         labelForEdge: (Node, Node, Label) => CoreLabel = FewestNodes.edgeToLabelConverter): (IndexedSeq[(Node, Node, Option[BrandesSteps[Node, CoreLabel]])], Map[Node, Double]) = {
          val digraphResult = self match {
            case indexed:IndexedLabelDigraph[Node,Label] => Brandes.allLeastPathsAndBetweenness(indexed.edges,indexed.nodes.asSeq,coreSupport,labelForEdge)
            case _ => Brandes.allLeastPathsAndBetweenness(diEdges,coreSupport = coreSupport,labelForEdge = labelForEdge)
          }
          correctForUndigraph(digraphResult)
        }
        ...
        def diEdges: GenTraversable[(Node, Node, Label)] = {
          self.edges.map(e => (e._1._1,e._1._2,e._2)) ++ self.edges.map(e => (e._1._2,e._1._1,e._2))
        }
    
        def correctForUndigraph[CoreLabel](digraphResult: (IndexedSeq[(Node, Node, Option[BrandesSteps[Node, CoreLabel]])], Map[Node, Double])) = {
          val halfMap = digraphResult._2.map(x => (x._1,x._2/2))
          (digraphResult._1,halfMap)
        }
      }
      ...     
    }

Again I put the implicit class in the package object to keep it in what feels like the right namespace. That code seems OK, so I added methods for other algorithms, did the same for directed graphs, and released it as [Disentangle 0.2.1](https://github.com/dwalend/Disentangle). 

I'm still openly suspicious of implicits. I wouldn't want to work with a whole library magically tacked together this way. However, using the pimp pattern to contain methods that would otherwise be drifting around in unrelated, undiscoverable code seems OK so far.
