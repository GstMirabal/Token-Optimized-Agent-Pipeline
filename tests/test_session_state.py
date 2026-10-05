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
import session_state as ss

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


# --- claim: entry-point-aware refusal message (S052-2) ---------------------

def _write_locked_anchor(root: Path) -> None:
    """An anchor already IN_PROGRESS under a different session, so a
    same-process `claim()` call is refused (the collision this guard
    exists to prevent)."""
    state = {
        "session_id": "other-session",
        "status": ss.IN_PROGRESS,
        "current_sprint": {"id": 52, "status": "IN_PROGRESS"},
    }
    (root / "docs" / "active_state.json").write_text(json.dumps(state), encoding="utf-8")


def test_retry_hint_for_boot_entry_point():
    assert ss.retry_hint("boot") == "python3 scripts/session_start.py --boot --takeover"


def test_retry_hint_for_claim_entry_point():
    assert ss.retry_hint("claim") == "python3 scripts/session_state.py claim --takeover"


def test_retry_hint_defaults_to_claim_wording_for_unknown_values():
    assert ss.retry_hint("anything-else") == "python3 scripts/session_state.py claim --takeover"


def test_claim_refusal_names_boot_invocation_when_entry_point_is_boot(
    repo: Path, capsys: pytest.CaptureFixture
):
    _write_locked_anchor(repo)

    rc = ss.claim("me", False, "terminal", entry_point="boot")

    assert rc == 2
    err = capsys.readouterr().err
    assert "python3 scripts/session_start.py --boot --takeover" in err
    assert "session_state.py claim --takeover" not in err


def test_claim_refusal_names_claim_invocation_by_default(
    repo: Path, capsys: pytest.CaptureFixture
):
    _write_locked_anchor(repo)

    rc = ss.claim("me", False, "terminal")

    assert rc == 2
    err = capsys.readouterr().err
    assert "python3 scripts/session_state.py claim --takeover" in err
    assert "session_start.py --boot" not in err


def test_claim_refusal_names_claim_invocation_when_entry_point_is_claim(
    repo: Path, capsys: pytest.CaptureFixture
):
    _write_locked_anchor(repo)

    rc = ss.claim("me", False, "terminal", entry_point="claim")

    assert rc == 2
    err = capsys.readouterr().err
    assert "python3 scripts/session_state.py claim --takeover" in err


def test_claim_succeeds_with_takeover_regardless_of_entry_point(repo: Path):
    _write_locked_anchor(repo)

    rc = ss.claim("me", True, "terminal", entry_point="boot")

    assert rc == 0
    state = json.loads((repo / "docs" / "active_state.json").read_text())
    assert state["session_id"] == "me"
    assert state["status"] == ss.IN_PROGRESS


def test_main_claim_passes_entry_point_boot_into_refusal_message(
    repo: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
):
    _write_locked_anchor(repo)
    monkeypatch.setattr(
        sys, "argv",
        ["session_state.py", "claim", "--session-id", "me", "--entry-point", "boot"],
    )

    assert ss.main() == 2
    assert "session_start.py --boot --takeover" in capsys.readouterr().err


def test_main_claim_defaults_entry_point_to_claim(
    repo: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
):
    _write_locked_anchor(repo)
    monkeypatch.setattr(
        sys, "argv", ["session_state.py", "claim", "--session-id", "me"],
    )

    assert ss.main() == 2
    assert "session_state.py claim --takeover" in capsys.readouterr().err


# --- open-sprint (S052-4) ---------------------------------------------------

def test_open_sprint_writes_id_and_status_preserving_siblings(repo: Path):
    _write_anchor(repo, {
        "current_sprint": {"id": 51, "status": "CLOSED_SUCCESSFULLY",
                            "layer": "core", "app": "pipeline", "last_audit_sprint": 49},
    })

    assert ss.open_sprint(52) == 0

    state = json.loads((repo / "docs" / "active_state.json").read_text())
    assert state["current_sprint"] == {
        "id": 52, "status": "OPEN",
        "layer": "core", "app": "pipeline", "last_audit_sprint": 49,
    }


def test_open_sprint_creates_current_sprint_when_absent(repo: Path):
    _write_anchor(repo, {"current_sprint": {}})

    assert ss.open_sprint(52) == 0

    state = json.loads((repo / "docs" / "active_state.json").read_text())
    assert state["current_sprint"] == {"id": 52, "status": "OPEN"}


def test_open_sprint_refuses_in_progress_other_sprint(repo: Path, capsys: pytest.CaptureFixture):
    _write_anchor(repo, {
        "current_sprint": {"id": 51, "status": "IN_PROGRESS", "layer": "core"},
    })
    before = json.loads((repo / "docs" / "active_state.json").read_text())

    rc = ss.open_sprint(52)

    assert rc == 2
    err = capsys.readouterr().err
    assert "51" in err and "IN_PROGRESS" in err
    after = json.loads((repo / "docs" / "active_state.json").read_text())
    assert after == before


def test_open_sprint_same_id_is_idempotent(repo: Path):
    _write_anchor(repo, {
        "current_sprint": {"id": 52, "status": "OPEN", "layer": "core"},
    })
    before = json.loads((repo / "docs" / "active_state.json").read_text())

    rc = ss.open_sprint(52)

    assert rc == 0
    after = json.loads((repo / "docs" / "active_state.json").read_text())
    assert after == before


def test_open_sprint_same_id_is_idempotent_even_when_in_progress(repo: Path):
    """Same id never refuses — the `IN_PROGRESS` guard applies only to
    a *different* id (S052-4: "same id → idempotent exit 0")."""
    _write_anchor(repo, {
        "current_sprint": {"id": 52, "status": "IN_PROGRESS", "layer": "core"},
    })
    before = json.loads((repo / "docs" / "active_state.json").read_text())

    rc = ss.open_sprint(52)

    assert rc == 0
    after = json.loads((repo / "docs" / "active_state.json").read_text())
    assert after == before


def test_open_sprint_exits_0_and_prints_confirmation(repo: Path, capsys: pytest.CaptureFixture):
    _write_anchor(repo, {"current_sprint": {"id": 51, "status": "CLOSED_SUCCESSFULLY"}})

    assert ss.open_sprint(52) == 0
    assert "52" in capsys.readouterr().out


def test_main_dispatches_open_sprint(repo: Path, monkeypatch: pytest.MonkeyPatch):
    _write_anchor(repo, {"current_sprint": {"id": 51, "status": "CLOSED_SUCCESSFULLY"}})
    monkeypatch.setattr(sys, "argv", ["session_state.py", "open-sprint", "--id", "52"])

    assert ss.main() == 0

    state = json.loads((repo / "docs" / "active_state.json").read_text())
    assert state["current_sprint"]["id"] == 52
    assert state["current_sprint"]["status"] == "OPEN"


def test_main_open_sprint_propagates_refusal_exit_code(
    repo: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
):
    _write_anchor(repo, {"current_sprint": {"id": 51, "status": "IN_PROGRESS"}})
    monkeypatch.setattr(sys, "argv", ["session_state.py", "open-sprint", "--id", "52"])

    assert ss.main() == 2
    assert "IN_PROGRESS" in capsys.readouterr().err


# --- open-sprint: sealed-vs-unsealed refusal (F-3, S052 QA Gate 1) ----------

def test_open_sprint_refuses_a_second_call_over_its_own_unsealed_open(
    repo: Path, capsys: pytest.CaptureFixture
):
    """Reproduces the live defect: nothing writes `current_sprint.status`
    to `IN_PROGRESS`, so `open_sprint()` itself is the only real writer —
    and its own output (`status: "OPEN"`) must not read as sealed. Fails on
    HEAD: the old guard (`current_status == IN_PROGRESS`) never matches
    `"OPEN"`, so `open_sprint(53)` used to succeed silently over an
    unclosed sprint 52 that `open_sprint(52)` itself opened."""
    assert ss.open_sprint(52) == 0
    before = json.loads((repo / "docs" / "active_state.json").read_text())

    rc = ss.open_sprint(53)

    assert rc == 2
    err = capsys.readouterr().err
    assert "52" in err
    after = json.loads((repo / "docs" / "active_state.json").read_text())
    assert after == before


def test_release_writes_current_sprint_status_closed_preserving_siblings(repo: Path):
    """The SPRINT fact `_sprint_is_sealed` reads — a `current_sprint` sibling
    key (`layer`), not a field `open_sprint()` owns, must survive untouched."""
    _write_anchor(repo, {"current_sprint": {"id": 52, "status": "OPEN", "layer": "core"}})

    assert ss.release() == 0

    state = json.loads((repo / "docs" / "active_state.json").read_text())
    assert state["current_sprint"] == {"id": 52, "status": "CLOSED_SUCCESSFULLY", "layer": "core"}


def test_release_does_not_add_current_sprint_when_absent(repo: Path):
    """`release()` must not invent a `current_sprint` the anchor never had."""
    (repo / "docs" / "active_state.json").write_text(
        json.dumps({"session_id": "keep-me"}), encoding="utf-8"
    )

    assert ss.release() == 0

    state = json.loads((repo / "docs" / "active_state.json").read_text())
    assert "current_sprint" not in state


def test_open_sprint_succeeds_after_release_then_a_new_session_claims(repo: Path):
    """The exact flow this fix protects: sprint 52 opened, released — sealed
    as a SPRINT fact — then a *new* session `claim`s (which resets the
    top-level SESSION status back to `IN_PROGRESS`) before Phase 3 opens
    sprint 53. Regression guard for the round-1 fix, which keyed sealed-ness
    on that top-level field and would have refused this exact call."""
    assert ss.open_sprint(52) == 0
    assert ss.release() == 0
    assert ss.claim("next-session", False, "terminal") == 0

    rc = ss.open_sprint(53)

    assert rc == 0
    state = json.loads((repo / "docs" / "active_state.json").read_text())
    assert state["status"] == ss.IN_PROGRESS  # claim() reset it; must not matter
    assert state["current_sprint"]["id"] == 53
    assert state["current_sprint"]["status"] == "OPEN"


def test_open_sprint_refuses_after_claim_without_a_release_between(
    repo: Path, capsys: pytest.CaptureFixture
):
    """A new session claiming the lock must not, by itself, read as a seal:
    sprint 52 was opened but never released before `open_sprint(53)` runs."""
    assert ss.open_sprint(52) == 0
    assert ss.claim("some-session", False, "terminal") == 0
    before = json.loads((repo / "docs" / "active_state.json").read_text())

    rc = ss.open_sprint(53)

    assert rc == 2
    err = capsys.readouterr().err
    assert "52" in err
    after = json.loads((repo / "docs" / "active_state.json").read_text())
    assert after == before


# --- CLI wiring --------------------------------------------------------------

# --- open-sprint: legacy seal alias (KI-052-2, Sprint 053 A1) ---------------

def test_sealed_statuses_contains_both_the_canonical_and_legacy_literal():
    assert {"CLOSED_SUCCESSFULLY", "CLOSED"} <= ss.SEALED_STATUSES


def test_sealed_statuses_contains_the_host_written_deployed_status():
    """`DEPLOYED` is written by a host after merge and tag (F-114-N2, D9)."""
    assert "DEPLOYED" in ss.SEALED_STATUSES


def test_open_sprint_accepts_a_host_written_deployed_status(repo: Path):
    """A host's deployment step moves `current_sprint.status` past
    `CLOSED_SUCCESSFULLY` to `DEPLOYED`; refusing it blocks every later sprint."""
    _write_anchor(repo, {"current_sprint": {"id": 7, "status": "DEPLOYED"}})

    rc = ss.open_sprint(8)

    assert rc == 0
    state = json.loads((repo / "docs" / "active_state.json").read_text())
    assert state["current_sprint"]["id"] == 8
    assert state["current_sprint"]["status"] == "OPEN"


def test_open_sprint_still_refuses_an_open_sprint(
    repo: Path, capsys: pytest.CaptureFixture
):
    """Regression guard: widening the sealed set must not admit `OPEN`."""
    _write_anchor(repo, {"current_sprint": {"id": 7, "status": "OPEN"}})

    rc = ss.open_sprint(8)

    assert rc == 2
    assert "7" in capsys.readouterr().err


def test_open_sprint_accepts_a_legacy_closed_alias(repo: Path):
    """`release()` wrote the bare `"CLOSED"` literal before Sprint 050;
    every host that sealed a sprint under that pin carries it in its anchor.
    Fails on HEAD: `_sprint_is_sealed` compares only against
    `CLOSED_SUCCESSFULLY`, so a legacy anchor refuses forever."""
    _write_anchor(repo, {"current_sprint": {"id": 51, "status": "CLOSED"}})

    rc = ss.open_sprint(52)

    assert rc == 0
    state = json.loads((repo / "docs" / "active_state.json").read_text())
    assert state["current_sprint"]["id"] == 52
    assert state["current_sprint"]["status"] == "OPEN"


def test_open_sprint_refuses_missing_status_and_names_release(
    repo: Path, capsys: pytest.CaptureFixture
):
    """A `current_sprint` with an `id` but no `status` key is genuinely
    unknown — possibly live — and must stay refused, naming the one-command
    remediation."""
    _write_anchor(repo, {"current_sprint": {"id": 51}})

    rc = ss.open_sprint(52)

    assert rc == 2
    err = capsys.readouterr().err
    assert "python3 scripts/session_state.py release" in err


def test_main_dispatches_set_topology(repo: Path, monkeypatch: pytest.MonkeyPatch):
    _write_changelog(repo, MULTI_SECTION_CHANGELOG)
    _write_anchor(repo)
    monkeypatch.setattr(sys, "argv", ["session_state.py", "set-topology"])

    assert ss.main() == 0

    state = json.loads((repo / "docs" / "active_state.json").read_text())
    assert state["topology_version"] == "4.32.0-050-in_progress"
