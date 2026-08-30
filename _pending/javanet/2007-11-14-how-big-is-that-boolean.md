---
layout: post
title: "How big is that boolean[]?"
date: 2007-11-14
permalink: /archive/2007/11/how-big-is-that-boolean/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2007/11/the_thing_about.html
---

My day job is software architect for a bunch of algorithm scientists who "feel the need for speed." We work to keep the system safe from [the evils of premature optimization](http://en.wikipedia.org/wiki/Optimization_(computer_science)#When_to_optimize) while finding hot spots that really speed things up. I won't bore you with the details, but we are computing a lot of solutions to a problem in advance, and looking up the answer in a big multidimensional boolean array. For this particular puzzle, the size and accuracy of the problem we can solve depends on how big a monster boolean array we can pack into memory.

We were blowing through the top of the JVM's heap violently via OutOfMemoryErrors, so I went digging with the profiler, and digging deeper with Google. From Sun's tutorial on [primitive types](http://java.sun.com/docs/books/tutorial/java/nutsandbolts/datatypes.html), "This data type represents one bit of information, but its "size" isn't something that's precisely defined." That's really freaky, given that bytes, shorts, ints, and longs are precisely defined, that floats and doubles are precisely defined by IEEE 754, and that chars are precisely defined by Unicode.

**Stack Frames**

A peak at bytecodes showed me that booleans are bigger than a bit. In a stack frame, booleans take 32 bits. That makes sense; the usual JVM is a 32 bit machine. From [a discussion forum posting](http://forum.java.sun.com/thread.jspa?threadID=457279&messageID=2088653), you can see that the operations are all integer operations (starting with 'i') in the bytecodes, with 31 unused bits in the register:

```java
0 iconst_0
1 istore_1
2 iconst_0
3 istore_2
```

**In the Heap**

Arrays of booleans are also bigger than I thought. The profiler and cheezy experiments were telling me booleans were about 8 times bigger than they should be. Google came through on this one, too, in [another forum](http://www.velocityreviews.com/forums/t364574-size-of-boolean-type.html). In my JVM, boolean array elements are bytes.

**Other People's Bits**

A little more digging showed me that a BitSet uses a long, and an EnumSet uses a long or arrays of longs to hold their bits, not boolean arrays. From BitSet.java:

```java
/**
     * The bits in this BitSet.  The ith bit is stored in bits[i/64] at
     * bit position i % 64 (where bit position 0 refers to the least
     * significant bit and 63 refers to the most significant bit).
     * INVARIANT: The words in bits[] above unitsInUse-1 are zero.
     *
     * @serial
     */
    private long bits[];  // this should be called unit[]
```

Arrays of booleans aren't java.util's choice. They won't be mine.

**More Questions**

Remaining questions: Why use longs and long[]s instead of ints and int[]s? Are the java.util programmers anticipating 64-bit machines? Is there something inherently more efficient about longs, which are usually less efficient? Or are the library writers trying to cover 33-64 members more efficiently and giving themselves twice the maximum upper size limit?

Does the weak definition of a boolean rate a bug or a request for enhancement? It seems to break write-once-run-anywhere because I can't predict how much memory my application requires. Should the compiler convert boolean[]s into the appropriate primitive or primitive array without us having to think about it? Do we want a sizeof() method?
