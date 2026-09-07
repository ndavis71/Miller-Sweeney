# Caltrans CADD Standards — Distilled for Miller-Sweeney

Source: Caltrans *CADD Users Manual* (May 2026 compilation), `01_References/Drawing Standards/cadd-manual-fulltext.pdf`.
Resource kit: `01_References/Drawing Standards/C3D_2024/`, installed to `C:\Caltrans\HQ\C3D_2024` (the kit's LISP and configs hardcode that root).
Section numbers below are manual sections; page numbers are the manual's own footers.

Where this note and the manual disagree, the manual governs. Where the manual is silent on structures detailing, it defers to the Caltrans *Bridge Design Details Manual* (BDD) — **not in our references; obtain before building sheet-generation skills.**

---

## 1. File naming — structures (§2.2 ¶4, p. 2.2-11 to 2.2-13)

Pattern: `cc-bbbb-p-sss.dwg`

| Part | Meaning | Miller-Sweeney |
|---|---|---|
| `cc` | County code | `33` (Alameda) |
| `bbbb` | Bridge number (no r/l suffix for a single bridge) | `C0147` (Br. No. 33C0147) |
| `p` | Print sequence code, single letter, sets plot order | from table below |
| `sss` | Sheet type identifier, variable length, `01`, `02`… for multiples | from table below |

Example: `33-C0147-a-gp01.dwg` = General Plan sheet 1.

Print sequence codes (manual table, p. 2.2-12/13). Sheet types most likely on this deck-rehab job are marked ►.

| Code | Sheet type | Identifier |
|---|---|---|
| a | GENERAL PLAN ► | `gp01` |
| a | INDEX TO PLANS ► | `itp` |
| b | GENERAL NOTES ► | `gnote` |
| c | STRUCTURE PLAN | `sp01` |
| d | DECK CONTOURS | `dc01` |
| e | FOUNDATION DATA / PLAN | `fdat01` / `fpl01` |
| f | ABUTMENT LAYOUT / DETAILS ► (approach slab, paving notch) | `a01_lo1` / `a01dt01` |
| g | RETAINING WALL LAYOUT / DETAILS / FOOTING | `rw_lo01` / `rwdt01` / `rwftg` |
| h | BENT LAYOUT / DETAILS / FOOTING | `b01_lo01` / `b01dt01` |
| i | PIER LAYOUT / DETAILS / FOOTING / RESTRAINER; COLUMN DETAILS ► (trunnion columns) | `p01_lo01` / `p01dt01` / `cdet01` |
| j | COLUMN ISOLATION CASING / RESTRAINER; TYPICAL SECTION ► | `ciso01` / `crdt01` / `ts01` |
| k | PART TYPICAL SECTION ►; GIRDER LAYOUT | `tsp01` / `g_lo01` |
| l | GIRDER DETAILS ► (Girder 4 weld repair) | `gdt01` |
| m | CAMBER DIAGRAM; LONGITUDINAL SECTION | `cam` / `lsec` |
| n | HINGE / HINGE DETAILS / BEARING / RESTRAINER | `hinge` / `hingedt01` |
| o | GIRDER REINFORCEMENT (TOP/BOTTOM) | `gir_rf01` / `gr_top01` / `gbot01` |
| p | PILE DETAILS | `pdt01` |
| q | BEARING DETAILS; JOINT DETAILS ► (Pier 5 seal, finger joints) | `brgdt01` / `jntdt` |
| r | DECK DRAINS / DRAIN DETAILS | `dd01` / `ddet01` |
| s | STRUCTURE APPROACH DRAIN DETAILS | `sadd` |
| t | BARRIER RAILING / CRASH CUSHIONS / RESTRAINER UNIT | `brdt` / `crc` / `resunit` |
| u | MISCELLANEOUS DETAILS ► (deck repair, methacrylate limits, staging) | `miscdt01` |
| v | END DIAPHRAGM DETAIL | `eddt` |
| w | ADDITIONAL SLAB REINFORCEMENT | `asr` |
| x | LADDER DETAILS | `ldt` |
| y | ACCESS OPENING / GIRDER ACCESS / EARTHQUAKE RETROFIT DETAILS | `aodt` / `gadt` / `erdt` |
| z | LOG OF TEST BORINGS | `ltb01` |

Movable-bridge sheets (deck panel layout, counterweight/balance, machinery) have no code in the manual table. **Decision needed from EOR / County:** slot them under `u` (misc details) with descriptive identifiers, or agree a project-specific extension. Record the decision in `project.json` → `sheet_index`.

File-state extensions (p. 2.2-11): `.dgn` through expedite; `.rev` revisions after expedite to second notice; `.add` second notice through bid opening; `.cco` bid opening through construction; `.avd` archived vector data. For a DWG workflow keep `.dwg` and put the state in the submittal folder name (`03_Plans/PDF/70pct/`, `100pct/`).

## 2. Working units — structures (§2.3 B, p. 2.3-2)

- Structures files are drawn **1'-0" = 1'-0"**, master unit US Survey Feet, sub-unit inches.
- In AutoCAD: `INSUNITS = 2` (feet), `LUNITS = 4` (architectural) or 2 (decimal feet) per H&H practice, `MEASUREMENT = 0`. Model space at full size; sheets in paper-space layouts at 1:1 on a 22"×34" border with viewports scaled.
- Roadway files use State Plane coordinates at 1:1 (§2.3 A). Do not mix: roadway base mapping from Alaco/Sanbell is XREF'd, not merged.

## 3. Layers — structures named-level convention (§2.4, p. 2.4-18/19)

Pattern: `groupname_Taskname-Subtaskname-plotdesignation-D`

- Group for all structural content is `str` (lower case).
- Task/sub-task in Title Case, separated by hyphens.
- Optional plot designation: `-drop`, `-dither` (legacy), `-NoPlot` / `-no_plot`, `-info_only`.
- Optional single upper-case data designation letter (`-A`, `-B`, …) for sub-grouping.

Manual task names for `str` (verbatim list, p. 2.4-19): Guideline, Arch-Treatment, As-Built-Changes, Border, Border-Plot-Shape, Border-PSE-OE-Rsvrd, Border-PSE-Seal, Border-PSE-Signature, Border-Text, Border-Title-Block, CCO-Changes, Center-Line, Concrete, Deck-Contours, Dimensions, Dropout, Engineering-Notes, Existing, Existing-Arch-Treatment, Existing-Concrete, Existing-Non-Metallic, Existing-Railroad, Existing-Reinforcement, Existing-Roadway, Existing-Steel, Existing-Utilities, Existing-Wood, Grades (+ -Exec-Backfill, -Finish-Grade, -Major-Grades, -Minor-Grades, -Origonal-Ground [sic], -Slope-Protection, -Top-Toe-Slope, -Water), Hatching, Layout, Masking-Shape, Misc-Steel, Non-Metallic-Components, Prestressed-Components, Railroad, Reinforcement, Structural-Steel, Text, Utilities, Wood.

**Starter layer set for this project** (all from the list above; add only names the manual allows):

| Layer | Use |
|---|---|
| `str_Border` | Sheet border linework (from Caltrans border template) |
| `str_Border-Title-Block` | Title block linework |
| `str_Border-Text` | Title block text, sheet no., project ID |
| `str_Border-PSE-Seal` | Engineer seal |
| `str_Border-PSE-Signature` | Signature |
| `str_Border-Plot-Shape` | Plot boundary (color 252 reserved, see §6) |
| `str_Existing-Steel` | Existing bascule girders, orthotropic deck, floor beams |
| `str_Existing-Concrete` | Existing deck, abutments, piers, trunnion columns |
| `str_Existing-Reinforcement` | Existing rebar where shown |
| `str_Existing-Roadway` | Approach AC, striping, curbs |
| `str_Structural-Steel` | New steel (weld repair plates, deck panels) |
| `str_Concrete` | New concrete (deck patches, approach slab) |
| `str_Reinforcement` | New rebar |
| `str_Misc-Steel` | Joint hardware, plates, anchors |
| `str_Center-Line` | Bridge CL, girder CLs, pier CLs |
| `str_Dimensions` | Dimensions and dimension text |
| `str_Text` | Callouts, labels |
| `str_Engineering-Notes` | Sheet notes blocks |
| `str_Hatching` | Concrete/steel hatching, removal limits |
| `str_Layout` | Layout lines, stationing |
| `str_Deck-Contours` | If deck contours are produced |
| `str_As-Built-Changes` | Reserved; not used until construction |
| `str_Guideline-NoPlot` | Construction lines, non-plotting |
| `str_Masking-Shape` | Masks (color 250 fill / 251 outline, see §6) |

## 4. Text — structures (§2.6 C, p. 2.6-3)

Heights are **plotted inches on the 22"×34" sheet** (V8-era values; pre-V8 used feet on a 22'×34' border — do not confuse).

| Use | Height/width (in) | Font | Weight |
|---|---|---|---|
| Informational notes; majority of plan lettering; border information | 0.14 | 3 (CTFONT1) | 1 or 2 |
| Detail titles | 0.14 | 3 (CTFONT1) | 4 |
| Sheet titles and border information | 0.24 | 43 (BOLD) | 0 |

- Font 3 = `CTFONT1_C3D.shx` (main Caltrans font). Font 43 = `bold_C3D.shx`. Leroy (font 2) is R/W only. Font 23 obsolete — never use.
- As-built change text: font 3 at 15° slant, 0.14 in (roadway table gives 8.75 ft @ 1"=50', §2.6 B; structures equivalent is the notes size).
- Waterway names: font 3 at 25° slant.
- For legibility at half size (11×17), do not go below 0.14 in for any readable text (§2.6 A rationale).
- AutoCAD text styles to create: `CT-NOTES` (CTFONT1, 0.14, width 1.0), `CT-DETAIL-TITLE` (CTFONT1, 0.14, heavier lineweight via layer or plot style), `CT-SHEET-TITLE` (bold_C3D, 0.24). Set model-space heights = paper height × viewport scale factor, or use annotative styles (Caltrans itself does not use annotative objects — `acaddoc.lsp` note — so prefer fixed heights per viewport scale).

## 5. Lines (§2.7, p. 2.7-1 to 2.7-4)

MicroStation weights map to plotted widths roughly: wt 0 ≈ 0.007", wt 1 ≈ 0.010", wt 2 ≈ 0.014", wt 3 ≈ 0.020", wt 4 ≈ 0.028" (approximate; use the STB named styles rather than hand-set lineweights).

| Weight | Feature |
|---|---|
| 0 | Dimension lines, object center lines, station callouts, table interior rows |
| 1 | Object lines, hidden lines, R/W lines, alignment stationing |
| 2 | Local street / ramp alignments; table exterior borders; profile grade line |
| 3 | Main route alignment |
| 4 | Sheet border |

Structures-specific weights: "defined in a table in each Structures Design seed file" (p. 2.7-2) — the seed is MicroStation; not in our kit. Use the table above plus BDD when obtained.

Line codes (§2.7 C): 0 solid (proposed); 1 dotted / 2 short dash (existing); 3 long dash (hidden details, existing non-structural, toe of fill); 4 dash-dot; 5 medium dash (top of cut); 6 dash-dot-dot (**existing structural features**); 7 long dash–short dash (**object centerlines**).

Every dashed line must be labeled for what it represents (§2.7 D). Notes govern over graphics (Std Spec 5-1.02, quoted §2.7 A).

Line style scale factor (§2.7 E): resource styles are drawn at 1:500 metric; scale factor = (plot ratio ÷ 500) × 3937/1200 → 1"=20' → 1.5748; 1"=50' → 3.937; 1"=100' → 7.874. For structures detail scales compute the same way (e.g. 1/4"=1'-0" is 1:48 → 48/500 × 3.2808 = 0.315).

## 6. Colors (§2.8, p. 2.8-1/2)

Standard roadway colors 0–15 (ctcolor.tbl): 0 white (plots black), 1 blue, 2 green, 3 red, 4 yellow, 5 purple, 6 orange, 7 brown, 8–15 lighter variants of 1–7.

Reserved colors: **250** masking fill (plots white), **251** mask outline (plots black), **252** plot-shape of sheet border — never use on any element, **255** background. Colors 85–116 force dropout/non-dropout in plotting scripts.

Plot appearance is by named plot style in AutoCAD (STB), not by color (CTB). Kit STBs: `BW.stb` (PS&E black & white), `GreyScale.stb`, `Color.stb`, `CT_DWFx.stb`. Use `BW.stb` for contract plans unless the County requests otherwise.

## 7. Sheets and plotting (§2.6 C, §5.x)

- Sheet size **22"×34" (ANSI D)**; half-size 11"×17" is the normal review print, so legibility is judged at half size.
- Border template: `C:\Caltrans\HQ\C3D_2024\Templates\Borders\Ct_2024_Design_PlanProfile.dwt` (Civil 3D roadway border; the kit has **no structures border**). Title block content for a County-administered project follows County/BDD practice — **confirm with EOR before first sheet**.
- PDF plotting: `C:\Caltrans\HQ\C3D_2024\Plotting\AutoCAD PDF (High Quality Print).pc3` with `DWG To PDF.pmp`. Plot to 22×34 at 1:1 from layout.
- Sheet border, seal, signature and printed names live on the border layers (§2.4 level 10 / 63; str_Border-*). Signature and seal data must be removed before issuing DWG files externally (§4.3 B).

## 8. As-built plans (§4.3)

Our as-built set is the record for existing conditions only. When we later prepare our own record drawings: all sheets in the set get the As-Built stamp, RE name, CCA date, contract number; redlines come only from the RE. Not needed for design phase — noted for completeness.

## 9. Kit contents relevant to us (`C:\Caltrans\HQ\C3D_2024\`)

| Path | What |
|---|---|
| `Templates\Ct_2024_Design.dwt` | Base drawing template (styles, layers — inventory via COM) |
| `Templates\Ct_2024_Design_Other_Styles.dwt` | Additional styles |
| `Templates\Borders\Ct_2024_Design_PlanProfile.dwt` | 22×34 plan/profile border |
| `Templates\Sheet Sets\NR_SheetSet_Master.dst` | Sheet set template |
| `Fonts\*.shx`, `Fonts\Ct_Font_Subtitution.fmp` | CTFONT1, BOLD, Leroy, etc. |
| `Plotting\Plot_Styles\*.stb` | Named plot styles |
| `Plotting\*.pc3`, `Plotting\PMP_Files\*.pmp` | PDF plotters |
| `DGN_Setups\Numbered_Levels_for_Consultants\50_Scale-Remap_C3D_to_MSta_Numbered_Levels.csv` | Layer → MicroStation level remap (roadway; useful if a DGN export is ever requested) |
| `Apps\Startup\Design\acaddoc.lsp` | Caltrans sysvar defaults (VISRETAIN 1, PROXYGRAPHICS 1, SAVEFIDELITY 0, PLINEGEN 1, LINETYPE3DPLINEON). **Optional** — it also loads Civil 3D DLLs; do not auto-load in plain AutoCAD. |
| `Apps\RW_Tools\*.lsp` | R/W utilities, not needed |

AutoCAD 2023 support paths to add (script `tools/_common/setup_acad_paths.py`): `Fonts`, `Plotting\Plot_Styles` (Printer Style Sheet path), `Plotting` (Printer Config path), `Templates`, `Templates\Borders` (Template path).

## 10. Not in the kit — needed before sheet production

- Caltrans **Bridge Design Details Manual** (structures sheet order, title conventions, standard detail lettering, structures lineweight table).
- Alameda County Public Works title block / signature block requirements for a County-administered structure project.
- Caltrans Standard Plans 2024/2025 sheets referenced by the SSPs (for callouts).
