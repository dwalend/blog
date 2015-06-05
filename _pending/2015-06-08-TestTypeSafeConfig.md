Testing Changes to TypeSafe Config

TL/DR

Which Compromise? - New JVM vs. config objects vs. changing the config?

config values must be defs - cost?

And the whole path has to be defs

First hack -- system properties, resetCache, try/finally

Second hack -- higher-order function

Third hack -- injecting a config, withFallback

Forth hack -- Try/Success/Failure

Fifth hack -- gist

