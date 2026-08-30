---
layout: post
title: "Understanding Service Oriented Architecture"
date: 2006-04-04
permalink: /archive/2006/04/understanding-service-oriented-architecture/
archived: true
originalUrl: http://today.java.net/pub/a/today/2006/04/04/understanding-service-oriented-architecture.html
---

Service Oriented Architecture (SOA) promises to provide us with the ability to assemble complex, distributed systems by selecting and creating compatible parts called services. So far, SOA has delivered a lot of hyperbole to the Web. Gartner recognized it as [one of the five hottest IT trends in 2005](http://www.gartner.com/DisplayDocument?doc_cd=125868), claiming that "By 2008, SOA will provide the basis for 80 percent of development projects." At JavaOne 2005, 82 of the 168 technical session PDFs contained "SOA." In July of 2005, there were 1.4 million Google hits for "service oriented architecture." By February, 2006, there were 72 million. SOA is riding a rising tide as the next big thing for enterprise developers.

Unfortunately, most developers find it hard to cut through this tide of hype to learn just what service oriented architecture is about. Forests of three-letter acronym (TLA) standards sprout, bloom, and are overgrown before any of us can learn enough about them to decide if they are appropriate for our own projects. The standards compete for our attention and allegiance. Further, most articles and presentations focus on a specific TLA, and how to make some legacy system fit within someone else's favorite web service plumbing. "Legacy" seems to mean "the software that has to keep working to keep the system alive and useful to the business."

I started working with distributed messaging systems in 1995 and can understand most of the articles, but I find the volume of hype daunting and largely irrelevant. This article focuses on what you can get out of SOA to make developing and maintaining software easy, and help your businesses run better. Here's what you can get out of service oriented architecture:

- Better understanding of the system being developed.

- Better-organized, better-focused incremental development.

- Easier integration with each others' systems.

- Well-defined boundaries for tests.

- More big-block reuse of code by reusing services.

- Scaling up by creating systems of systems.

- More reliability via restartable services.

- Development focused on executable business plans.

That list is a huge promise. No wonder there's so much hype. Unfortunately, the list doesn't hold anything we can code. Aside from being able to restart a service, it's not specific at all. Service oriented architectures bring together specific good ideas from the 1980s and 1990s to create a complex system from simple parts. Service oriented architectures have these characteristics:

- Services have strong software contracts.

- Services are encapsulated.

- Messages are documents.

- Services share a message bus.

- Services are loosely coupled.

- Services have a life cycle.

- Systems of services are assembled at runtime.

- Services can be discovered.

- Systems of services can grow into systems of systems.

## Services Have Strong Software Contracts

A strong software contract defines the role that the service plays. Services are a realization of [software design-by-contract](http://en.wikipedia.org/wiki/Design_by_contract). A service's contract describes what messages a service will receive, what messages a service will send, and what error signals a service will send when things go wrong. In service oriented architecture contracts, hidden state invariants tend to be less important. High-level descriptions of any side effects-- especially changes in exposed internal state--take center stage. The software contract serves as a design guide, test plan, and programmer's interface. Share the service's software contract with people when they ask you what the service does. Use the software contract to help your managers decide which services to build first, to address some immediate needs of your business.

Java's [JavaDoc](http://java.sun.com/j2se/javadoc/writingdoccomments/index.html) provides a nice start for software contracts. By using JavaDoc, especially [*package.html*](http://java.sun.com/j2se/javadoc/writingapispecs/index.html#package) files, you can guide other developers to the important parts of your code and share the important details. Most Java developers have learned to read the JavaDoc if they read anything at all, so it is your best bet for describing your contract to them. [WSDL](http://www.w3.org/TR/wsdl) files include a very precise description of a service's programming interface in a computer-readable format. However, WSDL files are separate from code (so they won't be found) and hard on the eyes (so important details will be missed). I like to create [Java interfaces](http://java.sun.com/docs/books/tutorial/java/concepts/interface.html) to hold specific details of services in my system. JDK 5 [annotations](http://java.sun.com/j2se/1.5.0/docs/guide/language/annotations.html) can help, too, especially those from [JSR-181](http://jcp.org/en/jsr/detail?id=181), which will be standard in JDK 6. Annotations are computer-readable, available in JavaDoc, and are embedded in code. I think they are the best choice for the structural part of a software contract, but are no substitute for a solid written description.

## Services Are Encapsulated

Services are encapsulated. A service only exposes the behaviors in its contract. Nothing outside the service can observe internal state and state transitions. How a service fulfills the contract remains hidden. No interesting service can achieve ideal encapsulation; even a service on dedicated hardware will still share limited bandwidth on a network. The best way to handle these details is to add them to the contract; if something that matters to the rest of the system is not in the contract, then the service's contract is incomplete. Fixing bugs in your contract is much easier than fixing encapsulation. Observing and enforcing encapsulation helps prevent creeping complexity growth, a maintenance nightmare.

The goals of encapsulation line up well with the original promise of object oriented programming: [keep responsibility localized and defined](http://www.javaworld.com/javaworld/jw-09-2003/jw-0905-toolbox.html). I'm not sure there can be a positive standard for encapsulation, a feature defined by an absence. I have used some existing language features to set boundaries. Java's [access keywords (`public`, `protected`, `default`, and `private`)](http://java.sun.com/developer/onlineTraining/Programming/BasicJava2/oo.html#access) and [JavaDoc](http://java.sun.com/j2se/javadoc/writingdoccomments/) provide a nice start. By controlling accessibility, you can keep some parts of the programmer's interface hidden. Language designers at Sun have muttered about some kind of [`friends` keyword in JDK 7](http://weblogs.java.net/blog/kgh/archive/2004/09/evolving_the_ja.html), but I haven't seen anything concrete yet.

## Message Contents Are Atomic Documents

Part of service oriented architecture is [document oriented architecture](http://www.mnot.net/blog/2004/08/05/document_oriented). The contents of the messages that flow in the system are well-defined data structures--like documents. Sending a message effectively makes a copy of a data structure. Once sent, the message can not generally be pulled back and changed. Message data structures need to be complete and compact, and have consistent rules for how to maintain referential integrity. You can easily and directly reference one part of this document data structure from another, but referencing something outside of the structure means extra work with foreign keys. The [Java Data Object](http://jcp.org/aboutJava/communityprocess/pfd/jsr243/index.html) specification section 6.3 describes this dichotomy well. Good JDO first-class objects are like documents, constructed of subordinate second-class objects. XML uses a slightly more implicit approach. XML files are documents that use IDs and IDREFs or [XPath expressions](http://www.w3.org/TR/xpath20/) for internal references. Most systems of services have a small local service responsible for finding the right document using foreign keys.

Obviously, one service needs to be able to understand messages received by another. Agreeing on syntax is the easy part; try Java's [serialization](http://java.sun.com/developer/technicalArticles/Programming/serialization/) if you've got Java on both ends, XML otherwise. If you pick XML, decide how your system will handle referential integrity inside the document. [XStream](http://xstream.codehaus.org/) provides a very simple solution that plays havoc with `XMLSchema`. [JAXB 2.0](http://java.sun.com/webservices/jaxb/) does a very good job. If you are trying to get services produced by separate groups to communicate for the first time, expect to spend an extraordinary amount of time getting the services to understand each other. Sorting out semantic meaning and corner cases is far more difficult than deciding on syntax.

## Services Share a Message Bus

Services communicate with each other by sending messages over a shared message bus. SOA proscribes messages to avoid the coupling that comes from services sharing a call stack; if the called service fails silently, the calling service has to wait for it to return. Services use messages in three main styles: request/reply, commands, and events. In request/reply, one service sends a request to another, and dedicates resources, usually a thread, to waiting for the reply. This style leads to coupling almost as tight as when sharing a call stack. One service can send another service a command: a fire-and-forget instruction to do something. The command style leads to modest coupling; the commanding service expects some other service to fulfill the command eventually, but does not dedicate any resources to make sure. A service can simply publish events--notifications that something of interest has happened--without depending on any service to receive the message. Event-based systems of services are very loosely coupled, and can scale up to the limit of the message bus. Monitoring the message bus provides great insight into how well the system works, and creates a reassuring picture for your manager.

My favorite API for messaging is the [Java Messaging Service](http://jcp.org/aboutJava/communityprocess/final/jsr914/index.html) standard. There are [many implementations](http://www.manageability.org/blog/stuff/open-source-jms-java), most of which focus on reliability in enterprise-scale environments, and some of which include APIs for non-Java systems. Some JMS implementations use peer-to-peer technologies to survive transitory internet and wireless networks. I created [SomnifugiJMS](http://somnifugijms.dev.java.net) for messaging between threads in a single Java process for small-scale systems. If you need to scale to something even smaller, try using [`BlockingQueue`](http://java.sun.com/j2se/1.5.0/docs/api/java/util/concurrent/BlockingQueue.html)s from `java.util.concurrent`. For large-scale systems on unreliable networks, try using [JXTA](http://www.jxta.org/) to construct a reliable network.

## Services Are Loosely Coupled

Ideally, services only interact by fulfilling their contracts over the message bus. The closer you can come to that ideal, the better. Try to discover and record hidden dependencies like shared call stacks, static tunnels in singletons, and shared processors, memory, disks, databases, and networks. Any dependency can lurk in the background, waiting to break your system. Be aware of coupling between services on the message bus. A service that issues commands and requests is assuming that some other service will fulfill these commands and requests. Even services that expect only events assume that some other service will publish the event. Try to catalog potential problems, but focus your energy on decoupling specific trouble spots before they matter. Loose coupling between services makes replacing one service with another possible. When your manager asks what will be involved in integrating a replacement service, you will have a sound answer.

A service's reaction to a message should be an atomic action, so services work best as optimistic transaction engines that record and attempt to fix problems. Two-phase-commit transactions across services tightly couple those services. Luckily, most systems larger than a database rarely need to roll back the transaction. Instead, a troubleshooting service in the system needs to be alerted to the problems so that the problems can be sorted out. The troubleshooting service fits surprisingly well into most business workflows because the business wants to reroute the problem transaction instead of wiping it out of existence.

## Services Have Independent Life Cycles

Each service has its own life and life cycle independent of other services. Individual services may be stopped, restarted, and replaced without stopping the whole system. Batching services like end-of-day processes can start, process all pending messages, and stop. A service can join a wireless network briefly, when a connection is available, and then disconnect later without causing harm. You can even replace an obsolete service with a new version without downtime. I haven't found a good standard for turning services on and off, but it isn't that hard to build. Simple volatile flags in a [`Runnable`](http://java.sun.com/j2se/1.5.0/docs/api/java/lang/Runnable.html)'s main loop have worked fine so far. [W3C](http://www.w3.org/TR/wslc/) has a description of possible states and transitions, but it seems like overkill to me. If you start building your own elaborate system, steer towards that W3C standard. The feature you want is the ability to stop one service and start another to replace it, without stopping the whole system.

## Orchestrators Assemble Services into Systems at Runtime

Orchestrators are special services that gather and assemble services into larger systems at runtime. Some orchestrators match contracts to orchestration instructions to registered services. Orchestrators often start the services they need. Assembling a service this way is a lot like using [Simulink](http://www.mathworks.com/products/simulink/description1.html) blocks; you choose the parts, connect them to a message bus, and sometimes stimulate the system with an initial message. [BPEL](http://www-128.ibm.com/developerworks/library/specification/ws-bpel/) and workflow engines like [Dalma](https://dalma.dev.java.net/nonav/maven/index.html) hold a lot of promise for orchestrating large systems, but I haven't used either for more than simple experiments. The java.net website uses Dalma to coordinate registering new projects. For the systems I have actually built, I used simpler, more general-purpose tools like [Jython](http://www.jython.org/) and [Beanshell](http://beanshell.org/) scripts, and simple Java code to orchestrate the services. I haven't found a language I like that lets me specify a workflow yet, although I am hopeful.

## Orchestrators Can Discover other Services Dynamically

Services generally register themselves with a [service locator](http://www.martinfowler.com/articles/injection.html#UsingAServiceLocator). An orchestrator can then use the service locator to find the services it needs dynamically, at runtime. The idea is similar to using the [Java Naming and Directory Interface](http://java.sun.com/products/jndi/) (JNDI) to find the right database connection. I have found service locators much more useful within a single process than on a large scale. I think that's because small systems tend to have a lot of diverse parts, and the larger scale systems I design use events, meaning there's less for them to look up. Systems where distributed services appear and vanish, like the battlefield, the internet, and wireless networks, need reliable large-scale service locators. [JNDI](http://java.sun.com/products/jndi/) works quite well as a service locator on a small scale. [Jini](http://www.jini.org/) works great on a larger scale. Jini can find services that implement a specific Java interface, which is very close to finding services by contract. Others report success with [Universal Description, Discovery, and Integration](http://www.uddi.org/) (UDDI) when some services are not in Java.

## Systems of Services Grow into Systems of Systems

A system composed of services can be a service in its own right. The more that messages are treated like events (instead of requests), the better your system can scale up. Scaling up this way can be the technology jewel in a business plan, and is the most interesting feature for academics and hobbyists. We software engineers need to avoid being too charmed by it. We have to stay focused on the problems at hand. However, compatibility and stability on a large scale will make our next project more gentle.

To make sure that your system of services can be a service in its own right, make sure the larger system has all of the features that a service should have. The larger system should have a strong service contract, be encapsulated, use atomic messages to communicate, be decoupled from other services, have an independent life cycle, and be discoverable. If all of that is true, a larger-scale orchestrator can use your system as service to assemble something bigger.

## Life in the Standards Zoo

A large zoo of standards already exists for Java coders. If you can use some of these standards, you will save yourself some effort now. With a little luck, your choice will help you be compatible with some undiscovered service later. WSDL and Java interfaces help define software contracts and encapsulation. Shared messaging busses can come from an ESB, JMS, or `java.concurrent.BlockingQueue`s. Messages as documents can come from XML or serializable objects. Assembly at runtime can come from business languages or scripting, plus a service locator like JNDI, Jini, or UDDI. New standards roll out every week. I use [JavaOne Online](http://developers.sun.com/learning/javaoneonline/) as a starting point, since these days, Google turns up too many pages trying to sell you something.

Practice some suspicion when you shop for [standards](http://www.artima.com/weblogs/viewpost.jsp?thread=4840). New standards generally haven't been tried in the field. They may solve problems you don't have, and may not solve the problems you care about. Learning how to get the most out of a standard requires some investment of your time; you won't have time to learn many of the standards before the next batch comes out. Welding your project to some new standard involves risk. If you pick the wrong one, you may wind up maintaining a useless, complex layer for a long time. Enterprise computing pundits battle for control of the standards bodies; they want your attention, your participation, and ultimately, want your money.

Getting encapsulated, well-designed services to fit behind some new standard is relatively easy. The standard tools get better in leaps and bounds. My own career shows the evolution. From 1998 to 2000 my team created an SOA framework ourselves. Needing three days to explain what we were selling contributed to the company's demise. In 2001, I was part of a contracting team that built a system of services using JMS, Perl and databases. In 2003 at a new job, we wrote our own WSDL to use with WSIF, JMS, and Jython, and put together a demonstration system of services in about a month. Converting an existing system has taken about a year. We ultimately dropped the WSDL in favor of Java interfaces, and stopped using WSIF. Restructuring the code was wonderfully straightforward, and will get easier over time. In June 2005 (post-JSR-181), creating a Java web service involved adding Sun's reference implementation JARs and adding `@webmethod` annotations to existing code. When JDK 6 provides JSR-181, we get the supporting parts just by adding the annotations.

## Wrapping Up

Service oriented architecture is a collection of ideas and patterns from the 1980s that survived the 1990s. The concepts behind SOA are sound, solid, tested, and proven. SOA ideas directly address details in business plans about how you will deploy, grow, and evolve your system. Creating encapsulated, loosely coupled software that obeys a clear contract requires discipline, but shows immediate benefits. Getting loosely coupled, encapsulated software behind some new web services standard will be easy.

*[David Walend](/pub/au/95) started learning Java with the alpha 3 release in 1994 after a kind computer science professor at Tufts University overheard his tantrum on distributed simulations, memory management, multithreaded code and meteorologists of questionable parentage. *
