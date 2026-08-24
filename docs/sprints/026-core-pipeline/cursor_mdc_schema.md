# Cursor `.mdc` schema — Sprint 026 (`P4.0`, `P4.0b`)

**Measured:** 2026-08-24  
**Cursor version:** not read from bundle (`CFBundleShortVersionString` unavailable in this session)  
**Probe file:** `.cursor/rules/_p4_schema_probe.mdc` (written under `.cursor/rules/`, read back from disk)

## Frontmatter keys observed

| Key | Literal fragment from probe | Notes |
| :--- | :--- | :--- |
| `description` | `description: Sprint 026 P4.0 schema probe — generated for frontmatter measurement` | String; used for Agent-selected rules |
| `globs` | `globs: docs/sprints/**/*` | Comma-separated string in `.mdc`; **not** a YAML list in the probe |
| `alwaysApply` | `alwaysApply: false` | Boolean lowercase |

**Keys used by `scripts/cursor_adapter.py`:** `description`, `globs`, `alwaysApply` only — no keys beyond this table.

## Case-sensitivity probe (`P4.0b`, `Design §D6`)

Command (equivalent filesystem on this machine; temp dir substituted for `.git/` path in the plan):

```text
python3 -c "import pathlib, tempfile
with tempfile.TemporaryDirectory() as td:
    p = pathlib.Path(td) / 'AGENTS_case_probe'
    p.write_text('x')
    print(pathlib.Path(td, 'agents_case_probe').exists())"
```

**Output:** `True`

**Decision:** Do **not** create `AGENTS.md` in the nucleus root. Entry point for Cursor in this repository is `.cursor/rules/00-constitution.mdc` with `alwaysApply: true` referencing `agents.md`.
