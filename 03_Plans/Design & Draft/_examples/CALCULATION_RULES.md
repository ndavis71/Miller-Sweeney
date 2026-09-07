# Calculation Rules

Every number here may end up on a sealed document. These rules are not
stylistic; violating them produces work that cannot be sealed.

## 1. Provenance of every number

- Each numeric input carries its source in a trailing comment: code clause,
  drawing number, spec section, report page, or `EOR decision`.
  `phi_f = 1.00  # AASHTO LRFD 6.5.4.2, flexure, steel`
- **Never supply a code coefficient, table value, or section property from
  memory.** If it isn't in this repo — data file, pasted table, uploaded
  spec — stop and ask. A plausible wrong digit is worse than a missing one,
  because it gets sealed instead of caught.
- Section properties come from a verified shapes database or from
  first-principles calculation written out in the code. Never recalled.
- Name the code edition and any agency modification in the module header
  (e.g. AASHTO LRFD 10th Ed. as modified by FDOT SDG). Mixing editions within
  one calculation is an error, not a detail.
- If a transcribed equation or published value looks wrong, report the
  discrepancy. Never silently correct it.

## 2. Assumptions are explicit or absent

- Each module opens with an `ASSUMPTIONS` block: one line each, stated so it
  could be falsified by inspection.
- If a calculation needs an assumption that wasn't given, do not choose one.
  Stop and ask. In the face of ambiguity, refuse the temptation to guess.
- Assumptions the provisions silently depend on — compact vs. noncompact,
  braced vs. unbraced, shored vs. unshored, simple vs. continuous, composite
  action — are enforced in code, not merely noted in prose.

## 3. Units

- One unit system per module, declared in the header.
- Units live in the variable name or its comment: `fy_ksi`, `Mu_kip_ft`,
  `Lb_in`.
- No inline conversion magic numbers. Named constants only.
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

- No more significant figures than the inputs justify.
- Round at presentation only, never mid-calculation.
- Never round in the direction that improves a D/C ratio.

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
  a D/C of 0.98, deciding a member is adequately braced, waiving a
  serviceability check — these belong to the EOR. Flag them; don't resolve
  them.
- You do not interpret code intent. Where a provision is ambiguous, present
  the readings, name the ambiguity, stop.
- State uncertainty where it occurs, at the point of use. Not in a preamble.
