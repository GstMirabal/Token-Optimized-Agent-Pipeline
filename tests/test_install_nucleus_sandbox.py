"""Tests for the sandbox block install_nucleus_bridge writes (Sprint 059 B-06, D12).

Every case runs against a tmp_path root; the real checkout is never touched.
"""

from __future__ import annotations

import importlib
import json
import shutil
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
BLOCK = {"enabled": True, "autoAllowBashIfSandboxed": True}
TEMPLATE = json.loads((REPO / "claude" / "settings.hooks.json").read_text())
PIP_ENV = {"PIP_USE_DEPRECATED": "legacy-certs", "PIP_CERT": "/etc/ssl/cert.pem"}
HOST_ONLY = {"./.agents", "./.git/modules/.agents"}


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
    (tmp_path / "claude").mkdir()
    shutil.copy(REPO / "claude" / "settings.hooks.json", tmp_path / "claude" / "settings.hooks.json")
    monkeypatch.setattr(module.sys, "platform", "linux")
    return module


def _settings(root: Path) -> Path:
    return root / ".claude" / "settings.json"


def _read(root: Path) -> dict:
    return json.loads(_settings(root).read_text())


def test_block_written_with_both_keys(install, tmp_path: Path) -> None:
    assert install.install_nucleus_bridge() == 0
    sandbox = _read(tmp_path)["sandbox"]
    assert {k: sandbox[k] for k in BLOCK} == BLOCK


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
    assert data["permissions"]["deny"][0] == "Y"
    assert set(TEMPLATE["permissions"]["deny"]) <= set(data["permissions"]["deny"])
    assert data["sandbox"]["network"]["a"] == 1
    assert data["sandbox"]["network"]["allowedDomains"] == TEMPLATE["sandbox"]["network"]["allowedDomains"]
    assert {k: data["sandbox"][k] for k in BLOCK} == BLOCK


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


def _is_subset(part, whole) -> bool:
    """Return True when every key and list item of part is present in whole."""
    if isinstance(part, dict):
        return isinstance(whole, dict) and all(
            k in whole and _is_subset(v, whole[k]) for k, v in part.items())
    if isinstance(part, list):
        return isinstance(whole, list) and all(i in whole for i in part)
    return part == whole


def test_nucleus_merge_holds_template_sandbox_and_permissions(install, tmp_path: Path) -> None:
    install.install_nucleus_bridge()
    data = _read(tmp_path)
    expected = json.loads(json.dumps({k: TEMPLATE[k] for k in ("sandbox", "permissions")}))
    expected["sandbox"]["filesystem"]["denyWrite"] = [
        e for e in expected["sandbox"]["filesystem"]["denyWrite"] if e not in HOST_ONLY]
    assert _is_subset(expected, data)
    assert set(TEMPLATE["sandbox"]) <= set(data["sandbox"])
    assert set(TEMPLATE["permissions"]) <= set(data["permissions"])


def test_nucleus_deny_write_has_nucleus_paths_and_no_host_paths(install, tmp_path: Path) -> None:
    install.install_nucleus_bridge()
    deny_write = _read(tmp_path)["sandbox"]["filesystem"]["denyWrite"]
    assert "./agents" in deny_write
    assert "./venv_skillopt" in deny_write
    assert not HOST_ONLY & set(deny_write)


def test_nucleus_never_gets_template_hooks(install, tmp_path: Path) -> None:
    install.install_nucleus_bridge()
    assert "hooks" not in _read(tmp_path)


def test_nucleus_env_on_darwin(install, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(install.sys, "platform", "darwin")
    install.install_nucleus_bridge()
    assert _read(tmp_path)["env"] == PIP_ENV


def test_nucleus_no_env_on_linux(install, tmp_path: Path) -> None:
    install.install_nucleus_bridge()
    assert "env" not in _read(tmp_path)


def test_nucleus_env_existing_value_kept(
        install, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(install.sys, "platform", "darwin")
    _settings(tmp_path).parent.mkdir()
    _settings(tmp_path).write_text(json.dumps({"env": {"PIP_CERT": "/own.pem", "X": "1"}}))
    install.install_nucleus_bridge()
    assert _read(tmp_path)["env"] == {
        "PIP_CERT": "/own.pem", "X": "1", "PIP_USE_DEPRECATED": "legacy-certs"}


def test_nucleus_second_run_identical_on_darwin(
        install, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(install.sys, "platform", "darwin")
    install.install_nucleus_bridge()
    first = _settings(tmp_path).read_text()
    install.install_nucleus_bridge()
    assert _settings(tmp_path).read_text() == first


def _host_install(install, tmp_path: Path) -> Path:
    dest = tmp_path / "host" / ".claude" / "settings.json"
    install.merge_into(tmp_path / "claude" / "settings.hooks.json", dest)
    install.merge_platform_env(dest)
    return dest


def test_host_env_on_darwin(install, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(install.sys, "platform", "darwin")
    dest = _host_install(install, tmp_path)
    assert json.loads(dest.read_text())["env"] == PIP_ENV


def test_host_no_env_on_linux(install, tmp_path: Path) -> None:
    dest = _host_install(install, tmp_path)
    assert "env" not in json.loads(dest.read_text())


def test_host_env_existing_value_kept_and_idempotent(
        install, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(install.sys, "platform", "darwin")
    dest = tmp_path / "host" / ".claude" / "settings.json"
    dest.parent.mkdir(parents=True)
    dest.write_text(json.dumps({"env": {"PIP_USE_DEPRECATED": "mine"}}))
    install.merge_platform_env(dest)
    first = dest.read_text()
    install.merge_platform_env(dest)
    assert dest.read_text() == first
    assert json.loads(first)["env"] == {"PIP_USE_DEPRECATED": "mine", "PIP_CERT": "/etc/ssl/cert.pem"}


def test_host_merge_keeps_host_denywrite_paths(install, tmp_path: Path) -> None:
    dest = _host_install(install, tmp_path)
    deny_write = json.loads(dest.read_text())["sandbox"]["filesystem"]["denyWrite"]
    assert HOST_ONLY <= set(deny_write)
    assert "./agents" not in deny_write
