---
layout: post
title: "Connecting to a Command Line Process"
date: 2005-08-24
permalink: /archive/2005/08/connecting-to-a-command-line-process/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2005/08/connecting_to_a.html
---

Connecting to a Command Line Process

[AdamTaglet](https://adamtaglet.dev.java.net/) alpha-0-1 is out! It's really rough; .gifs and .jpegs use the default font, instructions are sparse, and only links to classes in the same package work. But it meets the first release criterion. It does something useful.

Part of this project was adding a tographviz package to [JDigraph](https://jdigraph.dev.java.net/) to encapsulate interaction with the dot language and  the Graphviz command line. I built some fairly elaborate code to wrap around the Graphviz command line. I created the [GraphvizControl.java](https://jdigraph.dev.java.net/source/browse/jdigraph/v2/source/tographviz/net/walend/tographviz/GraphvizControl.java?rev=1.3&view=auto&content-type=text/vnd.viewcvs-markup) class to bundle it all up. It makes for a nice blog article.

I discovered early on that the operating system offered me a fairly short time to read in stderr and stdout. Sometimes I would get all of the output from dot, sometimes just pieces of an error message, or part of the drawing. I solved this problem by creating the StreamPull inner class:

```java
/**
Reads an InputStream until the stream reaches its end.
The contents of the stream are available in getResult().
Any exceptions encountered are in getTrouble().
*/
    private static class StreamPull
        implements Runnable
        {
            private InputStream is;
            private final Object guard = new Object();
            private String result = null;
            private IOException trouble = null;

            StreamPull(InputStream is)
            {
                this.is = is;
            }

            public void run()
            {
                try
                {
                    StringBuilder stringBuilder = new StringBuilder();

                    InputStreamReader streamReader = new InputStreamReader(is);

                    int i;
                    while((i = is.read()) != -1)
                    {
                        char c = (char)i;
                        stringBuilder.append(c);
                    }
                    synchronized(guard)
                    {
                        result = stringBuilder.toString();
                    }
                }
                catch(IOException ioe)
                {
                    synchronized(guard)
                    {
                        trouble = ioe;
                    }
                }
                finally
                {
                    try
                    {
                        is.close();
                    }
                    catch(IOException ioe)
                    {
                        synchronized(guard)
                        {
                            if(trouble==null)
                            {
                                trouble = ioe;
                            }
                        }
                    }
                }
            }

            String getResult()
            {
                synchronized(guard)
                {
                    return result;
                }
            }

            IOException getTrouble()
            {
                synchronized(guard)
                {
                    return trouble;
                }
            }
        }
```

Is there a better way to read an InputStream to its end? `while((i = is.read()) != -1)` looks like 1985. Shouldn't we have left that behind with the piano keyboard tie?

The other ugly part is that massive finally{} block. Four }s reminds me of lisp, but at least the error code is not mixed in to the rest.

The makePicture() method ties together the Process, the InputStreams, StreamPulls, Threads, and an OutputStream. It gets the process out of a ProcessBuilder, grabs the stdout and stderr streams from the process, feeds them to StreamPulls, starts Threads for the StreamPulls, and then writes the instructions to the process. After that, it waits for the process to complete, then joins the two StreamPulls. I didn't use buffers on the streams; the code seems to get by without them just fine. (Your profiler may say something different. Let me know if it does.) I wish Process had a waitFor() method with a time out so that I could add some warning against infinite loops short of calling process.destroy(). However, dot is a pretty solid program with some years of use behind it.

```java
public String makePicture(String dotString,String process,String format)
        throws GraphvizControlException
    {
        try
        {
            Process dotProcess = new ProcessBuilder(process, "-T"+format).start();

            InputStream fromDotStream = dotProcess.getInputStream();
            InputStream errorDotStream = dotProcess.getErrorStream();

            StreamPull errorDotPull = new StreamPull(errorDotStream);
            StreamPull fromDotPull = new StreamPull(fromDotStream);

            Thread errorThread = new Thread(errorDotPull);
            Thread fromThread = new Thread(fromDotPull);

            errorThread.start();
            fromThread.start();

            //write to standard out for the process
            OutputStream toDotStream = dotProcess.getOutputStream();
            PrintWriter printWriter = new PrintWriter(new OutputStreamWriter(toDotStream));

            printWriter.write(dotString);
            printWriter.close();

            dotProcess.waitFor();

            errorThread.join(1000);
            fromThread.join(1000);

```

And then there's this massive block of error handling code that opens with a colossal if statement. It translates to "if anything went wrong, build up an error message and throw an Exception." After that code there's one line that returns dot's output as a String, and a little more exception handling.

```java
if(errorDotPull.getTrouble()!=null
                || ((errorDotPull.getResult()!=null)&&(!errorDotPull.getResult().equals("")))
                || fromDotPull.getTrouble()!=null
                || fromDotPull.getResult()==null)
            {
                StringBuffer buffer = new StringBuffer();
                IOException cause = null;
                if((errorDotPull.getResult()!=null)&&(!errorDotPull.getResult().equals("")))
                {
                    buffer.append(errorDotPull.getResult());
                }
                if(fromDotPull.getResult()==null)
                {
                    buffer.append("result from process is null");
                }
                if(fromDotPull.getTrouble()!=null)
                {
                    buffer.append("IOException on external process' output stream.");
                    cause = fromDotPull.getTrouble();
                }
                if(errorDotPull.getTrouble()!=null)
                {
                    buffer.append("IOException on external process' error stream.");
                    cause = errorDotPull.getTrouble();
                }
                if(cause == null)
                {
                    throw new GraphvizControlException(buffer.toString());
                }
                else
                {
                    throw new GraphvizControlException(buffer.toString(),cause);
                }
            }

            return fromDotPull.getResult();
        }
        catch(IOException ioe)
        {
            throw new GraphvizControlException(ioe);
        }
        catch(InterruptedException ie)
        {
            throw new GraphvizControlException(ie);
        }
    }
```

I'm mostly happy with the way this class came out, but the whole works has the feel of something that should have just been there. I normally like the library Sun provides in Java, but I felt like I was working far from the context of my problem while bringing this class together. Building the code felt a little strange, like I was assembling a box of many small parts that should have come in larger, pre-assembled chunks. Creating Swing code often feels the same way to me, but the io package always feels fine. I think it's familiarity vs. complexity.
