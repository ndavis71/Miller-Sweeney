# Miller-Sweeney Bridge — Deck Rehabilitation (H&H)

Workspace for Hardesty & Hanover's structural scope on the Alameda County Miller-Sweeney
Bridge deck rehabilitation (Caltrans Br. No. 33C0147). Record-document reading, calculations,
and AutoCAD 2023 drafting to Caltrans CADD standards.

- [CLAUDE.md](CLAUDE.md) — how this workspace works: folders, skills, AutoCAD and reading rules.
- [CALCULATION_RULES.md](CALCULATION_RULES.md) — sealed-calculation discipline.
- [project.json](project.json) — project identity, team, dates, CADD settings.
- [01_References/Standards_Notes.md](01_References/Standards_Notes.md) — Caltrans CADD rules distilled.

## Quick start

```powershell
# one-time
"C:\Users\ndavis\.pyenv\pyenv-win\versions\3.11.9\python.exe" -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python .venv\Scripts\pywin32_postinstall.py -install

# tests (LOCK)
.venv\Scripts\pytest tools

# render as-built pages
.venv\Scripts\python tools\read-asbuilt\render_pages.py --pages 1-3

# AutoCAD 2023 connection check (AutoCAD open)
.venv\Scripts\python tools\check-autocad\check_autocad.py --require-2023
```

Caltrans resource kit is installed at `C:\Caltrans\HQ\C3D_2024` (copy of
`01_References/Drawing Standards/C3D_2024`).

## References not in this repository

The repository holds the workspace (rules, skills, tools, notes, indexes, calcs, plans). The
source PDFs under `01_References/` and the Caltrans C3D_2024 kit are excluded by `.gitignore`
because the AASHTO and AISC volumes are licensed to H&H and the rest is large. On a new machine:

| Local path | Content | Source |
|---|---|---|
| `01_References/As_Builts/*.pdf` | 1973 USACE as-built set (79 pp scan) | Alameda County PWA |
| `01_References/Inspection Reports/*.pdf` | Caltrans BIRIS reports 2013–2025 | Caltrans SM&I |
| `01_References/Design Codes/` | CA Amendments (Sept 2025), BDP 5th chapters, AASHTO LRFD 8th, AASHTO Movable 3rd, AISC 15th | Caltrans website (CA, BDP); H&H licensed copies (AASHTO, AISC) |
| `01_References/Drawing Standards/` | Caltrans CADD Users Manual + C3D_2024 kit | Caltrans CADD site; kit also installed at `C:\Caltrans\HQ\C3D_2024` |

The indexes (`As_Builts/INDEX.md`, `Design Codes/CODES_INDEX.md`, `Standards_Notes.md`) are
committed and describe what each file contains and where clauses live.
