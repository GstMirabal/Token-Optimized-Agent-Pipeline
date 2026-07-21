#!/usr/bin/env bash
# End-to-end sandbox test for scripts/install_claude.sh (and its Python core).
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
rm -f "$WORK/host/.agents/.claude_bridge.lock"

# Pre-existing host content that must survive untouched:
mkdir -p "$WORK/host/.claude/agents"
echo "host content" > "$WORK/host/.claude/agents/principal_agent.md"
echo '{"model": "opus"}' > "$WORK/host/.claude/settings.json"
printf 'node_modules/\n*.pyc\n' > "$WORK/host/.gitignore"

cd "$WORK/host"

# --- Act ---------------------------------------------------------------------
bash .agents/scripts/install_claude.sh --profile crypto-django > /dev/null

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
[ -L .claude/agents/backend_identity_specialist.md ] || fail "profile agent not linked"
[ -L .claude/skills/polymarket-gamma-3rd ] || fail "profile skill not linked"
grep -q "crowd_intelligence_standards" CLAUDE.md || fail "profile rule import missing"

grep -qxF "node_modules/" .gitignore || fail ".gitignore: pre-existing host entry was lost"
grep -qxF "*.pyc" .gitignore || fail ".gitignore: pre-existing host entry was lost"
for entry in "/CLAUDE.md" "/.claude/agents/" "/.claude/commands/" "/.claude/skills/" \
             "/.claude/settings.local.json" "/graphify-out/"; do
  grep -qxF "$entry" .gitignore || fail ".gitignore: missing bridge entry '$entry'"
done
grep -qxF "/.claude/settings.json" .gitignore \
  && fail ".gitignore: settings.json must stay trackable, not ignored"

# Idempotency: re-run must not duplicate imports nor error out.
bash .agents/scripts/install_claude.sh --profile crypto-django > /dev/null
[ "$(grep -cxF "@.agents/agents.md" CLAUDE.md)" = "1" ] || fail "duplicate import on re-run"
[ "$(grep -cxF "/graphify-out/" .gitignore)" = "1" ] || fail "duplicate .gitignore entry on re-run"

[ -f .agents/.claude_bridge.lock ] || fail "bridge lock not created"
[ -s .agents/.claude_bridge.lock ] || fail "bridge lock is empty (must record the submodule commit)"

echo "✅ installer sandbox test PASSED"

# ── Nucleus mode: a real .git directory must produce the minimal self-bridge ──
NUCLEUS="$WORK/nucleus"
mkdir -p "$NUCLEUS"
rsync -a --exclude='.git' --exclude='node_modules' --exclude='venv_skillopt' \
      --exclude='graphify-out' --exclude='.claude' "$AGENTS_SRC/" "$NUCLEUS/"
mkdir -p "$NUCLEUS/.git"   # real dir -> nucleus detection
rm -f "$NUCLEUS/.claude_bridge.lock" "$NUCLEUS/CLAUDE.md"
( cd "$NUCLEUS" && python3 scripts/install_claude.py > /dev/null )
[ -e "$NUCLEUS/.claude/commands/agents/start.md" ] || fail "nucleus: /agents:start not linked"
[ -e "$NUCLEUS/.claude/agents/principal_agent.md" ] || fail "nucleus: agents not linked"
grep -qx "@agents.md" "$NUCLEUS/CLAUDE.md" || fail "nucleus: constitution import missing"
[ ! -e "$NUCLEUS/.claude/skills" ] || fail "nucleus: skills must NOT be linked (minimal bridge)"
( cd "$NUCLEUS" && python3 scripts/install_claude.py --profile crypto-django > /dev/null 2>&1 ) \
  && fail "nucleus: profile install must be refused" || true
echo "✅ nucleus self-bridge test PASSED"
