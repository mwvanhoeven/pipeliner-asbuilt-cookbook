# FXL Builder

*A conversation protocol for any capable AI agent*

An FXL file is a Trimble field coding definition — it tells the data
collector what codes exist on a project, what attributes each code
collects, and what type each attribute is. Without one, the crew collects
points with no structure. With one, every shot is labeled and every
attribute is prompted in the right order.

The problem: FXL files are XML, and nobody wants to write XML by hand.
Data Halo generates them from its code library. But sometimes you inherit
a pile of points without the FXL that produced them, or you're starting
from scratch in the field and need one built fast.

This recipe builds it through conversation.

---

## Three ways in

### 1. From a point file

You have a CSV of collected points — codes and attributes already in the
data, but no FXL. The agent reads the file, infers the code list and
attribute structure from what's present, and proposes a draft. You
confirm, correct, or add to it. The conversational build takes over for
anything the agent can't infer — attribute types, required vs optional,
list items, defaults.

```
Here is a CSV of points from the Sabine River job. We weren't given an
FXL. Can you infer the code structure and build one?

[attach CSV]
```

The agent will tell you what it found, flag anything ambiguous (a column
that could be a list or a free-text string, a numeric field with no clear
range), and ask before assuming.

### 2. From a spreadsheet

You've already thought it through — codes in one column, attributes in
another, types and defaults filled in. The agent validates and renders.

Expected columns: CODE, ATTRIBUTE, TYPE, REQUIRED, DEFAULT, LIST_ITEMS.
TYPE values: STRING, LIST, FLOAT, INTEGER, PHOTO, DATE, DATE_AUTO.
LIST_ITEMS is a pipe-separated list of menu options (e.g. `YES|NO|NA`).

```
Here is my code definition spreadsheet. Build an FXL from it.

[attach CSV or Excel]
```

### 3. Pure conversation

You're starting from nothing. The agent asks, you answer.

```
I need an FXL for a new pipeline project. Walk me through it.
```

The agent will ask for your first code name, then work through its
attributes one at a time — name, type, required or optional, default value
or list items. When that code is done it asks for the next. When you say
done, it renders the file.

---

## Attribute types

| Type | What it is | When to use it |
|------|-----------|----------------|
| STRING | Free text | Heat numbers, comments, any open-ended field |
| LIST | Menu of options | Coating type, pipe grade, yes/no fields |
| FLOAT | Decimal number | Cover depth, wall thickness, joint length |
| INTEGER | Whole number | Weld number, joint count |
| PHOTO | Photo capture | Pipe end photos, damage documentation |
| DATE | Date, user enters | Survey date when crew sets it manually |
| DATE_AUTO | Date, auto-stamped | Survey date when collector sets it automatically |

---

## What you get

A valid FXL file named for the project (e.g. `sabine_river.fxl`), ready
to load onto a Trimble data collector or import into Data Halo.

If you used the point-file path, the agent will also tell you what it
assumed and where it guessed — so you can verify before the crew goes
back out.

---

## Troubleshooting

**Collector rejects the FXL** — The most common cause is a code or
attribute name with a space or special character. FXL names should use
letters, numbers, and underscores only. Ask the agent to sanitize the
names and regenerate.

**List items are wrong** — The agent inferred list items from values it
saw in the point file. If the field crew used abbreviations or
non-standard entries, the inferred list may be incomplete. Review the
LIST_ITEMS for each list attribute before loading the file.

**An attribute I need isn't in the inferred draft** — The agent can only
infer attributes that have a column in the point file. Attributes that
weren't collected (or weren't collected yet) won't appear. Add them in
the conversational follow-up.

**FLOAT range is wrong** — The agent sets range from the min and max
values it sees in the data, with some margin. If your actual valid range
is different, tell the agent and it will update.

---

## Relationship to Data Halo

Data Halo generates FXL files from its code library via the Export FXL
button on the Codes page. If you have a Data Halo project with codes
already defined, use that — it will be faster and exact. This recipe is
for when you don't have a project yet, or you're working from inherited
data and need to reconstruct the coding structure before you can import
anything.

Once you have a working FXL, you can import it into Data Halo as a seed
to bootstrap your code library.

---

*Recipe by [Data Halo](https://datahalo.asbuilt.systems) — pipeline survey and asbuilt software.*
