"""Fail when a versioned template cannot pass the check that consumes it.

An author starts a sprint artifact by copying a template out of
docs/standards/templates/. If the check that later judges that artifact rejects
the template itself, the template teaches the author to fail. Sprint 041 hit that
three times inside its own phases; the sharpest case rejected every plan written
faithfully from the official template, so the only plans that passed were the ones
that had dropped part of it.

This check renders each template declared in config/template_gates.json into a
scratch sprint directory and runs the declared check against the copy. Nothing is
linted in place: the checks decide by pattern-matching prose, so a check pointed at
a template trips over the template's own explanatory text.

The pairing must also be complete — a file in docs/standards/templates/ with
neither a case nor a typed exception fails the build, so a new template cannot be
added without deciding what judges it.

This module knows no check by name. Names live in config/template_gates.json; a
branch here that recognised one would make this a second copy of the checks, and
the second copy is what drifts.

invoked_by: Makefile `verify`.

Usage:
    python3 scripts/check_template_gates.py
    python3 scripts/check_template_gates.py --config config/template_gates.json

Exit codes:
    0 — every declared case passes and the pairing is complete
    2 — a case failed, a command is not permitted, or a template is undeclared
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root

CONFIG = Path("config/template_gates.json")
TEMPLATES = Path("docs/standards/templates")
INTERPRETER = "python3"
SPRINT_DIR_TOKEN = "{sprint_dir}"


def load_config(root: Path, config: Path) -> dict:
    """Read the pairing declaration.

    Args:
        root: Framework root.
        config: Path to the declaration, relative to root or absolute.

    Returns:
        The parsed declaration.
    """
    path = config if config.is_absolute() else root / config
    return json.loads(path.read_text(encoding="utf-8"))


def declared_templates(spec: dict) -> set[str]:
    """Return every template name a case renders or an exception excuses."""
    rendered = {name for case in spec["cases"] for name in case["render"]}
    return rendered | {item["template"] for item in spec["exceptions"]}


def check_completeness(root: Path, spec: dict) -> list[str]:
    """Compare the templates directory against the declaration."""
    present = {p.name for p in (root / TEMPLATES).iterdir() if p.is_file()}
    declared = declared_templates(spec)
    findings = [
        f"{name}: in {TEMPLATES}/ with no case and no typed exception"
        for name in sorted(present - declared)
    ]
    findings += [
        f"{name}: declared in {CONFIG} but absent from {TEMPLATES}/"
        for name in sorted(declared - present)
    ]
    return findings


def check_command(root: Path, command: list[str]) -> str | None:
    """Reject a command the declaration is not permitted to ask for.

    The declaration is data that gets executed, so these limits are enforced here
    rather than trusted to whoever edits the file.

    Args:
        root: Framework root.
        command: The declared argument vector.

    Returns:
        A finding, or None when the command is permitted.
    """
    if len(command) < 2 or command[0] != INTERPRETER:
        return f"command must start with {INTERPRETER!r}: {command}"
    script = (root / command[1]).resolve()
    if not str(script).startswith(str(root.resolve())):
        return f"script escapes the framework root: {command[1]}"
    if not script.is_file():
        return f"script does not exist: {command[1]}"
    return None


def render(root: Path, case: dict, sprint_dir: Path) -> None:
    """Copy each of a case's templates into the scratch directory verbatim.

    Placeholders are left untouched: substituting them would measure the fixture
    that replaced them rather than the template.
    """
    sprint_dir.mkdir(parents=True, exist_ok=True)
    for template, artifact in case["render"].items():
        shutil.copyfile(root / TEMPLATES / template, sprint_dir / artifact)


def run_case(root: Path, case: dict, scratch: Path) -> str | None:
    """Render one case and run its command against the copy.

    Returns:
        A finding, or None when the declared command exits 0.
    """
    refusal = check_command(root, case["command"])
    if refusal:
        return f"{case['id']}: {refusal}"
    sprint_dir = scratch / case["id"] / case["scratch_sprint_dir"]
    render(root, case, sprint_dir)
    command = [part.replace(SPRINT_DIR_TOKEN, str(sprint_dir)) for part in case["command"]]
    result = subprocess.run(command, cwd=root, capture_output=True, text=True, check=False)
    if result.returncode == 0:
        return None
    detail = (result.stderr or result.stdout).strip().splitlines()
    tail = detail[-1] if detail else "no output"
    return f"{case['id']}: {' '.join(case['command'][1:])} exited {result.returncode} — {tail}"


def check(root: Path, config: Path) -> int:
    """Run every declared case plus the completeness rule.

    Returns:
        The process exit code.
    """
    spec = load_config(root, config)
    findings = check_completeness(root, spec)
    with tempfile.TemporaryDirectory() as tmp:
        scratch = Path(tmp)
        for case in spec["cases"]:
            case = {**case, "scratch_sprint_dir": spec["scratch_sprint_dir"]}
            finding = run_case(root, case, scratch)
            if finding:
                findings.append(finding)
    if findings:
        print(f"❌ check_template_gates: {len(findings)} finding(s)", file=sys.stderr)
        for item in findings:
            print(f"   • {item}", file=sys.stderr)
        return 2
    print(f"[OK] check_template_gates: {len(spec['cases'])} case(s), pairing complete")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--config", type=Path, default=CONFIG, help="Pairing declaration")
    args = parser.parse_args()
    root = agents_root() if (Path.cwd() / "scripts").is_dir() else Path.cwd()
    return check(root, args.config)


if __name__ == "__main__":
    sys.exit(main())
