"""Tests for skills/env-shielding-auditor — F-086-S1.

The auditor's patterns were sound and the file list it applied them to was not:
it read `.py`, `.js`, `.ts`, `.json`, `.env`, `.sh` and `.bash` only, so every
configuration format a real deployment keeps its credentials in — Compose,
Helm values, Terraform, `.ini`, `.conf`, `.toml` — went unread, and files with
no extension at all (`Dockerfile`, `Makefile`) were invisible by construction.

Loaded through importlib because the skill directory name is hyphenated and is
therefore not a legal module path.
"""
import importlib.util
import sys
from pathlib import Path

import pytest

FRAMEWORK = Path(__file__).resolve().parent.parent
AUDITOR_PATH = (
    FRAMEWORK / "skills" / "env-shielding-auditor" / "scripts" /
    "env_shielding_auditor.py"
)


def _load_auditor():
    spec = importlib.util.spec_from_file_location("env_shielding_auditor", AUDITOR_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["env_shielding_auditor"] = module
    spec.loader.exec_module(module)
    return module


auditor = _load_auditor()

# A value that matches the auditor's own "Generic API Key" character class, so
# these cases isolate the FILE LIST defect and nothing else. The separate
# question of which value shapes the patterns accept is recorded in
# docs/sprints/023-core-pipeline/task_scope.md, not conflated here.
LIVE = "abcdef0123456789abcdef"


def _scanned(tmp_path, name: str, body: str) -> bool:
    """Reports whether scan_files opened `name` and found the planted secret."""
    (tmp_path / name).write_text(body, encoding="utf-8")
    return any(name in leak for leak in auditor.scan_files(str(tmp_path)))


@pytest.mark.parametrize("name,body", [
    ("docker-compose.yml", f'    environment:\n      API_KEY: "{LIVE}"\n'),
    ("values.yaml",        f'apiKey: "{LIVE}"\n'),
    ("config.toml",        f'api_key = "{LIVE}"\n'),
    ("settings.ini",       f"api_key = {LIVE}\n"),
    ("app.cfg",            f'secret_key = "{LIVE}"\n'),
    ("service.conf",       f"api_key = {LIVE}\n"),
    ("main.tf",            f'access_token = "{LIVE}"\n'),
    ("config.toml.example", f'api_key = "{LIVE}"\n'),
    ("Dockerfile",         "ENV AWS_KEY=AKIAIOSFODNN7EXAMPLE\n"),
    ("Makefile",           f'export API_KEY = "{LIVE}"\n'),
])
def test_configuration_formats_are_scanned(tmp_path, name, body):
    assert _scanned(tmp_path, name, body)


@pytest.mark.parametrize("name,body", [
    ("app.py",    f'api_key = "{LIVE}"\n'),
    ("index.js",  f'const apiKey = "{LIVE}";\n'),
    ("data.json", f'{{"api_key": "{LIVE}"}}\n'),
    ("run.sh",    f"export API_KEY={LIVE}\n"),
])
def test_previously_scanned_formats_still_are(tmp_path, name, body):
    """Regression: widening the list must not drop anything already on it."""
    assert _scanned(tmp_path, name, body)


@pytest.mark.parametrize("name", ["notes.md", "logo.png", "report.csv"])
def test_unlisted_formats_stay_unscanned(tmp_path, name):
    """The list is widened deliberately, not abolished."""
    assert not _scanned(tmp_path, name, f'api_key = "{LIVE}"\n')
