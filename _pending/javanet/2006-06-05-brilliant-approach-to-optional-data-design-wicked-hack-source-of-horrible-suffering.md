---
layout: post
title: "Brilliant Approach to Optional Data Design? Wicked Hack? Source of Horrible Suffering?"
date: 2006-06-05
permalink: /archive/2006/06/brilliant-approach-to-optional-data-design-wicked-hack-source-of-horrible-suffering/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2006/06/brilliant_appro.html
---

I've finally added message selector support for Topics in [SomnifugiJMS](https://somnifugijms.dev.java.net/), a single-process implementation of a Java Messaging Service. It's SomnifugiJMS's 14th alpha release. (Message selectors for Queues will be more difficult, but is the last piece keeping SomnifugiJMS in alpha releases. I think I can get it to work with j.u.c.Conditions and some extra work, but haven't had the time to design it yet.)

At JavaOne, I met up with Linda Schneider, one of the key people working on [https://mq.dev.java.net/](https://mq.dev.java.net/), at JavaOne. She sent me a pointer to the message selector implementation in the JMS reference implementation. The JMS RI just switched to [CDDL](http://www.sun.com/cddl/), which is [a file-based license](http://www.opensolaris.org/os/about/faq/licensing_faq/#CDDL-combo), so I picked up their code, edited it to play nice with my own, and now have message selectors for Topics. They even have a good set of tests in a main method; the JMS RI predates JUnit by a year or so.

The only snag I hit was that I use member fields in SomniMessage to hold information that every message should hold, but the JMS RI Selector API expects a Map.

```java
public class SomniMessage
    implements Message
{
...
    private String messageID;
    private long timeStamp=0;
    private String correlationID;
    private Destination replyTo;
    private Destination destination;
    private int deliveryMode;
    private long expirationTime;
    private int priority=0;
    private int producerCount=Integer.MIN_VALUE;
    private String producerConnectionClientID;
    private boolean readOnly=false;
    private boolean redelivered=false;
...
}
```

```java
public synchronized boolean match(Map properties, Map fields)
        throws SelectorFormatException
    { ... }
```

My first thought was to recode the JMS RI Selector to use javax.jms.Message-specific getters. That sounded tedious; I'm not familiar with the code, and am not overly interested in writing or modifying an SQL92 parser. Linda emailed, "[Selector.java is] huge because there is a lot of different items to parse," which seems to say it all. My second thought was to recode SomniMessage to use a Map to store this sort of information. In SomnifugiJMS these fields always have some value, so a Map just seems wrong. SomnifugiJMS is supposed to be faster and simpler than database JMS implementations, especially for small-scale work (which rarely needs message selectors). I didn't want to loose that simplicity to get the message selectors working.

I pondered a bit and came up with a third option: use reflection to implement a Map that calls getters when given a field name as a key:

```java
class ReflectingMap
    implements Map
{
    private static final String GETTERPREFIX = "get";

    private Object hasGetters;

    ReflectingMap(Object hasGetters)
    {
        this.hasGetters = hasGetters;
    }

    private String getterNameForKey(String key)
    {
        return GETTERPREFIX+key;
    }

    public boolean containsKey(Object key)
    {
        if(!(key instanceof String))
        {
            return false;
        }
        try
        {
            hasGetters.getClass().getMethod(getterNameForKey((String)key));
            return true;
        }
        catch(NoSuchMethodException nsme)
        {
            return false;
        }
    }

    public Object get(Object key)
    {
        if(!(key instanceof String))
        {
            return null;
        }
        try
        {
            Method method = hasGetters.getClass().getMethod(getterNameForKey((String)key));
            return method.invoke(hasGetters);
        }
        catch(NoSuchMethodException nsme)
        {
            return null;
        }
        catch(IllegalAccessException iae)
        {
            throw new SomniRuntimeException(iae);
        }
        catch(InvocationTargetException ite)
        {
            throw new SomniRuntimeException(ite);
        }
    }

    public Object put(String key,Object value)
    {
        throw new UnsupportedOperationException("I haven't done this yet. Maybe someday when I think about setters.");
    }

    public Object remove(Object key)
    {
        throw new UnsupportedOperationException("This will never work. What are you doing?");
    }

    //All other methods throw new UnsupportedOperationException("I haven't done this yet.");
}
```

I could implement a general purpose put() method by slipping another Map inside this one, and delegating put()s and get()s to that map for keys that hasGetters does not have. I can't implement the whole Map interface this way because there's no way to remove arbitrary keys. What would removing a field even mean?

I think that's an interesting piece of code, especially given the talk of invokeDynamic's evil partner, "changing the members of an object," at a [JavaOne talk](https://www28.cplan.com/javaone06_cv_124_1/sessions_catalog.jsp?ilc=124-1&ilg=english&isort=1&is=%3CISEARCH%3E&ip=no&itrack=+&isession_type=+&isession_id=TS-3886&iabstract=&ispeaker=&ispk_company=). It's an interesting choice for sometimes-optional fields when designing data structures.

However, "Interesting" might mean that it'll be a source of horrible suffering.

First, code that works this way will have to have `if(containsKey())` or `if(yourRef==null)` forks everywhere, will have to handle NullPointerExceptions, or (worst and most likely) will spew NullPointerExceptions. I'll predict the same problems as I've seen using [BeanShell's](http://beanshell.org/) [voids](http://beanshell.org/manual/specialvarsvalues.html#Undefined_Variables). Variables that don't exist in the a BeanShell name space are void (instead of null or some default value). Developers sometimes should check `if(hisRef==void)`, but usually don't.

Second, the keys are Strings, so there's no great way to predict what might be a key. For message selectors, I know from the JMS specification that the keys will be a small, defined set of Strings that happen to match method names. Perhaps an Enum of possible keys would better define the universe of possible optional members, but that shifts back toward the unsatisfying "this member hasn't been set yet" pattern for accessors. I can live with these problems in my own code, but I want to know these land mines are out there, especially after a decade of trying to avoid using nulls as magic error codes.

In my ears: Beethoven's Missa Solimnis. Wow.
