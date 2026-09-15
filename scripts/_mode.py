"""Which repository is the work: the framework, or the host that installs it.

Two files already answered this independently — `session_probe.py` with
`is_nucleus()` and `install.py` with an inline `(AGENTS_DIR / ".git").is_dir()`
— and a third was about to. `rules/code_craft.md §1` puts the extraction
threshold at two call sites, so this is one site late rather than speculative.

The test is git's own: a real repository keeps `.git` as a **directory**, while a
submodule checkout keeps it as a **file** holding a `gitdir:` pointer into the
superproject (`.git/modules/...`). Nothing else distinguishes those two from
inside the tree, and no configuration has to be maintained for it to stay true.

**Linked git worktrees are the exception the directory test gets wrong.** A
worktree of the nucleus repository also keeps `.git` as a *file*, so a framework
developer working in `git worktree add`-created checkout was misclassified as a
host. A worktree pointer and a submodule pointer are told apart by where their
`gitdir:` leads: a worktree's leads into the nucleus's own
`<root>/.git/worktrees/<name>/`, whose `commondir` resolves back to a real `.git`
directory whose parent carries the framework markers (`agents.md`, `workflows/`,
`scripts/_mode.py`); a submodule's leads into a superproject's `.git/modules/`.
The distinction is pure filesystem parsing — the `.git` file plus `commondir` —
with no `git` subprocess, so it stays correct under a restricted sandbox.

Jurisdiction follows from it. In nucleus mode the framework *is* the work and its
own records belong here. In submodule mode the host is the work, and
`agents.md §3 strict_rule` forbids the host from altering the framework in place
— framework improvements go through `§4 feedback_upstream`, a branch and pull
request against the nucleus repository, worked in a separate clone.

Root resolution used to live here as `agents_dir()`. Sprint 023 `C0.3` moved it
to `scripts/_root.py` as `agents_root()` — the rename that module was written in
anticipation of — because eleven scripts needed the root and only three needed
the mode, and a module named for one question is the wrong place to answer the
other.

invoked_by: scripts/submodule_purity.py, scripts/session_probe.py,
scripts/install.py, scripts/sync_agents_pin.py.

Usage:
    from _mode import is_nucleus
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root  # noqa: E402


def is_nucleus() -> bool:
    """True when this checkout is the framework repository itself.

    Three checkout shapes resolve to the nucleus:

    - `.git` is a real directory: a plain clone of the framework.
    - `.git` is a file whose `gitdir:` points into `<root>/.git/worktrees/<name>`
      and whose common `.git` directory has the framework at its parent: a
      linked git worktree of the nucleus repository.

    A submodule checkout also keeps `.git` as a file, but its `gitdir:` points
    into a superproject's `.git/modules/...`; that case resolves to a host, as
    does any unreadable or malformed `.git` pointer file.

    Returns:
        bool: True for a framework clone or a nucleus worktree, False for a
            submodule pointer or any unrecognised `.git` shape.
    """
    git_path = agents_root() / ".git"
    if git_path.is_dir():
        return True
    if not git_path.is_file():
        return False
    common = _nucleus_worktree_common_dir(git_path)
    return common is not None and _is_framework_dir(common.parent)


def _nucleus_worktree_common_dir(git_file: Path) -> Path | None:
    """Resolve the shared `.git` directory a worktree `.git` file points at.

    Args:
        git_file: The `.git` pointer file found inside a linked worktree.

    Returns:
        Path | None: The resolved common `.git` directory when `git_file` is a
            worktree pointer (`gitdir:` target sits under `.git/worktrees/` and
            is a real directory whose `commondir` is a real `.git` directory);
            None for a submodule pointer, a non-worktree target, or a
            malformed/unreadable file.
    """
    pointer = _read_gitdir_pointer(git_file)
    if pointer is None:
        return None
    gitdir = pointer if pointer.is_absolute() else agents_root() / pointer
    gitdir = gitdir.resolve()
    if not _has_git_child(gitdir.parts, "worktrees") or not gitdir.is_dir():
        return None
    common = _read_commondir(gitdir)
    if common.is_dir() and common.name == ".git":
        return common
    return None


def _read_gitdir_pointer(git_file: Path) -> Path | None:
    """Extract the `gitdir:` target from a `.git` pointer file.

    Args:
        git_file: Path to a `.git` file (worktree or submodule pointer).

    Returns:
        Path | None: The raw target as a Path, which may be relative, or None
            when the file cannot be read or carries no non-empty `gitdir:` line.
    """
    try:
        text = git_file.read_text(encoding="utf-8")
    except OSError:
        return None
    for line in text.splitlines():
        if line.startswith("gitdir:"):
            target = line.split(":", 1)[1].strip()
            return Path(target) if target else None
    return None


def _read_commondir(gitdir: Path) -> Path:
    """Resolve the common `.git` directory for a worktree's private git dir.

    Reads `<gitdir>/commondir` — a path relative to `gitdir`, or absolute — and
    falls back to the parent of the `worktrees/` directory when it is absent or
    unreadable.

    Args:
        gitdir: The resolved `<root>/.git/worktrees/<name>` directory.

    Returns:
        Path: The resolved candidate common `.git` directory.
    """
    try:
        target = (gitdir / "commondir").read_text(encoding="utf-8").strip()
    except OSError:
        target = ""
    if not target:
        return gitdir.parent.parent
    common = Path(target)
    if not common.is_absolute():
        common = gitdir / common
    return common.resolve()


def _has_git_child(parts: tuple[str, ...], name: str) -> bool:
    """True when `parts` contains the adjacent sequence `.git`, `name`.

    Args:
        parts: The path components to scan, as returned by `Path.parts`.
        name: The component that must immediately follow a `.git` component.

    Returns:
        bool: True when `<something>/.git/<name>/` appears in the path.
    """
    return any(
        parts[i - 1] == ".git" and parts[i] == name
        for i in range(1, len(parts))
    )


def _is_framework_dir(path: Path) -> bool:
    """True when `path` holds the framework's identifying files.

    Args:
        path: A directory that may be the framework root.

    Returns:
        bool: True when `agents.md`, `workflows/` and `scripts/_mode.py` all
            exist under `path`.
    """
    return (
        (path / "agents.md").is_file()
        and (path / "workflows").is_dir()
        and (path / "scripts" / "_mode.py").is_file()
    )
