"""LOCK tests for build_index.py."""

import json
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import build_index as bi  # noqa: E402


def good_entry(**over):
    e = {"pdf_page": 1, "sheet_no": "1", "title": "GENERAL PLAN", "dwg_no": None,
         "scale": "1\"=20'", "summary": "Plan and elevation.", "legibility": "good",
         "verified": False, "notes": ""}
    e.update(over)
    return e


def test_validate_accepts_good():
    bi.validate([good_entry(), good_entry(pdf_page=2, sheet_no="2")])


@pytest.mark.parametrize("bad", [
    {"pdf_page": "1"},
    {"legibility": "ok"},
    {"verified": "no"},
    {"pdf_page": 0},
    {"extra": 1},
])
def test_validate_rejects_bad(bad):
    with pytest.raises(ValueError):
        bi.validate([good_entry(**bad)])


def test_validate_rejects_duplicate_pages():
    with pytest.raises(ValueError):
        bi.validate([good_entry(), good_entry()])


def test_render_markdown_lists_missing_pages():
    md = bi.render_markdown([good_entry(), good_entry(pdf_page=3, sheet_no="3")], page_count=4)
    assert "| 1 | 1 | GENERAL PLAN |" in md
    assert "Pages not yet indexed" in md
    assert "2, 4" in md
    assert "Human-verified: 0" in md


def test_cli_roundtrip(tmp_path):
    idx = tmp_path / "index.json"
    out = tmp_path / "INDEX.md"
    idx.write_text(json.dumps([good_entry(notes="title block partly cut off")]), encoding="utf-8")
    rc = bi.main(["--index", str(idx), "--out", str(out), "--page-count", "2"])
    assert rc == 0
    text = out.read_text(encoding="utf-8")
    assert "GENERAL PLAN" in text and "title block partly cut off" in text
