One of my kids has been proofreading these blog entries before I publish them. She commented, "You don't seem to like using the AI very much," after proofing the second entry about how to work around problems. It's the second of five I plan to write. Also, I've shared a lot of disparaging anecdotes about AI in friends-only discussions on-line and in person. Time for me to write something positive.

Generative AI helps in three ways:

* It generates text much faster than creating it by hand
* The LLM aspect allows it to read, infer abstract associations, and write in ways people understand
* It provides novice-level knowledge for everything described on the internet

Generative AI Types Really Fast
      
I can type really fast. In high school on an IBM Selectric typing onto paper I won a typing race with a whopping 161 words-per-minute, with no mistakes. At hands-up the buffer in the Selectric just kept going until everyone in the room was staring at me. I was never able to repeat that feat, but I could consistently clock about 120 wpm by the end of the semester. Touch typing is pretty deep in my hippocampus; I'm not aware of typing beyond feeling when I have used a key that's not yet polished completely smooth. (The Q has more texture left than the Comma.) My code editor has excellent autocomplete that takes advantage of Scala's strong structures, but I don't use it as intended. It shows me a pop-up list where I can pick what I want from a menu. I think I can hit arrow keys and Tab to pick which option I want, but I usually switch over to an eyes-to-hands mode and type the whole thing. (I also tend to name the structures that are the best choice with short names, and give the awful compromises long names that are awful to type: "polyphonicStewardesses" - but with some meaning.) When I'm composing I'm a lot slower, maybe 30 wpm if my internal dialog is confident, but the part about getting thoughts through the keyboard doesn't matter.

A good Scala DSL library results in terse code. I first learned Scala while cradling a baby that had to be held all the time, typing with my free hand. I took the Odersky class the same way with the second child. (The early morning hours had me in class while the TAs just after the TAs finished their morning coffee in Switzerland.) That slow typing speed was not an issue while studying FP in depth. I'll bet my coding speed is something like 5 wpm. 

Claude Code running Opus types 350-700 wpm - two orders of magnitude faster than I do. https://artificialanalysis.ai/models/claude-opus-4-8 . 

A token is about what it takes to read or write 3/4ths of a word [todo some arithmetic to get from tokens/second to WPM] . If I can get Claude Code Opus to type the right things consistently then it is no contest. Investing in being an effective centaur pays a dividend.

I spend my time pondering, refining my directives for it, and reviewing its output. I'll occasionally code an example for it to follow, but it produces the lion's share of the actual code. I've always spent time thinking about how a system should work,  reviewing both my own work and my peers, and teaching our interns an new hires. My new activities are really writing down how the system needs to work instead of carrying it in my head and as company oral tradition (this is good), and managing Claude's delicate context (leading to five blog entries about how annoying the new chore is). 


An LLM Can (Kind Of) Process Natural Language
                      
I can write words that the AI interprets and acts on. It can write words that I can read. Sometimes it wildly misinterprets 
or simply ignores what I tell it. Sometimes I have to put in great effort to read what it says. I'm OK with that; it's 
still pretty amazing. Claude Code has achieved more than the "dancing bear" capability. ("The bear doesn't have to do a 
quick-step with Ginger Rogers. The remarkable thing is that the bear dances at all." - I was able to trace the reference 
back to James Boswell's _Life of Johnson_, but the full quote is unkind to a whole group of religious women. Samuel Johnson 
was not better than his peers in that regard.) 
                                              
For example Claude does not use the word "only," and struggles to work around it with existentially dramatic phrasing: 

> A script reports a finding by throwing a `BleepException`. bleep's `main` catches that and prints its message alone.  
                                                   
could be

> A script reports a problem by throwing a `BleepException`. bleep's `main` catches that exception but only prints the 
exception's message.
        
without angst or apprehension. 

I have a 475-line prose.md file of guidelines for how to write clear comments in code. That file grows by a line or two 
every day. The guidelines help, but they also might make things more strange. Claude is having a deep conversation with
itself but not providing context. It's sort of like a conversation with a 4-year-old who can't imagine what you already 
know.

> A person meets a broken fix on the first run because their own icon never appears.

Claude means: The only way a user who's GPS is not working ("a broken fix") sees an error is that their own icon doesn't show up on a map. That took me a few readings. 

However, if I ask Claude to rephrase something it stumbles on self-doubt. 

>  Claude: The Gateway replacement argues for the sweep and against the tag. After the Gateway goes, completion is waiting for 
the machine's address, recording that       
address wherever the replacement routes, and probing. EC2 already reports the address on the instance. No tag records 
that address. RestApiIdTag is the one     
piece of completion state a replacement deletes. That deletion is a second reason to keep the recovery path off the 
tag. The sweep's question survives the      
replacement unchanged. That question asks whether this duck line is reachable.

>  Me: It's really hard for me to read the strange language you used in this response. Show me an ascii table of the steps 
and what each step waits for in your proposal.

>  Claude: You are right. My argument against the step-watcher was wrong. I said a step-watcher needs a durable record per step. A step-watcher does not. EC2 reports the  
machine's state and address, the Gateway reports the resource, and a probe reports reachability. Every step's completion is already visible in the world.
                          
But it did finally show me a table.

It's really not ready to write words for unsympathetic readers, but I've had a lot of success with Claude Code reading my 
directives, creating code, and keeping documents that describe that code up-to-date. Twice in my career we actually had
projects where documenting what we did was more important than finishing sooner. For my current project Claude Code 
keeps the docs up to date. The docs effectively provide a replacement for the oral history I've had to extract in the 
past. They also make Claude Code work more efficiently and consistently. It is paying off.

 



---

blog ideas - 

long, awkward class and method names for things I don't want people to use vs short, dense names for things I want everyone to 

writing as an aide to thinking 