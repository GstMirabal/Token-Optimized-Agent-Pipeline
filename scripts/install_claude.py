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


def main() -> int:
    parser = argparse.ArgumentParser(description="Install the .agents Claude Code bridge.")
    parser.add_argument("--profile", help="Optional project profile to install (profiles/<name>)")
    args = parser.parse_args()

    # nucleus_neutrality (agents.md §5): refuse when .agents is the core repo itself.
    if (AGENTS_DIR / ".git").is_dir():
        print(f"🛑 Refusing to install: {AGENTS_DIR} is the .agents core repo itself, "
              "not a host project submodule.", file=sys.stderr)
        return 1

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

    (AGENTS_DIR / ".claude_bridge.lock").touch()
    print(f"🔒 Bridge installed. Marked {AGENTS_DIR / '.claude_bridge.lock'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
