---
layout: post
title: Bounding Complexity in Scala Projects
description: "Li Haoyi's Principle of Least Power, applied to three of my own Scala projects. Scala works best as your own little language, kept deliberately small."
comments: True
tags:
  - post
  - Scala
  - Scala-Basics
aliases:
  - /bounding-complexity-in-scala-projects/
---

Li Haoyi wrote a masterful blog entry [Strategic Scala Style: Principle of Least Power](https://www.lihaoyi.com/post/StrategicScalaStylePrincipleofLeastPower.html). It is a reaction to Tim Berners-Lee's personal notes on W3, [Principles of Design](https://www.w3.org/DesignIssues/Principles.html) . Berners-Lee's section on "The Principle of Least Power" opens with:

> The choice of language is a common design choice. The low power end of the scale is typically simpler to design, implement, and use, but the high power end of the scale has all the attraction of being an open-ended hook into which anything can be placed: a door to uses bounded only by the imagination of the programmer.

> Computer Science in the 1960s to 80s spent a lot of effort making languages which were as powerful as possible. Nowadays [1998?] we have to appreciate the reasons for picking not the most powerful solution but the least powerful.

That doesn't bode well for Scala - one of the most powerful languages in use. Scala has a Turing-complete compile-time type system. In this blog entry I hope to reconcile these grand architecture-level ideas by bounding how much of Scala's complexity to allow in a project.

First, allow me to defuse Berners-Lee's concerns. The preamble to the above quote is:

> In choosing computer languages, there are classes of program which range from the plainly descriptive (such as Dublin Core metadata, or the content of most databases, or HTML) though logical languages of limited power (such as access control lists, or conneg content negotiation) which include limited propositional logic, though declarative languages which verge on the Turing Complete (Postscript is, but PDF isn't, I am told) through those which are in fact Turing Complete though one is led not to use them that way (XSLT, SQL) to those which are unashamedly procedural (Java, C).

He goes on to say:

> The reason for this is that the less powerful the language, the more you can do with the data stored in that language. If you write it in a simple declarative from, anyone can write a program to analyze it in many ways. The Semantic Web is an attempt, largely, to map large quantities of existing data onto a common language so that the data can be analyzed in ways never dreamed of by its creators. If, for example, a web page with weather data has RDF describing that data, a user can retrieve it as a table, perhaps average it, plot it, deduce things from it in combination with other information. At the other end of the scale is the weather information portrayed by the cunning Java applet [remember 1998]. While this might allow a very cool user interface, it cannot be analyzed at all. The search engine finding the page will have no idea of what the data is or what it is about. This the only way to find out what a Java applet means is to set it running in front of a person.

These examples are data structure examples, specifically decoupling data from code. During the 1990s book layout evolved into data structure representation, leaving a fossil record from SGML to HTML to XML. It seems to have resolved with JSON from JavaScript in the 2000s. This was a big deal at the time, and Dr. Berners-Lee played a fantastic lead part. However, you could narrow the word "language" to "data serialization structure" and have an argument that better-matches the examples.

Anyone proposing to use the in-memory bytes that make a Scala case class outside of memory might be demonstrating [successful cryogenic revival](https://www.google.com/search?client=firefox-b-1-e&q=futurama+i+c+wiener#fpstate=ive&vld=cid:e0f6d940,vid:tIBmNOJZdWA,st:0) from the early Clinton era. It would stand out as an absolutely terrible proposal given all the [options available for JSON serialization in Scala](https://index.scala-lang.org/search?sort=stars&q=json&page=1): circe, upickle, play-json, zio-json, json-lenses, json4s, akka-http-json, tethys, nestorpersist, rojoma-json, sbt-json, jawn, argonaught, dijon, scalajson, scalajack, ...

I'll get back to language and complexity in a bit. This huge, incomplete list of JSON libraries highlights a related problem.

# Abundance in the Ecosystem

Scala started life piggybacking on the Java Virtual Machine's enormously successful ecosystem. Scala has always had access to an abundant ecosystem of Java libraries. Because the Scala language is so well structured we tend to pick and choose libraries instead of locking ourselves into frameworks. (Contrast with Ruby on Rails.) As a community we are very comfortable creating new solutions - new libraries - when old solutions don't match the problems of the day. Mostly that's for the better, but it does lead to a fractured community and complexity from the viable number of choices. Martin Odersky complained that we were not "Scala programs" but were "Cats programmers, or Akka programmers, or Spark programmers."

# ...and Abundant Language Features

The Scala language is actually quite small, with remarkably few caveats. However, many language-like features come in via the standard library. Scala is multi-paradigm; I've seen it work well for object-oriented programming, functional programming, declarative programming, procedural-style programming and even aspect-oriented programming. Further, in Scala it is very natural to make your own new control structures to fit your project's needs.

One common complaint is that Scala has a steep learning curve. I don't think that's true; I have taught 4th-graders how to write some useful Scala. It is easy to get started. The problem is not the steepness; the problem is the height of the curve.

When I ask for help from a typical Scala Users' Group often the answer is "Go read and understand [something I never even knew was there]." I value learning new things, but often want to learn separate from getting the job done.

> "Experience is what you get when you didn't get what you wanted." - Randy Pausch

Further, the Scala language often has multiple ways to get the same result. I think that leads directly to Li Haoyi's [Principle of Least Power](https://www.lihaoyi.com/post/StrategicScalaStylePrincipleofLeastPower.html) examples. Smart academics do amazing things with the language, but maybe that's not the right choice for your project. To get non-academic work done in an ecosystem this rich you need to set some boundaries for your project. You can control the height your developers need to climb by deciding to use simpler and fewer parts of Scala.

# Audience

I don't agree with Li Haoyi that "Complexity is your enemy." A project's ability to handle complexity is more like a scarce resource. Scala lets you treat complexity like items on a menu where other languages, frameworks, and ecosystems offer a fixed-price of complexity. Academics can afford an abundance of complexity. The rest of us, [not so much](https://www.google.com/search?client=firefox-b-1-e&sca_esv=568821e4bd74bee9&sca_upv=1&sxsrf=ACQVn0915nVZxnE9GxYNe--dLEfZ9tuPrQ:1714501579949&q=la+story+patrick+stewart&tbm=vid&source=lnms&prmd=ivnsbmtz&sa=X&ved=2ahUKEwi6zY6NyOqFAxX1ElkFHRRLApIQ0pQJegQIChAB&biw=1290&bih=913&dpr=2#fpstate=ive&vld=cid:ad5b044b,vid:C1IRqqp8vHw,st:0).

Think about who is going read and write your code to get some idea of what budget you have for complexity, and who might be using the software. You need to set expectations so that your audience is not surprised when they need to learn new skills to contribute.

I think the most important question to answer is "What do you expect people to do with the systems you create?" The people might be users, system admins, support crew, or future developers; there will be different audiences for different roles. They'll bring different levels of skill and expectations.

# Three Examples:

## [SHRINE](https://open.catalyst.harvard.edu/stash/projects/SHRINE/repos/shrine/browse)

SHRINE allows a researcher at any hospital in a network to query patient records at all hospitals in that network with the same query – without violating HIPAA. The audience includes researchers, local and network admins, and future software developers. (I just finished my work on SHRINE, which involved a lot of writing to archive it for future developers. I've been thinking about this issue a lot lately.)

SHRINE's users are pragmatic medical researchers; they are brilliant people but not computer scientists. The researchers drag-and-drop term labels in boxes to form logical queries for patients they hope to study. The researchers are using a visual domain-specific query language; behind the curtain it is all JSON.

The local and network admins mostly use Unix skills, [HOCON via Typelevel Config](https://github.com/lightbend/config), and peek inside databases and logs to bracket and understand problems. The admins are very capable with Unix and python scripts, but most of their interaction with SHRINE is via a single HOCON configuration file. It is extremely unusual to see any of them use any HOCON beyond the basic key/value pairs. (In the narrow realm of setting up SHRINE they are safe from Dr. Berners-Lee's fear of attraction to powerful language features.)

I left future SHRINE developers with a wiki entry opening with:

> SHRINE uses Scala 2.13.x for all of its back-end code. The Scala code style is functional and highly monadic. It features shallow object-oriented components - often comprised of shared parts - to separate concerns. This lets the code explain the details itself. We build it with Maven - the easiest system for our operations team to support. SHRINE uses http4s for its web API, cats effects and fs2 for concurrency, CQRS via slick for storing and retrieving state. SHRINE sends commands between nodes using MOM (AWS SQS, Kafka, or a home-grown REST API), circe for encoding JSON, i2b2 as a source of patient data, and Scala's xml library to create and read i2b2's xml. SHRINE stores very little state outside of stack references.

That opening lists out the core technologies and the minimum skill set to bring. A developer familiar with http4s, cats effects, and distributed programming would likely be able to contribute as soon as they understand the problem SHRINE solves. I would expect a generally capable Scala developer to "go read about" all of those technologies and get some level of how SHRINE uses them before attempting to make changes to SHRINE's code base. It's a punch-list like you would find in a job description.

In 2008 SHRINE began as a "Scala as a better Java" project that used Jakarta and Scala's in-line XML capability to imitate and distribute a single-hospital query system's web API. We were able to grow SHRINE from those initial decisions while keeping the whole works compatible release-to-release (mostly). SHRINE's transformation is a remarkable demonstration of the [power of refactoring](https://www.lihaoyi.com/post/StrategicScalaStylePrincipleofLeastPower.html#dont-fear-refactoring) in Scala Li Haoyi finds so compelling.

## [ev3dev-lang-scala](https://github.com/dwalend/ev3dev-lang-scala)

ev3dev-lang-scala is a library and toolkit for programming Lego Ev3 robots using Scala. Most programmers using the library are kids ages 9 to 13, mostly programming robots for [FIRST Lego League](https://www.firstinspires.org/robotics/fll/game-and-season). I've created a library that gives them a subset of the Scratch-like tool Lego provides. To keep things fair the library does not give them anything more than what Lego's base-level blocks provide, but they do have access to all of Scala. I try to get them to use some object-oriented containment to keep it easy to explain. Individual kids do not value that in their own work but complain when another kid makes a mess of it, especially while making presentations days before an FLL tournament. Most code the kids write is very procedural, like this method to drive the robot (backwards) to a "museum" objective:

```scala
  private def startToMuseum(): Unit = {
    Robot.moveStraightBackward(635.millimeters)
    Robot.leftRotation(135.degrees)
    Robot.moveStraightBackward(100.millimeters)
    Robot.leftRotation(100.degrees)
    Robot.moveStraightBackward(570.millimeters)
    Robot.rightRotation(135.degrees)
    Robot.rightRotation(180.degrees)
  }
```

The kids surprised me when they used a recursive loop to use feedback from a gyroscope to make precise turns:

```scala
  @tailrec
  def rightRotation(goalHeading:Degrees):Unit = {
    val heading: Degrees = Gyroscope.readHeading(SensorPort.One)
    val toGo: Degrees = goalHeading - heading
    val speed: DegreesPerSecond = (Robot.speed.v * (toGo.v/90)).degreesPerSecond

    Log.log(s"heading is $heading, speed is $speed")
    if(goalHeading > heading) {
      Movement.startMoving(speed,-speed)
      rightRotation(goalHeading)
    } else {
      Movement.stop()
    }
  }
```

To trim back their cut-paste tendencies I want to show them higher-order functions this year. A general feedback loop might be the thing, but they resist refactoring. "It works fine. Why change it?" They do not get it.

The other audience is library developers - just me so far. To make this thing work I had to learn the basics of interfacing with the [ev3dev OS](https://www.ev3dev.org/) (a variant Debian Linux!) and how to use that interface efficiently from inside the JVM. To get the control loops running at ~200 Hz after hot-spot warm-up the core uses Java NIO calls to read and write unix streams, very much "Scala as a better Java" in style:

```scala
case class ChannelRewriter(path: Path,bufferLength:Int = 32) extends AutoCloseable {

  private val channel = FileChannel.open(path,StandardOpenOption.WRITE)
  private val byteBuffer = ByteBuffer.allocate(bufferLength)

  def writeString(string: String):Unit = this.synchronized{
    byteBuffer.clear()
    byteBuffer.put(string.getBytes (StandardCharsets.UTF_8) )
    byteBuffer.flip()
    channel.truncate(0)
    channel.write(byteBuffer, 0)
    channel.force(false)
  }

  def writeAsciiInt(i: Int):Unit = writeString(Integer.toString(i))

  def close():Unit = this.synchronized{
    channel.close()
  }
}
```

I don't expect the kids to work at this level, but a beginner Scala developer with a Unix background and familiarity with Java's NIO API should be able to contribute. On their best days the kids will use the IDE to follow calls down from their own code into the library to see how things work.

You'll notice the kids' code refers to measured units like `.millimeters`, `.seconds`, and `.degrees` - Scala value classes. I have figured out how to program the Scala3 type system to understand measured units in arithmetic - some number of `degrees` divided by some number of `seconds` is `degrees/seconds`. I'm of two minds deciding if it is the right thing to do. It would save the kids having to dig out the values via `.v` to do their arithmetic, then rewrap up the result to have the correct type (all cooked out in the compiler via Scala's value class feature). However, it would add type-level arithmetic programming to the inner workings of the library code - a leap up the learning curve from "Scala as a better Java." I don't yet know what the right decision is.

Scala lets me put that decision off. The language supports the complex types.

## [Disentangle](https://github.com/dwalend/Disentangle)

Disentangle is a library of graph algorithms I use mostly for my own entertainment. (I did use the library at ActivateNetworks for analyzing social networks for marketing.) I implemented graph minimization algorithms - like Dijkstra's shortest path algorithm - with general-purpose semirings. The same algorithm code can find things like least-probable paths instead. To use an algorithm a developer needs to understand how to use Scala's tuple structures and collections library - entry-level Scala skills:

```scala
  /**
   * Edges are just a Seq of Tuple3[Node,Node,Edge]
   */
  lazy val edges: Seq[(String, String, String)] = Seq(
                                                  ("A","B","ab"),
                                                  ("B","C","bc"),
                                                  ("C","D","cd"),
                                                  ("D","E","de"),
                                                  ("E","F","ef"),
                                                  ("E","B","eb"),
                                                  ("E","H","eh"),
                                                  ("H","C","hc")
                                                )

  /**
   * Generate all the shortest paths in the graph
   */
  lazy val simpleShortPathLabels: Seq[(String, String, Option[FirstStepsTrait[String, Int]])] = Dijkstra.allPairsShortestPaths(edges)
```

I use Scala's generics to keep the types lined up right for different semirings, but otherwise the code is using shallow object-oriented ideas to keep different concerns separated. Scala's solid handling of generics for Disentangle is what first drew me into Scala. Here's a semiring for finding most-probable paths:

```scala
  object MostProbableSemiring extends Semiring {

    val I = 1.0
    val O = 0.0

    def inDomain(label: Label): Boolean = {
      I >= label && label > O
    }

    def summary(fromThroughToLabel:Label, currentLabel:Label):Label = {
      if(fromThroughToLabel > currentLabel) {
        fromThroughToLabel
      }
      else currentLabel
    }

    def extend(fromThroughLabel:Label,throughToLabel:Label):Label = {
      if ((fromThroughLabel == O) || (throughToLabel == O)) O
      else {
        fromThroughLabel * throughToLabel
      }
    }
  }
```

The core idea behind the library is to write algorithm code that looks identical to the pseudocode in fat algorithm books like [CLRS](https://www.amazon.com/Introduction-Algorithms-3rd-MIT-Press/dp/0262033844). Here's the Floyd-Warshall algorithm demonstrating "Scala as a better ~~Java~~ Fortran" :

```scala
  /**
   * O(n^3)
   */
  def floydWarshall[Node,Label,Key](labelDigraph:MatrixLabelDigraph[Node,Label],support:SemiringSupport[Label,Key]):IndexedLabelDigraph[Node,Label] = {
    val innerNodes = labelDigraph.innerNodes
    for (k <- innerNodes; i <- innerNodes; j <- innerNodes) {
      val summaryLabel = relax(labelDigraph,support.semiring)(i,k,j)
      labelDigraph.upsertEdge(i,j,summaryLabel)
    }
    labelDigraph
  }
```

There's this split between how different audiences will interact with the code. Someone could just use this library in a project with an entry-level understanding of Scala. To add new algorithms you need Scala generics to keep the code type-safe.

# In Contrast: My Early Career

My first job out of school involved converting Matlab code and Excel spreadsheets into Fortran (... and postscript). The third and fifth projects were converting Matlab into Objective C . The seventh project was an attempt to convert a system in C to Java. (It failed.) My eighth through twelfth projects were converting Matlab into Java. My second Scala project was translating R code into Scala.

I did take a job at MathWorks after all that Matlab translation. Jack Little, founder of MathWorks, pointed out that, "You can write a lot of really terrible Matlab code really fast. That's one of its greatest strengths." I get that as a marketing plan for MathWorks, an action plan for a researcher, and a business plan for a start-up. All that recoding paid my student loans, rent, and kept me in food for my early career, but was somewhat unsatisfying. I did observe that once a project chose a production ecosystem then that choice was for the life of the project. If the language or ecosystem didn't provide something that the project needed then that venture failed. Big rewrites were too expensive.

# Scala is Best as Your Little Language

Scala libraries regularly evolve into domain-specific languages as the authors get more understanding about how to write concise, clear code. The Scala community takes a lot of pride in that. Here's some SHRINE code that uses [http4s](https://http4s.org/v1/docs/dsl.html)' end-point DSL:

```scala
    case request @ POST -> Root / "startQuery" as user => startQuery(request,user)

    case request @ POST -> Root / "changeQueryNameAndNotes" / LongVar(queryId) as user => changeQueryNameAndNotes(queryId, request, user)

    case _ @ GET -> Root / "query" / LongVar(queryId) as user => getQuery(queryId, user)
```

In Scala the line between what's "just a library" vs "what is a DSL" is pretty blurry. We bring these into code via `import org.http4s.dsl...` but pieces we're importing are masterfully-designed `unapply` methods to be used in `case` statements. There's no new parser, no changes to a compiler, no magic plugins, not even annotations. It just lets our team write concise, clear Scala code.

By choosing which parts of Scala to use and which to leave out we can define the right little language for each project. Changes to these decision have an incremental, bound cost ; if we need to make a different choice in the future we can either let some new kind of complexity in, or refactor to simplify. That's a tremendous benefit. It helps Scala projects live long, healthy lives by letting them adapt to changing needs.
