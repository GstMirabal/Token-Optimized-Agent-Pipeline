"""The legacy `install_claude.sh` shim names the real installer (Gate 1 QA1-4)."""

import subprocess
from pathlib import Path

SHIM = Path(__file__).resolve().parent.parent / "scripts" / "install_claude.sh"


def test_deprecation_message_names_install_py() -> None:
    result = subprocess.run(
        ["bash", str(SHIM), "--help"], capture_output=True, text=True, check=False
    )
    assert result.returncode == 0, result.stderr
    assert "DEPRECATED: use scripts/install.py" in result.stderr
