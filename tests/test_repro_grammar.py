"""Tests for the shared ``Repro:`` trailer grammar (Sprint 057, A-4/B-1)."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from _repro_grammar import REPRO_MANUAL, REPRO_TEST, ReproClaim, parse_trailers

ACCEPTED = [
    ("Repro: tests/test_on_commit.py::test_x — fails at 46d07cf",
     ReproClaim("test", "tests/test_on_commit.py", "test_x", "46d07cf")),
    ("Repro: tests/test_on_commit.py -- fails at 46d07cf0a1b2c3d4e5f60718293a4b5c6d7e8f90",
     ReproClaim("test", "tests/test_on_commit.py", "", "46d07cf0a1b2c3d4e5f60718293a4b5c6d7e8f90")),
    ("Repro: tests/test_on_commit.py — fails at abc1234",
     ReproClaim("test", "tests/test_on_commit.py", "", "abc1234")),
    ("Repro: tests/calc.test.ts::adds — fails at abc1234",
     ReproClaim("test", "tests/calc.test.ts", "adds", "abc1234")),
    ("Repro: manual — SPRINT_LOG section 3", ReproClaim("manual", text="SPRINT_LOG section 3")),
    ("Repro: manual -- SPRINT_LOG section 3", ReproClaim("manual", text="SPRINT_LOG section 3")),
]

REJECTED = [
    "Repro: something",
    "Repro: manual",
    "Repro: manual — ",
    "Repro: tests/test_on_commit.py — fails at xyz",
    "Repro: tests/test_on_commit.py — fails at abc12",
    "Repro: tests/test_calc.py::test_add — SPRINT_LOG",  # loose-only: no "fails at"
    "Repro: tests/test_calc.py — fails at abc1234 trailing junk",  # loose-only: junk
    "Repro: tests/test_calc.py - fails at abc1234",  # single hyphen
    "Repro:tests/test_calc.py — fails at abc1234",  # no space after colon
    "Repro: a b — fails at abc1234",  # two tokens as path
]


@pytest.mark.parametrize(("trailer", "expected"), ACCEPTED)
def test_accepted_form_parses_identically(trailer: str, expected: ReproClaim) -> None:
    assert parse_trailers(f"fix(x): y #057\n\nbody\n\n{trailer}\n") == [expected]


@pytest.mark.parametrize("trailer", REJECTED)
def test_rejected_form_yields_no_claim(trailer: str) -> None:
    assert parse_trailers(f"fix(x): y #057\n\n{trailer}\n") == []


def test_no_trailer_gives_empty_list() -> None:
    assert parse_trailers("fix(x): y #057\n\nplain body\n") == []
    assert parse_trailers("") == []


def test_multiple_trailers_keep_message_order() -> None:
    msg = (
        "fix(x): y #057\n\n"
        "Repro: tests/test_a.py::test_one — fails at abc1234\n"
        "Repro: manual -- SPRINT_LOG 2\n"
        "Repro: tests/test_b.py -- fails at def5678\n"
    )
    assert [c.claim for c in parse_trailers(msg)] == [
        "tests/test_a.py::test_one",
        "manual",
        "tests/test_b.py",
    ]


def test_manual_wins_over_test_when_both_fit() -> None:
    claims = parse_trailers("Repro: manual — fails at abc1234\n")
    assert claims == [ReproClaim("manual", text="fails at abc1234")]


def test_regex_constants_match_the_hook_forms() -> None:
    assert REPRO_TEST.search("Repro: tests/t.py — fails at abc1234")
    assert REPRO_MANUAL.search("Repro: manual -- text")
