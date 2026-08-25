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
