"""Ping origin and checkout a newer published `.agents` tag when the host is behind.

Host `/start` used to report a newer tag and wait. O6 (human 2026-08-26): each
nucleus close publishes a tag so hosts can keep working; waiting left them on a
stale pin until someone noticed. Auto-update is **version tags only**
(``vX.Y.Z``, the deploy product), never ``main`` HEAD. Unreachable origin
degrades to the current pin (start continues). A dirty `.agents` tree while
behind exits ``2`` and does not overwrite (`submodule_purity`). Nucleus mode is
a no-op: this checkout *is* the framework.

invoked_by: workflows/start_workflow.md#lightweight_sync

Usage:
    python3 .agents/scripts/sync_agents_pin.py
    python3 scripts/sync_agents_pin.py   # nucleus (no-op)

Exit codes:
    0 — nucleus; already current; bumped; or ping failed (degraded)
    2 — dirty tree blocked a required bump (RA-11)
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _mode import is_nucleus
from _root import agents_root

FETCH_TIMEOUT_S = 20
GIT_TIMEOUT_S = 15


def git(
    args: list[str],
    cwd: Path | None,
    timeout: int | None = GIT_TIMEOUT_S,
) -> subprocess.CompletedProcess[str]:
    """Run git with prompts disabled. Does not raise on non-zero exit.

    Args:
        args: Arguments after ``git``.
        cwd: Working directory, or None for the process cwd.
        timeout: Seconds before ``TimeoutExpired``.

    Returns:
        subprocess.CompletedProcess[str]: stdout/stderr as text.
    """
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
        check=False,
    )


def parse_version(tag: str) -> tuple[int, ...]:
    """Numeric tuple from a ``vX.Y.Z`` tag. Non-digits inside a part stop it.

    Args:
        tag: Tag name, with or without a leading ``v``.

    Returns:
        tuple[int, ...]: Comparable version components.
    """
    body = tag.removeprefix("v")
    parts: list[int] = []
    for raw in body.split("."):
        digits = ""
        for char in raw:
            if char.isdigit():
                digits += char
            else:
                break
        parts.append(int(digits) if digits else 0)
    return tuple(parts)


def is_version_tag(tag: str) -> bool:
    """True when ``tag`` looks like a published framework version.

    Args:
        tag: A git tag name.

    Returns:
        bool: True for ``v`` + a digit, False otherwise.
    """
    return len(tag) >= 2 and tag[0] == "v" and tag[1].isdigit()


def remote_name(root: Path) -> str | None:
    """Prefer ``origin``, else the first remote, else None.

    Args:
        root: Framework checkout.

    Returns:
        str | None: Remote name to fetch.
    """
    result = git(["remote"], cwd=root)
    names = result.stdout.split()
    if "origin" in names:
        return "origin"
    return names[0] if names else None


def ping_fetch_tags(root: Path, remote: str) -> bool:
    """Fetch tags from ``remote``. False on timeout or non-zero git.

    Args:
        root: Framework checkout.
        remote: Remote name.

    Returns:
        bool: True when origin answered.
    """
    try:
        result = git(
            ["fetch", "--tags", remote],
            cwd=root,
            timeout=FETCH_TIMEOUT_S,
        )
    except subprocess.TimeoutExpired:
        print(
            f"[sync_agents_pin] ping timed out after {FETCH_TIMEOUT_S}s — "
            "keeping current pin"
        )
        return False
    if result.returncode != 0:
        err = (result.stderr or result.stdout).strip().replace("\n", " ")[:200]
        print(f"[sync_agents_pin] ping failed ({err}) — keeping current pin")
        return False
    return True


def porcelain(root: Path) -> list[str]:
    """Non-empty ``git status --porcelain -uall`` lines.

    Args:
        root: Framework checkout.

    Returns:
        list[str]: Dirty paths; empty when clean.
    """
    result = git(["status", "--porcelain", "-uall"], cwd=root)
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def current_tag(root: Path) -> str | None:
    """Nearest annotated/lightweight tag at HEAD, or None.

    Args:
        root: Framework checkout.

    Returns:
        str | None: ``vX.Y.Z`` or None when untagged.
    """
    result = git(["describe", "--tags", "--abbrev=0"], cwd=root)
    if result.returncode != 0:
        return None
    tag = result.stdout.strip()
    return tag or None


def version_tags(root: Path) -> list[str]:
    """Version tags newest-first (``--sort=-v:refname``).

    Args:
        root: Framework checkout.

    Returns:
        list[str]: Tags matching ``is_version_tag``.
    """
    result = git(["tag", "--sort=-v:refname"], cwd=root)
    return [line for line in result.stdout.split() if is_version_tag(line)]


def checkout_tag(root: Path, tag: str) -> bool:
    """Detach HEAD at ``tag``.

    Args:
        root: Framework checkout.
        tag: Version tag to check out.

    Returns:
        bool: True when git exited 0.
    """
    result = git(["checkout", "--detach", tag], cwd=root, timeout=30)
    if result.returncode != 0:
        err = (result.stderr or result.stdout).strip().replace("\n", " ")[:200]
        print(f"[sync_agents_pin] checkout {tag} failed ({err})")
        return False
    return True


def init_submodule(host: Path) -> bool:
    """``git submodule update --init -- .agents`` from the host root.

    Args:
        host: Superproject root (parent of `.agents`).

    Returns:
        bool: True when git exited 0.
    """
    result = git(
        ["submodule", "update", "--init", "--", ".agents"],
        cwd=host,
        timeout=60,
    )
    if result.returncode != 0:
        err = (result.stderr or result.stdout).strip().replace("\n", " ")[:200]
        print(f"[sync_agents_pin] submodule init failed ({err})")
        return False
    return True


def bump_if_behind(root: Path, current: str | None, latest: str) -> int:
    """Checkout ``latest`` when it is newer than ``current``.

    Args:
        root: Framework checkout.
        current: Tag at HEAD, or None if untagged.
        latest: Newest version tag after fetch.

    Returns:
        int: 0 bumped or already current; 2 dirty-while-behind.
    """
    if current is not None and parse_version(current) >= parse_version(latest):
        print(f"[sync_agents_pin] pin current ({current})")
        return 0
    dirty = porcelain(root)
    if dirty:
        print(
            "[sync_agents_pin] `.agents` is dirty and behind "
            f"{latest} — not overwriting. Stash or move host files, then "
            "re-run `/agents:start`.",
            file=sys.stderr,
        )
        return 2
    if not checkout_tag(root, latest):
        return 2
    was = current if current is not None else "untagged"
    print(
        f"[sync_agents_pin] bumped {was} -> {latest}. "
        "Host gitlink is dirty until committed. Read `.agents/CHANGELOG.md`. "
        "If `agents.md` §0 Rule Contexts gained a file, read it (advisory)."
    )
    return 0


def main() -> int:
    """Ping and bump the host pin, or no-op in nucleus mode.

    Returns:
        int: Process exit code (0 or 2).
    """
    if is_nucleus():
        print("[sync_agents_pin] nucleus: skip (this checkout is the framework)")
        return 0
    root = agents_root()
    if not (root / ".git").exists():
        host = root.parent
        print("[sync_agents_pin] submodule not initialized — running update --init")
        if not init_submodule(host):
            return 2
    remote = remote_name(root)
    if remote is None:
        print("[sync_agents_pin] no git remote — keeping current pin")
        return 0
    if not ping_fetch_tags(root, remote):
        return 0
    tags = version_tags(root)
    if not tags:
        print("[sync_agents_pin] no version tags after fetch — keeping current pin")
        return 0
    return bump_if_behind(root, current_tag(root), tags[0])


if __name__ == "__main__":
    sys.exit(main())
