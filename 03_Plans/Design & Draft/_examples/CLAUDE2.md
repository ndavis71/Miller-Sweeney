# Project Rules

Calculations in this repo are sealed by an engineer in responsible charge.
Before writing or modifying any calculation, read
[CALCULATION_RULES.md](CALCULATION_RULES.md).

Where these rules don't cover a case, ask. Don't infer a convention.

---

## Layout

```
repo-root/
├── src/
│   ├── rhino_automations/      # design / analysis / reporting library
│   └── csi_dev/                # CSiBridge OAPI wrapper
├── projects/
│   ├── _templates/
│   ├── _archive/               # frozen — never edit
│   └── <project>/
│       ├── pyproject.toml      # per-project Poetry env + [tool.project-meta]
│       ├── source_models/      # tracked input .bdb
│       ├── rhino_geometry/     # .3dm untracked; .gh/.ghx tracked (top level only)
│       ├── working/<git_user>/ # scratch, gitignored
│       └── R<n>/
│           ├── baseline/
│           ├── design_report/
│           └── studies/<topic>/
└── tests/                      # offline pytest suite (+ tests/manual/ probes)
```

`from rhino_automations.design import ...` · `from csi_dev import csi_api`

## Conventions

- **New work goes in `working/<your_git_username>/`** unless directed
  otherwise. Promote to a study folder once it stabilizes — a tracked
  deliverable must not depend on scripts that exist only in scratch.
- **Analysis runs write to untracked space** — `working/<git_user>/` or an
  `outputs/` subfolder. Write into a tracked study folder only when told to.
  `.gitignore` is authoritative for what is tracked; don't reason about it
  here.
- Plots → `plots/` (tracked). CSV summaries → study root (tracked).
- Revision-specific requests with no revision named operate on the latest.
  Resolve it with `get_active_config().latest_revision()`
  (`rhino_automations.project_config`); don't read a revision number off a
  file path or an earlier message.
- `connect_csi()` resolves the project's pinned CSi version from
  `[tool.project-meta]` itself — don't pass `version=`. Resolution is
  extension-aware: `.bdb` models resolve `csibridge_version`, `.sdb`
  models resolve `sap2000_version` (optional key; a `.sdb` in a project
  without it raises). An explicit `version=` is a deliberate override of
  the pin, nothing else.
- `connect_csi()` requires a model path; a bare call raises. There is no
  attach-to-running mode (`tests/test_csi_policy.py` keeps it deleted).
- `projects/_archive/**` is frozen. Claude sessions are denied Edit/Write
  there via `.claude/settings.json`; the deny doesn't cover shell-mediated
  writes — treat it as a boundary, not a challenge.

## Folder documentation

Every deliverable folder under `studies/`, `design_report/`, `baseline/`, or
`archived_iterations/` carries a `README.md` from
[projects/_templates/STUDY_README.md](projects/_templates/STUDY_README.md).
`tests/test_repo_structure.py` enforces existence, the six required sections,
artifact coverage, and that referenced files exist — run it rather than
checking by eye. Folders predating the rule sit in that test's LEGACY list,
which only shrinks: fix a folder, delete its entry; never add one.

What the test cannot check, and you must: **when results or conclusions
change, update the Results and Conclusions sections in the same commit.**
Stale numbers in a README are worse than no README. Documentation ships with
the code change, not after it.

## Revision deliverables

Every revision `R<n>` ships the same documentation package —
`design_report/` with a generated top-level `design_summary.md`, the
member-takeoff package in `section_summary/`, and one calcbook per design
group — per
[projects/_templates/REVISION_DELIVERABLES.md](projects/_templates/REVISION_DELIVERABLES.md).
R11/R12 are the reference implementations; `tests/test_repo_structure.py`
enforces the skeleton. Don't invent a new report layout for a new revision.

## Tests & Poetry workflow

```powershell
# repo root — offline suite (repo structure, config, CSi policy, cable math)
poetry install
poetry run pytest

# per-project env
cd projects/<project>
poetry env use python3.12     # any 3.11+ (tomllib floor)
poetry install
poetry run python -m rhino_automations.design.<script> <args>
```

Shared packages install editable — edits to `src/` take effect in every env.
Scripts under `tests/manual/` launch real CSiBridge and are run by hand only.
