For $20 And a Lot of Trial-and-Error You Get Four Legs and An Extra Torso That Lets You Eat Grass

My main long-term interest is in open models (which are most likely to survive the coming bubble bursting). However, my employer picked Anthropic Claude Code for us last November (2025). Anthropic Claude charges $20 a month for what I'll call "a generous allowance of tokens" doled out five-hourly portions and weekly portions. A token is maybe about what it costs to process 3/4ths of a word or so. I have used a few million tokens since lunch. The token budget seems impenetrably complicated, but I usually have to take a break before I run short. I've decided to measure my use for now and figure it out later. That lets me use their proprietary large language models (LLMs) and the Claude interface.

LLMs predict what symbol comes next from what came symbol came before. If you're working with writing words or code those symbols are like words or parameters or idea fragments.

The LLM seems to be good at three things:

* It writes code a lot faster than I do, but not as carefully.
* It can interpret written and spoken word with about the same accuracy as a sixth grader
* It lets me use skills at about the level a novice can get after skimming the internet for a few days.

I pay my $20 to Anthropic every month, and am using all three capabilities. Claude types most of my code based on examples and guidelines I write in English, MarkDown, and Scala. I have Claude write documents that maintain the trace between the high level ideas and features I want and the code that makes them real, instead of just memorizing the connections. I've had Claude read and synthesize Web APIs in formats I don't know into tight Scala Tapir specifications, then convert them into my first Swift programs. Thus, I'm a centaur.


A Centaur's Uneven Pace

The problem I've had with using LLMs is that the pacing is different. I've spent decades as a developer honing how to reserve four-hour blocks of time to think and write code. I would concentrate on work, and let the rest of the world fade into the background. After about 4 hours of meditative work I would need to move around and talk, then do the other half-day of work before dinner. Using AI, and using Claude specifically, has changed the rhythm of my work at every scale.

The Dev Loop

At the finest scale I write a little code, then check that everything is fine. That's the core software developer activity.

From the time I started using languages with memory managers to when I started using LLMs in November 2025 my work writing software had an extremely regular pace. I look at results from the last step, think for a bit, write some test code, write some production, compile and test, and repeat. I prefer using a tool set that prevents me from making mistakes (test-first strongly-typed functional-oriented Scala); I put in a little extra thought up front and usually get things right the first time. The build system needs a very predictable 90 seconds to compile and run all the tests, so I can take small breaks without changing the cadence. I would weave the system at a very deliberate, predictable pace. The fewer interruptions the faster I completed tasks. It was meditative. Watching me work has to be the least cinematic experience ever; reclining suburbanite in cargo shorts and a tee shirt stops typing, stares menacingly at the wall for some moments, smiles, then his expression relaxes as he types again. After four hours he eats lunch, then does it again. Maybe the director will ask the lighting designer to do something interesting for the montage to close the scene with a good sunset.


An Interrupt every 20 seconds to 20 minutes

The pace of working with AI is less regular, and less centered on my simple loop. It's turn-based: I give Claude a directive paragraph in a prompt. Claude ingests my request, uploads supporting background information from my laptop to the server at Anthropic, does whatever blackbox processing it does there, downloads changes from Anthropic, and applies the changes to my source code files. Then it's my turn to review the changes, decide if more are needed, and figure out the next directive. It's like chess without a clock. Claude may take 30 seconds or 30 minutes; big, broad-stroke work predictably takes longer than something simple, but sometimes what seems like a simple ask will take a suprizingly long time.

I do other things while I wait: I have three copies of the source code so I can work on multiple unrelated tasks. I attend to the "non-musical" details of my job. If I'm building some personal project instead of work I'll sometimes switch over to household chores or irritating my teenagers. I also have this amazing laptop with an internet full of distractions. Then Claude needs my permission or guidance or some next task. Claude stops and waits. I'm reading about archeology practices from the 1900s, or putting together slow bread or blackberry crumble recipies, or discussing Pokemon taxonomy with some kid (again). Claude's prompt stays open, ignored.

That won't do at all. I figured out those settings in the TL/DR to get Claude to go "boink" when it needs my attention. That lets me work on separate coding tasks simultaneously, plus write or review a document full of directives for the AI. I spend most of my effort reviewing directives for the AI's context and correcting the AI's work. It is not like working with a peer or an intern. It's more like being GM for an on-line multiplayer text game where I'm driving the plot forward for separated groups of impatient but chipper players. I'm working in parallel. It's a lot of activity, a lot of context switches, and a lot of boinks. I get more done in less time in code, and in the kitchen.

However, it is not meditative. Sometimes I'll take the time to write some example Scala structures just the way I want, or just write text to get back to that relaxed, focused state. .... TODO close up here?





Out of Tokens? Wait (5 Hours - t)

I've structured my work life around getting large chunks of time uninterrupted - preferably whole days. When I've led teams my North Star for my team was to keep everyone productive doing some valuable task. Everyone would chat status when they started work; I'd leave them to it unless I saw they were stuck or weren't talking to each other when they needed to. My job as a manager was to keep other people from bugging them, protect the current tasks until the team finished them, and to figure out the next most valuable tasks to tackle.

Claude doesn't play nice with that goal. Anthropic allocates its token allowance in 5-hour blocks. Claude is in control of how many tokens it is burning through, but is not at all aware of them. Token use is mostly a black box. Token use increases geometrically ( O(n^2) ) as the session continues, so I have to /exit Claude periodically. It feels like incinerating the recorded guides in TODO. Sometimes Claude will go haywire and burn the whole allowance of tokens babbling to itself - most notably if it uses sub-agents or the celebrated Fable model. If Claude burns through my allowance in less than five hours then Claude stops abruptly. I can either pay extra, or wait. That abrupt stop breaks my concentration. Claude can't see the hard stop coming and has no awareness of the interrupt. Claude assures me that it doesn't have an API that can monitor the coming hard stop.

That five-hour pace is absolutely diabolical to manage in a humane schedule. I get up when my household starts, stumble to the kitchen and try to issue my first prompt around 7:30 am . If I run out of tokens late morning then I'll get an enforced lunch break. I'll start again and work through until late afternoon when I'm moving the kids around. If I'm pushing then after dinner I'll be able to issue some more prompts while resetting the kitchen. A break after five hours when I'm expected to do 8-9 hours of professional work is just a mismatch.

TODO The best way I've found to do it is to watch my account deep inside Anthropic's UI at https://claude.ai/new#settings/usage . maybe automate that.

My fix so far has been to reduce the number of tokens Claude goes through for my work by exiting and restarting Claude between tasks, and by integrating Claude with non-AI tools. That's its own several blog entries about `mcp`s and the MCP Protocol - saved for future days. I want to believe that the token side of the problem is the important side, that tokens are real, measurable things that Anthropic meters out. However, I feel like I'm trying to fix the wrong end of the centaur.

Saturday Night Reset

Anthropic also sets a weekly token allowance. I haven't dug very deep but I know it is not 168/5 ~ 30x the five-hour allowance. My guess is it's about 12x the five-hour limit.

Tokens might be a real, metered thing. However, the token allowance is what Anthropic says it is. I get a generous portion for $20. That's the deal. With my improved tools I've gotten through the day and week just fine. Before I invested time in better tools I needed just over twice that to do a solid week's work. That's the deal. $40 a month to double the limit is not the deal, but $100 for five times the limit can be. Or I can pay a premium rate for "Usage Credits" which were about 5X the price of the subscriptions when I tried it. ($100 for June would have been more cost effective.) For most of the summer Anthropic has given me "Your weekly Claude Code limit is 50% higher through August 19 ... When each promotion ends, limits return to your plan's standard amounts." and "$100 Promotional creditExpires September 19, 2026" (from https://claude.ai/new#settings/usage ). I think Anthropic is easing me into paying that "Usage Credit" price.

That weekly reset has been trouble for an employer as well. Our team initially had both the five-our allowance and the weekly allowance before we moved to an enterprise-level deal. Ultimately the problem was the same for most commercial software tools, though. The problem with buying software or on-line services is not the price tag. The problem is the invoice. Getting a company to pay an invoice is a giant obstacle; generally developer teams do without the service until an open source version even if the commercial price is tiny.

Real financial analysts look at AI company's books and point out that they are operating with an unsustainable loss-leader. Ultimately I think Corey Doctorow is correct; after the AI bust open models will survive. TODO.

Reading: Cory Doctorow's _Little Brother_ . Fun start. Great pace.
Listening: The Mistholme Museum of Mystery . 