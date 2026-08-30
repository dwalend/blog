---
layout: post
title: "SomnifugiJMS for User Interfaces and Simple-Enough APIs"
date: 2003-09-11
permalink: /archive/2003/09/somnifugijms-for-user-interfaces-and-simple-enough-apis/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2003/09/somnifugijms_fo_6.html
---

[Somnifugi JMS](http://somnifugi.sourceforge.net) is an implementation of the [Java Messaging Service](http://java.sun.com/products/jms/) built on top of Doug Lea's Channels. This JMS implementation runs inside a single JVM, quickly delivering messages between java Threads. A few years back, I created Somnifugi JMS to speed up a project where the architects had gone overboard with messaging. I used Somnifugi JMS to prototype and test the next project, and left it in place to keep things fast. The project after that, I used a Somnifugi JMS Topic to communicate from the AWT Thread to other Threads where the controllers and models live. It worked great; I've used it in every Swing project since then, and a few others have started using it this way, too.

I have trouble tracking all the issues in building a Swing interface: Swing's API has about a hundred top-level classes, each with a few dozen methods, plus nine subpackages, AWT, and Java2D to get things just right. Getting a group of people to all use MVC, JavaBeans and Threads the same way is hard. The model always has its own dynamics, and usually changes a few times a day. Add users unfamiliar with the new UI to make the project even harder.

The "Use Topics to communicate from the view to the controllers" pattern is a nice complement to the "Use SwingUtils.invokeLater() to communicate from the controllers to the view" pattern. Extending the pattern to place model handling in separate Threads is just a matter of adding extra Topics or Queues for the controller to consume. Plus if I need to make the application fit a client-server model, all I have to do is swap the model's Somnifugi JMS Topics for distributed JMS Topics.

I think the power in this pattern comes from breaking up the task into small, easy-to-grasp pieces.

Using a Topic to communicate from the view to the controller simplifies both by decoupling them. The view generates messages whenever any user action happens. The controller digests those messages. The JMS API is small and easy to learn and use. Using Topics simplifies performance decisions about handling Threads and shared Objects. The projects become more predictable, easier to decouple and test, and more pleasant to work on.

I think a lot of this gain is because a JMS Topic is easier to use than Java's threading support. The JMS specification is one of the best written specifications to come out of the JCP. The underlying ideas work without bending the universe to match. Each interface fills an outlined role and I don't have to do anything weird to my own code to use them. There's no requiring me to inheriting from someone else's superclass for example. (See Allen Holub's article, ["The fragile base-class problem"](http://www.javaworld.com/javaworld/jw-08-2003/jw-0801-toolbox.html?).) I needed a single afternoon to read the spec, and I understood without strain.

I spoke briefly with Joseph Fialli (one of the authors of the JMS spec) after he gave an invited talk (on [JaxB](https://jaxb.dev.java.net/)) at a [local user group](http://www.acm.org/chapters/webtech). I described how I was using JMS behind Swing interfaces. He thought the pattern was pretty slick. He was the only person ever to compare it to [InfoBus](http://java.sun.com/products/javabeans/infobus/).* After the talk, I found my notes from reading the InfoBus spec in 1999. "InfoBus API looks more complex than just using the Thread API. We'd need to fill in most of the JavaBeans event spec. Not a good fit for our problem." Over the years, I've never seen a project that uses InfoBus, despite the hype it received in the late 90's. A [JSR to update the InfoBus specification](http://www.jcp.org/en/jsr/detail?id=33) was started in 1998 but withdrawn in 1999. I think the InfoBus spec has been abandoned, but some ideas live on in the JavaBeans spec.

I think there's a strong correlation between simple APIs and how likely developers are to use those APIs. JMS survives and thrives because it meets a need that developers recognize with relatively little overhead. JMS exemplifies a "Simple-Enough Principle" for API design. Developers never adopted InfoBus in large numbers because we didn't think InfoBus was any better than what we had before.

Because all the code I write becomes library code, I try to keep this principle in mind when I define APIs. I want to create an API rich enough to do the job, but simple enough for another developer to be able to use without expanding the problem he's working on. Perhaps the advances in Aspect-Oriented code will reduce the typing overhead for JavaBeans to the point where developers can meet the specification. But that's a different blog.

* As I added mark up to this article, I got email from Ted Shab asking about Somnifugi JMS, "We are looking for InfoBus-like functionality, as well as some other related concepts."
