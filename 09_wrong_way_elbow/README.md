# Wrong-Way Elbow Detector

*A conversation protocol for any capable AI agent*

A 3-point elbow in a pipeline asbuilt is three survey shots: one
approaching the fitting, one at the elbow, one leaving it. When the
survey is done carefully, the middle shot lands where the pipe actually
bends. When it isn't, the middle shot can land in the wrong place —
creating a vertex that bends the pipeline in the wrong direction before
it corrects back on the next segment.

On a map, a wrong-way elbow looks like a spike or a kink. The human eye
catches it instantly. In a coordinate table, it's invisible. This recipe
finds them automatically and marks the results so the field crew knows
exactly where to go.

This recipe works in 2D — plan view only. Anomalies in the vertical
profile are a separate problem.

---

## What you need

A DXF file containing the pipeline as a single polyline, or as line
segments that can be joined into one — or a CSV of coordinates. Both
inputs are supported. The agent prefers a single continuous sequence;
declare the input format in your prompt.

**DXF input:** The agent extracts polyline vertices directly. Multiple
disconnected polylines in the same file are processed separately. If
they represent one continuous pipeline, tell the agent and it will
attempt to join them in order before running the check.

**CSV input:** The agent recognizes Northing and Easting columns using
the standard names in [REFERENCE.md](../REFERENCE.md#northing). For
station column recognition, sorting behavior, and engineer's notation
conversion, see [REFERENCE.md](../REFERENCE.md#station).

The agent works in plan view (X, Y only). Z values are ignored.

---

## Sample prompts

**DXF input:**
```
Here is a DXF of the Brazos River lateral. Check it for wrong-way
elbows — vertices where the pipe bends back against its own trend.
Mark any you find and give me the DXF back.

[attach DXF]
```

**CSV input:**
```
Here is a coordinate CSV of my pipeline centerline, sorted by station.
Check it for wrong-way elbows and give me back a marked DXF.

[attach CSV]
```

Or if you want to set the sensitivity:

```
Here is my pipeline DXF. Find vertices where the deflection reverses
against the local trend and at least one of the flanking segments is
under 20 feet. Flag anything over 10 degrees of reversal.

[attach DXF]
```

---

## What the agent is doing

The agent walks the coordinate sequence vertex by vertex in 2D. At each
vertex it calculates:

- The **incoming bearing** — direction of the segment arriving at this vertex
- The **outgoing bearing** — direction of the segment leaving this vertex
- The **deflection** — the turn angle between them, and whether it is a
  left or right turn
- The **local trend** — the general direction of travel across the
  surrounding vertices

A vertex is flagged when two conditions are both true:

1. The deflection reverses against the local trend — the pipe turns left
   when the surrounding geometry is turning right, or vice versa
2. At least one of the two flanking segments is short — under 15 feet by
   default

The short-segment filter is what separates a wrong-way elbow from a
legitimate curve. A pipeline following a road or a river makes many small
consistent bends; each segment is short but they all turn the same way.
A wrong-way elbow has a reversal — and that reversal almost always
involves at least one very short leg.

The default short-segment threshold is 15 feet. Tell the agent a
different value if your 3-point elbows tend to span more than that.

---

## What you get

**If your input was a DXF:** A DXF file with the original polyline
intact, plus a new layer named `WRONG_WAY_ELBOWS`. On that layer, each
flagged vertex gets a circle and a text label with the distance along
the polyline from the start and the reversal angle
(e.g. `STA 4823.4 — reversal 31°`). The layer can be toggled off in
CAD or Civil 3D. The original geometry is not modified.

**If your input was a CSV:** Tell the agent what you need — a new DXF
containing the reconstructed polyline with flagged vertices marked, or
a CSV of the flagged coordinates with reversal details for you to map
yourself. The agent will produce whichever you ask for, or both.

In either case the agent provides a plain-English summary: how many
vertices were flagged, where they are, and the reversal angle at each
one. If nothing was flagged, it says so.

---

## Troubleshooting

**Nothing flagged but I can see a problem on the map** — The reversal
may not involve a short segment — the two flanking segments might both
be long, which the algorithm treats as a legitimate curve. Tell the
agent to remove the short-segment filter and flag all reversals above
a degree threshold instead.

**Too many flags on a curved section** — The pipeline follows a
sustained curve and the local trend calculation isn't spanning far
enough. Tell the agent to widen the trend window (default is 3 segments
on each side; try 5 or 7).

**Agent can't read the DXF** — Some DXF exports from data collectors
use older format versions or non-standard entity types. If the agent
reports a parse error, try re-exporting from Civil 3D or AutoCAD as
DXF R2010 or later.

**CSV rows are out of order and there's no station column** — Sort the
CSV by station before attaching, or add a station column so the agent
can sort it. See [REFERENCE.md](../REFERENCE.md#station).

**Multiple polylines processed as separate pipelines** — If your DXF
has segments that belong to one continuous pipeline but are stored as
separate entities, tell the agent to join them before running the check.
Provide the order if it isn't obvious from the coordinates.

---

## A note on field bends

Field bends — cold bends made on-site to follow terrain — can be almost
any angle and are intentional. This recipe does not attempt to flag field
bends as wrong. What it looks for is the signature of a *survey artifact*:
a reversal at a vertex flanked by at least one very short segment, which
is the geometry that results from a careless shot at a 3-point elbow.

If your pipeline has a lot of field bends in close succession, you may
get false positives in those areas. Review flagged vertices against your
field notes before sending a crew back out.

---

## Relationship to Data Halo

Data Halo's Vertical Profile page surfaces Z anomalies visually. The
Leaflet map on the project dashboard is where plan-view problems like
wrong-way elbows are easiest to spot by eye. This recipe automates what
the eye does on the map and puts the result back into the DXF — so the
finding travels with the file rather than living in someone's memory.

---

*Recipe by [Data Halo](https://datahalo.asbuilt.systems) — pipeline survey and asbuilt software.*
