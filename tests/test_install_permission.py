"""Tests for scripts/install.py behaviour when the bridge write is denied (Sprint 055 U05)."""

from __future__ import annotations

import importlib
import json
import os
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"

pytestmark = pytest.mark.skipif(
    hasattr(os, "geteuid") and os.geteuid() == 0,
    reason="root bypasses file permission bits",
)


@pytest.fixture()
def install(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """Import install with HOST_DIR redirected to a temporary host root."""
    monkeypatch.syspath_prepend(str(SCRIPTS))
    sys.modules.pop("install", None)
    module = importlib.import_module("install")
    monkeypatch.setattr(module, "HOST_DIR", tmp_path)
    return module


def _denied_destination(tmp_path: Path) -> tuple[Path, Path]:
    """Create a template and a read-only destination settings file."""
    template = tmp_path / "template.json"
    template.write_text(json.dumps({"a": 1}), encoding="utf-8")
    dest = tmp_path / ".claude" / "settings.json"
    dest.parent.mkdir()
    dest.write_text("{}\n", encoding="utf-8")
    dest.chmod(0o444)
    return template, dest


def test_merge_into_denied_write_exits_3_without_traceback(
    install, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys
) -> None:
    template, dest = _denied_destination(tmp_path)
    monkeypatch.setattr(install, "is_nucleus", lambda: False, raising=False)
    with pytest.raises(SystemExit) as excinfo:
        install.merge_into(template, dest)
    assert excinfo.value.code == 3
    err = capsys.readouterr().err
    assert "Traceback" not in err
    assert "PermissionError" in err
    assert ".claude/settings.json" in err
    assert str(tmp_path) not in err
    assert "bash .agents/scripts/install.sh --target claude" in err


def test_merge_into_denied_write_nucleus_form(
    install, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys
) -> None:
    template, dest = _denied_destination(tmp_path)
    monkeypatch.setattr(install, "is_nucleus", lambda: True, raising=False)
    with pytest.raises(SystemExit) as excinfo:
        install.merge_into(template, dest)
    assert excinfo.value.code == 3
    err = capsys.readouterr().err
    assert "bash scripts/install.sh --target claude" in err
    assert ".agents/scripts/install.sh" not in err
