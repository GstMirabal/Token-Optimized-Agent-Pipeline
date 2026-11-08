"""Tests for the sandbox block install_nucleus_bridge writes (Sprint 059 B-06, D12).

Every case runs against a tmp_path root; the real checkout is never touched.
"""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
BLOCK = {"enabled": True, "autoAllowBashIfSandboxed": True}


@pytest.fixture()
def install(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """Import install with AGENTS_DIR and HOST_DIR redirected to tmp_path."""
    monkeypatch.syspath_prepend(str(SCRIPTS))
    sys.modules.pop("install", None)
    module = importlib.import_module("install")
    monkeypatch.setattr(module, "AGENTS_DIR", tmp_path)
    monkeypatch.setattr(module, "HOST_DIR", tmp_path)
    (tmp_path / "commands").mkdir()
    (tmp_path / "agents").mkdir()
    return module


def _settings(root: Path) -> Path:
    return root / ".claude" / "settings.json"


def _read(root: Path) -> dict:
    return json.loads(_settings(root).read_text())


def test_block_written_with_both_keys(install, tmp_path: Path) -> None:
    assert install.install_nucleus_bridge() == 0
    assert _read(tmp_path)["sandbox"] == BLOCK


def test_no_hooks_and_no_excluded_commands(install, tmp_path: Path) -> None:
    install.install_nucleus_bridge()
    data = _read(tmp_path)
    assert "hooks" not in data
    assert "excludedCommands" not in data["sandbox"]


def test_existing_keys_preserved(install, tmp_path: Path) -> None:
    _settings(tmp_path).parent.mkdir()
    _settings(tmp_path).write_text(json.dumps(
        {"model": "x", "sandbox": {"network": {"a": 1}}, "permissions": {"deny": ["Y"]}}))
    install.install_nucleus_bridge()
    data = _read(tmp_path)
    assert data["model"] == "x"
    assert data["permissions"] == {"deny": ["Y"]}
    assert data["sandbox"] == {"network": {"a": 1}, **BLOCK}


def test_retired_entry_still_pruned(install, tmp_path: Path) -> None:
    _settings(tmp_path).parent.mkdir()
    _settings(tmp_path).write_text(json.dumps(
        {"sandbox": {"excludedCommands": ["gh pr create *", "host-own"]}}))
    install.install_nucleus_bridge()
    assert _read(tmp_path)["sandbox"]["excludedCommands"] == ["host-own"]


def test_second_run_changes_nothing(install, tmp_path: Path) -> None:
    install.install_nucleus_bridge()
    first = _settings(tmp_path).read_text()
    mtime = _settings(tmp_path).stat().st_mtime_ns
    install.install_nucleus_bridge()
    assert _settings(tmp_path).read_text() == first
    assert _settings(tmp_path).stat().st_mtime_ns == mtime


@pytest.mark.parametrize("bad", ["on", True, [1], None, 3])
def test_non_object_sandbox_fails_nonzero(install, tmp_path: Path, bad) -> None:
    _settings(tmp_path).parent.mkdir()
    original = json.dumps({"sandbox": bad})
    _settings(tmp_path).write_text(original)
    with pytest.raises(SystemExit) as exc:
        install.install_nucleus_bridge()
    assert exc.value.code not in (0, None)
    assert "not a JSON object" in str(exc.value.code)
    assert _settings(tmp_path).read_text() == original
