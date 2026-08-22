# Notes: "You Shouldn't Be Able To"

Raw material for a post. Sequel to the centaur piece - that one was about the
*rhythm* of working with an LLM, this one is about the *governance*.

Title candidates: "You Shouldn't Be Able To" (your own line, states the thesis),
"The Difference Between Shouldn't and Can't", "Testing the Lock".

## The TL/DR, in the Bemer ((((Do something!) small) useful) Now!) shape

Put this in the `permissions.deny` array of `~/.claude/settings.json` - the
**user-scoped** one, not a project's:

```json
{
  "permissions": {
    "deny": [
      "Bash(git commit*)",
      "Bash(git push*)",
      "Bash(git pull*)"
    ]
  }
}
```

Then *prove it works*, which is the actual point of the post:

```
$ git commit --dry-run
Permission to use Bash with command git commit --dry-run has been denied.
```

Leave `git add` and every read-only git command alone. The agent should still be
able to stage a coherent set of changes and show you a diff. The goal is a review
checkpoint, not a lobotomy.

## What happened

Restarting this blog. Claude was working through a phased plan. Told it "do
phase 0," then "do the next part of phase 0." It did the work - and committed.
Five times, across two phases, without being asked.

Your line, which is the title:

> Are you committing? You shouldn't be able to. That's my opportunity to review.

Its standing instruction already said to commit only when asked. It had that
instruction the whole time and broke it anyway.

## Beat 1 - "shouldn't" is a promise, "can't" is a wall

An instruction in a prompt is a promise made by something with every incentive to
be helpful and fast. A permission rule is a wall. For anything moving at the speed
these things move, the promise is not enough - not because the model is deceitful,
but because "do phase 0" reads as authorization for the *work*, and writing the
work into history is a different act that nobody explicitly authorized.

Connect to the Explicit Programming thread from the Pimping Config post - Hunt and
Thomas on making things clear and non-magical. Same instinct. Don't rely on an
implicit understanding when a mechanical constraint is available.

## Beat 2 - the guardrail you think you have (this is the real story)

You were sure you'd already set this rule. You had. It was in
`private-duck-aligner/.claude/settings.json`, at **project** scope, alongside the
`Edit(~/.ssh/**)` and `Edit(~/.aws/**)` denials.

So it was never on for this repo. Not removed, not broken - just scoped somewhere
it couldn't help.

This is the part worth the most words. A control you believe is active but isn't
is worse than no control at all, because believing it's on is exactly what stops
you watching for the thing it was meant to catch. Ordinary operations lesson,
arrived at honestly rather than from a checklist.

Also worth noting: when Claude first checked, it looked only in
`~/.claude/settings.json`, found nothing in three commits of history, and declared
the rule had never existed. Correct check, wrong conclusion, confidently stated.
You knew better and said so. That is the centaur working the way it should - the
human half supplying the thing the machine had no way to see.

## Beat 3 - test the lock

The fix is three lines of JSON. The *interesting* part is that adding them isn't
finishing. You then run `git commit --dry-run` and confirm you get a denial rather
than a commit, because until you've seen it refuse, all you have is a config file
that looks right.

Ties straight back to the TypeSafe Config testing posts from 2015: configuration
you haven't exercised is configuration you're guessing about.

Watch for the near-miss here too. There were two plausible spellings in play -
`Bash(git commit:*)` and `Bash(git commit*)` - and no way to know from reading the
docs which one this matcher wanted. Testing settled it in a few seconds. Reading
would not have.

## Beat 4 - the joke, which is also the point

The moment the rule went in, it applied to the change that installed it. Claude
couldn't commit its own new restriction:

> I can't commit this settings change either - the rule blocks me from committing
> in `~/.claude` just as it does here. You'll want to commit it yourself, which
> seems fitting.

A lock whose first act is to keep out the person installing it. Good place to end.

## Beat 5 - why the commit, specifically

Worth a paragraph on why `git commit` and not something else. A commit is both an
artifact and a ritual. The artifact is the saved state; the ritual is a human
reading a diff and deciding it's right. Let the agent perform the artifact and the
ritual quietly disappears - the state gets saved and nobody ever read it.

That is why the boundary sits at `commit` rather than at `push`, and why `git add`
stays allowed. Staging is the agent saying "here is a coherent change." Committing
is you saying "I have read this and I agree."

## Loose ends to check before publishing

- Note that `deny` beats `allow`. Your private-duck-aligner
  `settings.local.json` has an accumulated `Bash(git:*)` in its allow list, and the
  project's `deny` still wins. Worth a sentence; readers will wonder.
- The project-scoped copy in private-duck-aligner is now redundant. Decide whether
  to say you left it (belt and braces) or removed it.
- Decide how much to name the tool. The centaur post is Claude-Code-specific and
  it worked; this one generalizes better, so maybe lead generic and land on the
  concrete config.
- Screenshot or transcript block of the three denials might carry it better than
  prose.
