# Alignment Deflection Report

*A conversation protocol for any capable AI agent*

When a field crew stakes a pipeline construction baseline, they need to
know the deflection angle at each alignment vertex — how many degrees to
turn, and which direction. The instrument operator sets up over one point,
backsights the previous, and turns the deflection to the next. Without
the angle, they're guessing.

Data Halo generates this report from a loaded alignment. This recipe
produces the same output from a DXF or LandXML file, before the project
exists, or for anyone without Data Halo access.

---

## What you need

An alignment file — DXF or LandXML — containing the pipeline centerline
as a polyline or series of tangent lines. At least three vertices are
required; with fewer there are no interior deflection points to report.

**DXF input:** The agent extracts the polyline vertices in order. One
continuous polyline is preferred. If the file contains multiple polylines
or line segments, tell the agent which to use or ask it to join them.

**LandXML input:** LandXML is the preferred format when the alignment
has a non-zero begin station or station equations. The agent reads the
alignment geometry, begin station, and any station equations directly
from the file. No additional input is needed.

If your input is a DXF and your alignment has a non-zero begin station
or station equations, provide them separately:

```
Here is my alignment DXF. Begin station is 10+00.00.
I have one station equation: back 52+14.83, ahead 52+00.00.

[attach DXF]
```

---

## Sample prompts

**LandXML — simplest case:**
```
Here is a LandXML alignment file. Generate a deflection report.

[attach XML]
```

**DXF with no equations:**
```
Here is my pipeline alignment DXF. Generate a deflection report.
Begin station is 00+00.00.

[attach DXF]
```

**DXF with equations:**
```
Here is my pipeline alignment DXF. Begin station is 10+00.00.
Station equations: back 52+14.83 ahead 52+00.00,
back 103+27.41 ahead 103+00.00.
Generate a deflection report.

[attach DXF]
```

---

## What you get

An Excel workbook — one row per interior vertex, in station order —
with these columns:

| Column | Content |
|--------|---------|
| NORTHING | Projected northing at the vertex |
| EASTING | Projected easting at the vertex |
| LATITUDE | Latitude in DMS (e.g. `28°28'17.50551"`) |
| LONGITUDE | Longitude in DMS |
| EQU STATION | Equated station in plus notation (e.g. `05+84.30`) |
| DEFLECTION DD | Deflection angle in decimal degrees |
| DEFLECTION DMS | Deflection angle in degrees-minutes-seconds |

The file is ready to print and hand to the crew. The DMS column is what
the instrument operator reads.

**Sign convention:** Negative deflection is a left turn; positive is a
right turn. A `-33°47'36"` entry means turn left 33 degrees 47 minutes
36 seconds from the backsight.

---

## Station equations

A station equation is a point where the stationing resets — common when
an alignment is extended, shortened, or tied to an existing reference.
Equations are defined by a back station (the raw geometry station) and
an ahead station (the reported station from that point forward).

LandXML carries equations natively; the agent reads them automatically.

For DXF input, provide equations in your prompt as back/ahead pairs.
Multiple equations are listed in station order. The agent applies them
when computing the EQU STATION column.

If there are no equations, the EQU STATION column equals the raw
distance from the begin station.

---

## What the agent is doing

The agent walks the alignment vertices pairwise. At each interior vertex
(every vertex except the first and last) it:

1. Computes the incoming vector (previous vertex to this vertex) and
   the outgoing vector (this vertex to the next vertex)
2. Calculates the angle between the two vectors in decimal degrees
3. Determines the sign by checking whether the next vertex falls to the
   left or right of the incoming baseline — left is negative, right is
   positive
4. Converts to DMS
5. Computes the raw along-line distance from the start, applies the
   begin station offset and any equation adjustments, and formats as
   plus notation

Coordinates and distances are computed in the projected coordinate
system. Latitude and longitude are derived by transforming each vertex
back to WGS84. If no projection is declared, the agent will ask.

---

## Troubleshooting

**Agent asks for a projection** — The DXF has no coordinate system
declared. Provide the EPSG code for your project zone
(e.g. `EPSG:2278` for Texas South Zone US Survey Feet). LandXML
typically carries this information.

**Stations look wrong** — Check the begin station and any equations.
For DXF input, these must be provided in the prompt. For LandXML, they
are read from the file; verify the source export was correct.

**First and last vertices have no row** — Correct behavior. The first
vertex is the instrument setup point with no backsight; the last is the
final foresight with no ahead turn. Neither has a deflection to report.

**DMS angles show 60 seconds** — Rounding artifact at the seconds
boundary. The agent carries the same rounding logic as Data Halo:
when seconds round to 60, minutes increment and seconds reset to 00.

**Negative sign on what should be a right turn** — Check the vertex
order in the source file. If the polyline vertices are stored
counterclockwise or in reverse station order, the left/right
determination will invert. Re-export with vertices in station order.

---

## Relationship to Data Halo

Data Halo's Deflection Report is on the Alignments page and produces
this workbook directly from a loaded alignment, including equations.
Use this recipe when the project isn't loaded yet, when the crew needs
the report before import is complete, or when the alignment exists only
as a DXF or LandXML file.

---

*Recipe by [Data Halo](https://datahalo.asbuilt.systems) — pipeline survey and asbuilt software.*
