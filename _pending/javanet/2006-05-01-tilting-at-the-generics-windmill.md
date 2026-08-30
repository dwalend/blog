---
layout: post
title: "Tilting at the Generics Windmill"
date: 2006-05-01
permalink: /archive/2006/05/tilting-at-the-generics-windmill/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2006/05/tilting_at_the_1.html
---

I've got a quixotic streak that needs exercise every so often. It's time. I'm doing [a talk on usability problems in generics that I think can be fixed](http://wiki.java.net/bin/view/Javaone/CommunityCorner#MiniTalksSched) at 2:30 pm on Thursday in the [Java Community pavilion at JavaOne](http://wiki.java.net/bin/view/Javaone/CommunityCorner). That windmill aught to break a lance.

Just before JavaOne 2005 there was a huge dust-up over generics as people started using them, and trying to teach how they work. Ken Arnold [blogged](http://weblogs.java.net/blog/arnold/archive/2005/06/generics_consid_1.html) "Generics are a mistake... A design should have a complexity budget to keep its overall complexity under control. Generics are way out of whack." Trashing generics became the season's fashion. Chris Adamson [retorted](http://weblogs.java.net/blog/editors/archives/2005/10/broken_hearts_a.html) that we were experiencing "Buyer's remorse for Generics." After all, [JSR-14](http://jcp.org/en/jsr/detail?id=14) -- the generics proposal -- started in 1999, but did not appear in a release until JDK5 in late 2004. Any of us could play with generics in Java using the gj and pizzac compilers. We had five years to point out problems we found using the syntax. For example, borrowing C++ template syntax would look too much like XML. (If we get direct manipulation of XML, it won't look like XML. I'm not sure that's a bad thing. XML is pretty hard on the eyes. The angle brackets do make writing html about Generics or XML really painful -- &lt;s everywhere.) That's water over the dam at this point. I'd like to start a conversation about finding ways to fix the stumbling blocks we've found, targeted for Dolphin.

I like generics. I use them (and abuse them. See below) in my [JDigraph](http://jdigraph.dev.java.net) project. I wrote JSDK 1.4 code in a Digraph interface that looked like this:

```java
public Object addEdge(Object fromNode, Object toNode, Object edge) throws NodeMissingException;
```

which caused frequent `NodeMissingException`s from calls like

```java
hisDigraph.addEdge(hisFromNode, hisEdge, hisToNode);
```

. The compiler couldn't point out that the second argument was supposed to be a node and the third was supposed to be an edge. Autocompletion in IDEs, combined with some developers' habit of grabbing the top argument in the autocomplete list led to NodeMissingExceptions, confusion and frustration. In JDK 5, the code looks like this:

```java
public Edge addEdge(Node fromNode, Node toNode, Edge edge) throws NodeMissingException;
```

Just as Keys and Values in Maps are rarely of the same class, Nodes and Edges rarely share an ancestor closer than Object. The compiler helps the developers get things right. My code is much clearer to me (easier to figure out what I did) and much clearer to people trying to use it (fewer agitated developers at my office door).

One of Ken's specific complaints was about the complexity of `Enum&lt;E extends Enum&lt;E&gt;&gt;`, the abstract parent of all Java enums. This particular class interacts closely with the compiler, jumping through some high hoops to give us enums of Objects instead of short integers. It's powerful, but impossible to explain without guessing the java compiler developers' intent. The compiler will specify using your enum class for E. So

```java
public enum YourEnums
```

becomes something like

```java
public class YourEnums
    extends Enum<YourEnum>
```

so that YourEnums is always an Enum of YourEnums. To define the Enum class, it'd be great if someone at Sun could just code

```java
public abstract class Enum<E is this.getClass()>
```

and remove the guesswork. It's a corner case. I ran into something similar while I was generifying JDigraph's HasState interface. HasState provides a method to compare two objects with different representations, but share a defining principle interface that defines the interesting part of the state. For example, Digraphs and Subgraphs have the same principle interface, Digraph. Two Subgraphs are not equal if they are Subgraphs of different Digraphs. However, if the Subgraphs have the same nodes connected by the same edges then they have the same interesting internal state.

I'd love to say

```java
public interface HasState<HasS is this.getPrincipleInterface() which better extend HasState<HasS>>
```

but had to limit the generic type parameters to

```java
public interface HasState<HasS extends HasState<HasS>>
```

and hope that a developer implementing HasState doesn't do something diabolically mismatched between the type specification and the filling for

```java
public Class getPrincipleInterface();
```

The compiler has all the pieces to sort out Enum and HasState puzzles, but there's no way in the language to direct the compiler to do the right thing in the code for the abstract class or the interface. Since `this.getPrincipleInterface()` and `this.getClass()` return hard-coded Classes, maybe something could be done with annotations interacting with generics. However, I think these two examples really are corner cases and don't rate a change in the language. Others might disagree, citing last Summer's venting of the spleens.

In contrast, I do think we need something to help us avoid generics mismatch Hell. I think just having dot access to type parameters' type parameters would work well. It would look and feel about the same as using inner classes.

The JDigraph project is my demonstration of reusable directed graph algorithms. It uses a general purpose graph containers inspired by the Java collections kit, built off of the Digraph interface. Here's the illustration, with examples from JDigraph:

```java
public interface Digraph<Node,Edge>
```

is fine. You can specify any class to be Node, and any class to be Edge. Generics actually make the code easier to follow, as people stop confusing nodes with edges. (IndexedDigraph is a Digraph with indexed access to the nodes and edges. You'll see that in a few paragraphs.)

Generics mismatch Hell starts innocuously enough. Subgraph is an interface for directed graphs that hold subsets of the nodes and edges of some Supergraph. Someone using Subgraph has to match up the Node and Edge type specifications for a Subgraph with the Supergraph.

```java
public interface Subgraph<Node,Edge,Supergraph extends Digraph<Node,Edge>>
    extends Digraph<Node,Edge>
```

could be a bit simpler with dot access, because the compiler knows that Supergraph is a Digraph, and has type parameters for Node and Edge.

```java
public interface Subgraph<Supergraph extends Digraph>
    extends Digraph<Supergraph.Node,Supergraph.Edge>
```

It's not a huge difference, and in fact takes more characters. However, Subgraph's definition could do the work to line up the type parameters. Also, Subgraph would only need one type parameter, not the three required above.

The complexity grows from there. OverlayDigraph is an interface for representing a Digraph that shares nodes with an underlying Digraph, but has its own edges. Think about it like someone laying a transparency sheet over a bunch of dots and connecting the dots her own way with a sharpie.

```java
public interface OverlayDigraph<Node,Edge,UnderEdge,Undergraph extends Digraph<Node,UnderEdge>>
    extends Digraph<Node,Edge>
```

The compiler knows what Undergraph will be using for Node and Edge. This is just generics mismatch Heck. Someone using this interface has to get the Node and UnderEdge type specs correct. It'd be a lot nicer to be able to take advantage of the compiler's knowledge of Undergraph's type parameters with something like

```java
public interface OverlayDigraph<Edge,Undergraph extends Digraph>
    extends Digraph<Undergraph.Node,Edge>
```

and use Undergraph.Edge instead of UnderEdge in the code. That's two type parameters to fill in instead of four. (You're about to see IndexedMutableOverlayDigraph, which is an OverlayDigraph with indexed access to the nodes and mutators to add and remove edges.)

Semirings define a set of useful operators for general graph labeling and graph minimization algorithms that work on Digraphs. The theory is right out of [CLRS](http://mitpress.mit.edu/catalog/item/default.asp?ttype=2&tid=8570) chapter 26.4. Semirings hold identity and annihilator label constants, and extension, summary and relax operators. The extension operator calculates the label to move from one node to another across an edge. The summary operator calculates the label combining two alternative labels. The relax operator calculates a new label by combining the existing label with a new, alternative label. These operators are the basic parts for building the Floyd-Warshall, Dijkstra, Prim's, Johnson's, Bellman-Ford and A* algorithms. I also made Semiring responsible for creating the initial OverlayDigraph of Labels. Encapsulating these things in Semiring has saved me writing the same tricky algorithm code for every new graph minimization problem.

Still with me? Hold on to your synapses. Semiring's declaration looks like this:

```java
public interface Semiring<Node,
                            Edge,
                            Label,
                            BaseDigraph extends IndexedDigraph<Node,Edge>,
                            LabelDigraph extends IndexedMutableOverlayDigraph<Node,Label,Edge,BaseDigraph>>
```

All five of the type specifiers have to line up correctly to compile code using this vile beast. It's hard for me to tame, and I wrote the thing. This is a big part of why JDigraph only does alpha releases. That's generics mismatch Hell. If the compiler were a bit smarter, Semiring's declaration could just be

```java
public interface Semiring<LabelDigraph extends IndexedMutableOverlayDigraph>
```

Five type specifiers could collapse to just one! You tell the compiler what to use for LabelDigraph. LabelDigraph knows Undergraph and Label. Undergraph knows Node and Edge. The Semiring interface and the compiler could do all the work to match up the types. Remember, Semiring's reason to exist is to encapsulate all those operators so I can write generic algorithms. Dot access to type parameters would let Semiring encapsulate all the gory details of type parameters, too.

The Floyd-Warshall is about the simplest graph minimization algorithm there is (three nested for() loops). Got any synapses left? Here's what its declaration looks like now:

```java
public class FloydWarshall<Node,
                            Edge,
                            Label,
                            BaseDigraph extends IndexedDigraph<Node,Edge>,
                            LabelDigraph extends IndexedMutableOverlayDigraph<Node,Label,Edge,BaseDigraph>,
                            SRing extends Semiring<Node,Edge,Label,BaseDigraph,LabelDigraph>>
```

Six! Six type parameters! Ah ha ha! I feel like [that vampire from Sesame Street](http://pbskids.org/sesame/number/index.html). (Dijkstra's algorithm and AStar need a Comparator, for a total of seven!) Letting dots access type parameters would let Semiring encapsulate all the type complexity, as well as the operators.

```java
public class FloydWarshall<SRing extends Semiring>
```

Using dots to access contained parameters would be a [Get out of Hell free card](http://www.goohf.com/) for this sort of problem. As more people decide to use generics, it's likely to help a lot of people a little bit. It would help JDigraph immensely.

The next step is to figure out where in the community to propose the change. Graham Hamilton's [blog on language changes in Dolphin](http://weblogs.java.net/blog/kgh/archive/2004/09/evolving_the_ja.html) is a bit dated. My own blog and a JavaOne community talk should be a good start.
