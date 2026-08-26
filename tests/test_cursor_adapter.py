"""Tests for scripts/cursor_adapter.py — .mdc frontmatter contract (A3.1)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import cursor_adapter  # noqa: E402


def test_mdc_rule_frontmatter_keys_match_measured_contract() -> None:
    """Absorbed P4.0 contract: only these three keys leave the generator."""
    assert cursor_adapter.MDC_RULE_FRONTMATTER_KEYS == (
        "description",
        "globs",
        "alwaysApply",
    )


def test_write_rules_emits_only_contract_keys(tmp_path: Path) -> None:
    """Generated rule .mdc frontmatter must not invent keys beyond the contract."""
    # Avoid a directory named ``.cursor``: some sandboxes block creating it.
    bridge = tmp_path / "bridge"
    cursor_adapter._write_rules(bridge)
    sample = next(p for p in (bridge / "rules").glob("*.mdc"))
    text = sample.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    front = text.split("---", 2)[1]
    keys = tuple(
        line.split(":", 1)[0].strip()
        for line in front.strip().splitlines()
        if line.strip() and ":" in line
    )
    assert keys == cursor_adapter.MDC_RULE_FRONTMATTER_KEYS


def _frontmatter_keys(text: str) -> tuple[str, ...]:
    front = text.split("---", 2)[1]
    return tuple(
        line.split(":", 1)[0].strip()
        for line in front.strip().splitlines()
        if line.strip() and ":" in line
    )


def test_chat_title_rule_is_always_apply(tmp_path: Path) -> None:
    bridge = tmp_path / "bridge"
    cursor_adapter._write_chat_title_rule(bridge)
    path = bridge / "rules" / cursor_adapter.CHAT_TITLE_RULE
    text = path.read_text(encoding="utf-8")
    assert "alwaysApply: true" in text
    assert "rename_chat" in text
    assert "Chat initialization" in text


def test_write_agents_emits_cursor_contract(tmp_path: Path) -> None:
    bridge = tmp_path / "bridge"
    cursor_adapter._write_agents(bridge)
    dest = bridge / "agents"
    sources = list((cursor_adapter.AGENTS_DIR / "agents").glob("*.md"))
    written = list(dest.glob("*.md"))
    assert len(written) == len(sources)
    qa = (dest / "qa-agent.md").read_text(encoding="utf-8")
    assert _frontmatter_keys(qa) == cursor_adapter.CURSOR_AGENT_FRONTMATTER_KEYS
    assert "tools:" not in qa.split("---", 2)[1]
    assert "tier:" not in qa.split("---", 2)[1]
    assert "readonly: true" in qa
    assert "model: inherit" in qa
    implementer = (dest / "implementer-agent.md").read_text(encoding="utf-8")
    assert "readonly: false" in implementer
    assert (dest / "implementer-agent.md").is_file()
