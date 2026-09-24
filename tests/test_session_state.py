"""Tests for scripts/session_state.py.

First dedicated test file for this module (Sprint 050 `U6`): `grep -rln
'session_state' tests/` previously found three files that import it as a
fixture dependency for other mechanisms, none exercising it directly. This
file adds direct coverage, and pairs it with `set-topology` (Sprint 050
`D7`) — the writer that replaces the hand-edited `topology_version` defect.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import session_state as ss  # noqa: E402


# --- fixtures ------------------------------------------------------------

@pytest.fixture
def repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A cwd with `docs/` present, matching the `ACTIVE_STATE`/`CHANGELOG`
    module constants, which are both relative paths resolved against cwd."""
    (tmp_path / "docs").mkdir()
    monkeypatch.chdir(tmp_path)
    return tmp_path


MULTI_SECTION_CHANGELOG = """# Changelog

## [Unreleased]

### Added
- something not yet released

## [4.32.0] - 2026-09-20

### Fixed
- newest sealed release

## [4.31.0] - 2026-09-18

### Fixed
- older sealed release

## [4.30.0] - 2026-09-15

### Fixed
- oldest sealed release
"""


def _write_changelog(root: Path, body: str) -> None:
    (root / "CHANGELOG.md").write_text(body, encoding="utf-8")


def _write_anchor(root: Path, extra: dict | None = None) -> None:
    state = {
        "active_layer": "core",
        "session_id": "keep-me",
        "topology_version": "4.31.0-049-closed",
        "current_sprint": {"id": 50, "status": "IN_PROGRESS"},
    }
    if extra:
        state.update(extra)
    (root / "docs" / "active_state.json").write_text(json.dumps(state), encoding="utf-8")


# --- newest_sealed_version -------------------------------------------------

def test_newest_sealed_version_skips_unreleased_and_older_sections():
    version = ss.newest_sealed_version(MULTI_SECTION_CHANGELOG)
    assert version == "4.32.0"


def test_newest_sealed_version_none_when_only_unreleased_exists():
    body = "# Changelog\n\n## [Unreleased]\n\n### Added\n- pending\n"
    assert ss.newest_sealed_version(body) is None


# --- set-topology: format and derivation -----------------------------------

def test_set_topology_derives_expected_format(repo: Path):
    _write_changelog(repo, MULTI_SECTION_CHANGELOG)
    _write_anchor(repo)

    assert ss.set_topology() == 0

    state = json.loads((repo / "docs" / "active_state.json").read_text())
    assert state["topology_version"] == "4.32.0-050-in_progress"


def test_set_topology_lowercases_status(repo: Path):
    _write_changelog(repo, MULTI_SECTION_CHANGELOG)
    _write_anchor(repo, {"current_sprint": {"id": 50, "status": "CLOSED_SUCCESSFULLY"}})

    assert ss.set_topology() == 0

    state = json.loads((repo / "docs" / "active_state.json").read_text())
    assert state["topology_version"] == "4.32.0-050-closed_successfully"


def test_set_topology_zero_pads_sprint_id(repo: Path):
    _write_changelog(repo, MULTI_SECTION_CHANGELOG)
    _write_anchor(repo, {"current_sprint": {"id": 7, "status": "IN_PROGRESS"}})

    assert ss.set_topology() == 0

    state = json.loads((repo / "docs" / "active_state.json").read_text())
    assert state["topology_version"] == "4.32.0-007-in_progress"


DIFFERENT_VERSION_CHANGELOG = """# Changelog

## [Unreleased]

### Added
- something not yet released

## [7.1.4] - 2027-01-05

### Fixed
- newest sealed release, deliberately not 4.32.0

## [7.1.3] - 2026-12-20

### Fixed
- older sealed release
"""


def test_set_topology_writes_the_derived_version_not_a_fixed_one(repo: Path):
    """Every other fixture's newest sealed section is `4.32.0`, so a mutant
    that hardcodes that literal instead of using `newest_sealed_version`'s
    result passes them all undetected. This fixture's newest sealed section
    is `7.1.4` — distinguishing "derived" from "hardcoded to 4.32.0"."""
    _write_changelog(repo, DIFFERENT_VERSION_CHANGELOG)
    _write_anchor(repo, {"current_sprint": {"id": 12, "status": "IN_PROGRESS"}})

    assert ss.set_topology() == 0

    state = json.loads((repo / "docs" / "active_state.json").read_text())
    assert state["topology_version"] == "7.1.4-012-in_progress"


# --- set-topology: write-back preserves the rest of the anchor -------------

def test_set_topology_does_not_disturb_other_fields(repo: Path):
    _write_changelog(repo, MULTI_SECTION_CHANGELOG)
    _write_anchor(repo)

    assert ss.set_topology() == 0

    state = json.loads((repo / "docs" / "active_state.json").read_text())
    assert state["active_layer"] == "core"
    assert state["session_id"] == "keep-me"
    assert state["current_sprint"] == {"id": 50, "status": "IN_PROGRESS"}


def test_set_topology_corrects_the_known_stale_value(repo: Path):
    """Reproduces the live defect this unit fixes: `4.31.0-049-closed` is
    exactly one sprint and one CHANGELOG release behind."""
    _write_changelog(repo, MULTI_SECTION_CHANGELOG)
    _write_anchor(repo)
    before = json.loads((repo / "docs" / "active_state.json").read_text())["topology_version"]
    assert before == "4.31.0-049-closed"

    assert ss.set_topology() == 0

    after = json.loads((repo / "docs" / "active_state.json").read_text())["topology_version"]
    assert after != before
    assert after == "4.32.0-050-in_progress"


# --- set-topology: exit codes -----------------------------------------------

def test_set_topology_exits_0_and_prints_the_value(repo: Path, capsys: pytest.CaptureFixture):
    _write_changelog(repo, MULTI_SECTION_CHANGELOG)
    _write_anchor(repo)

    assert ss.set_topology() == 0

    out = capsys.readouterr().out
    assert "4.32.0-050-in_progress" in out


def test_set_topology_refuses_without_a_changelog(repo: Path, capsys: pytest.CaptureFixture):
    _write_anchor(repo)

    assert ss.set_topology() == 2
    assert "CHANGELOG.md" in capsys.readouterr().err


def test_set_topology_refuses_without_a_sealed_section(repo: Path, capsys: pytest.CaptureFixture):
    _write_changelog(repo, "# Changelog\n\n## [Unreleased]\n\n### Added\n- pending\n")
    _write_anchor(repo)

    assert ss.set_topology() == 2
    assert "sealed" in capsys.readouterr().err


def test_set_topology_refuses_without_current_sprint(repo: Path, capsys: pytest.CaptureFixture):
    _write_changelog(repo, MULTI_SECTION_CHANGELOG)
    _write_anchor(repo, {"current_sprint": {}})

    assert ss.set_topology() == 2
    assert "current_sprint" in capsys.readouterr().err


# --- CLI wiring --------------------------------------------------------------

def test_main_dispatches_set_topology(repo: Path, monkeypatch: pytest.MonkeyPatch):
    _write_changelog(repo, MULTI_SECTION_CHANGELOG)
    _write_anchor(repo)
    monkeypatch.setattr(sys, "argv", ["session_state.py", "set-topology"])

    assert ss.main() == 0

    state = json.loads((repo / "docs" / "active_state.json").read_text())
    assert state["topology_version"] == "4.32.0-050-in_progress"
