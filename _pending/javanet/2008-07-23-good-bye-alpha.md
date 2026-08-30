---
layout: post
title: "Good-bye, Alpha"
date: 2008-07-23
permalink: /archive/2008/07/good-bye-alpha/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2008/07/goodbye_alpha.html
javanetTopics:
  - Open Source
---

I released [SomnifugiJMS v22](https://somnifugijms.dev.java.net/) a few weeks back. Not alpha-0-22. This subtlety is a big change in approach for a small change in code. I make fewer changes in each release, and the extremely stabile JMS specification is only so big. I've added most of the features I intend to implement. After eight years of work, six years in production systems, and 21 alpha releases it's starting to feel done. I'd like to claim that I came to this conclusion on my own, but others had a big influence.

I hadn't thought to do it at all until I read [Kirill Grouchnikov's series of articles on his approach to open source projects](http://www.pushing-pixels.org/?p=305). Kirill says point blank not to do alpha releases: "...in a virtual world this means stripping the alpha / beta / 0.* status from your project. You have very short time window to impress the potential users, and a solid release number with no greek letters is a must-have. This is the least you can do after six years of development." Kirill's approach is not like mine, but his words got me thinking.

Bruno Ghisi pointed out [a remarkable survey](http://weblogs.java.net/blog/brunogh/archive/2008/06/why_do_we_write.html) on why we do open source work. I suspect Kirill is much closer to the "professionals" and "believers" groupings than I am. I straddle the "skill enhancers" and "fun seekers" groupings. I write most of my code after hours, even if it is for work instead of hobby. I pick projects that teach me about new technologies and keep my skills sharp. Further, I enjoy the meditative nature of coding the way other people enjoy watching TV. It's something I do to relax, clear my head and settle down at the end of the day. My only nod to the "professionals" is that I wait to register new open source projects until I have a first release ready to go. However, for me to stay focused on a project without pay, that project has to entertain me or at least teach me something.

Alpha labels on my projects are a warning to everyone: This code isn't ready for prime time. I'll change the API if I need to, and I think I'll need to. And I won't apologize for it.

SomnifugiJMS is easy for me to recognize as mature. The JMS specification has been stabile for six years. SomnifugiJMS supports most of it. I have no plans to support the missing parts. SomnifugiJMS is done except for maintenance releases.

[JDigraph](https://jdigraph.dev.java.net/) is a very different story. The project is, among other things, an experiment on how to create [good, clear API](http://www.infoq.com/presentations/effective-api-design). Splitting mutators off from accessors worked amazingly well. Adding type specifiers for nodes and edges taught me how to use generics well. That part of the code is now very stabile. Building generic graph minimization algorithms exposed some big weaknesses of the Java language change that no one was talking about. I want to fix that, although it really needs operator overloading to do well. (I'll probably use that project to teach myself Scala.) Eventually I'll snap a line, cut out the failed experiments, and change over to maintenance releases. But not just yet.

[SalutafugiJMS](https://salutafugijms.dev.java.net/) is in between. I finished its second release a few weeks ago. I've covered about a quarter of the big challenges in JMS. It's JMS again, so others determined the API six or more years ago. However, I know I want to switch over to [an open, pure Java ZeroConfig](http://sourceforge.net/projects/jmdns/) library underneath -- a big code quake. I marked the second release as alpha. Maybe release four will have enough of the JMS specification to drop the alpha label.
