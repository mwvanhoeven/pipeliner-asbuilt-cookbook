# Contributing to the Pipeliner Asbuilt Cookbook

If you have a workflow that works — one you have actually used in the field — this is the place for it.

---

## Not sure how to contribute? Start here.

You don't need a GitHub account or any technical knowledge to improve this cookbook. If something didn't work, or if you found a better way, your agent can handle the mechanics.

Just tell it:

- "Something in chapter 4 broke on my data — can you open an issue in the cookbook?"
- "We found a better way to handle X — can you draft a contribution?"
- "I want to suggest a new recipe idea — can you submit it?"

Your agent knows what to do. The humans here will take it from there.

---

## What belongs here

A recipe is a conversation protocol. It tells a field person what to say to an agent, in what order, and what to expect back. It does not require programming knowledge, a Data Halo account, or any specific tool beyond a capable AI agent with code execution.

If your workflow requires proprietary software to execute, it is not a recipe for this cookbook.

---

## What we are looking for

- A real problem that comes up in pipeline asbuilt work
- A prompt or prompt sequence that reliably solves it
- Enough context that a field person who has never tried this before can follow it
- Honest troubleshooting — what goes wrong, and what to do about it

---

## On included scripts

Some chapters include a ready-made Python script in the chapter folder. These are not proprietary — they are the straightforward implementation of the algorithm the chapter describes, the same code any capable agent would write given the recipe. Including them is hospitality: the user saves tokens, gets consistent behavior, and isn't dependent on the agent improvising the same logic fresh each session.

If your recipe has a stable, well-defined algorithm, consider including a script. If the recipe is conversational by design — like the FXL builder — leave it agent-driven.

Scripts that exist only because they are clever do not belong here. Scripts that exist because the algorithm is precise and the consistency matters do.

---

## Voice

Write for the person doing the work, not for the tool doing the compute. Name the real field problem in the opening paragraph before describing what the recipe does. In the "What you get" section, describe the output concretely — a file, its name pattern, what's in it — not what the agent is capable of. The hardest sentence is the table one-liner in the README index: it must name a specific artifact, not a general capability. Write it last.

Limitations sections earn their place by being honest about what the recipe cannot catch, not just what it handles gracefully.

---

## How to contribute

1. Fork this repository
2. Create a new chapter folder: `NN_your_chapter_name/` where NN is the next available number
3. Add a `README.md` following the structure of an existing chapter
4. Open a pull request

We expect an agent to be involved in drafting or reviewing your contribution. Note in your PR description which agent you used and what role it played. This is not a hard requirement — it is an expectation that helps us trust the recipe was tested with the tools it describes.

---

## Review

Pull requests are reviewed by a human and an agent together. We are looking for recipes that hold up against real field data, not just clean examples. If yours needs work, we will tell you specifically what and why.

---

## Issues

If a recipe breaks on your data, open an issue. Describe the data shape and what the agent did wrong. That is useful information even if you do not have a fix.

If you think you have found not just an issue but a fix — or a new recipe — say so in the issue. We can take it from there together.

---

*Cookbook by [Data Halo](https://data-halo.com) — pipeline survey and asbuilt software.*
