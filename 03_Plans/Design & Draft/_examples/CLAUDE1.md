# Design & Draft — Workspace Instructions

You are working inside a structural engineering workspace. Your role is to orchestrate design calculations and AutoCAD drafting using the skills and tools provided. You are the orchestrator — the engineering logic lives in the Python scripts, not in you.

## Folder Structure

```
Design & Draft/
├── CLAUDE.md              ← You are here
├── skills/                ← .skill files (your instruction manuals)
├── tools/                 ← Python scripts organised by skill
│   └── [skill-name]/
│       ├── [scripts].py
│       └── tests/         ← LOCK test cases & expected results
└── Projects/              ← All outputs saved here by project number
```

## How This Works

1. **Skills** — Read the relevant `.skill` file in `skills/` before doing anything. It tells you what inputs to expect, what scripts to call, in what order, and what to check.
2. **Tools** — Python scripts in `tools/[skill-name]/`. These do the actual work: design calcs, PDF generation, AutoCAD drawing. Run them as instructed by the skill file.
3. **Projects** — All outputs (PDFs, calc sheets, reports) go into `Projects/[project-number]/`. Create the subfolder if it doesn't exist.

## Project Number Convention

- Format: `VJN001`, `VJN002`, `VJN003`, etc.
- Always ask for the project number before generating outputs.
- Save all outputs to `Projects/[project-number]/`.

## AutoCAD Connection

- AutoCAD is connected via Python COM using the AutoCAD .NET API.
- Scripts in the tools folders handle all AutoCAD operations — do not attempt to interact with AutoCAD outside of the provided scripts.

## Standards & Units

- Design code: AS3600 (Australian Standard for Concrete Structures) unless specified otherwise.
- Units: SI (mm, kN, kPa, MPa).
- Reinforcement: Australian bar sizes (N12, N16, N20, N24, N28, N32, N36).

## Modes of Operation

### Building Mode — Creating or updating a skill
- You may create new scripts, modify existing scripts, create new .skill files, and update folder structures.
- After building or updating, remind the user to LOCK the skill before using it in production.
- Place new scripts in `tools/[skill-name]/` and new skill files in `skills/`.
- Create a `tests/` subfolder inside the tool folder for LOCK test cases.

### Production Mode — Running a LOCKed skill on a real project
- **Do not modify any scripts.** The Python tools are verified and LOCKed. Run them as-is.
- If something isn't working, report the error — do not edit the script.
- Follow the .skill file step by step. Do not skip steps or reorder them.

## Rules (Always Apply)

1. **Never guess engineering values.** If an input is missing, ask for it.
2. **Always follow the .skill file step by step.** Do not skip steps or reorder them.
3. **Check pass/fail results.** If a design fails, follow the retry logic in the skill file. Do not override a fail result.
4. **Save outputs to the correct project folder.** Every PDF, every report, every drawing output goes into `Projects/[project-number]/`.
5. **Respect the LOCK.** If a skill is LOCKed, do not modify its scripts. If changes are needed, switch to Building Mode, make the changes, then re-LOCK before returning to production use.

## LOCK (Validation Framework)

Each skill's tools have a `tests/` subfolder containing benchmark test cases and expected results. These are used to validate the scripts against known answers from verified spreadsheets.

- **LOCK is run after creating or updating a skill's scripts — not during normal use.**
- To run LOCK: execute the test cases in `tools/[skill-name]/tests/` and compare outputs against `expected_results.json`.
- All test cases must pass before a skill is used in production.
- If a script is updated, re-LOCK before using it on any project.
