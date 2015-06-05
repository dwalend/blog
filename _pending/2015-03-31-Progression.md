---
layout: post
title: Option, fold()(), case class, Slick, Spray
comments: True
---

While introducing my work for Shrine at HMS Catalyst, I came up with a good progression to let non-Scala developers get a taste of what scala is about. I introduced Option, fold()(), and case classes, then showed how gentle it is to combine them with Slick and Spray to build a classic web-front to db-can application.

##Shrine

Shrine lets researchers and doctors for sharing demographic and diagnostic patient data across academic networks. I'm working on a tool to help audit who has researched what so that someone can tell if a researcher is actually studying what she promised. For example, it might be fine for a neonatologist to study use of opiates in infants, but not OK for that person to shop for the ER that proscribes the most oxycodone. The checks in the system are all honor-based, after-the-fact, audits that require human judgement.

 The project contains a lot of complexity from wrapping a legacy search tool heavy with XML, privacy concerns, and presenting jargon-filled cryptic queries to non-programmer, non-medical stewards. I kept the back-end simple so we can focus on the more interesting, more important front-end design.

I fell into a greenfield project, so I picked Spray and Slick for the core technologies. However, I have to explain what I'm doing to Scala novices, and sometimes Scala skeptics. I put together a talk about the good, bad, and ugly of working in Scala with examples from my work that provide a gentle progression. Shrine is all open source, funded by the NIH, so it seemed like good fodder for this blog entry.

The core parts for my web app are Option, Option's fold()() method, and case classes. Those parts let me show just a little functional programming and show of Scala's capabilities by plugging directly into Slick and Spray. I think this approach goes a long way toward [Twitter's style ideal](TODO link and quote) .

##Option

During the talk I went over how great functional programming is, but the only functional programming I showed was Option and Option's fold()() method. I had way too much else to say.

An Option is a type-safe way to handle potentially missing information, a much better alternative to passing and checking nulls:

Option is an abstract class with two subclasses: Some, used when a value is present; and None, used when no value is present.

Option takes a type parameter, Option\[t\], so that the compiler knows the type of a potential value.

```Scala
val someString:Option[String] = Some("some string")
val noString:Option[String] = None
```

##fold()()

Option's fold()() method takes two functions

```Scala
def fold[Out](ifEmpty: ⇒ Out)(f: (T) ⇒ Out): Out
```

Some[T].fold()() evaluates the right function with the value as an argument

None[T].fold()() evaluates the left (no-argument) function

```Scala
scala> val stringToPrint = noString.fold(".")(string => s"!$string!")
stringToPrint: String = .

scala> val stringToPrint = someString.fold(".")(string => s"!$string!")
stringToPrint: String = !some string!
```
(This also gave me an excuse to open up and show off the Scala REPL, always a hit with people trapped by their compiler and build system.)

##A case class

##A table in Slick

##Composable Queries in Slick

##A Spray Route

##Getting URL Parameters via a Directive

##A Custom Directive

