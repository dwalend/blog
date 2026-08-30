---
layout: post
title: "Design For Exceptions"
date: 2003-10-06
permalink: /archive/2003/10/design-for-exceptions/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2003/10/design_for_exce_1.html
---

I read [Bill Venner's interview with James Gosling, "Failure and Exceptions,"](http://www.artima.com/intv/solidP.html) and with [Anders Hejlsberg, "The Trouble with Checked Exceptions,"](http://www.artima.com/intv/handcuffs.html) and was a little surprised. I thought exceptions would be in .Net since .Net has taken so many other features from Java. I've never found checked exception clauses to be much of a burden. It's one of my favorite features of Java. Anyway, given all the talk about exceptions and exception handling, I thought I'd take a minute to describe what I do and ask how others use them.

I think the problems that Dr. Hejlsberg describes, versionability and scalability, are easy to contain if the development team decides how they're going to handle trouble before they get too deep into their work. Here's what I usually do:

When I start a package, I create a handful of support classes. These classes are simple, but having them there encourages developers to use them instead of creating custom solutions. One of these classes is an abstract exception, a parent for all the concrete exceptions in that package. When developers discover they need a new exception, they extend this exception. The API for the package only throws subclasses of this exception. The abstract exception from JDigraph's net.walend.digraph package looks like this:

```java
package net.walend.digraph;

import java.io.Serializable;

/**
An abstract parent for all caught exceptions in the net.walend.digraph package.

@author @dwalend@
*/

public abstract class DigraphException
    extends Exception
    implements Serializable
{
    public DigraphException(String message)
    {
        super(message);
    }

    public DigraphException(Throwable wrapped)
    {
        super(wrapped);
    }

    public DigraphException(String message, Throwable wrapped)
    {
        super(message, wrapped);
    }

}

/*
@license@
*/
```

Unlike the rest of the API, which gets defined during design, I've found exceptions tend to bubble up from implementation. Sometimes it's obvious that something will go wrong at design time, but often I need to create some new exceptions while implementing the code. Plus I like to create very descriptive subclasses of my abstract exception. Specific subclasses make it easier for code handling the exception to determined what failed and how to react. That's what Dr. Gosling means by, "... in a throws clause ... be as specific as possible."

If I can't handle a checked exception, I like wrapping the exception with my own subclass of my package's abstract exception, then throw the wrapping exception. My API still only throws subclasses of my abstract exception. The overhead is just constructing the new exception. Wrapping exceptions bounds the scaling problem Dr. Hejlsberg describes by limiting what can appear in the throws clause.

Here's the part that's worth discussing: I like keeping my methods' throws list very specific, limited to the concrete exceptions actually thrown. This choice means that people writing code that calls these methods will be cognizant of each exception. If they like, they can still catch the common parent exception.

The alternative is having all methods declare that they throw only the same abstract exception. If you believe your public API can never be changed, this is the way to go. This approach solves the versioning problem Dr. Hejlsberg describes by insulating code from changes in the exceptions actually thrown, but does not give great hints for how to handle the problem.

For most of my work, the versioning problem is overstated. Most of the source code developers create stays small in scope. I understand that after some point in the development life cycle of code reused across many projects the throws clause in a method can't be changed anymore. If a project becomes popular enough, these detailed throws clauses will break down and having the parent exception in the throws clause is a better decision. I think that popularity is pretty rare: Interfaces from a JSR, or public methods in a popular apache project, or from a core software team at a big company should declare that they throw a general parent exception from day one. However, most code we write has a fairly small and well-defined group of developers. Changing the throws clause doesn't wag many lines of code. That code may need to be changed to handle the new exception in a thoughtful way. If the library is becoming more popular while it is still being developed, adding the parent exception to the end of the throws clauses is easy and well-received.

If that last paragraph doesn't generate some interesting talk back, the next two will.

When I've tried to use the standard exceptions available in java or javax packages, I've discovered that very few of these exceptions have constructors that take nested exceptions. Generally, developers will use constructors that take an exception, but will not use the initCause() method on their own. I usually have to subclass them to either call the initCause() method in the constructor or override getCause() (to stay compatible with JDK 1.3. See [Felipe Leme's latest blog](http://weblogs.java.net/pub/wlg/432).)

I avoid throwing my own RuntimeExceptions except at fairly high levels when it's time to stop or reset the application without cluttering the API. And I'll sometimes use them to mark states I think are impossible. If I control the main event loop, my code catches these exceptions and tries to bow out gracefully, whatever graceful means in the context. I've also used RuntimeExceptions when I was trying to make quick fixes to an existing code base. But I've regretted this shortcut in the past.

Do other people do anything radically different? Is it ever OK to use throws Exception in a declaration? Or, like .Net, to use all RuntimeExceptions no matter what?
