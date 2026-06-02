# Appendix — Conversational Agent Skill for Pipeline Asbuilt Platforms

This appendix is for office-side users: project managers, lead techs, coordinators, and clients who want to ask questions about their live project data without writing code or waiting on someone who can.

---

## What this is

A Claude skill is a saved configuration that gives your agent a standing set of instructions and tools. This one is built around the Python API examples published on various pages inside your pipeline asbuilt platform. The same code blocks you may have seen on export, report, and import pages — the ones with a username, password, and project alias — can be handed to a capable agent as-is. The agent runs them, reads the response, and answers your question in plain language.

You do not need to know how to program. The agent does the programming.

---

## What you can do with it

Once you have the skill installed and your credentials entered, you can ask plain-language questions about your project:

- "How far along is the mainline?"
- "How many weld points are in this project?"
- "Who imported files last week?"
- "What are the on-line codes for this project?"
- "Give me a full progress report across all lines."

The agent fetches live data from your platform, reasons over it, and answers. Downloads — KMZ, shapefiles — are also available. So is uploading a manifest or DXF sketch, with a confirmation step before anything is written.

---

## What you need

- A Claude account (claude.ai) — free tier works for occasional use; Pro recommended for regular use
- Your platform credentials (username and password)
- The skill file below

---

## The skill

**`asbuilt-systems.skill.md`** — works against any compatible platform. On launch it asks for your full server URL, then your credentials. One skill, no pre-configuration required.

To install: copy the contents of `asbuilt-systems.skill.md` into a new skill at claude.ai → Settings → Skills. Then type `/asbuilt-systems` to start a session.

---

## Demo walkthrough

Type:

```
/asbuilt-systems
```

When asked for a server URL, enter:

```
https://datahalo.asbuilt.systems
```

Enter your platform credentials when prompted. Pick a project from the list. Then ask:

```
Give me a progress report.
```

The agent fetches live data and returns phase coverage, baseline length, and percentage complete. From there, ask anything — point counts, file lists, code definitions.

---

## A note on the API examples in your platform

Every export, report, and import page in your platform includes a Python code block showing exactly how to call that page's endpoint. These examples are live — they use your actual project data, with only the password substituted. Any capable agent with code execution can run them directly.

This skill is the organized version of that capability: all the endpoints in one place, with a guided conversation to help you get answers without knowing which endpoint to call.

---

*Appendix by [Data Halo](https://datahalo.asbuilt.systems) — pipeline survey and asbuilt software.*
