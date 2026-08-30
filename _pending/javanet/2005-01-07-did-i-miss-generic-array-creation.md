---
layout: post
title: "Did I Miss Generic Array Creation?"
date: 2005-01-07
permalink: /archive/2005/01/did-i-miss-generic-array-creation/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2005/01/did_i_miss_gene.html
---

While sweeping up sawdust before the latest release of [JDigraph](https://jdigraph.dev.java.net/), I used -Xlint to spot remaining places where I have some things to clean up. I have just a handful to go. I'm having the most trouble with creating Arrays in collection-like classes. JDigraph is a generic efficient directed graph representation, so these arrays are everywhere. I've taken examples from [FibHeap.java](https://jdigraph.dev.java.net/source/browse/jdigraph/v2/source/collection/net/walend/collection/FibHeap.java?rev=1.6&content-type=text/vnd.viewcvs-markup).

```java
HeapMember<Key,Value,Comp$gt;[] fibNodes = (HeapMember<Key,Value,Comp>[])Array.newInstance(HeapMember.class,size());
```

results in a waring from lint.

The first thing I tried didn't compile:

```java
//doesn't compile
        HeapMember<Key,Value,Comp>[] fibNodes = new HeapMember<Key,Value,Comp>[size()];
```

results in
 

```java
jdigraph/v2/source/collection/net/walend/collection/FibHeap.java:57: generic array creation
        HeapMember<Key,Value,Comp>[] fibNodes = new HeapMember<Key,Value,Comp>[size()];
```

I tried dynamically creating the array using java.lang.reflect.Array:

```java
HeapMember<Key,Value,Comp>[] fibNodes = (HeapMember<Key,Value,Comp>[])Array.newInstance(HeapMember.class,size());
```

which gives me the warning from lint again.

```java
/Users/dwalend/projects/opensource/jdigraph/v2/source/collection/net/walend/collection/FibHeap.java:58: warning: [unchecked] unchecked cast
found   : java.lang.Object
required: net.walend.collection.HeapMember<Key,Value,Comp>[]
         HeapMember<Key,Value,Comp>[] fibNodes = (HeapMember<Key,Value,Comp>[])Array.newInstance(HeapMember.class,size());
```

I've tried doing other things, especially to the HeapMember.class argument, but haven't found a solution that compiles with no warnings.

Is there some bit of API I missed? Is there a good reason not to create arrays of generics? Or should I report a RFE to Sun asking them to add generic parameters to Array.newInstance()?

Thanks,

Dave
