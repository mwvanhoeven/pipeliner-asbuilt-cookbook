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

*Appendix by [Data Halo](https://datahalo.asbuilt.systems) — pipeline survey and asbuilt software.*
