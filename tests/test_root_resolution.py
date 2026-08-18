"""Tests for scripts/_root.py and the framework-scoped scripts that adopt it.

Sprint 023 `C0.3`. Five scripts addressed `README.md`, `skills/`, `workflows/`,
`rules/` and `config/` as bare relative paths, so they audited whichever
directory the caller stood in.

Measured before the fix, each script copied out of the tree and run from an
empty directory — the three failure modes are different, and only one of them
is loud in the right way:

| Script | From another directory, before `C0.3` |
| :--- | :--- |
| `scan_workflow_determinism.py` | `[OK] no candidates found`, exit `0` — **a clean pass over nothing** |
| `verify_references.py` | Crash: `FileNotFoundError: agents.md` |
| `check_manifest_parity.py` | Exit `1`, *"run from the .agents root"* — a false failure that told the human to compensate for the defect |

`map_workflows.py` is not measurable that way, because copying the file
displaces the `__file__` its registry path is anchored to; its `workflows/` and
output paths were bare relative like the rest.

The unit's stated limit is that **no observable behaviour changes** — what
passes from the repository root must pass identically, and additionally pass
from anywhere else. That is one assertion, and it is the one below: same exit
code, same stdout, same stderr, from two different working directories.
"""
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import _mode  # noqa: E402
import branch_sovereignty as bs  # noqa: E402
import docs_freshness_check as dfc  # noqa: E402
from _root import agents_root  # noqa: E402

# `check_readme_counts.py` is deliberately absent: it is Sprint 023 unit `C1`,
# which anchors it alongside repairing its five counters. Listing it here would
# fail for a defect this unit does not claim to have fixed.
FRAMEWORK_SCOPED = [
    ["scripts/check_manifest_parity.py"],
    ["scripts/map_workflows.py", "--check"],
    ["scripts/scan_workflow_determinism.py"],
    ["scripts/verify_references.py"],
]


def test_the_root_is_the_directory_holding_the_ruleset():
    root = agents_root()
    assert (root / "agents.md").is_file()
    assert (root / "workflows").is_dir()
    assert (root / "config").is_dir()


def test_the_root_is_absolute_and_symlink_resolved():
    """`.resolve()` is load-bearing: `install_claude.sh` exposes commands and
    agents into a host's `.claude/` as symlinks, and an unresolved root would
    point at the link's directory instead of the real tree."""
    root = agents_root()
    assert root.is_absolute()
    assert root == root.resolve()


def test_mode_detection_still_answers_through_the_shared_root():
    """`_mode.agents_dir` was the same function under another name. The merge
    must not have left `is_nucleus` reading a different root than everything
    else."""
    assert _mode.is_nucleus() is (agents_root() / ".git").is_dir()
    assert not hasattr(_mode, "agents_dir"), "the renamed duplicate is still exported"


@pytest.mark.parametrize("argv", FRAMEWORK_SCOPED, ids=lambda a: Path(a[0]).stem)
def test_a_framework_scoped_script_is_identical_from_any_directory(argv, tmp_path):
    """The acceptance criterion of `C0.3`, stated as a comparison rather than
    as an exit code: an anchored script cannot tell where it was called from.

    Run against the tree before this unit, every one of these returns a
    different result from `tmp_path` than from the repository root: a crash, a
    false failure, or the worst of the three — `scan_workflow_determinism`
    reporting `[OK] no candidates found` over a directory holding no workflows.
    """
    command = [sys.executable, *argv]
    from_root = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    from_elsewhere = subprocess.run(
        [sys.executable, str(ROOT / argv[0]), *argv[1:]], cwd=tmp_path,
        capture_output=True, text=True,
    )

    assert from_elsewhere.returncode == from_root.returncode
    assert from_elsewhere.stdout == from_root.stdout
    assert from_elsewhere.stderr == from_root.stderr


def test_the_waiver_list_is_framework_data_not_wherever_the_caller_stood():
    """`branch_sovereignty` is the mixed case: it audits the host's git in the
    cwd and reads the framework's `config/`. As a bare relative path the waiver
    list was silently empty from any other directory, and a declared exception
    that is silently ignored reads exactly like no exception."""
    assert bs.WAIVERS.is_absolute()
    assert bs.WAIVERS == agents_root() / "config" / "abandoned_branches.json"


def test_the_denylists_are_found_in_nucleus_mode():
    """`.agents/scripts/denylists` is correct inside a host and names a
    directory that does not exist in the nucleus, so the three denylists that
    ship were never loaded here and the density filter ran empty."""
    assert dfc.DENYLIST_DIR.is_dir()
    assert {p.name for p in dfc.DENYLIST_DIR.glob("*.txt")} >= {"python.txt", "js.txt", "go.txt"}


def test_the_host_scoped_checker_still_reads_the_host_not_the_framework(tmp_path):
    """The inverse error, and the more dangerous one: anchoring a host-scoped
    script to `agents_root()` would make it audit the framework's documentation
    while reporting on the host's."""
    (tmp_path / "docs" / "sprints").mkdir(parents=True)
    report = dfc.FreshnessReport()
    dfc.check_phase_artifacts(tmp_path, 23, report)
    messages = " ".join(f.message for f in report.findings)
    assert "Phase 3 instantiates" in messages
