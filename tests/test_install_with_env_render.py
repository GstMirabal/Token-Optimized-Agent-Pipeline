"""Tests for pruning previously rendered with_env exclusions in scripts/install.py (Sprint 055 U31, D12)."""

from __future__ import annotations

import importlib
import json
import os
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
RENDERED = "/usr/bin/python3 -I /h/.agents/scripts/with_env.py gh_run"
HOST_ENTRY = "gh run list *"


@pytest.fixture()
def install(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """Import install with HOST_DIR redirected to a temporary host root."""
    monkeypatch.syspath_prepend(str(SCRIPTS))
    sys.modules.pop("install", None)
    module = importlib.import_module("install")
    monkeypatch.setattr(module, "HOST_DIR", tmp_path)
    return module


def _settings(host: Path, data: dict | None) -> Path:
    """Write data to the host's settings.local.json and return its path."""
    dest = host / ".claude" / "settings.local.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    if data is not None:
        dest.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return dest


def test_rendered_lines_removed_host_entry_kept(install, tmp_path: Path) -> None:
    dest = _settings(tmp_path, {"sandbox": {"excludedCommands": [RENDERED, HOST_ENTRY]}})
    install.prune_rendered_exclusions(tmp_path)
    data = json.loads(dest.read_text(encoding="utf-8"))
    assert data["sandbox"]["excludedCommands"] == [HOST_ENTRY]


def test_empty_list_removes_key(install, tmp_path: Path) -> None:
    dest = _settings(tmp_path, {"sandbox": {"excludedCommands": [RENDERED]}})
    install.prune_rendered_exclusions(tmp_path)
    data = json.loads(dest.read_text(encoding="utf-8"))
    assert "excludedCommands" not in data["sandbox"]


def test_unrelated_keys_and_denies_untouched(install, tmp_path: Path) -> None:
    other = {
        "sandbox": {"excludedCommands": [RENDERED], "filesystem": {"denyWrite": ["/h/.agents/scripts"]}},
        "permissions": {"deny": ["Edit(//h/.agents/scripts/**)"]},
        "model": "x",
    }
    dest = _settings(tmp_path, json.loads(json.dumps(other)))
    install.prune_rendered_exclusions(tmp_path)
    data = json.loads(dest.read_text(encoding="utf-8"))
    del other["sandbox"]["excludedCommands"]
    assert data == other


def test_no_file_is_not_created(install, tmp_path: Path) -> None:
    install.prune_rendered_exclusions(tmp_path)
    assert not (tmp_path / ".claude").exists()


def test_nothing_to_prune_does_not_write(install, tmp_path: Path) -> None:
    dest = _settings(tmp_path, {"sandbox": {"excludedCommands": [HOST_ENTRY]}})
    os.utime(dest, (1_000_000, 1_000_000))
    before = dest.read_text(encoding="utf-8")
    install.prune_rendered_exclusions(tmp_path)
    assert dest.read_text(encoding="utf-8") == before
    assert dest.stat().st_mtime == 1_000_000


def test_write_denied_exits_only_when_pruning(install, tmp_path: Path) -> None:
    dest = _settings(tmp_path, {"sandbox": {"excludedCommands": [RENDERED]}})
    dest.chmod(0o444)
    if os.access(dest, os.W_OK):
        pytest.skip("running with privileges that ignore file modes")
    try:
        with pytest.raises(SystemExit) as exc:
            install.prune_rendered_exclusions(tmp_path)
        assert exc.value.code == install.BRIDGE_WRITE_DENIED
    finally:
        dest.chmod(0o644)
    dest.write_text(json.dumps({"sandbox": {"excludedCommands": [HOST_ENTRY]}}), encoding="utf-8")
    dest.chmod(0o444)
    try:
        install.prune_rendered_exclusions(tmp_path)
    finally:
        dest.chmod(0o644)
