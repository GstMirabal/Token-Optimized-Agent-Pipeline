"""Fail the build when the README's declared counts drift from the tree.

The README's "At a Glance" table states how many rule contexts, agents, skills,
workflows, slash commands, scripts, and config files the framework ships.
Nothing recalculated them, so they drifted silently and were corrected by hand —
three times in a single session, most recently when PR #29 updated a count in
prose two sections below the table and left the table itself saying
`10 protocols … 11 slash commands` while the tree held 12 and 13.

Only the seven counts derivable from the tree are checked. The table also says
"8 phases (Planning → Sprint Closeout)", which is prose about a workflow's
internal structure rather than a countable set of files; pretending to verify
it would be the PR #28 defect — a check that reports success on something it
never actually measured.

The `scripts/` and `config/` figures live inside a marked block
(`<!-- COUNTED_START -->` … `<!-- COUNTED_END -->`) that this script may
rewrite with `--write`. Verify mode never touches text outside that fence.

**Framework-scoped, and it was not.** `close_workflow.md` Phase 2 runs this from
the HOST root, where every path below resolved against the host: `README.md`
became the host's README, `rules/` and `agents/` globbed empty, and
`skills/`.iterdir() raised. Measured from a directory holding only a host
README — `FileNotFoundError: 'skills'`, **exit 1**, not the exit 2 this
docstring and that workflow both promise. A mandatory close step had therefore
never run to completion in any host (`F-093-N2`). Sprint 023 `C1` anchors it.

invoked_by: Makefile `verify` target, close_workflow.md#readme_counts.

Usage:
    python3 scripts/check_readme_counts.py
    python3 scripts/check_readme_counts.py --write

Exit codes:
    0 — every declared count matches the tree (and block, when present)
    2 — drift found (RA-11: 2 is what blocks)
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root

README = Path("README.md")
COUNTED_START = "<!-- COUNTED_START -->"
COUNTED_END = "<!-- COUNTED_END -->"


def count_scripts() -> int:
    """Count top-level ``scripts/*.py`` (excludes ``denylists/`` and shell shims)."""
    return len(list(Path("scripts").glob("*.py")))


def count_config() -> int:
    """Count ``config/*.json`` registry files."""
    return len(list(Path("config").glob("*.json")))


# Each entry: label -> (regex capturing the declared number, actual count).
CHECKS: dict[str, tuple[str, Callable[[], int]]] = {
    "rule contexts": (
        r"(\d+)\s+lazy-loaded domain rule contexts",
        lambda: len(list(Path("rules").glob("*.md"))),
    ),
    "agents": (
        r"(\d+)\s+role-segregated agents",
        lambda: len(list(Path("agents").glob("*.md"))),
    ),
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
    "scripts": (
        r"(\d+)\s+Python scripts in",
        count_scripts,
    ),
    "config": (
        r"(\d+)\s+JSON registries in",
        count_config,
    ),
}


def render_counted_line(scripts: int, config: int) -> str:
    """One At a Glance row for the generated infrastructure counts."""
    return (
        f"| **Infrastructure** | {scripts} Python scripts in [`scripts/`](scripts/) · "
        f"{config} JSON registries in [`config/`](config/) |"
    )


def extract_counted_block(text: str) -> str | None:
    """Return inner content between markers, or None when absent."""
    pattern = re.compile(
        re.escape(COUNTED_START) + r"(.*?)" + re.escape(COUNTED_END),
        re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        return None
    return match.group(1).strip()


def replace_counted_block(text: str, line: str) -> str:
    """Replace or insert the marked block without touching surrounding README."""
    inner = f"\n{line}\n"
    if COUNTED_START in text and COUNTED_END in text:
        pattern = re.compile(
            re.escape(COUNTED_START) + r".*?" + re.escape(COUNTED_END),
            re.DOTALL,
        )
        replacement = f"{COUNTED_START}{inner}{COUNTED_END}"
        return pattern.sub(replacement, text, count=1)

    marker = "### At a Glance\n\n"
    if marker not in text:
        raise ValueError("README missing '### At a Glance' heading for block insert.")
    insert_at = text.index(marker) + len(marker)
    block = f"{COUNTED_START}{inner}{COUNTED_END}\n\n"
    return text[:insert_at] + block + text[insert_at:]


def verify_counts(text: str) -> list[str]:
    """Compare declared README figures against the tree."""
    errors: list[str] = []
    for label, (pattern, counter) in CHECKS.items():
        match = re.search(pattern, text)
        actual = counter()
        if not match:
            errors.append(
                f"{label}: no declared count found (tree has {actual}) "
                f"— the check pattern no longer matches the README."
            )
            continue
        declared = int(match.group(1))
        if declared != actual:
            errors.append(f"{label}: README says {declared}, tree has {actual}.")
    return errors


def verify_counted_block(text: str) -> list[str]:
    """When markers exist, the fenced line must match live counts."""
    block = extract_counted_block(text)
    if block is None:
        return []
    expected = render_counted_line(count_scripts(), count_config())
    if block != expected:
        return [
            (
                "counted block: fenced At a Glance row drifted from the tree "
                f"(expected exactly:\n{expected})"
            )
        ]
    return []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="Rewrite only the <!-- COUNTED_START -->…<!-- COUNTED_END --> region.",
    )
    args = parser.parse_args([] if argv is None else argv)

    os.chdir(agents_root())

    if not README.exists():
        print(f"❌ {README} not found inside {agents_root()}.", file=sys.stderr)
        return 2

    text = README.read_text(encoding="utf-8")
    errors = verify_counts(text)
    errors.extend(verify_counted_block(text))

    if errors and not args.write:
        print("❌ README counts have drifted from the tree:", file=sys.stderr)
        for error in errors:
            print(f"  • {error}", file=sys.stderr)
        return 2

    if args.write:
        line = render_counted_line(count_scripts(), count_config())
        text = replace_counted_block(text, line)
        README.write_text(text, encoding="utf-8")
        errors = verify_counts(text)
        errors.extend(verify_counted_block(text))

    if errors:
        print("❌ README counts have drifted from the tree:", file=sys.stderr)
        for error in errors:
            print(f"  • {error}", file=sys.stderr)
        return 2

    summary = ", ".join(
        f"{label} {counter()}" for label, (_, counter) in CHECKS.items()
    )
    print(f"✅ README counts match the tree {summary}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
