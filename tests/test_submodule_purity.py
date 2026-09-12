"""Tests for `scripts/submodule_purity.py` `--ignored` anchor scanning.

Sprint 047 unit U23, paired with U17's `fix(` for `scripts/submodule_purity.py`.

U17 taught the script a second, narrowly-scoped scan: `ignored_anchors()` runs
`git status --porcelain --ignored=matching` restricted to exactly
`ANCHOR_PATHS` (`docs/active_state.json`, `.agent_state/`) — the two paths a
misrooted submodule-mode session can write straight into `.agents/` while
plain `git status --porcelain` (no `--ignored`) stays blind to them, because
they are gitignored by design (`agents.md §5 state_anchor`). `main()` gained a
`scan_ignored` parameter and a nucleus short-circuit: in nucleus mode
`--ignored` returns 0 immediately, because the nucleus's own anchor is
legitimately gitignored-but-present there.

Against `HEAD`'s `submodule_purity.py` (no `ANCHOR_PATHS`, no
`ignored_anchors()`, no `--ignored` flag, `main()` takes no arguments) the
nucleus-short-circuit and submodule-block cases below raise `TypeError` on the
unexpected `scan_ignored` keyword rather than returning an exit code — they
FAIL against HEAD and pass with U17 applied.

A real throwaway git repository is built under `tmp_path` for every case here
rather than a mocked `subprocess.run`: this is a git-behavior-correctness unit
(the exact `--ignored=matching` pathspec mode against a real `.gitignore`),
and a mock cannot catch a wrong flag reproducing the wrong git behaviour.
Skipped outright when `git` is not on `PATH`.

invoked_by: Makefile verify via pytest tests/.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import submodule_purity as sp

GIT_AVAILABLE = shutil.which("git") is not None

pytestmark = pytest.mark.skipif(not GIT_AVAILABLE, reason="git is not available on PATH")


def _run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run a git command inside `cwd`, raising on a non-zero exit.

    Args:
        args: The full `git ...` argument vector.
        cwd: The repository directory to run it in.

    Returns:
        subprocess.CompletedProcess[str]: The completed process, text mode.
    """
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=True)


def _make_repo(root: Path) -> Path:
    """Initialize a throwaway git repo with a baseline commit and a `.gitignore`
    covering the anchor paths plus the other legitimately-ignored trees.

    Args:
        root: Directory to initialize as a git repository.

    Returns:
        Path: `root`, now a git repository with one commit.
    """
    _run(["git", "init", "-q"], root)
    _run(["git", "config", "user.email", "test@example.com"], root)
    _run(["git", "config", "user.name", "Test"], root)
    (root / ".gitignore").write_text(
        "docs/active_state.json\n"
        ".agent_state/\n"
        "venv_skillopt/\n"
        "graphify-out/\n"
        "memory/\n",
        encoding="utf-8",
    )
    (root / "README.md").write_text("# throwaway repo\n", encoding="utf-8")
    _run(["git", "add", "."], root)
    _run(["git", "commit", "-q", "-m", "baseline"], root)
    return root


def _write_anchor_file(repo: Path) -> None:
    """Write a gitignored `docs/active_state.json` into `repo`."""
    (repo / "docs").mkdir(exist_ok=True)
    (repo / "docs" / "active_state.json").write_text("{}", encoding="utf-8")


def _write_agent_state_dir(repo: Path) -> None:
    """Write a gitignored `.agent_state/` into `repo`."""
    (repo / ".agent_state").mkdir(exist_ok=True)
    (repo / ".agent_state" / "session.json").write_text("{}", encoding="utf-8")


def _write_both_anchors(repo: Path) -> None:
    """Write both stray anchor paths into `repo`."""
    _write_anchor_file(repo)
    _write_agent_state_dir(repo)


def test_ignored_scan_ignores_unrelated_ignored_trees(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Populated `venv_skillopt/`, `graphify-out/`, `memory/` beside a clean
    anchor state report nothing — `ANCHOR_PATHS` scopes the scan to exactly the
    two anchor paths, never the trees this check has no opinion on."""
    repo = _make_repo(tmp_path)
    (repo / "venv_skillopt" / "bin").mkdir(parents=True)
    (repo / "venv_skillopt" / "bin" / "python").write_text("x", encoding="utf-8")
    (repo / "graphify-out").mkdir()
    (repo / "graphify-out" / "graph.json").write_text("{}", encoding="utf-8")
    (repo / "memory").mkdir()
    (repo / "memory" / "note.md").write_text("x", encoding="utf-8")
    monkeypatch.setattr(sp, "agents_root", lambda: repo)

    assert sp.ignored_anchors() == []


@pytest.mark.parametrize(
    ("make_anchors", "expected_substrings"),
    [
        (_write_anchor_file, ("docs/active_state.json",)),
        (_write_agent_state_dir, (".agent_state/",)),
        (_write_both_anchors, ("docs/active_state.json", ".agent_state/")),
    ],
    ids=["anchor-file-alone", "agent-state-dir-alone", "both-anchors-together"],
)
def test_ignored_anchors_detects_stray_anchor_paths(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    make_anchors: Callable[[Path], None],
    expected_substrings: tuple[str, ...],
) -> None:
    """`ignored_anchors()` reports the anchor file alone, the anchor directory
    alone, and both together."""
    repo = _make_repo(tmp_path)
    make_anchors(repo)
    monkeypatch.setattr(sp, "agents_root", lambda: repo)

    found = sp.ignored_anchors()

    assert len(found) == len(expected_substrings)
    joined = " ".join(found)
    for substring in expected_substrings:
        assert substring in joined


def test_plain_scan_still_reports_modified_tracked_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Without `--ignored`, a modified tracked file inside the fake `.agents`
    dir is still reported — the existing `porcelain()`/`classify()`/`report()`
    path is byte-for-byte unchanged by the new anchor scan."""
    repo = _make_repo(tmp_path)
    (repo / "framework.py").write_text("value = 1\n", encoding="utf-8")
    _run(["git", "add", "framework.py"], repo)
    _run(["git", "commit", "-q", "-m", "add framework file"], repo)
    (repo / "framework.py").write_text("value = 2\n", encoding="utf-8")
    monkeypatch.setattr(sp, "agents_root", lambda: repo)
    monkeypatch.setattr(sp, "is_nucleus", lambda: False)

    exit_code = sp.main()
    captured = capsys.readouterr()

    assert exit_code == 2
    assert "framework.py" in captured.err


def test_plain_scan_exits_zero_when_clean(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Without `--ignored`, a clean fake `.agents` dir still exits 0."""
    repo = _make_repo(tmp_path)
    monkeypatch.setattr(sp, "agents_root", lambda: repo)
    monkeypatch.setattr(sp, "is_nucleus", lambda: False)

    assert sp.main() == 0


def test_ignored_scan_short_circuits_in_nucleus_mode(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`--ignored` in nucleus mode returns 0 immediately even with the
    nucleus's own anchor files present on disk. Fails against HEAD: `main()`
    there takes no `scan_ignored` argument at all."""
    repo = _make_repo(tmp_path)
    _write_both_anchors(repo)
    monkeypatch.setattr(sp, "agents_root", lambda: repo)
    monkeypatch.setattr(sp, "is_nucleus", lambda: True)

    assert sp.main(scan_ignored=True) == 0


def test_ignored_scan_blocks_in_submodule_mode_with_stray_anchor(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """`--ignored` in submodule mode with a stray gitignored anchor exits 2
    and names the anchor path. Fails against HEAD: the feature is absent."""
    repo = _make_repo(tmp_path)
    _write_anchor_file(repo)
    monkeypatch.setattr(sp, "agents_root", lambda: repo)
    monkeypatch.setattr(sp, "is_nucleus", lambda: False)

    exit_code = sp.main(scan_ignored=True)
    captured = capsys.readouterr()

    assert exit_code == 2
    assert "docs/active_state.json" in captured.err


def test_parse_args_defaults_ignored_false() -> None:
    """Default CLI parsing carries `ignored=False`."""
    args = sp._parse_args([])

    assert args.ignored is False


def test_parse_args_ignored_flag_sets_true() -> None:
    """`--ignored` on the command line sets `ignored=True`."""
    args = sp._parse_args(["--ignored"])

    assert args.ignored is True
