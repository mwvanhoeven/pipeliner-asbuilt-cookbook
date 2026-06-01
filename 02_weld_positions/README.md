# Weld Position Calculator

*A conversation protocol for any capable AI agent*

You have an anchored 3D DXF polyline — the bore path, placed on real surveyed coordinates. This recipe pushes pipe joint lengths along that polyline and returns a CSV of calculated weld positions.

**Prerequisite:** The polyline must be anchored to surveyed control before you begin. If you are starting from a driller's report, complete [Recipe 01](../01_hdd_drill_to_dxf/) first, then anchor the resulting DXF in CAD before continuing here.

> **The anchor step is not optional.**
> A polyline that has not been anchored to surveyed coordinates will produce weld positions that are geometrically correct but locationally meaningless. Move and rotate the polyline in CAD so its entry vertex sits on your surveyed entry coordinate and its direction aligns with the known bore azimuth — before you bring it here.

---

## What you need

- **The anchored 3D DXF.** The polyline moved and rotated in CAD to align with surveyed control. Must have Z values — if your CAD export flattened it, see Troubleshooting.
- **Joint lengths.** The length of each pipe joint in the string, in order from entry to exit. From the pipe tally or fabrication records.

---

## Field reference

| Field             | What to enter                       | Notes                                                        |
| ----------------- | ----------------------------------- | ------------------------------------------------------------ |
| **DXF file**      | Your anchored 3D polyline           | Must have Z values. Must be anchored to surveyed coordinates |
| **Joint lengths** | Length of each pipe joint, in order | Entry to exit. The first value places weld 1                 |
| **First value**   | Distance to first weld              | Adjust this to position the weld string. If the lead joint is a pup, enter its actual length |
| **Last value**    | Distance to exit/endpoint           | Marks the endpoint. Label it "Endpoint" in the output to distinguish from welds |

---

## What the agent is doing

The agent reads the 3D polyline vertices and builds a cumulative length profile of the bore. It then walks that profile, advancing by each joint length in sequence, and places a point at each weld location. For each weld it interpolates northing, easting, and elevation between the nearest vertices in 3D space.

---

## What you get back

A CSV with one row per weld:

```
Weld, Northing, Easting, Elevation, Length Ahead
1, 5432089.14, 345698.33, 881.20, 40.25
2, 5432078.41, 345718.92, 863.15, 40.10
...
Endpoint, 5431944.22, 345891.05, 830.50, 0
```

Ready for import into survey data management systems, or for checking against crossing surveys and profile data.

---

## Sample prompt

```
I've anchored my bore polyline in CAD. Here is the updated DXF file.

Please calculate weld positions along this polyline using these joint lengths:
40.25
40.10
39.95
40.33
...

Please give me a CSV with columns: Weld, Northing, Easting, Elevation, Length Ahead.
```

Joint lengths can be space-separated, comma-separated, or one per line. Paste from Excel works.

---

## Troubleshooting

**Agent says the DXF has no Z values** — Your CAD export may have flattened the polyline. Re-export and verify the polyline type is 3DPOLY (AutoCAD) or equivalent in your CAD tool. LWPOLYLINE is 2D.

**Weld positions are in the wrong location** — The polyline was not properly anchored before export. Return to CAD, verify the entry vertex matches your surveyed control, and re-export.

**Joint lengths push past the end of the polyline** — Your tally sums to more than the bore length. Check for extra joints or transcription errors. The agent should warn you when this happens.

**CSV northings and eastings look swapped** — Coordinate order conventions vary by system. If your destination expects Easting, Northing order, swap the columns.

---

*Recipe by [Data Halo](https://data-halo.com) — pipeline survey and asbuilt software.*
