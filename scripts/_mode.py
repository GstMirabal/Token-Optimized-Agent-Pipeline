"""Which repository is the work: the framework, or the host that installs it.

Two files already answered this independently — `session_probe.py` with
`is_nucleus()` and `install.py` with an inline `(AGENTS_DIR / ".git").is_dir()`
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

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root  # noqa: E402


def is_nucleus() -> bool:
    """True when this checkout is the framework repository itself.

    Returns:
        bool: True if `.git` is a real directory (the nucleus), False when it is
            a submodule pointer file (installed inside a host).
    """
    return (agents_root() / ".git").is_dir()
