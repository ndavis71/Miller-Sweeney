# Open Items — assumptions and EOR decisions pending

Every `ASSUMED` value in any calc and every decision reserved to the EOR is listed here
until closed (CALCULATION_RULES §9, §10). Closed items move to the bottom with the decision
and date.

## Open

| # | Item | Raised | Where used | Needed by |
|---|---|---|---|---|
| 9 | Caltrans STPs, Std Specs 2025 / SSPs 2025, AWS D1.5 not in references; BDP Ch 9.1 unpublished | 2026-09-07 | specs, weld repair, deck | 70% |
| 2 | Checker name (TBD) | 2026-09-04 | project.json, title block | 70% QA check |
| 3 | Title block content for a County-administered structure (Caltrans BDD vs County format) | 2026-09-04 | acad-sheet skill | first sheet |
| 4 | Print-sequence code for movable-bridge sheets not in the CADD manual table | 2026-09-04 | file naming | plan set index |
| 5 | As-built PDF is 79 pages: pp 1-2 are letter crops of Sheet 1; Sheet 1 schedule lists Sheets 1-78 + 12A, 52A-F, 57A-C + 4 Modification Drawings (2-6-68). "Sheets 1-37" = structural portion. Confirm which sheets are actually in the PDF (77 sheet pages) and whether the Modification Drawings are included | 2026-09-04 | read-asbuilt index | indexing |
| 6 | Bridge Design Details Manual and Caltrans Standard Plans not in references | 2026-09-04 | drafting | acad-sheet skill |

## Closed

| # | Item | Decision | By | Date |
|---|---|---|---|---|
| 2a | H&H job no., EOR, PM, County project no. | Job 0006888.00; EOR Nicholas Davis; PM Tom Kubicz; no County project number | N. Davis | 2026-09-04 |
| 1 | Code editions for design basis | BDP 5th > AASHTO Movable 3rd > AASHTO LRFD 10th > AISC 15th; see DESIGN_BASIS.md | N. Davis | 2026-09-07 |
| 7 | California Amendments missing | Added: Sept 2025 addenda compilation in Caltrans BDP folder (tool key `ca`, precedence 1) | N. Davis | 2026-09-07 |
| 8 | BDP (8th Ed.) vs AASHTO 10th mismatch | AASHTO edition changed to 8th Ed. (2017); set is now internally consistent | N. Davis | 2026-09-07 |
