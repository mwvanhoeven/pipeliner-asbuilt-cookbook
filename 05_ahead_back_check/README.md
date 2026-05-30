# Ahead-Back Diagonal Check

*A conversation protocol for any capable AI agent*

Every weld in a pipeline has two neighbors. The pipe joint coming into it
has a heat number and a joint number — and so does the joint leaving it.
The field crew records both directions: ahead and back. When the data is
clean, the heat-ahead on weld N matches the heat-back on weld N+1. Same
for joint, and for any other tracked attribute — wall thickness, coating
grade, whatever the operator requires.

When they don't match, something is wrong. Transposition, typo, missed
shot, wrong joint pulled from the rack. Finding those mismatches across
hundreds of welds by eye is the job this recipe automates.

---

## What you need

A CSV of weld points with paired ahead/back columns. The agent recognizes
these direction words: **ahead**, **ah**, **back**, **bk** — in any case,
with or without a separator. Any attribute that appears in both an ahead
and a back column will be checked. If your direction words are something
else, rename the columns before handing the file to the agent.

Projects with only one pair work. Projects with six pairs work. Projects
with no pairs at all will produce a spreadsheet with nothing to check —
the agent will tell you.

If your CSV has a station column, the agent will sort the welds by station
and detect gaps. A gap is a stretch of pipe longer than one joint with no
weld recorded — usually a segment break, an uninspected bore, or data not
yet in. The threshold is project-specific; the rule of thumb is slightly
longer than a nominal joint. Eighty-foot pipe: use 85. Forty-foot pipe:
use 50. If you don't say, the agent uses 85.

See [REFERENCE.md](../REFERENCE.md#station) for how station columns are
recognized and how engineer's notation is handled.

If there is no station column, the agent takes the rows in the order they
appear. You are responsible for sort order. Gap detection does not run.

---

## Sample prompt

```
I have a weld CSV from the Brazos River crossing. Pipe is 40-foot joints.
Run the ahead-back check and give me an Excel file. Use a gap threshold of 50.

[attach CSV]
```

Or without a station column:

```
Here is my weld data. It's already in station order. Run the ahead-back
check and give me an Excel file.

[attach CSV]
```

---

## What you get

An Excel workbook. One row per weld, in station order if station was
present. The ahead and back columns for each tracked attribute sit
side by side. Where a back value disagrees with the ahead value on the
row above, the cell is filled pale red. The comparison ignores case and
leading or trailing spaces.

A thick horizontal line marks a gap in the sequence. The weld below that
line has no valid pair above it and will not show red on its back values
— there is nothing to compare against.

---

## Working the spreadsheet

This is a working document, not a report. Edit the red cells directly.
When the value agrees with its pair, the red clears. When you are
satisfied, export as CSV and import into Data Halo or Civil 3D.

The red is driven by a live formula. Nothing needs to be rerun.

---

## Troubleshooting

**No red cells, but I know there are mismatches** — Check that your
direction words are recognized. The agent handles ahead/ah/back/bk. If
your columns use something else (fwd, rev, in, out), rename them before
running.

**Welds are out of order** — Your CSV has a station column but the values
aren't sorting as expected. If stations are in engineer's notation, the
agent converts them automatically. If the sort still looks wrong, convert
to decimal feet before attaching.

**Red on every back cell in the first row of a segment** — This is correct
behavior. The first weld after a gap has no valid pair above it; the thick
border is the signal. Those cells will always be empty or unverifiable.

**The gap threshold is flagging joints that aren't gaps** — Your pipe is
shorter than the default 85-foot assumption. Tell the agent the nominal
joint length and it will adjust.

**Agent says no ahead/back pairs found** — Your column names don't contain
a recognized direction word. Rename the columns and reattach the file.

---

## A note on what this checks

This is a transcription check, not a material verification. The spreadsheet
tells you whether the data is internally consistent — whether what was
recorded ahead on one weld matches what was recorded back on the next.
It does not know whether the heat number itself is correct, whether the
joint was actually inspected, or whether the MTR on file matches the pipe
in the ground. Those are separate questions.

---

*Recipe by [Data Halo](https://datahalo.asbuilt.systems) — pipeline survey and asbuilt software.*
