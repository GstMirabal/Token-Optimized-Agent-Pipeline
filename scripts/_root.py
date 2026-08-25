"""Where the framework is, resolved once for every script that needs it.

Five framework-scoped scripts each spelled this differently and three of them
did not spell it at all: `check_readme_counts`, `check_manifest_parity`,
`map_workflows`, `scan_workflow_determinism` and `verify_references` addressed
`README.md`, `skills/`, `workflows/`, `rules/` and `config/` as **bare relative
paths**, so they read whichever directory the caller happened to be standing in.
Run from the repository root they were correct; run from anywhere else they
reported on a tree that was not the framework — silently, because a missing file
and an absent finding look identical from the outside.

**Two classes of script, with opposite requirements**, which is the distinction
that made "eleven scripts resolve the root wrongly" the wrong reading:

| Class | Root | Examples |
| :--- | :--- | :--- |
| Framework-scoped | This file's repository | `verify_references`, `map_workflows` |
| Host-scoped | The project being worked, i.e. the cwd | `docs_freshness_check`, `detect_drift` |
| Mixed | Both, deliberately | `branch_sovereignty` — audits the host's git, reads the framework's `config/` |

Host-scoped scripts MUST NOT adopt `agents_root()`. Anchoring them to the
framework would make them audit the framework instead of the host, which is a
larger defect than the one this module fixes. They declare their root in their
own docstring instead.

Sprint 025 wrote this same anchoring as `_mode.agents_dir()` on purpose, so that
this became a rename rather than a redesign. `_mode.py` now imports from here:
one function, one name, one definition.

## How a script adopts it, and why the two ways differ

**Framework-scoped scripts call `os.chdir(agents_root())` as the first statement
of their entry point.** Rewriting each `Path("workflows")` into
`agents_root() / "workflows"` was the obvious alternative and is worse in two
measurable ways: every message these scripts print would change from a relative
path to an absolute one — `C0.3`'s stated limit is that no observable behaviour
changes — and the next contributor to add a bare `Path("docs")` would silently
reintroduce the defect, because nothing in the file would tell them not to.
Setting the root once makes every relative path in the module correct by
construction, including the ones not written yet.

The cost is a process-global side effect, which is why it belongs in `main()`
and never at import: a test importing one of these modules must not have its
working directory moved underneath it. One consequence to know about — a module
constant that *evaluates* a glob at import time runs before `main()` and so
before the chdir. `verify_references.LOADABLE` was exactly that and is now a
function.

**Host-scoped and mixed scripts never chdir.** They anchor the specific
framework file they need — `agents_root() / "config" / "abandoned_branches.json"`
— and leave every other path resolving against the host, which is their subject.

invoked_by: scripts/_mode.py, scripts/branch_sovereignty.py,
scripts/check_manifest_parity.py, scripts/check_model_tiers.py,
scripts/check_readme_counts.py, scripts/detect_new_models.py,
scripts/docs_freshness_check.py, scripts/map_workflows.py,
scripts/scan_workflow_determinism.py, scripts/submodule_purity.py,
scripts/verify_references.py.

Usage:
    from _root import agents_root
"""

from pathlib import Path


def agents_root() -> Path:
    """The framework repository root, resolved from this file, never from the cwd.

    `.resolve()` is not decoration: without it a script invoked through a
    symlinked path — which is exactly how `install.sh` exposes commands
    and agents into a host's `.claude/` — resolves the root to the symlink's
    directory rather than to the real tree.

    Returns:
        Path: Absolute path to the directory holding `agents.md`, `workflows/`
            and `config/`. In nucleus mode this is the repository root; inside a
            host it is the `.agents/` submodule checkout.
    """
    return Path(__file__).resolve().parent.parent
