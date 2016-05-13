---
layout: post
title: Overcoming My Implicit Suspicions
comments: True
---

TL/DR - I'm very suspicious of Scala's use of implicit values. I got over it and I pimped Typesafe Config's Config class to handle Options.

# Typesafe Config
 
I like [Typesafe Config](https://github.com/typesafehub/config), a configuration library spun out of Akka. I like using it as the argument for apply methods in companion objects in case classes. 

TODO example

And I wish it were written in Scala instead of Java. In particular I want to be able to get Option results when I know a key might not be there, and I want to pass in my apply(Config) methods and get instances of case classes back out.

TODO like this

But Config is not Scala, so those ideas are pretty alien. I wish I could add the methods that I want to use.

# Explicit vs Implicit

I'm very much a proponent of explicit, clear, and sometimes long-winded programming. I like self-documenting code, with long argument lists and sometimes long method names.

TODO example

Implicits scare me. They seem too magical. I worry about having to decipher which implicits are flowing into code from where. I dread having to solve that kind of puzzle late at night when I'm trying to solve some other problem I care about and I'd rather be sleeping. I've tried to stay away from them in my Scala code, and succeeded for the most part. I was really hesitant to let them in.

# Pimp Pattern




# What I needed

Working with some older code at work I became really frustrated with the obfuscation and distant separation between where config keys were declared, values were loaded, and where the values were finally used. I started on a path to give case classes that were configured via Typesafe Config apply() methods that simply took configs.

# What I wanted
# Suspicious of implicit
# But this seemed OK
