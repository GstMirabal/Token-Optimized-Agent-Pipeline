"""Every profile reference in a tracked file resolves, or is a reviewed placeholder.

Plan D24 (Sprint 059, unit A-31). A reference is the text `profiles` plus a
slash, followed by a token. The token is one of:

* a slug (`[A-Za-z0-9_-]+`): it MUST name a real directory directly under the
  repository's `profiles/` directory (exact-case match);
* a placeholder form from `PLACEHOLDER_FORMS`, or no token at all (the bare
  directory name), which `BARE_TERMINATORS` bounds;
* anything else: reported as unclassified. The test fails closed.

Every tracked file is scanned, documents of already-removed profiles
included: a stale reference there fails like any other. Tracked files come
from `git ls-files` at the repository root; git missing or erroring fails the
test, it never skips.

Limit: this test checks references that carry the directory prefix. It does
NOT detect a host's bare name written without that prefix; that stays with
the Sprint 060 scanner (KI-059-12).
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# The prefix is assembled so this file never contains a reference itself.
PREFIX = "profiles" + "/"

# Reviewed placeholder tokens (measured over the tree at Sprint 059).
PLACEHOLDER_FORMS: dict[str, str] = {
    "<name>": "angle-bracket template slot for a profile name",
    "[name]": "square-bracket template slot for a profile name",
    "<slug>": "angle-bracket template slot for a profile slug",
    "*": "glob over every installed profile, e.g. in a path pattern",
}

# A bare directory mention ends at one of these characters (or end of line).
BARE_TERMINATORS = frozenset(" \t`*).,;:\"'")

REFERENCE_RE = re.compile(
    r"(?<![A-Za-z0-9_-])" + re.escape(PREFIX)
    + r"(?P<slug>[A-Za-z0-9_-]+)?"
    + r"(?P<form><[^>\s]+>|\[[^\]\s]+\]|\*)?"
)


def git_tracked_files() -> list[str]:
    """List tracked file paths relative to the repository root.

    Returns:
        list[str]: paths reported by `git ls-files`.

    Raises:
        AssertionError: when git is missing or exits non-zero.
    """
    try:
        done = subprocess.run(
            ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=False
        )
    except OSError as exc:
        raise AssertionError(f"git could not be run: {exc}") from exc
    assert done.returncode == 0, f"git ls-files exited {done.returncode}"
    names = done.stdout.decode("utf-8").split("\0")
    return [name for name in names if name]


def real_profile_dirs() -> set[str]:
    """Return the names of the directories directly under `profiles/`.

    Returns:
        set[str]: exact directory names; empty when the directory is absent.
    """
    base = ROOT / PREFIX
    if not base.is_dir():
        return set()
    return {entry.name for entry in base.iterdir() if entry.is_dir()}


def classify(line: str, match: re.Match[str], real: set[str]) -> str | None:
    """Judge one reference match on a line.

    Args:
        line: the line holding the match.
        match: the `REFERENCE_RE` match.
        real: names of the real profile directories.

    Returns:
        str | None: the reason the reference is not allowed, or None.
    """
    slug, form = match.group("slug"), match.group("form")
    if slug and form:
        return f"unclassified token {match.group(0)!r}"
    if slug:
        return None if slug in real else f"no such profile directory {slug!r}"
    if form:
        return None if form in PLACEHOLDER_FORMS else f"unreviewed form {form!r}"
    after = line[match.end():match.end() + 1]
    if after == "" or after in BARE_TERMINATORS:
        return None
    return f"unclassified token {match.group(0) + after!r}"


def scan_text(text: str, real: set[str]) -> list[tuple[int, str]]:
    """Find disallowed references in a text.

    Args:
        text: file content.
        real: names of the real profile directories.

    Returns:
        list[tuple[int, str]]: (1-based line number, reason) pairs.
    """
    found: list[tuple[int, str]] = []
    for number, line in enumerate(text.splitlines(), 1):
        for match in REFERENCE_RE.finditer(line):
            reason = classify(line, match, real)
            if reason:
                found.append((number, reason))
    return found


def read_text_or_none(name: str) -> str | None:
    """Read a tracked file as UTF-8 text.

    Args:
        name: path relative to the repository root.

    Returns:
        str | None: the text, or None for a binary file or a tracked file
            deleted from the working tree.
    """
    try:
        data = (ROOT / name).read_bytes()
    except FileNotFoundError:
        return None
    if b"\0" in data:
        return None
    return data.decode("utf-8", errors="replace")


def test_every_profile_reference_resolves() -> None:
    """No tracked file references a profile directory that does not exist."""
    real = real_profile_dirs()
    failures: list[str] = []
    for name in git_tracked_files():
        text = read_text_or_none(name)
        if text is None:
            continue
        for number, reason in scan_text(text, real):
            failures.append(f"{name}:{number}: {reason}")
    assert not failures, (
        f"{len(failures)} unresolved profile reference(s):\n" + "\n".join(failures)
    )


def test_scan_text_judges_each_kind_of_reference() -> None:
    """The scanner accepts real slugs and placeholders and rejects the rest."""
    real = {"present"}
    ok = f"`{PREFIX}present/` `{PREFIX}<name>` {PREFIX}[name]/x {PREFIX}* and {PREFIX}"
    assert scan_text(ok, real) == []
    assert scan_text(f"see {PREFIX}absent/", real) == [
        (1, "no such profile directory 'absent'")
    ]
    assert scan_text(f"see {PREFIX}Present", real)[0][0] == 1
    assert scan_text(f"see {PREFIX}{{x}}", real)[0][0] == 1
    assert scan_text(f"see {PREFIX}<other>", real)[0][0] == 1


def test_placeholder_forms_each_carry_a_reason() -> None:
    """Every reviewed placeholder states why it is allowed."""
    assert PLACEHOLDER_FORMS
    assert all(reason.strip() for reason in PLACEHOLDER_FORMS.values())
