# Design Basis — Miller-Sweeney Deck Rehabilitation

Status: **Editions set by the EOR (Nicholas Davis, 2026-09-07; AASHTO edition revised to 8th
and California Amendments added the same day).** Order of precedence as listed. Where two
documents address the same provision, the higher-precedence document governs; cite both and
flag the difference (CALCULATION_RULES §1, §8).

| Prec. | Document | Edition / date | File in `01_References/Design Codes/` | Tool key |
|---|---|---|---|---|
| 1 | California Amendments to AASHTO LRFD BDS 8th Ed. (binding Caltrans amendments; April 2019 base with addenda/errata through Sept 2025) | Sept 2025 compilation | `Caltrans BDP/202509-aashto-lrfd-ca-amendments-a11y.pdf` | `ca` |
| 1 | Caltrans Bridge Design Practice (BDP) — practice manual and worked examples | 5th Ed. (chapters Oct 2022 – Jan 2025) | `Caltrans BDP/` (21 chapter PDFs) | `bdp --chapter N` |
| 2 | AASHTO LRFD Movable Highway Bridge Design Specifications | 3rd Ed., August 2023 | `AASHTO LRFD MOVABLE 2023.pdf` | `movable` |
| 3 | AASHTO LRFD Bridge Design Specifications | 8th Ed., November 2017 | `AASHTO LRFD 2017 BridgeDesignSpecifications 8th Ed (US).PDF` | `lrfd` |
| 4 | AISC Steel Construction Manual (incl. ANSI/AISC 360-16 and RCSC bolt spec) | 15th Ed., 2017 | `AISC-Steel-Construction-Manual-15th-Edition-2017.pdf` | `aisc` |

How the top tier works: the California Amendments **replace or add to** specific AASHTO 8th Ed.
articles; an amended article is read from `ca`, everything else from `lrfd`. BDP is guidance
that conforms to "AASHTO 8th Ed. with California Amendments" (BDP Preface, June 2024) and
never overrides the Amendments. The Movable spec governs movable-bridge-specific provisions
(balance, machinery loads, trunnions) and itself defers to AASHTO LRFD for fixed-bridge design.

Look up clauses with `skills/read-code.skill` → `tools/read-code/find_clause.py`. Chapter map
and page notes in `01_References/Design Codes/CODES_INDEX.md`. The BDP 5th Ed. and the
Amendments are both written to the 8th Ed., so article numbers now line up across the set.

## Supporting documents (not design codes)

| Item | Document | Status |
|---|---|---|
| Construction specs | Caltrans Standard Specifications 2025; Standard Special Provisions 2025 | per scope; not yet in references |
| Existing design load | HS 20 (BIRIS 2025 item 31, "MS 18") | as-built 1973 |
| Load rating on record | Inventory RF 0.94, Operating RF 1.57 (BIRIS 2025 p. 3; LRE hand calcs 1997) | record only |
| Welding | AWS D1.5 Bridge Welding Code as referenced by Caltrans Std Specs | not in references |

## Known gaps (EOR to disposition — OPEN_ITEMS #9)

- **BDP Chapter 9.1 Concrete Decks is "under development"** (BDP Preface) and not
  available. Deck provisions come from AASHTO LRFD Section 9 as amended (`ca` Section 9,
  PDF p 233 ff.).
- **Caltrans Structure Technical Policies (STPs)** are cited by BDP Ch 1 §1.1 as mandatory
  supplements; not in references.
- Caltrans Standard Specifications / SSPs 2025 and AWS D1.5 are not in references.

Units: US customary throughout (CALCULATION_RULES §3).
