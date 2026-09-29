One of my kids has been proofreading these blog entries before I publish them. She commented, "You don't seem to like 
using the AI very much," after proofing the second entry about how to work around problems. It's the second of five or 
six I plan to write. Also, I've shared a lot of disparaging anecdotes about AI in discussions on-line and in person. 
Time for me to write something positive.

Generative AI helps in three ways:

* It generates text much faster than creating it by hand
* The LLM aspect allows it to read, infer abstract associations, and write in ways people understand
* It provides novice-level skills for everything described on the internet

Generative AI Types Really Fast
      
I can type really fast. In high school on an IBM Selectric typing onto paper I won a typing race with a whopping 161 
words-per-minute - no mistakes. At hands-up the buffer in the Selectric fed the staccato baning golf ball until 
everyone in the room was staring at me. I was never able to repeat that feat, but I could consistently clock about 
120 wpm by the end of the semester. Touch typing is pretty deep in my hippocampus; I'm not aware of typing beyond 
feeling when I have used a key that's not yet polished completely smooth. My Q has more texture than the well-worn P.
My code editor has excellent autocomplete that takes advantage of Scala's strong structures, but I don't use it as 
intended. It shows me a pop-up list where I can pick what I want from a menu. I think I can hit arrow keys and Tab to 
pick which option I want, but I usually switch over to a eyes-to-hands neuropathway and type the whole thing. (I also 
tend to name the structures that are the best choice with short names, and give the sad temporary compromises long 
names that are awful to type; "polyphonicStewardesses" - but with some meaning.) When I'm composing I'm a lot slower, 
maybe 30 wpm if my internal dialog is confident. The effort of thinking eclipses any work to get thoughts through the 
keyboard.

A good Scala DSL library results in terse code. I first learned Scala while cradling a baby who had to be held all the 
time, typing with my free arm. I took the Odersky class the same way with my second child. (The early morning hours 
had me in class just after the TAs finished their morning coffee in Switzerland.) That slow typing speed was not an 
issue while studying FP in depth. I'll bet my Scala typing speed is something like 5 wpm. 

Claude Code running Opus types 350-700 wpm - two orders of magnitude faster than I do. https://artificialanalysis.ai/models/claude-opus-4-8 . A token is about what it takes to read or write 3/4ths of a word [todo some arithmetic to get from tokens/second to WPM] . If I can get Claude Code Opus to type the right things consistently then it is no contest. 

Investing in being an effective centaur pays an immediate dividend. We're looking at the John Henry fable (TODO cite) repeating 
before our eyes (TODO cite history repeating).

I spend my time pondering, refining my directives for it, and reviewing its output. I'll occasionally code an example 
for it to follow, but Claude produces the lion's share of the production code and tests. I've always spent time 
thinking about how a system should work, reviewing both my own work and my peers, and teaching our interns and new 
hires. My new activities are really writing down how the system needs to work instead of carrying it in my head as 
company oral tradition - this is good (TODO cite local link) - and managing Claude's delicate context - five or six cranky blog articles (TODO cite). 


An LLM Can (Kind Of) Process Natural Language
                      
I can write words that the AI interprets and acts on. It can write words that I can read. 

Sometimes it wildly misinterprets or simply ignores what I tell it. Sometimes I have to put in great effort to read 
what it says. I'm OK with that; it's still pretty amazing. Claude Code has achieved more than the "dancing bear" 
capability. (TODO - move this to a footnote "The bear doesn't have to do a quick-step with Ginger Rogers. The 
remarkable thing is that the bear dances at all." - I was able to trace the reference back to James Boswell's _Life of 
Johnson_, but the orignal quote is unkind to a whole group of religious women. Samuel Johnson was not better than his 
peers in that regard.) 
                                              
For example Claude does not use the word "only," and struggles to work around it with existentially dramatic phrasing: 

> A script reports a finding by throwing a `BleepException`. bleep's `main` catches that and prints its message alone.  
                                                   
could be

> A script reports a problem by throwing a `BleepException`. bleep's `main` catches that exception but only prints the 
exception's message.
        
without the angst. 

I have a 475-line prose.md file of guidelines for how to write clear comments in code. That file grows by a line or two 
every day. The guidelines help, but they also might make things more strange. Claude is having a deep conversation with
itself but not providing context. It's sort of like a conversation with 4-year-olds who assume you know all but the 
one huge fact they want to tell you.

> A person meets a broken fix on the first run because their own icon never appears.

Claude means to say: The only way a user who's GPS is never going to provide a location ("a broken fix") sees an error 
is that their own icon doesn't show up on a map ("because their own icon never appears"). That took me a few readings. 

However, if I ask Claude to rephrase something it stumbles on crushing self-doubt: 

>  Claude: The Gateway replacement argues for the sweep and against the tag. After the Gateway goes, completion is 
waiting for the machine's address, recording that address wherever the replacement routes, and probing. EC2 already 
reports the address on the instance. No tag records 
that address. RestApiIdTag is the one     
piece of completion state a replacement deletes. That deletion is a second reason to keep the recovery path off the 
tag. The sweep's question survives the      
replacement unchanged. That question asks whether this duck line is reachable.

>  Me: It's really hard for me to read the strange language you used in this response. Show me an ascii table of the steps 
and what each step waits for in your proposal.

>  Claude: You are right. My argument against the step-watcher was wrong. I said a step-watcher needs a durable record 
per step. A step-watcher does not. EC2 reports the  
machine's state and address, the Gateway reports the resource, and a probe reports reachability. Every step's 
completion is already visible in the world.

(It did finally show me the table.)

It's really not ready to write words for unsympathetic readers, but I've had a lot of success with Claude Code reading my 
directives, creating code, and keeping documents that describe that code up-to-date. 

Up-to-date docs are fantastic. Twice in my career we actually had projects where documenting what we did was more 
important than finishing more quickly. For my current project Claude Code keeps the docs up to date. The docs 
effectively provide a replacement for the oral history I've had to extract in the past. They also make Claude Code work 
more efficiently and consistently. Having the LLM draft the docs is paying a dividend.


An LLM Offers Novice-Level Skills In Many Topics
                                      
The big revolution with LLMs is that for $20 a month I get access to a host of novice-level professional skills.

I value the process of writing and revising to help clarify my thoughts. I do not let Claude compose these blog 
entries. That would miss most of the value for me. I trust my high-school grammar expert to edit them for correctness. 
Claude's writing style is too alien to trust. 

In contrast, Claude does the Markdown formatting for me. Markdown formatting is easy and I don't expect to learn much 
from it. I hope it is someone else's passion.

Claude's out-of-box ability to code is very Python. Claude is capable of writing Python in any language. Everything is 
`Map[String,String]` and `List[String]` and hopeful string-matching. It's the Fog Creek Consulting advert for $20 a 
month. (cite) I'll eventually post an argument that people started using LLMs to write code because they really 
needed a compiler for Python. 

I've been able to write "my first Swift code," over the summer. I'm writing Scala FP style in Swift. I'm not kidding 
myself. At some point I'll need to bring in an experienced Swift developer 
to bewilder, then have them ridicule my efforts and tell me what's actually important to fix. I'm getting pretty far 
without the help but I don't know what I'm missing. I'll eventually need a teacher.

The real prize for me is tapping skills completely over my horizon. For the current project that skill is marketing. I 
wrote some paragraphs for two SBIR grant proposals at Alphatech. At Harvard I baked half-wheat bread for the team 
writing the big Catalyst Grant proposal that funded SHRINE. I've never done anything for mass consumer marketing. I'm a 
complete novice with a complete novice's marketing plan that at least makes me feel good.

I think the effect on professional work will be a lot like the effect of container shipping in the 1990s on 
manufacturing. At the beginning large-scale light manufacturing in the US collapsed the dominance of big-box 
near-commodity products. What manufacturing survived is extremely specialized. Here at the end we have single-container 
bespoke products at Kickstarter-scale. 

I don't know what that means for the professional class. Today I'm a centaur with a marketing leg.
