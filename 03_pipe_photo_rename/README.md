# Pipe Photo Rename

*A workflow guide for field photo batches*

Instead of renaming photos by hand, you paste a prompt into Claude and it reads the identifier written on each pipe — then renames every file automatically. No programming required.

---

## What you need

- Claude desktop app for Windows — [claude.ai/download](https://claude.ai/download)
- A folder of pipe photos copied to your Desktop
- The prompt below, customized for your job's marker format

---

## Steps

|       |                                                              |
| ----- | ------------------------------------------------------------ |
| **1** | **Copy your photos to a new Desktop folder.** Do not work in the original folder. Make a copy first — e.g., "Batch 47 Pipes" on your Desktop. |
| **2** | **Open Claude and click the Cowork tab.** Cowork is the tab that lets Claude work with files on your computer. |
| **3** | **Select your folder.** Click the folder icon and point Claude to the batch folder you just created. |
| **4** | **Paste the prompt and hit Enter.** Copy the prompt below, fill in the two bracketed parts, paste it into Claude, and send. |
| **5** | **Review and confirm.** Claude will show you what it plans to rename. Confirm, and it renames all files in one step. |

---

## The prompt

*Copy this exactly. Fill in the two bracketed sections before sending.*

```
I have a folder of pipe photos. Each pipe has an identifier written in [COLOR] marker.
The identifier format is: [DESCRIBE FORMAT]

Please look at each photo in this folder and rename it to match the pipe identifier
visible on the pipe (keep the .jpg extension). For example, a photo showing pipe
B-ML-058 should become B-ML-058.jpg.

If you cannot clearly read the identifier in a photo, leave that file unchanged and
tell me which ones you skipped.
```

**How to fill in the brackets:**

`[COLOR]` → the color of the marker used (e.g., blue, black, white)

`[DESCRIBE FORMAT]` → describe what the ID looks like on this job. Example: *"three letters, a hyphen, and a three-digit number — like B-ML-058"*

---

## Tips

**Always work on a copy.** Never point Claude at your original photo archive.

**Skipped files are fine.** If a photo is blurry or the identifier is hidden, Claude tells you which ones it skipped so you can handle them manually.

**One batch at a time.** Keep each job's photos in their own folder before you start.

---

*Recipe by [Data Halo](https://data-halo.com) — pipeline survey and asbuilt software.*
