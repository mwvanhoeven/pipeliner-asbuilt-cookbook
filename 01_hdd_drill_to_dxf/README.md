# HDD Drill Report to 3D Polyline

*A conversation protocol for any capable AI agent*

You have a driller's report. It contains columns of numbers describing the path of a bore — distances away, elevations, sometimes lateral offsets. That report is a self-consistent geometric description of what the drill did, **but it has no real-world coordinates.** It floats in space until someone anchors it to surveyed ground control.

This recipe describes how to turn that floating geometry into a 3D DXF polyline. The polyline is then ready for the anchor step in CAD, after which you can push weld positions along it (see [Recipe 02](../02_weld_positions/)).

You do not need a Data Halo account. You need a drill report, an AI agent with code execution, and a CAD tool that can open DXF files.

---

## What you need from the drill report

Before you talk to your agent, find these things:

- **A beginning coordinate (NEZ).** The northing, easting, and elevation of the entry point. If you have a surveyed entry point, use it. If not, a placeholder works — you will anchor it later anyway.
- **A foresight coordinate (NEZ).** A point downrange that establishes the bore azimuth. Does not need to be the exit point — it just needs to point in the right direction.
- **The away/elevation/lateral table.** The core of the drill report. Usually labeled "X Dist", "Away", or "Measured Depth" for the first column. Elevation or depth for the second. Lateral offset for the third — use 0 for every row if no lateral column exists.
- **Elevation mode.** See the [Elevation Mode appendix](#appendix-understanding-elevation-modes) if you are unsure which convention your report uses.

---

## Field reference

| Field              | What to enter                                     | Notes                                                        |
| ------------------ | ------------------------------------------------- | ------------------------------------------------------------ |
| **Beginning NEZ**  | Northing, Easting, Elevation                      | Coordinates of the entry point                               |
| **Foresight NEZ**  | Northing, Easting, Elevation                      | A point downrange that establishes bore azimuth              |
| **Away**           | Distance along bore path                          | Cumulative from entry. "X Dist", "Measured Depth", or "Away" in most reports |
| **Elevation**      | Depth or absolute elevation                       | Interpretation depends on elevation mode                     |
| **Lateral**        | Left/right offset from centerline                 | Positive = right, negative = left. Zero if no horizontal curves |
| **Elevation mode** | "Real world", "negative down", or "positive down" | See appendix if unsure                                       |

---

## What the agent is doing

- **Beginning + foresight** define the azimuth of the bore in plan view.
- **Away** is a station along that baseline — cumulative distance traveled along the bore path.
- **Lateral** is a perpendicular offset from the baseline at that station. Most bores have none.
- **Elevation** is the Z value at that point — absolute or relative to entry depending on mode.

The agent places a 3D point for each row, connects them in sequence, and outputs a DXF polyline. The result is internally consistent with the drill report. It has no real-world coordinate provenance until you anchor it in CAD.

---

## What you get back

A 3D DXF file containing a single polyline. Each vertex corresponds to a row in your away/elevation/lateral table, plus the entry point.

If the agent returns a WKT linestring or JSON coordinate list instead of a DXF, ask it to convert that to a 3D DXF in the same conversation.

---

## Sample prompt

```
I have an HDD drill report I need to convert to a 3D DXF polyline.

Beginning point (N, E, Elev): 5432100.00, 345678.00, 892.50
Foresight point (N, E, Elev): 5432050.00, 345900.00, 892.50
Elevations in the table are real-world (absolute).

Away, Elevation, Lateral:
100.00, 880.20, 0.00
200.00, 862.45, 0.00
300.00, 845.10, 2.50
400.00, 832.00, 2.50
500.00, 830.50, 0.00
...

Please produce a 3D DXF polyline from this data and give me a file I can download.
```

Paste-from-Excel works. Commas or tabs both work.

---

## After this step: the anchor

> **The polyline is geometrically correct but locationally meaningless until anchored.**

Before you push weld positions, take the DXF into CAD and move/rotate it so the entry vertex aligns with your surveyed control. This step cannot be automated. Only you have the survey.

See [Recipe 02](../02_weld_positions/) for the weld push step, which begins with the anchored DXF.

---

## Troubleshooting

**Profile looks wrong** — Check your elevation mode. If the bore dips far deeper than expected, you may have absolute elevations set to a relative mode.

**Bore curves the wrong direction** — Check your lateral signs. The convention is right = positive. If your report uses the opposite, negate the lateral column.

**Bore points the wrong direction** — Swap beginning and foresight, or provide a foresight that is clearly in the direction of travel.

**Agent can't produce a DXF** — Ask it to output the Python script that generates the DXF and run it yourself, or ask for WKT coordinates and construct the DXF in another tool.

---

## Appendix: Understanding elevation modes

Getting the elevation mode wrong produces a bore that looks reasonable in plan but is wildly wrong in profile.

**Real-world (absolute) elevations** — The column holds actual survey elevations. If your entry is at 892.50, the first row should show a value near that. Tell the agent: *"Elevations are real-world absolute."*

**Negative values down from beginning** — The column holds negative numbers representing depth below entry (e.g., -12.5 means 12.5 feet below entry). Tell the agent: *"Elevations are negative values down from entry."*

**Positive distances down from beginning** — The column holds positive numbers representing distance downward from entry (e.g., 12.5 means 12.5 feet below entry). Tell the agent: *"Elevations are positive distances down from entry."*

**Quick check:** Look at the first row. If the elevation is close to your entry elevation — real-world mode. If it's near zero — relative mode. If still unsure, paste the first few rows and ask the agent to identify the convention.

---

*Recipe by [Data Halo](https://data-halo.com) — pipeline survey and asbuilt software.*
