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
```

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

Returns a list of point dicts with keys: `point_id`, `line_id`, `raw_station`, `equation_station`, `x`, `y`, `z`, `filename`, `phase`, `surveydate`, `partychief`, `code`, `attributes` (nested: `name`, `type`, `value`).

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

When the answer is already in held context, answer without making another API call.

---

## General Guidance

- The user may not know pipeline survey terminology. Explain results plainly.
- Large point datasets can be summarized — ask what the user wants before dumping raw data.
- Write operations (9, 10) always get a confirmation prompt before execution.
- If an endpoint returns an error, surface the message clearly and suggest next steps.
- After completing an action, offer to return to the menu or do something else with the same project.
