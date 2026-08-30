---
layout: post
title: "A Trip in the Way-Back Machine"
date: 2005-04-26
permalink: /archive/2005/04/a-trip-in-the-way-back-machine/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2005/04/a_trip_in_the_w.html
---

Ever want to go back in time and unmake a coding decision? Was it after a honeymoon period where you found some critical problem in something you'd bet on heavily and publicly? This happened to me recently with those seductive JDK 5 language features. Someone needed the software to work in JSDK 1.4, and I wanted to step into the way-back machine, return to September and start again. Then a fellow developer sent me a link to Retroweaver.

I started using JDK 5 features in my open source projects very early. I prototyped a version of [SomnifugiJMS](https://somnifugijms.dev.java.net/) with the new concurrency kit to make sure [JSR-166](http://java.sun.com/j2se/1.5.0/docs/relnotes/features.html#concurrency) had what I needed, and had been waiting years to use generics in [JDigraph](https://jdigraph.dev.java.net/). I built releases of both these java.net projects on JDK 5 and released them over the winter. I'd planned to lead my team at work use JDK 5 in February, and maybe start using these two open source projects. At about the same time, our team's business guys realized we had a lucrative opportunity to get our research in an embedded system, provided our code base stayed compatible with JSDK 1.4.

In late March, Patrick Menard sent me a [request](https://somnifugijms.dev.java.net/servlets/ReadMsg?list=users&msgNo=3): "[We would like to use SomnifugiJMS in our project.] Unfortunately we have to stick with java 1.4 for a while, and I saw you used quite some amount of JDK 5 specific code in your project. Do we have any change to make SomnifugiJMS run with java 1.4?" It's not just my team at work stalled at JSDK 1.4. If anyone tried to compile with SomnifugiJMS under JSDK 1.4, they got

`[javac] class file has wrong version 49.0, should be 48.0`

Patrick and I ran a thread of emails where I basically gave him bad advice. By combining some wishful thinking and a quick glance at the ant manual, I thought he could compile JDK 5 code into a JSDK 1.4-compatible .class file using javac. After all, generics, for loops and enums are mostly syntactic sugar expanded and cleaned up in the compiler. Patrick could hack the source code to use the [backport](http://www.mathcs.emory.edu/dcl/util/backport-util-concurrent/) (which worked great), and be off and running.

`&lt;javac target="1.4" blah="blah" blah="blah" ... &gt;`

gave me

`javac: target release 1.4 conflicts with default source release 1.5`

Rats. The next try was

`&lt;javac source="1.5" target="1.4" blah="blah" blah="blah" ... &gt;`

which gave me the same sort of error message. The next try was

`&lt;javac source="1.4" target="1.4" blah="blah" blah="blah" ... &gt;`

which gave me the expected seventy-odd syntax errors from trying to compile JDK 5 generic notation as if it were JSDK 1.4 code, and convinced me there was no love in the world. I decided to fork v3 to be a JDK 1.4 version of SomnifugiJMS (instead of using CVS' somewhat unsatisfactory branching feature), switched the backport to be the standard and set about stripping the JDK 5 language features out.

About that time, Patrick sent a [message](https://somnifugijms.dev.java.net/servlets/ReadMsg?list=users&msgNo=8) describing how he'd gotten SomnifugiJMS with the JDK 5 features to work on JSDK 1.4. He'd used [Retroweaver](http://retroweaver.sourceforge.net/) to mix out the JDK 5 language changes at the byte code level. Retroweaver does not yet include support for java.util.concurrent, but handled generics and for loops once I grokked the ant target. I made the backport the default and juc support a separate subproject to keep the JDK dependencies out, and released SomnifugiJMS alpha-0-7 last week.

More About Using Retroweaver

I contacted Retroweaver's creator, Toby Reyelts, to better fill in some details in this blog. Toby had originally only intended to support new language features like generics, enums, autoboxing, and static imports. Enough people (possibly double-counting me) have asked for support of j.u.c he has decided to add it to some future release.

Toby's advice for supporting both JSKD 1.4 and JDK 5 at the same time was straightforward: Provide two different downloads. One made for standard JDK 5, one for JSDK 1.4. The retroweaved release will run fine on JDK 5, but will rely on the retroweaver-rt.jar. Interaction with JDK 5 parts may not work as hoped. For example, a com.rc.retroweaver.runtime.Enum_ can not be part of a JDK 5 java.util.EnumSet.

Wishing for Subversion Again

I am currently supporting one version of SomnifugiJMS with a single build file. To support a JDK 5 version separate from a JSDK 1.4 version, I would want two separate branches of the code. The JSDK 1.4 version would use Retroweaver and the concurrency backport (like the v3 directory I created for alpah-0-7), and would not have the juc subproject at all. The JDK 5 branch would have the net.walend.somnifugi.juc source in the somnifugi subproject and would not have the net.walend.somnifugi backport. Setting up this kind of branching is trivial in Subversion ("svn copy trunk jdk14" should do it), but java.net uses CVS. CVS branching is enough less pleasant that I am going to wait for Toby to release a version of Retroweaver that supports the concurrency backport.

This blog involves five new technologies: JDK 5, the juc backport, Retroweaver, Subversion and SomnifugiJMS alpha-0-7. (Well, six -- I'm using Mac OSX 10.4). JDK 5 had some features I wanted to use for a long time, but I almost had to stop using them. The juc backport worked fine. Retroweaver worked very well, but is very new. Subversion seems rock solid, but it's for source code. And the developer of SomnifugiJMS (that's me) isn't at all embarrassed about keeping projects in alpha for ever. Some might argue that I'd picked up JDK 5 too soon, but other emerging technologies (Retroweaver and the juc backport) had already anticipated the problems I would encounter.

What's the right time to adopt new technology? How does that interplay with Sun, the developer community on java.net and at large?
