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

## Elevation

ELEVATION, ELEVATIONS, ELEV, Z, HEIGHT, ELEV_COORD, ELEV COORD,
ELEV_COORDS, ELEV COORDS, ELEV.

## Station

Any column whose name contains **sta** (case-insensitive). If two station
columns are present, the decimal one is used. Engineer's notation
(100+00.00) is converted to decimal automatically.

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
