---
layout: post
title: "Coupling in Software Architecture"
date: 2004-01-11
permalink: /archive/2004/01/coupling-in-software-architecture/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2004/01/coupling_in_sof.html
javanetTopics:
  - Programming
---

Coupling in software architecture seems to form a spectrum, based on what has to change to make the system do something different. At one end of the spectrum are dissociated ubiquitous services, like those envisioned by JXTA. At the other end are the highly-coupled systems of architectural nightmares. In between I've identified configured services, component systems, and client-server systems. Are there other styles in the spectrum? Is this a valid view of them, or should I be thinking about something else entirely?

**Dissociated Ubiquitous Services are Assembled On-the-fly by Discovery**

Dissociated ubiquitous services are services that are simply put in place and act in a responsive role. A master program assembles the software system by finding the needed parts in-situ, and has to handle cases when the services are not available. The services have a very simple, very well defined API established in advance, and communicate with simple protocols that meet simple contracts. Substituting one service for another with an identical contract is effortless and generally unnoticed. These substitutions are assumed to be unimportant and can be difficult to control. Understanding the system requires
understanding the assumptions about the ubiquitous resources and how they should be used.

One example of this is a topic-based messaging system: The message producers launch messages out into the world, even if nothing is consuming them. Another example is web services coordinated with UDDI lookups: The orchestration describes what contracts the services need to obey. An interpreter tries to locate the services, then call them in order. As I understand it, JXTA is designed to work the same way.

**Known Services are Assembled at Run Time by Configuration**

Known services can be assembled at run time using a configuration script, usually without restarting the system. To support this, related services will feature a common protocol, usually the same protocol used in ubiquitous services. Families of services have simple, well defined APIs that use the common protocol for input and output. Substituting one service for another with an identical contract is trivial and easy to control by changing the configuration. Understanding the system requires understanding the service contracts and how the services are called. This is probably the easiest
model to understand. However, it forces the system to fit a simple procedural model with tightly controlled system state.

An example of a system of services is a queue-based messaging federation: One service can pass messages through a gateway, another can monitor message
flow in the system, and another can emit or receive messages. A central coordinator starts, stops and monitors the services. Another example is web services where the orchestration does not use UDDI lookups: A central script tells how to construct the system and how XML documents flow through it. A third example is Mathworks Simulink building blocks: each block accepts input signals from other blocks, and produces its own signal. Constructing the system is a matter of assembling the blocks visually.

**Components are Integrated at Compile Time by Glue Code**

Components are easy to work with at a code level: their API is well defined, and families of components will share some objects used in API. To link components together, a developer creates glue code to translate the output of one component into the input of the next. Understanding the system requires understanding the input and output of the components, and how they should link together. Changing the system requires modifying the glue code and recompiling. Because the components can be isolated from each other and their inputs make sense, testing is a matter of setting up the input and
checking the output. Most object-oriented architecture aims for this level of coupling. I think the component level of decoupling is the bottom limit for reusability.

An example of a system of components is Java's Swing framework: A developer can create a rich user interface by selecting widgets (like buttons and text fields) from a library, and writing glue code to combine the widgets inside container objects. The containers use LayoutManagers (also chosen by the developer) to decide where to place the widgets. A developer can assemble a user interface quickly. But changing the user interface means changing the code and recompiling.

**Client-Server systems are integrated at Design Time by Well-Defined API**

The client-server model focuses decoupling at a specific layer of the system, between the client and the server. The API is well defined and specific to the details of talking across the layer. Any client should work with any server, provided both meet the contract of the layer. Everywhere else, the system is tightly coupled. A developer decides what he's creating -- either a client or a server -- and implements the contract for that side of the layer. Understanding the system means understanding the layer, plus what a given client and a given server are doing. The system can be changed by working with the ad-hoc code in an existing client or server, or by creating a new client or server. Testing is easy at the client-server boundary, but difficult everywhere else. Clients and servers are hard to reperpose; problems with similar requirements for these larger parts are rare.

An example of a client-server system is a custom report generator (the client) for a database (the server): The database's tables are fixed and well-defined, so the report can send SQL queries to the database and build reports out of the result sets. Other clients might allow data entry or analysis of the database. Because the database's protocol is well-defined, another brand of database could be substituted as a server with little impact for the clients. (At least that's the theory. Database vendors almost always tweak SQL just a little to lock in their customers. These tweaks adjust the protocols at the client - server layer, breaking the contract.)

**More Coupled Systems Must be Redesigned or Hacked**

Some systems are so tightly coupled that no layer exists where the system can be tested. The system is too interdependent to break into smaller pieces. Testing is limited to testing the whole system all-at-once. Understanding the system requires understanding all of the interdependencies. Changing the system means revisiting the original design and propagating all the changes through the dependencies. For large systems, no developer will understand the whole system. We will program by coincidence -- if it doesn't crash, it must be OK. I won't list examples for these because I think we've all seen them. I have heard claims that the system got built this way because of strict performance requirements, but haven't seen that in practice.
