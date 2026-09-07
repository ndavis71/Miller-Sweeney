"""
AutoCAD Connection Check (Miller-Sweeney workspace).

Attaches to the running AutoCAD via COM, confirms a drawing is open and
writable, writes a hello text at the origin, and reports version info.

Usage (from project root):
    .venv\\Scripts\\python tools\\check-autocad\\check_autocad.py [--no-text] [--require-2023]

Outputs one JSON object:
    {"status": "ok", "version": "...", "product": "...", "document": "...", "text_written": true}
    {"status": "error", "code": "...", "message": "...", "fix": "..."}
Exit 0 on ok, 1 on error.
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.acad_com import AcadError, connect, point, version_info, write_test  # noqa: E402

HELLO_TEXT = "Hello from Claude. You are connected to AutoCAD."
HELLO_HEIGHT_DRAWING_UNITS = 1.0  # project units are feet (Standards_Notes §2); 1 ft is visible at any zoom


def check(write_text: bool = True, require_2023: bool = False) -> dict:
    try:
        acad, doc = connect(require_document=True, require_version=require_2023)
        write_test(doc)
    except AcadError as e:
        return e.to_dict()

    result = {"status": "ok", "document": doc.Name, "text_written": False}
    result.update(version_info(acad))

    if write_text:
        try:
            txt = doc.ModelSpace.AddText(HELLO_TEXT, point(0, 0, 0), HELLO_HEIGHT_DRAWING_UNITS)
            txt.Layer = "0"
            doc.Regen(1)
            result["text_written"] = True
        except Exception as e:  # noqa: BLE001 — connection is proven; report the write failure
            result["text_warning"] = f"Connected but could not write text: {e}"
    return result


if __name__ == "__main__":
    res = check(write_text="--no-text" not in sys.argv, require_2023="--require-2023" in sys.argv)
    print(json.dumps(res, indent=2))
    sys.exit(0 if res["status"] == "ok" else 1)
