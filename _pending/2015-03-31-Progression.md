---
layout: post
title: Option, fold()(), case class, Slick, Spray
comments: True
---

While introducing my work for HMS Catalyst and Shrine, I came up with a good progression to let non-Scala developers get a taste of what scala is about. I introduced Option, fold()(), and case classes, then showed how gentle it is to combine them with Slick and Spray to build a classic web-front to db-can application.

TODO lead with the twitter quote

##Shrine

Shrine lets researchers and doctors for sharing demographic and diagnostic patient data across academic networks. I'm working on a tool to help audit who has researched what so that someone can tell if a researcher is actually studying what she promised. For example, it might be fine for a neonatologist to study outcomes of opiates in infants, but not OK for that person to shop for the best adult ER for a fix. The checks in the system are all honor-based, after-the-fact, audits that require human judgement; the hard part of the project is getting the data out of the system in some way that helps show who is studying what. The back end of the application needs to be simple so we can focus on the more interesting, more important front-end design.

I lucked out with a greenfield project, so I got to pick Spray and Slick for the core technologies. However, I have to explain what I'm doing to Scala novices, and sometimes Scala skeptics. I put together a talk about the good, bad, and ugly of working in Scala with examples from my work that provide a gentle progression. Shrine is all opensource, funded by the NIH, so it seemed like good fodder for a blog entry.

The core parts for my web app are Option, Option's fold()() method, and case classes. Those parts let me show just a little functional programming and show of Scala's capabilities as "a better Java."

##Option

##fold()()

##A case class

##A table in Slick

##Composable Queries in Slick

##A Spray Route

##Getting URL Parameters via a Directive

##A Custom Directive

