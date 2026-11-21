"""Tests for the advisory user-scope sandbox check in install.py (Sprint 059 R-23, D70).

The fake home is a tmp_path; the real ~/.claude is never read or written.
"""

from __future__ import annotations

import importlib
import json
import os
import re
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
RULE = REPO / "rules" / "project_topology.md"
BASE = ["api.github.com", "github.com", "pypi.org", "files.pythonhosted.org", "registry.npmjs.org"]


@pytest.fixture()
def install(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """Import install with the user settings path redirected under tmp_path."""
    monkeypatch.syspath_prepend(str(SCRIPTS))
    sys.modules.pop("install", None)
    module = importlib.import_module("install")
    path = tmp_path / "home" / ".claude" / "settings.json"
    path.parent.mkdir(parents=True)
    monkeypatch.setattr(module, "user_settings_path", lambda: path)
    return module


def _user_file(install, data: dict | str) -> Path:
    path = install.user_settings_path()
    path.write_text(data if isinstance(data, str) else json.dumps(data))
    return path


def _net(strict: bool, domains: list[str]) -> dict:
    return {"sandbox": {"network": {"strictAllowlist": strict, "allowedDomains": domains}}}


def test_key_missing_prints_command(install, capsys) -> None:
    _user_file(install, {"sandbox": {}})
    install.advise_user_sandbox()
    out = capsys.readouterr().out
    assert "jq '.sandbox.network.strictAllowlist = true" in out
    assert "rules/project_topology.md" in out


def test_one_domain_missing_names_it(install, capsys) -> None:
    _user_file(install, _net(True, [d for d in BASE if d != "registry.npmjs.org"]))
    install.advise_user_sandbox()
    out = capsys.readouterr().out
    assert "registry.npmjs.org" in out.split("jq", 1)[0]
    assert "jq '.sandbox.network" in out


def test_complete_prints_nothing(install, capsys) -> None:
    _user_file(install, _net(True, BASE + ["extra.example"]))
    install.advise_user_sandbox()
    assert capsys.readouterr().out == ""


def test_malformed_json_warns_without_traceback(install, capsys) -> None:
    _user_file(install, "{not json")
    install.advise_user_sandbox()
    cap = capsys.readouterr()
    assert "malformed" in (cap.out + cap.err).lower()
    assert "jq '.sandbox.network" in cap.out
    assert "Traceback" not in cap.out + cap.err


def test_unhashable_allowed_domains_is_a_fault_boundary(install, capsys, monkeypatch) -> None:
    path = _user_file(install, _net(True, [{"x": 1}]))
    install.advise_user_sandbox()
    cap = capsys.readouterr()
    assert "check failed" in cap.err and str(path) in cap.err and "TypeError" in cap.err
    assert "Traceback" not in cap.out + cap.err

    class Fresh(Exception):
        pass

    def boom() -> None:
        raise Fresh("injected")

    monkeypatch.setattr(install, "_advise_user_sandbox", boom)
    install.advise_user_sandbox()
    assert "Fresh: injected" in capsys.readouterr().err


def test_missing_user_file_prints_advice(install, capsys) -> None:
    install.advise_user_sandbox()
    assert "jq '.sandbox.network" in capsys.readouterr().out


def test_file_untouched(install) -> None:
    path = _user_file(install, {"sandbox": {}})
    os.utime(path, (1_000_000, 1_000_000))
    before = (path.read_bytes(), path.stat().st_mtime_ns)
    install.advise_user_sandbox()
    assert (path.read_bytes(), path.stat().st_mtime_ns) == before
    assert sorted(p.name for p in path.parent.iterdir()) == ["settings.json"]


def test_base_list_comes_from_rule(install) -> None:
    command = re.search(r"`(cp ~/\.claude/settings\.json [^`]+)`", RULE.read_text()).group(1)
    domains = re.findall(r'"([^"]+)"', command.split("+ [", 1)[1].split("]", 1)[0])
    assert install.read_base_advice()[0] == domains == BASE
    assert install.read_base_advice()[1] == command
