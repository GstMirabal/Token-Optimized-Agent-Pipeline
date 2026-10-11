"""Tests for scripts/with_env.py (Sprint 055 U02/U03, remediation of QA round 1)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import with_env

SECRET = "s3cr3t-value-123"
SHIPPED_NAMES = {"graphify-extract", "graphify-extract-deep", "graphify-label"}


def _fixture_root(tmp_path: Path, argv: list[str]) -> Path:
    """Build a fake framework checkout whose allowlist has one command ``run``.

    Args:
        tmp_path: Pytest temporary directory.
        argv: Full argv of the entry; ``argv[0]`` may be absolute.

    Returns:
        Path: The fake checkout root.
    """
    root = tmp_path / "fw"
    (root / "config").mkdir(parents=True)
    entry = {"argv": argv, "reason": "test"}
    (root / "config" / "with_env_allowlist.json").write_text(
        json.dumps({"commands": {"run": entry}})
    )
    return root


def _setup(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    argv: list[str] | None,
    env_text: str | None,
    isolated: bool = True,
) -> Path:
    """Install a fixture checkout, a working directory and the isolation flag.

    Args:
        tmp_path: Pytest temporary directory.
        monkeypatch: Pytest monkeypatch fixture.
        argv: Allowlist argv for command ``run``, or None to skip the checkout.
        env_text: Content of ``.env``, or None for no file.
        isolated: Value the isolation check reports.

    Returns:
        Path: The working directory (already the cwd).
    """
    if argv is not None:
        monkeypatch.setattr(with_env, "FRAMEWORK_ROOT", _fixture_root(tmp_path, argv))
    monkeypatch.setattr(with_env, "_isolated", lambda: isolated, raising=False)
    work = tmp_path / "work"
    work.mkdir()
    if env_text is not None:
        (work / ".env").write_text(env_text)
    monkeypatch.chdir(work)
    return work


def test_shipped_allowlist_has_exactly_the_three_names() -> None:
    commands = with_env.load_allowlist(with_env.allowlist_path())
    assert set(commands) == SHIPPED_NAMES
    for argv in commands.values():
        assert argv[:3] == ["venv_skillopt/bin/python", "-I", "-m"]


def test_not_isolated_exits_2_before_reading_env(tmp_path, monkeypatch, capsys) -> None:
    _setup(tmp_path, monkeypatch, [sys.executable, "-c", "print(1)"], "K=value1234\n", isolated=False)
    assert with_env.main(["run"]) == 2
    assert "run as 'python3 -I" in capsys.readouterr().err


def test_unknown_name_exits_2(tmp_path, monkeypatch, capsys) -> None:
    work = _setup(tmp_path, monkeypatch, [sys.executable, "-c", "print(1)"], "K=value1234\n")
    assert with_env.main(["nope"]) == 2
    assert "config/with_env_allowlist.json" in capsys.readouterr().err
    assert not (work / "ran").exists()


def test_extra_arguments_exit_2_and_child_never_runs(tmp_path, monkeypatch) -> None:
    marker = tmp_path / "ran"
    argv = [sys.executable, "-c", f"open({str(marker)!r}, 'w')"]
    _setup(tmp_path, monkeypatch, argv, "K=value1234\n")
    assert with_env.main(["run", "extra"]) == 2
    assert with_env.main([]) == 2
    assert not marker.exists()


def test_cwd_package_cannot_shadow_graphify_under_isolated_mode(tmp_path, monkeypatch, capsys) -> None:
    argv = [sys.executable, "-I", "-m", "graphify"]
    work = _setup(tmp_path, monkeypatch, argv, "K=value1234\n")
    pkg = work / "graphify"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("")
    (pkg / "__main__.py").write_text("print('SHADOW-RAN')\n")
    with_env.main(["run"])
    out = capsys.readouterr()
    assert "SHADOW-RAN" not in out.out + out.err
    plain = subprocess.run(
        [sys.executable, "-m", "graphify"], capture_output=True, text=True, check=False
    )
    assert "SHADOW-RAN" in plain.stdout


def test_python_variables_are_stripped_from_child_env(tmp_path, monkeypatch, capsys) -> None:
    code_text = "import os;print(sorted(k for k in os.environ if k.startswith('PYTHON')))"
    _setup(tmp_path, monkeypatch, [sys.executable, "-c", code_text], "K=value1234\n")
    monkeypatch.setenv("PYTHONPATH", "/nonexistent-shadow")
    monkeypatch.setenv("PYTHONSTARTUP", "/nonexistent-startup")
    assert with_env.main(["run"]) == 0
    assert capsys.readouterr().out.strip() == "[]"


def test_missing_env_exits_2(tmp_path, monkeypatch, capsys) -> None:
    _setup(tmp_path, monkeypatch, [sys.executable, "-c", "print(1)"], None)
    assert with_env.main(["run"]) == 2
    assert ".env" in capsys.readouterr().err


def test_child_sees_variable_and_output_is_redacted(tmp_path, monkeypatch, capsys) -> None:
    code_text = "import os;print(os.environ['SBX_KEY'])"
    _setup(tmp_path, monkeypatch, [sys.executable, "-c", code_text], f'export SBX_KEY="{SECRET}"\n')
    code = with_env.main(["run"])
    out = capsys.readouterr()
    assert code == 0
    assert "***" in out.out
    assert SECRET not in out.out + out.err
    assert "SBX_KEY" not in os.environ


def test_malformed_line_warns_with_number_only(tmp_path, monkeypatch, capsys) -> None:
    _setup(tmp_path, monkeypatch, [sys.executable, "-c", "print('ok')"],
           "# c\n\nLEAKME-not-a-pair\nSBX_KEY=abcd1234\n")
    code = with_env.main(["run"])
    err = capsys.readouterr().err
    assert code == 0
    assert "line 3" in err
    assert "LEAKME" not in err


def test_missing_child_exits_127(tmp_path, monkeypatch) -> None:
    _setup(tmp_path, monkeypatch, [str(tmp_path / "ghost")], "K=value1234\n")
    assert with_env.main(["run"]) == 127


def test_malformed_allowlist_exits_2(tmp_path, monkeypatch) -> None:
    root = tmp_path / "fw"
    (root / "config").mkdir(parents=True)
    (root / "config" / "with_env_allowlist.json").write_text("{not json")
    _setup(tmp_path, monkeypatch, None, "K=value1234\n")
    monkeypatch.setattr(with_env, "FRAMEWORK_ROOT", root)
    assert with_env.main(["run"]) == 2
