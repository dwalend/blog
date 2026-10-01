---
layout: post
title: Three Big Things LLM AI is Good For
description: "Mostly I like being a centaur. Generative AI types faster than I do, reads and writes in ways people 
might understand, and gives me access to some novice-level skills."
comments: True
tags:
  - post
  - AI
  - Claude Code
---

One of my kids has been proofreading these blog entries before I publish them. She commented, "You don't seem to like 
using the AI very much," after proofing a second entry about how to work around problems. It's the second of five or 
six I plan to write on the same theme. I've also shared a lot of disparaging anecdotes about AI in discussions on-line 
and in person. However, mostly I like being a centaur. Time for me to write something positive.

Generative AI helps me in three ways:

* It writes code much faster than I type.
* The LLM aspect allows it to read, infer abstract associations, and write in ways people understand.
* It provides novice-level skills for everything described on the internet.

## Generative AI Types Very Fast

I can type really fast.

In high school on an IBM Selectric mashing ink onto actual paper I won a typing race with a whopping 161 
words per minute - no mistakes. At hands-up, the buffer in the Selectric fed that staccato banging golf ball until 
everyone in the room was staring at it. I was never able to repeat that feat, but I could consistently clock about 
120 wpm by the end of the semester. Touch typing is pretty deep in my hippocampus; I'm not aware of typing beyond 
feeling when I have used a key that's not yet polished completely smooth. The Q has deeper texture than the well-worn P.

I'm a lot slower when I'm composing - maybe 30 wpm if my internal dialogue is confident. The effort of thinking eclipses
any work to get thoughts through the keyboard.

My code editor has excellent autocomplete that takes advantage of Scala's strong structures, but I don't use it as 
intended. It shows me a pop-up list where I can pick what I want from a menu. I think I can hit arrow keys and Tab to 
pick which option I want, but I usually switch over to an eyes-to-hands neuropathway and type the whole name. (I also 
tend to give the structures that are the best choice short names, and give the sad temporary compromises long 
names that are awful to type. "PolyphonicStewardesses" - but with some meaning.)

I first learned Scala while cradling a baby who had to be held all the time, typing with my free arm. I took the 
Odersky class while cradling my second child. (The early morning hours had me in class just after the bright-eyed TAs in 
Switzerland finished their morning coffee.) That slow typing speed was not an issue while studying FP in depth. A good 
Scala DSL library results in terse, powerful code and little boilerplate. I'll bet my Scala typing speed is something 
like 10 wpm.

Claude Code running Opus types [350-700 wpm](https://artificialanalysis.ai/models/claude-opus-4-8) - two orders of 
magnitude faster than I do. A token is about what it takes to read, ponder, or write 3/4ths of a word; Think about that 
while you watch the token meter tick up.

Investing in being an effective AI centaur pays an immediate dividend. We're looking at the 
[John Henry fable](https://www.youtube.com/watch?v=BZGxZbOB1Eo) repeating before our eyes. (I'm not going to type so 
fast that my heart explodes.)

I spend my time pondering, refining my directives for the AI, then reviewing its output 
([Don't Let the Back End of the Centaur Commit to Git]({{ '/2026/09/The-Top-Of-The-Centaur-Commits/' | url }})). I'll 
occasionally code an example for it to follow, but Claude produces the lion's share of the production code and tests. 
I've always spent time thinking about how a system should work, reviewing both my own work and my peers, and teaching 
our interns and new hires. My new activities are really writing down how the system needs to work instead of carrying 
it in my head as company oral tradition - this is good - and managing Claude's delicate 
context - two (someday six) [cranky blog articles]({{ '/' | url }}).

## An LLM Can Process Natural Language

I can write words that the AI interprets and acts on. It can write words that I can read. I'll give that "Processing 
Natural Language," but not "communicating like a person."

Sometimes it wildly misinterprets or simply ignores what I tell it. Sometimes I have to put in great effort to read 
what it says. I'm OK with that; it's still pretty amazing. Claude Code has achieved more than the "dancing bear" 
capability.<sup><a href="#dancing-bear">*</a></sup>

For example Claude does not use the word "only," and struggles to work around it with existentially dramatic phrasing:

> A script reports a finding by throwing a `BleepException`. bleep's `main` catches that and prints its message alone.

could be

> A script reports a problem by throwing a `BleepException`. bleep's `main` catches that exception but only prints the 
> exception's message.

without the angst.

I have a 475-line prose.md file of guidelines for how to write clear comments in code. That file grows by a line or two 
every day. I haven't figured out how to explain prepositions yet. The guidelines help, but they also might make things 
more strange.

When Claude is working it is having a deep conversation within its own context, but it is bad at understanding my 
context. It's sort of like a conversation with 4-year-olds who assume you know everything except the one 
huge fact they want to tell you.

> A person meets a broken fix on the first run because their own icon never appears.

Claude means to say: The only way a user whose GPS is never going to provide a location ("a broken fix") sees an error 
is that their own icon doesn't show up on the UI's animated map ("because their own icon never appears"). That took me 
a few readings.

However, if I ask Claude to rephrase something it stumbles on what seems like crushing self-doubt:

> **Claude:** The Gateway replacement argues for the sweep and against the tag. After the Gateway goes, completion is 
> waiting for the machine's address, recording that address wherever the replacement routes, and probing. EC2 already 
> reports the address on the instance. No tag records that address. RestApiIdTag is the one piece of completion state 
> a replacement deletes. That deletion is a second reason to keep the recovery path off the tag. The sweep's question 
> survives the replacement unchanged. That question asks whether this server is reachable.
>
> **Me:** It's really hard for me to read the strange language you used in this response. Show me an ascii table of the 
> steps and what each step depends on in your proposal.
>
> **Claude:** You are right. My argument against the step-watcher was wrong. I said a step-watcher needs a durable 
> record per step. A step-watcher does not. EC2 reports the machine's state and address, the Gateway reports the 
> resource, and a probe reports reachability. Every step's completion is already visible in the world.

(Claude did finally show me the table.)

It's really not ready to write words for unsympathetic readers, but I've had a lot of success with Claude Code reading my 
directives, creating code, and keeping documents that describe that code up-to-date.

Up-to-date docs are fantastic. Only twice in my career we actually had projects where documenting what we did was more 
important than finishing more quickly. For my current project Claude Code keeps the docs up to date. The docs 
effectively provide a replacement for the oral history I've had to carry in the past. They also make Claude Code work 
more efficiently and consistently. Having the LLM draft updates to the docs is a good investment on balance. It does 
make the work seem slower, but centaur carries most of the weight.

## An LLM Offers Novice-Level Skills In Many Topics

The big revolution with LLMs is that for $20 a month we can all get access to a host of novice-level professional 
skills.

I value the process of writing and revising to help clarify my thoughts, so I do not let Claude compose these blog 
entries. That would miss most of the value for me. It's not just that Claude Code's prose is alien. I trust my 
resident high-school grammar expert to edit them for correctness. Her classmates infamously use AI to write their 
papers - badly - but my kid disparages their efforts with or without AI help. They really are novices. With practice, 
they will get better. I'm not sure the AI ever will.

In contrast, Claude does the Markdown formatting for me. Markdown formatting is easy and I don't expect to gain much 
from learning how to do it. I hope it is someone else's passion. 

The AI does not understand what it does not know. Claude Code's chipper confidence belies 
its ignorance of the 
[Dunning-Kruger Effect](https://www.semanticscholar.org/paper/Unskilled-and-unaware-of-it%3A-how-difficulties-in-to-Kruger-Dunning/f2c80eef3585e0569e93ace0b9770cf76c8ebabc?p2df). 
For example, Claude's out-of-box ability to code is heavily weighted to Python. Claude is capable of writing Python in any language. 
Without guidance its Scala code will map directly to Python's dictionary and list structures with 
`Map[String,String]` and `List[String]` and hopeful string-matching. Instead of using strong types to prevent mistakes 
Code bypasses the type system completely. It's the realization of  
[Fog Creek Consulting Claims](https://www.joelonsoftware.com/2006/09/01/language-wars/) for $20 a month. I'll 
eventually post an argument that people started using LLMs to write code because they really needed a 
compiler to catch Python typos.

I've been able to write "My First iPhone App" in Swift over the summer. I'm writing Scala FP style in Swift. I'm not 
kidding myself; at some point I'll need to bring in an experienced Swift developer to bewilder, then have them ridicule 
my sophomoric efforts, and tell me what's actually important to fix. I'm getting pretty far without the help, but I 
don't know what I'm missing. I'll eventually need a teacher.

The real prize for us all is tapping skills completely over our horizon. For my current project that skill is called 
"marketing." Years ago I wrote some paragraphs for two SBIR grant proposals at Alphatech. At Harvard, I baked half-wheat 
bread for the team writing the Big Catalyst Grant Proposal that funds SHRINE. I've never even poked mass consumer 
marketing with a stick. I'm a complete novice with a complete novice's marketing plan. It at least makes me feel good 
stepping onto the Dunning-Kruger rollercoaster.

I think AI's effect on professional work will be a lot like the impact of 
[container shipping in the 1990s](https://www.youtube.com/watch?v=nC2pgcagyRk) on light manufacturing. At the beginning 
of the 1990s large-scale light manufacturing in the US collapsed. What local manufacturing survived is extremely 
specialized. On the other side of the world China changed from a political adversary to an economic rival. We have 
bespoke products at single-container Kickstarter-scale. You can argue good or bad, but it changed the whole economy. 

I don't know what that means for the professional class. Today I'm a centaur taking a marketing leap.

---

<p id="dancing-bear">* "The bear doesn't have to do a quick-step with Ginger Rogers. The remarkable thing is that the
bear dances at all." - I was able to trace the reference back to James Boswell's <em>Life of Johnson</em>, but the
original quote is unkind to a whole group of religious women. Samuel Johnson was not better than his peers in that
regard.</p>

**Reading:** I finished Cory Doctorow's [_Little Brother_](https://craphound.com/category/littlebrother/) ... about a decade late. He should feel like a prophet. He 
earned it.

**Listening:** I went with the Harry Belafonte version of "John Henry" instead of [Joe Bonamassa](https://www.youtube.com/watch?v=DRxawmG5MfM). 
It wasn't the folk-tale I needed for the citation, but that's made my afternoon.
