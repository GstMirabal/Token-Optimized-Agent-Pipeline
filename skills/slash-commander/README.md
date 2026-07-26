# ⚡ Slash Commander: Matrix Bridge

<div align="center">
  <img src="../../../docs/assets/logo/agents_banner.svg" alt="Banner" width="100%">

  <h3 align="center">⚖️ Universal-Agents: Slash Commander</h3>

  <p align="center">
    <strong>Workflows-as-Commands Orchestration</strong>
    <br />
    Bridging the .agents Matrix with real Claude Code slash commands.
  </p>
</div>

---

## 🎯 Strategic Objective
The **Slash Commander** is the core skill that keeps every high-integrity protocol defined in `workflows/` invokable via a real, namespaced `/agents:<cmd>` slash command in the host project.

---

## 🏗️ Technical Architecture
| Layer | Namespace | Purpose |
| :--- | :--- | :--- |
| `skills/slash-commander/` | flat, no sub-layers | Documents and audits the command↔workflow bridge. |

### Component Breakdown
- **`SKILL.md`**: The procedural logic governing how `commands/*.md` map to `/agents:*` and how the link is installed/verified.
- **`scripts/verify_commands.py`**: Lint check — confirms every `commands/*.md` references a workflow file that actually exists. It does **not** generate anything; commands are hand-authored `.md` files, not generated `.ts` stubs.

---

## 🛡️ Governance Sentinel Handshake
- **Standard**: Trinity Standard (README, SKILL, /scripts/).
- **Jurisdiction**: `workflows/`, `commands/`, host `.claude/commands/agents/` (via the installer).
- **Status**: `ACTIVE`

---

## ⚖️ Federated Laws Alignment
- **Rule 113**: All operational workflows must be accessible via slash commands.
- **Rule 27**: All generated skill code must use Technical English.

---

## 🚀 Usage & Integration
Install/repair the bridge for a host project (run once after `git submodule add`, and again any time `.agents` updates):
```bash
.agents/scripts/install_claude.sh
```

Check for orphaned command→workflow references:
```bash
python3 .agents/skills/slash-commander/scripts/verify_commands.py
```
