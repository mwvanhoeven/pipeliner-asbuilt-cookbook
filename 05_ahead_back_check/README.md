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

## What you get

An Excel workbook with your data as it came in — same columns, same order,
same values. If a station column was present, rows are sorted by station;
otherwise the original row order is preserved.

Where an ahead value on one weld disagrees with the back value on the next,
both cells are filled pale red. The user decides which is wrong. The
comparison ignores case and leading or trailing spaces.

If a station column was present, a thick horizontal line marks each gap in
the station sequence. Welds on either side of a gap have no valid pair to
check against and will not be highlighted.

---

## Sample prompt

```
Brazos River crossing, 40-foot joints. Run the ahead-back check.

[attach CSV]
```

Or without a station column:

```
File is already in station order. Run the ahead-back check.

[attach CSV]
```

---

## Working the spreadsheet

This is a working document, not a report. Edit the red cells directly.
When the value agrees with its pair, the red clears. When you are
satisfied, export as CSV and import into Data Halo or Civil 3D.

The red is driven by a live formula. Nothing needs to be rerun. If your
file had a station column, a hidden column named `_GAP` is present in the
workbook. It drives the gap suppression. Do not delete it.

Construction unfolds daily. If new welds come in after you've run the
check, bring the new rows back to this chat as a CSV and ask the agent
to merge and rerun on the combined data. The output replaces the previous
workbook — sorted, regapped, reformatted from scratch.

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
