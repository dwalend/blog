Testing Changes to TypeSafe Config

TL/DR - I found an 11/13ths good compromise for testing with different configurations using [typesafe config](https://github.com/typesafehub/config). See this [gist](https://gist.github.com/dwalend/5a193daa24af8dbfbdc5).

I needed a good way to test SHRINE's Data Steward Web App with different configurations. Shrine controls its configuration via [typesafe config](https://github.com/typesafehub/config), which loads the config from a hierarchy of sources - primarily files on the classpath and Java system properties. I thought of three options, none of which was perfect.

I wanted the code to use the simplist structures that drew their configuration from a typesafe [Config](https://github.com/typesafehub/config/blob/master/config/src/main/java/com/typesafe/config/Config.java) object. Further, I did not want that Config exposed overmuch in my system's API. I should be able to use Scala singleton [```object```s] (https://raseshmori.wordpress.com/2013/06/20/scala-part-4-classes-objects/) in appropriate places. SHRINE's configuration is unchanging once set - except for during tests - so having it front-and-center distracts from more important details. I should not have to add strange parameters through my code that make me reach for an aspect-oriented style. It's just config after all.

The most brute force approach is to use a different jvm process for testing each configuration. That's how I'd have handled this back in the age of [ant](http://zeroturnaround.com/rebellabs/java-build-tools-part-2-a-decision-makers-comparison-of-maven-gradle-and-ant-ivy/). However, SHRINE uses maven. Creating a new process for tests is out-of-model in SHRINE and likely in any maven project. (I skipped from ant to sbt. During the age of maven I was at MathWorks. Mathworks used make. Maven feels very alien.) I don't know a tasteful way to spin up several new processes for running tests in the same maven subproject.

The older code in SHRINE uses config objects, skipping typesafe config to test parts of the system in isolation. A SHRINE config subproject uses typesafe config to make the config objects; those objects in turn plug into constructors of the things that do the work. Testing different configurations means constructing specialized config instances in the test code. The approach definitely solved the problem, but it put a long, twisty maze between the config files where a value is defined and the code that actually uses it. Following that path adds about five minutes to each task involving a config key-value pair. The approach seems particularly invasive because singletons that could have been ```object```s have to be constructed class instances. To keep the whole works from becoming a tangly furball the existing pattern tightly couples the larger system around a single instance of a ShrineConfig class. Testing more than a subsystem is very difficult. I found myself repeating my criticisms of Spring mixed with profane mutterings about pattern [GLOOP](TODO). I want to clean up that part of the code, not add to the confusion.

I decided to give typesafe config just a little mutability and use [defs](TODO) where I needed configurable values. Using defs for configurable values forces them to be reevaluated each time the owning code accesses them; there will always be a little in-memory overhead. However, any part of the system can access the Config when needed, with a key's name right next to the def that supplies the value. 

```Scala
TODO
```

My first hack at the solution was to set and clean up system properties in a try/finally block, and use [ConfigFactory](https://github.com/typesafehub/config/blob/master/config/src/main/java/com/typesafe/config/ConfigFactory.java)'s resetCache. The Data Steward App is nine-tenths a web app showing a database; I can afford considerable overhead, but it just seemed sloppy. I won't share some of the uglier code, but the progression to something clean went fine. The second hack was to put the try/finally into a higher-order function. The third step started to look less hacky; I replaced the cache flush and system properties with API to use [Config's withFallback()](https://github.com/typesafehub/config#merging-config-trees) to get the default (cached and unchanging) Config. I added an [AtomicReference](TODO) for minimal concurrent safety. Finally I dressed it up in a Scala-style Try/Success/Failure to try to detect one class of possible concurrency bugs that should never happen.

Here's what the code looks like:

```Scala
TODO
```

To use it, I create a Scala object to hold the config:

```Scala
TODO
```
