# Column Name Reference

Data Halo's import recognizes a wide range of column names from different
data collectors and office software. Recipes in this cookbook use the same
recognition lists. If your column name isn't here, tell the agent the
exact name and it will use it.

Matching is case-insensitive.

---

## Point Identifier

P, POINT, POINT ID, POINT_ID, POINT IDS, POINT_IDS, ID, IDS, PNUM,
NAME, NAMES, POINT NUMBER, POINT_NUMBER, POINT NUMBERS, POINT_NUMBERS,
POINT NO, POINT_NO, POINT NOS, POINT_NOS, POINT NAME, POINT_NAME,
POINT NAMES, POINT_NAMES, PT#, #POINTID, #P, PTNUM

## Code

CODE, CODES, FEATURE CODE, FEATURE_CODE, FEATURE CODES, FEATURE_CODES, D

## Northing

NORTHING, NORTHINGS, NORTH, N, Y, Y COORD, Y COORDS, Y_COORD, Y_COORDS

## Easting

EASTING, EASTINGS, EAST, E, X, X COORD, X COORDS, X_COORD, X_COORDS

## Latitude

LATITUDE, LAT, LAT., LATITUDE_DD, LAT_DD, LATITUDE DD

## Longitude

LONGITUDE, LON, LONG, LNG, LON., LONG., LONGITUDE_DD, LON_DD, LONGITUDE DD

## Elevation

ELEVATION, ELEVATIONS, ELEV, Z, HEIGHT, ELEV_COORD, ELEV COORD,
ELEV_COORDS, ELEV COORDS, ELEV.

## Station

**Column name recognition:** Any column whose name contains **sta**
(case-insensitive) is treated as a station column. Examples that match:
STATION, STA, STA., STATION NO, PIPE_STA, WELD_STATION. If two station
columns are present, the decimal one is used.

**Engineer's notation:** Station values in plus notation (e.g. 100+00.00,
52+17.43) are converted to decimal feet automatically before sorting or
gap detection.

**Behavior when station is present:**
- Rows are sorted by station before any processing
- Gap detection runs automatically using the nominal joint length as
  threshold (default 85 feet; tell the agent your joint length if
  different)
- The first row after a gap has no valid prior row to compare against
  and is treated accordingly — flagged, excluded from diagonal
  comparisons, or marked as a segment start depending on the recipe

**Behavior when station is absent:**
- Rows are taken in the order they appear in the file
- Sort order is the user's responsibility
- Gap detection does not run
- If you tell the agent the file is already in station order, it will
  proceed without sorting; if order is uncertain, sort before attaching

## Direction Words

Weld records describe the pipe segment **ahead** of the weld by default.
A bare attribute column — `heat`, `joint`, `wall` — records the material
of the joint being laid in the ahead direction. This is not a convention
of any particular software; it is what a weld point means in pipeline
construction.

Back columns record the material of the joint already in the ground behind
the weld. They appear when the project requires a transcription check —
confirming that what one weld recorded ahead matches what the next weld
recorded back.

**Recognized direction words:**

| Direction | Recognized forms |
|-----------|-----------------|
| Ahead     | ahead, ah       |
| Back      | back, bk        |

Recognition is case-insensitive. The direction word may appear as a prefix
or suffix, separated from the attribute name by any consistent separator
— underscore, hyphen, space, period, or none. The separator convention is
a property of the file, not of the recipe: if a file uses `heat_ahead` it
will also use `heat_back`, not `heat-back`.

**Pairing key:** everything that remains after stripping the direction word
and its separator. Multi-word attributes are supported. `coating grade ah`
and `coating grade bk` pair on `coating grade`. `pipe_wall_thickness_ahead`
and `pipe_wall_thickness_back` pair on `pipe_wall_thickness`.

**Bare columns:** a column with no direction word is treated as ahead. If
`heat` and `heat_back` both appear, `heat` is the ahead column. If only
`heat` appears with no back counterpart, it still describes the ahead
material — it just has no pair to check against.

**Unrecognized direction words:** if your file uses words other than those
listed above (fwd, rev, in, out, dn, us, etc.), rename the columns before
attaching the file.

## File Name

FILE, FILES, FILENAME, FILE NAME, FILENAMES, FILE NAMES, FILE_NAME,
FILE_NAMES

## Phase

PHASE, PHASES

## Party Chief

PARTY CHIEF, PARTY_CHIEF, PC, P.C., PARTYCHIEF, PARTY CHIEFS,
PARTY_CHIEFS

## Survey Date

SURVEY DATE, SURVEY_DATE, SURVEYDATE, DATE SURVEYED, DATE_SURVEYED, DATE

Expected format: yyyy-mm-dd

## Comment / Field Notes

FIELD NOTES, FIELD_NOTES, FIELD NOTE, FIELD_NOTE, FIELDNOTE, FIELDNOTES,
VOLUME, VOL, VOLUMES, VOLS, VOL., FIELDNOTE REF, COMMENT, COMMENTS,
NOTE, NOTES

---

*Reference by [Data Halo](https://datahalo.asbuilt.systems) — pipeline survey and asbuilt software.*
