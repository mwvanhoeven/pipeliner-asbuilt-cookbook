# CSV Pre-Import Cleanup

*A conversation protocol for any capable AI agent*

Point data arrives from everywhere — data collectors, office software,
other surveyors, clients, contractors. The file looks fine in Excel.
It may not be fine. Excel hides things: invisible characters at the start
of the file, empty rows that aren't quite empty, columns with no name
that trail off to the right, duplicate column names that will confuse any
import system, encoding quirks that only surface downstream.

This recipe has the agent look at the file the way an import system looks
at it — before the import system does. It reports what it finds, asks
before fixing anything ambiguous, and returns a clean file only when
you're satisfied. If the file is already clean, it says so and stops
there.

---

## Sample prompt

```
Here is a CSV I'm about to import. Check it for problems before I do.

[attach CSV]
```

Or if you already suspect something:

```
This CSV came from a client. It opens fine in Excel but the import
failed. Can you find what's wrong?

[attach CSV]
```

---

## What the agent checks

### Encoding
The file's character encoding is normalized to UTF-8 without BOM. Excel
defaults to UTF-8 with a byte-order mark — an invisible three-byte
sequence at the start of the file that most import systems handle, but
some don't. Other encoding problems (Windows-1252, Latin-1, mixed
encodings from copy-paste) are detected and converted. Any characters
that don't survive the conversion cleanly are flagged individually.

### Line endings
Mixed or non-standard line endings (Windows CRLF, old Mac CR, mixed
within the same file) are normalized to standard LF.

### Empty rows
Rows where every cell is empty or contains only whitespace are detected
and listed. This includes rows that *look* empty in Excel but contain a
space, a tab, or a formula result of `""`. The agent reports how many
and where, and asks before removing them.

### Empty columns
Columns with no header name are flagged as likely artifacts — the result
of using the Delete key rather than deleting the column properly in Excel.
The agent reports which column positions they occupy and asks before
dropping them. Columns that have a name but no data values are reported
separately; those may be intentional.

### Duplicate column names
If two or more columns share the same name, the agent flags them. This is
a must-confirm before any fix — the user needs to decide which column to
keep, which to drop, or how to rename them. Silently dropping one would
lose data.

### Undesirable characters
The agent scans for characters that commonly cause import failures:
non-breaking spaces (often pasted from web content or PDFs), smart quotes
and curly apostrophes (from Word or email), null bytes, control
characters, and other non-printable characters. Each is reported with the
column and row where it appears. The agent asks before replacing or
removing them, since some may be legitimate — a degree symbol in a
notes field, for example, is probably fine.

### Leading and trailing whitespace in values
Values with leading or trailing spaces look correct in Excel but can cause
mismatch failures on import — `"X70 "` and `"X70"` are not the same
string. The agent reports how many cells are affected and asks before
stripping them.

### Inconsistent row length
If some rows have more or fewer delimited fields than the header, the
agent flags them by row number. This usually means an embedded comma in
an unquoted field, or a field with an embedded newline.

---

## The confirmation step

After the report, the agent lists every proposed fix and asks whether to
apply all of them, skip specific ones, or stop. Nothing is changed without
confirmation.

Some findings are judgment calls. A column named `NOTES` with no values
might be a data gap or a template column the user wants to keep. A
non-breaking space in a comments field might be legitimate. The agent
flags and asks — it does not decide.

---

## What you get

If the file is already clean, the agent says so. No output file is
produced.

If fixes were applied, a cleaned CSV is returned. The default filename
adds a `_clean` suffix (e.g. `sabine_river_clean.csv`). The agent will
use a different name if you ask. The original file is not modified.

The agent also provides a plain-English summary of everything it found and
everything it changed — written for someone who has never opened a file in
a text editor, and doesn't need to.

---

## Troubleshooting

**The import still fails after cleanup** — The problem may be structural
rather than cosmetic: wrong column names, missing required fields, values
outside the expected range. The cleanup recipe checks the file's
condition, not its content against a specific schema. For schema
validation, describe the import format to the agent and ask it to check
the values against those rules.

**The agent flagged something I want to keep** — Skip that fix during the
confirmation step. The agent will apply the others and leave that one
alone.

**The file is large and the scan is slow** — Large CSVs (tens of thousands
of rows) may take a moment to scan fully. The agent will work through it;
no need to split the file first.

---

## Why Excel hides this

Excel renders data for humans, not for import systems. A cell with a
non-breaking space looks empty. A column that extends to XFD because
somebody hit the spacebar in row 1 of column AAA looks like nothing.
Smart quotes look like regular quotes. A BOM at the start of the file is
invisible. None of this is Excel's fault — it's doing its job. But its
job is display, not data integrity, and the gap between those two things
is where import failures live.

The agent reads the raw bytes. That's the difference.

---

*Recipe by [Data Halo](https://datahalo.asbuilt.systems) — pipeline survey and asbuilt software.*
