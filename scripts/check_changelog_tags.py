"""Fail the build when the framework CHANGELOG.md disagrees with its git tags.

Checks exactly these two properties and nothing else (no coverage claim,
`agents.md` §1 `fail_closed_claims`):

1. Presence: every git tag matching `^v(\\d+)\\.(\\d+)\\.(\\d+)$` has a header line
   `## [X.Y.Z]` in `CHANGELOG.md`.
2. Order: the `## [X.Y.Z]` version headers (`## [Unreleased]` ignored) appear in
   strictly descending semantic-version order, compared numerically.

It does not check header dates, section bodies, tag-to-commit mapping, or that
a header has a tag. "Fail-closed" here means only fail-closed on error: a
missing CHANGELOG or a failing `git` exits 2.

Stated limit: a checkout where `git tag` shows zero semver tags (a shallow clone
without tags, e.g. `actions/checkout` at default depth) gets the order check
only. Check 1 and the stale-gap check are skipped, one notice goes to stderr,
and the exit code follows check 2. With at least one semver tag visible, both
checks run.

Why (`KI-056-8`): the Sprint 056 `[Unreleased]` insertion overwrote the
`## [4.38.0] - 2026-10-11` header. `make verify`, drift detection, both gates
and CI passed, and `session_state.py set-topology` silently derived `4.37.0`.

`HISTORICAL_GAPS` lists tags that predate a ledger section. Closed history is
not rewritten (`workflows/standardization_workflow.md`), so those tags are
skipped for check 1 only. A listed tag that now has a header, or is no longer a
tag, is a stale entry and exits 2.

Framework-scoped: reads the framework's own `CHANGELOG.md` and `git tag`,
anchored with `os.chdir(agents_root())` in `main()` (`scripts/_root.py`).

invoked_by: Makefile `verify` target.

Usage:
    python3 scripts/check_changelog_tags.py
    python3 scripts/check_changelog_tags.py --changelog <path>

Exit codes:
    0 - both checks pass
    2 - violation or error (RA-11: 2 is what blocks)
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from itertools import pairwise
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root

TAG_RE = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")
HEADER_RE = re.compile(r"^## \[(\d+)\.(\d+)\.(\d+)\]", re.MULTILINE)

# Tags released without a CHANGELOG section. Closed history is not rewritten.
HISTORICAL_GAPS: frozenset[str] = frozenset(
    {
        # Annotated "v3.4.0 - documentation_standard" (2026-07-24); the ledger
        # jumps from 3.5.0 to 3.3.2 with no 3.4.0 section.
        "v3.4.0",
        # Patch tag on fix(hooks) telemetry bugs (2026-07-26, #17); the ledger
        # tops out at 3.5.1 for that day with no 3.5.2 section.
        "v3.5.2",
    }
)

Version = tuple[int, int, int]

NO_TAGS_NOTICE = "no semver tags visible (shallow clone without tags); presence check skipped"


def parse_tags(tags: list[str]) -> dict[str, Version]:
    """Map each semver tag name to its numeric version; other tags are ignored.

    Args:
        tags: Raw tag names.

    Returns:
        dict[str, Version]: Tag name to (major, minor, patch).
    """
    found: dict[str, Version] = {}
    for tag in tags:
        match = TAG_RE.match(tag.strip())
        if match:
            found[tag.strip()] = (
                int(match.group(1)),
                int(match.group(2)),
                int(match.group(3)),
            )
    return found


def parse_headers(changelog_text: str) -> list[Version]:
    """Return the `## [X.Y.Z]` header versions in file order.

    Args:
        changelog_text: Full CHANGELOG.md text.

    Returns:
        list[Version]: Versions as numeric tuples, in appearance order.
    """
    return [
        (int(m.group(1)), int(m.group(2)), int(m.group(3)))
        for m in HEADER_RE.finditer(changelog_text)
    ]


def fmt(version: Version) -> str:
    """Render a version tuple as `X.Y.Z`.

    Args:
        version: A `(major, minor, patch)` tuple.

    Returns:
        str: The dotted version string.
    """
    return ".".join(str(part) for part in version)


def check_stale_gaps(tags: dict[str, Version], headers: set[Version]) -> list[str]:
    """Report HISTORICAL_GAPS entries that are no longer true.

    Args:
        tags: Semver tags from `parse_tags`.
        headers: Set of header versions present.

    Returns:
        list[str]: One message per stale entry.
    """
    errors = [
        f"stale HISTORICAL_GAPS entry {gap}: no longer a tag"
        for gap in sorted(HISTORICAL_GAPS)
        if gap not in tags
    ]
    errors.extend(
        f"stale HISTORICAL_GAPS entry {gap}: CHANGELOG.md now has its header"
        for gap in sorted(HISTORICAL_GAPS)
        if gap in tags and tags[gap] in headers
    )
    return errors


def check_presence(tags: dict[str, Version], headers: set[Version]) -> list[str]:
    """Check 1 plus stale-gap detection.

    Args:
        tags: Semver tags from `parse_tags`.
        headers: Set of header versions present.

    Returns:
        list[str]: One violation message per problem.
    """
    errors: list[str] = []
    for name, version in sorted(tags.items(), key=lambda item: item[1]):
        if name not in HISTORICAL_GAPS and version not in headers:
            errors.append(f"tag {name} has no '## [{fmt(version)}]' header in CHANGELOG.md")
    errors.extend(check_stale_gaps(tags, headers))
    return errors


def check_order(headers: list[Version]) -> list[str]:
    """Check 2: headers strictly descending by numeric version.

    Args:
        headers: Header versions in file order.

    Returns:
        list[str]: One violation per adjacent pair that is not descending.
    """
    errors: list[str] = []
    for previous, current in pairwise(headers):
        if current >= previous:
            errors.append(
                f"header order: [{fmt(current)}] follows [{fmt(previous)}] "
                "but must be strictly lower"
            )
    return errors


def check(tags: list[str], changelog_text: str) -> list[str]:
    """Run both checks on injected inputs.

    Args:
        tags: Raw git tag names.
        changelog_text: Full CHANGELOG.md text.

    Returns:
        list[str]: All violations; empty when clean.
    """
    headers = parse_headers(changelog_text)
    semver = parse_tags(tags)
    errors = check_presence(semver, set(headers)) if semver else []
    errors.extend(check_order(headers))
    return errors


def read_git_tags() -> list[str]:
    """List git tags of the current directory.

    Returns:
        list[str]: Tag names.

    Raises:
        RuntimeError: When `git tag` cannot run or exits non-zero.
    """
    try:
        result = subprocess.run(
            ["git", "tag", "--list"], capture_output=True, text=True, check=False
        )
    except OSError as exc:
        raise RuntimeError(f"cannot run git: {exc}") from exc
    if result.returncode != 0:
        raise RuntimeError(f"git tag failed: {result.stderr.strip()}")
    return result.stdout.split()


def main(argv: list[str] | None = None) -> int:
    """Entry point.

    Args:
        argv: Arguments without the program name.

    Returns:
        int: 0 clean, 2 on violation or error.
    """
    parser = argparse.ArgumentParser(description="Check CHANGELOG.md against git tags.")
    parser.add_argument(
        "--changelog",
        help="CHANGELOG path, relative to the current directory (default: framework CHANGELOG.md).",
    )
    args = parser.parse_args([] if argv is None else argv)

    given = Path(args.changelog).resolve() if args.changelog else None
    os.chdir(agents_root())
    path = given or Path("CHANGELOG.md")
    try:
        text = path.read_text(encoding="utf-8")
        tags = read_git_tags()
    except (OSError, RuntimeError) as exc:
        print(f"check_changelog_tags: error: {exc}", file=sys.stderr)
        return 2

    if not parse_tags(tags):
        print(NO_TAGS_NOTICE, file=sys.stderr)
    errors = check(tags, text)
    if errors:
        print("CHANGELOG.md disagrees with git tags:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 2
    print(
        f"OK: {len(parse_tags(tags))} semver tags, "
        f"{len(parse_headers(text))} version headers, "
        f"{len(HISTORICAL_GAPS)} historical gaps."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
