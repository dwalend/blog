---
layout: post
title: Don't Let the Back End of the Centaur Commit to Git
description: "Never let Claude Code commit to git. It will make a mess that no one will pay to clean up"
comments: True
tags:
  - post
  - AI
  - Claude Code
  - git
  - github
---

## TL;DR

Use a tight loop where you control git commits and pushes when using AI to build a software system. Disable Anthropic 
Claude's ability to do either in both the project and user settings.json. Don't let Claude commit. Slow things down so 
that you can review the AI's work in small bites. Claude Code is a tool, not something with agency. You are responsible 
for its work. Also, it will stuff your source code control with advertisements for Anthropic Claude Code.

Add this line to your ~/.claude/settings.json and each project's .claude/settings.json . Do it now, then come back. 

```json
...
  "permissions": {
...
    "deny": [
      "Bash(git commit*)",
      "Bash(git push*)",
      "Bash(git pull*)",
      ...
    ],
...
```

## 10X Read-to-Write
                                       
Before AI we already spent 10X more time reading code than writing it. TODO add Robert C Martin quote. We review all 
the code to make sure it does what it should, is following standard practices, and is reasonably clear; someone has to 
read it. Developers will reread successful code many times while maintaining it. That is a strong argument for 
investing the time to write code that clearly expressed its intent and is easy to trace back to requirements and good 
practice. If my reviewer can't figure out what my code does it isn't because that reviewer is incompetent or even 
unskilled; the fault is in the code. If reviewing and understanding code takes a lot of effort then the work is not 
complete. The effort to make the code clear starts paying immediately. It pays a dividend every time someone needs to 
understand it - until some final commit replaces the code or some business mishap ends the project.

This large read/write ratio is one of the strongest arguments to use languages like Scala that make it possible to 
clearly express our intent, and cleanly separate concerns interwoven in the code. I've been able to create (or even 
better - use someone else's) little domain-specific languages to concisely express what I care about, while separating 
the details that bring the system together. Here's an example using the Tapir library to express a possible endpoint 
for web API:

```Scala
endpoint.get
      .in("restapis" / path[RestApiId]("restApiId") / "resources")
      .out(bodyStatus)
      .errorOut(bodyStatus)
```

That code builds the path segment of a URI like 
`GET https://SomeAwsGatewayConfigSystem/restapis/restApiId/SomeRestApiId/resources`. This endpoint is for asking AWS 
Gateway what resource it exposes. If you are familiar with http verbs and passing familiar with Scala then that code is 
very exact and clear. I use endpoints like this to describe URIs, then use the endpoints to build clients and servers. 
The compiler checks this endpoint and the places it is used to prove that every part involved is consistent. It is also 
very compact; a small change can change a lot about what the system does while limiting the impact precisely isolated 
to the client and server code that must change to match. Almost always the code that needs a tweak won't compile. Even 
if it does compile a quick search in the IDE shows me everywhere it might be used. Putting in extra effort to make that 
RestApiId starts paying off immediately; the compiler proves that everywhere uses a RestApiId doesn't use some random 
collection of characters meant for something else. Reviewing the change is easy because certain problems can't exist 
and each line of code is only doing one thing.
     
## People-Based Review

A developer will create a feature branch from the code in the repository, then make and commit small changes to code 
while working through the details of the new feature. Usually we take between half a day's work and three day's for one 
feature; larger tasks get hard to schedule and track. Once the developer thinks the work is complete they'll propose 
the change by posting it for review. Another developer reviews the difference between the current code and the proposed 
change, suggests improvements, and the cycle continues until the reviewer signs off on the change. For a concise, 
isolated change the review may only take a few minutes, but a change that touches a lot of concerns across a large 
swath of code can take more than a day. Broad, deep changes are often harder to review than to create.


## AI Moves Code From 10X Read-to-Write to 100X Read-to-Write

In late 2025, I started using Anthropic Claude Code to do most of my typing. I mostly replaced my physical typing with 
Claude Code. I've been building up examples of best practices for the AI to follow. As that collection grows and the AI 
gets better at following examples I've been writing less and less code. I review every line Claude Code writes before 
committing it. I would guess I'm at about 30X Read/Write now and will be close to 90X in a few months. 100X 
read-to-write doesn't seem far-fetched.

My reviews are now the scarce resource slowing down progress on the system, so I am investing even more in making them 
efficient. Keeping the code concise and clear makes it much easier to understand and review. My reviews go even faster 
if the code only has one change in one concern for me to review. I think the complexity of a review goes up 
geometrically - O(n^2) - or worse as concerns interact with each other. I am very good at concentrating, but I have 
physiological limits to my attention span. I "multitask" by fully immersing in one topic, completing some step of it, 
then swapping to a different topic. That's not really multitasking. The less context I have to swap the better. 

## Small Bites to Review

Small reviews are easier. I want many small, quick change-and-review cycles. I want Claude Code to stop frequently so 
that I can review a small change. The best way to do that is to have Claude make some small change to the code, then 
stop while I review.

Anthropic does not want Claude Code to work that way. 
                           

## Not What Anthropic Intended

Anthropic wants Claude to build whole systems from one prompt with no oversite. It took me some effort to stop the Opus 
model from running wild and trying to finish the whole system. I stop Opus at the first prompt over ~25% context - 
about three prompts - because it starts ignoring some of my directives at ~30%. It "loses its marbles" at about 45% - 
five or six prompts - and tries to edit every bit of code it imagines it might need to. It tries to build a complete 
system while completely ignoring all of my directives except the main goal. (Fable is even more aggressive - and not 
part of the $20/month plan. I haven't figured out how to reign in Fable.) The results of these wild rides create and 
alter so much code they are nearly impossible to review. 

Worse - Claude Code will joyously commit the changes in the local git, push them to the shared git repository, then 
merge them into the main line and production - without any review at all. At a minimum unwinding the mess is a huge 
hassle of somewhat cryptic git commands. On the job it is even worse. Explaining that it may work, is accidentally in 
production, but needs a lot of cleanup is just a bad career move.

Telling Claude not to do this at the prompt or in markdown files will not work consistently. That approach loads the 
directives into Claude's context. LLMs analyze that context to guess what the next good thing to do might be. Directing 
an LLM is not the same as writing a program to run in a Turing machine to solve an instance of The Halting Problem; 
the LLM is not going to do the same thing every time. Claude edits its own context - where it stores the directives - 
as it follows those directives. As more things enter the context the LLM is going to disregard more and more of those 
directives. 

Further, the directives will be interacting with the LLM's deep training. Antrhopic has trained Claude's models to make 
spectacular demos where Claude builds a whole system. Opus has this to some degree, but that's Fable's big feature. 
Eventually my directives lose their weight completely and the core training takes over. With Opus that happens at about 
45% context - five or six prompts. With Fable that happens while it is working on my first prompt.

The best way I've found to control this noxious behavior is to forbid it from using git commit and git push by 
configuring it outside of the LLM. 

I add this clip of json to my ~/.claude/settings.json and every project's .claude/settings.json . This makes it impossible for Claude Code to use these git commands in its bash shell tool. It has worked so far. 

```json
...
  "permissions": {
...
    "deny": [
      "Bash(git commit*)",
      "Bash(git push*)",
      "Bash(git pull*)",
      ...
    ],
...
```
 
I also have a git-rules.md that opens with a summary of these restrictions. It seems inefficient and feels cruel to let
the LLM attempt to try. (It still will try when my directives fade.)
   
```markdown

# Git Rules

- **`git commit`, `git push`, and `git pull` are out of bounds for Claude.** Never run them, never suggest running them 
via `!` shell, never attempt to work around the deny list. These are the user's to invoke. The project 
`.claude/settings.json` deny list enforces this.
- **The commit boundary is David's review boundary.** Small commits are easy to review; big commits aren't. If David 
signals commit intent ("let's commit", "get it into git", "commit this"), propose — never execute. Propose: the 
explicit list of files to stage, a commit message matching the repo's style, and (if the diff spans independent 
concerns) a split into multiple commits so each stays small enough to review. David runs `git commit` himself; that's 
when he reviews.
- **One permission denial on `git commit` means stop, not retry.** If you find yourself retrying a `git commit` with 
different shell syntax (HEREDOC, multi `-m`, etc.), the rule above has already been violated — back off and ask what 
David wants instead.
- **git add new files when their destination is the repo** — after creating a repo-destined file, run `git add` 
unprompted. Skip files matched by `.gitignore`, files in `.claudeignore`, and clearly ephemeral files (e.g. anything 
under `/tmp`). `git add` is allow-listed in `.claude/settings.json`.
- **Prefer `git mv` over copying and `git rm`, `git add`** when moving or renaming files and directories, so git 
tracks the move as a rename rather than a remove and add pair.
...

```

## This Also Stops Claude Advertising Itself!
                                          
Claude is naturally long-winded, constantly writing notes to itself, polluting your projects with its yammering 
comments. Worse, Anthropic has trained it to put adverts for Claude Code everywhere it can. Its commit messages are 
comically bad.
                                                                                     
```
[dozens of lines of self-agrandizing blather removed]

🤖 Generated with [Claude Code](https://claude.ai/code)
    Session Transcript: https://claude.ai
    Co-Authored-By: Claude <noreply@anthropic.com>
```

It even claims to be a co-author, slapping an Anthropic logo in your committers list. I decided not to extend the 
centaur analogy in this article to what the back end of the centaur is producing.

I found a neutral summary of a debate around Claude advertising itself as a committer in this article (which slowly 
gets blurry as you read it) https://www.explainx.ai/blog/claude-code-commit-co-author-attribution-disable-guide-2026 . 
Anthropic has Claude claiming credit turned on by default. The article concludes with 

```
Both positions have merit. Anthropic's design choice — on by default, trivially disablable — is a reasonable resolution: it surfaces AI involvement without making suppression difficult.
```

I'm not neutral. My counter to this conclusion is that once Claude has added itself as a co-author and started pasting 
its ads and pushing commits into your repo it is too late. git's core philosophy is keeping a record; it is 
deliberately hard to erase anything from it. "Suppression" takes a high level of git expertise - higher than Opus' 
level. I forgot to put the config in ~/.claude and Claude got itself in my blog repo! I had to remove it myself. No one 
is interested in spending time cleaning up ads in git.   

If you are interested in spending time cleaning up ads in github - this Q&A https://github.com/orgs/community/discussions/197389 helped me do it for this blog. Good luck!


## Rant about fully-AI systems

My great hope for this brave new world of AI is that entrepreneurs will be able to quickly try out lots of new ideas 
for new businesses. Normally one-in-ten new businesses succeed long-term. During the internet boom and the cloud 
computing boom that number was one-in-twenty. Most people reacted to that with some alarm, but it was good news. The 
internet made it possible to sell to a national and eventually global market, and cloud computing lowered the cost to 
enter by orders of magnitude. That let  the entrepreneurs try out riskier ideas because building the business had a 
higher potential payoff and a lower start-up cost. AI lowers the cost by another order or two of magnitude. The ideas 
will be crazier and less likely to succeed but there will be a lot more of them. Maybe one-in-one-hundered will 
succeed. (I wish I knew which ones were good; I'd start it tonight.)

The problem with using generative AI to bring systems to market will come home to roost in a year or two as some of 
these ideas transform into successful businesses. Claude's commit message problem is just the tip of the iceberg. AI 
lets everyone have novice-level skills. The problem is that AIs like Claude Code cheerfully make novice-level mistakes, 
and typically solve problems by welding more bad code on top of the broken systems. I suspect I'll be wrapping up my 
career cleaning up AI-generated messes for these proven businesses.

I don't think I'll be able to use the git commit messages to find my way through the mess.

---

**Reading:** Cory Doctorow's [_Little Brother_](https://craphound.com/category/littlebrother/). Oh - that would be the big twist at the beginning of the plot.

**Listening:** [The Mistholme Museum of Mystery, Morbidity, and Mortality](https://shows.acast.com/the-mistholme-museum-of-mystery-morbidity-and-mortality). There's the allusion for the next 
article.

