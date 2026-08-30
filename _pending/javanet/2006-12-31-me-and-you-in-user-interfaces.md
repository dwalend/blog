---
layout: post
title: "Me and You In User Interfaces"
date: 2006-12-31
permalink: /archive/2006/12/me-and-you-in-user-interfaces/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2006/12/pronouns_in_com.html
---

The pronouns we use when we address computers and imagine them addressing us hides some profound insight. I haven't pinned down exactly what. Wikipedia has a nice grammar description on [first, second and third person](http://en.wikipedia.org/wiki/Grammatical_person). I think the way we use these implied points of view in computing is really strange and not very consistent. Someone could write a decent master's thesis drawing some conclusions on these inconsistencies.

First Person

I've always found "I," "me," and "my" disconcerting in computing. Some of that unease is from growing up on Unix systems. /home/dwalend feels natural to me. Windows' "My Documents" clashes. The computer screen is referring to documents I wrote, so the file system's word is recognizing that I am part of the narrative. The computer's language implies that it wants to become an extension of me, as part of my internal narrative. Microsoft Visual Basic apparently has a [My keyword](http://blogs.msdn.com/danielfe/archive/2005/06/14/429092.aspx) to invite a programmer in. The computer drops into [passive voice](http://www.unc.edu/depts/wcweb/handouts/passivevoice.html) to avoid defining itself. (My coworkers have endured many of my tirades on how passive voice always hides something important.) "My Documents not found." I know where I left them. Not found by whom?

I've observed a very different use of first person prevalent in computer programming examples. Example writers often use "my" as a prefix in a reference name to imply unshared possession -- a filled UML diamond aggregate. Instead of the computer trying to merge with my subconscious, a class grows its own ego and takes possession of its parts.

[

```java
public static JFrame myFrame;

    public static void main(String[] args) {
      myFrame = new JFrame("Tutorial");
      myFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
      JGraph graph = new Tutorial();
      myFrame.getContentPane().add(graph);
      myFrame.setSize(520, 390);
      myFrame.show();
```

](http://www.jgraph.com/example/Tutorial.java)

However, ["My" as a prefix to a class name](http://cs.nyu.edu/~yap/classes/visual/03s/lect/l7/) implies that some person -- the writer or the reader -- possesses the class. "MyFrame" invites a third person into the dialog with my computer and me. It's like [Who's on First](http://www.youtube.com/watch?v=IEaKjRyPjVY) but not funny.

Second Person

I've found myself using second person, -- "you" and "your" -- in my examples to refer to the person reading the examples:

[

```java
MutableDigraph yourDigraph = new MutableHashDigraph();

    yourDigraph.addNode(nodeA);
    yourDigraph.addNode(nodeB);
    yourDigraph.addEdge
    (nodeA,nodeB,objectContainingDataAssociatedWithRelationship);
```

](https://jdigraph.dev.java.net/servlets/ReadMsg?list=users&msgNo=2)

Second person works for me as a style here. It extends a dialog that I have with another person; we both know what "you" refers to.

However, second-person dialog between people and computers have mixed results at best. [Clippy](http://www.microsoft.com/presspass/features/2001/apr01/04-11clippy.mspx) was the definitive  failure and reduced to a target for [spoofs](http://www.rjlsoftware.com/software/entertainment/clippy/). Bob the dog still digs pixels on the windows machine at work when I search. [Ms. Dewey](http://www.msdewey.com/) seems to focus more on, well, Ms. Dewey than getting anything useful done. She's entertaining on her own, but would you really want her to stay for dinner? [Wildfire](http://www.lacba.org/lalawyer/tech/wildfire.html) was better. She did something useful and told great jokes, but never quite caught on. Creating a first-person/second person dialog with a computer isn't so much science fiction as fiscal fiction. I did a little work with voice interaction in graduate school; I built a voice-interactive version of [Cluedo](http://en.wikipedia.org/wiki/Cluedo). Voice interaction isn't that hard to do, provided your software can limit what a person might say.  When people speak, they really want to talk to something with a sense of self.

Third Person

I grew up with unix, which is all about third person; /home/dwalend is where the heart is. The computer doesn't talk about itself as an entity beyond its host name, and every reference has to be third-person. The words that appear on the computer screen don't show a pretense of self-awareness. Java's "this" keyword is also third-person, referring to "this instance of a class." I find third-person the least jarring for our current window-interface mouse-pointer interactions. A dialog with a machine that has no sense of self is really uncomfortable. I've done a little work with voice user interfaces; third-person spoken dialog feels even more unnatural.

Wrapping Up

Microsoft created or paid for "My Documents," Visual Basic, Clippy, Bob and Ms. Dewey. I'm not sure what conclusions to draw about one company producing so many examples that make me cringe. I'll admire their bold public attempts, and leave the rest unsaid.

I'm not yet convinced that a computer with a sense of self is a useful thing. The computers we have now are mostly tools or for entertainment. The market place so far has rejected computers which pretend to have any sense of self. However, the examples I have sited for the most part had very assertive personalities relative to the help they provide; [Clippy always injects himself at the least opportune times](http://ftrain.com/art/graphics/archive/ftraintwo/badword.gif).
