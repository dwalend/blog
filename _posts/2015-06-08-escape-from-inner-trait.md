---
layout: post
title: Escape to an Inner Object
comments: True
---
## An Inner Trait Puzzle

I blundered into this strange puzzle with visibility, inner traits, and inner objects while putting together code to plug [Semirings into Dijkstra's algorithm](https://github.com/dwalend/ScalaGraphMinimizer). I'm not sure if the problem rates a bug report, or two, or a feature request, or is just something I don't fully understand. I'd like to hear some advice before reporting (or not reporting) it.

Find some code you can paste into the REPL in this [gist](https://gist.github.com/dwalend/464a3c69c94165f02cd4) to try different hacks.

Here's code that illustrates the dissonance fully:

```scala
// A top-level trait defines a def
trait TopTrait {
  def topDef:String
}

// A trait that has an inner trait that extends TopTrait
trait BeyondTrait {

  def innerThing:InnerTrait

  trait InnerTrait extends TopTrait{
    def innerDef = "innerDef"
    def topDef = "topDef"
  }
}

// A class that extends that more complex trait
class Beyond extends BeyondTrait {

  // An inner class that extends the InnerTrait, and a def that implements the more complex trait's contract
  override def innerThing = new InnerTrait{
    def beyondDef = "innerThing from beyond"
  }
}

// A class that uses the class that implements the complex trait
class OuterClass(beyond: Beyond){

  object InnerObject {

    // this won't compile
    // "private value beyond escapes its defining scope as part of type OuterClass.this.beyond.InnerTrait"
    // the compiler won't walk up the tree to find TopTrait
    // and it won't decide that it has access to the private beyond member
    val innerThing = beyond.innerThing

    // and innerThing won't be defined for these two vals
    val topDefResult = innerThing.topDef

    val innerDefResult = innerThing.innerDef

    val comboResult = s"$innerDefResult and $topDefResult"
  }
}
```

It looked like it would work; even Intellij thought it would. However, the REPL tells me: 

```bash
:20: error: private value beyond escapes its defining scope as part of type OuterClass.this.beyond.InnerTrait
     val innerThing = beyond.innerThing
```

I'd blundered into this problem while refactoring some code to better fit the Law of Demeter and make it more readable. The original code just used the outer class' reference inside the inner object. It was cluttered, but it worked.

```scala
class OuterClass(beyond: Beyond){
...
  object InnerObject {
...
    //this works as expected
    val innerDefResult = beyond.innerThing.innerDef

    //as does this
    val topDefResult = beyond.innerThing.topDef
...
```

I didn't see why this should work but my first example did not. One of the reasons I like Scala is that I get to learn something new most days, so I decided to invest an hour and learn about what is going on.

The error message says beyond is private. Making ```beyond``` a public member appeases the compiler, but doesn't provide much understanding:

```scala
class OuterClass(val beyond: Beyond){
...
```

Assigning a type of TopTrait to innerThing compiles past that, but the compiler can't find the inner trait's def. This seems correct to me and is the fix I settled for in the project's code. However, it doesn't explain what's going on.

```scala 
    val innerThing:TopTrait = beyond.innerThing
```

I think I've tilled up two problems. First, some things - types from the outer class' member variables - that should be visible inside the inner object are not. Second, the compiler is giving up inferring innerThing's type instead of either using the publicly visible TypeTrait or shrugging and inferring that the type is Any.

Or possibly the behavior is correct, my intuition is faulty, and there's more for me to learn from this code. Thoughts?

