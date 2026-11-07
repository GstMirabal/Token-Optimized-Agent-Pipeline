"""Report prose lost from a sprint's records across a commit range (plan D34).

`rules/documentation_standard.md` requires superseded prose to be annotated in
place, never deleted. This check covers three zones and makes no claim beyond
them:

1. KI rows of `SPRINT_LOG.md` (a table row whose last cell is a `KI-n-n` id):
   a commit that touches the log may not drop a word of a row, nor the row. The
   comparison is a word multiset, so reordered words or a changed meaning that
   keeps every word are NOT detected.
2. Sentences after `error_mining` in `SPRINT_LOG.md`, wherever the line sits:
   each one must survive verbatim somewhere in the log of that commit.
3. Decision rows of `IMPLEMENTATION_PLAN.md` at the range end: a row saying
   `sustituye a Dn` requires row `Dn` to open with a bold `Sustituida` or
   `Ampliada` mark. The pattern matches the Spanish wording plans use; any other
   wording is NOT detected.

Waiver: a commit that must delete (host data under `RA-15`, a false figure)
carries the trailer `Log-Rewrite: <reason>`. Its losses are printed and do not
fail. An empty reason waives nothing. Zone 3 has no waiver.

A record absent at the range end is reported and skipped: a log deleted inside
the range still fails zones 1 and 2, because the deleting commit is compared.

invoked_by: Makefile `verify` target (`--current-sprint`), which applies it to
sprint ids >= 60 (`ENFORCED_FROM`). Sprint 059 QA Gate 1 passes `--range` by hand.

Usage:
    python3 scripts/check_log_append_only.py --current-sprint
    python3 scripts/check_log_append_only.py --sprint-dir <dir> --range <base>..<end>

Exit codes:
    0 - no unwaived loss, or nothing to check
    2 - an unwaived loss, an unmarked decision row, or a git/range failure
        (fail closed on error)
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root
from check_task_scope import current_sprint_dir, sprint_id_from_dir

ENFORCED_FROM = 60
LOG_NAME = "SPRINT_LOG.md"
PLAN_NAME = "IMPLEMENTATION_PLAN.md"
MINING_TOKEN = "error_mining"
WAIVER_KEY = "Log-Rewrite"
KI_ROW_RE = re.compile(r"^\|.*\|\s*(KI-\d+-\d+)\s*\|\s*$")
WORD_RE = re.compile(r"[\w`.-]+")
SENTENCE_END_RE = re.compile(r"(?<=\.)\s+")
DECISION_ROW_RE = re.compile(r"^\|\s*(D\d+)\s*\|(.*)$")
# Spanish on purpose: these match plan text, the one artifact written in Spanish.
SUPERSEDES_RE = re.compile(r"sustituy\w*\s+a\s+`?(D\d+)\b", re.IGNORECASE)
MARK_RE = re.compile(r"^\s*\*\*(Sustituida|Ampliada)\b")


def _git(root: Path, *args: str) -> str:
    """Run git in `root` and return stdout; a failure raises CalledProcessError."""
    done = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True, check=True,
    )
    return done.stdout


def _blob(root: Path, rev: str, path: str) -> str | None:
    """Return the file at `rev`, or None when that revision does not hold it."""
    spec = f"{rev}:{path}"
    probe = subprocess.run(
        ["git", "cat-file", "-e", spec], cwd=root, capture_output=True, check=False,
    )
    return _git(root, "show", spec) if probe.returncode == 0 else None


def ki_rows(text: str) -> dict[str, str]:
    """Map each KI id to its table row."""
    matches = ((KI_ROW_RE.match(line), line) for line in text.splitlines())
    return {m.group(1): line for m, line in matches if m}


def ki_losses(old: str, new: str) -> list[str]:
    """Describe KI rows of `old` that lost words or vanished in `new`."""
    current = ki_rows(new)
    losses: list[str] = []
    for key, row in ki_rows(old).items():
        before = Counter(WORD_RE.findall(row))
        lost = before - Counter(WORD_RE.findall(current.get(key, "")))
        if lost:
            losses.append(f"{key}: lost {sum(lost.values())} of {sum(before.values())} words")
    return losses


def mining_sentences(text: str) -> list[str]:
    """Return each sentence from `error_mining` to the end of its line."""
    found: list[str] = []
    for line in text.splitlines():
        at = line.find(MINING_TOKEN)
        if at >= 0:
            found.extend(s for s in SENTENCE_END_RE.split(line[at:].strip()) if s)
    return found


def mining_losses(old: str, new: str) -> list[str]:
    """Describe `error_mining` sentences of `old` absent from `new`."""
    return [
        f"{MINING_TOKEN} sentence gone: {sentence[:80]}"
        for sentence in mining_sentences(old)
        if sentence not in new
    ]


def unmarked_decisions(plan: str) -> list[str]:
    """Describe decision rows a later row supersedes that carry no mark."""
    rows = {m.group(1): m.group(2) for m in map(DECISION_ROW_RE.match, plan.splitlines()) if m}
    problems: list[str] = []
    for source, body in rows.items():
        problems.extend(
            f"{target}: superseded by {source}, no Sustituida/Ampliada mark"
            for target in SUPERSEDES_RE.findall(body)
            if not MARK_RE.match(rows.get(target, ""))
        )
    return problems


def _commit_failures(root: Path, commit: str, log_path: str) -> list[str]:
    """Compare one commit's log with its parent; print waived losses, return the rest."""
    old = _blob(root, f"{commit}^", log_path) or ""
    new = _blob(root, commit, log_path) or ""
    losses = ki_losses(old, new) + mining_losses(old, new)
    if not losses:
        return []
    short = commit[:7]
    key = f"%(trailers:key={WAIVER_KEY},valueonly)"
    reason = _git(root, "log", "-1", f"--format={key}", commit).strip()
    if reason:
        for loss in losses:
            print(f"WAIVED {short} {loss} ({WAIVER_KEY}: {reason})")
        return []
    return [f"{short} {loss}" for loss in losses]


def check(root: Path, sprint_dir: str, rng: str) -> int:
    """Run the three zones over `rng`.

    Args:
        root: repository root.
        sprint_dir: sprint directory relative to `root`, with forward slashes.
        rng: a `<base>..<end>` git range.

    Returns:
        int: 0 when clean, 2 on any unwaived loss or unmarked decision row.
    """
    log_path = f"{sprint_dir}/{LOG_NAME}"
    end = rng.split("..", 1)[1] or "HEAD"
    commits = _git(root, "rev-list", "--reverse", rng, "--", log_path).split()
    failures = [f for c in commits for f in _commit_failures(root, c, log_path)]
    plan = _blob(root, end, f"{sprint_dir}/{PLAN_NAME}")
    if plan is None:
        print(f"check_log_append_only: no {PLAN_NAME} at {end} (zone 3 skipped)")
    failures.extend(unmarked_decisions(plan or ""))
    if _blob(root, end, log_path) is None and not commits:
        print(f"check_log_append_only: no {LOG_NAME} at {end} (zones 1 and 2 skipped)")
    for failure in failures:
        print(f"VIOLATION {failure}")
    print(f"check_log_append_only: {len(commits)} log commit(s), {len(failures)} violation(s)")
    return 2 if failures else 0


def _current_sprint_target(root: Path) -> tuple[str, str] | None:
    """Return (sprint dir, range) for the anchor's sprint, or None when out of scope."""
    target = current_sprint_dir(root)
    sprint_id = sprint_id_from_dir(target) if target else None
    if target is None or sprint_id is None or sprint_id < ENFORCED_FROM:
        return None
    state = json.loads((root / "docs" / "active_state.json").read_text(encoding="utf-8"))
    base = state["last_close_commit"]
    return target.resolve().relative_to(root.resolve()).as_posix(), f"{base}..HEAD"


def _dispatch(args: argparse.Namespace, parser: argparse.ArgumentParser) -> int:
    """Run the mode the arguments select."""
    if args.current_sprint:
        root = agents_root()
        found = _current_sprint_target(root)
        if found is None:
            print(f"[OK] check_log_append_only: no sprint >= {ENFORCED_FROM} (skip)")
            return 0
        return check(root, *found)
    if not args.sprint_dir or not args.rng or ".." not in args.rng or "..." in args.rng:
        parser.error("--current-sprint, or --sprint-dir with --range <base>..<end>")
    return check(Path.cwd(), args.sprint_dir.rstrip("/"), args.rng)


def main() -> int:
    """Parse arguments and run the check; git and anchor failures exit 2."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--sprint-dir", help="Sprint directory, relative to the working directory")
    parser.add_argument("--range", dest="rng", help="<base>..<end>")
    parser.add_argument("--current-sprint", action="store_true")
    args = parser.parse_args()
    try:
        return _dispatch(args, parser)
    except (subprocess.CalledProcessError, OSError, ValueError, KeyError) as exc:
        detail = getattr(exc, "stderr", "") or exc
        print(f"check_log_append_only: error: {detail}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
