"""
Render pages of a scanned PDF to PNG so Claude can read them visually.

The as-built set has no text layer; every dimension must be read from a
rendered image. This script only renders — it never interprets.

Usage (from project root):
    .venv\\Scripts\\python tools\\read-asbuilt\\render_pages.py --pages 1-3,12
    .venv\\Scripts\\python tools\\read-asbuilt\\render_pages.py --pages 14 --dpi 300 --crop 0.5,0.0,1.0,0.5

Options:
    --pdf PATH      PDF to render (default: the as-built set in 01_References/As_Builts)
    --pages SPEC    e.g. "1-5,12,30-31" or "all" (default: all)
    --dpi N         render resolution (default 150; use 300 for dimensions)
    --out DIR       output folder (default: 01_References/As_Builts/renders)
    --crop x0,y0,x1,y1   fractional crop of the page (0..1), written as a
                    separate file with suffix _crop
    --force         overwrite existing PNGs
    --info          print page count and page sizes only

Output file names: p001.png, p001_300dpi.png, p001_300dpi_crop.png ...
Prints a JSON object listing written files. Exit 1 on any error.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_PDF = os.path.join(
    PROJECT_ROOT, "01_References", "As_Builts",
    "01A Fruitvale Avenue Highway Bridge AS-BUILT-1.pdf",
)
DEFAULT_OUT = os.path.join(PROJECT_ROOT, "01_References", "As_Builts", "renders")
DEFAULT_DPI = 150
PDF_POINTS_PER_INCH = 72.0


def parse_pages(spec: str, page_count: int) -> list[int]:
    """'1-3,7' -> [1,2,3,7] (1-based). 'all' -> every page. Raises on out-of-range."""
    if spec.strip().lower() == "all":
        return list(range(1, page_count + 1))
    pages: list[int] = []
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            a, b = chunk.split("-", 1)
            start, end = int(a), int(b)
            if start > end:
                raise ValueError(f"Bad range '{chunk}': start > end")
            pages.extend(range(start, end + 1))
        else:
            pages.append(int(chunk))
    bad = [p for p in pages if p < 1 or p > page_count]
    if bad:
        raise ValueError(f"Pages out of range 1..{page_count}: {bad}")
    seen: set[int] = set()
    return [p for p in pages if not (p in seen or seen.add(p))]


def parse_crop(spec: str | None) -> tuple[float, float, float, float] | None:
    if spec is None:
        return None
    vals = [float(v) for v in spec.split(",")]
    if len(vals) != 4:
        raise ValueError("--crop needs four values x0,y0,x1,y1 as fractions 0..1")
    x0, y0, x1, y1 = vals
    if not (0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1):
        raise ValueError(f"--crop fractions must satisfy 0<=x0<x1<=1 and 0<=y0<y1<=1, got {vals}")
    return x0, y0, x1, y1


def page_info(pdf_path: str) -> dict:
    import pymupdf

    doc = pymupdf.open(pdf_path)
    try:
        sizes = []
        for i, page in enumerate(doc, start=1):
            r = page.rect
            sizes.append({
                "page": i,
                "width_in": round(r.width / PDF_POINTS_PER_INCH, 2),
                "height_in": round(r.height / PDF_POINTS_PER_INCH, 2),
                "rotation": page.rotation,
                "has_text": bool(page.get_text().strip()),
            })
        return {"pdf": pdf_path, "page_count": len(doc), "pages": sizes}
    finally:
        doc.close()


def render(pdf_path: str, pages: list[int], dpi: int, out_dir: str,
           crop: tuple[float, float, float, float] | None, force: bool) -> dict:
    import pymupdf

    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(pdf_path)
    os.makedirs(out_dir, exist_ok=True)
    doc = pymupdf.open(pdf_path)
    try:
        written, skipped = [], []
        suffix = "" if dpi == DEFAULT_DPI else f"_{dpi}dpi"
        for p in pages:
            page = doc[p - 1]
            rect = page.rect
            clip = None
            name = f"p{p:03d}{suffix}"
            if crop:
                x0, y0, x1, y1 = crop
                clip = pymupdf.Rect(
                    rect.x0 + x0 * rect.width, rect.y0 + y0 * rect.height,
                    rect.x0 + x1 * rect.width, rect.y0 + y1 * rect.height,
                )
                name += "_crop"
            out_path = os.path.join(out_dir, name + ".png")
            if os.path.exists(out_path) and not force:
                skipped.append(out_path)
                continue
            pix = page.get_pixmap(dpi=dpi, clip=clip, alpha=False)
            pix.save(out_path)
            written.append({"file": out_path, "page": p, "dpi": dpi,
                            "px": [pix.width, pix.height], "crop": list(crop) if crop else None})
        return {"pdf": pdf_path, "page_count": len(doc), "written": written, "skipped": skipped}
    finally:
        doc.close()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pdf", default=DEFAULT_PDF)
    ap.add_argument("--pages", default="all")
    ap.add_argument("--dpi", type=int, default=DEFAULT_DPI)
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--crop", default=None)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--info", action="store_true")
    args = ap.parse_args(argv)

    try:
        if args.info:
            print(json.dumps(page_info(args.pdf), indent=2))
            return 0
        if args.dpi < 50 or args.dpi > 600:
            raise ValueError("--dpi must be between 50 and 600")
        info = page_info(args.pdf)
        pages = parse_pages(args.pages, info["page_count"])
        result = render(args.pdf, pages, args.dpi, args.out, parse_crop(args.crop), args.force)
        print(json.dumps(result, indent=2))
        return 0
    except Exception as e:  # noqa: BLE001 — CLI boundary: report and fail loudly
        print(json.dumps({"status": "error", "message": f"{type(e).__name__}: {e}"}, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
