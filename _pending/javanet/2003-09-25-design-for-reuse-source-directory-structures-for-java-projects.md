---
layout: post
title: "Design for Reuse: Source Directory Structures for Java Projects"
date: 2003-09-25
permalink: /archive/2003/09/design-for-reuse-source-directory-structures-for-java-projects/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2003/09/design_for_reus.html
javanetTopics:
  - Open Source
---

I've found I want to reuse code from almost every project I've ever worked on. Plus other people treat my code as library code years longer than I thought possible. So when I create Java code, I produce reusable .jars of code. Structuring the project correctly at the beginning to help reuse seems to be important, but isn't without cost. I have settled on one way, but am not convinced it's the best. (The examples are from [JDigraph](http://jdigraph.sourceforge.net), a library for representing and working with directed graphs.)

I pack a few complete packages into each .jar I produce. Although it's possible to split a package between multiple .jar files, .jar files work best when one .jar file holds all the .class files from specific packages. The manifest file contains version and security information based on specific packages. Signing a package in a .jar file prevents others from adding code to that package, so splitting a package between .jar files can result in security exceptions. More importantly, if someone asks me about a ClassNotFoundException, I can quickly figure out which .jar file is missing from their classpath.

I have a simple rule for figuring out which packages go in which .jar files: If two packages depend on each other -- java.lang and java.io, for example -- then they should go in the same .jar file. If not, they should be in different ones. Making this decision early seems to be important for making smaller pieces reusable.

I know two ways to structure source code in Java projects: All-In-One and Many-Subprojects. Both allow me to build the .jars I want to. Neither is perfect. I think Many-Subprojects is best in most cases, but if there's a third, I'd love to hear about it.

**All-In-One:** The most common way I've seen Java projects set up is with all the source code under a common source root:

![](https://bloggers.dev.java.net/files/documents/84/1073/projects-first-way.jpg)

The great feature of All-In-One is that everyone can find things in the source code. The approach grows organically as the project grows; there aren't any choices beyond deciding when and where to create a new package. People expect to find this sort of structure. It's a simple structure that works well for small projects with few people working on them.

The All-In-One approach makes it hard to safely break the kit into smaller reusable .jars. Because the project grows organically, nothing enforces dependency directions between packages. If a developer adds a dependency in the wrong direction, the packages have to be in the same .jar file to safely use either package. If someone adds a dependency, javac will ignore the rules I lay down in your build.xml and reach across the directory structure to compile source code that is supposed to be independent; the build.xml looses control of the source path.

The All-In-One approach doesn't scale well. It's fine for three good programmers for about six months, but for twenty developers or for three good developers for two years, it becomes brittle. The build file has to hold the complexity of creating the two separate .jar files. I use ant build.xmls for builds. Ant build.xml files are easy to hack under the pressure of the moment, which makes them brittle over time. Most projects that I've worked on have had increasingly complex build.xml files that get very difficult to maintain and follow. Further, as the project grows larger, it gets harder to use a test-first style and harder to refactor. If I want to try out a change in API, I have to wag all my code to match the new API before I can run my tests.

**Many-Subprojects:** An alternative is Many-Subprojects. A project is made of several subprojects, each with its own build file that builds a single .jar file of library code. Each subproject contains only the source code needed for its root. The uber subproject orchestrates the other build files and creates the final product. It looks like this:

![](https://bloggers.dev.java.net/files/documents/84/1074/projects-second-way.jpg)

The best thing about the Many-Subprojects approach is that it organizes things into smaller reusable pieces from the start. I can even snap off a subproject and convert it to a new project. There's no shared common source root, so javac can enforce the dependency rules I've laid down. And the build.xml keeps tyrannical control of the classpath.

This approach scales well; as I start new packages, I add new subprojects. The build.xml files for the subprojects are generally identical. Some subprojects will need an odd target or two, but the changes stay isolated. The approach encourages refactoring and a test-first approach; I can try out a change in one subproject's test code before propagating the change beyond that subproject.

The worst thing about Many-Subprojects is that the directory structure is less intuitive. Few developers have seen the style before. When I start a new package, I have to decide if the new package is independent enough to rate its own .jar file and subproject immediately. Some people find that task difficult. Setting up the structure initially takes more work.

All-In-One seems fine for projects with few people and a short life time. Although I usually only work with a few developers, my projects tend to last for years, grow, and create new projects. Converting an All-In-One project to Many-Subprojects is a thankless task that uncovers ugly cross-dependencies, but converting Many-Subprojects to All-In-One is trivial. I use the Many-Subprojects approach from the start.

Does anyone have a third structure that will give me the best of both worlds?
