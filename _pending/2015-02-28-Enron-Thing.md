---
layout: post
title: Between People at Enron
comments: True
---

The tests in my [graph algorithm library](https://github.com/dwalend/ScalaGraphMinimizer) up to now have all used randomly connected graphs -- graphs with some random edges connecting nodes. To test Brandes' betweenness algorithm and (soon) the Louvain method I wanted some graph from nature. The Louvain method would be particularly bad at random graphs, and betweenness doesn't make a lot of sense.

At ActivateNetworks we did a lot of work with social graphs; I implemented Brandes' algorithm while there. Social graphs are more sane because [people form communities of about 150 members, Dunbar's number](http://en.wikipedia.org/wiki/Dunbar%27s_number). I couldn't share our customers' data, so I pulled in part of the [Enron email corpus](http://en.wikipedia.org/wiki/Enron_Corpus) to use for tests, which I turned into a [still-very-hacky github project](https://github.com/dwalend/EnronMetaData).

One thing that always bothered me at ActivateNetworks was our base-level assumption that any email meant a relationship existed. I can swap the FewestNodes semiring in Brandes algorithm for something else, like the MostProbable semiring (with cheezy normalized probability weights from dividing the number of emails between two people by the maximum number in the month). If that's radically different then I've discovered something worth bugging my old comrades about.

## The Enron Email Corpus

The Justice Department seized Enron's email logs from the company and went fishing for crooks. The [Enron email corpus](http://en.wikipedia.org/wiki/Enron_Corpus) may be the largest clob of email available for research. I'll let others report [the results](http://en.wikipedia.org/wiki/Enron_scandal); they found what they were looking for. [Andrew McCallum](http://en.wikipedia.org/wiki/Andrew_McCallum) purchased a copy of it and made it available to us all. You can download the whole works from a variety of sources, including the full text of the emails. Most of them are remarkably dull, but are great fodder for a talk on (the total lack of) electronic privacy.

I downloaded them from [Forever Data](http://foreverdata.org/1009/). (I could not make up that company's name for a sophomore short story class.) I use the email metadata only, which, for each email sent, shows who was emailing who. It's much smaller, and in an easy-to-parse CSV format. I also only used the data for April 2000 for my tests. I don't need more, and github gets cranky about [files bigger than 100 MB](https://help.github.com/articles/what-is-my-disk-quota/).


## Experience is What You Get When You Really Wanted Something Else

I'd thought parsing the CSVs would be a good way to get a little experience with [Parboiled](https://github.com/sirthias/parboiled2). It didn't go so well. The CSV example didn't work out of the box, but [Mathias](https://github.com/sirthias) fixed it when I asked. He then added it as an official example. I had a companion object for my Transmissions class, which [caused trouble](https://github.com/sirthias/parboiled2); "Note that there is one quirk: For some reason this notation stops working if you explicitly define a companion object for your case class. You'll have to write ~> (Person(_, _)) instead." Having the companion object extend the right Tuple13 fixed it (and possibly problems with Slick).

    import implicit.expletives

    object Transmission extends ((String,Int,Long,Email,Email,String,Boolean,Boolean,Boolean,String,String,String,String) => Transmission)

I can't recommend trying to maintain that extends clause in a project where anyone gets to add or remove columns, but at least the compiler will complain if you break it.

My parser ran out of memory. [Parboiled2 can't stream](https://groups.google.com/forum/#!topic/parboiled-user/b7PH49fiFco).

## Parsing Email Metadata

I gave up and wrote my own CSV parser. I was a bit [intimidated at first](http://tburette.github.io/blog/2014/05/25/so-you-want-to-write-your-own-CSV-code/), but Scala kept it down to about [25 lines of uninteresting imperative code](https://github.com/dwalend/EnronMetaData/blob/master/src/main/scala/net/walend/enron/CsvParser.scala).

The more interesting, more idiomatic feature of the code is that parsing any line produces either a record of someone sending an email or a description of what problem the parser encountered -- Either\[Problem,Transmission\] in Scala. The bulk of the code is lines that dig out problems with the data.

      def create(fileName:String,lineNumber:Int,lineContents:Seq[String]):Either[Problem,Transmission] = {
        if (lineContents.size != 11) {
          if (lineContents.size < 11) Left(Problem(fileName, lineNumber,Category.tooFewColumns.name, s"(${lineContents.size}) in $lineContents"))
          else Left(Problem(fileName, lineNumber,Category.tooManyColumns.name, s"(${lineContents.size}) in $lineContents"))
        }
        else {
          val sender = Email(lineContents(1))
          val recipient = Email(lineContents(2))
          if(!sender.address.contains('@')) Left(Problem(fileName,lineNumber,Category.missingAt.name,s"sender $sender"))
          else if (!recipient.address.contains('@')) Left(Problem(fileName,lineNumber,Category.missingAt.name,s"recipient $recipient"))

          //Finally it's OK to make a Transmission
          else  Right(Transmission(fileName = fileName,


This approach works amazingly well. At the end of one pass it gives me a large sample of clean data plus a list of problems to fix, caveat problems I've never thought about that bring down the whole works. (I really need Bill Venners' [Eastwood -- Good, Bad, or Ugly](https://thenewcircle.com/s/post/1704/comparing_functional_error_handling_in_scalaz_and_scalactic?utm_campaign=twitter_channel&utm_source=twitter&utm_medium=social&utm_content=%22Comparing%20Functional%20Error%20Handling%20in%20Scalaz%20and%20Scalactic%2C%22%20%40bvenners%27s%20talk%20from%20%40nescalas%20is%20now%20live!) , late in the talk and in an unrecorded session the next day. We couldn't figure out how to make Eastwood play nice with monadic idioms. However, Either will get us through the night.)

The only really aggravating problem I encountered while reading in the data was "java.nio.charset.MalformedInputException: Input length = 1" , which is pretty unhelpful. Adding the iso-8859-1 encoding parameter to

    Source.fromFile(file,"iso-8859-1").getLines().toIterable.drop(1)

fixed that. Thank you, Google.

## Slick, Because I Really Just Want a SQL Database

After fiddling around a bit in the REPL I decided that I liked fiddling around with the data. The data was columnar, and not terribly interrelated. What I really wanted was a database.

I hacked in some [Slick](http://slick.typesafe.com/) code, which worked exactly as advertised. I'd be highly critical of Slick if it had trouble with a schema of two tables. The remarkable thing about this Slick code is how unremarkably simple it is.

## Json, Because I Don't Want a DB in my Graph Algorithms Test Code

Github is good at flat files. It's not that hard to pull a database out of an archive, but I didn't want to put that flavor of complexity into the graph algorithms project. I am willing to do something uninvasive and standard if it saves some weight of code. [Scala pickling](https://github.com/scala/pickling) is the future of Json in Scala (but not quite the present yet -- [no spray.io support](https://github.com/spray/spray/issues/1002) for example). It uses macros everywhere, so it is very efficient and doesn't need help in the parsing. That's the sort of hammer I want to swing.

I was fiddling around in the REPL anyway, so I made my data file for the graph algorithm tests there.

    import scala.pickling._
    import scala.pickling.json._
    import net.walend.enron.EnronDatabase
    import java.nio.file.{Paths, Files}
    import java.nio.charset.StandardCharsets

    val edges = EnronDatabase.extractTransmissionCounts
    val edgeString:String = pickledEdges.value
    JSONPickle(edgeString).unpickle[Seq[(String,String,Int)]]
    Files.write(Paths.get("results/LessEnron2000Apr.txt"), pickledEdges.toString.getBytes(StandardCharsets.UTF_8))
    val fileString = scala.io.Source.fromFile("results/LessEnron2000Apr.txt").mkString
    Files.write(Paths.get("results/LessEnron2000Apr.txt"), pickledEdges.value.getBytes(StandardCharsets.UTF_8))

The only explicative was figuring out to use pickledEdges.value instead of pickledEdges.toString .

## A Test of Betweenness on the Enron Data

Pulling the graph back out and running Brandes' betweenness was very tidy:

    "Betweenness for Enron data" should "be calculated" in {

      import scala.io.Source
      import scala.pickling._
      import scala.pickling.json._

      val fileContents = Source.fromURL(getClass.getResource("/Enron2000Apr.json")).mkString
      val edges = JSONPickle(fileContents).unpickle[Seq[(String,String,Int)]]

      val labelGraphAndBetweenness = Brandes.allLeastPathsAndBetweenness(edges,Seq.empty,FewestNodes,FewestNodes.convertEdgeToLabel)
    }

## Results

In the REPL via sbt test:console, I ran

    scala> import scala.io.Source
    scala> import scala.pickling._
    scala> import scala.pickling.json._
    scala> import net.walend.graph.SomeGraph._
    scala> import net.walend.graph.semiring.Brandes.BrandesSteps
    scala> import net.walend.graph.semiring
    scala> import net.walend.graph.semiring._
    scala> val fileContents = Source.fromURL(getClass.getResource("/Enron2000Apr.json")).mkString
    scala> val edges = JSONPickle(fileContents).unpickle[Seq[(String,String,Int)]]
    scala> val labelGraphAndBetweenness = Brandes.allLeastPathsAndBetweenness(edges,Seq.empty,FewestNodes,FewestNodes.convertEdgeToLabel)
    scala> val betweenness = labelGraphAndBetweenness._2

And finally

    scala> betweenness.to[Seq].sortBy(x => x._2)
    java.lang.AssertionError: assertion failed: List(value _2$mcD$sp, value _2$mcD$sp, value _2$mcD$sp, value _2$mcD$sp, value _2$mcD$sp, value _2$mcD$sp, value _2$mcD$sp, value _2$mcD$sp, value _2$mcD$sp, value _2$mcD$sp)
    	at scala.reflect.internal.Symbols$Symbol.suchThat(Symbols.scala:1916)
    	at scala.tools.nsc.transform.SpecializeTypes$$anon$2.matchingSymbolInPrefix$1(SpecializeTypes.scala:1460)
    	at scala.tools.nsc.transform.SpecializeTypes$$anon$2.transformSelect$1(SpecializeTypes.scala:1483)
     ...
     	at sbt.TrapExit$App.run(TrapExit.scala:248)
     	at java.lang.Thread.run(Thread.java:745)

     That entry seems to have slain the compiler.  Shall I replay
     your session? I can re-run each line except the last one.
     [y/n]

How civilized, but not quite what I wanted for a finale. It's only 1700 email addresses, so sortBy should be fine. A quick search lead to [a bug report vs Scala 2.11.5](https://issues.scala-lang.org/browse/SI-9099), already fixed in 2.11.6. Switching to 2.11.4 got through the trouble.

Here's a list of the people with the 10 highest betweenness values in April 2000 at Enron:

    (steven.kean@enron.com,53260.58012691413)
    (jeff.dasovich@enron.com,59156.98903661527)
    (chris.germany@enron.com,61701.19086004503)
    (carol.clair@enron.com,67655.27390774187)
    (susan.scott@enron.com,76157.68561454736)
    (sally.beck@enron.com,82040.94643046238)
    (sara.shackleton@enron.com,89571.2341102196)
    (vince.kaminski@enron.com,96123.70935699047)
    (tana.jones@enron.com,110579.53312945696)
    (mark.taylor@enron.com,111545.81230355639)

Switching to the MostProbable semiring was just a matter of mapping the edges to normalized edges and rerunning Brandes'. (The most frequented sender and recipient pair in the sample is vince.kaminski@enron.com writing to vince.kaminski@aol.com 274 times. I'm sure there's an anecdote behind that.)

    val weightedEdges = edges.map(x => (x._1,x._2,x._3.toDouble/274))
    val normalizedGraphAndBetweenness = Brandes.allLeastPathsAndBetweenness(edges,Seq.empty,MostProbable,MostProbable.convertEdgeToLabel)
    val normalizedBetweenness = normalizedGraphAndBetweenness._2

The nodes with the 10 highest betweenness using this probability model are not that different; debra.perlingiere@enron.com replaced jeff.dasovich@enron.com, and the other rankings moved around a bit. The ActivateNetworks assumption was fine.

    (chris.germany@enron.com,72725.80682360567)
    (steven.kean@enron.com,81287.60122108378)
    (debra.perlingiere@enron.com,89005.54636283437)
    (susan.scott@enron.com,90021.18526949426)
    (sally.beck@enron.com,115103.96001437954)
    (vince.kaminski@enron.com,119572.49086838862)
    (tana.jones@enron.com,159331.96521970455)
    (mark.taylor@enron.com,179964.3443774904)
    (carol.clair@enron.com,186060.8626406191)
    (sara.shackleton@enron.com,206970.0875042239)

Betweenness did not do that good a job finding [the executives accused in the scandal](http://en.wikipedia.org/wiki/Enron_scandal#Trials). Hopefully the Louvain method will do better.

Probably the most interesting of these is Vincent Kaminski, Enron's managing director for research. [An NY Times article](http://www.nytimes.com/2006/01/29/business/businessspecial3/29profiles.html?pagewanted=all) describes him as ethical, professional, and heroic, in contrast to the other power brokers around him. "As Enron was collapsing, Mr. Kaminski helped all 50 of his former research staff members find jobs elsewhere."




