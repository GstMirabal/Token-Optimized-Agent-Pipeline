"""Detect work that happened outside the protocol, before trusting the anchor.

The case: commits were made without `start`, without `close`, or without
either. The recorded state and the repository then disagree, and every workflow
that follows reasons from a false premise.

This is not hypothetical. Five pull requests (#26-#30) were merged after tag
`v4.3.0` with no `CHANGELOG.md` entry, no roadmap phase record, and
`docs/active_state.json` frozen at sprint 017 dated 2026-07-27 while the work
continued to 2026-08-02. Nothing noticed, because nothing could: the anchor
recorded no commit to compare against.

`last_close_commit` — written by `session_state.py release` — is that missing
comparison point. Detection is then one command.

**Ordering matters.** This runs BEFORE `state_claim`, never after: claiming the
lock sets `status: IN_PROGRESS`, and a check keyed on the previous status would
read its own side effect. The check is deliberately status-agnostic for the
same reason — it compares commits, not state labels.

invoked_by: start_workflow.md#drift_check.

Usage:
    python3 scripts/detect_drift.py

Exit codes:
    0 — no drift, or no baseline yet to compare against
    2 — drift found: run /agents:reconcile before handing off to Planning
"""

import json
import subprocess
import sys
from pathlib import Path

ACTIVE_STATE = Path("docs/active_state.json")
CHANGELOG = Path("CHANGELOG.md")


def git(*args: str) -> str | None:
    result = subprocess.run(["git", *args], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def unreleased_is_empty() -> bool:
    """True when the Master Ledger has no entries under [Unreleased]."""
    if not CHANGELOG.exists():
        return False
    text = CHANGELOG.read_text(encoding="utf-8")
    if "## [Unreleased]" not in text:
        return False
    section = text.split("## [Unreleased]", 1)[1].split("\n## ", 1)[0]
    return not any(line.lstrip().startswith(("-", "*")) for line in section.splitlines())


def main() -> int:
    if not ACTIVE_STATE.exists():
        print("ℹ️  No state anchor yet — first session in this repository.")
        return 0

    try:
        state = json.loads(ACTIVE_STATE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("⚠️  State anchor is not valid JSON; the mirror is authoritative "
              "for crash recovery (start_workflow.md read_anchor).", file=sys.stderr)
        return 0

    baseline = state.get("last_close_commit")
    if not baseline:
        # Not an error: the field is written by the first close that runs with
        # it. Saying so is the point — silence here is what let the drift last.
        print("ℹ️  No `last_close_commit` baseline recorded yet. Drift cannot be "
              "measured until the next close writes one.")
        return 0

    if git("cat-file", "-e", f"{baseline}^{{commit}}") is None:
        print(f"⚠️  Recorded baseline {baseline[:7]} is not in this repository "
              f"(history rewritten, or a different clone). Drift not measured.",
              file=sys.stderr)
        return 0

    log = git("log", "--oneline", f"{baseline}..HEAD") or ""
    commits = [line for line in log.splitlines() if line]
    if not commits:
        print(f"✅ No drift — HEAD matches the last sealed close ({baseline[:7]}).")
        return 0

    print(f"❌ {len(commits)} commit(s) landed after the last sealed close "
          f"({baseline[:7]}), outside the protocol:", file=sys.stderr)
    for line in commits[:20]:
        print(f"   • {line}", file=sys.stderr)
    if len(commits) > 20:
        print(f"   … and {len(commits) - 20} more", file=sys.stderr)

    if unreleased_is_empty():
        print("\n   The Master Ledger's [Unreleased] section is empty, so none of "
              "it is recorded.", file=sys.stderr)

    print("\n   Run `/agents:reconcile` before handing off to Planning. New work "
          "on top of a state that misreports the repository multiplies the "
          "inconsistency instead of resolving it.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
