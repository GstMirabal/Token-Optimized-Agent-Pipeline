"""Static scanner for `token_economy_agent`'s Filter 5 (skills/token-saver-
auditor/SKILL.md): finds workflow steps that look like they run every
sprint-close/commit and rely on agent judgment where a deterministic
script/make-target would do.

Deliberately structural, not phrase-matching. An earlier design searched
for literal strings like "requires agent judgment" -- tested against the
real workflows/, it matched nothing, including close_workflow.md's own
`history_sync` step (the founding example this whole feature exists to
catch). Structural signal instead: a table row inside a per-close/
per-commit phase whose action starts with Update/Refresh/Review and
never names a script or `make` target.

Runs at definition time (when a workflow is edited, via `make verify`),
never at execution time -- the same discipline the rest of the framework
holds itself to (rules/token_economy.md).
"""
import re
from pathlib import Path

WORKFLOWS_DIR = Path("workflows")
TABLE_ROW_RE = re.compile(r"^\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$", re.MULTILINE)
UPDATE_VERB_RE = re.compile(r"\b(Update|Refresh|Review)\b", re.IGNORECASE)
SCRIPT_OR_MAKE_RE = re.compile(r"`make[^`]*`|\.py`|\.sh`|script")
PER_CLOSE_PHASE_RE = re.compile(r"close|commit", re.IGNORECASE)


def is_per_close_or_commit(phase_cell: str, source_file: Path) -> bool:
    """True if this row's phase, or the workflow file itself, is a
    per-sprint-close or per-commit cadence."""
    if "close" in source_file.stem.lower():
        return True
    return bool(PER_CLOSE_PHASE_RE.search(phase_cell))


def find_determinism_candidates(text: str, source_file: Path) -> list[str]:
    """Return human-readable descriptions of candidate rows in one workflow file."""
    candidates: list[str] = []
    for phase, step, action in TABLE_ROW_RE.findall(text):
        if phase.startswith(":---") or phase.lower() == "phase":
            continue
        if not is_per_close_or_commit(phase, source_file):
            continue
        if not UPDATE_VERB_RE.search(action):
            continue
        if SCRIPT_OR_MAKE_RE.search(action):
            continue
        candidates.append(f"{source_file}: [{phase} / {step}] {action[:100]}")
    return candidates


def scan(repo_root: Path) -> list[str]:
    """Scan every workflows/*.md for determinism-bypass candidates."""
    findings: list[str] = []
    workflows_dir = repo_root / WORKFLOWS_DIR
    if not workflows_dir.is_dir():
        return findings
    for path in sorted(workflows_dir.glob("*.md")):
        findings.extend(find_determinism_candidates(path.read_text(encoding="utf-8"), path))
    return findings


if __name__ == "__main__":
    import sys

    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    results = scan(root)
    if not results:
        print("[OK] scan_workflow_determinism: no candidates found")
    for line in results:
        print(f"[WARN] {line}")
