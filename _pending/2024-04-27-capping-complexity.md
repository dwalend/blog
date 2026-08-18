The Principle of Least Power:
Capping Complexity in Scala Projects
                          
Li Haoyi wrote a masterful blog entry Strategic Scala Style: Principle of Least Power https://www.lihaoyi.com/post/StrategicScalaStylePrincipleofLeastPower.html . It uses the same words as Tim Berners-Lee's personal notes on W3, Principles of Design https://www.w3.org/DesignIssues/Principles.html . Berners-Lee's section on "The Principle of Least Power" opens with 

```ignorelang
 The choice of language is a common design choice. The low power end of the scale is typically simpler to design, implement, and use, but the high power end of the scale has all the attraction of being an open-ended hook into which anything can be placed: a door to uses bounded only by the imagination of the programmer.

Computer Science in the 1960s to 80s spent a lot of effort making languages which were as powerful as possible. Nowadays [1998?] we have to appreciate the reasons for picking not the most powerful solution but the least powerful.
```
As a Scala developer that's worrying advice. I like to use one of the most feature-rich languages. For example, Scala has a Turing-complete compile-time type system. In this blog entry I hope to reconcile these grand architecture-level ideas by bounding how much of Scala's complexity to allow in a project.

First, allow me to defuse Berners-Lee's concerns. The preamble to the above quote is:

```ignorelang
In choosing computer languages, there are classes of program which range from the plainly descriptive (such as Dublin Core metadata, or the content of most databases, or HTML) though logical languages of limited power (such as access control lists, or conneg content negotiation) which include limited propositional logic, though declarative languages which verge on the Turing Complete (Postscript is, but PDF isn't, I am told) through those which are in fact Turing Complete though one is led not to use them that way (XSLT, SQL) to those which are unashamedly procedural (Java, C). 
```

He goes on to say:

```ignorelang
The reason for this is that the less powerful the language, the more you can do with the data stored in that language. If you write it in a simple declarative from, anyone can write a program to analyze it in many ways. The Semantic Web is an attempt, largely, to map large quantities of existing data onto a common language so that the data can be analyzed in ways never dreamed of by its creators. If, for example, a web page with weather data has RDF describing that data, a user can retrieve it as a table, perhaps average it, plot it, deduce things from it in combination with other information. At the other end of the scale is the weather information portrayed by the cunning Java applet [remember 1998]. While this might allow a very cool user interface, it cannot be analyzed at all. The search engine finding the page will have no idea of what the data is or what it is about. This the only way to find out what a Java applet means is to set it running in front of a person.
```
     
These examples are all about data structures, specifically decoupling data from code. During the 1990s book layout evolved into data structure representation, leaving a fossil record from SGML to HTML to XML, that seems to have ended with JSON as Javascript became a dominant standard in the 2000s. It was a big deal at the time, and Dr. Berners-Lee played a fantastic lead part. However, you could narrow the word "language" to "data serialization structure" and have a paragraph that matches the examples. 

Anyone proposing to use the in-memory bytes that make a Scala case class outside of memory might be proof of time travel, or at least successful cryogenic storage https://www.google.com/search?client=firefox-b-1-e&q=futurama+i+c+wiener#fpstate=ive&vld=cid:e0f6d940,vid:tIBmNOJZdWA,st:0 from the early Clinton era. It would stand out as an absolutely terrible proposal given all the options available https://index.scala-lang.org/search?sort=stars&q=json&page=1  : circe, upickle, play-json, zio-json, json-lenses, json4s, akka-http-json, tethys, nestorpersist, rojoma-json, sbt-json, jawn, argonaught, dijon, scalajson, scalajack, ...
                         
I'll get back to language and complexity in a bit. This huge, incomplete list of json libraries highlights a related, more general problem.

Complexity From an Abundance Ecosystem 

Scala started life piggybacking on the Java Virtual Machine's enourmosly successful ecosystem. Scala has always had access to an abundant ecosystem of Java libraries. Martin Odersky complained that as a community we were not "Scala programs" but were "Cats programmers or Akka programers." We got very used to that and very comfortable creating new libraries. This many choices leads to a different sort of problem for Scala projects. 

and Abundant Languate Features

The Scala language has a lot of features. It is multi-paradigm; I've seen it work well for object-oriented programming, functional programming, declaritive programming, and procedural-style programming. I don't doubt it could do more. 

Smart academics do amazing things with the language. One common complaint is that Scala has a steep learning curve. I don't think that's true; I have taught 4th-graders how to write some useful Scala. It's easy to get started. The problem is not the steepness; the problem is the height. Academics do amazing things with a few lines of Scala and sometimes leave the rest of us behind. When I ask for help from a typical Scala Users' Group often the answer is "Go read and understand [something I never even knew was there]." I value learning new things, but often want to learn separate from getting the job done. "Experience is what you get when you didn't get what you wanted." -
Randy Pausch.

Further, the Scala language often has multiple ways to get the same result. I think that leads directly to Li Haoyi's Principle of Least Power essay and its applications. To get non-academic work done in an ecosystem this rich you need to set some boundaries for your project. 

Audience

I don't agree with Li Haoyi that "Complexity is your enemy." A project's ability to handle complexity is more like a scarce resource. Think about who is going to use your code and who might write it to get some idea of what budget you have for complexity. The people might be users, system admins, support crew, or future developers; there will be different audiences for different levels. They'll bring different levels of skill. You need to set expectations. Scala lets you treat complexity like a budget that you spend miserly where other languages, frameworks, and ecosystems offer more of a fixed price.

I think the most important question to answer is "What do you expect people to do with the systems you create?" The people might be users, system admins, support crew, or future developers; there will be different audiences for different levels. They'll bring different levels of skill and expectations.

Three examples from my recent experience:

SHRINE https://open.catalyst.harvard.edu/stash/projects/SHRINE/repos/shrine/browse

I'm thinking about this issue mostly because I have wrapped up work on SHRINE and archived it for future developers. SHRINE allows a researcher at any hospital in a network to query patient records at all hospitals in that network with the same query – without violating HIPAA. The audience includes researchers, local and network admins, and future software developers.

SHRINE's users are pragmatic medical researchers; they are brilliant people but not computer scientists. The researchers drag-and-drop  term labels in boxes to form logical queries for the patients they hope to find. The researchers are using a domain-specific query language they see; behind the curtain it is all JSON. 

The local and network admins mostly use unix skills, HOCON via Typelevel Config https://github.com/lightbend/config , and peek inside databases and logs to bracket and understand problems. The admins are very capable with unix and python scripts, but most of their interaction with SHRINE is via a single HOCON configuration file. It is extremely unusual to see any of them use more than the basic key/value pairs of HOCON's features. In the narrow realm of setting up SHRINE they don't seem to share Dr. Berners-Lee's attraction to powerful language features.

I left future SHRINE developers with a wiki entry opening with:

```ignorelang
SHRINE uses Scala 2.13.x for all of its back-end code. The Scala code style is functional and highly monadic. It features shallow object-oriented components - often comprised of shared parts - to separate concerns. This lets the code explain the details itself. We build it with Maven - the easiest system for the our operations team to support. SHRINE uses http4s for its web API, cats effects and fs2 for concurrency, CQRS via slick for storing and retrieving state, sends commands between nodes using MOM (AWS SQS, Kafka, or a home-grown REST API), circe for encoding json, i2b2 as a source of patient data, and Scala's xml library to create and read i2b2's xml. The Scala code is mostly functional. Further, SHRINE stores very little state outside of stack references.
```

That opening lists out the core technologies and the minimum skill set to bring. A developer familiar with http4s and cats effects would likely be able to contribute as soon as they understand the problem context. I would expect a generally capable Scala developer to "go read about" all of those technologies and get some level of how SHRINE uses them before attempting to make changes to SHRINE's code base. It's a punch-list.

In 2008 SHRINE began as a "Scala as a better Java" project that used Jakarta, Java servlets, and Scala's in-line XML capability to imitate and distribute a single-hospital query system's web API. We were able to evolve SHRINE from those initial decisions while keeping the whole works compatible release-to-release (mostly). SHRINE's transformation is a remarkable demonstration of the power of refactoring in Scala. https://www.lihaoyi.com/post/StrategicScalaStylePrincipleofLeastPower.html#dont-fear-refactoring


ev3dev-lang-scala  https://github.com/dwalend/ev3dev-lang-scala

ev3dev-lang-scala is a library and toolkit for programming Lego Ev3 robots using Scala. The programmers using the library are kids ages 9 to 13, mostly programming robots for FIRST Lego League. I've created a library that gives them a subset of what Lego provides in something that looks like Scratch (but is an overlay of their older LabView product). To keep things fair I don't give them anything more than Lego's base-level tool provides, but they do have access to all of Scala. I try to get them to use some object-oriented containment to keep it easy to explain. Individual kids do not value that in their own work but complain when another kid makes a mess of it, especially while making presentations just before the FLL competition. Most code the kids write is very procedural, like this method to drive the robot to a "museum" objective:

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
  
The kids surprised me with this recursive loop to use feedback from a gyroscope to make precise turns:

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
To trim back their cut-paste tendencies I want to show them higher-order functions this year. A general feedback loop might be the thing, but they are really against the concept of refactoring that Li Haoyi says is Scala's great strength. "It works fine. Why change it?" 

The other audience is library developers - just me so far. To make this thing work I had to learn the basics of interfacing with the ev3dev OS (a variant Debian Linux - OMG!) and how to use that interface efficiently from inside the JVM. To get the kids' control loops running at ~200 Hz after hot-spot warm-up the core uses Java NIO calls to read and write unix streams, very much "Scala as a better Java" in style:

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

I don't expect the kids to work at this level, but a beginner Scala developer with a unix backgrond and willingness to read through Java's NIO API should be able to contribute. On their best days the kids will use the IDE to follow calls down from their own code into the library calls to see what is going on.

You'll notice the kids' code refers to measured units like `.millimeters`, `seconds`, and `.degrees` - as value classes. I have figured out how to program the Scala3 type system to understand that some number of degrees divided by some number of seconds is degrees-per-second. I'm of two minds deciding if it is the right thing to do. It would save the kids having to dig out the values to do some arithmetic, then wrap up the result to have the correct type. However, it would add type-level arithmetic programming to the inner workings of the library code - a big jump from Scala-as-a-better-Java. I don't yet know what the right decision is. ... Scala lets me put that off.


Disentangle https://github.com/dwalend/Disentangle

Disentangle is a library of graph algorithms I use mostly for my own entertainment. (I did use them at ActivateNetworks for analyzing social networks.) I implemented graph minimization algorithms - like Dijkstra's shortest path algorithm - with general-purpose semirings - so the same algorithm code can find things like least-probable paths instead. Doing this project was what first drew me into Scala. To use the algorithm a developer needs to understand how to use Scala's tuple structures and collections library - entry-level skills:
   
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
I use Scala's generics to keep the types lined up right for different semirings, but otherwise the code is using shallow object-oriented ideas to keep different concerns separated. Here's a semiring for finding most-probable paths:

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

The core idea behind the library is to write algorithm code that looks identical to the pseudocode in fat algorithm books like https://www.amazon.com/Introduction-Algorithms-3rd-MIT-Press/dp/0262033844 . Here's the Floyd-Warshall algorithm ("Scala as a better Fortran"!):
   
```scala
  /**
   * O(n&#94;3)
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
Again, there's this split between how different audiences will interact with the code. Someone could just use this library in a project with a most-basic understanding of Scala. To add algorithms you don't need much more Scala to keep the code type-safe, but you would need to take care to keep the code efficient.

In Contrast: My Early Career

My first job out of school involved converting Matlab code into Fortran. (... and postscript). The third project was converting Matlab into Objective C . My fifth project was converting Matlab into Object C. The seventh project was an attempt to convert a system in C to Java (which failed). My eighth through twelfth projects were converting Matlab into Java. My second Scala project was translating R code into Scala.

I did take a job at Mathworks after all that Matlab translation. Jack Little, founder of Mathworks, pointed out that, "You can write a lot of really terrible matlab code really fast. That's one of its greatest strengths." I get it as a marketing plan for MathWorks, an action plan for a researcher, and a business plan for a start-up. All that recoding paid my student loans, rent, and kept me in food for my early career. I did observe that once a project chose a production language and framework then that choice was forever. If the language or ecosystem didn't provide something that the business needed then either we contorted our code to make it work or the venture failed. Big changes were too expensive.

Scala is Best as a Little Language

Scala libraries regularly evolve into domain-specific languages as the authors get more understanding about how to write concise, clear code. The Scala community takes a lot of pride in that. However, the line between what's "just a library" vs "what is a DSL" is pretty blurry. Here's some SHRINE code that uses http4s' end-point DSL:

```scala
    case request @ POST -> Root / "startQuery" as user => startQuery(request,user)

    case request @ POST -> Root / "changeQueryNameAndNotes" / LongVar(queryId) as user => changeQueryNameAndNotes(queryId, request, user)

    case _ @ GET -> Root / "query" / LongVar(queryId) as user => getQuery(queryId, user)
```
We bring these into code via `import org.http4s.dsl...` but pieces we're importing are masterfully-designed unapply methods to be used in match/case statements. There's no new parser, no changes to a compiler, and no new language definition. It just lets our team write concise, clear Scala code. In Scala we're always making choices about what to use and what to leave out. By choosing which parts of Scala to use and which to leave out we can define our own little languages for our projects. Changes to this decision have incremental cost; if we need to make a different choice in the future we can either let some new kind of complexity in, or refactor to simplify. That's a tremendous benefit, and seems to be a real thing.