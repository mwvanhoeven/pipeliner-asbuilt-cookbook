# Pipeliner Asbuilt Cookbook

Practical AI agent recipes for pipeline asbuilt work.

Each recipe is a prompt template. Paste the chapter URL into Claude or ChatGPT and ask it to follow the recipe — the agent can read the full chapter and navigate to supporting documents from there. If your agent can't fetch URLs, copy the sample prompt directly from the chapter, attach the file it asks for, and follow the conversation. No programming required.

The recipes are written for people doing the work — surveyors, field engineers, data managers. They assume you know what a bore log is, what a weld tally looks like, and why the anchor step matters. They do not assume you know how to code. Any capable AI agent with file access and code execution will work — Claude, ChatGPT, or similar.

---

## Working with Your Agent

You don't need to know how GitHub works to get value from this cookbook. Your agent does.

### What your agent is

If you've been using your agent mostly to look things up or rewrite emails, there's more available. An agent can *try things*, remember what happened, notice patterns, and act on your behalf. The cookbook is designed to be worked by agents — not just read by people.

### What to tell your agent

Plain language works:

- "Try the station naming recipe and tell me what happened."
- "Something in chapter 4 didn't work — can you flag it?"
- "We figured out a better way to handle X — can you share it with the cookbook."
- "What's been added or changed in the cookbook recently?"

Your agent knows what to do with these. You don't need to learn GitHub to make them happen.

### What your agent can do here

- Try recipes against your actual data and report results
- Flag something broken or confusing so it can be fixed
- Submit a variation that worked better for your situation
- Check for updates since you last visited
- Contribute a win your team figured out

The cookbook gets better every time an agent reports back. Yours can be part of that.

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
| 10 | [Alignment Deflection Report](10_deflection_report/) | An Excel workbook of deflection angles at each alignment vertex, ready to hand to the field crew |

Recipes 01 and 02 are designed to run in sequence — 01 produces the DXF that 02 consumes.

---

## Supporting documents

- [REFERENCE.md](REFERENCE.md) — column name recognition lists used across recipes. If a recipe says "the agent recognizes these column names," the full list is here.
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to add a recipe. Reviews are done by a human and an agent together.

---

*Recipes by [Data Halo](https://datahalo.asbuilt.systems) — pipeline survey and asbuilt software.*
