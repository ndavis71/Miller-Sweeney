"""LOCK tests for read-code/find_clause.py. Run: .venv\\Scripts\\pytest tools/read-code"""

import json
import os
import re
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import find_clause as fc  # noqa: E402

with open(os.path.join(HERE, "expected_results.json"), encoding="utf-8") as f:
    EXP = json.load(f)

pymupdf = pytest.importorskip("pymupdf")


def _open(code, chapter=None):
    return pymupdf.open(fc.resolve_path(code, chapter))


def test_all_bdp_chapters_exist():
    missing = [k for k in fc.BDP_CHAPTERS if not os.path.isfile(fc.resolve_path("bdp", k))]
    assert missing == []


@pytest.mark.parametrize("code", ["lrfd", "ca", "movable", "aisc"])
def test_page_counts(code):
    assert len(_open(code)) == EXP["page_count"][code]


def test_no_page_labels_raises_clear_error():
    doc = _open("lrfd")
    with pytest.raises(ValueError):
        fc.page_by_label(doc, "6-55")


def test_lrfd_clause_bookmark():
    doc = _open("lrfd")
    probe = EXP["lrfd_clause_probe"]
    hits = fc.search_bookmarks(doc, probe["clause"], clause_mode=True)
    assert hits, "expected a bookmark for the probe clause"
    assert hits[0]["pdf_page"] == probe["pdf_page"]
    assert probe["title_contains"].lower() in hits[0]["title"].lower()


def test_ca_clause_bookmark():
    doc = _open("ca")
    probe = EXP["ca_clause_probe"]
    hits = fc.search_bookmarks(doc, probe["clause"], clause_mode=True)
    assert hits and hits[0]["pdf_page"] == probe["pdf_page"]


def test_movable_text_clause():
    doc = _open("movable")
    hits = fc.search_text(doc, fc.clause_regex(EXP["movable_clause_probe"]["clause"]), 5)
    assert hits and hits[0]["pdf_page"] == EXP["movable_clause_probe"]["pdf_page"]


def test_bdp_chapter_probe():
    doc = _open("bdp", EXP["bdp_probe"]["chapter"])
    hits = fc.search_text(doc, re.compile(EXP["bdp_probe"]["pattern"]), 5)
    assert hits and hits[0]["pdf_page"] == EXP["bdp_probe"]["pdf_page"]


def test_clause_regex_does_not_match_longer_numbers():
    rx = fc.clause_regex("6.6.1")
    assert rx.search("6.6.1 Fatigue") is not None
    assert rx.search("6.6.1.2 Load-Induced Fatigue") is None
    assert rx.search("16.6.1 Something") is None


def test_precedence_order():
    assert fc.CODES["ca"]["precedence"] == fc.CODES["bdp"]["precedence"] == 1
    assert fc.CODES["movable"]["precedence"] < fc.CODES["lrfd"]["precedence"] < fc.CODES["aisc"]["precedence"]


def test_unknown_code_and_missing_chapter():
    with pytest.raises(ValueError):
        fc.resolve_path("nope", None)
    with pytest.raises(ValueError):
        fc.resolve_path("bdp", None)
    with pytest.raises(ValueError):
        fc.resolve_path("bdp", "9.1")


def test_cli_list_chapters(capsys):
    assert fc.main(["bdp", "--list-chapters"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert "6.2" in out["bdp_chapters"]
