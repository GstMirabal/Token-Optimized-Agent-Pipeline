"""Portable installer for the .agents bridge.

invoked_by: scripts/install.sh, start_workflow.md#bridge_check, hooks/on_init.py.

Cross-platform port of the original bash installer (install.sh is now a
thin wrapper around this). Idempotent: safe to re-run any time.

Usage:
    python3 .agents/scripts/install.py [--profile <name>] [--profile-path <path>]
        [--target claude|cursor|both]

What it does:
  1. Symlinks agents/*.md, commands/*.md and skills/*/ into the host's .claude/
     tree, so Claude Code auto-discovers them (it never reads inside a submodule).
     Falls back to copying when symlinks are unavailable (e.g. Windows without
     Developer Mode) — re-run after submodule updates to refresh copies.
  2. Non-destructively merges claude/settings.hooks.json into the host's
     .claude/settings.json, and claude/mcp.json into the host's .mcp.json.
  3. Appends the constitution import (@.agents/agents.md) to the host CLAUDE.md.
  4. Appends any missing .gitignore entries for the bridge mirror (CLAUDE.md,
     .claude/agents|commands|skills, .claude/settings.local.json) and
     graphify-out/ — everything regenerated locally that must never be
     committed. .claude/settings.json itself is left trackable on purpose:
     it degrades gracefully without the submodule and must survive a fresh
     clone for SessionStart to ever bootstrap the rest.
  5. With --profile or --profile-path: additionally links the profile's
     {agents,skills} and imports its rules. --profile resolves
     profiles/<name> inside the submodule (illustrative packs only). --profile-path
     accepts a host-controlled directory outside the submodule (RA-15 production
     profiles). The two flags are mutually exclusive.
  6. Prunes, per machine, any `sandbox.excludedCommands` line a previous
     install rendered for `with_env.py` from the host's untracked
     .claude/settings.local.json (host mode only). No exclusions are shipped:
     a command chained after any excluded entry runs unsandboxed. Other keys
     are left untouched; no change means no write. Before any write, the
     Claude bridge refuses with exit 2 when an excluded entry would survive
     the install in .claude/settings.json or .claude/settings.local.json
     (Sprint 056, D8): it names each entry and its file, and writes nothing.
  7. Marks .agents/.bridge_claude.lock and/or .agents/.bridge_cursor.lock
     (per --target) so hooks/on_init.py and start_workflow bridge_check
     can detect a deliberate submodule update and re-link automatically.
"""
import argparse
import errno
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
AGENTS_DIR = SCRIPT_DIR.parent
HOST_DIR = AGENTS_DIR.parent

sys.path.insert(0, str(SCRIPT_DIR))
import json

from _mode import is_nucleus
from merge_json import RETIRED_VALUES, merge

BRIDGE_WRITE_DENIED = 3
EXCLUSION_REFUSED = 2
RENDER_OWNED_RE = re.compile(r"^.+ -I .+/scripts/with_env\.py \S+$")


def _symlink_matches(dest: Path, target: str) -> bool:
    """Whether dest is already a symlink pointing at target.

    Args:
        dest: Existing symlink to inspect.
        target: Expected relative link target.

    Returns:
        bool: True if dest's readlink equals target; False on mismatch or OSError.
    """
    try:
        return str(dest.readlink()) == target
    except OSError:
        return False


def link_one(target: str, dest: Path) -> None:
    """Creates dest as a relative symlink to target, never clobbering host content."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_symlink():
        if _symlink_matches(dest, target):
            return  # already correctly linked
        print(f"⚠️  Skipping {dest}: exists as a different symlink.")
        return
    if dest.exists():
        print(f"⚠️  Skipping {dest}: already exists and is not our symlink.")
        return
    try:
        dest.symlink_to(target)
        print(f"✅ Linked {dest} -> {target}")
    except OSError:
        # Windows without Developer Mode: degrade to a copy.
        src = (dest.parent / target).resolve()
        if src.is_dir():
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)
        print(f"✅ Copied (no symlink support) {dest}")


def install_command(target: str, nucleus: bool) -> str:
    """The exact command a human runs outside the sandbox to install a target.

    Args:
        target: Bridge target (`claude`, `cursor` or `both`).
        nucleus: True in nucleus mode, False in a host (submodule) checkout.

    Returns:
        str: `python3 scripts/install.py --target <t>` in the nucleus,
        `python3 .agents/scripts/install.py --target <t>` in a host.
    """
    prefix = "" if nucleus else ".agents/"
    return f"python3 {prefix}scripts/install.py --target {target}"


def _report_write_denied(dest: Path) -> None:
    """Print the one-line advisory for a denied bridge write to stderr.

    Args:
        dest: Path whose write was refused; shown relative to the host directory when possible.
    """
    try:
        shown = dest.relative_to(HOST_DIR)
    except ValueError:
        shown = dest
    print(
        f"⚠️  PermissionError: cannot write {shown} (agent sandbox protects it). "
        f"Run `{install_command('claude', is_nucleus())}` outside the sandbox.",
        file=sys.stderr,
    )


def _write_json(dest: Path, data: dict) -> None:
    """Write data to dest as JSON, translating a refused write into an advisory.

    Args:
        dest: Settings file to create or overwrite.
        data: JSON-serialisable mapping to store.

    Raises:
        SystemExit: With BRIDGE_WRITE_DENIED when the write is refused by
            permissions; any other OSError propagates unchanged.
    """
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(data, indent=2) + "\n")
    except OSError as exc:
        if not isinstance(exc, PermissionError) and exc.errno not in (errno.EPERM, errno.EACCES):
            raise
        _report_write_denied(dest)
        raise SystemExit(BRIDGE_WRITE_DENIED) from exc


def merge_into(template: Path, dest: Path) -> None:
    """Merge a JSON template into dest without clobbering existing keys.

    Args:
        template: Template JSON file shipped by the framework.
        dest: Settings file to create or update.

    Raises:
        SystemExit: With BRIDGE_WRITE_DENIED when the write is refused by
            permissions; any other OSError propagates unchanged.
    """
    template_data = json.loads(template.read_text())
    dest_data = json.loads(dest.read_text()) if dest.exists() else {}
    _write_json(dest, merge(dest_data, template_data))
    print(f"✅ Merged {template} -> {dest}")


def prune_rendered_exclusions(host_dir: Path) -> None:
    """Remove with_env exclusion lines of the rendered shape from settings.

    The framework ships no `sandbox.excludedCommands`: a command chained
    after any excluded entry runs unsandboxed. Every string entry shaped
    `<interpreter> -I <path>/scripts/with_env.py <name>` (RENDER_OWNED_RE,
    anchored on that suffix; interpreter and path may contain spaces) is
    removed. That covers lines rendered by an earlier install and also a
    host-written `python3 -I .agents/scripts/with_env.py <name>` line; the
    pruning of the latter is the safe direction, since it is the same escape.
    Every other key and entry, including other host exclusions and the
    rendered write-denies, is left untouched. No file, a root JSON value
    that is not an object, or nothing to prune means no write.

    Args:
        host_dir: Host root holding `.claude/settings.local.json`.

    Raises:
        SystemExit: With BRIDGE_WRITE_DENIED when the write is refused.
    """
    dest = host_dir / ".claude" / "settings.local.json"
    if not dest.exists():
        return
    data = json.loads(dest.read_text())
    if not isinstance(data, dict):
        return
    sandbox = data.get("sandbox")
    current = sandbox.get("excludedCommands") if isinstance(sandbox, dict) else None
    if not isinstance(current, list):
        return
    kept = [c for c in current if not (isinstance(c, str) and RENDER_OWNED_RE.match(c))]
    pruned = len(current) - len(kept)
    if pruned == 0:
        return
    if kept:
        sandbox["excludedCommands"] = kept
    else:
        del sandbox["excludedCommands"]
    _write_json(dest, data)
    print(f"✅ Pruned {pruned} rendered with_env exclusion(s) -> {dest}")


def _excluded_commands(dest: Path) -> list:
    """Return the sandbox.excludedCommands list of a settings file.

    Args:
        dest: Settings JSON file to read.

    Returns:
        list: The entries, or an empty list when the file, the `sandbox`
            object or the list is absent, or the root is not an object.
    """
    if not dest.exists():
        return []
    data = json.loads(dest.read_text())
    sandbox = data.get("sandbox") if isinstance(data, dict) else None
    current = sandbox.get("excludedCommands") if isinstance(sandbox, dict) else None
    return current if isinstance(current, list) else []


def surviving_exclusions(host_dir: Path) -> list[tuple[str, object]]:
    """List the excludedCommands entries the install would leave in place.

    In `.claude/settings.json` the merge prunes only the values retired from
    earlier templates (`merge_json.RETIRED_VALUES`); in
    `.claude/settings.local.json` `prune_rendered_exclusions` removes only
    render-owned lines (RENDER_OWNED_RE). Every other entry survives, and any
    surviving entry is an escape: a command chained after it runs unsandboxed
    (`N1`). Reads only; writes nothing.

    Args:
        host_dir: Host root holding the `.claude/` settings files.

    Returns:
        list[tuple[str, object]]: (relative file path, entry) pairs, in file order.
    """
    retired = RETIRED_VALUES["sandbox.excludedCommands"]
    found: list[tuple[str, object]] = []
    for entry in _excluded_commands(host_dir / ".claude" / "settings.json"):
        if not (isinstance(entry, str) and entry in retired):
            found.append((".claude/settings.json", entry))
    for entry in _excluded_commands(host_dir / ".claude" / "settings.local.json"):
        if not (isinstance(entry, str) and RENDER_OWNED_RE.match(entry)):
            found.append((".claude/settings.local.json", entry))
    return found


def report_surviving_exclusions(found: list[tuple[str, object]]) -> None:
    """Print the refusal for host-owned excludedCommands entries to stderr.

    Args:
        found: (relative file path, entry) pairs from surviving_exclusions.
    """
    print("🛑 Install refused: the host's Claude Code settings carry "
          "sandbox.excludedCommands entries.", file=sys.stderr)
    for rel, entry in found:
        print(f"   - {rel}: {json.dumps(entry)}", file=sys.stderr)
    print("   Reason: any excluded entry is an escape. A command chained after it runs "
          "wholly unsandboxed (N1; rules/project_topology.md section 4, "
          "\"Excluded commands\" row). No entry may be added, by the framework or by a host.",
          file=sys.stderr)
    print(f"   Fix: remove each entry listed above from the file named, then re-run "
          f"`{install_command('claude', False)}`. Nothing was written.", file=sys.stderr)


USER_ADVICE_RE = re.compile(r"`(cp ~/\.claude/settings\.json [^`]*\.sandbox\.network\.strictAllowlist[^`]*)`")


def user_settings_path() -> Path:
    """Return the user-scope Claude settings path (patched by tests).

    Returns:
        Path: `~/.claude/settings.json` under the current home directory.
    """
    return Path.home() / ".claude" / "settings.json"


def read_base_advice() -> tuple[list[str], str]:
    """Parse the base domain list and the jq command from the topology rule.

    The rule file is the single source (`rules/project_topology.md` section 5);
    nothing is duplicated here.

    Returns:
        tuple[list[str], str]: (base domains, backup-and-jq command); ([], "")
        when the rule file or its command line is absent.
    """
    try:
        text = (AGENTS_DIR / "rules" / "project_topology.md").read_text(encoding="utf-8")
    except OSError:
        return [], ""
    match = USER_ADVICE_RE.search(text)
    if not match:
        return [], ""
    command = match.group(1)
    listed = command.split("+ [", 1)[-1].split("]", 1)[0]
    return re.findall(r'"([^"]+)"', listed), command


def _user_network(path: Path) -> tuple[dict, str]:
    """Read the user-scope sandbox.network block read-only.

    Args:
        path: User settings file; never created or modified.

    Returns:
        tuple[dict, str]: (network block, warning); the block is empty and the
        warning set when the file is unreadable or malformed. A missing file
        yields an empty block and no warning.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}, ""
    except (OSError, UnicodeDecodeError):
        return {}, f"{path} is unreadable"
    except ValueError:
        return {}, f"{path} is malformed JSON"
    sandbox = data.get("sandbox") if isinstance(data, dict) else None
    network = sandbox.get("network") if isinstance(sandbox, dict) else None
    return (network if isinstance(network, dict) else {}), ""


def advise_user_sandbox() -> None:
    """Print the jq command when the user-scope sandbox allowlist is incomplete.

    Advisory only: it never writes the user file and never changes the exit
    code of the install. Complete settings print nothing. This is a fault
    boundary: any Exception from the check becomes a one-line warning.
    """
    try:
        _advise_user_sandbox()
    except Exception as exc:  # noqa: BLE001 - fault boundary: advisory never changes the exit code
        print(f"⚠️  User-scope sandbox check failed for {user_settings_path()}: "
              f"{type(exc).__name__}: {exc}; install exit code unchanged.", file=sys.stderr)


def _advise_user_sandbox() -> None:
    """Run the user-scope sandbox check; may raise on malformed settings content."""
    base, command = read_base_advice()
    if not command:
        print("⚠️  Could not read the base allowlist from rules/project_topology.md; "
              "user-scope sandbox check skipped.", file=sys.stderr)
        return
    network, warning = _user_network(user_settings_path())
    if warning:
        print(f"⚠️  {warning}; treating the user-scope sandbox as unconfigured.", file=sys.stderr)
    listed = network.get("allowedDomains")
    present = set(listed) if isinstance(listed, list) else set()
    missing = [d for d in base if d not in present]
    if network.get("strictAllowlist") is True and not missing:
        return
    if network.get("strictAllowlist") is not True:
        print("ℹ️  User-scope sandbox: sandbox.network.strictAllowlist is not true.")
    if missing:
        print(f"ℹ️  User-scope sandbox: allowedDomains is missing {', '.join(missing)}.")
    print("   Advisory only (install exit code unchanged). Run, then see "
          "rules/project_topology.md section 5:")
    print(f"   {command}")


def add_claude_import(import_line: str) -> None:
    claude_md = HOST_DIR / "CLAUDE.md"
    existing = claude_md.read_text() if claude_md.exists() else ""
    if import_line not in existing.splitlines():
        with claude_md.open("a") as f:
            f.write(import_line + "\n")
        print(f"✅ Added import to CLAUDE.md: {import_line}")


# Submodule-dependent bridge mirror (regenerated by this script) and the
# graphify knowledge-graph output (regenerated by its own git hooks on every
# commit/checkout — see skills/graphify/SKILL.md "For git commit hook") must
# never be committed to the host. Found the hard way on a live host: a
# pre-existing broad `settings.json` rule silently swallowed
# .claude/settings.json (which must stay tracked — see below) while leaving
# the actual bridge mirror merely untracked-but-not-ignored, so an accidental
# `git add -A` or a plain `git clean -fd` could commit/wipe it either way;
# separately, graphify-out/ had accumulated 23MB across 20 commits with no
# pruning. `.agents`'s own .gitignore already excludes both for itself
# (nucleus_neutrality doesn't apply here — every host needs this, not just
# the nucleus), so hosts get the same hygiene automatically.
GITIGNORE_ENTRIES = [
    "/CLAUDE.md",
    "/.claude/agents/",
    "/.claude/commands/",
    "/.claude/skills/",
    "/.claude/settings.local.json",
    "/.cursor/commands/",
    "/.cursor/rules/",
    "/.cursor/agents/",
    "/.cursor/mcp.json",
    "/graphify-out/",
]


def ensure_gitignore_entries() -> None:
    """Appends any missing bridge/graphify entries to the host's root
    .gitignore. Idempotent: never touches or reorders existing lines, never
    removes a host's own entries (e.g. if they deliberately track
    graphify-out/ for some reason, re-running this won't fight them — it only
    adds what's absent)."""
    gitignore = HOST_DIR / ".gitignore"
    existing_lines = gitignore.read_text().splitlines() if gitignore.exists() else []
    missing = [e for e in GITIGNORE_ENTRIES if e not in existing_lines]
    if not missing:
        return
    with gitignore.open("a") as f:
        if existing_lines and existing_lines[-1] != "":
            f.write("\n")
        f.write(
            "\n# .agents Claude/Cursor bridge + graphify output "
            "(regenerated locally, never commit)\n"
        )
        for entry in missing:
            f.write(entry + "\n")
    print(f"✅ Added {len(missing)} missing .gitignore entr{'y' if len(missing) == 1 else 'ies'} "
          f"for the bridge/graphify output: {', '.join(missing)}")


def scaffold_identity_config() -> None:
    """Copies docs/standards/templates/IDENTITY_TEMPLATE.json to the host root
    as identity.config.json, but only the first time — never touches or merges
    over a host's existing copy (plain existence-guard, same criterion as
    link_one(), not a recursive merge since this is a flat file). Best-effort
    auto-fills repo_slug from `git remote get-url origin`; a missing/foreign
    remote is not a failure, it just leaves repo_slug blank for the human to
    fill in manually. This script never runs render_readme.py itself — that
    stays a deliberate, manual step for the host owner.
    """
    dest = HOST_DIR / "identity.config.json"
    if dest.exists():
        return
    template = AGENTS_DIR / "docs" / "standards" / "templates" / "IDENTITY_TEMPLATE.json"
    data = json.loads(template.read_text())

    try:
        remote_url = subprocess.run(
            ["git", "-C", str(HOST_DIR), "remote", "get-url", "origin"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        match = re.search(r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>.+?)(?:\.git)?/?$", remote_url)
        if match:
            data["repo_slug"] = f"{match.group('owner')}/{match.group('repo')}"
    except (subprocess.CalledProcessError, OSError) as exc:
        print(f"ℹ️  Could not auto-detect repo_slug from 'git remote get-url origin': {exc}")

    dest.write_text(json.dumps(data, indent=2) + "\n")
    print(f"✅ Scaffolded {dest}")
    print("📝 Fill in identity.config.json with your project's details, then run "
          "`.agents/scripts/render_readme.py` manually to generate your README — "
          "the installer never does this automatically.")


BRIDGE_LOCKS_BY_TARGET = {
    "claude": (".bridge_claude.lock",),
    "cursor": (".bridge_cursor.lock",),
    "both": (".bridge_claude.lock", ".bridge_cursor.lock"),
}


def current_submodule_commit() -> str:
    """HEAD of the .agents submodule, or ``unknown`` outside a git context."""
    try:
        return subprocess.run(
            ["git", "-C", str(AGENTS_DIR), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (subprocess.CalledProcessError, OSError):
        return "unknown"


def write_bridge_locks(target: str) -> None:
    """Record the installed submodule commit in per-target lock files."""
    commit = current_submodule_commit()
    legacy_lock = AGENTS_DIR / ".claude_bridge.lock"
    if legacy_lock.exists():
        legacy_lock.unlink()
    for lock_name in BRIDGE_LOCKS_BY_TARGET[target]:
        lock_path = AGENTS_DIR / lock_name
        lock_path.write_text(commit + "\n")
        print(f"🔒 Bridge installed at commit {commit[:12]}. Marked {lock_path}")


NUCLEUS_SANDBOX_BLOCK: dict = {"sandbox": {"enabled": True, "autoAllowBashIfSandboxed": True}}

# Settings `env` pair that lets pip pass TLS inside the sandbox (HM A1-10). The
# certificate path is the macOS one and the failure is trustd's, so the pair is
# merged only when `sys.platform == "darwin"` (plan D59).
DARWIN_PIP_ENV: dict[str, str] = {
    "PIP_USE_DEPRECATED": "legacy-certs",
    "PIP_CERT": "/etc/ssl/cert.pem",
}

# `sandbox.filesystem.denyWrite` entries owned by the nucleus (ADR-0019 D9 A3, B5).
NUCLEUS_DENY_WRITE: tuple[str, ...] = ("./agents", "./venv_skillopt")

# Template `denyWrite` entries naming the host-side submodule; `./.agents` does
# not exist in the nucleus, so they are left out of the nucleus merge.
HOST_ONLY_DENY_WRITE: frozenset[str] = frozenset({"./.agents", "./.git/modules/.agents"})


def platform_env_block() -> dict:
    """Return the settings fragment of the platform `env` pair.

    Returns:
        `{"env": DARWIN_PIP_ENV}` copy when `sys.platform == "darwin"`, else `{}`.
    """
    return {"env": dict(DARWIN_PIP_ENV)} if sys.platform == "darwin" else {}


def merge_platform_env(dest: Path) -> None:
    """Merge the platform `env` pair into a host settings file, non-destructively.

    An `env` key the file already holds keeps its value (the shared merge leaves
    a conflicting scalar alone). On a platform other than macOS nothing is
    read or written.

    Args:
        dest: Settings file to update.

    Raises:
        SystemExit: With BRIDGE_WRITE_DENIED when the write is refused.
    """
    block = platform_env_block()
    if not block:
        return
    data = json.loads(dest.read_text()) if dest.exists() else {}
    merged = merge(json.loads(json.dumps(data)), block)
    if merged != data:
        _write_json(dest, merged)
        print(f"✅ Merged the pip env pair -> {dest}")


def nucleus_settings_block(root: Path) -> dict:
    """Build the settings fragment the nucleus bridge merges.

    Holds the sandbox flags, the `sandbox` and `permissions` keys of the
    template (minus the host-only submodule `denyWrite` paths), the nucleus
    `denyWrite` entries and the platform `env` pair. The template `hooks` block
    is never included: its paths are host-relative.

    Args:
        root: Nucleus root holding `claude/settings.hooks.json`.

    Returns:
        A new dict ready for `merge`.
    """
    template = json.loads((root / "claude" / "settings.hooks.json").read_text())
    shipped = {key: template[key] for key in ("sandbox", "permissions") if key in template}
    block = merge(json.loads(json.dumps(NUCLEUS_SANDBOX_BLOCK)), json.loads(json.dumps(shipped)))
    deny_write = block["sandbox"].setdefault("filesystem", {}).setdefault("denyWrite", [])
    deny_write[:] = [e for e in deny_write if e not in HOST_ONLY_DENY_WRITE]
    deny_write.extend(e for e in NUCLEUS_DENY_WRITE if e not in deny_write)
    return merge(block, platform_env_block())


def merge_nucleus_sandbox(root: Path) -> None:
    """Merge the nucleus settings block into `.claude/settings.json`.

    Writes the fragment of `nucleus_settings_block` (D12, plan D59): no hook and
    no `sandbox.excludedCommands`. Existing keys are kept, retired entries are
    pruned by the shared merge, and a second run changes nothing.

    Args:
        root: Nucleus root holding `.claude/settings.json`.

    Raises:
        SystemExit: Non-zero with a message when the file root, its `sandbox`
            value or its `permissions` value is present and not an object;
            nothing is written.
    """
    dest = root / ".claude" / "settings.json"
    data = json.loads(dest.read_text()) if dest.exists() else {}
    bad_key = isinstance(data, dict) and any(
        k in data and not isinstance(data[k], dict) for k in ("sandbox", "permissions", "env"))
    if not isinstance(data, dict) or bad_key:
        raise SystemExit(f"🛑 {dest}: the root or its `sandbox`, `permissions` or `env` value is "
                         "not a JSON object; refusing to overwrite it. "
                         "Fix the file and re-run the installer.")
    merged = merge(data, nucleus_settings_block(root))
    if not dest.exists() or merged != json.loads(dest.read_text()):
        _write_json(dest, merged)
        print(f"✅ Merged the nucleus settings block -> {dest}")
    prune_rendered_exclusions(root)


def install_nucleus_bridge() -> int:
    """Minimal self-bridge for the nucleus repo itself: commands + agents +
    constitution import + the sandbox/permissions settings block, so `/agents:*` works
    while developing the framework. No hooks (paths are host-relative), no
    skills links, no MCP, no scaffolding — nucleus_neutrality governs
    structure, not tooling access."""
    print(f"🧬 Nucleus detected — installing minimal self-bridge into {AGENTS_DIR / '.claude'} ...")
    merge_nucleus_sandbox(AGENTS_DIR)
    for f in sorted((AGENTS_DIR / "commands").glob("*.md")):
        link_one(f"../../../commands/{f.name}",
                 AGENTS_DIR / ".claude" / "commands" / "agents" / f.name)
    for f in sorted((AGENTS_DIR / "agents").glob("*.md")):
        link_one(f"../../agents/{f.name}", AGENTS_DIR / ".claude" / "agents" / f.name)
    claude_md = AGENTS_DIR / "CLAUDE.md"
    existing = claude_md.read_text() if claude_md.exists() else ""
    if "@agents.md" not in existing.splitlines():
        with claude_md.open("a") as f:
            f.write("@agents.md\n")
        print("✅ Added constitution import to nucleus CLAUDE.md")
    print("🔒 Nucleus self-bridge installed. Restart the Claude Code session to load it.")
    return 0


def install_git_commit_msg(
    *,
    hooks_dir: Path | None = None,
    script_path: str = ".agents/hooks/on_commit_msg.py",
) -> None:
    """Install a native commit-msg hook so message gates cover every commit.

    `on_commit.py` runs at pre-commit time, where the message does not yet
    exist — git has not finalised `COMMIT_EDITMSG`, so reading it there would
    test the previous commit's message. The agent path escapes this because its
    Bash command carries `-m`; a terminal or IDE commit had no message gate at
    all. `commit-msg` is the hook that does have it.

    Same ownership rule as the pre-commit installer: an existing hook belongs
    to the project and is never overwritten.
    """
    if hooks_dir is None:
        hooks_dir = HOST_DIR / ".git" / "hooks"
    if not hooks_dir.parent.is_dir():
        return
    hooks_dir.mkdir(parents=True, exist_ok=True)

    hook_path = hooks_dir / "commit-msg"
    body = (
        "#!/usr/bin/env bash\n"
        "# Installed by .agents/scripts/install.py\n"
        "#\n"
        "# Conventional Commit format, regression-test and dependency-\n"
        "# justification gates. pre-commit cannot run these: the message does\n"
        "# not exist yet at that point.\n"
        "set -euo pipefail\n"
        f"[ -f {script_path} ] || exit 0\n"
        f'exec python3 {script_path} "$1"\n'
    )

    if hook_path.exists():
        current = hook_path.read_text(encoding="utf-8", errors="replace")
        if "on_commit_msg.py" in current:
            return
        print(
            "ℹ️  A commit-msg hook already exists and was left alone. To gate "
            "commit messages too, add:\n"
            f'      python3 {script_path} "$1"'
        )
        return

    hook_path.write_text(body, encoding="utf-8")
    hook_path.chmod(0o755)
    print("🪝 Installed .git/hooks/commit-msg (message gates on every commit path)")


def install_git_pre_commit(
    *,
    hooks_dir: Path | None = None,
    script_path: str = ".agents/hooks/on_commit.py",
) -> None:
    """Install a native pre-commit hook so a terminal commit is scanned too.

    The secret scanner runs as a Claude Code `PreToolUse` hook, which sees only
    commits the agent makes through its Bash tool. A commit typed in a terminal,
    made from an IDE, or produced by any other tool bypasses it entirely — and
    those are most of the commits in a repository with a human in it.

    Written only when no pre-commit hook exists. An existing one belongs to the
    project and is never overwritten; the path to add is printed instead.
    """
    if hooks_dir is None:
        hooks_dir = HOST_DIR / ".git" / "hooks"
    if not hooks_dir.parent.is_dir():
        return
    hooks_dir.mkdir(parents=True, exist_ok=True)

    hook_path = hooks_dir / "pre-commit"
    body = (
        "#!/usr/bin/env bash\n"
        "# Installed by .agents/scripts/install.py\n"
        "#\n"
        "# The Claude Code PreToolUse hook only sees commits the agent makes.\n"
        "# This covers every other path into the repository.\n"
        "set -euo pipefail\n"
        f"[ -f {script_path} ] || exit 0\n"
        f"exec python3 {script_path}\n"
    )

    if hook_path.exists():
        current = hook_path.read_text(encoding="utf-8", errors="replace")
        if "on_commit.py" in current:
            return
        print(
            "ℹ️  A pre-commit hook already exists and was left alone. To scan "
            "terminal commits too, add:\n"
            f"      python3 {script_path}"
        )
        return

    hook_path.write_text(body, encoding="utf-8")
    hook_path.chmod(0o755)
    print("🪝 Installed .git/hooks/pre-commit (scans terminal commits too)")


def install_git_pre_push(
    *,
    hooks_dir: Path | None = None,
    script_path: str = ".agents/hooks/on_push.py",
) -> None:
    """Install a native pre-push hook so force-push is blocked under any tool."""
    if hooks_dir is None:
        hooks_dir = HOST_DIR / ".git" / "hooks"
    if not hooks_dir.parent.is_dir():
        return
    hooks_dir.mkdir(parents=True, exist_ok=True)

    hook_path = hooks_dir / "pre-push"
    body = (
        "#!/usr/bin/env bash\n"
        "# Installed by .agents/scripts/install.py\n"
        "#\n"
        "# Blocks force-push and non-fast-forward updates. Claude Code\n"
        "# permissions.deny does not apply under Cursor.\n"
        "set -euo pipefail\n"
        f"[ -f {script_path} ] || exit 0\n"
        f'exec python3 {script_path} "$@"\n'
    )

    if hook_path.exists():
        current = hook_path.read_text(encoding="utf-8", errors="replace")
        if "on_push.py" in current:
            return
        print(
            "ℹ️  A pre-push hook already exists and was left alone. To block "
            "force-push too, add:\n"
            '      python3 .agents/hooks/on_push.py "$@"'
        )
        return

    hook_path.write_text(body, encoding="utf-8")
    hook_path.chmod(0o755)
    print("🪝 Installed .git/hooks/pre-push (blocks force-push for every tool)")


def install_host_git_hooks() -> None:
    """Install native git hooks that must cover terminal and Cursor paths."""
    install_git_pre_commit()
    install_git_commit_msg()
    install_git_pre_push()


def install_nucleus_git_hooks() -> None:
    """Install git hooks into the nucleus repo (repo-relative hook script paths)."""
    hooks_dir = AGENTS_DIR / ".git" / "hooks"
    install_git_pre_commit(hooks_dir=hooks_dir, script_path="hooks/on_commit.py")
    install_git_commit_msg(hooks_dir=hooks_dir, script_path="hooks/on_commit_msg.py")
    install_git_pre_push(hooks_dir=hooks_dir, script_path="hooks/on_push.py")


def install_profile_from_dir(profile_dir: Path) -> None:
    """Link a profile pack's agents/skills into the host bridge and import rules."""
    profile_dir = profile_dir.resolve()
    agents_src = profile_dir / "agents"
    if agents_src.is_dir():
        for agent_file in sorted(agents_src.glob("*.md")):
            dest = HOST_DIR / ".claude" / "agents" / agent_file.name
            link_one(os.path.relpath(agent_file, dest.parent), dest)
    skills_src = profile_dir / "skills"
    if skills_src.is_dir():
        for skill_dir in sorted(p for p in skills_src.iterdir() if p.is_dir()):
            dest = HOST_DIR / ".claude" / "skills" / skill_dir.name
            link_one(os.path.relpath(skill_dir, dest.parent), dest)
    rules_src = profile_dir / "rules"
    if rules_src.is_dir():
        for rule_file in sorted(rules_src.glob("*.md")):
            import_path = os.path.relpath(rule_file, HOST_DIR)
            add_claude_import(f"@{import_path}")
    registry = profile_dir / "mcp" / "registry.json"
    if registry.exists():
        print(
            f"ℹ️  Profile MCP servers listed in {registry} "
            "— add the ones you need to .mcp.json manually (they may require API keys)."
        )


def resolve_profile_dir(profile: str | None, profile_path: str | None) -> Path | None:
    """Resolve --profile (submodule) or --profile-path (host/external) to a directory."""
    if profile and profile_path:
        print("🛑 Use only one of --profile or --profile-path.", file=sys.stderr)
        sys.exit(1)
    if profile_path:
        candidate = Path(profile_path)
        if not candidate.is_absolute():
            candidate = (HOST_DIR / candidate).resolve()
        else:
            candidate = candidate.resolve()
        if not candidate.is_dir():
            print(f"🛑 Profile path not found: {candidate}", file=sys.stderr)
            sys.exit(1)
        return candidate
    if profile:
        profile_dir = AGENTS_DIR / "profiles" / profile
        if not profile_dir.is_dir():
            print(f"🛑 Profile not found: {profile_dir}", file=sys.stderr)
            sys.exit(1)
        return profile_dir
    return None


def install_host_claude_bridge(profile_dir: Path | None) -> int:
    """Install the full Claude Code bridge into a host checkout.

    Refuses before any write when an excludedCommands entry would survive the
    install (surviving_exclusions; Sprint 056, D8).

    Args:
        profile_dir: Profile pack to link after the bridge, or None.

    Returns:
        int: 0 on success, EXCLUSION_REFUSED when a host exclusion is found.
    """
    found = surviving_exclusions(HOST_DIR)
    if found:
        report_surviving_exclusions(found)
        return EXCLUSION_REFUSED
    print(f"🌉 Installing Claude Code bridge for .agents into {HOST_DIR} ...")

    for f in sorted((AGENTS_DIR / "agents").glob("*.md")):
        link_one(f"../../.agents/agents/{f.name}", HOST_DIR / ".claude" / "agents" / f.name)

    for f in sorted((AGENTS_DIR / "commands").glob("*.md")):
        link_one(f"../../../.agents/commands/{f.name}",
                 HOST_DIR / ".claude" / "commands" / "agents" / f.name)

    for d in sorted((AGENTS_DIR / "skills").iterdir()):
        if d.is_dir():
            link_one(f"../../.agents/skills/{d.name}", HOST_DIR / ".claude" / "skills" / d.name)

    merge_into(AGENTS_DIR / "claude" / "settings.hooks.json",
               HOST_DIR / ".claude" / "settings.json")
    merge_platform_env(HOST_DIR / ".claude" / "settings.json")
    merge_into(AGENTS_DIR / "claude" / "mcp.json", HOST_DIR / ".mcp.json")
    prune_rendered_exclusions(HOST_DIR)

    add_claude_import("@.agents/agents.md")
    ensure_gitignore_entries()
    scaffold_identity_config()
    install_host_git_hooks()

    if profile_dir is not None:
        print(f"📦 Installing profile: {profile_dir}")
        install_profile_from_dir(profile_dir)
    return 0


def install_nucleus(args: argparse.Namespace, install_cursor_bridge) -> int:
    """Install the nucleus self-bridge for one target.

    Nucleus mode (`agents.md §5 nucleus_neutrality`): the full host bridge is
    refused, but the minimal self-bridge (commands, agents, constitution
    import, and the `sandbox` block in `.claude/settings.json`) is installed
    so the framework's own workflows are invocable while developing it.

    **Every target ends the same way** — git hooks, then the lock. Neither is
    Cursor-specific: the hooks are the secret scanner, the `#[Sprint_ID]`
    commit-message gate and the force-push block, and the lock is what tells
    the next boot the bridge is current. The `claude` branch used to
    `return install_nucleus_bridge()` before reaching either, so a Claude-only
    checkout had no gates and a lock that was never written (Sprint 041).

    Args:
        args: Parsed CLI arguments; `target` and the profile flags are read.
        install_cursor_bridge: Imported lazily by the caller to keep the
            adapter off the import path of a Claude-only install.

    Returns:
        int: 0 on success, 1 when a profile was requested.
    """
    if args.profile or args.profile_path:
        print("🛑 Profiles cannot be installed into the nucleus.", file=sys.stderr)
        return 1
    if args.target in ("claude", "both"):
        rc = install_nucleus_bridge()
        if rc != 0:
            return rc
    if args.target in ("cursor", "both"):
        install_cursor_bridge(AGENTS_DIR, nucleus=True)
    install_nucleus_git_hooks()
    write_bridge_locks(args.target)
    advise_user_sandbox()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Install the .agents bridge.")
    parser.add_argument(
        "--profile",
        help="Illustrative profile name under .agents/profiles/<name> (submodule)",
    )
    parser.add_argument(
        "--profile-path",
        dest="profile_path",
        help="Host-controlled profile directory outside the submodule (absolute or relative to host root)",
    )
    parser.add_argument(
        "--target",
        choices=["claude", "cursor", "both"],
        default="claude",
        help="Installation target: 'claude' (Claude Code, default), 'cursor' (Cursor), or 'both'"
    )
    args = parser.parse_args()
    from cursor_adapter import install_cursor_bridge

    if (AGENTS_DIR / ".git").is_dir():
        return install_nucleus(args, install_cursor_bridge)

    profile_dir = resolve_profile_dir(args.profile, args.profile_path)

    if args.target in ("claude", "both"):
        rc = install_host_claude_bridge(profile_dir)
        if rc != 0:
            return rc

    if args.target in ("cursor", "both"):
        install_cursor_bridge(HOST_DIR, nucleus=False, profile_dir=profile_dir)
        ensure_gitignore_entries()
        if args.target == "cursor":
            install_host_git_hooks()

    write_bridge_locks(args.target)
    advise_user_sandbox()
    return 0


if __name__ == "__main__":
    sys.exit(main())
