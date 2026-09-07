"""
Add the Caltrans C3D_2024 resource kit to the current AutoCAD 2023 profile.

Appends (never replaces) support-file, plot-style, plotter-config and template
paths in `acad.Preferences.Files`. Requires AutoCAD 2023 to be running.
Idempotent: paths already present are skipped.

Usage (from project root, with AutoCAD 2023 open):
    .venv\\Scripts\\python tools\\_common\\setup_acad_paths.py [--dry-run]

Prints a JSON summary. Exit 0 on success, 1 on failure.
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.acad_com import AcadError, connect  # noqa: E402

KIT_ROOT = r"C:\Caltrans\HQ\C3D_2024"

# (Preferences.Files property, list of folders to append)
PATH_UPDATES = [
    ("SupportPath", [os.path.join(KIT_ROOT, "Fonts")]),
    ("PrinterStyleSheetPath", [os.path.join(KIT_ROOT, "Plotting", "Plot_Styles")]),
    ("PrinterConfigPath", [os.path.join(KIT_ROOT, "Plotting")]),
    ("TemplateDwgPath", [os.path.join(KIT_ROOT, "Templates")]),
]


def _norm(p: str) -> str:
    return os.path.normcase(os.path.normpath(p.strip().rstrip("\\")))


def main(dry_run: bool) -> dict:
    missing = [p for _, ps in PATH_UPDATES for p in ps if not os.path.isdir(p)]
    if missing:
        raise AcadError(
            "Kit folders missing: " + "; ".join(missing),
            fix="Copy 01_References/Drawing Standards/C3D_2024 to C:\\Caltrans\\HQ\\C3D_2024 first.",
        )

    acad, _ = connect(require_document=False, require_version=True)
    files = acad.Preferences.Files
    report = {}
    for prop, folders in PATH_UPDATES:
        current = str(getattr(files, prop))
        # SupportPath is ';'-separated; the single-folder properties hold one path.
        parts = [p for p in current.split(";") if p.strip()]
        existing = {_norm(p) for p in parts}
        added = []
        for folder in folders:
            if _norm(folder) in existing:
                continue
            if prop == "SupportPath":
                parts.append(folder)
            else:
                # Single-value property: AutoCAD accepts only one folder here.
                # Keep the user's current value unless it is empty or missing on disk.
                if current.strip() and os.path.isdir(current.strip()):
                    report.setdefault("skipped_single_value", []).append(
                        {prop: current, "kit_folder": folder,
                         "note": "left as-is; set manually in OPTIONS > Files if you want the kit folder default"}
                    )
                    continue
                parts = [folder]
            added.append(folder)
        new_value = ";".join(parts)
        if added and not dry_run:
            setattr(files, prop, new_value)
        report[prop] = {"before": current, "after": new_value, "added": added}
    report["dry_run"] = dry_run
    report["status"] = "ok"
    return report


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    try:
        result = main(dry)
    except AcadError as e:
        print(json.dumps(e.to_dict(), indent=2))
        sys.exit(1)
    print(json.dumps(result, indent=2))
    sys.exit(0)
