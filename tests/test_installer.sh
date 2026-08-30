#!/usr/bin/env bash
# End-to-end sandbox test for scripts/install.sh (and its Python core).
# Simulates a host project with .agents as a submodule and asserts:
#   - symlinks resolve, host content is never clobbered, JSON merges are valid,
#   - CLAUDE.md import is added exactly once (idempotency),
#   - --profile links profile agents/skills and imports profile rules.
set -euo pipefail

AGENTS_SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

fail() { echo "❌ FAIL: $1" >&2; exit 1; }

# --- Arrange: fake host with .agents as a submodule-style checkout ----------
mkdir -p "$WORK/host/.agents"
rsync -a --exclude='.git' --exclude='node_modules' --exclude='venv_skillopt' \
  "$AGENTS_SRC/" "$WORK/host/.agents/"
echo "gitdir: ../.git/modules/.agents" > "$WORK/host/.agents/.git"
rm -f "$WORK/host/.agents/.bridge_claude.lock" "$WORK/host/.agents/.bridge_cursor.lock"

# Pre-existing host content that must survive untouched:
mkdir -p "$WORK/host/.claude/agents"
echo "host content" > "$WORK/host/.claude/agents/principal_agent.md"
echo '{"model": "opus"}' > "$WORK/host/.claude/settings.json"
printf 'node_modules/\n*.pyc\n' > "$WORK/host/.gitignore"

cd "$WORK/host"

# --- Act ---------------------------------------------------------------------
bash .agents/scripts/install.sh --profile example-project > /dev/null

# --- Assert ------------------------------------------------------------------
[ -L .claude/agents/orchestrator.md ] || fail "agent symlink missing"
[ -f .claude/agents/orchestrator.md ] || fail "agent symlink broken"
[ -L .claude/commands/agents/start.md ] || fail "command symlink missing"
[ -L .claude/skills/graphify ] || fail "skill symlink missing"
[ "$(cat .claude/agents/principal_agent.md)" = "host content" ] \
  || fail "host file was clobbered"

python3 - <<'EOF'
import json
s = json.load(open('.claude/settings.json'))
assert s["model"] == "opus", "host scalar overwritten"
assert "hooks" in s and "SessionStart" in s["hooks"], "hooks not merged"
assert "Stop" in s["hooks"], "Stop hook not merged"
assert "permissions" in s, "permissions not merged"
m = json.load(open('.mcp.json'))
assert "graphify" in m["mcpServers"], "mcp not merged"
EOF

grep -qxF "@.agents/agents.md" CLAUDE.md || fail "constitution import missing"
[ -L .claude/agents/domain_specialist_example.md ] || fail "profile agent not linked"
[ -L .claude/skills/example-api-bridge-3rd ] || fail "profile skill not linked"
grep -q "domain_example_standard" CLAUDE.md || fail "profile rule import missing"

grep -qxF "node_modules/" .gitignore || fail ".gitignore: pre-existing host entry was lost"
grep -qxF "*.pyc" .gitignore || fail ".gitignore: pre-existing host entry was lost"
for entry in "/CLAUDE.md" "/.claude/agents/" "/.claude/commands/" "/.claude/skills/" \
             "/.claude/settings.local.json" "/.cursor/commands/" "/.cursor/rules/" \
             "/.cursor/mcp.json" "/graphify-out/"; do
  grep -qxF "$entry" .gitignore || fail ".gitignore: missing bridge entry '$entry'"
done
grep -qxF "/.claude/settings.json" .gitignore \
  && fail ".gitignore: settings.json must stay trackable, not ignored"

# Idempotency: re-run must not duplicate imports nor error out.
bash .agents/scripts/install.sh --profile example-project > /dev/null
[ "$(grep -cxF "@.agents/agents.md" CLAUDE.md)" = "1" ] || fail "duplicate import on re-run"
[ "$(grep -cxF "/graphify-out/" .gitignore)" = "1" ] || fail "duplicate .gitignore entry on re-run"

[ -f .agents/.bridge_claude.lock ] || fail "bridge lock not created"
[ -s .agents/.bridge_claude.lock ] || fail "bridge lock is empty (must record the submodule commit)"

echo "✅ installer sandbox test PASSED"

# ── Nucleus mode: a real .git directory must produce the minimal self-bridge ──
NUCLEUS="$WORK/nucleus"
mkdir -p "$NUCLEUS"
rsync -a --exclude='.git' --exclude='node_modules' --exclude='venv_skillopt' \
      --exclude='graphify-out' --exclude='.claude' "$AGENTS_SRC/" "$NUCLEUS/"
mkdir -p "$NUCLEUS/.git"   # real dir -> nucleus detection
rm -f "$NUCLEUS/.bridge_claude.lock" "$NUCLEUS/.bridge_cursor.lock" "$NUCLEUS/CLAUDE.md"
( cd "$NUCLEUS" && python3 scripts/install.py > /dev/null )
[ -e "$NUCLEUS/.claude/commands/agents/start.md" ] || fail "nucleus: /agents:start not linked"
[ -e "$NUCLEUS/.claude/agents/principal_agent.md" ] || fail "nucleus: agents not linked"
grep -qx "@agents.md" "$NUCLEUS/CLAUDE.md" || fail "nucleus: constitution import missing"
[ ! -e "$NUCLEUS/.claude/skills" ] || fail "nucleus: skills must NOT be linked (minimal bridge)"
# INVERTED in Sprint 041, because the reason this was pinned stopped being true.
# The original assertion was `[ ! -e .bridge_claude.lock ]`, justified as:
# "start_workflow.md bridge_check for Claude still keys on symlink-per-source
# rather than a lock". Sprint 041 made the portable boot key on both - the lock
# AND the mirror, through scripts/bridge_state.py - so a Claude install that
# writes no lock now leaves every subsequent boot finding it stale, reinstalling,
# and still writing nothing. The premise expired; the assertion followed it.
# Same correction shape as Sprint 021 amending loop_governance.md's "advisory
# budget" once the meter existed: leaving the old justification standing while
# the fact changed is the drift RA-14 pursues.
[ -e "$NUCLEUS/.bridge_claude.lock" ] || fail "nucleus: Claude install must write its bridge lock"
[ ! -e "$NUCLEUS/.bridge_cursor.lock" ] || fail "nucleus: Claude default must write no cursor bridge lock"
( cd "$NUCLEUS" && python3 scripts/install.py --profile example-project > /dev/null 2>&1 ) \
  && fail "nucleus: profile install must be refused" || true
( cd "$NUCLEUS" && python3 scripts/install.py --profile-path /tmp/x > /dev/null 2>&1 ) \
  && fail "nucleus: external profile-path must be refused" || true
mkdir -p "$NUCLEUS/.git/hooks"
# Clear the lock the default (Claude) install above now leaves behind, so the
# isolation assertion below measures what it claims: any .bridge_claude.lock
# present after a --target cursor run was written BY that run. Before Sprint
# 041 the Claude install wrote no lock, so this directory was incidentally
# clean and the assertion passed without ever being exercised.
rm -f "$NUCLEUS/.bridge_claude.lock"
( cd "$NUCLEUS" && python3 scripts/install.py --target cursor > /dev/null )
[ -x "$NUCLEUS/.git/hooks/pre-push" ] || fail "nucleus cursor: pre-push hook missing"
grep -q "hooks/on_push.py" "$NUCLEUS/.git/hooks/pre-push" \
  || fail "nucleus cursor: pre-push hook must use repo-relative path"
[ -x "$NUCLEUS/.git/hooks/pre-commit" ] || fail "nucleus cursor: pre-commit hook missing"
[ -x "$NUCLEUS/.git/hooks/commit-msg" ] || fail "nucleus cursor: commit-msg hook missing"
[ -f "$NUCLEUS/.bridge_cursor.lock" ] || fail "nucleus cursor: .bridge_cursor.lock missing"
[ ! -e "$NUCLEUS/.bridge_claude.lock" ] || fail "nucleus cursor: must not write Claude lock"
echo "✅ nucleus self-bridge test PASSED"

# ── P4.1: --target cursor and --target both on a host with a real .git ───────
HOST_CURSOR="$WORK/host-cursor"
mkdir -p "$HOST_CURSOR/.agents"
rsync -a --exclude='.git' --exclude='node_modules' --exclude='venv_skillopt' \
  "$AGENTS_SRC/" "$HOST_CURSOR/.agents/"
echo "gitdir: ../.git/modules/.agents" > "$HOST_CURSOR/.agents/.git"
rm -f "$HOST_CURSOR/.agents/.bridge_claude.lock" "$HOST_CURSOR/.agents/.bridge_cursor.lock"
( cd "$HOST_CURSOR" && git init -q && git config user.email t@t && git config user.name t )
( cd "$HOST_CURSOR" && python3 .agents/scripts/install.py --target cursor > /dev/null )
[ -d "$HOST_CURSOR/.cursor/commands" ] || fail "cursor host: .cursor/commands missing"
[ "$(ls -1 "$HOST_CURSOR/.cursor/commands" | wc -l | tr -d ' ')" = "13" ] \
  || fail "cursor host: expected 13 commands"
[ "$(ls -1 "$HOST_CURSOR/.cursor/rules" | wc -l | tr -d ' ')" = "13" ] \
  || fail "cursor host: expected 13 rules"
[ -d "$HOST_CURSOR/.cursor/agents" ] || fail "cursor host: .cursor/agents missing"
[ "$(ls -1 "$HOST_CURSOR/.cursor/agents" | wc -l | tr -d ' ')" = "14" ] \
  || fail "cursor host: expected 14 Cursor subagents"
[ -f "$HOST_CURSOR/.cursor/agents/implementer-agent.md" ] \
  || fail "cursor host: implementer-agent.md missing"
[ -f "$HOST_CURSOR/.cursor/mcp.json" ] || fail "cursor host: mcp.json missing"
[ -x "$HOST_CURSOR/.git/hooks/pre-push" ] || fail "cursor host: pre-push missing"
grep -q "on_push.py" "$HOST_CURSOR/.git/hooks/pre-push" \
  || fail "cursor host: pre-push must call on_push.py"
[ -f "$HOST_CURSOR/.agents/.bridge_cursor.lock" ] || fail "cursor host: cursor lock missing"
[ ! -f "$HOST_CURSOR/.agents/.bridge_claude.lock" ] \
  || fail "cursor host: must not write claude lock"
for entry in "/.cursor/commands/" "/.cursor/rules/" "/.cursor/agents/" "/.cursor/mcp.json"; do
  grep -qxF "$entry" "$HOST_CURSOR/.gitignore" \
    || fail "cursor host: .gitignore missing $entry"
done
echo "✅ host --target cursor test PASSED"

HOST_BOTH="$WORK/host-both"
mkdir -p "$HOST_BOTH/.agents"
rsync -a --exclude='.git' --exclude='node_modules' --exclude='venv_skillopt' \
  "$AGENTS_SRC/" "$HOST_BOTH/.agents/"
echo "gitdir: ../.git/modules/.agents" > "$HOST_BOTH/.agents/.git"
rm -f "$HOST_BOTH/.agents/.bridge_claude.lock" "$HOST_BOTH/.agents/.bridge_cursor.lock"
( cd "$HOST_BOTH" && git init -q && git config user.email t@t && git config user.name t )
( cd "$HOST_BOTH" && python3 .agents/scripts/install.py --target both > /dev/null )
[ -L "$HOST_BOTH/.claude/commands/agents/start.md" ] || fail "both: claude command missing"
[ -d "$HOST_BOTH/.cursor/commands" ] || fail "both: cursor commands missing"
[ "$(ls -1 "$HOST_BOTH/.cursor/commands" | wc -l | tr -d ' ')" = "13" ] \
  || fail "both: expected 13 cursor commands"
[ -f "$HOST_BOTH/.agents/.bridge_claude.lock" ] || fail "both: claude lock missing"
[ -f "$HOST_BOTH/.agents/.bridge_cursor.lock" ] || fail "both: cursor lock missing"
# --target both installs cursor bridge but git hooks only on cursor-only path;
# claude path already installs hooks via install_host_claude_bridge.
[ -x "$HOST_BOTH/.git/hooks/pre-push" ] || fail "both: pre-push missing"
echo "✅ host --target both test PASSED"

# ── Sprint 028: --profile-path (host-controlled profile outside submodule) ───
HOST_EXT="$WORK/host-ext-profile"
EXTERNAL_PROFILE="$WORK/external-profile"
mkdir -p "$HOST_EXT/.agents" "$EXTERNAL_PROFILE/agents" "$EXTERNAL_PROFILE/rules"
rsync -a --exclude='.git' --exclude='node_modules' --exclude='venv_skillopt' \
  "$AGENTS_SRC/" "$HOST_EXT/.agents/"
echo "gitdir: ../.git/modules/.agents" > "$HOST_EXT/.agents/.git"
cat > "$EXTERNAL_PROFILE/agents/custom_agent.md" <<'EOF'
---
name: custom-agent
description: External profile fixture for install --profile-path.
---
# Custom agent (test fixture)
EOF
echo "# Custom rule (test fixture)" > "$EXTERNAL_PROFILE/rules/custom_rule.md"
( cd "$HOST_EXT" && git init -q && git config user.email t@t && git config user.name t )
( cd "$HOST_EXT" && python3 .agents/scripts/install.py --profile-path "$EXTERNAL_PROFILE" > /dev/null )
[ -L "$HOST_EXT/.claude/agents/custom_agent.md" ] \
  || fail "profile-path: external agent symlink missing"
[ -f "$HOST_EXT/.claude/agents/custom_agent.md" ] \
  || fail "profile-path: external agent symlink broken"
grep -q "custom_rule" "$HOST_EXT/CLAUDE.md" || fail "profile-path: rule import missing"
echo "✅ host --profile-path test PASSED"

# ---------------------------------------------------------------------------
# Native pre-commit hook. The Claude Code PreToolUse hook only sees commits the
# agent makes; every other path into the repository bypassed the scanner.
# ---------------------------------------------------------------------------

test_pre_commit_hook_is_installed() {
    local repo="$1"
    [ -x "$repo/.git/hooks/pre-commit" ] || return 1
    grep -q "on_commit.py" "$repo/.git/hooks/pre-commit" || return 1
}

test_existing_pre_commit_hook_is_not_overwritten() {
    local repo="$1"
    printf '#!/bin/sh\necho project-owned\n' > "$repo/.git/hooks/pre-commit"
    chmod +x "$repo/.git/hooks/pre-commit"
    python3 "$repo/.agents/scripts/install.py" >/dev/null 2>&1
    grep -q "project-owned" "$repo/.git/hooks/pre-commit" || return 1
}

# ---------------------------------------------------------------------------
# Nucleus --target claude (Sprint 041, U13). The branch returned
# install_nucleus_bridge() directly, skipping the git hooks and the bridge
# lock that the cursor and both branches have always installed. A Claude-only
# nucleus checkout therefore had no secret scanner and no commit-message gate,
# and its lock was never written, so every boot found it stale, reinstalled,
# and still wrote nothing. Asserted here rather than in pytest because the
# defect is in the installer's own end-to-end path.
# ---------------------------------------------------------------------------

# A directory of its own, never the $NUCLEUS reused above: this block asserts
# the Cursor mirror is absent, which is only meaningful on a checkout where no
# Cursor install has ever run. A real `git init` too, because the lock records
# HEAD and the hooks are installed into .git/hooks.
NUC_CLAUDE="$WORK/nucleus_claude_only"
mkdir -p "$NUC_CLAUDE"
rsync -a --exclude='.git' --exclude='node_modules' --exclude='venv_skillopt' \
  --exclude='.claude' --exclude='.cursor' "$AGENTS_SRC/" "$NUC_CLAUDE/"
rm -f "$NUC_CLAUDE/.bridge_claude.lock" "$NUC_CLAUDE/.bridge_cursor.lock"
git -C "$NUC_CLAUDE" init -q
git -C "$NUC_CLAUDE" config user.email "t@t"
git -C "$NUC_CLAUDE" config user.name "t"
git -C "$NUC_CLAUDE" add -A > /dev/null 2>&1
git -C "$NUC_CLAUDE" commit -q -m "seed" --no-verify > /dev/null 2>&1

python3 "$NUC_CLAUDE/scripts/install.py" --target claude > /dev/null

[ -L "$NUC_CLAUDE/.claude/commands/agents/start.md" ] \
  || fail "nucleus claude: command symlink missing"
[ -f "$NUC_CLAUDE/.bridge_claude.lock" ] \
  || fail "nucleus claude: .bridge_claude.lock not written"
[ "$(cat "$NUC_CLAUDE/.bridge_claude.lock")" = "$(git -C "$NUC_CLAUDE" rev-parse HEAD)" ] \
  || fail "nucleus claude: lock does not record HEAD"
[ -x "$NUC_CLAUDE/.git/hooks/pre-commit" ] \
  || fail "nucleus claude: pre-commit hook not installed"
[ -x "$NUC_CLAUDE/.git/hooks/commit-msg" ] \
  || fail "nucleus claude: commit-msg hook not installed"
[ ! -d "$NUC_CLAUDE/.cursor" ] \
  || fail "nucleus claude: touched the Cursor mirror it must leave alone"
echo "✅ nucleus --target claude test PASSED"
