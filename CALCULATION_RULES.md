# Calculation Rules — Miller-Sweeney Bridge Deck Rehabilitation

Every number here may end up on a sealed document. These rules are not
stylistic; violating them produces work that cannot be sealed.

**Design basis — order of precedence set by the EOR (N. Davis, 2026-09-07); full table and
known gaps in `04_Calcs/DESIGN_BASIS.md`; look clauses up with `skills/read-code.skill`:**

1. California Amendments to AASHTO LRFD BDS 8th Ed. (Sept 2025 compilation) together with
   Caltrans Bridge Design Practice, 5th Edition (`01_References/Design Codes/Caltrans BDP/`).
   The Amendments are binding; BDP is guidance conforming to them.
2. AASHTO LRFD Movable Highway Bridge Design Specifications, 3rd Edition (2023).
3. AASHTO LRFD Bridge Design Specifications, 8th Edition (2017) — always read with the Amendments.
4. AISC Steel Construction Manual, 15th Edition (2017).

Supporting: Caltrans Standard Specifications / SSPs 2025 for materials and construction;
as-built drawings (1973 USACE) and Caltrans BIRIS reports for the existing structure.

**Units: US customary.** kip, ft, in, ksi, psf, kip-ft. Suffixes in variable names: `_kip`, `_lb`, `_ft`, `_in`, `_ksi`, `_psi`, `_psf`, `_kipft`, `_kipin`, `_deg`, `_rad`.

## 1. Provenance of every number

- Each numeric input carries its source in a trailing comment: code clause,
  as-built sheet number, spec section, BIRIS report date and page, test memo, or `EOR decision`.
  `phi_f = 1.00  # AASHTO LRFD 6.5.4.2, flexure, steel`
  `t_deck_plate_in = 0.5  # AS-BUILT Sheet 14, orthotropic deck plate`
- **Never supply a code coefficient, table value, or section property from
  memory.** If it isn't in this repo — data file, pasted table, uploaded
  spec — stop and ask. A plausible wrong digit is worse than a missing one,
  because it gets sealed instead of caught.
- Section properties come from a verified shapes database or from
  first-principles calculation written out in the code. Never recalled.
- Name the code edition and any agency modification in the module header.
  Mixing editions within one calculation is an error, not a detail.
- If a transcribed equation or published value looks wrong, report the
  discrepancy. Never silently correct it.

## 2. Assumptions are explicit or absent

- Each module opens with an `ASSUMPTIONS` block: one line each, stated so it
  could be falsified by inspection.
- If a calculation needs an assumption that wasn't given, do not choose one.
  Stop and ask. In the face of ambiguity, refuse the temptation to guess.
- Assumptions the provisions silently depend on — compact vs. noncompact,
  braced vs. unbraced, composite action, span seated vs. open, brakes set vs.
  released, counterweight pocket fill state — are enforced in code, not merely
  noted in prose.

## 3. Units

- One unit system per module, declared in the header.
- Units live in the variable name or its comment: `fy_ksi`, `Mu_kipft`, `Lb_in`.
- No inline conversion magic numbers. Named constants only
  (`IN_PER_FT = 12.0`, `LB_PER_KIP = 1000.0`).
- Guard input ranges. A range check catches a kip/lb error that review reads
  straight past.

## 4. Range of applicability

- Every code equation gets an explicit guard on its stated range of
  applicability, raising when violated.
- Never extrapolate past a table or curve. Never silently clamp to a bound.
- Where a provision branches on a condition, evaluate and report the
  condition. Don't assume which branch applies.

## 5. Failure and reporting

- **Errors never pass silently.** No `except` returning a default. No
  fallback to a simplified equation because the rigorous one failed.
- Guards that protect a sealed number use `raise`, never `assert` —
  assertions vanish under `python -O`. `assert` belongs in `tests/` only.
- A check that could not be performed reports `NOT CHECKED`. Never as
  passing, never omitted. Absence must never read as compliance.
- Report the D/C ratio for every limit state evaluated, not only the
  controlling one, and name which governs. The reviewer needs to see what
  didn't govern.
- Outputs are generated. Never hand-edit a result; change the input and
  rerun.

## 6. Precision

- No more significant figures than the inputs justify. As-built dimensions
  read from a scanned sheet are good to the nearest 1/8 in at best; say so.
- Round at presentation only, never mid-calculation.
- Never round in the direction that improves a D/C ratio or reduces an
  imbalance.

## 7. Reviewability

- The calculation must be hand-checkable. Name and print intermediate
  quantities instead of collapsing them into one expression. A reviewer with
  the code book and a calculator should follow every line.
- Variable names match the notation in the governing code (`Mu`, `Cb`, `Rb`,
  `Fcr`). Matching the code book *is* the readability requirement here —
  engineering symbol names take precedence over generic Python naming
  conventions; don't "fix" them.
- Prefer a clear loop to vectorized cleverness. If the implementation is hard
  to explain, it is a bad idea.
- For anything to be sealed, provide an independent check — hand calc,
  simplified bound, or comparison to a known solution — or state plainly that
  you have not.

## 8. Judgment stays with the engineer

- You do not make engineering judgment calls. Load path selection, accepting
  a D/C of 0.98, deciding a member is adequately braced, setting the
  allowable imbalance, waiving a serviceability check — these belong to the
  EOR. Flag them; don't resolve them.
- You do not interpret code intent. Where a provision is ambiguous, present
  the readings, name the ambiguity, stop.
- State uncertainty where it occurs, at the point of use. Not in a preamble.

## 9. Field and record data

Existing-structure numbers come from documents, and every one is tagged with
its status:

| Tag | Meaning |
|---|---|
| `AS-BUILT` | Read from the 1973 as-built set. Cite `AS-BUILT Sheet N (PDF p M)`. A render must have been viewed; never quote from memory of a sheet. |
| `FIELD-VERIFIED` | Measured by H&H in the field, cite the field note/date. |
| `BIRIS` | From a Caltrans inspection report. Cite report type, inspection date, page. |
| `TEST` | From the H&H balance test / strain-gauge memo. Cite memo and table. |
| `ASSUMED` | Not in any document. Listed in the module `ASSUMPTIONS` block **and** in `04_Calcs/OPEN_ITEMS.md` for EOR disposition. |

- As-built and field values that disagree are both reported; the calc uses
  the one the EOR designates, with the decision recorded.
- Scanned-sheet dimensions carry a legibility note when the render is poor
  (`# AS-BUILT Sheet 9, dimension partly illegible, read as 3'-6"`).
- Deficiencies from BIRIS (spall sizes, crack widths, section loss) enter as
  inputs with their inspection date; a repair calc states which inspection
  it is based on.

## 10. Movable-bridge specifics

- Span balance, imbalance limit, counterweight geometry and block inventory,
  trunnion reactions, and machinery capacity are EOR-signed inputs. Scripts
  read them from `04_Calcs/inputs/*.json`, where each value carries
  `value`, `unit`, `source`, `date`. No inline literals for these.
- Deck-rehab weight changes are tracked as a signed ledger (removed −,
  added +) by span region and lever arm about the trunnion axis; the ledger
  is an output file, regenerated, never edited.
- Report both **span seated** and **span open** (and any intermediate angle
  the EOR names) for every balance and machinery check. A check run at one
  position only is `NOT CHECKED` for the others.
- The operating-imbalance limit that goes on the plans is an EOR decision.
  The calc presents the machinery-limited and brake-limited values with
  their D/C; it does not select the number.

## 11. Where calculations live

```
04_Calcs/
├── DESIGN_BASIS.md          # code editions, agency amendments, confirmed by EOR
├── OPEN_ITEMS.md            # every ASSUMED value and every EOR decision pending
├── inputs/                  # *.json with value/unit/source/date per entry
└── <topic>/                 # e.g. balance/, trunnion/, weld_repair/, deck_patch/
    ├── README.md            # purpose, inputs, method, results, conclusions, reproduction
    ├── *.py                 # the calculation
    ├── outputs/             # generated; regenerable
    └── tests/               # known-answer checks (LOCK)
```

A topic README updates in the same change as the numbers it reports. Stale
numbers in a README are worse than no README.
