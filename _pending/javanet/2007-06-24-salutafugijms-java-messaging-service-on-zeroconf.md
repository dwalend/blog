---
layout: post
title: "SalutafugiJMS -- Java Messaging Service on ZeroConf"
date: 2007-06-24
permalink: /archive/2007/06/salutafugijms-java-messaging-service-on-zeroconf/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2007/06/salutafugijms_j_1.html
---

[SalutafugiJMS](https://salutafugijms.dev.java.net/) is a peer-to-peer implementation of the [Java Messaging Service specification](http://jcp.org/en/jsr/detail?id=914) that uses [ZeroConf DNS-SD discovery](http://www.dns-sd.org/) and TCP sockets to communicate in a distributed computing system. I built it after seeing [Daniel Steinberg's JavaOne talk on ZeroConf](http://developers.sun.com/learning/javaoneonline/2007/pdf/TS-1916.pdf). SalutafugiJMS uses [SomnifugiJMS](https://somnifugijms.dev.java.net/) as a skeleton and [Apple's Bonjour implementation of ZeroConf](http://developer.apple.com/networking/bonjour/) for muscle inside special SomnifugiJMS [FanOuts](https://somnifugijms.dev.java.net/nonav/api/net/walend/somnifugi/channel/FanOut.html) and [Channels](https://somnifugijms.dev.java.net/nonav/api/net/walend/somnifugi/channel/Channel.html). SalutafugiJMS eliminates the central (or federated or clustered) message broker found in traditional JMS implementations and the need to manage specific services required by traditional DNS-SD systems. Name the JMS Queues and Topics for information your system needs to exchange. Your system consumes what your system needs. Your system sends out what it chooses. SalutafugiJMS takes care of the rest, leaving your system very loosely coupled.

**Broker-Free JMS**

In a traditional JMS application, message producers and message consumers don't have to know about each other. That feature creates [highly decoupled systems](http://today.java.net/pub/a/today/2006/04/04/understanding-service-oriented-architecture.html#share-message-bus). However, message producers and consumers all have to get connections to the same JMS message broker. That shared knowledge about the JMS broker usually comes from magic connection url strings to summon objects out of JNDI servers. Getting those magic strings correct is tedious; many elaborate projects focus on abstracting away those strings, sometimes to the point of programming in XML. SalutafugiJMS is a peer-to-peer system -- producers send messages directly to consumers -- while remaining highly decoupled. The only magic string for you to wrangle is the name of the JMS Topic or Queue. No central broker exists; the system can handle failures in any single service and keep going.

**Anonymous ZeroConf**

In a traditional ZeroConf system, ZeroConf provides [service discovery](http://today.java.net/pub/a/today/2006/04/04/understanding-service-oriented-architecture.html#discover-dynamically); a service registers itself so that applications can discover and use it. Those applications browse for the services they need, and resolve them by name. The system is loosely coupled at build time, but becomes very tightly coupled as soon as the application resolves the services at runtime. If the application depends on a service that fails midway through a run, that application suffers. SalutafugiJMS adds JMS' anonymous endpoints to ZeroConf to eliminate that tight coupling. Behind the curtain, SalutafugiJMS consumers register what Queue or Topic they wish to receive messages from. SalutafugiJMS manages browsing and resolving the services inside the producers. Your applications simply produce and consume messages in the system when they need to.

**Building SalutafugiJMS**

I spent about thirty hours' total reading, designing and coding to get messages flowing between JMS Topic Publishers and Subscribers. Bonjour's programmers' interface is a little call-back heavy. Stopping all the services' monitor threads took some thought and a little reworking of SomnifugiJMS. Daniel and Stuart Cheshire's book was very good; everything worked like they said it would. Getting to the initial release was easy and fun. I'd hoped to be able to mine the effort for half-a-dozen blogs, but I think I'll only get two -- one on Thread.sleep(), and one comparing ZeroConf, JXTA and JINI.

The only aggravating part was getting the Bonjour dns_sd.jar from Apple. I do most of my work on an older G4 Mac (amazingly long battery life). Apple's Bonjour page provided a windows .exe installer to get at that dns_sd.jar. I got the jar from a friend with a newer Intel Mac. Daniel tells me I could have pulled in the [Bonjour source code](http://developer.apple.com/opensource/internet/bonjour.html) and built the dns_sd.jar myself after all. I've gotten very used to Java's jar-based library distribution. I normally only pull in source code to help fix problems and add features. I didn't even think to look.

SalutafugiJMS' first release is very much alpha-0-1, JMS Topics-only, and missing many features. SalutafugiJMS seems a little slow and I haven't looked into why. I haven't used SalutafugiJMS in any of my own applications yet, so downloader beware. Alpha-0-2 will focus on logging and fault management, alpha-0-3 on filling in features for Topics.

If you're more interested in broker-free JMS now and can swallow a GPL (or maybe MPL) license, have a look at [MantaRay](http://sourceforge.net/projects/mantaray/). I think they use a proprietary multicast protocol, not ZeroConf. They've had a working peer-to-peer JMS for a few years.
