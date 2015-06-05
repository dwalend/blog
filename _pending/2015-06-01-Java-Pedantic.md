Posted to Quora June 1st.

TL/DR - I think Java requires a lot of work to get things done because of how Java's cultural roots interacted with its language structure, not Java's syntax.
 
First an example that looks as irrelevant as "Hello, World!" but illuminates both structural and cultural problems.
  
In Java, to create a String of repeated '-'s I found this piece of code on Stack Overflow:
  
[code Java]  
    private String dashes(String censoredWord) {
        // Thanks to StackOverflow for this hack. http://stackoverflow.com/questions/2804827/create-a-string-with-n-characters
        return CharBuffer.allocate(censoredWord.length).toString().replace('\0','-');
    }
[/code]
  
What's a CharBuffer? How alien is allocate() in Java? I felt compelled to wrap it in a special method to keep it from polluting the rest of my code. It's not comfortable. 

One of Java's great strengths is that (almost) everything is an Object - an instance of some Class. To figure something out, a developer needs only to find the right import, then walk up a (hopefully shallow) class inheritance hierarchy to find the right method. There aren't a lot of alternatives for invoking methods; those are rarely used and easy to spot due to boilerplate.  
 
The right way to solve most problems in Java is to create a new class in a new source file. Alternatives include creating new methods (like dashes()), static methods, inner classes, and lambdas. None of these scale up particularly well. Class inheritance seemed like a good idea at the time, but turned out to be a trap. The only thing that scaled up well was making new unrelated classes. We did that often. 

The gang-of-four Design Patterns book was published just before Java 1.0, and had a huge influence on Java libraries. Teams of developers found it hard to apply the knowledge in the book while preserving encapsulation, so bits of the underlying complexity tended to peek through the pattern-level API. Over time frustrated developers might let the underlying code escape without removing the pattern code that was supposed to contain it. The book gave us a vocabulary for handling complexity by creating more classes. We made more classes. 

What you'll find in many long-lived Java projects is a lot of public classes with broad APIs that leak a bit of their internals. The leaks often compound the proliferation of classes. A developer can feel the complexity rise as names get more absurd - SimpleAdapterBridgeFacade.java for example.

Toby Thain proposed that Scala was better in his quick answer. Here's what I did for dashes in Scala:

[code Scala]
    "-" * censoredWord.length
[/code]

I didn't split it out into a special method. I just typed Scala code. In this example * is a method, but not on String. It comes from StringLike.scala via a technique unfortunately named "Pimping." (See http://java.dzone.com/articles/scala-snippets-4-pimp-my if you've got a little time to digest.) Scala gives us access to many different styles of programming. The * operator here feels like procedural programming to me; * manipulates Strings, but isn't fundamental to being a String. The problems that Design Patterns addresses are much less likely to come up and take much less bulk in the code. (See http://alvinalexander.com/scala/how-scala-killed-oop-strategy-design-pattern#What_about_those_other_OOP_design_patterns .)

Java's creators decided to provide one simple way to invoke methods. Java's community decided to take that to its logical limit. I think that's much more relevant than syntax.  