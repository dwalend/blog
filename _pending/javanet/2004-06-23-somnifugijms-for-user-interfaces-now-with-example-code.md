---
layout: post
title: "SomnifugiJMS for User Interfaces, Now With Example Code"
date: 2004-06-23
permalink: /archive/2004/06/somnifugijms-for-user-interfaces-now-with-example-code/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2004/06/somnifugijms_fo_4.html
javanetTopics:
  - Extreme Programming
---

Somnifugi JMS is a lightweight, single-JVM implementation of the JMS interface. I've used Somnifugi to simplify the threading architecture on a few user interfaces for clients over the years. The architecture has worked well, especially for developers who weren't familiar with Java's multi-threading.

I've been meaning to follow up on an article by Johnathan Simon where he [hinted that one could use it to handle threads efficiently in a Swing interface.](http://today.java.net/pub/a/today/2003/10/24/swing.html) Last month, Brian Goetz wrote [an article about using parts of J2EE for non-enterprise systems.](http://www-106.ibm.com/developerworks/java/library/j-jtp04204.html) He mentioned that I provided example code for how to use Swing in the Somnifugi JMS download. He asked me to read through the article before publishing it, but the reference slipped through. After he published, the email requests for the example code started. After too many promises, I finally took advantage of a sit on an airplane to code up examples of Queues and Topics for separating work from the awt thread. I based the examples on Johnathan's original event listener example. Our coding styles are different enough that you can assume that any bugs are mine. Look in the [CVS repository"](http://cvs.sourceforge.net/viewcvs.py/somnifugi/somnifugi/v1/somnifugi/source/net/walend/somnifugi/example/) to see the full examples. Like most examples that scale up well, the code I'm presenting will seem a little awkward in the smallest, simplest case.

I found ways to apply two general metaphors for using JMS behind a GUI; a command queue and an event publisher. [Spin](http://spin.sourceforge.net/) may offer a third metaphor, more like request/reply. I haven't had time to investigate Spin yet. I hope to look into it on my way to JavaOne next week.

Command Queue Metaphor

A system can use a JMS Queue as a command queue for receiving threads. It works like this: A user causes the GUI to construct commands on the view thread. If the command will take a while to run, the GUI sends the command to the command Queue. Other threads receive commands from the Queue and carry out the user's wishes. The receiving threads make changes back to the GUI through calls to SwingUtilities.invokeLater().

Relevant code from CommandQueueExample.java:

```java
    private QueueSender sender;
...
//run on the view thread.
    protected void searchButtonActionPerformed()
    {
        try
        {
            //create a new command
            LookupRequest request = new LookupRequest(searchTF.getText());

            //and place it in the Queue
            Message message = session.createObjectMessage(request);
            sender.send(message);
        }
        catch(JMSException jmse)
        {
            handleThrowable(jmse);
        }
    }
```

The command queue metaphor is particularly valuable when the user expects things to change in a particular order; use just one receiving thread to preserve that order. If your users are more sophisticated and your GUI concept can explain what is happening, you can use more receiver threads to get more than one thing done at a time. Be careful with multiple worker threads; the Queue will preserve the order of start times, but not completion times. This metaphor is particularly easy to explain to developers just beginning to grok concurrent systems. The developers' cognitive leap for creating command instances to pass around is fairly simple. However, this metaphor can hit a scale limit in complex component systems. If the command receivers become a complex tangle, try using the event publisher metaphor.

Event Publisher Metaphor

The event publisher metaphor uses a Topic to publish events from the user interface to subscriber threads. It works like this: A user causes the GUI to construct events. The GUI publishes the events to a Topic. Various subscriber threads subscribe to this Topic. Each subscriber reacts to the event to carry out part of the work required. Again, the subscribing threads make changes to the GUI through calls to SwingUtilities.invokeLater().

Relevant code from EventTopicExample.java:

```java
    private TopicPublisher publisher;
...
    protected void searchButtonActionPerformed()
    {
        try
        {
            //create a new event
            LookupRequest request = new LookupRequest(searchTF.getText());

            //and place it in the Topic
            Message message = session.createObjectMessage(request);
            publisher.publish(message);
        }
        catch(JMSException jmse)
        {
            handleThrowable(jmse);
        }
    }
```

Each subscriber specializes in maintaining particular facets of the system. The resulting design keeps the facets separated. The event publisher metaphor is a great fit for complex user interfaces assembled by several small teams, and for user interfaces with rapidly changing requirements. All teams publish events about what's going on in their part of the system. Any team can create new subscribers to these events. The metaphor scales up remarkably, handles rapidly changing requirements very well, and encourages teams to create isolated unit tests. Beware that this looser coupling has a cost. Debugging involves tracking flow through Java code as well as watching events in the Topic. (Always have a subscriber that logs the events in your back pocket.) The cognitive leap for the developers is much greater; many senior architects have trouble with the Zen of Topics. Also, if your project needs to preserve the feel of commands executed in order, you will need to create one subscriber that treats events like commands (easy) and insure the other subscribers don't treat events like commands (more difficult).

No Escape From SwingUtilities.invokeLater(Runnable)

Java's GUI kit comes with its own EventQueue, which follows the command queue metaphor. We developers can only change what the user sees on the view Thread using the EventQueue. The only good way I found to do this was to use SwingUtilities.invokeLater(Runnable). I could have set up a separate MessageListener to act as a proxy for the EventQueue. However, spinning up an extra thread just to move events from one queue to another seems excessive. Plus someone still has to define Runnables somewhere. I wound up putting

```java
SwingUtilities.invokeLater(new Runnable()
            {
                public void run()
                {
//Change the view
                }
            });
```

in my code whenever I needed to change something in the UI. I expect most Swing programmers at least know to use SwingUtilities.invokeLater() for GUI changes ([Johnathan's experience differs](http://weblogs.java.net/pub/wlg/1277)), but it takes discipline. Public forums seem especially good at catching these mistakes.

Reading: *The Visual Display of Quantitative Information*, Tufte  

  
  

Hearing: *Daphnis and Chloe*, Ravel
