---
layout: post
title: "Our Grass is Greenest: OGNL and LINQ"
date: 2006-06-19
permalink: /archive/2006/06/our-grass-is-greenest-ognl-and-linq/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2006/06/our_grass_is_gr.html
---

About a month ago there was a [flurry](http://weblogs.java.net/blog/jonbruce/archive/2006/05/a_java_perspect.html) [of](http://weblogs.java.net/blog/robogeek/archive/2006/05/syntactic_sugar.html) [blogs](http://humbleblogger.blogspot.com/2006/05/language-wars-redux-imminent-approach.html) about [LINQ](http://msdn.microsoft.com/data/ref/linq/) (Language Integrated Query. I'm not sure what the N stands for.) These articles are a very good description of LINQ, which looks like a useful add-on to the Microsoft CLR family of languages. LINQ would let me wind through layers of getters from the top level, to pluck out just the objects I care about. That's a nice way of saying I feel our usual C#-induced draw of language feature envy.

Deja vu followed that feeling of envy. Two years ago I was checking on what some old coworkers from VNP were doing. Drew Davidson and Luke Blanshard had created [OGNL](http://www.ognl.org/), the Object-Graph Navigation Language. OGNL is "an expression language for getting and setting properties of Java objects. You use the same expression for both getting and setting the value of a property." I've been looking for a nail for the OGNL hammer since I saw it. I think the main reason I haven't used OGNL is that writing a big chain of accessors is straightforward (for simple queries), and custom methods to select and build up collections of things inside of classes I control is not hard (for more interesting queries). So unless I force myself to do the (easy) overhead work of adding OGNL to a project, I'll continue to add the (not hard to write) one-off code to get the feature.

OGNL was inspired by frustration with [commons beanutils' PropertyUtils](http://jakarta.apache.org/commons/beanutils/commons-beanutils-1.7.0/docs/api/org/apache/commons/beanutils/package-summary.html#standard.nested); Java developers have been sharing this sort of thing for at least five years. We've no reason to feel envy. We just need to get some clue of what we already have, filter out the better ideas, share them and eventually convince the JCP to codify them.

I'll also have to regain my waning faith in Sun's process to evolve Java. We've still no bug parade number for my generics RFE.
