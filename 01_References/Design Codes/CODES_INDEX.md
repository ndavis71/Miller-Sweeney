# Design Codes — Index

Generated 2026-09-07 from the PDFs in this folder (pymupdf page counts and bookmarks). Revised
the same day when the EOR replaced AASHTO 10th Ed. with 8th Ed. and added the California
Amendments. Precedence (N. Davis, 2026-09-07): **CA Amendments + BDP → Movable → LRFD 8th → AISC**.
Look up clauses with `tools/read-code/find_clause.py` (skill `read-code`). Cite as
`Doc Ed. Art. x.y.z (p. <printed>; PDF p <n>)`. No PDF in this set carries page labels; printed
page numbers appear in the page text.

| Prec. | Key | Document | Pages | Bookmarks | Text |
|---|---|---|---|---|---|
| 1 | `ca` | California Amendments to AASHTO LRFD BDS 8th Ed. — Sept 2025 addenda/errata compilation (base April 2019) | 430 | 430 (section + article) | yes |
| 1 | `bdp` | Caltrans Bridge Design Practice, 5th Ed. | 21 PDFs | per chapter | yes |
| 2 | `movable` | AASHTO LRFD Movable Highway Bridge Design Specifications, 3rd Ed., Aug 2023 | 312 | none | yes |
| 3 | `lrfd` | AASHTO LRFD Bridge Design Specifications, 8th Ed., Nov 2017 | 1783 | 1933 | yes |
| 4 | `aisc` | AISC Steel Construction Manual, 15th Ed., 2017 | 2324 | 102 | yes |

AASHTO and AISC files are H&H-licensed copies (IHS / Accuris watermark). Do not copy outside the firm.

---

## 1a. California Amendments to AASHTO LRFD 8th Ed. (`Caltrans BDP/202509-aashto-lrfd-ca-amendments-a11y.pdf`)

PDF pp 1–22 are the Sept 2025 addenda/errata cover memo and revision table (revisions in bold);
the compiled Amendments start at PDF p 23 (title page, April 2019). Amended articles keep AASHTO
numbering; Caltrans-inserted pages carry a letter suffix (`3-29B`). Sections not listed (7, 15)
have no amendments.

| Section | Title | PDF p |
|---|---|---|
| — | Addenda / errata memo and revision table | 1 |
| — | Preface to California Amendments | 25 |
| 1 | Introduction | 26 |
| 2 | General Design and Location Features | 32 |
| 3 | Loads and Load Factors (3.4.1 Load Factors and Load Combinations at p 41) | 38 |
| 4 | Structural Analysis and Evaluation | 83 |
| 5 | Concrete Structures | 117 |
| 6 | Steel Structures | 201 |
| 8 | Wood Structures | 231 |
| 9 | Decks and Deck Systems | 233 |
| 10 | Foundations | 240 |
| 11 | Walls, Abutments, and Piers | 351 |
| 12 | Buried Structures and Tunnel Liners | 387 |
| 13 | Railings | 407 |
| 14 | Joints and Bearings (14.8.3.1 at p 427; 14.10 References p 429) | 413 |

## 1b. Caltrans BDP 5th Ed. — chapters present (`Caltrans BDP/`)

BDP conforms to **AASHTO LRFD 8th Ed. with California Amendments**, Caltrans Seismic Design
Criteria v2.0, Caltrans Seismic Design Specifications for Steel Bridges 2nd Ed., and Bridge
Design Memos (Preface, June 2024). Chapters are numbered to align with AASHTO sections.
`--chapter` key → file:

| Key | Chapter | Date | Pages | File |
|---|---|---|---|---|
| cover | Cover and TOC | Oct 2022 | 4 | `BDP-5thCover and TOC-A11y.pdf` |
| preface | Preface | Jun 2024 | 2 | `202406-BDP-5thPreface-A11y.pdf` |
| terms | Terms and Abbreviations | Sep 2024 | 5 | `202409-BDP-5thTermsAndAbbreviations-A11y2.pdf` |
| 1 | Bridge Design Specifications | Jun 2024 | 15 | `202406-BDP-Chapter-1BridgeDesignSpecifications-A11y.pdf` |
| 3 | Loads and Load Combinations | Oct 2022 | 58 | `202210-BDP-Chapter-3LoadsAndLoadCombinations-A11y.pdf` |
| 4 | Structural Modeling and Analysis | Oct 2022 | 58 | `202210-BDP-Chapter-4StructuralModelingAndAnalysis-A11y.pdf` |
| 5.1 | Concrete Design Theory | Jun 2024 | 31 | `202406BDPChapter51ConcreteDesignTheoryA11y.pdf` |
| 5.2 | Post-Tensioned Concrete Girders | Oct 2022 | 114 | `202210BDPChapter52PostTensionedConcreteGirderA11y.pdf` |
| 5.3 | Precast Pretensioned Concrete I-Girders | Oct 2022 (file 2026-04) | 112 | `202604bdp0503-a11y.pdf` |
| 5.4 | Precast Pretensioned Box Girders | Oct 2022 | 74 | `202210BDPChapter54PrecastPretensionedBoxGirderA11y.pdf` |
| 5.5 | Precast Pretensioned Voided Slabs | Oct 2022 | 84 | `202210BDPChapter55PrecastPretensionedVoidedSlabA11y.pdf` |
| 5.6 | Concrete Bent Caps | Oct 2022 | 80 | `202210BDPChapter56Concrete Bent CapsA11y.pdf` |
| 5.7 | Concrete Columns | Oct 2022 | 84 | `202210BDPChapter57ConcreteColumnA11y.pdf` |
| 6.1 | Steel Design Theory | Oct 2022 | 31 | `202210BDPChapter61SteelDesignTheoryA11y.pdf` |
| 6.2 | Steel Plate Girders | Oct 2022 | 122 | `202210BDPChapter62SteelPlateGirdersA11y.pdf` |
| 10.1 | Shallow Foundations | Jan 2025 | 41 | `202501BDPChapter101ShallowFoundationsA11y.pdf` |
| 11.1 | Abutments | Oct 2022 | 52 | `202210BDPChapter111AbutmentsA11y.pdf` |
| 11.2 | Earth Retaining Systems | Oct 2022 | 152 | `202210BDPChapter112EarthRetainingSystemsA11y.pdf` |
| 16.1 | Strengthening Steel Girders for Live Loads | Oct 2022 | 138 | `202210BDPChapter161StrengtheningSteelGirdersA11y.pdf` |
| 20.1 | Seismic Design of Concrete Bridges | Oct 2022 | 140 | `202210BDPChapter201SesimicDesignofConcreteBridgesA11y.pdf` |
| 20.2 | Seismic Design of Steel Bridges | Oct 2022 | 136 | `202210BDPChapter202SeismicDesignofSteelBridgesA11y.pdf` |

Not published by Caltrans as of the June 2024 preface (so not here): Ch 2 Architecture,
**Ch 9.1 Concrete Decks**, Ch 10.2 Deep Foundations, Ch 12.1 Buried Structures, Ch 14.1
Bearings, Ch 14.2 Expansion Joints.

Most relevant to this job: Ch 1 (design philosophy; CA sets η_D = η_R = η_I = 1.0 per §1.5.5),
Ch 3 (loads), Ch 5.1 (concrete repair basis), Ch 6.1 / 6.2 (steel, fatigue detail practice),
Ch 16.1 (strengthening existing steel girders — nearest analogue for the Girder 4 weld repair),
Ch 5.3 (Spans 4–5 PC/PS I-girders), Ch 11.1 (abutment approach slab / paving notch).

## 2. AASHTO LRFD Movable Highway Bridge Design Specifications, 3rd Ed. (2023)

No bookmarks. Each section has its own TOC page(s) immediately before the body. Search text
(`--search`, `--clause`) and cite the PDF page plus the printed page from the page text.

| Section | Title | Body starts (PDF p) |
|---|---|---|
| 1 | General Provisions (TOC p 11; 1.4.1 Structural Design body p 21) | 13 |
| 2 | Structural Design | 35 |
| 3 | Seismic Design | 53 |
| 4 | Vessel Collision Considerations | between 53 and 93 (header not machine-detected; `--search "Section 4"`) |
| 5 | Mechanical Design Loads and Power Requirements | 93 |
| 6 | Mechanical Design | 115 |
| 7 | Hydraulic Design | 197 |
| 8 | Electrical Design | 235 |
| App. A | SI Versions of Equations, Tables, and Figures | after 235 |

Key for this project: Section 2 dead load / counterweight / balance; Section 5 machinery design
loads and imbalance; Section 6 trunnions and brakes.

## 3. AASHTO LRFD Bridge Design Specifications, 8th Ed. (2017)

1933 bookmarks, but depth varies by section (Section 6 is bookmarked only to a coarse level;
`--clause` falls back to text search automatically). Printed page numbers (`6-5`) are in the
page text under the section header line.

| Section | Title | PDF p |
|---|---|---|
| — | Changed and Deleted Articles, 2017 | 12 |
| 1 | Introduction | 16 |
| 2 | General Design and Location Features | 26 |
| 3 | Loads and Load Factors | 54 |
| 4 | Structural Analysis and Evaluation | 240 |
| 5 | Concrete Structures | 342 |
| 6 | Steel Structures | 686 |
| 7 | Aluminum Structures | 1046 |
| 8 | Wood Structures | 1112 |
| 9 | Decks and Deck Systems | 1152 |
| 10 | Foundations | 1200 |
| 11 | Walls, Abutments, and Piers | 1378 |
| 12 | Buried Structures and Tunnel Liners | 1508 |
| 13 | Railings | 1624 |
| 14 | Joints and Bearings | 1654 |
| 15 | Design of Sound Barriers | 1746 |
| — | Index | 1760 |

Read every AASHTO article together with `ca` for the same article number.

## 4. AISC Steel Construction Manual, 15th Ed. (2017)

Bookmarks at Part / Chapter / major table level; no page labels. PDF pages:

| Part | Title | PDF p |
|---|---|---|
| 1 | Dimensions and Properties | 11 |
| 2 | General Design Considerations | 149 |
| 3 | Design of Flexural Members | 203 |
| — | Specification for Structural Steel Buildings (ANSI/AISC 360-16) | 1389 |
| — | Spec Ch. A–N | 1445–1616 |
| — | Spec App. 1–8 (App. 3 Fatigue p 1640; App. 5 Evaluation of Existing Structures p 1677) | 1629–1693 |
| — | Commentary | 1697 |
| — | RCSC Specification for Structural Joints Using High-Strength Bolts | 2065 |

Parts 4–17 are not bookmarked at level 1; use `--search` on the part title. Use AISC only where
the higher-precedence documents are silent (shape properties, Part 1; bolt/weld tables where
AASHTO 6.13 defers).

---

## Gaps (see `04_Calcs/DESIGN_BASIS.md`, OPEN_ITEMS #9)

Caltrans Structure Technical Policies; Caltrans Standard Specifications / SSPs 2025; AWS D1.5;
BDP Ch 9.1 Concrete Decks (unpublished).
