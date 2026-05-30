# Material Transition Finder

*A conversation protocol for any capable AI agent*

A material transition is where pipe spec changes along a string — coating
grade flips, wall thickness steps up, manufacturer changes. When field
crews record it, the data is there as a dedicated transition point. When
they don't, it's still there — it's latent in the weld tally. Every joint
carries its attributes. Every change from one row to the next is a
transition waiting to be found.

This recipe finds those transitions automatically. You choose which
attributes to watch. The agent compares them row to row, sorted by
station, and flags every row where any selected attribute changes. The
result is a discrete CSV of transition points, ready to import or patch
into your project.

---

## What you need

A CSV of weld points. The agent recognizes material attributes by column
name — it will identify the likely candidates from names like COATING,
DIAMETER, WT, GRADE, MANUFACTURER, HT_AHEAD, JT_AHEAD and similar.
Where an attribute has an ahead variant, that is the value used for
comparison — ahead is the weld's forward-looking material record.
If your column names are ambiguous, tell the agent which ones to watch.
WELD_NO, COMMENTS, and administrative fields will be skipped unless you
ask for them.

If your CSV has a station column — any column with "sta" in the name —
the agent will sort by station before comparing. Without a station column,
rows are taken in the order they appear. If the data is not already in
station order, say so; sort it before handing it over or tell the agent
which column to use.

Station values in engineer's notation (100+00.00) are converted to
decimal automatically.

Gap detection works the same as in the ahead-back check. If a gap is
present, the first weld after the gap is always treated as a transition —
there is no valid prior row to compare against. Those rows are flagged in
the output. The default gap threshold is 85 feet; tell the agent your
nominal joint length if your pipe is shorter.

---

## Sample prompt

```
Here is my weld tally for the Red River crossing. Find all material
transitions — I care about COATING, WT, GRADE, and MANUFACTURER.
Pipe is 40-foot joints.

[attach CSV]
```

Or if you want the agent to decide:

```
Here is my weld CSV. Identify the material attribute columns and find
all rows where any of them change from the previous row. Sort by station.

[attach CSV]
```

---

## What you get

A CSV of transition points only — one row per detected transition, named
to make its purpose clear (e.g. `redriver_material_transitions.csv`).

Each row includes:

- The station and weld number of the transition point
- The attributes that changed — before and after values, side by side
- A gap flag if the transition immediately follows a data gap

This is a discrete file. It does not modify your original weld table.
Import it into Data Halo as a separate layer, patch it into your project,
or use it to annotate alignment sheets.

---

## Recoding and renumbering

Many projects use a dedicated code for material transition shots —
`MATL_TRANS`, `PIPE_TRANS`, or whatever the operator named it — with
the same schema as the weld table but a different CODE value.

After finding the transitions, the agent will ask:

1. **Recode?** — The agent looks for a code column in your data. It
   recognizes these names: CODE, CODES, FEATURE CODE, FEATURE_CODE,
   FEATURE CODES, FEATURE_CODES. If found, it will offer to replace the
   existing code value on each transition row with a new one you specify.

2. **Renumber POINT_ID?** — If your data has a POINT_ID column, the agent
   will offer to renumber the transition rows. Tell it whether you want a
   prefix, a suffix, or plain sequential integers, and what the pattern
   should be. For example: prefix `MT-` produces MT-1, MT-2, MT-3.
   Suffix `_T` produces 1_T, 2_T, 3_T. Plain sequential starts at 1.

Both are optional. If you don't need them, say so and the agent skips
ahead.

---

## What the agent is doing

The agent sorts the weld table by station, then walks the rows in order.
At each row it compares the selected attribute values to the row above.
If any value differs, that row is a transition. The transition row is the
first weld carrying the new material — which is the standard convention
for recording transitions in the field.

---

## Limitations

This is a data-consistency method. If the material was recorded wrong in
the field — wrong heat number, wrong coating grade entered — this recipe
finds where the *recorded* attributes change, not necessarily where the
*actual* pipe spec changes. Verify against MTRs when it matters.

If the same spec returns after an interruption — X70 pipe, then X65, then
X70 again — each change is flagged. That is correct behavior.

---

## Troubleshooting

**More transitions than expected** — Check for inconsistent formatting:
trailing spaces, mixed case, leading zeros on wall thickness. The agent
normalizes case and whitespace by default; tell it if numeric fields need
rounding.

**Transitions at every row** — The data is not sorted. Either provide a
station column or sort the CSV before attaching.

**First row is always flagged** — The first weld has no prior row. It will
always appear as a transition. This is expected; it marks the beginning
of the string.

**Gap rows flagging all attributes** — If a gap introduces a new segment,
the first weld after the gap will show all attributes as changed — there
is nothing to compare against. The gap flag identifies these rows. Filter
on `gap_flag = False` to see only mid-segment transitions.

**Code column not recognized** — Your column name isn't in the recognized
set (CODE, CODES, FEATURE CODE, FEATURE_CODE, FEATURE CODES,
FEATURE_CODES). Tell the agent the exact column name and it will use it.

---

## Relationship to Data Halo's Transitions page

Data Halo's Transitions export does exactly this — user selects attributes
via checkboxes, the server walks the sorted weld table and returns the
transition rows as a CSV. This recipe is the field-side equivalent: same
logic, same output, no login required. If you have Data Halo access and a
loaded project, use the page. If you're working offline or with data that
isn't imported yet, use this recipe.

---

*Recipe by [Data Halo](https://datahalo.asbuilt.systems) — pipeline survey and asbuilt software.*
