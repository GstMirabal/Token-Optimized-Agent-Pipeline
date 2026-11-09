"""Tests for scripts/graph_update.py (Sprint 059 L-01, D39)."""

from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path
from typing import Any

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "graph_update.py"
spec = importlib.util.spec_from_file_location("graph_update_under_test", SCRIPT)
assert spec is not None and spec.loader is not None
graph_update = importlib.util.module_from_spec(spec)
spec.loader.exec_module(graph_update)


def _install(
    monkeypatch: pytest.MonkeyPatch,
    *,
    threshold: bool = True,
    rebuild: Any = "ok",
) -> tuple[types.ModuleType, list[dict[str, Any]]]:
    """Put fake graphify modules into `sys.modules`.

    Args:
        monkeypatch: pytest monkeypatch fixture.
        threshold: Whether the fake `graphify.extract` defines `_PARALLEL_THRESHOLD`.
        rebuild: `"ok"` returns True, `"missing"` omits `_rebuild_code`, a bool is
            returned as is, an exception instance is raised.

    Returns:
        tuple[types.ModuleType, list[dict[str, Any]]]: The fake extract module and
        the recorded `_rebuild_code` calls.
    """
    calls: list[dict[str, Any]] = []
    package = types.ModuleType("graphify")
    extract = types.ModuleType("graphify.extract")
    watch = types.ModuleType("graphify.watch")
    if threshold:
        extract._PARALLEL_THRESHOLD = 20  # type: ignore[attr-defined]

    def fake_rebuild(path: Path, **kwargs: Any) -> bool:
        calls.append({"path": path, "threshold": extract.__dict__.get("_PARALLEL_THRESHOLD"), **kwargs})
        if isinstance(rebuild, Exception):
            raise rebuild
        return True if rebuild == "ok" else bool(rebuild)

    if rebuild != "missing":
        watch._rebuild_code = fake_rebuild  # type: ignore[attr-defined]
    for name, mod in (("graphify", package), ("graphify.extract", extract), ("graphify.watch", watch)):
        monkeypatch.setitem(sys.modules, name, mod)
    return extract, calls


@pytest.mark.parametrize("force", [False, True])
def test_success_raises_threshold_and_passes_force(monkeypatch: pytest.MonkeyPatch, force: bool) -> None:
    extract, calls = _install(monkeypatch)
    assert graph_update.main(["--force"] if force else []) == 0
    assert len(calls) == 1
    assert calls[0]["path"] == Path(".")
    assert calls[0]["force"] is force
    assert calls[0]["threshold"] >= 10**6
    assert extract._PARALLEL_THRESHOLD >= 10**6


def test_import_failure_is_nonzero(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    for name in ("graphify", "graphify.extract", "graphify.watch"):
        monkeypatch.setitem(sys.modules, name, None)  # None makes the import raise
    assert graph_update.main([]) == 1
    assert len(capsys.readouterr().err.strip().splitlines()) == 1


def test_missing_threshold_is_nonzero(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    _, calls = _install(monkeypatch, threshold=False)
    assert graph_update.main([]) == 1
    assert calls == []
    assert "_PARALLEL_THRESHOLD" in capsys.readouterr().err


def test_missing_rebuild_is_nonzero(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    _install(monkeypatch, rebuild="missing")
    assert graph_update.main([]) == 1
    assert "_rebuild_code" in capsys.readouterr().err


def test_rebuild_false_is_nonzero(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    _install(monkeypatch, rebuild=False)
    assert graph_update.main([]) == 1
    assert len(capsys.readouterr().err.strip().splitlines()) == 1


def test_rebuild_raising_unlisted_exception_is_nonzero(monkeypatch: pytest.MonkeyPatch) -> None:
    class Fresh(Exception):
        pass

    _install(monkeypatch, rebuild=Fresh("boom"))
    assert graph_update.main([]) == 1
