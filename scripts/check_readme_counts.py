"""Fail the build when the README's declared counts drift from the tree.

The README's "At a Glance" table states how many rule contexts, agents, skills,
workflows and slash commands the framework ships. Nothing recalculated them, so
they drifted silently and were corrected by hand — three times in a single
session, most recently when PR #29 updated a count in prose two sections below
the table and left the table itself saying `10 protocols … 11 slash commands`
while the tree held 12 and 13.

Only the five counts derivable from the tree are checked. The table also says
"8 phases (Planning → Sprint Closeout)", which is prose about a workflow's
internal structure rather than a countable set of files; pretending to verify
it would be the PR #28 defect — a check that reports success on something it
never actually measured.

**Framework-scoped, and it was not.** `close_workflow.md` Phase 2 runs this from
the HOST root, where every path below resolved against the host: `README.md`
became the host's README, `rules/` and `agents/` globbed empty, and
`skills/`.iterdir() raised. Measured from a directory holding only a host
README — `FileNotFoundError: 'skills'`, **exit 1**, not the exit 2 this docstring
and that workflow both promise. A mandatory close step had therefore never run
to completion in any host (`F-093-N2`). Sprint 023 `C1` anchors it.

invoked_by: Makefile `verify` target, close_workflow.md#readme_counts.

Usage:
    python3 scripts/check_readme_counts.py

Exit codes:
    0 — every declared count matches the tree
    2 — drift found (RA-11: 2 is what blocks)
"""

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root  # noqa: E402

README = Path("README.md")

# Each entry: label -> (regex capturing the declared number, actual count).
# The regexes are anchored on wording that carries meaning ("rule contexts",
# "agents in", "flat skills") rather than on position, so re-ordering the table
# does not silently disable a check.
CHECKS = {
    "rule contexts": (
        r"(\d+)\s+lazy-loaded domain rule contexts",
        lambda: len(list(Path("rules").glob("*.md"))),
    ),
    "agents": (
        r"(\d+)\s+role-segregated agents",
        lambda: len(list(Path("agents").glob("*.md"))),
    ),
    # `iterdir()` is deliberately not wrapped in try/except. Anchored to the
    # framework root these directories always exist, so an exception means a
    # broken checkout — and catching it would report 0 skills, which reads as
    # drift against the README rather than as the installation failure it is.
    # A crash names its own cause; a false count sends the reader to edit the
    # README until it agrees with a number that was never measured.
    "skills": (
        r"(\d+)\s+flat skills",
        lambda: len([p for p in Path("skills").iterdir() if p.is_dir()]),
    ),
    "workflows": (
        r"(\d+)\s+protocols in",
        lambda: len(list(Path("workflows").glob("*.md"))),
    ),
    "slash commands": (
        r"(\d+)\s+`/agents:\*` slash commands",
        lambda: len(list(Path("commands").glob("*.md"))),
    ),
}


def main() -> int:
    # Framework-scoped: the README and the five directories counted below are
    # this repository's, never the caller's. `close_workflow.md` invokes this
    # from the host root, which is why anchoring is the whole unit. See
    # `scripts/_root.py` for why the cwd is set rather than each path rewritten.
    os.chdir(agents_root())

    if not README.exists():
        print(f"❌ {README} not found inside {agents_root()}.", file=sys.stderr)
        return 2

    text = README.read_text(encoding="utf-8")
    errors = []

    for label, (pattern, counter) in CHECKS.items():
        match = re.search(pattern, text)
        actual = counter()
        if not match:
            # A claim that vanished is not a claim that passes: the README may
            # have been rewritten in a way this check no longer inspects.
            errors.append(f"{label}: no declared count found (tree has {actual}) "
                          f"— the check pattern no longer matches the README.")
            continue
        declared = int(match.group(1))
        if declared != actual:
            errors.append(f"{label}: README says {declared}, tree has {actual}.")

    if errors:
        print("❌ README counts have drifted from the tree:", file=sys.stderr)
        for error in errors:
            print(f"  • {error}", file=sys.stderr)
        return 2

    print("✅ README counts match the tree "
          + ", ".join(f"{label} {counter()}" for label, (_, counter) in CHECKS.items())
          + ".")
    return 0


if __name__ == "__main__":
    sys.exit(main())
