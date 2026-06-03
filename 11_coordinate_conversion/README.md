# Coordinate Conversion

*A conversation protocol for any capable AI agent*

You received a file from a client. The coordinates are in the wrong system for your project. Maybe it's Texas South Central NAD27 and you need NAD83 2011. Maybe it's UTM in meters and you need State Plane in US Survey Feet. Maybe you need to go the other direction — zoned coordinates to latitude/longitude, or the reverse. Historically you would have opened CorpsCon and worked through it manually. This recipe hands that job to an agent.

You do not need a Data Halo account. You need a coordinate file, an AI agent with code execution, and a clear description of what system you are coming from and what system you are going to.

---

## What you need before you start

- **Your coordinate file.** CSV, TXT, or Excel. The columns need to contain coordinates — the agent will recognize common column names automatically (see [Column Name Reference](../REFERENCE.md)).
- **Source coordinate system.** What system are your incoming coordinates in? Name, FIPS code, or description. "Texas South Central NAD27", "UTM Zone 14 North meters", "latitude/longitude WGS84" — any of these works.
- **Target coordinate system.** Same — what do you need them converted to?
- **Replace or append.** Do you want the original coordinate columns replaced, or new columns added alongside them?

If you are not sure of the source system, check the survey report or the CAD project settings that came with the file. State Plane zone names often appear in Trimble or Leica job settings. If you genuinely do not know, paste a few coordinate values and ask the agent to make an educated guess — it can often narrow it down from the magnitude and sign of the numbers.

---

## What the agent is doing

The agent reads your file, identifies the coordinate columns, and reprojects them using `pyproj` — the same underlying library used by GDAL, QGIS, and most professional GIS tools. It resolves your plain-language zone description to an EPSG code internally. You never need to know the EPSG code.

**Precision handling.** The agent matches output decimal places to your input. If your incoming coordinates are in feet with two decimal places, the reprojected coordinates will carry the same. If the conversion crosses unit types — meters to feet or feet to meters — the agent will not truncate prematurely.

**US Survey Feet vs. International Feet.** These differ by approximately 2 parts per million — small enough to ignore in casual work, large enough to accumulate across a long pipeline. Most Texas and US State Plane work uses US Survey Feet. The agent resolves this from the coordinate system description; if there is any ambiguity, it will ask before proceeding.

**Latitude/longitude.** Going to or from geographic coordinates (lat/long) is supported. The agent will output latitude as the northing equivalent and longitude as the easting equivalent, or recognize them on input — see the [Column Name Reference](../REFERENCE.md) for recognized column names.

---

## What you get back

A file in the same format as your input — same rows, same non-coordinate columns untouched — with coordinate columns either replaced or added. The filename carries the target zone name as you described it, for example:

`bore_log_Texas_South_Central_NAD83_2011.csv`

---

## Sample prompt

```
I have a CSV with survey points I need to reproject.

Source: Texas South Central, NAD27
Target: Texas South Central, NAD83 2011 Adjustment
Coordinate columns: Northing, Easting

Please add new columns for the reprojected coordinates rather than replacing the originals,
and give me a file I can download.
```

Attach the file or paste the table. The agent will confirm the column match before proceeding.

---

## Implementation note

The agent uses `pyproj` for all transformations. If it is not already installed in your agent's environment:

```bash
pip install pyproj pandas openpyxl
```

A ready-made script is included in this chapter: [`convert.py`](convert.py). The agent can run it directly or use it as the basis for your session. Either way, the transformation logic is stable — the agent is not improvising it fresh each time.

---

## Troubleshooting

**"I'm not sure which zone this is"** — Paste a few coordinate values and ask the agent to identify the likely system. Northing/Easting values in the 700,000–1,000,000 range in feet often point to a US State Plane zone. Values near 3,000,000–10,000,000 in meters suggest UTM.

**Coordinates shift by a small but consistent amount** — This is usually a datum mismatch (NAD27 vs. NAD83) or a feet/feet confusion (US Survey vs. International). Tell the agent which datum applies and ask it to verify the feet convention for your target zone.

**Latitude/longitude comes back wrong** — Confirm axis order. Some systems expect longitude first (XY), others latitude first. Tell the agent "latitude first" or "longitude first" if the output looks flipped.

**Agent cannot identify the zone from your description** — Try the FIPS code from your CAD or survey software project settings, or look up the zone name in the coordinate system list of any Esri or Trimble product you have on hand.

---

*Recipe by [Data Halo](https://data-halo.com) — pipeline survey and asbuilt software.*
