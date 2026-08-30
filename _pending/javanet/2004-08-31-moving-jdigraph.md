---
layout: post
title: "Moving JDigraph"
date: 2004-08-31
permalink: /archive/2004/08/moving-jdigraph/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2004/08/moving_jdigraph.html
---

I started writing the code that's grown into JDigraph in an algorithms class in 1995. I wanted to share it with some friends in 2000, so I added a BSD license on it in 2000 and hung it on sourceforge. I've got stronger loyalties to java.net, so I wanted to move JDigraph. I had a few spare evenings in August, so I moved JDigraph to [http://jdigraph.dev.java.net](http://jdigraph.dev.java.net). Here's what I learned while moving.

Spring Cleaning

Both sourceforge and java.net use CVS for source code control. Changing directory structures in CVS is a pain; in CVS, files really can't be moved around or renamed without loosing their history. CVS commands for directories feel like an afterthought. As a result, my directory structures in CVS projects tend to calcify into whatever I try first. So I took the opportunity to reorganize the source code tree, using ideas I've learned over the last few years.

Ant's Import Task

Changing the directory structure meant reworking the build.xml files, another chore I'd put off for half a decade. I considered shifting to Maven or Jython for the builds, but ultimately decided to stay with Ant. Maven gives a nice canned build, but it doesn't match my environments well (java.net, sourceforge, the day job). Jython would give a more powerful language, but leave behind entry level developers who can pick up Ant in a day. Ant 1.6's new import task really provides what I want.

For years, I've had almost identical build.xml files copied through many projects and subprojects. Ant lacked a nice way to pull functionality from one build file to another. (I know a few XML tricks, but those are more challenging than Jython.) JDigraph demonstrates that import was the main thing I was missing. Here's what a subproject's build file looks like now:

```xml
<project name="collection" default="test" basedir=".">

 <import file="../common/common-build.xml" />

<!-- set global properties for this build -->
 <target name="set-subproject" >
  <property name="subproject" value="collection"/>
 </target>

</project>
```

Into java.net

After I rearranged all the code, checking it in to dev.java.net was easy. CVS on java.net is a little more trusting than on sourceforge; I only had to provide my password at the beginning of a session, instead of during every operation.

JavaDoc on java.net

The only real obstacle I hit was getting JavaDoc (and the rest of the web site) up on java.net. After a few rounds of email with the java.net support crew, I took their advice and put the whole web site into source code control, under the www/ top-level directory. (java.net's support is great. Thanks, Helen.) I can hear people I've worked with gasping in amazement; one of the big tenets I've held over the years was "never check in anything to source code control that comes from the build." My big concern is mechanical. If I have to check in all of the javadoc every time I do a release, then I have to somehow disconnect the old javadoc. CVS is not so good at removing whole directories. Tracking down all the obsolete javadoc files is even worse. So I created a directory under www/ called alpha-0-7-2/ (the name of the current version), and checked in all the source code there. Next release, I'll create a new directory for the javadoc; the build already puts in the correct link on the project's home page.

The CVS mailing list for JDigraph rewarded my cleverness with a fifteen megabyte CVS log.

The next problem was the javadoc didn't show in java.net's frames. Another email to java.net. Helen said to add "nonav" to the beginning of my links. ("nonav." "No navigation." I didn't get it for about two hours.) [It worked like a charm.](https://jdigraph.dev.java.net/nonav/alpha-0-7-2/api/index.html)

Finding a Home

java.net is focused on about two dozen communities. That wasn't the case in June 2003 when I first reserved a spot for jdigraph. This summer when I finally moved JDigraph in, it was an orphan. At JavaOne, I spoke to a few people involved with [edu-research at JECL](http://edu-research.dev.java.net), which seemed like a good fit. A few emails to Daniel Brookshier and Robert Stephenson closed the loop. I get the impression that a body of working, interesting, relevant code would get any project in the community (and an interesting idea would make the incubator).

What Could Be Better?

Helen knows I'm going to ask for Subversion. (She's not above encouraging me.) Wrangling the javadoc in CVS is labor. Switching from CVS to Subversion would answer most of the problem. I'd still have javadoc -- a product -- in source code control, but Subversion would make the job of swapping in a new version easy. Collabnet helps run java.net, and paid to have Subversion written. It seems like a natural move. The word from the support crew at java.net is that we'll have it someday, but it might be a while.
