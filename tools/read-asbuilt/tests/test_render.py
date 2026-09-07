"""LOCK tests for render_pages.py. Run from project root: .venv\\Scripts\\pytest tools"""

import json
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import render_pages as rp  # noqa: E402

with open(os.path.join(HERE, "expected_results.json"), encoding="utf-8") as f:
    EXPECTED = json.load(f)

pdf_available = pytest.mark.skipif(not os.path.isfile(rp.DEFAULT_PDF), reason="as-built PDF not present")


def test_parse_pages_ranges():
    assert rp.parse_pages("1-3,7", 10) == [1, 2, 3, 7]
    assert rp.parse_pages("all", 4) == [1, 2, 3, 4]
    assert rp.parse_pages("3,3,2", 5) == [3, 2]


def test_parse_pages_rejects_out_of_range():
    with pytest.raises(ValueError):
        rp.parse_pages("0", 5)
    with pytest.raises(ValueError):
        rp.parse_pages("6", 5)
    with pytest.raises(ValueError):
        rp.parse_pages("4-2", 5)


def test_parse_crop():
    assert rp.parse_crop(None) is None
    assert rp.parse_crop("0,0,1,1") == (0.0, 0.0, 1.0, 1.0)
    with pytest.raises(ValueError):
        rp.parse_crop("0.5,0,0.5,1")
    with pytest.raises(ValueError):
        rp.parse_crop("0,0,1")


@pdf_available
def test_page_count_matches_expected():
    info = rp.page_info(rp.DEFAULT_PDF)
    assert info["page_count"] == EXPECTED["asbuilt_page_count"]


@pdf_available
def test_asbuilt_is_scanned():
    info = rp.page_info(rp.DEFAULT_PDF)
    assert not any(p["has_text"] for p in info["pages"][:5]), "expected no text layer on scanned as-built"


@pdf_available
def test_render_page_one(tmp_path):
    result = rp.render(rp.DEFAULT_PDF, [1], 72, str(tmp_path), None, force=True)
    assert len(result["written"]) == 1
    w = result["written"][0]
    assert os.path.isfile(w["file"])
    assert os.path.getsize(w["file"]) > EXPECTED["min_png_bytes_at_72dpi"]
    assert w["px"][0] >= EXPECTED["min_width_px_at_72dpi"]


@pdf_available
def test_render_skips_existing(tmp_path):
    rp.render(rp.DEFAULT_PDF, [1], 72, str(tmp_path), None, force=True)
    again = rp.render(rp.DEFAULT_PDF, [1], 72, str(tmp_path), None, force=False)
    assert again["written"] == [] and len(again["skipped"]) == 1


@pdf_available
def test_render_crop(tmp_path):
    full = rp.render(rp.DEFAULT_PDF, [1], 72, str(tmp_path), None, force=True)["written"][0]
    crop = rp.render(rp.DEFAULT_PDF, [1], 72, str(tmp_path), (0.0, 0.0, 0.5, 0.5), force=True)["written"][0]
    assert crop["file"].endswith("_crop.png")
    assert crop["px"][0] < full["px"][0] and crop["px"][1] < full["px"][1]
