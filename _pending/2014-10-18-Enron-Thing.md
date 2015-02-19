---
layout: post
title: Just Between People at Enron
comments: True
---

The testing in my [graph algorithm library](https://github.com/dwalend/ScalaGraphMinimizer) up to now has all been on randomly connected graphs -- graphs with some random edges connecting nodes. To test Brandes' betweenness algorithm and (soon) the Louvain method I wanted some graph from nature. The Louvain method would be particularly bad at random graphs. At ActivateNetworks we did a lot of work with social graphs; I implemented Brandes' algorithm while there but no longer have access to our customers' data. Social graphs are more sane because [people form communities of about 140 members, tightly linked](link to Luke's slide about brain volume and social group size). I pulled in part of the [Enron email corpus](http://en.wikipedia.org/wiki/Enron_Corpus) to use for tests, which I turned into a [still-very-hacky github project](https://github.com/dwalend/EnronMetaData).

## The Enron Email Corpus

The [Enron email corpus](http://en.wikipedia.org/wiki/Enron_Corpus) may be the largest clob of email available for research. The Justice Department seized the email logs from the company and went fishing for crooks. I'll let others report [the results](http://en.wikipedia.org/wiki/Enron_scandal); they found what they were looking for. [Andrew McCallum](http://en.wikipedia.org/wiki/Andrew_McCallum) purchased a copy of it and made it available to us all. You can download the whole works from a variety of sources, including the full text of the emails. Most of them are remarkably dull, but are great fodder for a talk on (total lack of) electronic privacy.

I downloaded them from [Forever Data](http://foreverdata.org/1009/). (I could not use that company name for a creepy short story.) I use the email metadata only, which, for each email sent, shows who was emailing who. It's much smaller, and in an easy-to-parse CSV format. I also only used the data for April 2000 for my tests. I don't need much more, and github gets cranky about [files bigger than 100 MB](https://help.github.com/articles/what-is-my-disk-quota/).


## Experience is What You Get When You Really Wanted Something Else

I'd thought parsing the CSVs would be a good way to get a little experience with [Parboiled](https://github.com/sirthias/parboiled2). It didn't go so well. The CSV example didn't work out of the box, but [Mathias](https://github.com/sirthias) fixed it when I asked. He then added it as an official example. I had a companion object for my Transmissions class, which [caused trouble](https://github.com/sirthias/parboiled2): "Note that there is one quirk: For some reason this notation stops working if you explicitly define a companion object for your case class. You'll have to write ~> (Person(_, _)) instead." Having the companion object extend the right Tuple13 fixed it (and possibly problems with Slick).

    import implicit.expletives

    object Transmission extends ((String,Int,Long,Email,Email,String,Boolean,Boolean,Boolean,String,String,String,String) => Transmission)

I can't recommend trying to maintain that inheritance in a project where someone gets to add or remove columns, but the compiler will complain if you don't cross your ts.

My parser ran out of memory. [Parboiled2 can't stream](https://groups.google.com/forum/#!topic/parboiled-user/b7PH49fiFco).

## Parsing Email Metadata

I gave up and wrote my own CSV parser. I was a bit [intimidated at first](http://tburette.github.io/blog/2014/05/25/so-you-want-to-write-your-own-CSV-code/), but Scala kept it down to about [25 lines of uninteresting imperative code](https://github.com/dwalend/EnronMetaData/blob/master/src/main/scala/net/walend/enron/CsvParser.scala).

The more interesting, more idiomatic feature of the code is that parsing any line produces either a record of someone sending an email or a description of what problem the parser encountered -- Either\[Problem,Transmision\] in Scala. The code has a lot of lines that dig out individual problems with the data.

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


This approach works amazingly well. At the end of one pass I have a first cut of good, clean data plus a list of problems to fix, caveat problems I've never thought about that bring down the whole works. (I really need Bill Venners' [Eastwood -- Good, Bad, or Ugly](https://thenewcircle.com/s/post/1704/comparing_functional_error_handling_in_scalaz_and_scalactic?utm_campaign=twitter_channel&utm_source=twitter&utm_medium=social&utm_content=%22Comparing%20Functional%20Error%20Handling%20in%20Scalaz%20and%20Scalactic%2C%22%20%40bvenners%27s%20talk%20from%20%40nescalas%20is%20now%20live!) , late in the talk and in an unrecorded session the next day. We couldn't figure out how to make Eastwood play nice with monadic stuff. However, Either will get us through the night.)

The only really aggravating problem I encountered while reading in the data was "java.nio.charset.MalformedInputException: Input length = 1" , which is pretty cryptic. Adding the iso-8859-1 encoding parameter to

    Source.fromFile(file,"iso-8859-1").getLines().toIterable.drop(1)

fixed that.

## Slick, Because I Really Just Want a SQL Database

After fiddling around a bit I decided that I liked fiddling around. The data was columnar, and not terribly interrelated. What I really wanted was a database.

I hacked in some [Slick]() code, which worked as advertised. I'd be highly critical of Slick if it had trouble with a schema of two unrelated tables. The remarkable thing about this Slick code is how unremarkable it is.

## Json, Because I Don't Want a DB in my Graph Algorithms (just yet)

I was fiddling around in the REPL anyway, so I made my data file for the tests there. [Scala pickling]() is the future of Json in Scala (but not quite the present yet -- [no spray.io support]() for example). It uses macros everywhere, so it is very efficient and doesn't need help in the parsing. I've got the usual concerns about changing data structures, but the compiler would have to know the history of the class being unpickled to make that easy for me. I don't think anyone has solved that puzzle yet.

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

The only explicitive was pickledEdges.toString vs .value

About Betweenness

And how weird betweenness is

Betweenness at Enron

Did Betweenness catch the crooks?

From https://github.com/sirthias/parboiled2 , "Note that there is one quirk: For some reason this notation stops working if you explicitly define a companion object for your case class. You'll have to write ~> (Person(_, _)) instead."  Tell him the companion object has to extend Tuple.

Asked Mathias to fix the CSV example. Thanks! But Parboiled2 can't stream . https://groups.google.com/forum/#!topic/parboiled-user/b7PH49fiFco and the thing is running out of memory on the first file.

Code was really straight-forward to load the data, loads a file in about 30 seconds. But ran out of memory when I tried to groupby (sender,receiver) all 30 files at once, after about 12 minutes.

Changed over to do my filtering early and all of my evaluation as late as possible.

java.nio.charset.MalformedInputException: Input length = 1

No data for metadata2000mar.csv , metadata2000sep.csv , metadata2001aug.csv . Deleted the files, but that wasn't the problem, so I restored them. Added "iso-8859-1" and fixed it.
