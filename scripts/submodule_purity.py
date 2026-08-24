"""Refuse to let a host session's work land inside the framework submodule.

`agents.md §3 strict_rule` forbids a host from altering the framework in place,
and `§4 feedback_upstream` routes framework-class findings to the nucleus
repository through a branch and a pull request. The doctrine was complete; the
enforcement was one sentence.

`close_workflow.md` Phase 5 `submodule_purity` said *"Verify
`git -C .agents status --porcelain` is clean"* and no script existed.
`scripts/scan_workflow_determinism.py` had been flagging that step in every
`make verify` run, unactioned. So the only protection against a host dirtying
`.agents` depended on an agent remembering to type a command.

**And until Sprint 024 the command was blind.** `git status --porcelain` does not
list ignored files, and `.gitignore` excluded `docs/sprints/`, `task_scope.md`,
`implementation_plan*` and the anchor — precisely the paths a host session
writes. Verified then: a file created under `docs/sprints/` left that command
completely empty. The exclusion meant to protect the submodule was hiding the
contamination from the only check built to catch it.

**Why "empty" needs no allowlist.** Everything legitimately transient inside
`.agents` is already ignored: `venv_skillopt/`, `graphify-out/`, `memory/`,
`.claude/`, the lock files, the anchor and its mirror. Anything that reaches
`--porcelain` is real content, so this check needs no severity scale and no
judgement.

**The answer it carries.** `config/abandoned_branches.json` records the doctrine
that a gate with no answer gets disabled rather than satisfied. There is no
legitimate dirty state to waive here, so the answer is in the message: contribute
upstream from a separate clone, stash an experiment, or — for a deliberate
version change — bump the gitlink in the host, which is not a dirty tree.

invoked_by: close_workflow.md#submodule_purity, hooks/on_commit.py.

Usage:
    python3 .agents/scripts/submodule_purity.py

Exit codes:
    0 — nucleus mode (nothing to protect), or the submodule is clean
    2 — a host session has content inside the framework (RA-11: only 2 blocks)
"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _mode import agents_dir, is_nucleus  # noqa: E402

UNTRACKED = "??"


def porcelain() -> list[str]:
    """Non-empty status lines for the framework tree, or [] when clean.

    `-uall` is not cosmetic. Plain `--porcelain` collapses an untracked tree to
    its top directory — a host writing `docs/sprints/085-backend-api/task_scope.md`
    reports as `?? docs/`, which tells the operator something is wrong and not
    what. The verdict is identical either way; the remedy is only actionable with
    the real paths, and this check exists to be acted on.
    """
    result = subprocess.run(
        ["git", "-C", str(agents_dir()), "status", "--porcelain", "-uall"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def classify(lines: list[str]) -> tuple[list[str], list[str]]:
    """Split status lines into untracked additions and edits to tracked files.

    The two are different failures with different remedies: an untracked file is
    a host session writing its own records into the wrong repository, while a
    modified tracked file is a host editing the framework in place, which is the
    `strict_rule` violation proper.

    Args:
        lines: `git status --porcelain` output lines.

    Returns:
        tuple: (untracked paths, modified tracked paths).
    """
    untracked, modified = [], []
    for line in lines:
        (untracked if line.startswith(UNTRACKED) else modified).append(line[3:].strip())
    return untracked, modified


def report(untracked: list[str], modified: list[str]) -> None:
    """Name what dirtied the submodule and the remedy for that specific case."""
    print("\n❌ This host session has content inside the framework submodule. "
          "`agents.md §3 strict_rule` forbids altering it in place.", file=sys.stderr)

    if modified:
        print(f"\n   {len(modified)} tracked framework file(s) modified:", file=sys.stderr)
        for path in modified[:10]:
            print(f"   • {path}", file=sys.stderr)
        print("     → A framework change belongs in the nucleus repository. Work it "
              "in a separate clone and open a pull request (`agents.md §4 "
              "feedback_upstream`); it reaches this host as a deliberate pin bump.",
              file=sys.stderr)

    if untracked:
        print(f"\n   {len(untracked)} untracked file(s) written into the submodule:",
              file=sys.stderr)
        for path in untracked[:10]:
            print(f"   • {path}", file=sys.stderr)
        print("     → A host sprint's records belong at the HOST root "
              "(`docs/sprints/[Sprint_ID]-[Stack]-[Layer]/`, `agents.md §5`), never "
              "inside `.agents/`. Move them, or remove them if they were written by "
              "a script run with the wrong working directory.", file=sys.stderr)

    print("\n   To park an experiment instead: `git -C .agents stash`.", file=sys.stderr)


def main() -> int:
    """Verify the framework submodule carries no host work.

    Returns:
        int: 0 in nucleus mode or when clean, 2 when a host has dirtied it.
    """
    if is_nucleus():
        # No submodule exists to protect, and the framework's own sprint records
        # belong here. A guard that fired inside its own jurisdiction would be
        # Sprint 024's `D7` defect rebuilt — the branch-sovereignty gate that
        # refused the very branch it was sealing.
        print("✅ Nucleus mode — the framework is the work; nothing to protect.")
        return 0

    lines = porcelain()
    if not lines:
        print("✅ Framework submodule is clean — no host work inside `.agents`.")
        return 0

    report(*classify(lines))
    return 2


if __name__ == "__main__":
    sys.exit(main())
