---
layout: post
title: "Shutdown Hooks"
date: 2004-05-09
permalink: /archive/2004/05/shutdown-hooks/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2004/05/shutdown_hooks_2.html
---

I just handed in my last assignment for my masters degree, completing a ten-year effort. Maybe there is a reason why they put a "Slow Children" sign in front of our house. And JSDK 1.5 is rolling out some time soon. It's a good week for a blog about finishing things -- time for an article about shutdown hooks.

A shutdown hook is a Thread designed to be run after a program receives a signal to exit, but before daemon threads stop, finalizers run, and the JVM goes poof. Shutdown hooks are great for clearing dirty caches, closing out open resources, and announcing this shutdown to other processes.

In 1999 I sent Sun a "request for enhancement" for the equivalent of C's onexit() facility. I was building this funky distributed logging system and needed a way to record cached log messages if someone hit control-C or called System.exit(). The JSDK of the day, 1.2 I suppose, didn't offer me anything beyond runFinalizersOnExit(). I needed to write log messages and flush the system, which I couldn't do reliably if the objects were in the process of dissolving. The team found a hacky way to solve the immediate problem; we added our own way to shut down the system via messaging, and tried to reeducate the rest of the company to use it instead of control-C (but that's another blog).

Sun added the shutdown hook feature in JSDK 1.3, about eighteen months later. RFEs take patience, but make the system better for us all. The company that asked me to build that logging system is long gone, but I've used shutdown hooks on a dozen projects since they were introduced.

Here's a code segment for setting up a shutdown hook to clean out an arbitrary Cache:

```java
...
//A static inner class Runnable.
        private static class CacheCleaner
            implements Runnable
        {
            private Cache cache

            private CacheCleaner(Cache cache)
            {
                this.cache = cache;
            }

            public void run()
            {
                try
                {
                    cache.clean();
                }
                catch(CacheException ce)
                {
                    Log.IT.log(Level.SEVERE,"Unable to clean cache during shutdown",ce);
                }
            }
        }
...
//Inside the Cache class:
    private CacheCleaner cleaner = new CacheCleaner(this);

    public Runnable getShutdownRunnable()
    {
        return cleaner;
    }
...

//in setup code somewhere.
        Thread hook = new Thread(cache.getShutdownRunnable());
        Runtime.getRuntime().addShutdownHook(hook);
```

I like Runnable implementations for my shutdown hooks instead of extending Thread. It keeps the API for my stuff separate from the zoo of methods available for Thread. In the library side of the code, I make the shutdown Runnable accessible so that I can control the order that things shut down from another part of the code. I usually have to customize the shutdown order. It changes via negotiation with the rest of the system. I try to log what's going on if things go wrong; debugging as the system fades away can be frustrating.

Shutdown hooks need to be quick, deadlock-safe and can not start new threads. Read through the JSKD API in the [addShutdownHook()](http://java.sun.com/j2se/1.4.2/docs/api/java/lang/Runtime.html#addShutdownHook(java.lang.Thread)) method before trying this out.

Night school and RFEs exist on a different time scale. An RFE in the JSDK core kit may take a year or two to sort out, if it's accepted. Before posting an RFE for some core thing, make sure that the only way to add the feature is through the change you are suggesting.

Reading: *Chessmen of Mars*, Burroughs.  

Hearing: *La Mort de Cleopatre*, Berlioz.
