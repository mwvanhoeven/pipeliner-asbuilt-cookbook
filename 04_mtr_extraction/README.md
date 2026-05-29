# MTR Data Extraction

*A conversation protocol for any capable AI agent*

Material test reports and inspection certificates arrive from multiple manufacturers, in inconsistent formats, with inconsistent field names. This recipe uses an AI agent to survey what you have before extracting anything — so the output columns match your actual documents rather than a generic template.

---

## What you need

- A folder of MTR PDFs or inspection certificates
- Claude desktop app (Cowork tab) or any capable agent with file access

---

## Starting prompt

Do not customize this prompt before sending. Let the agent tell you what it sees first.

```
I have a folder of PDF documents — material test reports and inspection certificates
from a pipeline project. They come from different manufacturers and some pages may
not have useful data.

I need to pull specific information out of them into a CSV file.

Before you extract anything, look through what I've given you and tell me what types
of documents you see and what information is available. Then let's talk about exactly
what columns I need in the output.
```

---

## What happens next

The agent will inventory the documents and describe what fields are consistently present across manufacturers. From there you decide together what the output columns should be — heat number, yield strength, chemistry, cert number, whatever your project requires.

That conversation produces a second prompt, specific to your document set, which does the actual extraction.

---

> *This recipe is a stub. A worked example with real document types and a complete extraction prompt will be added when available.*

---

*Recipe by [Data Halo](https://data-halo.com) — pipeline survey and asbuilt software.*
