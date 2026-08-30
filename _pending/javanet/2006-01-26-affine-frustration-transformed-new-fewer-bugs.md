---
layout: post
title: "Affine Frustration Transformed - New! Fewer Bugs!"
date: 2006-01-26
permalink: /archive/2006/01/affine-frustration-transformed-new-fewer-bugs/
archived: true
originalUrl: http://weblogs.java.net/blog/dwalend/archive/2006/01/affine_frustrat_1.html
---

I put together a generic ZoomPane that holds other Swing components. Hand ZomePane's `transformChanged()` method
 a new AffineTransform to show a new portion of the underlying view. ZoomPane uses a little linear animation to glide into the new view gracefully.

I set up ZoomButtonPane as a simple interface. (I want to play with something more complex and transparent. It's been a while since I've worked with Swing, so I wanted to warm up with some easy buttons.) ZoomButtonPane hands off AffineTransforms to a ZoomPane.

Panning worked great. Zooming in and out was a pain to get right. I found similar old questions in some forums, with no answers. I asked for help in other forums, and got a few responses that pointed to example code. Unfortunately, none of the examples solved the whole problem; in each case, some controller held on to some of the state information used by ZoomPane. I figured out how to get those details from just the old transform and size of the window. 

```java
private void zoom(double newScale)
    {
        AffineTransform oldDestinationTransform = zoomPane.getCopyOfDestionationTransform();

//Unwind the centering from the old transform.
        double centerX = zoomPane.getWidth()/2;
        double centerY = zoomPane.getHeight()/2;

        double oldScale = oldDestinationTransform.getScaleX();

        oldDestinationTransform.translate(centerX,centerY);
        oldDestinationTransform.scale(1.0/oldScale,1.0/oldScale);
        oldDestinationTransform.translate(-centerX,-centerY);

        oldDestinationTransform.translate((oldDestinationTransform.getTranslateX()/oldScale)
                                            -oldDestinationTransform.getTranslateX(),
                                            (oldDestinationTransform.getTranslateY()/oldScale)
                                            -oldDestinationTransform.getTranslateY());

        AffineTransform newDestinationTransform = new AffineTransform();

        newDestinationTransform.translate(centerX,centerY);
        newDestinationTransform.scale(newScale,newScale);
        newDestinationTransform.translate(-centerX,-centerY);

        newDestinationTransform.concatenate(oldDestinationTransform);

        zoomPane.transformChanged(newDestinationTransform);
    }
```

Here's an applet showing it working:

*[Java applet, no longer runnable]*

Kick the code around yourself at [https://tokenarranger.dev.java.net](https://tokenarranger.dev.java.net).
