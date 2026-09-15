"""Tests for scripts/map_workflows.py — the U12 change (Sprint 047, S045-27).

U12 taught the parser to tell a step list from a reference table and to label
each step's effect rather than guess:

- `_is_prose` / `_effect` classify a step cell as `read` / `write` / `verify`
  when the verb is recognised, else `prose` (a `**Bold sentence.**`) or
  `ambiguous` (an unrecognised verb on a real step id).
- A table whose immediately preceding non-blank line equals
  `<!-- map_workflows:skip-table -->` is excluded from `parse` entirely.
- `parse` now returns 4-tuples `(phase, step, action, effect)`; it returned
  3-tuples before.

Cases 1-4 fail against HEAD (helpers absent, `parse` returns 3-tuples and keeps
every `| a | b | c |` row). Case 5 is a regression guard that also passes on
HEAD's shape once the 4th element is accounted for.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import map_workflows


def _write_workflow(tmp_path: Path, body: str) -> Path:
    """Write `body` to a mini workflow file under `tmp_path` and return its path.

    Args:
        tmp_path (Path): The pytest per-test temporary directory.
        body (str): The full Markdown contents of the workflow file.

    Returns:
        Path: The path the contents were written to.
    """
    path = tmp_path / "sample_workflow.md"
    path.write_text(body, encoding="utf-8")
    return path


STEP_AND_SKIP_TABLE = """\
# Sample Workflow

## Phase 1 - Setup

| Phase | Step | Action |
| :--- | :--- | :--- |
| Setup | `state_claim` | verify the tree |
| Setup | `plan_write` | write the plan |

<!-- map_workflows:skip-table -->

| Legacy artifact | Destination | Action |
| :--- | :--- | :--- |
| old_thing.md | docs/archive/ | move it here |
| stale.txt | trash/ | delete it now |
"""

PLAIN_STEP_TABLE = """\
# Regression Workflow

## Phase 2

| Phase | Step | Action |
| :--- | :--- | :--- |
| Planning | `roadmap_read` | read the roadmap |
| Execution | `module_create` | create the module |
| Gate | `qa_verify` | verify the standards |
"""


# --- Case 1: _is_prose ------------------------------------------------------


def test_is_prose_code_span_is_a_step_id() -> None:
    assert map_workflows._is_prose("`state_claim`") is False


def test_is_prose_short_bold_label_is_a_step_id() -> None:
    assert map_workflows._is_prose("**Option B**") is False


def test_is_prose_bold_sentence_is_prose() -> None:
    assert map_workflows._is_prose("**Graph first.** Do X.") is True


def test_is_prose_anchor_then_bold_sentence_is_prose() -> None:
    assert map_workflows._is_prose('<a id="x"></a>**Bold sentence.** more') is True


# --- Case 2: _effect ------------------------------------------------------


def test_effect_recognised_verb_is_the_classify_label() -> None:
    assert map_workflows._effect("`x`", "verify the tree") == "verify"


def test_effect_unrecognised_verb_on_step_id_is_ambiguous() -> None:
    assert map_workflows._effect("`x`", "frobnicate") == "ambiguous"


def test_effect_unrecognised_verb_on_bold_sentence_is_prose() -> None:
    assert map_workflows._effect("**A bold sentence.**", "frobnicate") == "prose"


# --- Case 3: skip-marker integration ------------------------------------------


def test_parse_excludes_skip_marked_reference_table(tmp_path: Path) -> None:
    path = _write_workflow(tmp_path, STEP_AND_SKIP_TABLE)

    rows = map_workflows.parse(path)

    assert ("Setup", "state_claim", "verify the tree", "verify") in rows
    assert ("Setup", "plan_write", "write the plan", "write") in rows
    assert {row[1] for row in rows} == {"state_claim", "plan_write"}
    joined = [" ".join(row) for row in rows]
    assert not any("Legacy artifact" in text for text in joined)
    assert not any("old_thing.md" in text for text in joined)
    assert not any("stale.txt" in text for text in joined)


# --- Case 4: parse returns 4-tuples ------------------------------------------


def test_parse_returns_four_tuples_with_classify_as_fourth(tmp_path: Path) -> None:
    path = _write_workflow(tmp_path, STEP_AND_SKIP_TABLE)

    rows = map_workflows.parse(path)

    assert rows
    for row in rows:
        assert len(row) == 4
    for _phase, _step, action, effect in rows:
        if map_workflows.classify(action) != "?":
            assert effect == map_workflows.classify(action)


# --- Case 5: regression on a plain step table ------------------------------


def test_parse_plain_step_table_yields_read_write_verify(tmp_path: Path) -> None:
    path = _write_workflow(tmp_path, PLAIN_STEP_TABLE)

    rows = map_workflows.parse(path)

    assert rows == [
        ("Planning", "roadmap_read", "read the roadmap", "read"),
        ("Execution", "module_create", "create the module", "write"),
        ("Gate", "qa_verify", "verify the standards", "verify"),
    ]
    assert all(row[3] in {"read", "write", "verify"} for row in rows)
