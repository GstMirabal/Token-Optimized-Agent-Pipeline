"""Which repository is the work: the framework, or the host that installs it.

Two files already answered this independently — `session_probe.py` with
`is_nucleus()` and `install_claude.py` with an inline `(AGENTS_DIR / ".git").is_dir()`
— and a third was about to. `rules/code_craft.md §1` puts the extraction
threshold at two call sites, so this is one site late rather than speculative.

The test is git's own: a real repository keeps `.git` as a **directory**, while a
submodule checkout keeps it as a **file** holding a `gitdir:` pointer into the
superproject. Nothing else distinguishes them from inside the tree, and no
configuration has to be maintained for it to stay true.

Jurisdiction follows from it. In nucleus mode the framework *is* the work and its
own records belong here. In submodule mode the host is the work, and
`agents.md §3 strict_rule` forbids the host from altering the framework in place
— framework improvements go through `§4 feedback_upstream`, a branch and pull
request against the nucleus repository, worked in a separate clone.

invoked_by: scripts/submodule_purity.py, scripts/session_probe.py,
scripts/install_claude.py.

Usage:
    from _mode import is_nucleus, agents_dir
"""

from pathlib import Path


def agents_dir() -> Path:
    """The framework root, resolved from this file rather than from the cwd.

    Sprint 023 `C0.3` unifies root resolution across the five framework-scoped
    scripts that each spell it differently. This is deliberately the same
    anchoring those will adopt, so that change is a rename and not a redesign.
    """
    return Path(__file__).resolve().parent.parent


def is_nucleus() -> bool:
    """True when this checkout is the framework repository itself.

    Returns:
        bool: True if `.git` is a real directory (the nucleus), False when it is
            a submodule pointer file (installed inside a host).
    """
    return (agents_dir() / ".git").is_dir()
