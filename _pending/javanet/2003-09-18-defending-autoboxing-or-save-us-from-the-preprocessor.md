---
layout: post
title: "Defending Autoboxing (or Save Us From the Preprocessor)"
date: 2003-09-18
permalink: /archive/2003/09/defending-autoboxing-or-save-us-from-the-preprocessor/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2003/09/defending_autob.html
---

I plan to use autoboxing in a project, so I'm responding to [Erb Cooper's damning blog, "The Terror That Is Autoboxing."](http://weblogs.java.net/pub/wlg/447) I haven't read the spec yet -- Only JCP members have had the chance. I think we should reserve judgment at least until we can see what the [JSR expert group](http://jcp.org/en/jsr/detail?id=201) has come up with. Under the eye-catching headline, Erb's complaint is that autoboxing could create a lot of objects for no good reason, use a lot of memory, and create a lot of garbage. I hope autoboxing will be a bit more sophisticated, and that developers will use the same care they show with Strings.

I want to solve a design problem using autoboxing and generics for [JDigraph](http://jdigraph.sourceforge.net/) that I'll otherwise have to solve with a preprocessor, or Jython, or a compiler and ClassLoader hack that will basically repeat what the generics and autoboxing should do for me. I think autoboxing and generics will do the job, but won't know until I get a chance to read what the expert group has decided. I might even have to wait until the JSDK 1.5 betas are out to try it.

JDigraph's measured package has a collection of path optimization algorithms. Path optimization algorithms like Johnson's, Dijkstra's and Floyd-Warshall use a relax() procedure at their core. relax() compares the current cost to traverse between a "from" node and a "to" node to the cost of using a "through" node. The three indexes (fromIndex, throughIndex and toIndex) correspond with the nodes. safeLength() returns the lowest known cost to cross an edge between two nodes. Here's the the relax() method from AbstractShortestCEDistances.java.

```java
private int[][] distances;

    protected void relax(int fromIndex,int throughIndex,int toIndex)
    {
        int fromThrough = safeLength(fromIndex,throughIndex);
        if(fromThrough==Integer.MAX_VALUE)
        {
            return;
        }

        int throughTo = safeLength(throughIndex,toIndex);
        if(throughTo==Integer.MAX_VALUE)
        {
            return;
        }

        int startLength = Integer.MAX_VALUE;

        int fromTo = safeLength(fromIndex,toIndex);
        if(fromTo fromThrough+throughTo)
        {
            distances[fromIndex][toIndex]=fromThrough+throughTo;
        }
    }
```

Right now this code uses an int[][] for distances. I would like to use autoboxing and generics to easily switch this class from ints to doubles or other Number subclasses. A generic should generate a subclass of the parent class with the correct types, which would be very efficient. I'm hoping that autoboxing will let me keep the efficiency of primitive types while letting me access that flexibility. A profiling investigation showed that the algorithm spent most of its time assigning new distances in that last if block, so this method should be a good test of efficiency. It will be easy to measure once the JSDK 1.5 betas start to come out; I've got the timing study ready.

One alternative approach is to use a preprocessor to change the primitives. (And to rename the class so that the same ClassLoader context can use versions for different primitives). But to do that I'd have to guess what all the possible child classes of Number should be at build time. (Plus I'd need to do the same thing to my Heap for Dijkstra's algorithm. Plus all the interfaces involving path length would have to run through the same process to have the right APIs.)

A second alternative is to use string substitution, code generation, and a compiler at runtime to build the .class files I need at runtime. Defining the interfaces for these would be difficult; I'd still have to do some tricks at compile time. That work would repeat what the generics feature does already.

A third alternative is to write the code in Jython. But I expect this numeric-intensive code would be much slower. A disappointing implementation of autoboxing would run at Jython speed. (Like Erb says, "Wouldn't I be just as well off using Python?") However, it would work and I could speed it up when it's important.

I hope and expect that autoboxing will be efficient enough to let this work well, instead of just work.
