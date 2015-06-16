Testing Changes to TypeSafe Config

TL/DR - I found a workable compromise for testing with different configurations using [typesafe config](https://github.com/typesafehub/config) without starting a new JVM. See this [gist](https://gist.github.com/dwalend/5a193daa24af8dbfbdc5).

I needed a good way to test [Shrine](http://catalyst.harvard.edu/services/shrine/)'s Data Steward Web App with different configurations. Shrine controls its configuration via [typesafe config](https://github.com/typesafehub/config), which loads the config from a hierarchy of sources - primarily files on the classpath and java.lang.System properties. I thought of three options. None are perfect. One is good enough.

I want the code to use simple structures that draw their configuration from a typesafe [Config](https://github.com/typesafehub/config/blob/master/config/src/main/java/com/typesafe/config/Config.java) object. I want to be able to replicate the technique shamelessly without sharing code between subprojects. Further, I did not want that Config exposed overmuch in my system's API. I should be able to use Scala's singleton [```object```s] (https://raseshmori.wordpress.com/2013/06/20/scala-part-4-classes-objects/) where I need singletons. Shrine's configuration is unchanging once set - except for during tests - so having it front-and-center distracts from more important details. I should not have to couple my code via constructor parameters that make me wish for an aspect-oriented style. It's just config after all.

The most brute force approach is to use a different JVM process for testing each configuration. That's how I'd have handled this back in the age of [ant](http://zeroturnaround.com/rebellabs/java-build-tools-part-2-a-decision-makers-comparison-of-maven-gradle-and-ant-ivy/). However, Shrine uses maven. Creating a new JVM process for tests is out-of-model in Shrine and possibly in any maven project. (I skipped from ant to [sbt](todo link to zeroturnaround's reference). During the age of maven I was at MathWorks where we used make. Maven feels very alien.) I don't know a tasteful way to spin up several new processes for running tests in the same maven subproject.

The older code in Shrine uses config objects, skipping typesafe config to test parts of the system in isolation. A maven subproject uses typesafe config to drive various abstract-factory-pattern-inspired parts to construct parts for Shrine. Testing different configurations means constructing specialized config instances in the test code without using Config. The approach definitely solved the problem, but it adds a long, twisty maze between the config files where a value is defined and the code that actually uses it. Following that path adds about five minutes to each task involving a config key-value pair. The approach seems particularly invasive because singletons that could have been ```object```s have to be constructed class instances. To keep the whole works from becoming a furball the existing pattern tightly couples the Shrine system around a single instance of a ShrineConfig class. Testing more than a single subsystem is very difficult. I found myself repeating my criticisms of Spring mixed with profane mutterings about [GLOOP](http://perl.plover.com/yak/design/samples/slide004.html). I want to clean up that part of the code, not add to the confusion.

I decided to give typesafe config just a little mutability and use [defs](http://blog.jessitron.com/2012/07/choices-with-def-and-val-in-scala.html) where I needed configurable values. Using defs for configurable values forces them to be reevaluated each time the owning code accesses them; there will always be a little in-memory overhead. However, any part of the system can access the Config when needed, with a key's name right next to the def that supplies the value. 

```Scala
  def dbUrl = ExampeConfigSource.config.getString("database.url")
```

My first hack at the solution was to set and clean up system properties in a try/finally block, and use [ConfigFactory](https://github.com/typesafehub/config/blob/master/config/src/main/java/com/typesafe/config/ConfigFactory.java)'s resetCache method. The Data Steward App is a web app showing a database; I can afford considerable overhead, but it just seemed sloppy. I won't share some of the uglier code, but the progression to something clean went fine. The second hack was to put the try/finally into a higher-order function. The third step started to look less hacky; I replaced the cache flush and system properties with API to use [Config's withFallback()](https://github.com/typesafehub/config#merging-config-trees) to get the default (cached and unchanging) Config. I put the changable Config inside an [AtomicReference](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/atomic/package-summary.html) for minimal concurrent safety. Finally I dressed it up in a Scala-style [Try/Success/Failure](todo) to try to detect one class of possible concurrency bugs that should never happen.

Here's what the code looks like:

```Scala
import java.util.concurrent.atomic.AtomicReference
import scala.util.{Failure, Success, Try}
import com.typesafe.config.{Config, ConfigFactory}

/**
Use to tweak a Config without clearing and reloading a new config (for testing).

@author dwalend
 */
class AtomicConfigSource(baseConfig:Config) {
  val atomicConfigRef = new AtomicReference[Config](ConfigFactory.empty())
 
  /**
   * Get the atomic Config. Be sure to use defs for all config values that might be changed.
   */
  def config:Config = atomicConfigRef.get().withFallback(baseConfig)
 
  /**
   * Use the config in a block of code with just one key/value replaced.
   */
  def configForBlock[T](key:String,value:AnyRef,origin:String)(block: => T):T = {
    val configPairs = Map(key -> value)
    configForBlock(configPairs,origin)(block)
  }
 
  /**
   * Use the config in a block of code.
   */
  def configForBlock[T](configPairs:Map[String, _ <: AnyRef],origin:String)(block: => T):T = {
    import scala.collection.JavaConverters.mapAsJavaMapConverter
 
    val configPairsJava:java.util.Map[String, _ <: AnyRef] = configPairs.asJava
    val blockConfig:Config = ConfigFactory.parseMap(configPairsJava,origin)
    val originalConfig:Config = atomicConfigRef.getAndSet(blockConfig)
    val tryT:Try[T] = Try(block)
 
    val ok = atomicConfigRef.compareAndSet(blockConfig,originalConfig)
 
    tryT match {
      case Success(t) => {
        if(ok) t
        else throw new IllegalStateException(
          s"Expected config from ${blockConfig.origin()} to be from ${atomicConfigRef.get().origin()} instead.")
      }
      case Failure(x) => {
        if(ok) throw x
        else throw new IllegalStateException(
          s"Throwable in block and expected config from ${blockConfig.origin()} to be from ${atomicConfigRef.get().origin()} instead.",x)
      }
    }
  }
}
```

To use it, I create a Scala object to hold the config:

```Scala
/**
 * A little object to let you reach your config from anywhere.
 * 
 * @author dwalend
 */
object ExampeConfigSource {
  //load from application.conf and the usual typesafe config sources
  val atomicConfig = new AtomicConfigSource(ConfigFactory.load()) 
 
  def config:Config = atomicConfig.config
 
  def configForBlock[T](key:String,value:AnyRef,origin:String)(block: => T):T = 
    atomicConfig.configForBlock(key,value,origin)(block)
}
```
