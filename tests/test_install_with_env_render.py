"""Tests for pruning previously rendered with_env exclusions in scripts/install.py (Sprint 055 U31, D12)."""

from __future__ import annotations

import importlib
import json
import os
import sys
from pathlib import Path
from types import ModuleType

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
RENDERED = "/usr/bin/python3 -I /h/.agents/scripts/with_env.py gh_run"
HOST_ENTRY = "gh run list *"


@pytest.fixture()
def install(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> ModuleType:
    """Import install with HOST_DIR redirected to a temporary host root.

    Args:
        monkeypatch: Pytest fixture used to redirect the module attribute.
        tmp_path: Temporary directory standing in for the host root.

    Returns:
        ModuleType: The freshly imported install module.
    """
    monkeypatch.syspath_prepend(str(SCRIPTS))
    sys.modules.pop("install", None)
    module = importlib.import_module("install")
    monkeypatch.setattr(module, "HOST_DIR", tmp_path)
    return module


def _settings(host: Path, data: dict | None) -> Path:
    """Write data to the host's settings.local.json and return its path.

    Args:
        host: Host root directory.
        data: Mapping to serialise, or None to create only the parent directory.

    Returns:
        Path: Location of settings.local.json.
    """
    dest = host / ".claude" / "settings.local.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    if data is not None:
        dest.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return dest


def test_rendered_lines_removed_host_entry_kept(install: ModuleType, tmp_path: Path) -> None:
    """A rendered line is pruned and an unrelated host entry is kept."""
    dest = _settings(tmp_path, {"sandbox": {"excludedCommands": [RENDERED, HOST_ENTRY]}})
    install.prune_rendered_exclusions(tmp_path)
    data = json.loads(dest.read_text(encoding="utf-8"))
    assert data["sandbox"]["excludedCommands"] == [HOST_ENTRY]


def test_empty_list_removes_key(install: ModuleType, tmp_path: Path) -> None:
    """Pruning the last entry removes the excludedCommands key."""
    dest = _settings(tmp_path, {"sandbox": {"excludedCommands": [RENDERED]}})
    install.prune_rendered_exclusions(tmp_path)
    data = json.loads(dest.read_text(encoding="utf-8"))
    assert "excludedCommands" not in data["sandbox"]


def test_unrelated_keys_and_denies_untouched(install: ModuleType, tmp_path: Path) -> None:
    """Keys other than excludedCommands survive the prune unchanged."""
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


def test_no_file_is_not_created(install: ModuleType, tmp_path: Path) -> None:
    """A missing settings file is not created."""
    install.prune_rendered_exclusions(tmp_path)
    assert not (tmp_path / ".claude").exists()


def test_nothing_to_prune_does_not_write(install: ModuleType, tmp_path: Path) -> None:
    """With nothing to prune the file is not rewritten."""
    dest = _settings(tmp_path, {"sandbox": {"excludedCommands": [HOST_ENTRY]}})
    os.utime(dest, (1_000_000, 1_000_000))
    before = dest.read_text(encoding="utf-8")
    install.prune_rendered_exclusions(tmp_path)
    assert dest.read_text(encoding="utf-8") == before
    assert dest.stat().st_mtime == 1_000_000


def test_write_denied_exits_only_when_pruning(install: ModuleType, tmp_path: Path) -> None:
    """A refused write exits with BRIDGE_WRITE_DENIED only when pruning."""
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


SPACED = "/Users/Jane Doe/venv/bin/python3 -I /Users/Jane Doe/My Host/.agents/scripts/with_env.py gh_run"
HOST_WRITTEN = "python3 -I .agents/scripts/with_env.py gh_run"
NEAR_MISS = "echo with_env.py gh_run"


def test_spaced_interpreter_and_host_paths_are_pruned(install: ModuleType, tmp_path: Path) -> None:
    """Rendered lines with spaces in interpreter and host paths are pruned."""
    dest = _settings(tmp_path, {"sandbox": {"excludedCommands": [SPACED, HOST_ENTRY]}})
    install.prune_rendered_exclusions(tmp_path)
    data = json.loads(dest.read_text(encoding="utf-8"))
    assert data["sandbox"]["excludedCommands"] == [HOST_ENTRY]


def test_host_written_with_env_line_is_pruned_and_near_miss_kept(install: ModuleType, tmp_path: Path) -> None:
    """A host-written with_env line is pruned; a near miss is kept."""
    dest = _settings(tmp_path, {"sandbox": {"excludedCommands": [HOST_WRITTEN, NEAR_MISS]}})
    install.prune_rendered_exclusions(tmp_path)
    data = json.loads(dest.read_text(encoding="utf-8"))
    assert data["sandbox"]["excludedCommands"] == [NEAR_MISS]


def test_non_dict_root_json_is_left_untouched(install: ModuleType, tmp_path: Path) -> None:
    """A non-object JSON root returns without writing."""
    dest = _settings(tmp_path, None)
    dest.write_text("[1, 2]\n", encoding="utf-8")
    os.utime(dest, (1_000_000, 1_000_000))
    install.prune_rendered_exclusions(tmp_path)
    assert dest.read_text(encoding="utf-8") == "[1, 2]\n"
    assert dest.stat().st_mtime == 1_000_000
