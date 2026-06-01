# Ahead-Back Check

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

A CSV of weld points with ahead and back columns. Any attribute that
appears in both directions will be checked. Columns without a direction
word are treated as ahead by default — see
[REFERENCE.md](../REFERENCE.md#direction-words) for the full recognition
rules, pairing logic, and what to do if your direction words aren't
recognized.

Projects with only one pair work. Projects with six pairs work. Projects
with no pairs at all will produce a spreadsheet with nothing to check —
the agent will tell you.

If your CSV has a station column, the agent sorts by station, detects
gaps, and marks segment breaks in the output. The default gap threshold
is 85 feet — tell the agent your nominal joint length if different. See
[REFERENCE.md](../REFERENCE.md#station) for the full station handling
behavior, column name recognition, and engineer's notation conversion.

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
direction words are recognized. See
[REFERENCE.md](../REFERENCE.md#direction-words) for the recognized forms.
If your columns use something else, rename them before running.

**Welds are out of order** — Your CSV has a station column but the values
aren't sorting as expected. See [REFERENCE.md](../REFERENCE.md#station)
for how engineer's notation is handled. If the sort still looks wrong,
convert to decimal feet before attaching.

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
