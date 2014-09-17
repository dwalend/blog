---
layout: post
title: Generics and Semirings and Knocking Over Windmills
comments: True
---

# Generics and Semirings and Knocking Over Windmills

One of the coolest things you can do with graphs is find the shortest paths between nodes. One of the coolest things you can do with those algorithms is change what "shortest" means using semirings. It's so cool it makes group theory useful. Scala's type system is rich enough to handle all that without hurting my eyes, so I did it in [ScalaGraphMinimizer](https://github.com/dwalend/ScalaGraphMinimizer). 

# Type Families and Semirings

My biggest frustration with trying to define semirings in Java was that I had to carry everything around inside layered generic type specifications. There was no way to bound and encapsulate the layering. The (best-available) advice I got was to not use Java's type system that way. The only workable alternative was to cast as needed and hope it worked out at runtime. In contrast, Scala's type system handles it gracefully. Scala lets me declare a namespace of types and use those declared types where needed. Here's SemiringSupport, which is primarily about declaring types.

    trait SemiringSupport[L,Key] {
    
      type Label = L
    
      def semiring:Semiring
    
      def heapOrdering:HeapOrdering[Key]
    
      def heapKeyForLabel:Label => Key

SemiringSupport needs something to define a Label -- the things the semiring operates on, a Semiring which brings the operators, and some bits to support heaps for Dijkstra's algorithm.  

Here's Semiring's declaration, embedded inside the namespace. I think it is easy to map to the corresponding passage from Cormen’s _Algorithms_, “A general framework for solving path problems in directed graphs,” 26.4 in my 1989 copy.

      trait Semiring {
    
        /** identity */
        def I:Label
    
        /** annihilator */
        def O:Label
    
        def inDomain(label:Label):Boolean
    
        def summary(fromThroughTo:Label,current:Label):Label
    
        def extend(fromThrough:Label,throughTo:Label):Label
    
        def relax(fromThrough:Label,throughTo:Label,current:Label):Label = {
          summary(extend(fromThrough,throughTo),current)
        }   
      }
    }

With that in hand, a Semiring that counts nodes in a path was pretty simple. The Label is an Int. The heapKey is that Label. Existing edges in the graph have a Label of 1. The identity, I, is 0, and the annihilator, O, is Int.MaxValue. The summary operator picks the least Label. The extends method adds two Labels together. I did have to monkey around inside the extend method to avoid wrapping Ints.

    object FewestNodes extends SemiringSupport[Int,Int] {
    
      def semiring = FewestNodesSemiring
    
      def heapOrdering = FewestNodesHeapOrdering
    
      def heapKeyForLabel = {label:Label => label}
    
      def convertEdgeToLabel[Node, EdgeLabel](start: Node, end: Node, label: EdgeLabel): FewestNodes.Label = 1
    
      object FewestNodesSemiring extends Semiring {
    
        def I = 0
        def O = Int.MaxValue
    
        def inDomain(label: Label): Boolean = {
          I <= label && label < O
        }
    
        def summary(fromThroughToLabel:Label,
                    currentLabel:Label):Label = {
          if(fromThroughToLabel < currentLabel) {
            fromThroughToLabel
          }
          else currentLabel
        }
    
        def extend(fromThroughLabel:Label,throughToLabel:Label):Label = {
          if ((fromThroughLabel == O) || (throughToLabel == O)) O
          else {
            val result = fromThroughLabel + throughToLabel
            if(result < 0) O //Wrapped
            else result
          }
        }
      }
    
      /**
       * A heap ordering that puts lower numbers on the top of the heap
       */
      object FewestNodesHeapOrdering extends HeapOrdering[Int] {
        //uninteresting HeapOrdering
      }
    
    }

# Algorithms in Scala Can Look Like Algorithms In Text Books Even With Complex Types

Dijkstra's algorithm looks almost identical to the code from [Wikipedia](http://en.wikipedia.org/wiki/Dijkstra's_algorithm#Using_a_priority_queue):

      def dijkstraSingleSource[Node,Label,Key](initialGraph:IndexedLabelDigraph[Node,Label],
                                               support:SemiringSupport[Label,Key])
                                              (source:initialGraph.InnerNodeType):Seq[(Node,Node,Label)] = {
        //Set up an array of Labels by node index
        val labels:ArrayBuffer[Label] = ArrayBuffer.fill(initialGraph.nodeCount)(support.semiring.O)
    
        //Set up the heap
        val heap:Heap[Key,initialGraph.InnerNodeType] = new FibonacciHeap(support.heapOrdering)
    
        val heapMembers:IndexedSeq[heap.HeapMember] = initialGraph.innerNodes.map(node => heap.insert(support.heapKeyForLabel(support.semiring.O),node))
        
        //Raise sourceInnerNode's to I
        labels(source.index) = support.semiring.I
        heapMembers(source.index).raiseKey(support.heapKeyForLabel(support.semiring.I))
    
        //While the heap is not empty
        while(!heap.isEmpty) {
          //take the top node
          val topNode = heap.takeTopValue()
          //For any node that is reachable from this node 
          for(successor <- topNode.successors) {
            val heapKey = heapMembers(successor._2.index)
            //if the node has not yet been visited (because its key is still in the heap)
            if(heapKey.isInHeap) {
              //Relax to get a new label
              val label = relaxSource(initialGraph,labels,support.semiring)(source,topNode,successor)
              labels(successor._2.index) = label
              heapKey.raiseKey(support.heapKeyForLabel(label))
            }
          }
        }
    
        //put everything back together
        labels.zipWithIndex.map(x => (source.value,initialGraph.node(x._2),x._1)).filter(x => x._3 != support.semiring.O)
      }

Creating new semirings, like this one for finding the most probable path, is easy and kinda fun:

    object MostProbable extends SemiringSupport[Double,Double] {
    
      def semiring = MostProbableSemiring
    
      def heapOrdering = MostProbableOrdering
    
      def heapKeyForLabel = {label:Label => label}
    
      def convertEdgeToLabel[Node, Label](start: Node, end: Node, label: Label): MostProbable.Label = semiring.I
    
      object MostProbableSemiring extends Semiring {
    
        def I = 1.0
        def O = 0.0
    
        def inDomain(label: Label): Boolean = {
          I >= label && label > O
        }
    
        def summary(fromThroughToLabel:Label,
                    currentLabel:Label):Label = {
          if(fromThroughToLabel > currentLabel) {
            fromThroughToLabel
          }
          else currentLabel
        }
    
        def extend(fromThroughLabel:Label,throughToLabel:Label):Label = {
          if ((fromThroughLabel == O) || (throughToLabel == O)) O
          else {
            fromThroughLabel * throughToLabel
          }
        }
      }
    
      /**
       * A heap ordering that puts lower numbers on the top of the heap
       */
      object MostProbableOrdering extends HeapOrdering[Double] {
        //still not interesting 
      }

Best of all, Scala's compiler is able to work out what the types are without my help

    val labelEdges = Dijkstra.allPairsShortestPaths(testGraph.edges,testGraph.nodesSeq,FewestNodes,FewestNodes.convertEdgeToLabel)


Compare that to this eye-buringing call to Dijkstra's algorithm in JDigraph:

       Dijkstra<LeastPathLabel,
              IndexedMutableSimpleDigraph<TestBean>,
              NextStepDigraph<TestBean,LeastPathLabel,SimpleDigraph.SimpleEdge,IndexedMutableSimpleDigraph<TestBean>>,
              LeastPathComparator,
              LeastPathSemiring<TestBean,SimpleDigraph.SimpleEdge,IndexedMutableSimpleDigraph<TestBean>>> dijkstra = new Dijkstra<LeastPathLabel,
																								                      IndexedMutableSimpleDigraph<TestBean>,
																								                      NextStepDigraph<TestBean,LeastPathLabel,SimpleDigraph.SimpleEdge,IndexedMutableSimpleDigraph<TestBean>>,
																								                      LeastPathComparator,
																								                      LeastPathSemiring<TestBean,SimpleDigraph.SimpleEdge,IndexedMutableSimpleDigraph<TestBean>>>();

(Yes, the diamond operator might make this half the size. Too bad the code didn't compile in JDK7 despite being correct.)
  

# Maybe that Lance Wasn't the Right Tool for Attacking this Windmill

I'm very happy with how the code came out this early in the project. I've been able to make something both explainable and powerful, and extend it to solve for betweenness (which deserves its own blog article). It took eight weeks of a few hours after work when family and chores left me a little time, maybe 25 hours total. The code looks just like the algorithms in the book, not an example of some vile boundary case. 

Download it and try it out. In sbt, it's easy to type in a graph and try out different algorithms:

    libraryDependencies += "net.walend" %% "scalagraphminimizer" % "0.1.0"

Dave