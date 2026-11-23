"""Install the GitHub broker from a signed tag or a `main` commit (ADR-0025 D5).

The human runs this script. It copies `scripts/github_broker.py` out of git
history (`git show <ref>:scripts/github_broker.py`), never from the working
tree, so agent-writable content is not executed by the installation
(`RA-19` (3)). A tag is accepted only after `verify_tag` of
`scripts/sync_agents_pin.py` validates its SSH signature against
`config/allowed_signers`. The first bootstrap has no signed tag yet, so
`--commit` accepts a full 40-hex SHA that is an ancestor of (or equal to) the
local `main` ref.

The destination is `$AGENTS_BROKER_HOME`, or `~/.config/agents-broker` when
unset (the same rule as `scripts/github_broker.py`). Only `github_broker.py` is
written; `keys/` and `config.json` are never touched.

invoked_by: docs/guides/GITHUB_BROKER_SETUP_GUIDE.md

Usage:
    python3 scripts/install_broker.py --tag vX.Y.Z
    python3 scripts/install_broker.py --commit <40-hex sha>

Exit codes:
    0 - the file was installed; one line names the source ref and destination
    2 - bad arguments, invalid or unsigned tag, commit not on `main`, git
        failure, or write failure; nothing is written (fail closed)
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root
from sync_agents_pin import verify_tag

SOURCE_PATH = "scripts/github_broker.py"
TARGET_NAME = "github_broker.py"
TAG_RE = re.compile(r"^v\d+\.\d+\.\d+$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
GIT_TIMEOUT_S = 30


def broker_home() -> Path:
    """Return the broker install directory.

    Returns:
        Path: `$AGENTS_BROKER_HOME`, or `~/.config/agents-broker` when unset.
    """
    override = os.environ.get("AGENTS_BROKER_HOME")
    return Path(override) if override else Path.home() / ".config" / "agents-broker"


def fail(reason: str) -> int:
    """Print a one-line reason on stderr.

    Args:
        reason: Why the installation was refused.

    Returns:
        int: Always 2.
    """
    print(f"[install_broker] {reason}", file=sys.stderr)
    return 2


def run_git(root: Path, args: list[str]) -> subprocess.CompletedProcess[bytes]:
    """Run git in `root` with prompts disabled; does not raise on non-zero exit.

    Args:
        root: Repository root.
        args: Arguments after `git`.

    Returns:
        subprocess.CompletedProcess[bytes]: Raw stdout and stderr.
    """
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    return subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        timeout=GIT_TIMEOUT_S,
        env=env,
        check=False,
    )


def commit_on_main(root: Path, sha: str) -> bool:
    """Tell whether `sha` is an ancestor of (or equal to) the local `main` ref.

    Args:
        root: Repository root.
        sha: Full 40-hex commit id.

    Returns:
        bool: True only when git exited 0.
    """
    result = run_git(root, ["merge-base", "--is-ancestor", sha, "refs/heads/main"])
    return result.returncode == 0


def read_source(root: Path, ref: str) -> bytes | None:
    """Read the broker source at `ref` from git history.

    Args:
        root: Repository root.
        ref: Tag name or commit SHA.

    Returns:
        bytes | None: File content, or None when git cannot produce it.
    """
    result = run_git(root, ["show", f"{ref}:{SOURCE_PATH}"])
    if result.returncode != 0 or not result.stdout:
        return None
    return result.stdout


def write_atomic(dest_dir: Path, content: bytes) -> Path:
    """Write `content` to `dest_dir/github_broker.py` atomically.

    Args:
        dest_dir: Broker home; created with mode 0o700 when missing.
        content: Bytes to install.

    Returns:
        Path: The installed file.
    """
    dest_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    target = dest_dir / TARGET_NAME
    fd, tmp_name = tempfile.mkstemp(dir=dest_dir, prefix=".github_broker.")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
        os.chmod(tmp_name, 0o600)
        os.replace(tmp_name, target)
    except BaseException:
        Path(tmp_name).unlink(missing_ok=True)
        raise
    return target


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser.

    Returns:
        argparse.ArgumentParser: Parser with the two source flags.
    """
    parser = argparse.ArgumentParser(description="Install the GitHub broker from git history.")
    parser.add_argument("--tag", help="signed tag vX.Y.Z")
    parser.add_argument("--commit", help="full 40-hex SHA of a commit of main")
    return parser


def validate_ref(root: Path, tag: str | None, commit: str | None) -> str | None:
    """Check the single source ref; return a failure reason or None.

    Args:
        root: Repository root.
        tag: Value of `--tag`, if given.
        commit: Value of `--commit`, if given.

    Returns:
        str | None: Reason to refuse, or None when the ref is trusted.
    """
    if (tag is None) == (commit is None):
        return "exactly one of --tag or --commit is required"
    if tag is not None:
        if not TAG_RE.match(tag):
            return f"tag {tag!r} does not match vX.Y.Z"
        if not verify_tag(root, tag):
            return f"tag {tag} has no valid signature"
        return None
    if not SHA_RE.match(commit or ""):
        return "--commit needs a full 40-hex lowercase SHA"
    if not commit_on_main(root, commit or ""):
        return f"commit {commit} is not an ancestor of main"
    return None


def main(argv: list[str] | None = None, root: Path | None = None) -> int:
    """Entry point.

    Args:
        argv: Arguments; defaults to `sys.argv[1:]`.
        root: Repository root; defaults to the framework root.

    Returns:
        int: 0 on success, 2 on every failure.
    """
    try:
        args = build_parser().parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 2
    repo = root if root is not None else agents_root()
    try:
        reason = validate_ref(repo, args.tag, args.commit)
        if reason:
            return fail(reason)
        ref = args.tag or args.commit
        content = read_source(repo, ref)
        if content is None:
            return fail(f"cannot read {SOURCE_PATH} at {ref}")
        target = write_atomic(broker_home(), content)
    except Exception as exc:  # noqa: BLE001 - fault boundary: any failure exits 2
        return fail(f"{type(exc).__name__}: {str(exc)[:150]}")
    print(f"[install_broker] installed {ref} -> {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
