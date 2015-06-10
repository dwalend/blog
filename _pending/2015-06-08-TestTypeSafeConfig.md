Testing Changes to TypeSafe Config

TL/DR - See this [gist](todo)

I needed a good way to test SHRINE's Data Steward App with different configurations. Shrine controls its configuration via typesafe config, which loads the config from a hierarchy of sources - primarily files on the classpath and Java system properties. I thought of three options, none of which was perfect.

I wanted the code to be simple structures that drew their configuration from a typesafe Config object. Further, I did not want that Config exposed overmuch in my system's API. I should be able to use Scala ```object```s in appropriate places. I should not have to add strange parameters through my code that make me long for an aspect-oriented style. SHRINE's configuration is unchanging except for during tests so having it front-and-center is simply distracting. 

The most brute force approach is to use a different jvm process for testing each configuration. That's how I'd have handled this back in the age of ant. However, SHRINE uses maven. Creating a new process for tests is out-of-model in SHRINE and likely in maven. Further, I skipped from ant to sbt (MathWorks uses make) and maven seems very alien. I don't know a tasteful way to spin up several new processes for running tests in the same maven subproject.

The older code in SHRINE uses config objects, skipping typesafe config to testing parts of the system in isolation. A SHRINE subsystem uses typesafe config to make the config objects; those objects in turn plug into constructors of the things that do the work. Testing different configurations means constructing different config objects in the test code. The approach definitely solved the problem, but it put a long, twisty maze between the config files where a value is defined and the code that actually uses it. Following that path adds about ten minutes to each task involving a config key-value pair. The approach seems particularly invasive because singletons that could have been ```object```s have to be constructed class instances. Further, the existing pattern tightly couples the whole system around a single ShrineConfig class; testing more than a subsystem is very difficult. I found myself repeating my criticisms of Spring mixed with profane mutterings about pattern GLOOP. I want to clean up that part of the code, not add to it.

I decided to give typesafe config just a little mutability and use defs where I needed configurable values. Using defs for configurable values forces them to be reevaluated each time the owning code accesses them; there will always be a little overhead. However, the owning code has the Config key's name right next to the value. 

The Data Steward App is nine-tenths a web app showing a database. I can afford considerable overhead, but it just seemed sloppy. I won't share some of the uglier code, but the progression to something tollerable went fine. My first hack at the solution was to set and clean up system properties in a try/finally block, and use the TODO's resetCache. The second hack was to put that into a higher-order function. The third step started to look less hacky; I replaced the cache flush and system properties with API to take a Config and use withFallback to get the default (cached and unchanging) Config. I added an AtomicReference for minimal concurrency support, and dressed it up in a Scala-style Try/Success/Failure to try to detect one class of possible concurrency bugs that should never happen.

Here's what the code looks like:

TODO

To use it, I create a Scala object to hold the config:

TODO

Then use defs where I need configurable values that tests can change:

TODO

