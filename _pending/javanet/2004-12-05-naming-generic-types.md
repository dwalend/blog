---
layout: post
title: "Naming Generic Types"
date: 2004-12-05
permalink: /archive/2004/12/naming-generic-types/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2004/12/naming_generic_1.html
---

Naming Generic Types

We've had blogs covering DRY and magic Strings in the last week. I'm going to blog about generic type names, specifically using names longer than one letter.

Some of us are old enough to have used systems with a limit the length of variable names. But I haven't seen anyone use "x" as a generic double name in years (caveat coordinates). We left that habit behind because of the confusion it caused. We now teach people to write self-documenting code with descriptive variable names.

The [generics tutorial](http://java.sun.com/j2se/1.5/pdf/generics-tutorial.pdf) that comes with JDK 5 suggests using one capitol letter to represent generic types: "A note on naming conventions. We recommend that you use pithy (single character if possible) yet evocative names for formal type parameters. It’s best to avoid lower case characters in those names, making it easy to distinguish formal type parameters from ordinary classes and interfaces. Many container types use E, for element, as in the examples above." I tried to follow this advice; I used N for the node type and E for the edge type.

```java
public interface IndexedDigraph<N,E>
    extends Digraph<N,E>
```

wasn't so bad. But the typespec for Semirings has five generic types.

```java
public interface Semiring<N,E,L,B extends IndexedDigraph<N,E>,LD extends IndexedMutableDigraph<N,L>>
```

It got painful quickly. What's L? What was E again? Element?

Using fully spelled out names removes the guessing from Digraph:

```java
public interface IndexedDigraph<Node,Edge>
    extends Digraph<Node,Edge>
```

and changes Semiring from cryptically intimidating to merely complex:

```java
public interface Semiring<Node,
                          Edge,
                          Label,
                          BaseDigraph extends IndexedDigraph<Node,Edge>,
                          LabelDigraph extends IndexedMutableDigraph<Node,Label>>
```

Changing "E"s to "Edges", etc. was mindless drudgery. "E"s and "N"s are much more common than "x"s. I made mistakes during the cleanup. Changing full names would have been much easier for me. Reading full names should be easier for everyone else.

I like to name generics after the role they play in code. I didn't have any problem distinguishing the generic names from interfaces or classes. JDigraph doesn't have a Node, Edge or Label class (which is much easier to figure out now that I've used generics to cut the number of classes in half).

To avoid abbreviations in code, I keep a thesaurus on my desk. My thesaurus is probably the right tool to clear up any confusion between generic typespecs, classes and interfaces.
