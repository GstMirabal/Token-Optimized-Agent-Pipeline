"""Create a GitHub Release whose notes are the sealed CHANGELOG section.

`deployment_workflow.md` Phase 4 `release_tagging` pushes the git tag.
This script is the next step: the GitHub Release the README promises.
Through `v4.9.1` the workflow named only `git tag -a`, so Latest on
GitHub stayed at `v4.3.0` (the one-shot backfill) while seven later
tags had no landing page.

Notes come from `## [X.Y.Z]` in CHANGELOG.md. A tag with no matching
section is not a release — the same rule `detect_drift.py` uses for
sealing tags. `--notes-from-tag` is how a landing page diverges from
the ledger and is never used. `--verify-tag` is required so `gh`
cannot mint a tag from `main` as a side effect of creating a Release.

Host-scoped: CHANGELOG.md and `origin` belong to the repository being
deployed (the host, or the nucleus when this repository deploys itself).
Do not resolve them through `scripts/_root.py`.

invoked_by: deployment_workflow.md#github_release

Usage:
    python3 scripts/publish_github_release.py vX.Y.Z
    python3 scripts/publish_github_release.py --missing

Exit codes:
    0 — release created, already existed, or --notes-only printed
    2 — no matching CHANGELOG section, tag missing, or gh failed
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

CHANGELOG = Path("CHANGELOG.md")
SECTION = re.compile(r"^## \[(\d[^\]]*)\]", re.MULTILINE)


def normalize(raw: str) -> str:
    """Strip a leading ``v`` from a tag-shaped version string.

    Args:
        raw: Tag or section id (``v4.9.1`` or ``4.9.1``).

    Returns:
        str: Bare ``X.Y.Z`` used as the CHANGELOG heading.
    """
    text = raw.strip()
    if text.startswith("v") and len(text) > 1 and text[1].isdigit():
        return text[1:]
    return text


def tag_name(version: str) -> str:
    """Return the git tag name for a bare version.

    Args:
        version: Bare ``X.Y.Z``.

    Returns:
        str: ``vX.Y.Z``.
    """
    return version if version.startswith("v") else f"v{version}"


def sealed_versions(text: str) -> list[str]:
    """Released section ids in ledger order (newest first).

    Args:
        text: Full CHANGELOG.md contents.

    Returns:
        list[str]: Bare versions; ``[Unreleased]`` is excluded by the regex.
    """
    return SECTION.findall(text)


def extract_notes(text: str, version: str) -> str | None:
    """Body of ``## [version]``, excluding the heading and the next section.

    Args:
        text: Full CHANGELOG.md contents.
        version: Bare ``X.Y.Z``.

    Returns:
        str | None: Stripped body, or None when the section is missing or empty.
    """
    heading = re.search(
        rf"^## \[{re.escape(version)}\][^\n]*\n", text, re.MULTILINE
    )
    if heading is None:
        return None
    rest = text[heading.end():]
    nxt = re.search(r"^## \[", rest, re.MULTILINE)
    body = rest[: nxt.start()] if nxt else rest
    stripped = body.strip()
    return stripped or None


def origin_slug(url: str) -> str | None:
    """Parse ``owner/name`` from a GitHub remote URL.

    Args:
        url: ``git remote get-url origin`` output.

    Returns:
        str | None: Slug, or None when the remote is not GitHub.
    """
    cleaned = url.strip().rstrip("/").removesuffix(".git")
    marker = "github.com"
    if marker not in cleaned:
        return None
    tail = cleaned.split(marker, 1)[1].lstrip("/:")
    parts = [p for p in tail.split("/") if p]
    if len(parts) < 2:
        return None
    return f"{parts[0]}/{parts[1]}"


def release_body(notes: str, slug: str | None) -> str:
    """Append the ledger footer used since the ``v4.3.0`` backfill.

    Args:
        notes: Section body from CHANGELOG.md.
        slug: GitHub ``owner/name``, or None when origin is not GitHub.

    Returns:
        str: Notes plus a CHANGELOG link (not duplicated if already present).
    """
    if "Full history:" in notes:
        return notes if notes.endswith("\n") else f"{notes}\n"
    if slug is None:
        footer = "---\nFull history: CHANGELOG.md"
    else:
        footer = (
            "---\n"
            f"Full history: [CHANGELOG.md](https://github.com/{slug}/blob/main/CHANGELOG.md)"
        )
    return f"{notes.rstrip()}\n\n{footer}\n"


def is_newest(version: str, sealed: list[str]) -> bool:
    """True when ``version`` is the first sealed section (newest in the ledger).

    Args:
        version: Bare ``X.Y.Z``.
        sealed: ``sealed_versions`` result.

    Returns:
        bool: Whether this release should be marked Latest.
    """
    return bool(sealed) and sealed[0] == version


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    """Run a command, capturing text output.

    Args:
        cmd: Argument vector.

    Returns:
        subprocess.CompletedProcess[str]: Completed process.
    """
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def git_remote_url() -> str:
    """Return ``origin`` URL, or empty string when git fails."""
    result = run(["git", "remote", "get-url", "origin"])
    return result.stdout.strip() if result.returncode == 0 else ""


def git_tags() -> set[str]:
    """Bare versions that exist as local git tags."""
    result = run(["git", "tag"])
    if result.returncode != 0:
        return set()
    return {normalize(t) for t in result.stdout.split() if t.strip()}


def release_exists(tag: str) -> bool:
    """True when GitHub already has a Release for ``tag``."""
    return run(["gh", "release", "view", tag]).returncode == 0


def create_release(
    tag: str, body: str, latest: bool
) -> subprocess.CompletedProcess[str]:
    """Create the Release. Never ``--notes-from-tag``; always ``--verify-tag``.

    Args:
        tag: ``vX.Y.Z``.
        body: Release notes.
        latest: Whether to mark this Release as Latest.

    Returns:
        subprocess.CompletedProcess[str]: ``gh release create`` result.
    """
    latest_flag = "--latest" if latest else "--latest=false"
    return run([
        "gh", "release", "create", tag,
        "--title", tag,
        "--notes", body,
        "--verify-tag",
        latest_flag,
    ])


def publish_one(
    version: str, text: str, slug: str | None, notes_only: bool
) -> int:
    """Publish one version, or print its notes.

    Args:
        version: Bare ``X.Y.Z``.
        text: Full CHANGELOG.md contents.
        slug: GitHub slug for the footer, or None.
        notes_only: Print notes and skip ``gh``.

    Returns:
        int: 0 on success or already-exists; 2 on missing section or gh failure.
    """
    notes = extract_notes(text, version)
    if notes is None:
        print(
            f"No CHANGELOG.md section ## [{version}]. A tag without a ledger "
            "section is not a release.",
            file=sys.stderr,
        )
        return 2
    tag = tag_name(version)
    body = release_body(notes, slug)
    latest = is_newest(version, sealed_versions(text))
    if notes_only:
        sys.stdout.write(body if body.endswith("\n") else f"{body}\n")
        print(f"# tag={tag} latest={latest}", file=sys.stderr)
        return 0
    if release_exists(tag):
        print(f"GitHub Release {tag} already exists.")
        return 0
    result = create_release(tag, body, latest)
    if result.returncode != 0:
        err = (result.stderr or result.stdout).strip()
        print(f"gh release create {tag} failed: {err}", file=sys.stderr)
        return 2
    print(f"Created GitHub Release {tag} (latest={latest}).")
    return 0


def load_changelog() -> str | None:
    """Read CHANGELOG.md from the current working directory."""
    if not CHANGELOG.exists():
        print("CHANGELOG.md is missing.", file=sys.stderr)
        return None
    return CHANGELOG.read_text(encoding="utf-8")


def missing_versions(text: str, tagged: set[str]) -> list[str]:
    """Tagged sealed versions, oldest first, so Latest is applied last.

    Args:
        text: Full CHANGELOG.md contents.
        tagged: Bare versions that exist as git tags.

    Returns:
        list[str]: Versions to publish.
    """
    return [v for v in reversed(sealed_versions(text)) if v in tagged]


def main() -> int:
    """CLI entry: one version, or every tagged section still unpublished."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("version", nargs="?", help="vX.Y.Z or X.Y.Z")
    parser.add_argument(
        "--missing",
        action="store_true",
        help="create a Release for every tagged CHANGELOG section that has none",
    )
    parser.add_argument(
        "--notes-only",
        action="store_true",
        help="print notes; do not call gh",
    )
    args = parser.parse_args()
    if bool(args.version) == args.missing:
        print("Pass exactly one of VERSION or --missing.", file=sys.stderr)
        return 2
    text = load_changelog()
    if text is None:
        return 2
    slug = origin_slug(git_remote_url())
    if args.version:
        return publish_one(normalize(args.version), text, slug, args.notes_only)
    versions = missing_versions(text, git_tags())
    if not versions:
        print("No tagged CHANGELOG sections to publish.")
        return 0
    for version in versions:
        step = publish_one(version, text, slug, args.notes_only)
        if step != 0:
            return step
    return 0


if __name__ == "__main__":
    sys.exit(main())
