"""Tests for scripts/sync_agents_pin.py (Sprint 034 Track P)."""

from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"


def _done(code: int, stdout: str = "", stderr: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(
        args=["git"], returncode=code, stdout=stdout, stderr=stderr
    )


@pytest.fixture()
def pin_mod(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.syspath_prepend(str(SCRIPTS))
    sys.modules.pop("sync_agents_pin", None)
    mod = importlib.import_module("sync_agents_pin")
    monkeypatch.setattr(mod, "is_nucleus", lambda: False)
    monkeypatch.setattr(mod, "agents_root", lambda: tmp_path)
    (tmp_path / ".git").mkdir()
    return mod


def test_parse_version_orders_tags(pin_mod) -> None:
    assert pin_mod.parse_version("v4.16.0") < pin_mod.parse_version("v4.17.0")
    assert pin_mod.parse_version("v9.9.9") < pin_mod.parse_version("v10.0.0")
    assert pin_mod.parse_version("v4.16.0") == pin_mod.parse_version("4.16.0")


def test_is_version_tag(pin_mod) -> None:
    assert pin_mod.is_version_tag("v4.16.0") is True
    assert pin_mod.is_version_tag("nightly") is False
    assert pin_mod.is_version_tag("v") is False


def test_nucleus_skips(pin_mod, monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    monkeypatch.setattr(pin_mod, "is_nucleus", lambda: True)
    assert pin_mod.main() == 0
    assert "nucleus" in capsys.readouterr().out


def test_no_remote_keeps_pin(pin_mod, monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    monkeypatch.setattr(pin_mod, "git", lambda *a, **k: _done(0, ""))
    assert pin_mod.main() == 0
    assert "no git remote" in capsys.readouterr().out


def test_ping_timeout_degrades(pin_mod, tmp_path: Path, capsys) -> None:
    def fake_git(args: list[str], cwd: Path | None, timeout: int | None = None):
        if args[:1] == ["remote"]:
            return _done(0, "origin\n")
        if args[:2] == ["fetch", "--tags"]:
            raise subprocess.TimeoutExpired(cmd=["git"], timeout=timeout or 0)
        return _done(0, "")

    pin_mod.git = fake_git
    assert pin_mod.ping_fetch_tags(tmp_path, "origin") is False
    assert "timed out" in capsys.readouterr().out


def test_ping_nonzero_degrades(pin_mod, tmp_path: Path, capsys) -> None:
    def fake_git(args: list[str], cwd: Path | None, timeout: int | None = None):
        if args[:2] == ["fetch", "--tags"]:
            return _done(1, "", "could not resolve host")
        return _done(0, "")

    pin_mod.git = fake_git
    assert pin_mod.ping_fetch_tags(tmp_path, "origin") is False
    assert "ping failed" in capsys.readouterr().out


def test_already_current_exits_0(pin_mod, monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    def fake_git(args: list[str], cwd: Path | None, timeout: int | None = None):
        if args[:1] == ["remote"]:
            return _done(0, "origin\n")
        if args[:2] == ["fetch", "--tags"]:
            return _done(0)
        if args[:2] == ["tag", "--sort=-v:refname"]:
            return _done(0, "v4.16.0\nv4.15.0\n")
        if args[:3] == ["describe", "--tags", "--abbrev=0"]:
            return _done(0, "v4.16.0\n")
        return _done(0, "")

    monkeypatch.setattr(pin_mod, "git", fake_git)
    assert pin_mod.main() == 0
    assert "pin current (v4.16.0)" in capsys.readouterr().out


def test_bump_checks_out_newer_tag(
    pin_mod, monkeypatch: pytest.MonkeyPatch, capsys
) -> None:
    calls: list[list[str]] = []

    def fake_git(args: list[str], cwd: Path | None, timeout: int | None = None):
        calls.append(args)
        if args[:1] == ["remote"]:
            return _done(0, "upstream\n")
        if args[:2] == ["fetch", "--tags"]:
            return _done(0)
        if args[:2] == ["tag", "--sort=-v:refname"]:
            return _done(0, "v4.17.0\nv4.16.0\n")
        if args[:3] == ["describe", "--tags", "--abbrev=0"]:
            return _done(0, "v4.16.0\n")
        if args[:2] == ["status", "--porcelain"]:
            return _done(0, "")
        if args[:2] == ["checkout", "--detach"]:
            return _done(0)
        return _done(0, "")

    monkeypatch.setattr(pin_mod, "git", fake_git)
    assert pin_mod.main() == 0
    out = capsys.readouterr().out
    assert "bumped v4.16.0 -> v4.17.0" in out
    assert ["checkout", "--detach", "v4.17.0"] in calls
    assert ["fetch", "--tags", "upstream"] in calls


def test_dirty_while_behind_exits_2(
    pin_mod, monkeypatch: pytest.MonkeyPatch, capsys
) -> None:
    def fake_git(args: list[str], cwd: Path | None, timeout: int | None = None):
        if args[:1] == ["remote"]:
            return _done(0, "origin\n")
        if args[:2] == ["fetch", "--tags"]:
            return _done(0)
        if args[:2] == ["tag", "--sort=-v:refname"]:
            return _done(0, "v4.17.0\n")
        if args[:3] == ["describe", "--tags", "--abbrev=0"]:
            return _done(0, "v4.16.0\n")
        if args[:2] == ["status", "--porcelain"]:
            return _done(0, " M agents.md\n")
        if args[:2] == ["checkout", "--detach"]:
            raise AssertionError("must not checkout over a dirty tree")
        return _done(0, "")

    monkeypatch.setattr(pin_mod, "git", fake_git)
    assert pin_mod.main() == 2
    assert "dirty" in capsys.readouterr().err


def test_checkout_failure_exits_2(
    pin_mod, monkeypatch: pytest.MonkeyPatch, capsys
) -> None:
    def fake_git(args: list[str], cwd: Path | None, timeout: int | None = None):
        if args[:1] == ["remote"]:
            return _done(0, "origin\n")
        if args[:2] == ["fetch", "--tags"]:
            return _done(0)
        if args[:2] == ["tag", "--sort=-v:refname"]:
            return _done(0, "v4.17.0\n")
        if args[:3] == ["describe", "--tags", "--abbrev=0"]:
            return _done(1, "")
        if args[:2] == ["status", "--porcelain"]:
            return _done(0, "")
        if args[:2] == ["checkout", "--detach"]:
            return _done(1, "", "pathspec unknown")
        return _done(0, "")

    monkeypatch.setattr(pin_mod, "git", fake_git)
    assert pin_mod.main() == 2
    assert "checkout" in capsys.readouterr().out


def test_no_version_tags_keeps_pin(
    pin_mod, monkeypatch: pytest.MonkeyPatch, capsys
) -> None:
    def fake_git(args: list[str], cwd: Path | None, timeout: int | None = None):
        if args[:1] == ["remote"]:
            return _done(0, "origin\n")
        if args[:2] == ["fetch", "--tags"]:
            return _done(0)
        if args[:2] == ["tag", "--sort=-v:refname"]:
            return _done(0, "nightly\n")
        return _done(0, "")

    monkeypatch.setattr(pin_mod, "git", fake_git)
    assert pin_mod.main() == 0
    assert "no version tags" in capsys.readouterr().out


def test_init_when_git_missing(
    pin_mod, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys
) -> None:
    (tmp_path / ".git").rmdir()
    inits: list[Path] = []

    def fake_init(host: Path) -> bool:
        inits.append(host)
        (tmp_path / ".git").mkdir()
        return True

    def fake_git(args: list[str], cwd: Path | None, timeout: int | None = None):
        if args[:1] == ["remote"]:
            return _done(0, "origin\n")
        if args[:2] == ["fetch", "--tags"]:
            return _done(0)
        if args[:2] == ["tag", "--sort=-v:refname"]:
            return _done(0, "v4.16.0\n")
        if args[:3] == ["describe", "--tags", "--abbrev=0"]:
            return _done(0, "v4.16.0\n")
        return _done(0, "")

    monkeypatch.setattr(pin_mod, "init_submodule", fake_init)
    monkeypatch.setattr(pin_mod, "git", fake_git)
    assert pin_mod.main() == 0
    assert inits == [tmp_path.parent]
    assert "not initialized" in capsys.readouterr().out


def test_init_failure_exits_2(pin_mod, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    (tmp_path / ".git").rmdir()
    monkeypatch.setattr(pin_mod, "init_submodule", lambda host: False)
    assert pin_mod.main() == 2


def test_init_submodule_reports_git_error(
    pin_mod, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys
) -> None:
    monkeypatch.setattr(
        pin_mod, "git", lambda *a, **k: _done(1, "", "no submodule mapping")
    )
    assert pin_mod.init_submodule(tmp_path) is False
    assert "submodule init failed" in capsys.readouterr().out


def test_porcelain_ignores_git_failure(pin_mod, tmp_path: Path) -> None:
    pin_mod.git = lambda *a, **k: _done(1, " M x\n")
    assert pin_mod.porcelain(tmp_path) == []


def test_remote_name_prefers_origin(pin_mod, tmp_path: Path) -> None:
    pin_mod.git = lambda *a, **k: _done(0, "upstream\norigin\n")
    assert pin_mod.remote_name(tmp_path) == "origin"


def test_checkout_tag_success(pin_mod, tmp_path: Path) -> None:
    pin_mod.git = lambda *a, **k: _done(0)
    assert pin_mod.checkout_tag(tmp_path, "v4.17.0") is True


def test_git_wrapper_runs(pin_mod, tmp_path: Path) -> None:
    result = pin_mod.git(["--version"], cwd=tmp_path)
    assert result.returncode == 0
    assert "git" in result.stdout.lower()


def test_current_tag_none_on_failure(pin_mod, tmp_path: Path) -> None:
    pin_mod.git = lambda *a, **k: _done(1, "")
    assert pin_mod.current_tag(tmp_path) is None
