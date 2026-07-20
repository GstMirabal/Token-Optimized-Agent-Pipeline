"""Portable installer for the .agents -> Claude Code bridge.

Cross-platform port of the original bash installer (install_claude.sh is now a
thin wrapper around this). Idempotent: safe to re-run any time.

Usage:
    python3 .agents/scripts/install_claude.py [--profile <name>]

What it does:
  1. Symlinks agents/*.md, commands/*.md and skills/*/ into the host's .claude/
     tree, so Claude Code auto-discovers them (it never reads inside a submodule).
     Falls back to copying when symlinks are unavailable (e.g. Windows without
     Developer Mode) — re-run after submodule updates to refresh copies.
  2. Non-destructively merges claude/settings.hooks.json into the host's
     .claude/settings.json, and claude/mcp.json into the host's .mcp.json.
  3. Appends the constitution import (@.agents/agents.md) to the host CLAUDE.md.
  4. With --profile: additionally links profiles/<name>/{agents,skills} and
     imports the profile's rules. Profiles are opt-in only.
  5. Marks .agents/.claude_bridge.lock so hooks/on_init.py knows not to re-run.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
AGENTS_DIR = SCRIPT_DIR.parent
HOST_DIR = AGENTS_DIR.parent

sys.path.insert(0, str(SCRIPT_DIR))
from merge_json import merge  # noqa: E402
import json  # noqa: E402


def link_one(target: str, dest: Path) -> None:
    """Creates dest as a relative symlink to target, never clobbering host content."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_symlink():
        try:
            if str(dest.readlink()) == target:
                return  # already correctly linked
        except OSError:
            pass
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


def merge_into(template: Path, dest: Path) -> None:
    template_data = json.loads(template.read_text())
    dest_data = json.loads(dest.read_text()) if dest.exists() else {}
    merged = merge(dest_data, template_data)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(merged, indent=2) + "\n")
    print(f"✅ Merged {template} -> {dest}")


def add_claude_import(import_line: str) -> None:
    claude_md = HOST_DIR / "CLAUDE.md"
    existing = claude_md.read_text() if claude_md.exists() else ""
    if import_line not in existing.splitlines():
        with claude_md.open("a") as f:
            f.write(import_line + "\n")
        print(f"✅ Added import to CLAUDE.md: {import_line}")


def install_nucleus_bridge() -> int:
    """Minimal self-bridge for the nucleus repo itself: commands + agents +
    constitution import, so `/agents:*` works while developing the framework.
    No hooks (paths are host-relative), no skills links, no MCP, no scaffolding
    — nucleus_neutrality governs structure, not tooling access."""
    print(f"🧬 Nucleus detected — installing minimal self-bridge into {AGENTS_DIR / '.claude'} ...")
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Install the .agents Claude Code bridge.")
    parser.add_argument("--profile", help="Optional project profile to install (profiles/<name>)")
    args = parser.parse_args()

    # Nucleus mode (agents.md §5 nucleus_neutrality): the full host bridge is
    # refused, but the minimal self-bridge (commands/agents/constitution) is
    # installed so the framework's own workflows are invocable while developing it.
    if (AGENTS_DIR / ".git").is_dir():
        if args.profile:
            print("🛑 Profiles cannot be installed into the nucleus.", file=sys.stderr)
            return 1
        return install_nucleus_bridge()

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
    merge_into(AGENTS_DIR / "claude" / "mcp.json", HOST_DIR / ".mcp.json")

    add_claude_import("@.agents/agents.md")

    if args.profile:
        profile_dir = AGENTS_DIR / "profiles" / args.profile
        if not profile_dir.is_dir():
            print(f"🛑 Profile not found: {profile_dir}", file=sys.stderr)
            return 1
        print(f"📦 Installing profile: {args.profile}")
        for f in sorted((profile_dir / "agents").glob("*.md")):
            link_one(f"../../.agents/profiles/{args.profile}/agents/{f.name}",
                     HOST_DIR / ".claude" / "agents" / f.name)
        if (profile_dir / "skills").is_dir():
            for d in sorted((profile_dir / "skills").iterdir()):
                if d.is_dir():
                    link_one(f"../../.agents/profiles/{args.profile}/skills/{d.name}",
                             HOST_DIR / ".claude" / "skills" / d.name)
        for r in sorted((profile_dir / "rules").glob("*.md")):
            add_claude_import(f"@.agents/profiles/{args.profile}/rules/{r.name}")
        if (profile_dir / "mcp" / "registry.json").exists():
            print(f"ℹ️  Profile MCP servers listed in profiles/{args.profile}/mcp/registry.json "
                  "— add the ones you need to .mcp.json manually (they may require API keys).")

    # Record the installed submodule commit so hooks/on_init.py (and the
    # start_workflow bridge_check) can detect a deliberate submodule update
    # and re-link any new agents/commands/skills automatically.
    try:
        commit = subprocess.run(
            ["git", "-C", str(AGENTS_DIR), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (subprocess.CalledProcessError, OSError):
        commit = "unknown"
    (AGENTS_DIR / ".claude_bridge.lock").write_text(commit + "\n")
    print(f"🔒 Bridge installed at commit {commit[:12]}. Marked {AGENTS_DIR / '.claude_bridge.lock'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
