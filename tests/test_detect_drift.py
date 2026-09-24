"""Tests for scripts/detect_drift.py — the routine `docs(state)` exclusion.

`F-BOOT-4`: every close and deployment appends a commit touching only
`docs/active_state.json` after `last_close_commit`. With `[Unreleased]` empty
those read as drift (verdict `U`/`A`) and force a no-op `/agents:reconcile` on
every session in between. They are outside the drift range by construction; a
commit that also touches another file, or one without the `docs(state)`
subject, is still counted.

Sprint 051 adds the second exclusion, on a different axis: commits that have
not reached the integration branch. `RA-12` puts every sprint on
`ai-sprint/[ID]` and `RA-05` puts its ledger entry at Sprint Closeout, so
in-flight work is correctly unrecorded and must not block. What must still
block is unrecorded work that already landed — the `PRs #26-#30` failure this
check exists for — and the last three tests assert that boundary from both
sides.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import detect_drift as dd


@pytest.fixture
def repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A real repository — these checks are about git semantics."""
    monkeypatch.chdir(tmp_path)

    def run(*args: str) -> None:
        subprocess.run(
            ["git", *args], cwd=tmp_path, check=True, capture_output=True, text=True
        )

    run("init", "-q", "-b", "main")
    run("config", "user.email", "t@example.com")
    run("config", "user.name", "T")
    (tmp_path / "f.txt").write_text("base\n")
    run("add", "-A")
    run("commit", "-qm", "base")
    (tmp_path / "docs").mkdir()
    return tmp_path


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repo, check=True, capture_output=True, text=True
    ).stdout.strip()


def _head(repo: Path) -> str:
    return _git(repo, "rev-parse", "HEAD")


def _commit_all(repo: Path, message: str) -> None:
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", message)


def _commit_state_only(repo: Path, message: str) -> None:
    """Commit only docs/active_state.json (staging that path alone)."""
    _git(repo, "add", "docs/active_state.json")
    _git(repo, "commit", "-qm", message)


def _write_anchor(repo: Path, **fields: object) -> None:
    (repo / "docs" / "active_state.json").write_text(json.dumps(fields))


def test_single_routine_state_commit_reads_clean(repo: Path) -> None:
    """The F-BOOT-4 case: the only commit past the baseline is a docs(state) write.

    Against the pre-Sprint-044 tree this is verdict `R` and exits 2.
    """
    baseline = _head(repo)
    _write_anchor(repo, status="X", last_close_commit=baseline)
    _commit_state_only(repo, "docs(state): open Sprint 099")
    assert dd.main() == 0


def test_a_docs_state_commit_that_also_touches_code_is_still_drift(repo: Path) -> None:
    """Both conditions are required — a smuggled file change is still counted."""
    baseline = _head(repo)
    _write_anchor(repo, status="X", last_close_commit=baseline)
    (repo / "f.txt").write_text("smuggled change\n")
    _commit_all(repo, "docs(state): open Sprint 099")
    assert dd.main() == 2


def test_a_state_only_commit_without_the_docs_state_subject_is_still_drift(
    repo: Path,
) -> None:
    """Subject must match `^docs\\(state\\)` — a state-only chore is still counted."""
    baseline = _head(repo)
    _write_anchor(repo, status="X", last_close_commit=baseline)
    _commit_state_only(repo, "chore: fiddle with the anchor")
    assert dd.main() == 2


def test_a_routine_commit_does_not_hide_a_real_one(repo: Path) -> None:
    """A routine state commit is dropped; a real out-of-protocol commit is not."""
    baseline = _head(repo)
    _write_anchor(repo, status="X", last_close_commit=baseline)
    _commit_state_only(repo, "docs(state): open Sprint 099")
    (repo / "g.txt").write_text("out of protocol\n")
    _commit_all(repo, "add g outside the protocol")
    assert dd.main() == 2


def test_routine_shas_helper_identifies_only_the_state_only_docs_commit(
    repo: Path,
) -> None:
    """Unit-level: `_routine_state_shas` picks the one qualifying commit."""
    _write_anchor(repo, status="X")
    _commit_state_only(repo, "docs(state): first")
    sha_routine = _head(repo)[:9]
    (repo / "f.txt").write_text("real\n")
    _commit_all(repo, "docs(state): but also code")
    lines = subprocess.run(
        ["git", "log", "--oneline", "-2"],
        cwd=repo, capture_output=True, text=True, check=True,
    ).stdout.splitlines()
    routine = dd._routine_state_shas(lines)
    assert len(routine) == 1
    assert next(iter(routine)).startswith(sha_routine[:7])


# --- Sprint 051: the in-flight half of the range is listed, never blocking ----


def _seal(repo: Path, version: str = "1.0.0") -> None:
    """A ledger with a non-empty `[Unreleased]` plus one released section, tagged.

    Both are required to reach verdict `A`: `sealing_tags` only counts a tag
    whose version owns a section, and `A` is the verdict that fires when
    `[Unreleased]` is not empty. Without this setup the fixture reaches `R`,
    which exits 2 for a different reason and would not test the split.
    """
    (repo / "CHANGELOG.md").write_text(
        "# Changelog\n\n"
        "## [Unreleased]\n\n- an entry, so the section is not empty\n\n"
        f"## [{version}] - 2026-01-01\n\n- sealed\n",
        encoding="utf-8",
    )
    _commit_all(repo, "docs(changelog): seal")
    _git(repo, "tag", f"v{version}")


def test_in_flight_sprint_commits_do_not_block(repo: Path) -> None:
    """RA-12 work on `ai-sprint/[ID]` is not drift: its entry is due at close.

    Against the pre-Sprint-051 tree this is verdict `A` and exits 2, which is
    what stopped a host's boot before its briefing could deliver the
    Documentation Entry Point.
    """
    _seal(repo)
    baseline = _head(repo)
    _write_anchor(repo, status="X", last_close_commit=baseline)
    _git(repo, "checkout", "-q", "-b", "ai-sprint/051")
    (repo / "design.md").write_text("in-flight sprint work\n")
    _commit_all(repo, "docs(design): sprint work not yet merged")
    assert dd.main() == 0


def test_landed_unrecorded_work_still_blocks_from_a_sprint_branch(repo: Path) -> None:
    """The `PRs #26-#30` failure: unrecorded work ON the integration branch.

    Checked out on a sprint branch, so it proves the split does not let a
    sprint branch launder a commit that already reached `main`.
    """
    _seal(repo)
    baseline = _head(repo)
    _write_anchor(repo, status="X", last_close_commit=baseline)
    (repo / "landed.txt").write_text("merged but never recorded\n")
    _commit_all(repo, "feat: landed on main with no ledger entry")
    _git(repo, "checkout", "-q", "-b", "ai-sprint/051")
    assert dd.main() == 2


def test_a_sprint_branch_does_not_hide_a_landed_commit(repo: Path) -> None:
    """Mixed range: one landed and unrecorded, one in flight. Only one blocks."""
    _seal(repo)
    baseline = _head(repo)
    _write_anchor(repo, status="X", last_close_commit=baseline)
    (repo / "landed.txt").write_text("merged but never recorded\n")
    _commit_all(repo, "feat: landed on main with no ledger entry")
    landed = _head(repo)[:7]
    _git(repo, "checkout", "-q", "-b", "ai-sprint/051")
    (repo / "design.md").write_text("in-flight sprint work\n")
    _commit_all(repo, "docs(design): sprint work not yet merged")
    in_flight = _head(repo)[:7]

    verdict, every, unsealed, _tags, flight = dd.classify(baseline)
    assert verdict == "A"
    assert [c.split()[0] for c in unsealed] == [landed]
    assert [c.split()[0] for c in every] == [landed]
    assert [c.split()[0] for c in flight] == [in_flight]
    assert dd.main() == 2


def test_integration_refs_is_empty_when_head_is_the_integration_branch(
    repo: Path,
) -> None:
    """On `main` there is no in-flight half, so the pre-051 path runs unchanged."""
    assert _git(repo, "rev-parse", "--abbrev-ref", "HEAD") == "main"
    assert dd.integration_refs() == []
    _git(repo, "checkout", "-q", "-b", "ai-sprint/051")
    assert dd.integration_refs() == ["main"]


def test_a_stale_local_branch_cannot_hide_work_that_landed_on_its_remote(
    repo: Path,
) -> None:
    """Gate 1's `charter` finding, pinned.

    The first form of `integration_ref` tried the local branch before `origin/`
    and returned the first that resolved. In a clone whose local `main` is behind
    `origin/main` — the normal state of a clone that has not pulled — a commit
    already on `origin/main` was absent from the ref consulted, read as in
    flight, and dropped from the half that blocks. That is the `PRs #26-#30`
    failure, reintroduced by the fix meant to sharpen it.
    """
    _seal(repo)
    baseline = _head(repo)
    _write_anchor(repo, status="X", last_close_commit=baseline)

    # A remote whose `main` carries a commit the local `main` has not caught up to.
    remote = repo.parent / "remote.git"
    _git(repo, "init", "-q", "--bare", str(remote))
    _git(repo, "remote", "add", "origin", str(remote))
    (repo / "landed.txt").write_text("landed on the remote\n")
    _commit_all(repo, "feat: landed on the integration branch, unrecorded")
    _git(repo, "push", "-q", "origin", "main")
    _git(repo, "fetch", "-q", "origin")
    # Leave `main` before rewinding it: git refuses `branch -f` on the checked-out
    # branch. Then local `main` sits behind `origin/main`, which is the state
    # under test.
    _git(repo, "checkout", "-q", "-b", "ai-sprint/051")
    _git(repo, "branch", "-f", "main", baseline)

    assert "origin/main" in dd.integration_refs()
    # Absent from the stale local `main`, present on `origin/main` — so NOT in
    # flight, and the verdict must still block.
    assert dd.classify(baseline)[4] == []
    assert dd.main() == 2


def test_a_citation_inside_a_longer_hex_run_does_not_clear_a_commit(
    repo: Path,
) -> None:
    """Gate 1's `F-2`: a substring test matched a different commit's SHA."""
    _seal(repo)
    baseline = _head(repo)
    _write_anchor(repo, status="X", last_close_commit=baseline)
    (repo / "landed.txt").write_text("landed on main\n")
    _commit_all(repo, "feat: landed on main")
    sha = _head(repo)[:7]
    # A longer hex run that CONTAINS the short sha but starts one nibble earlier.
    _add_unreleased_entry(repo, f"unrelated blob `0{sha}`")
    _commit_all(repo, "docs(changelog): an entry citing something else")

    verdict, _every, unsealed, _tags, _flight = dd.classify(baseline)
    assert verdict == "A"
    assert len(unsealed) == 1
    assert dd.main() == 2


# --- Sprint 051: landed work that the ledger already accounts for -------------


def _add_unreleased_entry(repo: Path, text: str) -> None:
    """Append one bullet under `## [Unreleased]`, leaving the file otherwise alone."""
    path = repo / "CHANGELOG.md"
    body = path.read_text(encoding="utf-8")
    path.write_text(
        body.replace("## [Unreleased]\n", f"## [Unreleased]\n\n- {text}\n", 1),
        encoding="utf-8",
    )


def test_a_ledger_maintenance_commit_cannot_appear_in_the_ledger_it_writes(
    repo: Path,
) -> None:
    """`reconciliation_workflow.md` Phase 3 produces exactly this commit.

    The reporting host had the commit that authored an `[Unreleased]` entry
    flagged as uncovered by that same entry, on every session afterwards.
    """
    _seal(repo)
    baseline = _head(repo)
    _write_anchor(repo, status="X", last_close_commit=baseline)
    _add_unreleased_entry(repo, "reconstructed entry")
    _commit_all(repo, "docs(changelog): reconstruct the missing entry")
    assert dd.main() == 0


def test_a_changelog_commit_that_also_touches_code_is_still_drift(repo: Path) -> None:
    """The exemption needs both halves; a mis-subjected commit is still counted."""
    _seal(repo)
    baseline = _head(repo)
    _write_anchor(repo, status="X", last_close_commit=baseline)
    _add_unreleased_entry(repo, "an entry")
    (repo / "code.txt").write_text("and code\n")
    _commit_all(repo, "docs(changelog): but also code")
    assert dd.main() == 2


def test_an_unreleased_entry_naming_the_commit_is_per_commit_proof(
    repo: Path,
) -> None:
    """Verdict C: citation is the evidence reachability cannot supply."""
    _seal(repo)
    baseline = _head(repo)
    _write_anchor(repo, status="X", last_close_commit=baseline)
    (repo / "landed.txt").write_text("landed on main\n")
    _commit_all(repo, "feat: landed on main")
    sha = _head(repo)[:7]
    _add_unreleased_entry(repo, f"landed in `{sha}`")
    _commit_all(repo, "docs(changelog): record the landed commit")

    verdict, _every, unsealed, _tags, _flight = dd.classify(baseline)
    assert verdict == "C"
    assert unsealed == []
    assert dd.main() == 0


def test_an_unreleased_entry_that_names_nothing_still_asks_a_human(
    repo: Path,
) -> None:
    """Verdict A survives: a non-empty section is not proof about a given commit."""
    _seal(repo)
    baseline = _head(repo)
    _write_anchor(repo, status="X", last_close_commit=baseline)
    (repo / "landed.txt").write_text("landed on main\n")
    _commit_all(repo, "feat: landed on main")
    _add_unreleased_entry(repo, "something happened, unattributed")
    _commit_all(repo, "docs(changelog): an entry naming no commit")

    verdict, _every, unsealed, _tags, _flight = dd.classify(baseline)
    assert verdict == "A"
    assert len(unsealed) == 1
    assert dd.main() == 2


# --- Sprint 051 Gate 1 round 2 (`G2-3`): every verdict asserted directly -------
#
# `main()` collapses CLEAN/S/C to exit 0 and R/U/M/A to exit 2, so a
# verdict-identity regression is invisible through the CLI. This sprint made that
# exact argument about `check_task_scope.py` (`F-051-R2`) and had not applied it
# to the file it claimed three times.


def _ledger(repo: Path, version: str = "1.0.0", unreleased: str = "") -> None:
    """A ledger whose `[Unreleased]` is empty unless `unreleased` is given."""
    (repo / "CHANGELOG.md").write_text(
        "# Changelog\n\n"
        f"## [Unreleased]\n\n{unreleased}\n"
        f"## [{version}] - 2026-01-01\n\n- sealed\n",
        encoding="utf-8",
    )
    _git(repo, "add", "CHANGELOG.md")
    _git(repo, "commit", "-qm", "docs(changelog): ledger")


def test_verdict_clean_when_the_range_is_empty(repo: Path) -> None:
    _write_anchor(repo, status="X", last_close_commit=_head(repo))
    assert dd.classify(_head(repo))[0] == "CLEAN"


def test_verdict_r_when_no_tag_owns_a_released_section(repo: Path) -> None:
    """Unproven coverage is not coverage — `R` blocks for that reason."""
    baseline = _head(repo)
    _write_anchor(repo, status="X", last_close_commit=baseline)
    (repo / "g.txt").write_text("work\n")
    _commit_all(repo, "feat: unprovable")
    assert dd.classify(baseline)[0] == "R"
    assert dd.main() == 2


def test_verdict_s_when_a_sealing_tag_reaches_every_commit(repo: Path) -> None:
    baseline = _head(repo)
    _write_anchor(repo, status="X", last_close_commit=baseline)
    (repo / "g.txt").write_text("work\n")
    _commit_all(repo, "feat: sealed work")
    _ledger(repo)
    _git(repo, "tag", "v1.0.0")
    assert dd.classify(baseline)[0] == "S"
    assert dd.main() == 0


def test_verdict_u_when_every_commit_is_unsealed_and_unreleased_is_empty(
    repo: Path,
) -> None:
    baseline = _head(repo)
    _write_anchor(repo, status="X", last_close_commit=baseline)
    _ledger(repo)
    _git(repo, "tag", "v1.0.0")
    (repo / "g.txt").write_text("work\n")
    _commit_all(repo, "feat: after the tag")
    verdict, every, unsealed, _tags, _flight = dd.classify(baseline)
    assert verdict == "U"
    assert len(unsealed) == len(every) == 1


def test_verdict_m_when_only_some_commits_are_unsealed(repo: Path) -> None:
    baseline = _head(repo)
    _write_anchor(repo, status="X", last_close_commit=baseline)
    (repo / "a.txt").write_text("first\n")
    _commit_all(repo, "feat: before the tag")
    _ledger(repo)
    _git(repo, "tag", "v1.0.0")
    (repo / "b.txt").write_text("second\n")
    _commit_all(repo, "feat: after the tag")
    verdict, every, unsealed, _tags, _flight = dd.classify(baseline)
    assert verdict == "M"
    assert len(unsealed) < len(every)
