# A Centaur's Gait

Using an LLM has changed the rhythm of how I work on a minute-by-minute scale. It bothered me at first, but I've figured out some things. In the spirit of ((((Do something!) small) useful) Now!) from ascii inventor Bob Bemer:

# TL/DR

Get Anthropic Claude Code to play a alert tone when it needs your attention by adding this to your "hooks" section to your `~/.claude/settings.json` . Changing over to AI-assisted coding means I work faster, but also at a much less regular pace. Having Claude play a tone when it needs my attention helps. [TODO add a link here to Boink!]




Those Hoofbeats You Hear are Centaurs

The "centaur analogy" is one of the more positive images for working with AI. AI makes you like a centaur; you're faster and stronger but still have all the abilities you have now. If something turned you into a centaur it would replace your human legs with a horse's four legs (and ... um ... whole extra torso) so that you can gallop and leap over streams and fences instead of just boring old walking. AI supplements your ability to do whatever AI can help with, but you're still the human-on-top, and are still in charge. This analogy comes from Garry Kasparov. Back in 1997 Deep Blue beat Kasparov in a fair chess match. In 1998 Garry Kasparov bounced back and invented a new game - Centaur Chess - where chess masters partnered with machines to play chess at a new level of dazzling skill. AI advocates and satarists have extended that analogy to the new generation of LLMs. 

( Murray Campbell, one of Deep Blue's engineers later pointed out that the illogical sacrifice Deep Blue used to beat Kasparov the year before to inspire Centaur Chess was "neither human interference nor artificial ingenuity. It was just a glitch." The six-limbed centaur was begat by a bug! https://www.sciencehistory.org/stories/magazine/thinking-machines-the-search-for-artificial-intelligence/ ) 

I've spent about 10 months now trying out my centaur legs. Work bought us a license for Anthropic's Claude Code, and I've purchased their $20/mo plan for my hobby work. It's time I write up what I've learned.


A Centaur's Uneven Pace

The problem I've had with using LLMs is that the pacing is very different and very uneven compared with my last thirty years of professional work. Working with LLMs impacts the pace at the 3-second time-scale all the way to planning my weeks. This blog is mostly about that fine-scale. I'll talk about the longer loops in future blogs.
  
My Pedestrian Dev Loop
            
At the finest scale I write a little code, then check that everything is fine. That's the core software developer activity. The finest scale loop is me typing while my code editor checks what I just typed for obvious mistakes. This works at about the same speed as my visual focus, about 1-3 seconds. The second-finest is when I've made some small change complete enough to compile, assemble into a working system, and test. Depending on the project that takes between ten seconds (for a small, isolated project where I've optimized the build) to five minutes (for a big, warty legacy project that depends on automated tests). I look at results from the previous step, think for a bit, write some test code, write some production code, compile and test, repeat until the next meeting. Watching me work has to be the least cinematic experience ever: reclining suburbanite in cargo shorts and a tee shirt stops typing, stares menacingly out the window for some moments, smiles, then his expression relaxes as he types again. After four hours he eats lunch, then does more of the same. Maybe the director will ask the lighting designer to do something interesting for the montage to close the scene with a good sunset. I like that it is meditative. 

Walk-Trot-Walk-Gallop-Walk-Jump-Walk

The pace of working with Claude Code is less even, and less centered on my simple loop. Claude Code and I editing the same files at the same time results in us paving over each other's changes, so using Claude Code is turn-based: I give Claude a directive paragraph in a prompt. Claude ingests my request, uploads supporting background information from my laptop to the server at Anthropic, does whatever blackbox processing it does there, downloads changes from Anthropic, and applies the changes to my source code files. Then it's my turn to review the changes, decide if more are needed, and figure out the next directive. The rhythm is like chess without a clock. Claude may take 10 seconds or 40 minutes. Big, broad-stroke work predictably takes longer than something simple. (Claude Code tends not to ask for clarification; it'll just guess and keep going.) However, sometimes what seems like a simple ask will take a suprizingly long time. 

I do other things while I wait: I have three copies of the source code so I can work on multiple unrelated tasks. I attend to the "non-software" details of my job. If I'm building some personal project instead of work I'll sometimes switch over to household chores or irritating my teenagers. I also have this amazing laptop with an internet full of distractions. Then Claude needs my permission or guidance or review. Claude stops and waits. I'm reading about destructive archeology practices from the 1900s, or putting together slow bread or blackberry crumble recipes, or discussing Pokemon taxonomy with some kid. Claude's prompt stays open, ignored, forgotten.

Boink!

That won't do at all. I figured out these settings to get Claude to go "boink" when it needs my attention. 

```json
{
  ...
  "hooks": {
    ...
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "afplay /System/Library/Sounds/Glass.aiff &"
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "afplay /System/Library/Sounds/Funk.aiff &"
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "afplay /System/Library/Sounds/Sosumi.aiff &"
          }
        ]
      }
    ],
    "StopFailure": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "afplay /System/Library/Sounds/Basso.aiff &"
          }
        ]
      }
    ]
  },
  ...
}
```      
If you're on a Mac these afplay commands should work. Other platforms have other options for playing sounds or flashing the screen. Some of those options - like printing the ascii bell character - are likely disabled, possibly at several levels. (Try and get Claude to play an ascii bell tone if you're mad at it.) Cut-and-paste this into a Claude Code prompt, and it will gleefully do the work for you.

That lets me work on separate coding tasks simultaneously, plus write or review a document full of directives for the AI for next turn. It is not like working with a peer or an intern. It's more like being GM for an on-line multiplayer text game where I'm driving the plot forward for separated groups of impatient but chipper players. I'm working in parallel. It's a lot of activity, a lot of context switches, and a lot of boinks. I get more done in less time in code, and in the kitchen. 

However, it is not meditative. Sometimes I'll take the time to write some example Scala structures just the way I want, or just write text to get back to that relaxed, focused state.

Reading: Cory Doctorow's _Little Brother_ https://craphound.com/category/littlebrother/ . Fun start. Great pace.
Listening: The Mistholme Museum of Mystery https://shows.acast.com/the-mistholme-museum-of-mystery-morbidity-and-mortality . Good vignettes for driving ... and it seems there's a larger plot after all.
