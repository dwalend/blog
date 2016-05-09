---
layout: post
title: def apply(config:Config) !
comments: True
---

TL/DR I started using apply methods in companion objects that take a TypeSafe Config instance parameter and am much happier. 

    def apply(config:Config) 
    
I use to allow for easy configurations of standard parts. I took that a step further for singletons by letting them simply load their own Config. The resulting code is very clear and very flat. Competing options meant developing a new skill in that each option's discipline and avoiding the regret of YANGTNI.

# SHRINE's use of TypeSafe Config

For my day-job I work on work on an open-source bioinformatics project called [SHRINE](https://catalyst.harvard.edu/services/shrine/). I'm (mostly) fortunate to have inherited a project that is a business success built on well-tested code. SHRINE started life as "Scala-as-a-better-Java," is cradled inside a Tomcat servlet behind Jersey, and needs some weeding. (I'm slowly refactoring it toward less baroque dependencies - a different rant.) It has a lot of config. We fix about a third of SHRINE troubles in the field by tweaking a node's shrine.config file. Our team needs to be able to quickly trace what a configuration value does in the code, hopefully to a nearby log message. I'm the first to use reference.conf files.

At the bottom of the stack is TypeSafe Config, which is really quite good. However, the optional config of optional parts with optional parts that a eight-year-old project develops leave their scars, and SHRINE's config is warty. I spotted four themes written in the code: At least one of my predecessors really missed having Spring handle his configuration: "ManuallyWiredShrineJaxrsResources," plus two layers of empty case classes (and tests) as middle stages between Config and the actual places that use the configured values. At least one of other predecessor really didn't understand that earlier predecessor had built Spring Junior. A third predecessor added a layer of higher-order functions for a different sort of [dependency injection](http://www.lihaoyi.com/post/StrategicScalaStylePrincipleofLeastPower.html#dependency-injection), but had stopped before using those functions more than once.

When our team tries to gain some quick understanding to help system admins in the field we flounder around tracing variables. We can't provide good support on the phone or in chat because tracing through the code takes too long. The whole thing should be simpler. After all, it is just config.
 
# In the Beginning 
 
The history of config on the JVM is pretty embarrassing for everyone involved. Back in the Age of Plaid Flannel we started with java.lang.System.getProperty() , which was pretty good in hindsight. Everyone understood that it was a Map[String,String] just from the API. You could stuff values into it from the command line (provided you didn't have too many characters for your command line). java.lang.System.setProperty() had problems that predicted the general goodness of immutability and were easy to avoid. The main work was figuring out what the property keys were. It was great for just getting a database name, password, and url.

# DI, Cake, Spring, and JNDI - Oh My

Sun created a standard called [JNDI](http://www.oracle.com/technetwork/java/jndi/), declared that we should use it, and used it as underpinning for whole fleet of standards. JNDI had two big problems: First, the API is full of uninspiring boilerplate like TODO. Second, you had to supply something to be the back-end for it - almost always a big framework that you program in an XML schema that will not be different from the next big framework's XML schema. [Spring](https://projects.spring.io/spring-framework/) made it so that I could get my own Java POJ object out the other end, and made the XML schema a bit better, but I was still programming in XML. The [Cake Pattern](http://www.cakesolutions.net/teamblogs/2011/12/19/cake-pattern-in-depth) finally let me program in something not XML, in exchange for lots of traits. Someone finally [formalized what they meant by dependency injection](http://www.cakesolutions.net/teamblogs/2011/12/15/dependency-injection-vs-cake-pattern) while declaring its associates dinosaurs. Understanding that helped me conclude that [most of the time I didn't want it in my system](http://www.lihaoyi.com/post/StrategicScalaStylePrincipleofLeastPower.html#hardcode-it). 

# Finally TypeSafe Config

The Akka project spun out [TypeSafe Config](https://github.com/typesafehub/config) as a separate project. The gritty details fit on a single, short readme.md page in github, and [the API example fits on a screen](https://github.com/typesafehub/config#api-example). Most of the page is about corner-case features that I don't use frequently. You TypeSafe Config in a superset of JSON. 

# def apply(config:Config) is Enough (and sometimes more than enough)

I wound up happy with an apply(Config) method in a companion object for the client's case class.
 
TODO example
 
Sometimes there's really ever only going to be one thing, so I use an object.

TODO example

Sometimes I need some control over the configuration, usually to support testing, so I "inject" new config variables into a config source singleton

TODO example

And then inject the configuration I need for just that one test.

