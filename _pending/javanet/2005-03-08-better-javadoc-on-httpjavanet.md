---
layout: post
title: "Better JavaDoc on http://java.net"
date: 2005-03-08
permalink: /archive/2005/03/better-javadoc-on-httpjavanet/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2005/03/better_javadoc.html
---

Last August I posted a [blog on setting up a project on http://java.net](http://weblogs.java.net/blog/dwalend/archive/2004/08/moving_jdigraph.html). I spent a paragraph on how I posted my project's JavaDoc API. I've worked with that solution for seven months, but I'm not really happy with it. I'd like to ask the people who run java.net for a better way, but I'm not sure exactly what to ask for.

The Problems with using CVS for JavaDoc

I have two problems with using CVS to store JavaDoc. The first is philosophical -- CVS is a source code control system, and JavaDoc .html files are a derived product, not source code. If you can check out the source code, you can build the JavaDoc yourself. If you change the JavaDoc, it doesn't matter; next time you rebuild it, those changes are lost. The second problem is logistical -- I either have to remove all the JavaDoc from the last release and add all the new JavaDoc from the latest release. Or I have to put each release under a new directory; that saves me removing it, but means that everyone's links point to an old copy and grows the www subdirectory over time. Either way, I have to add several layers deep of JavaDoc directories. And I get a 15 MB cvs change log in email every time.

Sourceforge's Approach

Sourceforge gives each user a unix account and each project a public web directory. Back when I kept projects on Sourceforge, I ftped a tar ball of .html files for the web pages, including the JavaDoc. It worked, but was fairly primitive. Plus it relied on letting the users log in remotely to sourceforge's servers. That's probably more than Sun, O'reilly and Collabnet are willing to pay for.

I've thought of three alternatives, but don't know which would be the best.

Subversion

Collabnet, one of java.net's sponsors, paid to create [Subversion](http://subversion.tigris.org/), a replacement for CVS. I've used it at home for a while, and on a few projects at work. I'd rather use Subversion than CVS in any case; Subversion treats each commit as a transaction, linking all the changes together. Using Subversion to store source code and web pages would still not address my philosophical concerns. However, Subversion's ability to easily remove and add whole directory structures would be a huge improvement over CVS. I could even get rid of the top level v1, v2, v3, etc. directories.

.war Files

In the previous blog, straun suggested a separate repository of .war files for web sites. Using .war files would let us maintain project web sites the way Java developers are used to. The approach addresses both of my concerns. When I'm ready to release a new version of the web site, I build a .war file and post it in the appropriate place, instead of checking in the files as source code. And I handle the site as a single .war file instead of single files in directories. How close is http://java.net from being able to support that? What other pitfalls are involved? Would the administrators have to do something special to keep developers from putting executable code in the .war files?

Shared JavaDoc Database

A more compelling solution: Join with [JDocs](http://www.jdocs.com/), a shared cross-linked JavaDoc database, or to set up something similar on java.net hardware. The JavaDocs would be completely separate from source code. And over time, we would grow a large, cross-linked set of API docs that would help us use each others' work. The JDoc site hasn't added new material since September 7th. I don't know what would be involved for the java.net administrators to set up such a system, or the java.net sponsors to link up with JDoc.

Those are the options I've thought of. Which of these should we ask for? Is there some other option we should consider?

Thanks,

Dave
