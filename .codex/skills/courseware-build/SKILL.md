---
name: courseware-build
description: Single-source build pipeline for the WSQ "Application Integration with Docker and Kubernetes" (TGS-2021010366) courseware. One canonical content module (labs_data.py) drives ALL artifacts so they stay 100% aligned — the labs/ folder, the all-white slide deck (PPT), the Lesson Plan (LP), the Learner Guide (LG) and its Markdown mirror. Use to regenerate any courseware after editing course content.
---

# Courseware Build Pipeline (single source of truth)

All course content lives in **`labs_data.py`** (19 labs: 12 Docker + 7 Kubernetes, built
around the **TaskBoard** sample app). Every other artifact is generated from it, so the
slides, labs, Lesson Plan, Learner Guide and Markdown never drift apart.

## Files
| File | Generates |
|---|---|
| `labs_data.py` | **THE source of truth** — 19 labs (metadata + step-by-step `body` blocks + `test`). Edit here. |
| `build_labs.py` | `labs/labNN-*/lab.md` + working files + `labs/README.md` |
| `build_slides.py` + `build_slides_content.py` | `courseware/…​.pptx` — all-white n8n-house-style deck |
| `build_lesson_plan.py` | `courseware/LP-…​.docx` (9:00–6:00, 8 h/day, Day 2 assessment 4:00 PM, lists every lab) |
| `build_learner_guide.py` | `LG-…​.md` (root) **and** `courseware/LG-…​.docx` (step-by-step per lab) |
| `prodoc.py` | shared DOCX helpers (cover, version control, TOC, footer) |

## How to run
From the **repo root** (scripts resolve I/O via `$COURSE_REPO` or the current dir):
```bash
SK=.claude/skills/courseware-build
python3 $SK/build_labs.py
python3 $SK/build_slides.py
python3 $SK/build_lesson_plan.py
python3 $SK/build_learner_guide.py
```
Then convert to PDF with LibreOffice:
```bash
soffice --headless --convert-to pdf --outdir courseware courseware/*.pptx courseware/LP-*.docx courseware/LG-*.docx
```

## Design rules
- **Slides: all-white theme** (blue `#1F6FEB` / teal `#10B981` accents, Arial), reusing the
  `tertiary-course-slides` helpers + its `assets/icons`. Cover with Tertiary + course logos,
  admin front matter, per-topic concept slides, then per lab: overview → command slides → Test it.
- **Lesson Plan**: 2 days, 9:00 AM–6:00 PM, 8 training hours/day (1 h lunch, tea within),
  Day 2 final assessment at 4:00 PM; schedule lists every lab; each day asserts 480 min.
- **Learner Guide**: one section per lab — Goal · What you'll build · Step-by-step · Test it —
  plus setup, troubleshooting and glossary; MD and DOCX emitted from one source.
- **Labs**: realistic, follow the KillerCoda scenarios, built around the TaskBoard app.

To change course content, edit `labs_data.py` and re-run all four generators.
