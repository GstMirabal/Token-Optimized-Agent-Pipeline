"""Tests for the per-machine absolute with_env exclusion render in scripts/install.py (Sprint 055 U23)."""

from __future__ import annotations

import importlib
import json
import os
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
PYTHON = "/usr/bin/python3"


@pytest.fixture()
def install(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """Import install with HOST_DIR redirected to a temporary host root."""
    monkeypatch.syspath_prepend(str(SCRIPTS))
    sys.modules.pop("install", None)
    module = importlib.import_module("install")
    monkeypatch.setattr(module, "HOST_DIR", tmp_path)
    return module


@pytest.fixture()
def dirs(tmp_path: Path) -> tuple[Path, Path]:
    """Build a host dir and a fake agents dir whose allowlist holds two names."""
    host = tmp_path / "host"
    agents = tmp_path / "host" / ".agents"
    (agents / "config").mkdir(parents=True)
    allowlist = {
        "commands": {
            "zeta": {"argv": ["scripts/zeta.py"]},
            "alpha": {"argv": ["scripts/alpha.py"]},
        }
    }
    (agents / "config" / "with_env_allowlist.json").write_text(json.dumps(allowlist), encoding="utf-8")
    return host, agents


def _read(host: Path) -> dict:
    return json.loads((host / ".claude" / "settings.local.json").read_text(encoding="utf-8"))


def _protected(agents: Path) -> list[str]:
    return [str(agents / s) for s in ("scripts", "config", "venv_skillopt")]


def test_one_absolute_line_per_name_sorted(install, dirs) -> None:
    host, agents = dirs
    install.render_with_env_exclusions(host, agents, PYTHON)
    wrapper = agents / "scripts" / "with_env.py"
    assert _read(host)["sandbox"]["excludedCommands"] == [
        f"{PYTHON} -I {wrapper} alpha",
        f"{PYTHON} -I {wrapper} zeta",
    ]


def test_denies_hold_three_absolute_paths(install, dirs) -> None:
    host, agents = dirs
    install.render_with_env_exclusions(host, agents, PYTHON)
    data = _read(host)
    paths = _protected(agents)
    assert data["sandbox"]["filesystem"]["denyWrite"] == paths
    assert data["permissions"]["deny"] == [f"Edit(/{p}/**)" for p in paths]
    assert all(e.startswith("Edit(//") for e in data["permissions"]["deny"])


def test_idempotent(install, dirs) -> None:
    host, agents = dirs
    install.render_with_env_exclusions(host, agents, PYTHON)
    first = _read(host)
    install.render_with_env_exclusions(host, agents, PYTHON)
    assert _read(host) == first


def test_stale_lines_replaced_host_entries_survive(install, dirs) -> None:
    host, agents = dirs
    dest = host / ".claude" / "settings.local.json"
    dest.parent.mkdir(parents=True)
    dest.write_text(json.dumps({
        "model": "keep",
        "sandbox": {
            "excludedCommands": [
                "gh run list *",
                "/old/python3 -I /old/checkout/scripts/with_env.py alpha",
            ],
            "filesystem": {"denyWrite": ["/unrelated"]},
        },
        "permissions": {"deny": ["Read(.env)"]},
    }), encoding="utf-8")
    install.render_with_env_exclusions(host, agents, PYTHON)
    data = _read(host)
    excluded = data["sandbox"]["excludedCommands"]
    assert excluded[0] == "gh run list *"
    assert not any("/old/" in e for e in excluded)
    assert len(excluded) == 3
    assert "/unrelated" in data["sandbox"]["filesystem"]["denyWrite"]
    assert "Read(.env)" in data["permissions"]["deny"]
    assert data["model"] == "keep"


def test_no_python_warns_and_writes_nothing(install, dirs, capsys) -> None:
    host, agents = dirs
    install.render_with_env_exclusions(host, agents, None)
    assert not (host / ".claude" / "settings.local.json").exists()
    err = capsys.readouterr().err
    assert "python3" in err
    assert "human" in err


@pytest.mark.skipif(
    hasattr(os, "geteuid") and os.geteuid() == 0,
    reason="root bypasses file permission bits",
)
def test_write_denied_exits_bridge_code_without_traceback(install, dirs, capsys) -> None:
    host, agents = dirs
    dest = host / ".claude" / "settings.local.json"
    dest.parent.mkdir(parents=True)
    dest.write_text("{}\n", encoding="utf-8")
    dest.chmod(0o444)
    with pytest.raises(SystemExit) as excinfo:
        install.render_with_env_exclusions(host, agents, PYTHON)
    assert excinfo.value.code == install.BRIDGE_WRITE_DENIED
    assert "Traceback" not in capsys.readouterr().err
