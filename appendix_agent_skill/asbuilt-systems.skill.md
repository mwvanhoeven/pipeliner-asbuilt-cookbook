---
name: asbuilt-systems
description: Conversational interface to the asbuilt.systems pipeline survey platform via its Python API. Activate immediately when the user types /asbuilt-systems (with or without arguments). Guides the user through authentication, project selection, and available actions — no programming skill required. Use this skill for any request to query asbuilt.systems project data, check progress, retrieve points, download KMZ or shapefiles, upload manifests or DXF sketches, or interact with any asbuilt.systems API endpoint.
---

---

> **Maintainer note:** This skill is also published at `appendix_agent_skill/asbuilt-systems.skill.md` in the pipeliner-asbuilt-cookbook. Keep them in sync.

---

# asbuilt.systems API Skill

This is a generic skill template for any pipeline survey platform running a compatible API. The user supplies their server name at runtime — no pre-configuration required. Cookbook-safe: no proprietary server names or client information.

This skill gives the user a conversational interface to their asbuilt.systems instance. The user never needs to write code — the agent runs the API calls on their behalf.

## Knowledge Base

Before doing anything else, fetch these three documents and hold them for the session. They are the authoritative source on what this platform is, what its pages do, and why it was built. Use them to answer product questions without making API calls.

```python
import requests
MASTER = requests.get('https://<server_name>/kb/H0l6r88r26gk_sCZyckPylugb4fPqZKFK542l-SugUhnfLxXXwTedw/').text
PAGES  = requests.get('https://<server_name>/kb/-LYCgS6cB4UNzvyQhMWhy9neyoVVpMXTqPZSpw9WAAWY0Hr3sfXo5g/').text
WHY    = requests.get('https://<server_name>/kb/uw60HN18S_xTBFIAd8iE7mA3W74oNUnySr93wIuYd1JAYAt6p7xOgA/').text
```

- `MASTER.md` — canonical context: product, architecture, clients, ecosystem
- `PAGES.md` — every page and what it does; includes the METRIC_PROJECTIONS list used to derive `must_scale`
- `WHY.md` — the philosophical grounding; why the product exists and what it refuses to become

Do not announce this fetch to the user.

## Entry Point

On `/asbuilt-systems`, do this in order:

1. Greet briefly. Ask for the server name — the subdomain or full host (e.g. `datahalo.asbuilt.systems`). Hold this as `server_name` for the session. All endpoints are constructed as `https://{server_name}/path/`.
2. Ask for username.
3. Ask for password. Never store or display it after receipt.
4. Call the **Project List** endpoint and present results as a numbered list: project title, client, alias.

```python
import requests
data = {
    'username': '<username>',
    'password': '<password>'
}
response = requests.post('https://<server_name>/project/json-active-project-list/', data=data)
projects = response.json()
```

Staff credentials return all active projects. User credentials return only assigned projects.

5. Ask the user to pick a project.
6. Present the **Available Actions** menu for that project (see below).

---

## Project Context Load (silent, on project selection)

Immediately after the user selects a project, silently fetch and hold:

**From the project list response** (already in hand — no extra call needed):
- `primary_weld` — authoritative weld code for this project (e.g. `WLD`, `WELD`)
- `loose_end` — authoritative loose end code
- `line_ids` — list of all line IDs on this project; if more than one, this is a multi-line project
- `epsg` — coordinate system
- `utms_are_usft` — whether survey foot units apply
- `code_xref`, `linework_xref`, `manifest_xref` — if set, this project inherits rules from another alias; note this to the user if they ask why code rules or sketches look different
- `project_admin`, `project_manager`, `lead_tech` — for context
- `bbox` — bounding box if spatial context is needed

Derive and hold:
- `must_scale` — True if `utms_are_usft` is True AND `epsg` appears in the METRIC_PROJECTIONS list in the held PAGES.md. When True, raw coordinates are stored in US survey feet despite a metric EPSG — flag this to the user any time coordinates are returned.

**Code rules** — fetch once, hold for the session:

```python
import requests
data = {
    'username': '<username>',
    'password': '<password>',
    'project_alias': '<alias>'
}
response = requests.post('https://<server_name>/code/json-code-rules/', data=data)
code_rules = response.json()
```

From code rules, derive and hold:
- `on_line_codes` — list of codes where `on_line == True`
- Full code lookup by code string for answering "what is X?" questions

Use `primary_weld` and `loose_end` from the project object directly — do not guess weld codes from naming patterns.

Do not announce this fetch to the user. Present the action menu immediately after.

---

## Available Actions Menu

After project selection, present this menu:

```
What would you like to do?

Read
  1. Progress summary
  2. Point data
  3. Line geometry
  4. File list
  5. Code rules

Download
  6. KMZ
  7. Shapefile — Points
  8. Shapefile — Joints

Write
  9. Upload manifest (CSV or XLSX)
 10. Upload DXF sketch

QC
 11. Ahead-back joint continuity
 12. Tie Ins (stacked duplicate points)
 13. Manifests (tally vs survey reconciliation)
 14. On Joint (joint attribute inheritance)
 15. Dupe Atts (non-unique attribute values)
 16. Begin-End (alternating marker continuity)
 17. Validation (attributes vs code-rule dictionary)
```

> **QC note:** Actions 11–17 are the agent-facing half of the dashboard's seven QC badges (Ahead-Back / Tie Ins / Manifests / On Joint / Dupe Atts / Begin-End / Validation). Each feed reads the same auth-blind assessment its page and XLSX export read — the badge count and the feed count are always the same source. A combined XLSX report is also available as a human download but is not a separate API.

Wait for the user's choice, then execute the corresponding action below.

---

## Actions

### 1. Progress Summary

If `line_ids` has more than one entry, fetch progress for all lines without asking — loop and present a full report. If only `primary` exists, fetch once with no `line_id` param.

```python
import requests
for line_id in line_ids:
    data = {
        'username': '<username>',
        'password': '<password>',
        'project_alias': '<alias>',
        'line_id': line_id
    }
    response = requests.post('https://<server_name>/progress/json-progress/', data=data)
    result = response.json()
```

Present as a table: line, baseline length, covered, percentage. Note lines with zero coverage. Note if lines share a baseline length (likely alignment placeholders).

---

### 2. Point Data

```python
import requests
data = {
    'username': '<username>',
    'password': '<password>',
    'project_alias': '<alias>'
}
response = requests.post('https://<server_name>/points/json-points/', data=data)
result = response.json()
```

Returns a list of point dicts with keys: `point_id`, `line_id`, `raw_station`, `equation_station`, `x`, `y`, `z`, `latitude`, `longitude`, `filename`, `phase`, `surveydate`, `partychief`, `code`, `attributes` (nested: `name`, `type`, `value`).

Use held code context to answer intelligently:
- "How many weld points?" → count points where `code == primary_weld` (from project object)
- "How many on-line points?" → count points where `code` is in `on_line_codes`
- "What is a BND?" → look up in held code rules
- Filter by phase, party chief, date, or code on request
- Summarize by code, phase, or file rather than dumping raw data unless asked
- If `must_scale` is True, note that coordinates are in US survey feet

---

### 3. Line Geometry

```python
import requests
data = {
    'username': '<username>',
    'password': '<password>',
    'project_alias': '<alias>'
}
response = requests.post('https://<server_name>/points/json-lines/', data=data)
result = response.json()
```

Optional: ask for `line_id` (default: primary).

Returns nested list of coordinate pairs: `[[[x,y,z],[x,y,z]], ...]`. Summarize segment count and coordinate range unless the user asks for raw data. If `must_scale` is True, note that coordinates are in US survey feet.

---

### 4. File List

```python
import requests
data = {
    'username': '<username>',
    'password': '<password>',
    'project_alias': '<alias>'
}
response = requests.post('https://<server_name>/points/json-file-list/', data=data)
result = response.json()
```

Returns list of dicts: `filename`, `partychief`, `surveydate` (yyyy-mm-dd), `phase`, `username`. Present as a table or summary. Can filter by date, party chief, or phase on request.

> **Note:** The file list is a census — one record per unique filename across all points. It is not a log of import events and carries no upload timestamp. Think of it as a point group index, not a history.

---

### 5. Code Rules

```python
import requests
data = {
    'username': '<username>',
    'password': '<password>',
    'project_alias': '<alias>'
}
response = requests.post('https://<server_name>/code/json-code-rules/', data=data)
result = response.json()
```

Returns list of dicts: `code`, `feature_name`, `on_line` (bool), `attributes` (nested: `code`, `name`, `number`, `validation_type`, `required`, `menu_items`). Summarize or answer specific questions about code definitions.

---

### 6. KMZ Download

Ask for a destination path before proceeding.

Optionally ask which popup metadata fields to include: `phase`, `filename`, `uploaded_by`, `survey_date`, `party_chief`, `station`. Also available: `marker_point_id`, `station_markers`, `sketches`, `yesterday`.

```python
import requests, re
destination_path = '<prompted>'
data = {
    'username': '<username>',
    'password': '<password>',
    'project_alias': '<alias>'
    # add any True options here
}
r = requests.post('https://<server_name>/kmz/remote-kmz/', data=data)
d = r.headers['content-disposition']
fname = re.findall("filename=(.+)", d)[0]
with open(destination_path + fname, 'wb') as f:
    f.write(r.content)
```

Confirm filename and path after save.

---

### 7. Shapefile — Points

Ask for destination path. Optionally ask which columns to include: `raw_station`, `equation_station`, `offset`, `northing_easting`, `elevation`, `code`, `lat_long`, `phase`, `survey_date`, `party_chief`, `dh_comment`, `detailed_filenames`, `line_id`.

```python
import requests, re
destination_path = '<prompted>'
data = {
    'username': '<username>',
    'password': '<password>',
    'project_alias': '<alias>'
    # add any True column options here
}
r = requests.post('https://<server_name>/points/remote-shp-points/', data=data)
d = r.headers['content-disposition']
fname = re.findall("filename=(.+)", d)[0]
with open(destination_path + fname, 'wb') as f:
    f.write(r.content)
```

---

### 8. Shapefile — Joints

Ask for destination path. Optional: `line_id` (default: primary).

> **Note on `line_id`:** On multi-line projects, the endpoint defaults to `primary`. If `primary` has no coverage, the response will be an error file rather than a shapefile. Always prompt for `line_id` on multi-line projects.

**Key field: `LENGTH_3D`**

The DBF includes a `LENGTH_3D` column — the 3D surveyed length of each joint (weld-to-weld span). This is computed from the on-line geometry between welds, including any intervening on-line events such as bends. It is not a straight-line distance and is not derived from station math. Summing `LENGTH_3D` grouped by attributes such as `OD`, `GRADE`, or `CI_WALL` produces a material takeoff directly from the asbuilt. This is the primary use case for the joints shapefile.

```python
import requests, re
destination_path = '<prompted>'
data = {
    'username': '<username>',
    'password': '<password>',
    'project_alias': '<alias>'
}
r = requests.post('https://<server_name>/points/remote-shp-joints/', data=data)
d = r.headers['content-disposition']
fname = re.findall("filename=(.+)", d)[0]
with open(destination_path + fname, 'wb') as f:
    f.write(r.content)
```

---

### 9. Upload Manifest

**Confirm before proceeding — this writes to the project.**

Ask for the full path to the CSV or XLSX file.

```python
import requests
path_and_filename = '<prompted>'
data = {
    'username': '<username>',
    'password': '<password>',
    'project_alias': '<alias>'
}
with open(path_and_filename, 'rb') as f:
    r = requests.post('https://<server_name>/manifests/remote-update-manifest/', files={'file': f}, data=data)
```

Report success or surface `r.text` on failure.

---

### 10. Upload DXF Sketch

**Confirm before proceeding — this writes to the project.**

Ask for the full path to the DXF file. Ask if the file's EPSG differs from the project setting (optional `epsg` param).

```python
import requests
path_and_filename = '<prompted>'
data = {
    'username': '<username>',
    'password': '<password>',
    'project_alias': '<alias>'
    # 'epsg': <if different from project>
}
with open(path_and_filename, 'rb') as f:
    r = requests.post('https://<server_name>/sketch/remote-dxf-sketch-update/', files={'file': f}, data=data)
```

Report success or surface `r.text` on failure.

---

### 11. Ahead-Back Joint Continuity

*Checks whether weld attributes agree across joints — every weld's "ahead" value must match the next weld's "back" value on the same line. Mismatches are busts.*

```python
import requests
data = {
    'username': '<username>',
    'password': '<password>',
    'project_alias': '<alias>'
}
response = requests.post('https://<server_name>/ahead-back/json/', data=data)
result = response.json()
```

Auth: staff OR Assignment membership on the project. A sandboxed Contributor pull returns only their own welds.

**Response shape:**

```
{
  "summary": {
    "project_alias": str,
    "primary_weld": str,
    "is_clean": bool,
    "has_primary_weld": bool,
    "has_welds": bool,
    "bustcount": int,        # project-wide badge; single-weld isolated busts count here
    "pairs": [{"ahead": str, "back": str}, ...],
    "ignored_values": [str, ...]
  },
  "busts": [
    {
      "line_id": str,
      "stretch": int,        # 1-based adjacency group on the line
      "station": str,
      "point_id": int,
      "owner": str,
      "attributes": [{"name": str, "value": str, "busted": bool}]
    },
    ...
  ]
}
```

**Interpreting the response:**

- `is_clean` — True if `bustcount` is zero. Lead with this.
- `bustcount` — project-wide count. Single-weld isolated busts (a weld with no valid neighbor) count toward this total but are **not** listed in `busts` — they cannot form a stretch.
- `busts` — flat list of busted welds that belong to a stretch of two or more consecutive mismatches. Each weld's `attributes` list contains every tracked attribute; `busted: true` marks which one(s) disagreed.
- `stretch` — adjacency group number (1-based, per line). Welds sharing the same `line_id` and `stretch` value are consecutive busts — present them together.
- `pairs` — the attribute pairs that were checked (e.g. `[{"ahead": "HEAT_AHEAD", "back": "HEAT_BACK"}]`). Useful for explaining to the user what the check covers.
- `ignored_values` — strings excluded from comparison by exact match or prefix. A value is skipped if it equals an entry in this list, or if it begins with one (e.g. `"FAB"` suppresses `"FAB-001"`, `"FAB-123"`, and any other value starting with `"FAB"`). If a weld isn't flagged and the user expects it to be, check whether its value matches an ignored prefix.

**Presenting results:**

If `is_clean` is True: confirm the project is clean and state the weld count from the badge.

If busts exist, group by `line_id`, then by `stretch`. For each stretch, list the busted welds in order with their station and which attributes are flagged. Explain that consecutive busts form a stretch because each weld is both the "back" of the prior and the "ahead" of the next — a single bad entry can flag two welds at once.

> **Note:** The recipe in `05_ahead_back_check/` walks the same check from a CSV export using a spreadsheet-based workflow. This endpoint pulls the live platform assessment directly — same logic, no export required.

---

### 12. Tie Ins (Stacked Duplicate Points)

*Checks for spatially-coincident stacked points — two or more points that occupy the same location on the same line. Common cause: duplicate imports or field re-shots not cleaned up.*

```python
import requests
data = {
    'username': '<username>',
    'password': '<password>',
    'project_alias': '<alias>'
}
response = requests.post('https://<server_name>/clusters/json/', data=data)
result = response.json()
```

Auth: staff OR Assignment membership on the project. A sandboxed Contributor pull returns only clusters involving their own points.

**Response shape:**

```
{
  "summary": {
    "project_alias": str,
    "is_clean": bool,
    "has_online_points": bool,
    "bustcount": int,
    "justified_count": int,
    "ignored_codes": [str, ...]
  },
  "busts": [
    {
      "line_id": str,
      "code": str,
      "le_over_weld": bool,
      "atts_same": bool,
      "inverse_distance": float,
      "tolerance": float,
      "points": [
        {
          "point_id": int,
          "owner": str,
          "station": str,
          "party_chief": str,
          "survey_date": str
        },
        ...   # 2-element list, one per stacked point
      ]
    },
    ...
  ]
}
```

**Interpreting the response:**

- `is_clean` — True if `bustcount` is zero. Lead with this.
- `bustcount` — project-wide badge count.
- `justified_count` — clusters that have been reviewed and marked as intentional; these are not in `busts`.
- `ignored_codes` — codes excluded from the check entirely (e.g. reference marks that are legitimately stacked).
- Each bust represents one cluster pair. `le_over_weld` flags a loose end stacked on a weld (a common legitimate pattern — worth noting to the user). `atts_same` indicates whether the two points' attributes are identical (a stronger signal that the second is a duplicate import). `inverse_distance` and `tolerance` are the spatial proximity values used by the check.
- `points` is always a 2-element list: the two stacked points. Present both with station and owner so the user can identify which to remove.

**Presenting results:**

If `is_clean`: confirm clean and note `justified_count` if nonzero (so the user knows some clusters exist but have been reviewed).

If busts exist, group by `line_id` and `code`. For each cluster, show both points' station, owner, and survey date. Flag `le_over_weld` clusters separately — those may be intentional and worth a second look before deleting.

---

### 13. Manifests (Tally vs Survey Reconciliation)

*Reconciles the survey record against the material tally — checks that every pipe joint in the manifest appears in the asbuilt, and vice versa.*

```python
import requests
data = {
    'username': '<username>',
    'password': '<password>',
    'project_alias': '<alias>'
}
response = requests.post('https://<server_name>/manifests/qc-json/', data=data)
result = response.json()
```

Auth: staff OR Assignment membership on the project.

**Response shape:**

```
{
  "summary": {
    "project_alias": str,
    "is_clean": bool,
    "has_queries": bool,
    "bustcount": int,
    "total_matched": int,
    "total_missing": int,
    "warnings": [str, ...]
  },
  "queries": [
    {
      "owner": str,
      "line_id": str,
      "code": str,
      "inventory": str,
      "is_manifest_vs_manifest": bool,
      "point_join": str,
      "point_match": str,
      "inventory_join": str,
      "inventory_match": str,
      "tolerance": float,
      "matched": int,
      "busted": int,
      "missing": int,
      "is_current": bool
    },
    ...
  ]
}
```

**Interpreting the response:**

- `is_clean` — True if `bustcount` is zero. Lead with this.
- `bustcount` — total reconciliation failures across all queries.
- `total_matched` / `total_missing` — aggregate counts across all queries.
- `warnings` — non-fatal issues surfaced by the check (e.g. a manifest uploaded with no matching points yet).
- Each query represents one reconciliation rule. `point_join` / `point_match` are the survey-side attribute fields; `inventory_join` / `inventory_match` are the manifest-side fields. `is_manifest_vs_manifest` flags rules that compare two manifest columns rather than manifest vs. points. `is_current` indicates whether the query's manifest data is up to date.

**Presenting results:**

If `is_clean`: confirm clean, note matched count and any warnings.

If busts exist, group by `line_id` and `code`. For each query with failures, report the join fields being compared, the matched/missing counts, and any warnings. If `is_manifest_vs_manifest` is True, note that this query compares manifest to manifest rather than manifest to survey.

---

### 14. On Joint (Joint Attribute Inheritance)

*Checks that features immediately following a weld carry the weld's attribute values — the "on joint" rule requires inheritance from the weld behind the feature.*

```python
import requests
data = {
    'username': '<username>',
    'password': '<password>',
    'project_alias': '<alias>'
}
response = requests.post('https://<server_name>/on-joint/json/', data=data)
result = response.json()
```

Auth: staff OR Assignment membership on the project. A sandboxed Contributor pull returns only busts involving their own points.

**Response shape:**

```
{
  "summary": {
    "project_alias": str,
    "primary_weld": str,
    "is_clean": bool,
    "has_alignment": bool,
    "has_defs": bool,
    "bustcount": int,
    "warnings": [str, ...]
  },
  "defs": [
    {
      "line_id": str,
      "code": str,
      "attribute": str,
      "weld_att": str,
      "bustcount": int,
      "busts": [
        {
          "feature_point_id": int,
          "feature_value": str,
          "feature_owner": str,
          "station": str,
          "weld_point_id": int,
          "weld_value": str
        },
        ...
      ]
    },
    ...
  ]
}
```

**Interpreting the response:**

- `is_clean` — True if `bustcount` is zero. Lead with this.
- `has_alignment` — whether the project has alignment data (required for on-joint checks).
- `has_defs` — whether any on-joint rules are defined for this project.
- Each def represents one inheritance rule: `attribute` on code `code` must match `weld_att` on the preceding weld. `bustcount` is the per-def count.
- Each bust shows the feature point and the weld it should have inherited from, with both values so the user can see the discrepancy.

**Presenting results:**

If `is_clean`: confirm clean. Note if `has_defs` is False (no rules configured — clean means unchecked).

If busts exist, group by `line_id`, then by def. For each bust, show the feature station, the mismatched attribute, the feature's actual value, and the weld value it should carry. Explain the inheritance direction: the feature must echo the weld behind it, not ahead of it.

---

### 15. Dupe Atts (Non-Unique Attribute Values)

*Checks for attribute values that appear on more than one point when they should be unique — distinct from Tie Ins (action 12), which checks location. This check is about value uniqueness, not spatial position.*

```python
import requests
data = {
    'username': '<username>',
    'password': '<password>',
    'project_alias': '<alias>'
}
response = requests.post('https://<server_name>/duplicates/json/', data=data)
result = response.json()
```

Auth: staff OR Assignment membership on the project. A sandboxed Contributor pull returns only clusters involving their own points.

**Response shape:**

```
{
  "summary": {
    "project_alias": str,
    "is_clean": bool,
    "has_defs": bool,
    "bustcount": int
  },
  "defs": [
    {
      "line_id": str,          # 'All' when the rule is project-wide
      "code": str,
      "attribute": str,
      "bustcount": int,
      "ignored_values": [str, ...],
      "clusters": [
        {
          "value": str,
          "count": int,
          "points": [
            {
              "point_id": int,
              "station": str,
              "joint_length": str,
              "owner": str
            },
            ...
          ]
        },
        ...
      ]
    },
    ...
  ]
}
```

**Interpreting the response:**

- `is_clean` — True if `bustcount` is zero. Lead with this.
- `has_defs` — whether any uniqueness rules are defined. If False, clean means unchecked.
- `line_id` of `'All'` means the rule applies across all lines on the project, not just one.
- `ignored_values` — values excluded from the uniqueness check for this def (e.g. a placeholder value that is legitimately reused).
- Each cluster groups all points sharing the same duplicate value. `count` is the number of points. Present `value`, `count`, and the point list (point_id, station, owner) so the user can identify which entries to correct.

**Presenting results:**

If `is_clean`: confirm clean. Note if `has_defs` is False.

If busts exist, group by `line_id` and `attribute`. For each cluster, show the repeated value, how many points carry it, and the point list. Note `ignored_values` if the user asks why a value they expected to see flagged is not present.

---

### 16. Begin-End (Alternating Marker Continuity)

*Checks that begin/end markers alternate correctly — a begin must be followed by an end before the next begin, and vice versa. Consecutive same-value markers are busts.*

```python
import requests
data = {
    'username': '<username>',
    'password': '<password>',
    'project_alias': '<alias>'
}
response = requests.post('https://<server_name>/begin-end/json/', data=data)
result = response.json()
```

Auth: staff OR Assignment membership on the project. A sandboxed Contributor pull returns only busts involving their own points.

**Response shape:**

```
{
  "summary": {
    "project_alias": str,
    "is_clean": bool,
    "has_defs": bool,
    "bustcount": int
  },
  "defs": [
    {
      "line_id": str,
      "code": str,
      "attribute": str,
      "bustcount": int,
      "busts": [
        {
          "value": str,
          "count": int,
          "points": [
            {
              "point_id": int,
              "station": str,
              "owner": str
            },
            ...
          ]
        },
        ...
      ]
    },
    ...
  ]
}
```

**Interpreting the response:**

- `is_clean` — True if `bustcount` is zero. Lead with this.
- `has_defs` — whether any begin-end rules are defined. If False, clean means unchecked.
- `bustcount` counts adjacent-equal **pairs**. A run of N consecutive same-value points = N−1 pairs. So a run of 3 "BEGIN" markers counts as 2 busts, not 3.
- Each bust represents a **run** of consecutive same-value markers. `value` is the repeated marker value (e.g. `"BEGIN"`). `count` is the number of consecutive points. `points` lists them in order with station and owner.
- This feed shows only the doubled-up runs — the clean alternating pairs are not listed. The platform's page shows every feature with busts flagged inline; this feed gives only the actionable failures.

**Presenting results:**

If `is_clean`: confirm clean. Note if `has_defs` is False.

If busts exist, group by `line_id` and `code`. For each run, show the repeated value, how many consecutive points are involved, and the station range. Explain that each adjacent pair in the run counts as one bust — a run of 3 is 2 busts.

---

### 17. Validation (Attributes vs Code-Rule Dictionary)

*Checks every point's attributes against the code-rule dictionary — flags values that don't match a menu item, attributes that aren't defined for the code, missing required attributes, and points with too many attributes.*

```python
import requests
data = {
    'username': '<username>',
    'password': '<password>',
    'project_alias': '<alias>'
}
response = requests.post('https://<server_name>/code/json-validation/', data=data)
result = response.json()
```

Auth: staff OR Assignment membership on the project. A sandboxed Contributor pull returns only busts involving their own points.

**Response shape:**

```
{
  "summary": {
    "project_alias": str,
    "is_clean": bool,
    "has_busts": bool,
    "bustcount": int
  },
  "busts": [
    {
      "code": str,
      "point_id": int,
      "owner": str,
      "att_number": str,   # blank for point-level busts
      "att_name": str,     # blank for point-level busts
      "att_value": str,    # blank for point-level busts
      "menu_bust": bool,
      "issue": str
    },
    ...
  ]
}
```

**Interpreting the response:**

- `is_clean` — True if `bustcount` is zero. Lead with this.
- `has_busts` mirrors `not is_clean`; use `is_clean` as the primary flag.
- `bustcount` — total attribute violations across the project.
- Each bust is a single attribute violation. The `att_*` fields identify which attribute is at fault. When `att_number`, `att_name`, and `att_value` are all blank, the bust is **point-level** — the point itself has too many attributes or is missing its Line ID.
- `menu_bust` — True when the value is not among the allowed menu items for that attribute.
- `issue` — a human-readable description of the rule that was broken (e.g. "Value not in menu", "Required attribute missing", "Unknown attribute for this code").

**Presenting results:**

If `is_clean`: confirm clean and state the bustcount (zero).

If busts exist, group by `code`, then by `issue` type. For each group, list the affected point IDs, owners, and attribute details. Separate point-level busts (blank `att_*` fields) from attribute-level busts — they require different corrective actions. Note `menu_bust` busts specifically; these are often typos or legacy values that need updating to current menu items.

---

## Natural Language Routing

The user may not pick from the menu — they may just ask a question. Route intelligently:

- "How far along is the project?" / "What's the progress?" → Action 1, fetch all lines automatically
- "How many points?" / "How many welds?" → Action 2, use `primary_weld` from project object
- "What files have been imported?" / "Who surveyed last week?" → Action 4
- "What does code X mean?" → answer from held code rules, no API call needed
- "Download a KMZ" → Action 6, ask for destination
- "What's the EPSG?" / "Is this metric?" → answer from held project settings, no API call needed
- "What lines does this project have?" → answer from `line_ids`, no API call needed
- "Does this project scale?" → derive from `must_scale`, no API call needed
- "Are there any ahead-back busts?" / "Is the ahead-back clean?" / "Check joint continuity" → Action 11
- "How many ahead-back busts?" / "Show me the ahead-back issues" → Action 11, surface `bustcount` and `busts`
- "Any stacked points?" / "Check tie ins" / "Are there duplicate locations?" → Action 12
- "Check manifests" / "Is the tally reconciled?" / "Any manifest mismatches?" → Action 13
- "Check on-joint" / "Are the joint attributes inherited correctly?" → Action 14
- "Any duplicate attribute values?" / "Check dupe atts" → Action 15
- "Check begin-end" / "Are the alternating markers correct?" / "Any begin-end issues?" → Action 16
- "Validate attributes" / "Any code violations?" / "Check validation" → Action 17
- "How many QC busts?" / "What's the QC status?" → run all seven QC feeds (11–17) and present a summary table: badge name, bustcount, is_clean

When the answer is already in held context, answer without making another API call.

---

## General Guidance

- The user may not know pipeline survey terminology. Explain results plainly.
- Large point datasets can be summarized — ask what the user wants before dumping raw data.
- Write operations (9, 10) always get a confirmation prompt before execution.
- If an endpoint returns an error, surface the message clearly and suggest next steps.
- After completing an action, offer to return to the menu or do something else with the same project.
