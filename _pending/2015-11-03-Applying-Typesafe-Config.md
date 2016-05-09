---
layout: post
title: def apply(config:Config) !
comments: True
---

TL/DR I started using apply methods that take a tyepesafe Config instance in companion objects 

    def apply(config:Config) 
    
to allow for easy configurations of standard parts. I took that a step further for singletons by letting them simply load their own Config. The resulting code is very clear and very flat. Competing options meant developing a new skill in that each option's discipline.

# SHRINE's use of TypeSafe Config

For my day-job I work on work on an open-source bioinformatics project called [SHRINE](TODO link). I'm fortunate to have inherited a project that is a business success built on well-tested, sound code. SHRINE started life as "Scala-as-a-better-Java," is cradled inside a Tomcat servlet behind Jersey, and needs some weeding. (I'm slowly refactoring it toward less baroque dependencies - a different rant.) It has a lot of config. We fix about a quarter of SHRINE troubles in the field by tweaking a node's shrine.config file. Our team needs to be able to quickly trace what a configuration value does in the code, hopefully to a nearby log message. I'm the first to use reference.conf files.

At the bottom of the stack is TypeSafe Config, which is really quite good. However, the optional config of optional parts with optional parts that a TODO-year project develops leave their mark, and SHRINE's config is warty. I spotted four themes written in the code: At least one of my predecessors really missed having Spring handle his configuration. He added MannualyWiredShrineBulder (TODO name) , two layers of empty case classes (and tests) as middle stages between Config and the actual places that use the config. At least one of other predecessor really didn't understand that earlier predecessor had built Spring Junior. A third predecessor added a layer of [higher-order functions](TODO link to Lee Haoyi article), but had stopped before using those functions more than once.

When our team tries to gain some quick understanding to help system admins in the field we flounder around tracing variables. We can't provide good support on the phone or in chat because tracing through the code takes too long. The whole thing should be simpler because, after all, it is just config.
 
# In the Beginning 
 
The history of config on the JVM is pretty embarrassing for everyone involved. Back in the Age of Plaid Flannel we started with java.lang.System.getProperty() , which was pretty good in hindsight. Everyone understood that it was a Map[String,String] just from the API. You could stuff values into it from the command line provided you didn't have too many characters for your command line. java.lang.System.setProperty() had obvious problems that were easy to avoid. The main work was figuring out what the property keys were. It was great for just getting a database name and password.

# DI, Cake, Spring, and JNDI - Oh My

Sun created a standard called [JNDI](TODO), declared that we should use it, and pinned it to their whole fleet of standards. JNDI had two big problems: First, the API is full of uninspiring boilerplate. Second, you had to supply something to be the back-end for it - almost always a big framework that you program in an XML schema that will not be like the next big framework's XML schema. [Spring](TODO) made it so that I could get my own Java object out the other end, and made the XML schema a bit better, but I was still programming in XML. The [Cake Pattern](TODO) finally let me program in XML, in exchange for lots of parameters in my constructors. Someone finally formalized what they meant by dependency injection. Understanding that helped me conclude that most of the time I didn't want it in my system. [TODO Haoyi Link]() .

# def apply(config:Config) is Enough (and sometimes more than enough)

I wound up happy with an apply(Config) method in a companion object for the client's case class.
 
TODO example
 
Sometimes there's really ever only going to be one thing, so I use an object.

TODO example

Sometimes I need some control over the configuration, usually to support testing, so I "inject" new config variables into a config source singleton

TODO example

And then inject the configuration I need for just that one test.

