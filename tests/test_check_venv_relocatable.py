"""Tests for scripts/check_venv_relocatable.py (Sprint 043 D2).

A fake ``venv_skillopt`` tree is built under ``tmp_path`` with a ``pyvenv.cfg``
and a ``bin/pip`` console-script. The ``command =`` line and the ``bin/pip``
shebang either point at the fixture itself (consistent) or at an unrelated path
(relocated / broken).

Sprint 043 Gate-2 regression cases: a checkout path containing whitespace, and
pip's POSIX ``#!/bin/sh`` + ``'''exec' '<python>' "$0" "$@"`` console-script
wrapper. Both were false-positived by the pre-fix tokenising extractors.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
sys.path.insert(0, str(SCRIPTS))
import check_venv_relocatable as cvr

# Fixture content only — never executed; the CLI tests use sys.executable.
_SYSTEM_PY = "/opt/python/3.13/bin/python3"


def _make_venv(root: Path, build_path: Path) -> Path:
    """Create a minimal fake venv whose recorded build path is ``build_path``."""
    venv = root / "venv_skillopt"
    (venv / "bin").mkdir(parents=True)
    (venv / "pyvenv.cfg").write_text(
        "home = /usr/bin\n"
        "version = 3.13.13\n"
        f"executable = {_SYSTEM_PY}.13\n"
        f"command = {_SYSTEM_PY} -m venv {build_path}\n",
        encoding="utf-8",
    )
    (venv / "bin" / "pip").write_text(
        f"#!{build_path}/bin/python3.13\n# console script\n", encoding="utf-8"
    )
    (venv / "bin" / "python3.13").write_text("# stub interpreter\n", encoding="utf-8")
    return venv


def _make_sh_wrapper_pip(venv: Path, interpreter: Path) -> None:
    """Write ``bin/pip`` as pip's POSIX space-safe ``#!/bin/sh`` exec wrapper."""
    (venv / "bin").mkdir(parents=True, exist_ok=True)
    (venv / "bin" / "pip").write_text(
        "#!/bin/sh\n"
        f"'''exec' '{interpreter}' \"$0\" \"$@\"\n"
        "' '''\n"
        "import sys\n",
        encoding="utf-8",
    )


def test_consistent_venv_returns_no_problems(tmp_path: Path) -> None:
    venv = _make_venv(tmp_path, tmp_path / "venv_skillopt")
    assert cvr.check(venv) == []


def test_relocated_venv_flags_cfg_and_shebang(tmp_path: Path) -> None:
    venv = _make_venv(tmp_path, Path("/somewhere/else/venv_skillopt"))
    problems = cvr.check(venv)
    assert len(problems) == 2
    assert any("pyvenv.cfg" in p for p in problems)
    assert any("console-script interpreter" in p for p in problems)


def test_absent_venv_is_not_a_failure(tmp_path: Path) -> None:
    assert cvr.check(tmp_path / "nonexistent") == []


def test_clear_flag_in_command_line_is_parsed(tmp_path: Path) -> None:
    venv = tmp_path / "venv_skillopt"
    (venv / "bin").mkdir(parents=True)
    (venv / "pyvenv.cfg").write_text(
        f"command = {_SYSTEM_PY} -m venv --clear {venv}\n", encoding="utf-8"
    )
    assert cvr.check(venv) == []


def test_cli_exit_0_on_consistent(tmp_path: Path) -> None:
    venv = _make_venv(tmp_path, tmp_path / "venv_skillopt")
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "check_venv_relocatable.py"), "--venv", str(venv)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "[OK]" in result.stdout


def test_cli_exit_2_on_relocated(tmp_path: Path) -> None:
    venv = _make_venv(tmp_path, Path("/somewhere/else/venv_skillopt"))
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "check_venv_relocatable.py"), "--venv", str(venv)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert "[FAIL]" in result.stdout


def test_spaced_build_path_is_consistent(tmp_path: Path) -> None:
    """A correctly-located venv under a path with a space is not a failure."""
    spaced_root = tmp_path / "My Projects" / "host" / ".agents"
    venv = _make_venv(spaced_root, spaced_root / "venv_skillopt")
    assert cvr.check(venv) == []
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "check_venv_relocatable.py"), "--venv", str(venv)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "[OK]" in result.stdout


def test_spaced_relocated_build_path_still_flagged(tmp_path: Path) -> None:
    """A space in the path must not mask a genuinely relocated venv."""
    venv = _make_venv(tmp_path, Path("/other root/My Projects/venv_skillopt"))
    problems = cvr.check(venv)
    assert len(problems) == 2
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "check_venv_relocatable.py"), "--venv", str(venv)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2


def test_posix_sh_wrapper_under_venv_is_consistent(tmp_path: Path) -> None:
    """pip's ``#!/bin/sh`` wrapper whose interpreter is inside the venv passes."""
    venv = tmp_path / "venv_skillopt"
    interpreter = venv / "bin" / "python3.13"
    _make_sh_wrapper_pip(venv, interpreter)
    interpreter.write_text("# stub interpreter\n", encoding="utf-8")
    assert cvr.check(venv) == []


def test_posix_sh_wrapper_outside_venv_flags_one_problem(tmp_path: Path) -> None:
    """The same wrapper pointing at an interpreter outside the venv is flagged."""
    venv = tmp_path / "venv_skillopt"
    _make_sh_wrapper_pip(
        venv, Path("/gone/other place/venv_skillopt/bin/python3.13")
    )
    problems = cvr.check(venv)
    assert len(problems) == 1
    assert "console-script interpreter" in problems[0]
