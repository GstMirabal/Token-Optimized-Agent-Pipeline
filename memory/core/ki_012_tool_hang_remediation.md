# KI-012: Remediation for Agent Tool Hangs during File I/O

- **ID:** KI-012
- **Title:** Remediation for Agent Tool Hangs during File I/O
- **Context:** Occurred during initialization of project-specific records (task.md) in high-latency or locked environments.
- **Blockage:** Standard `write_to_file` and `replace_file_content` tools may hang or be canceled by the human due to 20s+ latency in specific IDE/Filesystem integrations.

## 🛠️ The Solution (Rule 41.1)

1.  **Atomic CLI fallback**: Use terminal-based Here-Docs (`cat << 'EOF' > file`) for rapid, non-blocking file creation.
2.  **Diagnostic Echo**: Verify filesystem access with `echo "test" > check.txt` before massive write operations.
3.  **Governance Shielding**: If the tool fails twice, the agent MUST immediately pivot to native terminal commands (printf/cat) to maintain operational continuity.

---
> [!IMPORTANT]
> **Rule Update:** This lesson catalyzed the creation of [Rule 41.1](file:///Users/gstmirabal/Developer/.agents/governance/constitution/global_user_rules.md) regarding session state cache and CLI-first diagnostics.
