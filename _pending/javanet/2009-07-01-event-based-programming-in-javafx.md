---
layout: post
title: "Event Based Programming in JavaFX"
date: 2009-07-01
permalink: /archive/2009/07/event-based-programming-in-javafx/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2009/07/event_based_pro.html
---

**Old Song, New World**

I decided to try my hand at some JavaFX programming to see what the language had to offer. Two of the key features of JavaFX are its ability to bind to data, and its access to all Java libraries. I used that to see how it handles for event-based programming. I built this minesweeper game:

*[JavaFX applet, no longer runnable]*

*[JavaFX applet, no longer runnable]*

**As the World Turns: Reactive Data Models**

JavaFX let me build reactive data models using `bind` and `on replace`. When some piece of state changes, the change propagates through based on code right of the declarations. These keywords shrink the boilerplate down to a few readable characters. Here's a piece of code from TileControl.fx that uses both:

```
package class TileControl {
...
    var tileNode : TileNode; //View of the tile
    public-init var cell: HexBoards.ClientCell; //Model of the tile

    def cellState = bind cell.state on replace oldCellState {
            if(tileNode != null) {
                tileNode.update(cellState);
            }
        };
...}
```

I'm not completely convinced that TileControl -- and MVC-- is worth the extra class. I could have bound cell.state directly to a field in tileNode. It does prevent these few important lines from being lost in a sea of graphics code, and keeps the model from leaking into the verbose TileNode graphics code. More importantly, it lets a model of several layers, say rules for a more complex board game or some obscure business logic, propagate based on their declarations. An outer layer can define its own dependencies on the inner layer, so the system stays very clean.

**Old World Meets New: Event-based Programming and Clean Code**

I like event-based programming. It tends to keep class structures shallow and clean, and separates a program into understandable parts. When I throw in a way to distribute the events I can get multiple machines to form a coherent system, usually fairly painlessly. That minesweeper game shows the idea in JavaFX on a small scale. I used JMS to separate a Server, which knows where all the mines are, from a Client, which only knows what the player has uncovered. The client and server have no direct access to each other's objects; they are loosely coupled via JMS events. It's overkill for this little project, with one player, no reward (not even bragging rights) in the game, and client and server collocated in a single process. However, it'd make creating a distributed multiplayer game, or any other distributed system very easy. (To save me having to work with network connections on your web page, I've used SomnifugiJMS and colocated the Server and Client in the applet. It needs your permission to read system properties and to use JMX.)

I set up some simple wrapper classes to handle the JMS calls. Nothing to write home about, but it does bundle up the boiler plate neatly. JavaFX doesn't do much with exception handling. I haven't spotted where uncaught exceptions go yet. (Maybe another blog there...) In any case, here's one of the four helper classes:

```
package class Publisher {
    def connection = SomniJNDIBypass.IT.getTopicConnectionFactory().createTopicConnection();
    def session = connection.createTopicSession(false,Session.AUTO_ACKNOWLEDGE);
    public-init var topicName : String;

    var publisher : TopicPublisher;

    init {
        def topic = SomniJNDIBypass.IT.getTopic(topicName);
        publisher = session.createPublisher(topic);
        connection.start();
        }

    package function publishObject(object : Serializable) {
        var message = session.createObjectMessage();
        message.setObject(object);
        publisher.publish(message);
    }

    package function close() {
        publisher.close();
        session.close();
        connection.close();
    }
}
```

**Earth To Mars**

Once I'd typed the boilerplate, publishing events when something changed was easy with `on replace`. Here's what happens in the server after a client finds a safe cell:

```
package class Game {
...
var safeTestedAddresses = [] on replace oldValue {
        def address = safeTestedAddresses[sizeof safeTestedAddresses - 1] as Address2D;
        def cell : HexBoards.ServerSafeCell = board.getCell(address) as HexBoards.ServerSafeCell;

        def event = Events.SafeCellTestedEvent {
                        address: address;
                        mineNeighborCount: cell.minesTouched;
                        }
            publisher.publishObject(event);
    };
...
}
```

**Receiving Events... "Oh, Crap... Alien Thread"**

Inbound messages seemed like they'd be just as easy. They kind of worked in JavaFX 1.1, although I saw some screen twitching that reminded me of trying to run Swing-based code on the wrong thread. JavaFX 1.2 seems to spike the whole works and just did nothing -- no error message, just not responsive. I asked Josh for some help, and he sent this reply:

&gt; All JavaFX stuff happens on the GUI thread by default. The exceptions are APIs which do threading for you, such as loading an image in the background. If you create your own (Java) Thread then you are on your own. We won't stop you but if you touch some JavaFX structures some weird things may happen. If you need to do some non GUI work in a different thread (talk to the network, compute some calculation, etc.) then you should do it in Java and use a callback to get back into the JavaFX side. You can either use the usual Swing way, SwingUtilities.invokeLater(), or use the new FX.deferLater function.  Since we have function references in JavaFX this sort of callback works quite well.

Just before I got that response, I found this [ two-year-old email from Tom Ball](https://openjfx-compiler.dev.java.net/servlets/ReadMsg?list=issues&msgNo=4):

&gt; Part 2 is to come up with a replacement for "do later".  The canonical use case 
&gt; for "do later" is "oh, crap, I got called back in some other thread that isn't 
&gt; the EDT, get me to the EDT!"  This comes about because you may implement an 
&gt; interface that represents a callback, and the callback happens in the wrong 
&gt; thread.  In that case, the body of "do later" should really be the whole 
&gt; method, since you don't want to be touching any data from the alien thread.

**Aliens Among Us**

I normally prefer receive()s in my own threads to MessageListeners, but I didn't see a good way to use receive() or even receiveNoWait() without either polling or locking down the graphics thread with a blocking call. Using FX.deferAction() inside a MessageListener was pretty easy, and everything flowed from there:

```
package class TestMessageListener extends MessageListener {

    var board : HexBoards.ClientMineBoard;
//On a JMS Thread. Oh crap.
    override function onMessage(message : Message) {
//Get back to the GUI thread before something bad happens.
        FX.deferAction(function() {
            def event : Events.CellTestedEvent = (message as ObjectMessage).getObject() as Events.CellTestedEvent;

            board.processEvent(event);
        });
    }
}
```

**The World Is Not Enough**

JavaFX is already doing some event-based programming in the background, single-threaded, on the graphics thread, using its single queue. The reactive data model is great, so long as it can live on the graphics thread along with everything else, without bogging things down. But bogging down the graphics thread was always one of the risks in AWT and Swing. JavaFX doesn't save us from that. Simon Morris posted [an approach for building very clean parsers in JavaFX](http://weblogs.java.net/blog/javakiddy/archive/2009/05/thinking_declar.html). If the program is only about parsing, that should work well. However, if you need the graphics thread for graphics, your JavaFX program might sputter or jam during the parse, or any other big computation or big i/o operation.

**World on a Thread**

Osvaldo Pinali posted a [blog with a postscript](http://weblogs.java.net/blog/opinali/archive/2009/06/javafx_script_a.html) about the power of automatic propagation through bind. Fabrizio Giudici's [concerns about encapsulation](http://weblogs.java.net/blog/fabriziogiudici/archive/2009/06/javafx_binding.html) I think are misplaced.* The great thing about bind is that when you create your objects' code, you don't have to predict how those objects will be used and build the corresponding boilerplate. Someone later uses bind when they want an update, binding to the fields they care about. It's getting back to OO's forgotten roots in message-passing, and taking a step beyond. Instead of being limited to API provided by a developer, you ask an object to send a message when something you care about changes.

Osvaldo talks about his days in constraint programming. Propagation in constraint programming was tricky to get right. Mixing concurrency and propagation is even tricker. JavaFX solves this problem by only propagating changes on the graphics thread, alongside all the other graphics work. It can't take advantage of multiple threads and multiple cores; it can't dedicate one core to keep graphics responsive and use the rest for computation and i/o.

The tail end of Tom Ball's email lays out a long term goal:

&gt; Part 3 (to be deferred for a while) involves creating a functional subset of FX 
&gt; that can be safely invoked in threads other than the EDT. I hold out some hope 
&gt; that the "valueof" operator discussed this week (in the context of holding some 
&gt; variables constant in bind expressions) would provide the key: that an "async 
&gt; closure" would be a closure which could not have the side effect of reading or 
&gt; writing FX attributes. Instead, at the time the closure was created, the 
&gt; appropriate values would have to be copied with "valueof", so that the closure 
&gt; was operating on local copies.  The goal is to create FX code that can't touch 
&gt; arbitrary application state, but instead copies what it needs.

Josh says, 

&gt; We have basically done parts 1 and 2 of Tom's plan. ...  Part 3, a threadsafe functional subset of the language hasn't been done yet." Tom's description of where they're going implies that the graphics thread is going to control all the data and hand copies off to other threads via some programming construct. It'd be better, but will still be limited by flows in and out of a single thread.

* Fabrizio has a solid practical point, though. His example shows that some part of control flow and mutability is out of kilter. I'll keep my binds on defs, one-way only, for now.

**World of Tomorrow**

Osvaldo Pinali's blog's main point was to open a discussion about what we need next in JavaFX. I think the ability to use JavaFX for big jobs beyond user interface work should be high on the list. `FX.deferAction()` is already using the graphics event queue; one queue already exists. One easy way to gain some concurrency is with events flowing into multiple queues from wherever, processed by a thread dedicated to each queue. The complexity comes in when figuring out which objects live on which queues. JavaFX right now makes an easy choice; there's only one queue for one world of data structures. The other extreme, one thread per object, is too resource-heavy to sustain. I'd like the power to segregate my objects into groups that I define. For example, I'd like to put the user interface of a game on one thread, the game's logic on a second thread, and large computes and i/o operations on other threads. That would give JavaFX unique power in two domains: user interfaces and scalable propagation.
