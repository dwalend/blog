---
layout: post
title: "Sharpening the Axe or Shaving the Yaks?"
date: 2005-01-22
permalink: /archive/2005/01/sharpening-the-axe-or-shaving-the-yaks/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2005/01/sharpening_the.html
---

I've got this great new project at work right now. The deadlines are very gentle and the boundaries are very vague. I am to "make the department's job [experimental planning systems research] easier" and I need to be done by September. I've started puzzling through what people in our group need by asking them questions and filling in a spreadsheet (more a letter to Santa), adding columns for my own thoughts, and sieving for things that look like real goals.

And I started thinking through what sorts of tools might fit the problem well. Since we don't know what sorts of data structures we'll need, but do need to manage a lot of data early, XML:DB and xml binding technology looks like a good fit. JaxB 2.0 isn't ready, XStream comes close to doing what I want, XPath 2.0 isn't available yet, etc. I'm considering asking for time at work to pour into open source efforts. And I can switch the project to JDK 5, and swap out the source code control system to Subversion, and pretty print the whole works while I'm moving things around.

I took a break to discuss these ideas with a respected colleague. He said, "Be careful. You're talking about shaving a lot of yaks."

Yak shaving is what James Gosling is worried about in this [blog](http://weblogs.java.net/jag/page13.html#106):

"But for me, the big problem with "axe sharpening" is that it's recursive, in a Xeno's paradox kinda way ... to sharpen the axe, you need a sharpening stone. ... But to get there, you need to build a dog sled...."

But to use a dog sled I need snow, so I need to go to town to get a snow cone machine. I grab my trusty yak to help you haul the machine from town. But it'll be summer before I get to town, and I don't want the yak to get to hot, so I shave the yak. In mid February, I proudly lead my shining, bald, shivering yak into my quarterly progress review...

Yak shaving is downloading an old JDK and rearranging an open source project's code to run inside of Eclipse's debugger to fix a problem of automatically generating ant build.xml files to build a searchable version of your source code to help find cut-and-paste sections of code with a thready bug. When you need to upgrade your linux to get a new glibc, you should smell fresh Essence du Yurt aftershave.

It's yak shaving when the people you work for have no hope of fathoming what you're doing. Sharpening an axe is fine; someone asked you to chop down trees, so explaining that you need a good sharp axe is easy. When they catch you shaving the yak, they get mad and you get embarrassed. Yak shaving is something to avoid, and something I think I'm wandering towards.

Now for some technical content: Has anyone out there used a nice, well-heeled XML-database subsystem? How do things like Xindice and Xstream play with each other? Any way to make an XML database aware of java inheritance without waiting for XPath 2.0? Or is there a better general way to take on this sort of problem without "X" anywhere?

Meanwhile, my yak is looking a little stubbly. I better lather him up.
