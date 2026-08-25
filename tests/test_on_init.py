"""Regression tests for hooks/on_init.py path resolution (Sprint 027 A3 / F-026-A3)."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"


@pytest.fixture()
def on_init(monkeypatch: pytest.MonkeyPatch):
    """Import hooks.on_init with scripts/ on sys.path."""
    monkeypatch.syspath_prepend(str(REPO))
    monkeypatch.syspath_prepend(str(SCRIPTS))
    sys.modules.pop("hooks.on_init", None)
    sys.modules.pop("on_init", None)
    return importlib.import_module("hooks.on_init")


def test_docstring_declares_host_scoped(on_init) -> None:
    """F-026-A3: scope must live on the module, not only in a distant workflow."""
    assert "Host-scoped" in (on_init.__doc__ or "")


def test_framework_paths_use_agents_root(
    on_init, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """INSTALL_SCRIPT and bridge lock resolve via agents_root, not bare .agents/."""
    fake_root = tmp_path / "agents-checkout"
    fake_root.mkdir()
    (fake_root / "scripts").mkdir()
    (fake_root / "scripts" / "install.py").write_text("# stub\n", encoding="utf-8")
    (fake_root / ".bridge_claude.lock").write_text("abc123\n", encoding="utf-8")

    monkeypatch.setattr(on_init, "agents_root", lambda: fake_root)

    assert on_init.install_script_path() == fake_root / "scripts" / "install.py"
    assert on_init.bridge_lock_path() == fake_root / ".bridge_claude.lock"
    assert on_init.install_script_path().is_file()
    assert on_init.bridge_lock_path().is_file()


def test_host_anchors_remain_cwd_relative(on_init) -> None:
    """Bridge anchors and .env paths stay relative to the host cwd."""
    assert on_init.CONFIG_PATH == Path(".env")
    assert on_init.ENV_TEMPLATE == Path(".env.template")
    assert all(not path.is_absolute() for path in on_init.BRIDGE_ANCHORS)
    assert all(
        str(path).startswith(".claude/") for path in on_init.BRIDGE_ANCHORS
    )


def test_bare_agents_prefix_not_used_for_framework_paths(on_init) -> None:
    """The false-green pattern Path('.agents/...') for framework files is gone."""
    source = Path(on_init.__file__).read_text(encoding="utf-8")
    assert 'Path(".agents/' not in source
    assert "agents_root" in source
