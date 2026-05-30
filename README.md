# Pipeliner Asbuilt Cookbook

Practical AI agent recipes for pipeline asbuilt work.

Each recipe is a conversation protocol: what to tell the agent, in what order, what to expect back, and what to watch for. No programming required. Any capable AI agent with file access and code execution will work — Claude, ChatGPT, or similar.

The recipes are written for people doing the work — surveyors, field engineers, data managers. They assume you know what a bore log is, what a weld tally looks like, and why the anchor step matters. They do not assume you know how to code.

---

## Recipes

| #  | Recipe | What it produces |
|----|--------|-----------------|
| 01 | [HDD Drill Report to 3D Polyline](01_hdd_drill_to_dxf/) | A 3D DXF polyline from a driller's away/elevation/lateral table — ready to anchor in CAD |
| 02 | [Weld Position Calculator](02_weld_positions/) | A CSV of calculated weld coordinates, pushed along an anchored bore polyline using joint lengths |
| 03 | [Pipe Photo Rename](03_pipe_photo_rename/) | A renamed photo batch — Claude reads the identifier written on each pipe and renames the file |
| 04 | [MTR Data Extraction](04_mtr_extraction/) | Structured data pulled from material test reports and inspection certificates into a CSV |
| 05 | [Ahead-Back Diagonal Check](05_ahead_back_check/) | An Excel workbook that flags heat, joint, and attribute mismatches across adjacent welds |
| 06 | [Material Transition Finder](06_material_transitions/) | A CSV of transition points where pipe spec changes, ready to import or patch into your project |
| 07 | [FXL Builder](07_fxl_builder/) | A Trimble field coding file built from a point file, a spreadsheet, or a guided conversation |
| 08 | [CSV Pre-Import Cleanup](08_csv_cleanup/) | A cleaned CSV with a plain-English report of everything Excel was hiding |
| 09 | [Wrong-Way Elbow Detector](09_wrong_way_elbow/) | A marked DXF with flagged vertices where the pipeline bends against its own trend |

Recipes 01 and 02 are designed to run in sequence — 01 produces the DXF that 02 consumes.

---

## Supporting documents

- [REFERENCE.md](REFERENCE.md) — column name recognition lists used across recipes. If a recipe says "the agent recognizes these column names," the full list is here.
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to add a recipe. Reviews are done by a human and an agent together.

---

*Recipes by [Data Halo](https://datahalo.asbuilt.systems) — pipeline survey and asbuilt software.*
