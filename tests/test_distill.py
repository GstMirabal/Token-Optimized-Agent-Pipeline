"""Regression coverage for skills/governance-sentinel/scripts/distill.py's
ROOT resolution — a prior unconditional 4-parent count always landed inside
.agents/ for a host install, so this script had never once found real
telemetry on any host (memory/ only ever exists at the host root, never
inside the .agents submodule — submodule_purity).
"""
import importlib.util
import sys
from pathlib import Path

DISTILL_PATH = (
    Path(__file__).resolve().parent.parent
    / "skills" / "governance-sentinel" / "scripts" / "distill.py"
)


def _load_distill():
    spec = importlib.util.spec_from_file_location("distill", DISTILL_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["distill"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_host_mode_root_is_one_level_above_agents(tmp_path):
    # Simulates .agents installed as a host's submodule: AGENTS_ROOT/.git is
    # a gitlink *file*, not a directory, so ROOT must climb one more level.
    agents_root = tmp_path / "host" / ".agents"
    scripts_dir = agents_root / "skills" / "governance-sentinel" / "scripts"
    scripts_dir.mkdir(parents=True)
    (agents_root / ".git").write_text("gitdir: ../.git/modules/.agents\n")

    fake_file = scripts_dir / "distill.py"
    fake_file.write_text(DISTILL_PATH.read_text())

    spec = importlib.util.spec_from_file_location("distill_host", fake_file)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["distill_host"] = mod
    spec.loader.exec_module(mod)

    assert mod.ROOT == agents_root.parent
    assert mod.TELEMETRY_PATH == agents_root.parent / "memory/telemetry/raw_errors.json"


def test_nucleus_mode_root_is_agents_root_itself(tmp_path):
    # Simulates running distill.py inside the .agents repo's own checkout:
    # .git there is a real directory, so ROOT stays at AGENTS_ROOT.
    agents_root = tmp_path / "nucleus-checkout"
    scripts_dir = agents_root / "skills" / "governance-sentinel" / "scripts"
    scripts_dir.mkdir(parents=True)
    (agents_root / ".git").mkdir()

    fake_file = scripts_dir / "distill.py"
    fake_file.write_text(DISTILL_PATH.read_text())

    spec = importlib.util.spec_from_file_location("distill_nucleus", fake_file)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["distill_nucleus"] = mod
    spec.loader.exec_module(mod)

    assert mod.ROOT == agents_root
    assert mod.TELEMETRY_PATH == agents_root / "memory/telemetry/raw_errors.json"


def test_load_telemetry_reads_real_file(tmp_path, monkeypatch):
    mod = _load_distill()
    fake_telemetry = tmp_path / "raw_errors.json"
    fake_telemetry.write_text('[{"hook": "on_commit", "type": "X"}]')
    monkeypatch.setattr(mod, "TELEMETRY_PATH", fake_telemetry)

    data = mod.load_telemetry()
    assert data == [{"hook": "on_commit", "type": "X"}]
