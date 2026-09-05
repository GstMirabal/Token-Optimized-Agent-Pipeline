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

The declaration is a data file that gets executed, so every field it contributes
is constrained here rather than trusted to whoever edits it: the interpreter is
pinned, the script and every rendered path must resolve inside the directory that
owns it, the scratch directory name is one relative component, and `{sprint_dir}`
is the only expandable token. Guarding the argument vector alone is not enough —
the render map reaches the filesystem too.

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
import os
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
VALID_EXCEPTION_REASONS = frozenset({"no-automated-gate", "phase-mismatch"})


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


def check_exceptions(spec: dict) -> list[str]:
    """Reject an exemption that is not typed.

    An untyped exemption excuses a template while saying nothing about why, which
    is how a stale one survives. The valid set lives here, in code, and the
    declaration's own mirror of it is compared against this one so the two cannot
    drift — the drift being the defect class this whole check exists to close.
    """
    findings = [
        f"{item.get('template', '<unnamed>')}: exception reason "
        f"{item.get('reason')!r} is not one of {sorted(VALID_EXCEPTION_REASONS)}"
        for item in spec["exceptions"]
        if item.get("reason") not in VALID_EXCEPTION_REASONS
    ]
    declared = set(spec.get("_valid_exception_reasons", []))
    if declared != set(VALID_EXCEPTION_REASONS):
        findings.append(
            f"{CONFIG} `_valid_exception_reasons` {sorted(declared)} disagrees with "
            f"the set this check enforces, {sorted(VALID_EXCEPTION_REASONS)}"
        )
    return findings


def check_gate_exceptions(root: Path, spec: dict) -> list[str]:
    """Hold a recorded non-pairing to the same standard as an exemption.

    `gate_exceptions` records a check deliberately not paired with a template —
    a decision, not a grant, so nothing depends on it at runtime. That is exactly
    why it rots: measured by Gate 2, an entry naming a non-existent check, a
    non-existent template and an invented reason passed in silence, one array away
    from three guards written to prevent that staleness.
    """
    findings = []
    for item in spec.get("gate_exceptions", []):
        gate = item.get("gate", "")
        template = item.get("template", "")
        if item.get("reason") not in VALID_EXCEPTION_REASONS:
            findings.append(f"{gate or '<unnamed>'}: reason {item.get('reason')!r} is not typed")
        if not (root / gate).is_file():
            findings.append(f"gate_exceptions names a check that does not exist: {gate!r}")
        if not (root / TEMPLATES / template).is_file():
            findings.append(f"gate_exceptions names a template that does not exist: {template!r}")
    return findings


def check_scratch_name(spec: dict) -> list[str]:
    """Require the scratch directory to be one relative path component.

    It is joined onto a temporary directory. A name carrying separators or `..`
    would place the rendered copies outside that directory, where nothing cleans
    them up and something may already live.
    """
    name = spec["scratch_sprint_dir"]
    if Path(name).parts == (name,) and name not in {".", ".."}:
        return []
    return [f"scratch_sprint_dir must be a single relative path component: {name!r}"]


def check_completeness(root: Path, spec: dict) -> list[str]:
    """Compare the templates directory against the declaration."""
    present = {
        p.name
        for p in (root / TEMPLATES).iterdir()
        if p.is_file() and not p.name.startswith(".")
    }
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
    if not script.is_relative_to(root.resolve()):
        return f"script escapes the framework root: {command[1]}"
    if not script.is_file():
        return f"script does not exist: {command[1]}"
    return None


def check_render_paths(root: Path, case: dict, sprint_dir: Path) -> list[str]:
    """Reject a render map that reads or writes outside its two directories.

    `check_command` guarded the argument vector and nothing else, while the render
    map from the same file reached `shutil.copyfile` directly — so a declaration
    could read any readable file and overwrite any writable one. A source must be
    a template; a target must land inside the scratch sprint directory.

    The caller MUST establish that `sprint_dir` is itself inside the temporary
    directory before calling this. Target containment is measured against that
    anchor, so an anchor the declaration chose would satisfy it vacuously — which
    it did, silently, until Gate 1 round 2 of Sprint 042 measured it.
    """
    findings = []
    templates = (root / TEMPLATES).resolve()
    for template, artifact in case["render"].items():
        source = (root / TEMPLATES / template).resolve()
        if not source.is_relative_to(templates) or source == templates:
            findings.append(f"render source is not a file in {TEMPLATES}/: {template}")
        target = (sprint_dir / artifact).resolve()
        if not target.is_relative_to(sprint_dir.resolve()) or target == sprint_dir.resolve():
            findings.append(f"render target escapes the scratch directory: {artifact}")
    return findings


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
    if not sprint_dir.resolve().is_relative_to(scratch.resolve()):
        return f"{case['id']}: scratch sprint directory escapes the temporary directory"
    unsafe = check_render_paths(root, case, sprint_dir)
    if unsafe:
        return f"{case['id']}: {unsafe[0]}"
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
    findings = (
        check_completeness(root, spec)
        + check_exceptions(spec)
        + check_gate_exceptions(root, spec)
    )
    unsafe_scratch = check_scratch_name(spec)
    findings += unsafe_scratch
    with tempfile.TemporaryDirectory() as tmp:
        scratch = Path(tmp)
        for case in spec["cases"] if not unsafe_scratch else []:
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
    os.chdir(agents_root())
    return check(agents_root(), args.config)


if __name__ == "__main__":
    sys.exit(main())
