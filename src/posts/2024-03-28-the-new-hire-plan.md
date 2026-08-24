---
layout: post
title: The New Hire Plan
description: "In the first two days of a new job I get the code building and one small change checked in. When I lead, I plan the first weeks and months the same way."
comments: True
tags:
  - post
aliases:
  - /the-new-hire-plan/
---

In the first two days of a new job I like to get the code checked out, building in my environment, then get some small change tested, and checked in where others can see it. Exercising that simple development loop sets the tone for the first weeks, and reassures everyone that I'll be able to contribute. When I am in a lead position - bringing new interns or employees on projects I run - I take things a step further. Beyond that first code change I find small projects that show important concepts for the first weeks, and a larger project with significant impact for the first few months. I often have that first project in mind while I am interviewing.

My boss' direction for our first intern at HMS was, "Just drop him into the project and treat him like any other software engineer on the team." We hadn't had any developers join the team since I had been hired two years prior, so I took it as a license to pull from my experience, especially as tech lead for a growing team at BAE. I came up with some steps that matched what I would want for myself, and steps that I thought would get that engineer up to speed quickly. We used the process successfully with four interns and one new employee at HMS Catalyst.

I had led something similar for a dozen new hires at BAE. There we had the new hires give a presentation to the whole team in the first few weeks to introduce themselves and show how their experience would help us. We had an ulterior motive; we were doing defense research and could never predict who might be read into which compartment and suddenly be called on to present to a customer. (Misadventures followed, but it all worked out.) At HMS the interns gave a presentation on what they had done at the end of their term.

MathWorks had a very well-thought-out monthly orientation class for all new employees about how the company worked. (MathWorks put thought into everything.) It was really good, but at a more grand scale than I would expect anywhere else ... ever. When I listed what I wanted to do in my first few days at MathWorks my boss there replied with something like, "Yes, that's what we want you to do. Sign up for the orientation class." MathWorks was already doing what I thought was a good idea.

I think these steps would work well anywhere, when combined with the 20-minute rule (... a future blog entry):

Day 1 - Get a computer working with internal systems, check out the code, get it to build, start on an easy ticket.

Day 2 - Finish the fix for that easy ticket, check it in, ask for a review.

Day 3 - Merge that change into a git branch headed for a release.

Weeks 1 & 2 - Get a grand tour of key libraries and concepts central to our product by fixing more interesting tickets.

Week 3 and onward - Take on some major, unifying project that works across teams and has a deep impact to learn to work "like any other software engineer on the team."

Some time in the first four months - Present something relevant to the team.

To follow that plan I had to set the stage for the new hires before they started. I was able to delegate getting set up as a Harvard employee and getting a laptop going; I'm grateful others could help navigate the bureaucracy. The software tasks were easy to find. I had inherited a Jira system with hundreds of open tickets to sieve. We were moving SHRINE through a major architectural transformation from a promising prototype to a resilient system. I had to balance difficulty of a change, value of that change, and the risk that a new hire would get lost and need more help than the team could provide. The interns needed good stories to tell for job interviews, which eliminated some of the more arduous SHRINE-specific tasks and wholesale deleting of dead code. The limit came from abundance of work and my own limited time to coach.

Unit tests and cosmetic changes provided early, easy tickets. This also made completing these "fold the laundry" sorts of tasks more valuable than using them as fill at the end of sprints.

The Jira backlog provided tasks for the tour of key libraries and concepts. SHRINE uses http4s for its web API, cats effects for concurrency, CQRS via slick for database work (Our first intern could not contain his delight about writing monadic database code on day three.), AWS SQS for messaging, circe for json, i2b2 as a source of patient data, and Scala's xml library to read and write i2b2's xml. I found a ticket in each of these categories to fix some minor bug or make some minor improvement. I could usually line the tasks up in an order that built one skill on another.

New features provided that important project. I gave interns major responsibility; that freed me to lead the project, manage day-to-day tasks, and deal with the crisis of the moment. The projects included things like "simplify the query sign/verify code" and "create and fill in the API we will use for message-oriented middleware." The one employee who started under my watch had more than a decade of experience at HMS Catalyst, so I asked her to "pick a web API library to replace Jakarta and Spray, then rework the web API endpoints to use that library," a very broad project. She was a bit taken aback by that, but she gained expertise, then shared it. It couldn't have worked better.

Some parts of our work were simply not good tasks for new hires. Some of the vital parts of SHRINE - especially communicating with i2b2 - required years to accumulate all the unstated caveats. Refactoring tangled code or deleting obsolete subsystems would just frustrate a new developer without helping them learn the system. It's more efficient to have an old hand (me) clean up the mess and refactor it to something easier to understand. The new hires can help review the change to get that understanding of the improved code.

Overall this new hire process worked so well I decided to use it as my first blog entry for the 2024 blogging restart. Next time I start a new job or hire someone new I hope to follow it and learn a little more about how to start a job right.
