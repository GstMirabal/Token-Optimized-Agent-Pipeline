"""Tests for scripts/with_env.py (Sprint 055 U02/U03)."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import with_env

SECRET = "s3cr3t-value-123"


def _fixture_root(tmp_path: Path, exe: str) -> Path:
    """Build a fake framework checkout whose allowlist names ``exe``.

    Args:
        tmp_path: Pytest temporary directory.
        exe: Absolute path used as ``argv_prefix[0]`` (join keeps it absolute).

    Returns:
        Path: The fake checkout root.
    """
    root = tmp_path / "fw"
    (root / "config").mkdir(parents=True)
    entry = {"argv_prefix": [exe, "-c"], "reason": "test"}
    (root / "config" / "with_env_allowlist.json").write_text(json.dumps({"commands": [entry]}))
    return root


def _workdir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, env_text: str | None) -> None:
    """Create a working directory, optionally with a ``.env``, and enter it.

    Args:
        tmp_path: Pytest temporary directory.
        monkeypatch: Pytest monkeypatch fixture.
        env_text: Content of ``.env``, or None for no file.
    """
    work = tmp_path / "work"
    work.mkdir()
    if env_text is not None:
        (work / ".env").write_text(env_text)
    monkeypatch.chdir(work)


def test_shipped_allowlist_contains_graphify() -> None:
    prefixes = with_env.load_allowlist(with_env.allowlist_path())
    assert ["venv_skillopt/bin/python", "-m", "graphify"] in prefixes
    assert len(prefixes) == 1


def test_non_allowlisted_command_exits_2(tmp_path, monkeypatch, capsys) -> None:
    _workdir(tmp_path, monkeypatch, "K=value1234\n")
    marker = tmp_path / "ran"
    code = with_env.main(["sh", "-c", f"touch {marker}"])
    assert code == 2
    assert not marker.exists()
    assert "is not in config/with_env_allowlist.json" in capsys.readouterr().err


def test_missing_env_exits_2(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.setattr(with_env, "FRAMEWORK_ROOT", _fixture_root(tmp_path, sys.executable))
    _workdir(tmp_path, monkeypatch, None)
    assert with_env.main([sys.executable, "-c", "print(1)"]) == 2
    assert ".env" in capsys.readouterr().err


def test_child_sees_variable_and_output_is_redacted(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.setattr(with_env, "FRAMEWORK_ROOT", _fixture_root(tmp_path, sys.executable))
    _workdir(tmp_path, monkeypatch, f'export SBX_KEY="{SECRET}"\n')
    code = with_env.main([sys.executable, "-c", "import os;print(os.environ['SBX_KEY'])"])
    out = capsys.readouterr()
    assert code == 0
    assert "***" in out.out
    assert SECRET not in out.out + out.err
    assert "SBX_KEY" not in os.environ


def test_malformed_line_warns_with_number_only(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.setattr(with_env, "FRAMEWORK_ROOT", _fixture_root(tmp_path, sys.executable))
    _workdir(tmp_path, monkeypatch, "# c\n\nLEAKME-not-a-pair\nSBX_KEY=abcd1234\n")
    code = with_env.main([sys.executable, "-c", "print('ok')"])
    err = capsys.readouterr().err
    assert code == 0
    assert "line 3" in err
    assert "LEAKME" not in err


def test_symlink_argv0_does_not_match(tmp_path, monkeypatch, capsys) -> None:
    link = tmp_path / "linked_python"
    link.symlink_to(sys.executable)
    other = tmp_path / "other_python"
    monkeypatch.setattr(with_env, "FRAMEWORK_ROOT", _fixture_root(tmp_path, str(other)))
    _workdir(tmp_path, monkeypatch, "K=value1234\n")
    assert with_env.main([str(link), "-c", "print(1)"]) == 2
    assert "not in config" in capsys.readouterr().err


def test_missing_child_exits_127(tmp_path, monkeypatch) -> None:
    ghost = str(tmp_path / "ghost")
    monkeypatch.setattr(with_env, "FRAMEWORK_ROOT", _fixture_root(tmp_path, ghost))
    _workdir(tmp_path, monkeypatch, "K=value1234\n")
    assert with_env.main([ghost, "-c", "x"]) == 127


def test_malformed_allowlist_exits_2(tmp_path, monkeypatch) -> None:
    root = tmp_path / "fw"
    (root / "config").mkdir(parents=True)
    (root / "config" / "with_env_allowlist.json").write_text("{not json")
    monkeypatch.setattr(with_env, "FRAMEWORK_ROOT", root)
    _workdir(tmp_path, monkeypatch, "K=value1234\n")
    assert with_env.main(["x"]) == 2
