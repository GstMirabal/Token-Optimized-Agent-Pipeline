# ⚡ Slash Commander: Matrix Bridge

<div align="center">
  <img src="../../../docs/assets/logo/institutional_banner.png" alt="Banner" width="100%">

  <h3 align="center">⚖️ Universal-Agents: Slash Commander</h3>

  <p align="center">
    <strong>Workflows-as-Commands Orchestration</strong>
    <br />
    Bridging the .agents Matrix with the Claude Code Skill Ecosystem.
  </p>
</div>

---

## 🎯 Strategic Objective
The **Slash Commander** is a specialized core skill that synchronizes Markdown-based workflows with the native Slash Command system of the AI client. It ensures that every high-integrity protocol defined in `workflows/` is invokable via standard `/cmd` syntax.

---

## 🏗️ Technical Architecture
| Layer | Namespace | Purpose |
| :--- | :--- | :--- |
| **`core/`** | `slash-commander` | Strategic bridge for command registration. |

### Component Breakdown
- **`SKILL.md`**: The procedural logic governing the translation of workflows to `.ts` skills.
- **`scripts/generate_commands.py`**: The engine responsible for parsing workflows and generating the shadow skill infrastructure.

---

## 🛡️ Governance Sentinel Handshake
- **Standard**: Trinity Standard (README, SKILL, /scripts/).
- **Jurisdiction**: `workflows/`, `.claude.code/skills/`.
- **Status**: `DEVELOPMENT_PHASE`

---

## ⚖️ Federated Laws Alignment
- **Rule 113**: All operational workflows must be accessible via slash commands.
- **Rule 27**: All generated skill code must use Technical English.

---

## 🚀 Usage & Integration
Trigger the synchronization using the following command (orchestrated by the **DevOps Sentinel**):
```bash
python3 skills/core/slash-commander/scripts/generate_commands.py --sync
```

---

## 📬 Contact
**Architect**: Gst Mirabal - [gst.mirabal@gmail.com](mailto:gst.mirabal@gmail.com)
**Project**: Universal-Agents Matrix
