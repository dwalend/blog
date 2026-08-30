---
layout: post
title: "Bad Things In adamTaglet"
date: 2006-11-14
permalink: /archive/2006/11/bad-things-in-adamtaglet/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2006/11/bad_things_in_a.html
javanetTopics:
  - Tools
---

[adamTaglet -- Architecture Driven Assisted Modeling Taglet --](https://adamtaglet.dev.java.net/) is a taglet that generates class diagrams from a custom JavaDoc tag. The tag holds a list of the leaf classes for the diagram and a list of forbidden classes. adamTaglet walks the class and interface inheritance structures from the leaves, building up a [directed graph](https://jdigraph.dev.java.net/nonav/alpha-0-14-0/api/net/walend/digraph/Digraph.html). The taglet stops walking the graph whenever it reaches an uninteresting forbidden class like Object or Serializable. The taglet then feeds the resulting directed graph to [GraphViz](http://graphviz.org/) to generate a picture of the class relationships and a client-side image map. Finally, adamTaglet replaces the custom tag with the [picture and image map](https://jdigraph.dev.java.net/nonav/alpha-0-14-0/api/net/walend/digraph/package-summary.html#classHierarchy). Click on a class or interface, and go to its JavaDoc.

I had to use the [verboten com.sun API](http://weblogs.java.net/blog/robogeek/archive/2006/01/the_nonpublic_c.html) to build up the URLs for the links in [ClassDiagramVisitor](https://adamtaglet.dev.java.net/source/browse/adamtaglet/v1/source/adamtaglet/net/walend/adamtaglet/ClassDiagramVisitor.java?rev=1.7&view=auto&content-type=text/vnd.viewcvs-markup). I found it in com.sun.tools.doclets.internal.toolkit.Configuration after digging through a lot of the javadoc source code.

```java
/**
    @return a URL String to link to node.
    */
    private String urlForNode(Class node)
    {
        //If the node is in the same package
        if(node.getPackage().equals(packag))
        {
            return shortNameOfClass(node) + ".html";
        }
        else
        {
            //If the node is from some other JavaDoc repository
            int nameSize = node.getPackage().getName().length();
            String shortClassName = node.getName().substring(nameSize+1);

            String result = configuration.extern.getExternalLink(node.getPackage().getName(),"relativePath",shortClassName);

            //If the node is from some other package in this repository
            if(result==null)
            {
                result = pathToClass(node);
            }
            return result+".html";
        }
    }
```

The API I'm calling is pretty rickety. That `"relativePath"` magic String worries me. Worse, I'm interpreting a null return value, which is always a little scary. If someone changes that `getExternalLink()` method to return `"No Link, Dude"` then adamTaglet will make broken links. Plus there's my lingering fear that some developer at Sun will need to change Configuration's API to at least not expose the extern member variable. That'd lead to different compiles for different JDKs

I don't mean to be too discouragingly critical of the javadoc tool's code base, but I do need to warn others about what they'll find diving in. The javadoc code has characteristics of code written by a series of developers over time -- new strata of API wrapped over old layers, naming and style limited to certain strata, and magic Strings to bind the layers together. I suspect these developers didn't know each other and were afraid of breaking existing code by making it simpler. The resulting code is pretty much opaque. I had to rely on an IDE (Netbeans this time) to stumble through it. (At some point I'll write a scathing blog about our dependence on IDEs, but I haven't the courage just now.)

Taglets were new in JDK 5, but don't seem to have found a lot of use. To me it looks like most people doing interesting extensions to JavaDoc are using custom Doclets. There aren't any big changes for JavaDoc in JDK 6. [JSR-260](http://jcp.org/en/jsr/detail?id=260) promised a revamp of the javadoc tool and tags in 2004, but missed the deadline for JDK6. I wonder if others are waiting to see what this JSR delivers before starting new large projects.

Javadoc itself comes from the dawn of Java in 1995. JavaDoc has been remarkably useful over the years, and remarkably unchanging. The existence of JSR-260 suggests that we as a community may be outgrowing the existing javadoc tool. JDK 6 does provide the new [compiler API](http://jcp.org/en/jsr/detail?id=199), which might make a good starting point for a new javadoc tool.

Now that Java is going open source the Java community might finally be ready for [cross-linked javadoc](http://today.java.net/pub/a/today/2004/08/26/ashkelon.html) more sophisticated than [`-link`](http://java.sun.com/j2se/1.5.0/docs/tooldocs/solaris/javadoc.html#link). (Accept that Sun's lawyers are part of our community even if they seem to [get underfoot more often than not](http://blogs.sun.com/jag/entry/contribution_agreements_considered_%22just_stupid%22).) The Java Tools community has talked about how to show which of our projects use each other's work. Hosting cross-linked javadoc would be a great pillar to add to java.net.

In my ears: Monteverdi Vespers of 1610
