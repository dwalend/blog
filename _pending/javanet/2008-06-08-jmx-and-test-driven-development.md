---
layout: post
title: "JMX and Test-Driven Development"
date: 2008-06-08
permalink: /archive/2008/06/jmx-and-test-driven-development/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2008/06/jmx_and_testdri_1.html
javanetTopics:
  - Testing
---

At JavaOne this year I did a [short talk](http://today.java.net/pub/a/today/2008/05/08/j1-2k8-mtW07.html?page=last#thread) on using JMX in test-driven development. The talk was based on what I discovered working with JMX on another project, and delved deeper into while adding JMX support to [SomnifugiJMS](https://somnifugijms.dev.java.net/) as part of [release 21](https://somnifugijms.dev.java.net/servlets/ProjectDocumentList?folderID=9103&expandFolder=9103&folderID=0). Test-driven development worked extremely well when combined with JMX. JMX should help testing systems with some defined life cycle.

**Test Driven Development**

[Test driven development](http://en.wikipedia.org/wiki/Test_driven_development) maximizes the benefits of writing tests by demanding that we write the tests before the code that will attempt to pass those tests. It ensures some level of quality because all work completed will pass at least one test. Developers establish a rapid, highly iterative development loop. The tests provide an easy way to measure progress. Managers enjoy having the detailed insight that a list of tests gives them. When I've got a little time away from the day job to do open source work, I can write a small test, then get back to making the test pass later.

Test code and JMX monitoring code have a shared programatic problem. We promise ourselves that we'll go back and write test code later, and will add JMX monitoring code before we need it. Deadlines loom large, we get things working, and move on to the next project without doing either job well. Test driven development breaks that vicious cycle for tests. Using JMX in the tests breaks the cycle for both. (Thanks to [Chris](http://weblogs.java.net/blog/editors/) for pointing this out after my talk.)

The test driven development loop is pretty simple. First, decide what feature to implement next. Design the API for that feature. Next, write a test for that feature and observe that all the other tests still pass. Finally write code to make the new test pass. Repeat until tests of all the features pass. Like [John says](http://weblogs.java.net/blog/johnsmart/archive/2008/06/tests_first_or.html), you can write the tests just after the code so long as you create tests in the same flow and are done before your work escapes your head and your desktop. Your code will have tests before it leaves the cradle.

Test driven development presents some challenges. You have to have some clue about what features to develop before starting the loop. You need to have some idea about the classes and methods that will form your API. Test driven development works best for black-box testing, so you'll have to expose enough of your system to test your work. In Java, that often means adding public access to classes and methods, hacking in via reflection, or excising test code out of packages and classes after you run your tests. JMX can help with these challenges somewhat, by providing an alternative way to get information out.

**JMX**

JMX is the [Java Management eXtension](http://java.sun.com/j2se/1.5.0/docs/guide/jmx/index.html) API (from the late 1990s -- the X dates it). JMX provides a standard way for Java systems to report their state and health to the outside world, and to allow themselves to be adjusted and tuned via standard tools. It provides two main styles of interacting with the running system: MBeans expose select getters, setters and methods to outside control. Notifications push information out from the Java system to listeners.

MBeans expose select methods on a class to the JMX system. Java classes follow a special design pattern -- the MBean -- and registering instances of the class with an MBean server. An MBean interface defines the exposed methods. You could use this interface to expose useful attributes to make them observable in tests, and to set attributes and call methods in order to drive tests. For testing, the MBean interface doesn't provide any great advantage over just using public methods. However, I found I could use the MBean's existence in the MBean server to provide a simple test of an object's lifecycle.

JMX also specifies using Notifications to signal lifecycle and state changes from inside objects via the speaker/listener pattern. Add NotificationListeners to objects that implement the NotificationEmitter interface. When something of note happens within the MBean object, have it send a Notification to the listeners. This speaker/listener pattern works well in testing. It provides a good alternative to exposing state because the exposure is controlled by your code sending the Notifications, not via public method calls to your object. Further, it lets you write tests of lifecycle changes instead of tests based on methods. Lifecycle events are easier to get right early in development, generally easier to change, and are less likely to change over time than method signatures. Your tests will be less brittle and you'll spend less time rewriting them.

**JMX-Based Tests**

I found a few key features to make the code easy to test, and a few key features to test. MBeans will be easier to test if each MBean knows its ObjectName. Tests should check that expected MBeans exist. Because the MBean server will hold on to stray references, tests should check that MBeans are cleaned up at the end of their useful life.  Notifications need to be machine-understandable; I subclassed Notification and added an enum field. Define the MBean interface and the Notification help in the same file to make it easier for others to find the Notifications. Tests should check that the code sent the expected Notifications exercised during the test run. These code examples are from [SomniMessageConsumer.java](https://somnifugijms.dev.java.net/source/browse/somnifugijms/v3/source/somnifugi/net/walend/somnifugi/SomniMessageConsumer.java?view=markup), [SomniMessageConsumerMBean.java](https://somnifugijms.dev.java.net/source/browse/somnifugijms/v3/source/somnifugi/net/walend/somnifugi/SomniMessageConsumerMBean.java?view=markup) and [MonitorTest.java](https://somnifugijms.dev.java.net/source/browse/somnifugijms/v3/source/somnifugi/net/walend/somnifugi/test/MonitorTest.java?view=markup).

**Each MBean Knows its ObjectName**

To make each MBean know its object name, put the method in the MBean interface:

```java
public interface SomniMessageConsumerMBean
{
    public ObjectName getObjectName();
    ...
}
```

and fill it in:

```java
public abstract class SomniMessageConsumer
    implements MessageConsumer, SomniMessageConsumerMBean, NotificationEmitter
{

...
    private final ObjectName objectName;

    protected SomniMessageConsumer(String name,
                                             Takable feed,
                                             SomniExceptionListener somniExceptionListener,
                                             String destinationName,
                                             SomniSession session)
    {

...
        try
        {
            objectName = new ObjectName("net.walend.somnifugi:type="
                                                       +this.getClass().getName()+",
                                                       name="+name);
            registerWithJMX();
        }
        catch(MalformedObjectNameException mone)
        {
            throw new SomniRuntimeException("JMX problem with "+this.getName(),mone);
        }
    }
```

Using the MBean in your test code becomes easy; you aren't constantly writing queries to find the right MBean.

```java
expectedMBeans.add(subscriber.getObjectName());
```

**Tests Check for Expected MBeans**

I check what MBeans were registered in the server at least twice per test, so I carved out a method to make sure that everything was there, with nothing extra, using an MBean query.

```java
@SuppressWarnings("unchecked")
    void checkExpectedMBeanNames(Set<ObjectName> expected)
        throws MalformedObjectNameException,
                   MBeanException,
                   AttributeNotFoundException,
                   InstanceNotFoundException,
                   ReflectionException
    {
        MBeanServer server = ManagementFactory.getPlatformMBeanServer();

        ObjectName query = new ObjectName("net.walend.somnifugi:*");
        Set<ObjectName> result = (Set<ObjectName>)server.queryNames(query,null);

        Set<ObjectName> remainder = new HashSet<ObjectName>(result);
        remainder.removeAll(expected);

        assertTrue("Remainder is not empty: "+remainder,remainder.isEmpty());

        assertEquals(expected,result);
    }
```

Then I fell into a regular pattern in the tests -- The code makes all the JMS parts, then makes sure they are all in the server.

```java
SomniTopicConnection connection = (SomniTopicConnection)SomniJNDIBypass.IT.getTopicConnectionFactory().createTopicConnection();
        SomniTopicSession session = (SomniTopicSession)connection.createTopicSession(false,Session.AUTO_ACKNOWLEDGE);
        String topicName = "testNotifyTopicSubscribers";
        SomniTopic topic = SomniJNDIBypass.IT.getTopic(topicName);
        SomniTopicPublisher publisher = (SomniTopicPublisher)session.createPublisher(topic);
        SomniTopicSubscriber subscriber = (SomniTopicSubscriber)session.createSubscriber(topic);

        connection.start();

        MBeanServer server = ManagementFactory.getPlatformMBeanServer();

        Set expectedMBeans = new HashSet();
        expectedMBeans.add(connection.getObjectName());
        expectedMBeans.add(topic.getObjectName());
        expectedMBeans.add(session.getObjectName());
        expectedMBeans.add(publisher.getObjectName());
        expectedMBeans.add(subscriber.getObjectName());
        checkExpectedMBeanNames(expectedMBeans);
```

**Tests Check that MBeans are Cleaned Up**

The second call to checkExpectedMBeanNames() makes sure that the test cleans out all of the MBeans at the end of the test. If the code doesn't clean them out, the server holds onto a reference, which prevents the garbage collector from reclaiming the memory. Some of these objects hold many references, so a leak can use a lot of memory.

```java
connection.close();
        SomniJNDIBypass.IT.removeTopic(topicName);

        expectedMBeans.clear();
        checkExpectedMBeanNames(expectedMBeans);
    }
```

**Machine-Understandable Notifications**

For a finer lifecycle test, I created machine-understandable Notification subclasses. Notification comes with a String type, Object source, and a long sequenceNumber. The source and sequence number are pretty straightforward to use. The type String offers very little. I made a subclass to carry a machine-understandable enum and to help with consistency in the type string. This enum has to implement SomniNotificationType. There's no way to enforce that in Java, but it's at least javadoced. getSomniNotificationType() provides a way to check the enum in code.

```java
@SuppressWarnings("serial")
public class SomniNotification
    extends Notification
    implements Serializable
{
    private final SomniNotificationType noteType;
    private final String partName;

    public SomniNotification(SomniNotificationType noteType,
                                         Object source,long sequenceNumber,
                                         String partName)
    {
        super(noteType.getTypeString(),source,sequenceNumber,partName + noteType.getVerbPhrase());

        this.noteType = noteType;
        this.partName = partName;
    }

    public SomniNotificationType getSomniNotificationType()
    {
        return noteType;
    }

    public String getPartName()
    {
        return partName;
    }

    /**
    To be implemented by an enum defined in the MBean interface.
    */
    public static interface SomniNotificationType
    {
        public String getTypeString();

        public String getVerbPhrase();
    }

}
```

**Collocate the MBean interface and Notification Enum**

I put the notification enum in the same file, as a static inner class of the MBean interface. This grouping means there's only one place to look in source code to understand how the MBean interacts with a JMX monitor.

```java
public interface SomniMessageConsumerMBean
{
...
    @SuppressWarnings("serial")
    public static enum SomniMessageConsumerNotificationType
        implements SomniNotification.SomniNotificationType, Serializable
    {
        CONSUMERCLOSED("net.walend.somnifugi.ConsumerClosed"," closed"),
        MESSAGECONSUMED("net.walend.somnifugi.MessageConsumed"," consumed"),
        MESSAGELISTENERCHANGED("net.walend.somnifugi.MessageListenerChanged"," changed"),
        MESSAGETIMEDOUT("net.walend.somnifugi.MessageTimedOut"," timed out");

        private final String typeString;
        private final String verbPhrase;

        private SomniMessageConsumerNotificationType(String typeString,String verbPhrase)
        {
            this.typeString = typeString;
            this.verbPhrase = verbPhrase;
        }

        public String getTypeString()
        {
            return typeString;
        }

        public String getVerbPhrase()
        {
            return verbPhrase;
        }
    }
```

**Tests Check Notifications Sent During the Run**

I created TestNotificationListener to test that the system was producing the right notifications. It takes a list of expected notifications in the constructor, and verifies that all the notifications came in the right order inside a check() method.

```java
private static class TestNotificationListener
        implements NotificationListener
    {
        private List expected;
        private List received = new ArrayList();

        TestNotificationListener(List expected)
        {
            this.expected = expected;
        }

        public void handleNotification(Notification notification, Object handback)
        {
            SomniNotification somniNotification = (SomniNotification)notification;
            received.add(somniNotification.getSomniNotificationType());
        }

        void check()
        {
            assertEquals(expected,received);
        }
    }
```

In the test, I give the TestNotificationListener a list of notifications, do things during the test, and make sure the right notifications were sent. This approach lets me define the expected lifecycle steps within the class, and observe them from outside, without using public methods.

```java
List expected = new ArrayList();
        expected.add(SomniMessageConsumerMBean.SomniMessageConsumerNotificationType.MESSAGECONSUMED);
        expected.add(SomniMessageConsumerMBean.SomniMessageConsumerNotificationType.MESSAGECONSUMED);
        expected.add(SomniMessageConsumerMBean.SomniMessageConsumerNotificationType.CONSUMERCLOSED);
        TestNotificationListener listener = new TestNotificationListener(expected);

        Object handback = null;
        server.addNotificationListener(name,listener,null,handback);

        ...//Lots of code for the test

        listener.check();
```

**Where This Technique Will Work**

Using JMX for test-driven development will work very well in some cases, but doesn't fit all problems. If you want to support JMX MBeans and Notifications, using this technique is an easy right decision. If objects in your system have nontrivial lifecycles, it is a very good fit. If you aren't sure about the methods your system should support, but know more about the lifecycle of the objects, it should work well. SomnifugiJMS was a particularly good fit for JMX-based tests. I wanted to add JMX support. The Java Message Service specification defines a horde of parts used to ship message around. Each part has its own lifecycle. Plus I wanted to remove non-JMS public methods, and to use JMX to support more complex tests.

Some systems may have trouble using this technique. JMX has some overhead; if you are concerned about how much CPU and memory goes into creating and shuffling strings for logging, JMX may be too heavyweight. It's not a very good fit for data structure or algorithm code, where the public API is the main focus. Systems with no lifecycle won't get much benefit. JMX-based tests written for systems with extremely complex, changing lifecycle may be too brittle.

**References**

[Wikipedia](http://en.wikipedia.org/wiki/Test_driven_development) has a non-volatile description of test-first development. I found this when I was looking for something with minimal hype and political agenda. The [JMX reference](http://java.sun.com/j2se/1.5.0/docs/guide/jmx/index.html) from Sun contains examples of how to use JMX in your source code. The bias in the document is more toward monitoring existing systems -- it does a great job of telling how to hook up monitors via different protocols, but a skilled programmer see how to use stock JMX classes in an existing system via delegation. Eamonn McManus' [Eamonn McManus' blog](http://weblogs.java.net/blog/emcmanus/) is the best source for what's coming next in JMX.
