"""Replay every ``fix(`` commit of a range: its tests must fail on the parent, pass at the commit.

The ``Repro:`` trailer on a ``fix(`` commit is only a claim (``hooks/on_commit.py``).
This script observes it: for each ``fix(`` commit that touches a source file it
creates a temporary worktree at the parent and at the commit, copies the
commit's version of the named test files into each, runs pytest, and requires
exit code EXACTLY 1 on the parent and 0 at the commit. A collection or usage
error on the parent (pytest exit 2/3/4/5) is not a reproduction.

Verdicts: OK, MANUAL, MISSING_TRAILER, UNREPLAYED, PASSES_ON_PARENT,
WRONG_FAILURE, FAILS_AT_COMMIT. Everything except OK and MANUAL is a violation.
RUNNER_UNAVAILABLE is not a per-commit verdict: the runner interpreter cannot
run pytest (checked with ``<python> -m pytest --version`` before any replay), so
nothing is replayed and the script exits 2.

Runner interpreter: ``--python <path>``, else ``<repo>/venv_skillopt/bin/python``
when it exists, else the interpreter running this script.

invoked_by: agents/qa_agent.md (QA Gate 1, first check),
workflows/pipeline_workflow.md Phase 7.

Usage:
    python3 scripts/check_fix_reproduces.py --range <base>..<head>
    python3 scripts/check_fix_reproduces.py --range <base> --repo <path>
    python3 scripts/check_fix_reproduces.py --range <base>..<head> --python <venv python>

Exit codes:
    0 - no violation (including a range with zero ``fix(`` commits)
    2 - at least one violation, a bad range, no git repository, or
        RUNNER_UNAVAILABLE (RA-11)
"""

from __future__ import annotations

import argparse
import contextlib
import logging
import os
import re
import subprocess
import sys
import tempfile
from collections.abc import Iterator
from pathlib import Path

LOG = logging.getLogger(__name__)
RUNNER_PYTHON: str = sys.executable
STRIPPED_ENV = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "DJANGO_SETTINGS_MODULE")
NON_SOURCE_SUFFIXES = frozenset({".md", ".rst", ".txt", ".json", ".yml", ".yaml", ".toml"})
_REPRO = re.compile(r"^Repro:\s*(.+?)\s+(?:—|--)\s+(.*?)\s*$", re.MULTILINE)
_FIX_SUBJECT = re.compile(r"^fix(\([^)]*\))?!?:|^fix\(")
HINT = (
    "make the test fail by assertion on the parent (for example import the new "
    "name inside the test function), not by a collection error"
)


def _env() -> dict[str, str]:
    """Return the child-process environment with replay hygiene applied.

    Returns:
        A copy of ``os.environ`` without git and framework-settings variables
        and with bytecode writing disabled.
    """
    env = {k: v for k, v in os.environ.items() if k not in STRIPPED_ENV}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Run git in ``repo`` and capture text output.

    Args:
        repo: Repository (or worktree) directory used as cwd.
        *args: Arguments after ``git``.

    Returns:
        The completed process; the caller inspects ``returncode``.
    """
    return subprocess.run(
        ["git", *args], cwd=repo, env=_env(), capture_output=True, text=True, check=False
    )


def normalize_range(spec: str) -> str:
    """Complete a range so its head defaults to HEAD.

    Args:
        spec: ``base..head``, ``base..`` or a bare ``base``.

    Returns:
        A ``base..head`` string.
    """
    base, sep, head = spec.partition("..")
    return f"{base}..{head or 'HEAD'}" if sep or base else spec


def list_commits(repo: Path, spec: str) -> list[str]:
    """List the commits of a range, oldest first.

    Args:
        repo: Repository directory.
        spec: A normalized ``base..head`` range.

    Returns:
        Full SHAs in ``git rev-list --reverse`` order.

    Raises:
        ValueError: If git rejects the range or ``repo`` is not a repository.
    """
    result = _git(repo, "rev-list", "--reverse", spec)
    if result.returncode != 0:
        raise ValueError(f"cannot list range {spec!r} in {repo}: {result.stderr.strip()}")
    return result.stdout.split()


def is_test_path(path: str) -> bool:
    """Tell whether a repository path is a test file.

    Args:
        path: Repository-relative path.

    Returns:
        True for files under a ``tests``/``test`` directory or named like a test.
    """
    p = Path(path)
    name = p.name
    return (
        bool({"tests", "test", "__tests__"} & set(p.parts[:-1]))
        or name.startswith("test_")
        or p.stem.endswith(("_test", ".test", ".spec"))
    )


def touches_source(repo: Path, sha: str) -> bool:
    """Tell whether a commit changes at least one source file.

    Args:
        repo: Repository directory.
        sha: Commit to inspect.

    Returns:
        True when a changed path is neither a test nor a documentation/config file.
    """
    out = _git(repo, "diff-tree", "--no-commit-id", "--name-only", "-r", "--root", sha).stdout
    return any(
        not is_test_path(f) and Path(f).suffix not in NON_SOURCE_SUFFIXES
        for f in out.splitlines()
        if f
    )


def parse_trailers(message: str) -> list[str]:
    """Extract the claim of every ``Repro:`` trailer.

    Args:
        message: Full commit message.

    Returns:
        The left-hand side of each trailer (a test id, or ``manual``).
    """
    return [m.group(1) for m in _REPRO.finditer(message)]


@contextlib.contextmanager
def worktree(repo: Path, rev: str) -> Iterator[Path]:
    """Provide a detached temporary worktree, always removed afterwards.

    Args:
        repo: Repository directory.
        rev: Revision to check out detached.

    Yields:
        The worktree directory.

    Raises:
        RuntimeError: If the worktree cannot be created.
    """
    base = Path(tempfile.mkdtemp(prefix="fix-repro-"))
    path = base / "wt"
    try:
        added = _git(repo, "worktree", "add", "--detach", str(path), rev)
        if added.returncode != 0:
            raise RuntimeError(f"git worktree add {rev} failed: {added.stderr.strip()}")
        yield path
    finally:
        _git(repo, "worktree", "remove", "--force", str(path))
        _git(repo, "worktree", "prune")
        try:
            base.rmdir()
        except OSError as exc:
            LOG.debug("temporary directory %s not removed: %s", base, exc)


def run_pytest(cwd: Path, test_ids: list[str]) -> int:
    """Run pytest on the given ids and return its exit code.

    Args:
        cwd: Worktree used as working directory.
        test_ids: Pytest node ids or file paths.

    Returns:
        The pytest process exit code, run with the module-level ``RUNNER_PYTHON``.
    """
    cmd = [RUNNER_PYTHON, "-m", "pytest", "-q", "-p", "no:cacheprovider", *test_ids]
    return subprocess.run(
        cmd, cwd=cwd, env=_env(), capture_output=True, text=True, check=False, timeout=900
    ).returncode


def resolve_python(repo: Path, override: str | None) -> str:
    """Choose the interpreter that runs pytest.

    Args:
        repo: Repository directory searched for ``venv_skillopt/bin/python``.
        override: Value of ``--python``, or None.

    Returns:
        ``override`` if given, else the repository venv interpreter if it exists,
        else ``sys.executable``.
    """
    if override:
        return override
    venv_python = repo / "venv_skillopt" / "bin" / "python"
    return str(venv_python) if venv_python.exists() else sys.executable


def runner_can_run_pytest(interpreter: str) -> bool:
    """Check that an interpreter can import and run pytest.

    Args:
        interpreter: Path of the interpreter used for replays.

    Returns:
        True when ``<interpreter> -m pytest --version`` exits 0.
    """
    try:
        result = subprocess.run(
            [interpreter, "-m", "pytest", "--version"],
            env=_env(), capture_output=True, text=True, check=False, timeout=60,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        LOG.debug("runner preflight failed for %s: %s", interpreter, exc)
        return False
    return result.returncode == 0


def _copy_tests(repo: Path, commit: str, wt: Path, test_ids: list[str]) -> None:
    """Copy the commit's version of each named test file into a worktree.

    Args:
        repo: Repository directory.
        commit: Commit supplying the file contents.
        wt: Destination worktree.
        test_ids: Test ids from the trailers.

    Raises:
        RuntimeError: If a named file does not exist at ``commit``.
    """
    for rel in sorted({t.split("::")[0] for t in test_ids}):
        shown = _git(repo, "show", f"{commit}:{rel}")
        if shown.returncode != 0:
            raise RuntimeError(f"{rel} does not exist at {commit[:7]}")
        target = wt / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(shown.stdout, encoding="utf-8")


def replay(repo: Path, commit: str, rev: str, test_ids: list[str]) -> int:
    """Run the commit's tests inside a worktree at ``rev``.

    Args:
        repo: Repository directory.
        commit: Commit whose version of the test files is copied in.
        rev: Revision checked out in the worktree.
        test_ids: Test ids from the trailers.

    Returns:
        The pytest exit code.
    """
    with worktree(repo, rev) as wt:
        _copy_tests(repo, commit, wt, test_ids)
        return run_pytest(wt, test_ids)


def judge(repo: Path, sha: str) -> tuple[str, str]:
    """Replay one ``fix(`` commit and return its verdict.

    Args:
        repo: Repository directory.
        sha: The ``fix(`` commit.

    Returns:
        ``(verdict, detail)``.
    """
    claims = parse_trailers(_git(repo, "log", "-1", "--format=%B", sha).stdout)
    if not claims:
        return "MISSING_TRAILER", "fix( commit carries no 'Repro:' trailer"
    ids = [c for c in claims if c != "manual"]
    if not ids:
        return "MANUAL", "Repro: manual (not replayed)"
    bad = sorted({i.split("::")[0] for i in ids if not i.split("::")[0].endswith(".py")})
    if bad:
        return "UNREPLAYED", f"no runner for {', '.join(bad)} (pytest replays .py only)"
    code = replay(repo, sha, f"{sha}^", ids)
    if code == 0:
        return "PASSES_ON_PARENT", "tests pass on the parent, so they do not reproduce the defect"
    if code != 1:
        return "WRONG_FAILURE", f"pytest exited {code} on the parent, expected 1; {HINT}"
    code = replay(repo, sha, sha, ids)
    if code != 0:
        return "FAILS_AT_COMMIT", f"pytest exited {code} at the commit, expected 0"
    return "OK", f"{len(ids)} test id(s) fail on the parent and pass at the commit"


def select_fixes(repo: Path, commits: list[str]) -> list[str]:
    """Keep the ``fix(`` commits that touch a source file.

    Args:
        repo: Repository directory.
        commits: Candidate SHAs.

    Returns:
        The SHAs to replay, in order.
    """
    picked = []
    for sha in commits:
        subject = _git(repo, "log", "-1", "--format=%s", sha).stdout.strip()
        if _FIX_SUBJECT.match(subject) and touches_source(repo, sha):
            picked.append(sha)
    return picked


def main(argv: list[str] | None = None) -> int:
    """Entry point.

    Args:
        argv: Argument list; defaults to ``sys.argv[1:]``.

    Returns:
        0 when no violation, 2 otherwise.
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--range", dest="spec", required=True, help="<base>..<head>")
    parser.add_argument("--repo", default=".", help="repository path (default: cwd)")
    parser.add_argument(
        "--python",
        default=None,
        help="interpreter that runs pytest (default: <repo>/venv_skillopt/bin/python, else this one)",
    )
    args = parser.parse_args(argv)
    repo = Path(args.repo).resolve()
    global RUNNER_PYTHON
    RUNNER_PYTHON = resolve_python(repo, args.python)
    try:
        fixes = select_fixes(repo, list_commits(repo, normalize_range(args.spec)))
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if fixes and not runner_can_run_pytest(RUNNER_PYTHON):
        print(
            f"RUNNER_UNAVAILABLE: {RUNNER_PYTHON} cannot run pytest; nothing was replayed. "
            "Re-run with --python <venv python> (for example venv_skillopt/bin/python).",
            file=sys.stderr,
        )
        return 2
    violations = 0
    for sha in fixes:
        verdict, detail = judge(repo, sha)
        violations += verdict not in ("OK", "MANUAL")
        print(f"{sha[:7]} {verdict} {detail}")
    print(f"{len(fixes)} fix( commits in range, {violations} violation(s)")
    return 2 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
