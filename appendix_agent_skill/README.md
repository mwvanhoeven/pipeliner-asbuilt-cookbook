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

---

## Installing the skill

The skill definition is in `asbuilt-systems.skill.md` in this directory. To turn it into an installable Claude skill, ask your agent:

> "Read this file and use the skill-creator to build and install a skill from it."

Point your agent at the raw GitHub URL of `asbuilt-systems.skill.md` or paste the contents directly. The agent handles the rest. Once installed, type `/asbuilt-systems` to start a session.

---

## What you can read

- `asbuilt-systems.skill.md` — the skill definition; readable on its own if you want to understand what the agent will do before installing it.

---

*Appendix by [Data Halo](https://datahalo.asbuilt.systems) — pipeline survey and asbuilt software.*
