"""
Locate and read clauses in the design-code PDFs (01_References/Design Codes).

Every code cited in a calculation must be read, not recalled (CALCULATION_RULES §1).
This tool finds where a clause lives and prints its text so the reader can quote it
with a page reference.

Codes are addressed by short key (see CODES):
    ca       California Amendments to AASHTO LRFD BDS 8th Ed. (Sept 2025) — binding Caltrans document
    bdp      Caltrans Bridge Design Practice, 5th Ed. (chapter PDFs; use --chapter)
    movable  AASHTO LRFD Movable Highway Bridge Design Specifications, 3rd Ed. 2023
    lrfd     AASHTO LRFD Bridge Design Specifications, 8th Ed. 2017 (read with `ca`)
    aisc     AISC Steel Construction Manual, 15th Ed. 2017

Usage (from project root):
    .venv\\Scripts\\python tools\\read-code\\find_clause.py lrfd --clause 6.6.1.2.3
    .venv\\Scripts\\python tools\\read-code\\find_clause.py lrfd --search "orthotropic deck" --max 20
    .venv\Scripts\python tools\read-code\find_clause.py ca --clause 3.4.1              # California Amendments
    .venv\Scripts\python tools\read-code\find_clause.py lrfd --pdf-page 700          # 8th Ed. has no page labels
    .venv\\Scripts\\python tools\\read-code\\find_clause.py movable --pdf-page 120 --chars 6000
    .venv\\Scripts\\python tools\\read-code\\find_clause.py bdp --chapter 6.2 --clause 6.2.5
    .venv\\Scripts\\python tools\\read-code\\find_clause.py bdp --list-chapters
    .venv\\Scripts\\python tools\\read-code\\find_clause.py aisc --toc "Chapter J"

Output is JSON. --clause / --toc search bookmarks first, then full text as fallback.
Text hits show the PDF page (1-based) and the printed page label when the PDF has one
(none of the current PDFs carry labels; the printed page number appears in the page text).
Always read `ca` alongside `lrfd`: an amended article replaces the AASHTO text.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CODES_DIR = os.path.join(PROJECT_ROOT, "01_References", "Design Codes")

CODES = {
    "lrfd": {
        "file": "AASHTO LRFD 2017 BridgeDesignSpecifications 8th Ed (US).PDF",
        "cite": "AASHTO LRFD BDS 8th Ed. (2017)",
        "precedence": 3,
    },
    "ca": {
        "file": os.path.join("Caltrans BDP", "202509-aashto-lrfd-ca-amendments-a11y.pdf"),
        "cite": "California Amendments to AASHTO LRFD BDS 8th Ed. (Sept 2025 addenda/errata)",
        "precedence": 1,
    },
    "movable": {
        "file": "AASHTO LRFD MOVABLE 2023.pdf",
        "cite": "AASHTO LRFD Movable Highway Bridge Design Specs 3rd Ed. (2023)",
        "precedence": 2,
    },
    "aisc": {
        "file": "AISC-Steel-Construction-Manual-15th-Edition-2017.pdf",
        "cite": "AISC Steel Construction Manual 15th Ed. (2017)",
        "precedence": 4,
    },
    "bdp": {
        "dir": "Caltrans BDP",
        "cite": "Caltrans Bridge Design Practice 5th Ed.",
        "precedence": 1,
    },
}

# BDP chapter number -> file name (folder listing, 2026-09-07)
BDP_CHAPTERS = {
    "cover": "BDP-5thCover and TOC-A11y.pdf",
    "preface": "202406-BDP-5thPreface-A11y.pdf",
    "terms": "202409-BDP-5thTermsAndAbbreviations-A11y2.pdf",
    "1": "202406-BDP-Chapter-1BridgeDesignSpecifications-A11y.pdf",
    "3": "202210-BDP-Chapter-3LoadsAndLoadCombinations-A11y.pdf",
    "4": "202210-BDP-Chapter-4StructuralModelingAndAnalysis-A11y.pdf",
    "5.1": "202406BDPChapter51ConcreteDesignTheoryA11y.pdf",
    "5.2": "202210BDPChapter52PostTensionedConcreteGirderA11y.pdf",
    "5.3": "202604bdp0503-a11y.pdf",
    "5.4": "202210BDPChapter54PrecastPretensionedBoxGirderA11y.pdf",
    "5.5": "202210BDPChapter55PrecastPretensionedVoidedSlabA11y.pdf",
    "5.6": "202210BDPChapter56Concrete Bent CapsA11y.pdf",
    "5.7": "202210BDPChapter57ConcreteColumnA11y.pdf",
    "6.1": "202210BDPChapter61SteelDesignTheoryA11y.pdf",
    "6.2": "202210BDPChapter62SteelPlateGirdersA11y.pdf",
    "10.1": "202501BDPChapter101ShallowFoundationsA11y.pdf",
    "11.1": "202210BDPChapter111AbutmentsA11y.pdf",
    "11.2": "202210BDPChapter112EarthRetainingSystemsA11y.pdf",
    "16.1": "202210BDPChapter161StrengtheningSteelGirdersA11y.pdf",
    "20.1": "202210BDPChapter201SesimicDesignofConcreteBridgesA11y.pdf",
    "20.2": "202210BDPChapter202SeismicDesignofSteelBridgesA11y.pdf",
}


def resolve_path(code: str, chapter: str | None) -> str:
    if code not in CODES:
        raise ValueError(f"unknown code key '{code}'; choose from {sorted(CODES)}")
    if code == "bdp":
        if not chapter:
            raise ValueError("bdp needs --chapter (e.g. 6.2); use --list-chapters to see them")
        if chapter not in BDP_CHAPTERS:
            raise ValueError(f"BDP chapter '{chapter}' not in folder; available: {sorted(BDP_CHAPTERS)}")
        path = os.path.join(CODES_DIR, CODES["bdp"]["dir"], BDP_CHAPTERS[chapter])
    else:
        path = os.path.join(CODES_DIR, CODES[code]["file"])
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    return path


def _norm(s: str) -> str:
    return re.sub(r"[\s—–\- ]+", " ", s).strip().lower()


def clause_regex(clause: str) -> re.Pattern:
    """Match '6.6.1.2.3' at a line start followed by a title (em dash, en dash, hyphen or spaces)."""
    esc = re.escape(clause)
    return re.compile(rf"(?m)^\s*(?:Article\s+)?{esc}(?![\d.])\s*[—–\-:]?\s*\S")


def search_bookmarks(doc, query: str, clause_mode: bool) -> list[dict]:
    hits = []
    q = _norm(query)
    for lvl, title, page in doc.get_toc():
        t = _norm(title)
        if clause_mode:
            ok = t.startswith(q + " ") or t == q or t.startswith(q + "—") or re.match(rf"^{re.escape(q)}(?![\d.])", t) is not None
        else:
            ok = q in t
        if ok:
            hits.append({"level": lvl, "title": title.strip(), "pdf_page": page, "label": _label(doc, page)})
    return hits


def _label(doc, pdf_page: int) -> str | None:
    try:
        lab = doc[pdf_page - 1].get_label()
        return lab or None
    except Exception:  # noqa: BLE001
        return None


def search_text(doc, pattern: re.Pattern, max_hits: int, context: int = 160) -> list[dict]:
    hits = []
    for i, page in enumerate(doc, start=1):
        text = page.get_text()
        for m in pattern.finditer(text):
            a, b = max(0, m.start() - context // 4), min(len(text), m.end() + context)
            hits.append({"pdf_page": i, "label": _label(doc, i), "snippet": " ".join(text[a:b].split())})
            if len(hits) >= max_hits:
                return hits
    return hits


def page_by_label(doc, label: str) -> int:
    for i in range(len(doc)):
        if doc[i].get_label() == label:
            return i + 1
    raise ValueError(f"no page carries label '{label}' (this PDF may have no labels; use --pdf-page)")


def page_text(doc, pdf_page: int, chars: int) -> dict:
    if pdf_page < 1 or pdf_page > len(doc):
        raise ValueError(f"pdf page {pdf_page} out of range 1..{len(doc)}")
    text = doc[pdf_page - 1].get_text()
    return {"pdf_page": pdf_page, "label": _label(doc, pdf_page), "chars_total": len(text),
            "text": text[:chars], "truncated": len(text) > chars}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("code", choices=sorted(CODES))
    ap.add_argument("--chapter", help="BDP chapter key, e.g. 6.2")
    ap.add_argument("--list-chapters", action="store_true", help="list BDP chapter keys and files")
    ap.add_argument("--clause", help="article number, e.g. 6.10.1.1.1a")
    ap.add_argument("--toc", help="substring to find in bookmarks")
    ap.add_argument("--search", help="regex to find in full text")
    ap.add_argument("--page", help="printed page label (only PDFs that carry labels; none of the current set do)")
    ap.add_argument("--pdf-page", type=int, help="1-based PDF page index")
    ap.add_argument("--chars", type=int, default=4000, help="characters of page text to print")
    ap.add_argument("--max", type=int, default=25, help="max text hits")
    args = ap.parse_args(argv)

    try:
        if args.list_chapters:
            print(json.dumps({"bdp_chapters": BDP_CHAPTERS}, indent=2))
            return 0
        import pymupdf

        path = resolve_path(args.code, args.chapter)
        doc = pymupdf.open(path)
        out = {"code": args.code, "cite": CODES[args.code]["cite"], "precedence": CODES[args.code]["precedence"],
               "file": os.path.relpath(path, PROJECT_ROOT), "page_count": len(doc)}
        did = False
        if args.clause:
            did = True
            out["clause"] = args.clause
            out["bookmark_hits"] = search_bookmarks(doc, args.clause, clause_mode=True)
            out["text_hits"] = search_text(doc, clause_regex(args.clause), args.max)
        if args.toc:
            did = True
            out["toc_hits"] = search_bookmarks(doc, args.toc, clause_mode=False)
        if args.search:
            did = True
            out["text_hits"] = search_text(doc, re.compile(args.search, re.IGNORECASE), args.max)
        if args.page:
            did = True
            out["page"] = page_text(doc, page_by_label(doc, args.page), args.chars)
        if args.pdf_page:
            did = True
            out["page"] = page_text(doc, args.pdf_page, args.chars)
        if not did:
            raise ValueError("give one of --clause, --toc, --search, --page, --pdf-page, --list-chapters")
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0
    except Exception as e:  # noqa: BLE001 — CLI boundary
        print(json.dumps({"status": "error", "message": f"{type(e).__name__}: {e}"}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
