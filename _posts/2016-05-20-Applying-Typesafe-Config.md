---
layout: post
title: Just apply(Config)
comments: True
---

TL/DR - I started using apply methods in companion objects that take a TypeSafe Config instance parameter. Now I am much happier. 

    object UsefulConfigurableThing {
        def apply(config:Config):UsefulConfigurableThing = { ... }
    }
    
I use this method to make standard parts easy to configure. I let things be even simpler for singletons - a singleton just accesses the Config it needs. The resulting code is clear and very flat. Competing options meant filing my head with a new bag of API names and sometimes a new skill in an uninteresting discipline. This flat approach saves me from depending on a mountain of YANGTNI framework features.

# SHRINE's use of TypeSafe Config

For my day-job I work on work on an open-source bioinformatics project called [SHRINE](https://catalyst.harvard.edu/services/shrine/). I'm (mostly) fortunate to have inherited a project that is a business success built on well-tested code. SHRINE started life as "Scala-as-a-better-Java," first check-in I can find was in 2008. SHRINE is cradled inside a Tomcat servlet behind Jersey, and needs some weeding. (I'm slowly refactoring it toward less baroque dependencies - a different rant.) It has a lot of config. We fix about a third of SHRINE troubles in the field by tweaking a node's shrine.config file. Our team needs to be able to quickly trace what a configuration value does in the code. 

At the bottom of the stack is TypeSafe Config, which is really quite good. However, the optional config of optional parts with optional parts that a eight-year-old project develops leave their scars, and SHRINE's config is warty. One of the background whispers in the code is a fear of breaking things that work. I spotted four themes written in the code: "ManuallyWiredShrineJaxrsResources," plus two layers of empty case classes (and tests) as middle stages between Typesafe Config and the actual places that use the configured values hint that at least one of my predecessors really missed having Spring handle his configuration. He expected to use those extra layers for validation, but never did. At least one of other predecessor really didn't understand that this earlier predecessor had built mini-Spring. A third predecessor added a layer of higher-order functions for a different sort of [dependency injection](http://www.lihaoyi.com/post/StrategicScalaStylePrincipleofLeastPower.html#dependency-injection), but had stopped before using those functions more than once. I'm the first developer to use Config's reference.conf files. I might be the first to use a deep embrace of TypeSafe Config.

When our team tries to gain some quick understanding to help system admins in the field we flounder around tracing variables to configured values. We struggle to provide timely support on the phone or in chat because tracing through the code takes too long. It frustrates us. The whole thing should be simpler. After all, it is just config.
 
# System.getProperty() 
 
In Java we started with java.lang.System.getProperty() back in the Age of Plaid Flannel. System.getProperty() was pretty solid and is still in wide use. Everyone understood that Properties was a HashMap[String,String] just from the API. You could stuff values into it from the command line (provided you didn't have too many characters for DOS). java.lang.System.setProperty() had problems that predicted the general goodness of immutability and were easy to avoid. The main work was figuring out what the property keys were. It was great for just getting a database name, password, and url.

# Cake, Spring, DI, and JNDI 

Sun created a standard called [JNDI](http://www.oracle.com/technetwork/java/jndi/), declared that we should use it, and used it as underpinning for whole fleet of standards. JNDI had two big problems: First, the API is full of uninspiring boilerplate like InitialContext and catching NamingExceptions. Second, you had to supply something to be the back-end for it - almost always a big framework that you program in an XML schema that will be different from the next big framework's XML schema. [Spring](https://projects.spring.io/spring-framework/) made it so that I could get my own Java POJ object out the other end, and made the XML schema a bit better, but I was still programming in XML. The [Cake Pattern](http://www.cakesolutions.net/teamblogs/2011/12/19/cake-pattern-in-depth) finally let me program in something not XML, in exchange for lots of traits. Someone finally [formalized what they meant by dependency injection](http://www.cakesolutions.net/teamblogs/2011/12/15/dependency-injection-vs-cake-pattern) while declaring its alternatives "dinosaurs." Understanding that helped me conclude that [most of the time I didn't want it in my system](http://www.lihaoyi.com/post/StrategicScalaStylePrincipleofLeastPower.html#hardcode-it). 

(Is anyone else bothered that the "DI" in JNDI means something completely different and predates "DI" by five years or more? Maybe Oracle should make it a backronym.)

# Finally TypeSafe Config

The Akka project spun out [TypeSafe Config](https://github.com/typesafehub/config) as a separate project. The gritty details fit on a single, short readme.md page in github, and [the API example fits on a screen](https://github.com/typesafehub/config#api-example). Most of the page is about corner-case features that I don't use frequently. You program TypeSafe Config in a superset of JSON that basically lets you leave out quotes. A Config is a container of key -> object pairs. All of the objects are built from JSON strings. Many of the objects built are Configs. Most of the breadth of the API is about getting the right type into Java.

# def apply(config:Config) is Enough

I settled on using an apply(Config) method in a case class' companion object as my standard approach. 
 
    case class StewardQueryAuthorizationService(qepUserName:String,
                                                qepPassword:String,
                                                stewardBaseUrl:URL,
                                                defaultTimeout:FiniteDuration = 10 seconds) extends 
                 QueryAuthorizationService with 
                 Loggable with 
                 Json4sSupport {...} 
 
    object StewardQueryAuthorizationService {

      def apply(config:Config):StewardQueryAuthorizationService = StewardQueryAuthorizationService (
        qepUserName = config.getString("qepUserName"),
        qepPassword = config.getString("qepPassword"),
        stewardBaseUrl = config.get("stewardBaseUrl", new URL(_))
      )
    }

The apply() method pulls arguments from the Config for the case class' constructor, then calls the case class. JSON to case class. Standard, general tools. No special skills or big patterns to explain. No mystery. 

# Sometimes apply(Config) is More Than Enough
 
That technique works great in general, but sometimes there'd only be one instance of the class. A Scala object is a better choice. For that, I apply Li Haoyi's principle of least power. I go one step further than hard-coding, and pull the value out of the Config exactly where I need it. 
 
    object StewardSchema {

      val allConfig:Config = StewardConfigSource.config
      val config:Config = allConfig.getConfig("shrine.steward.database")
    
      val slickProfileClassName = config.getString("slickProfileClassName")
      val slickProfile:JdbcProfile = StewardConfigSource.objectForName(slickProfileClassName)
    
      val schema = StewardSchema(slickProfile)
    }

Did you notice that StewardConfigSource.config? Sometimes I need some control over the configuration for testing. I've already [blogged about how I inject new config variables for testing](http://dwalend.github.io/blog/2015/06/21/Test-With-TypeSafeConfig.html). That does put in one extra hop to answer "Where does this Config come from?" However, outside of testing anyone's first guess will be right. I've preserved the most important easy answer for "How do I control this value?"

