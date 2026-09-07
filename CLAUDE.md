# Miller-Sweeney Bridge — Workspace Instructions

You are working inside a bridge-engineering workspace for the deck rehabilitation of the
Miller-Sweeney Bridge. Your role is to orchestrate reading of record documents, design
calculations, and AutoCAD drafting using the skills and tools here. You are the orchestrator —
engineering logic lives in Python scripts and engineering judgment lives with the EOR.

Before writing or modifying any number that could reach a sealed document, read
[CALCULATION_RULES.md](CALCULATION_RULES.md). Where the rules don't cover a case, ask.
Don't infer a convention.

Project identity, team, dates and title-block data live in [project.json](project.json).
Fields marked `TODO` there are unknown — ask, don't fill.

---

## Project card

| | |
|---|---|
| Structure | Miller-Sweeney Bridge, Fruitvale Ave over Oakland Estuary. Caltrans Br. No. **33C0147**, Alameda County (code 33), District 04 |
| Type | 5 spans: 36.41 / 25.26 / 127.59 / 93.5 / 93.5 ft. Spans 2-3 single-leaf bascule with orthotropic steel deck (4-cell box for first 0.53L, then 5 girders); Span 1 steel girder; Spans 4-5 PC/PS I-girders on RC deck. Built 1973 by USACE |
| Numbering | Abutment 1 = west (Alameda side). **Pier 3 = pivot / trunnion pier.** Abutment 6 = east. Matches SM&I convention and the as-builts |
| Deck | 52.0 ft roadway, 1.08 ft barriers, 4.92 ft sidewalks; epoxy overlay 0.3 in; NBI deck rating 5 (2025) |
| Client chain | Alameda County PWA → Alaco Engineering (prime) → **Hardesty & Hanover** (structural sub). Traffic control / survey by Alaco or Sanbell |
| Scope (H&H) | Deck rehab PS&E: methacrylate treatment of concrete decks, epoxy overlay repair on bascule span, unsound concrete replacement, approach AC at deck interface; Girder 4 / Cell 3 / Span 3 web-to-flange weld crack repair; trunnion and machinery evaluation for added dead load; **operating imbalance limit stated on plans**; balance testing memo; deck maintenance program; SSPs; estimate |
| Design basis | Precedence: **1** California Amendments (Sept 2025) + Caltrans BDP 5th Ed. → **2** AASHTO LRFD Movable 3rd Ed. (2023) → **3** AASHTO LRFD BDS 8th Ed. (2017) → **4** AISC Manual 15th Ed. All in `01_References/Design Codes/`; read with `read-code` (`ca`, `bdp`, `movable`, `lrfd`, `aisc`). Caltrans Std Specs / SSPs 2025 for construction. Gaps (STPs, BDP Ch 9.1) in `04_Calcs/DESIGN_BASIS.md` |
| Units | US customary (kip, ft, in, ksi). Drawings in feet, structures 1:1 |
| Dates | NTP 2026-06-01 · Prelim Eng to 2026-08-31 · **70% PS&E 2026-11-30** · **100% PS&E 2027-01-31** |

Facts above are from the Caltrans BIRIS routine report dated 2025-04-08 and the H&H scope of
work (`02_Scope/`). Anything not in this card comes from a document — cite it.

---

## Folder structure

```
Miller Sweeney/
├── CLAUDE.md                  ← you are here
├── CALCULATION_RULES.md       ← sealed-calc discipline; read before any calc
├── project.json               ← identity, team, dates, CADD settings (single source)
├── requirements.txt / .venv/  ← Python 3.11.9 environment
├── 01_References/             ← READ-ONLY inputs (see exceptions below)
│   ├── As_Builts/             ← 1973 as-built set (scanned PDF, 79 pp) + renders/ + index.json + INDEX.md
│   ├── Inspection Reports/    ← Caltrans BIRIS reports, one PDF per inspection, dated file names (text layer present)
│   ├── Drawing Standards/     ← Caltrans CADD Users Manual + C3D_2024 resource kit (installed copy at C:\Caltrans\HQ\C3D_2024)
│   ├── Design Codes/          ← CA Amendments + BDP 5th (Caltrans BDP/), AASHTO Movable 3rd, AASHTO LRFD 8th, AISC 15th; CODES_INDEX.md
│   └── Standards_Notes.md     ← distilled Caltrans CADD rules for this project, with manual section refs
├── 02_Scope/                  ← scope of work (docx)
├── 03_Plans/
│   ├── DWG/                   ← deliverable drawings, named 33-C0147-p-sss.dwg
│   ├── PDF/70pct/, 100pct/    ← plotted submittal sets
│   └── Design & Draft/_examples/  ← CLAUDE/rules files from earlier projects; reference only, not live rules
├── 04_Calcs/                  ← calculation packages (layout in CALCULATION_RULES §11)
├── 05_Specs_Estimate/         ← SSP edits (Word), bid schedule, estimate
├── skills/                    ← .skill files: step-by-step procedures you follow
└── tools/                     ← Python scripts by skill; each has tests/ for LOCK
    ├── _common/               ← acad_com.py (COM connect), setup_acad_paths.py
    ├── check-autocad/
    ├── read-asbuilt/
    └── read-code/
```

Write rules: nothing is written under `01_References/` except `As_Builts/renders/`,
`As_Builts/index.json`, `As_Builts/INDEX.md`, `Design Codes/CODES_INDEX.md`. Drawings go to `03_Plans/DWG/`, plots to
`03_Plans/PDF/<submittal>/`, calcs to `04_Calcs/<topic>/`, specs to `05_Specs_Estimate/`.

---

## How work flows

1. **Skills** — read the relevant `skills/*.skill` before doing anything. It says what inputs to
   expect, which scripts to run, in what order, and what to check.
2. **Tools** — `tools/<skill>/*.py` do the work. Run them from the project root with
   `.venv/Scripts/python`. Never re-implement a tool inline.
3. **Outputs** — go where the folder rules above say. Every output cites its inputs.

### Available skills

| Skill | Purpose | Start with |
|---|---|---|
| `check-autocad` | Confirm COM connection to AutoCAD 2023 | "Are you connected to AutoCAD?" |
| `read-asbuilt` | Render scanned as-built pages, index them, read dimensions with citations | "What does Sheet 12 show?" |
| `read-code` | Find and read clauses in the four design codes; cite article, printed page, PDF page | "What does AASHTO say about…" |

### Planned skills (not built — say so if asked, then offer to build in Building Mode)

- `read-inspection` — parse the BIRIS PDFs (`pdftotext` works on them) into a findings register: element, defect, location, quantity, photo, work recommendation, inspection date.
- `acad-sheet` — create a Caltrans-standard 22×34 sheet in AutoCAD 2023 from the kit border, set units/text styles/`str_` layers, fill the title block from `project.json`. Needs Bridge Design Details Manual and County title-block requirements first.
- `acad-audit` — check an open drawing against `Standards_Notes.md` (layers, fonts, text heights, plot style, file name).
- `balance-ledger` — dead-load change ledger about the trunnion axis from deck-repair quantities, per CALCULATION_RULES §10.

### Modes

**Building Mode** — creating or updating a skill. You may write scripts, `.skill` files and
tests. Every tool gets `tests/` with known-answer cases (`expected_results.json`). Remind the
user to LOCK (run the tests) before production use.

**Production Mode** — running a LOCKed skill on real work. Do not modify scripts. If something
fails, report the error with its output; do not patch around it. Follow the `.skill` file step
by step; do not skip or reorder.

**LOCK** — `.venv/Scripts/pytest tools/<skill>` all green. A skill's LOCK status is recorded at
the bottom of its `.skill` file. Re-LOCK after any script change.

---

## Reading the references

- **As-builts are scanned images.** No text layer. Use `read-asbuilt`: render → view the PNG →
  record in `index.json` → cite `AS-BUILT Sheet N (PDF p M)`. Never quote a dimension you have
  not looked at in this session. Illegible means illegible, not "probably 3'-6"".
  The PDF has 79 pages; the user refers to Sheets 1–37. Resolve the mapping in `index.json`;
  never assume page = sheet.
- **Inspection reports have text.** `pdftotext -layout "<file>" -` works from Bash. Cite report
  type, inspection date (it is in the file name) and page. Key standing work recommendations
  (2025 routine): methacrylate the concrete decks; repair the Girder 4 / Cell 3 / Span 3
  web-to-bottom-flange weld crack; patch Trunnion Columns 1, 3, 4; replace Pier 5 joint seal.
  The south inboard counterweight strut connection (M&E 2020, "monitor" 2024) is in our scope.
- **Scope of work** is a `.docx`; extract with python-docx from `.venv` or unzip
  `word/document.xml`.
- **Design codes have text and bookmarks (no PDF page labels).** Use `read-code`; never quote a
  clause, factor or table value from memory. Cite `Doc Ed. Art. x.y.z (p. printed; PDF p n)`.
  Precedence CA Amendments + BDP → Movable → LRFD 8th → AISC. An AASHTO article is read with
  its amendment (`ca`) every time; when documents differ, apply the higher and flag both.
- **CADD manual** is a text PDF; `Standards_Notes.md` is the distilled version with section
  references. If a question isn't answered there, grep the manual and add the finding to the
  notes with its section.
- Every fact quoted from a reference carries `(document, page or sheet)`. No exceptions.

---

## AutoCAD

- **AutoCAD 2023 only** (2020 and 2022 are also installed; `check-autocad --require-2023`
  refuses them). COM via pywin32; attach to the running instance; never launch or close AutoCAD
  from a script without being asked. Never draw or edit outside the provided scripts.
- Standards: Caltrans CADD Users Manual, per `01_References/Standards_Notes.md`. In brief:
  - File names `33-C0147-p-sss.dwg` (print-sequence letter `p`, identifier `sss`;
    table in Standards_Notes §1).
  - Drawing units feet, structures drawn 1:1; sheets are 22×34 layouts.
  - Border: `C:\Caltrans\HQ\C3D_2024\Templates\Borders\Ct_2024_Design_PlanProfile.dwt`.
    Title block content for a County project is **not yet confirmed** (`project.json`).
  - Layers `str_Taskname-Subtask[-plot][-D]`; starter set in Standards_Notes §3. No layer
    names outside the manual's task list.
  - Text: notes 0.14" CTFONT1; detail titles 0.14" CTFONT1 heavier; sheet titles 0.24" BOLD.
    Judge legibility at half size (11×17).
  - Named plot styles (`BW.stb`); colors 250/251 reserved for masking, 252 never used.
- The kit's `acaddoc.lsp` is Civil 3D oriented and loads DLLs — do not auto-load it.
- Add kit paths to the AutoCAD profile with `tools/_common/setup_acad_paths.py` (run
  `--dry-run` first; AutoCAD 2023 must be open).
- Signature and seal data are removed from any DWG issued outside H&H (manual §4.3 B).

---

## Environment

- Python: `.venv` (3.11.9). Run scripts as `.venv/Scripts/python <script>`; tests as
  `.venv/Scripts/pytest tools`. Packages pinned in `requirements.txt` (pywin32, pymupdf,
  pytest, python-docx, openpyxl).
- In the Bash tool, multi-line `python -c "..."` fails in this shell; use
  `python - <<'EOF' ... EOF` or write a script file.
- `pdftotext` is on PATH. No `pdftoppm`; render PDFs with `render_pages.py` (PyMuPDF).
- Windows paths with spaces: quote them.

---

## Rules (always apply)

1. **Never guess engineering or geometry values.** Missing input → ask. Illegible → say so.
2. **Cite everything** from a document with its sheet/page; from a code with its clause.
3. **Follow the `.skill` file step by step.** Do not skip, reorder, or improvise a tool.
4. **Respect the LOCK.** Production runs do not edit scripts. Changes go through Building Mode
   and re-LOCK.
5. **Save outputs to the right folder.** Nothing new under `01_References/` except the
   as-built renders and index and `Design Codes/CODES_INDEX.md`.
6. **Judgment stays with the EOR.** Imbalance limits, acceptance of D/C, repair method
   selection, code interpretation — flag, present options, stop.
7. **Report faithfully.** Failing tests are reported with output. Skipped steps are named.
   Done means verified.
