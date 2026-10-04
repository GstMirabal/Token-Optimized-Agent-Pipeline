"""Tests for the root `ruff.toml` (Sprint 053 `C02`, `D6`/`D7`).

Pins the vendored-exclusion parity between `ruff.toml` `extend-exclude` and
`config/quality_audit_exclusions.json`, and the ruff version pin.

invoked_by: Makefile verify via pytest tests/.
"""

from __future__ import annotations

import json
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[1]


def _ruff_config() -> dict:
    return tomllib.loads((ROOT / "ruff.toml").read_text(encoding="utf-8"))


def test_extend_exclude_matches_quality_audit_exclusions() -> None:
    data = json.loads(
        (ROOT / "config" / "quality_audit_exclusions.json").read_text(encoding="utf-8")
    )
    expected = {entry["path"] for entry in data["exclusions"]}
    assert set(_ruff_config()["extend-exclude"]) == expected
    assert len(_ruff_config()["extend-exclude"]) == len(expected)


def test_required_version_is_pinned() -> None:
    assert _ruff_config()["required-version"] == "==0.16.3"
