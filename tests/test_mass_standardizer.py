"""Tests for skills/mass-standardizer/scripts/mass_standardizer.py.

Sprint 023 `C4`. `agents.md §3 enforcement` calls this script the official
auditor of the Three-File Skill Standard, and it had never audited anything:
it resolved its root **five** `.parent` levels up where four are correct, so
`manifest_skills.json` was looked up one directory *above* the framework. From
the repository root the measured output was

    ERROR: Manifest not found at /Users/<user>/Developer/skills/manifest_skills.json

followed by exit **0** — the failure was printed and then reported as success,
so no caller checking the status code could see it.

Two further defects were hidden behind that one, and only a live run exposed the
third, which is why this file pins all three:

| # | Defect | Consequence |
| :--- | :--- | :--- |
| 1 | Root resolved one level too high | The auditor could not run from anywhere |
| 2 | The failure path printed its error and returned `0` | A caller reading the status code was told the run succeeded |
| 3 | `scripts/` created for **every** skill | The auditor violated the standard it enforces: `agents.md §3` prohibits padding a knowledge skill with empty scaffolding, and the first run that reached this library added it to 11 of them |

A fourth property is pinned here because the first attempt at this unit
**violated it**: replacement of a root `SKILL.md` was licensed by the presence of
the template's `(Automatic scaffolding)` sentence, and on that basis
`skills/django-expert-3rd/SKILL.md` was deleted. That file carried the sentence
*and* three authored directives, one of them the mandate `RA-02` states. A
substring cannot tell generated from generated-then-edited. The licence is now
byte-equality with the freshly rendered template, and
`test_a_root_file_edited_after_scaffolding_is_never_deleted` is that exact file's
shape.

Every test builds a **stand-in framework** under `tmp_path`. Pointing `cwd` at a
temporary directory isolates nothing here — the anchoring fix is precisely what
makes the working directory irrelevant — so a subprocess test that ran the real
script would exercise its write *and delete* paths against the tracked tree. The
`Makefile` carries a comment about a test that destroyed
`config/abandoned_branches.json` while the suite stayed green; this is the same
hazard, avoided by giving the script a different repository to find.

Measured against the tree before `C4`: **14 of these 15 fail**, the survivor
being the executable-skill case — the regression this unit must not cause, which
therefore passes on both sides. The failures are not of equal weight and the
distinction is worth recording, because a test that dies during setup has
reproduced nothing:

| Failure | Tests | Weight |
| :--- | :--- | :--- |
| The defect's own assertion — `assert None == 1`, `assert 0 == 1` on the process return code, `assert not scripts.exists()`, `'left untouched' in out`, the real wrong path in stdout | 8 | **Strong** |
| `AttributeError: no attribute 'vendored_skill_md'` | 5 | Weak — these cover helpers that did not exist before, so there is no earlier behaviour for them to contradict |
| `OSError: [Errno 22]` from `readlink()` on a regular file | 1 | Weak — `test_the_pointer_is_relative_so_it_survives_the_bridge` never reaches its comparison. The behaviour it names is pinned by the assertion in the test above it; this one adds the relative-target check only |

Fixtures are rendered by `scaffold_text` from `SKILL_MD_TEMPLATE` rather than by
the module's own `render_skill_md`, so that the eight strong tests reach their
assertions on both trees instead of dying on a missing symbol.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "mass-standardizer" / "scripts" / "mass_standardizer.py"
sys.path.insert(0, str(SCRIPT.parent))
import mass_standardizer as ms  # noqa: E402

VENDORED_BODY = "---\nname: vendored\ndescription: The real skill.\n---\n\n# Vendored\n"


def scaffold_text(skill_data: dict) -> str:
    """What the script writes for a skill with no `SKILL.md`, rendered locally.

    Deliberately formatted from `SKILL_MD_TEMPLATE` rather than obtained from
    `render_skill_md`: the template exists on both sides of this unit, the
    function does not. A fixture built from a symbol the pre-fix module lacks
    dies with `AttributeError` during setup, and a test that cannot reach its
    assertion has not reproduced anything.

    Args:
        skill_data: One `manifest_skills.json` entry.

    Returns:
        str: The rendered scaffold.
    """
    return ms.SKILL_MD_TEMPLATE.format(
        name=skill_data["name"],
        name_human=skill_data["name"].replace("-", " ").title(),
        description=skill_data["description"],
        category=skill_data["category"],
        tags=json.dumps(skill_data.get("tags", [])),
    )


def entry(name: str = "my-skill", path: str | None = None) -> dict:
    """One `manifest_skills.json` entry, minimal but complete.

    Args:
        name: The skill's manifest name.
        path: Its directory under `skills/`, defaulting to `name`.

    Returns:
        dict: The entry `standardize_skill` consumes.
    """
    return {
        "name": name,
        "path": path or name,
        "description": "A skill under test.",
        "category": "Testing",
        "tags": ["test"],
    }


def make_skill(base: Path, name: str = "my-skill") -> Path:
    """Create an empty skill directory inside a throwaway library.

    Args:
        base: The stand-in framework root.
        name: The skill directory's name.

    Returns:
        Path: The created skill directory.
    """
    skill = base / "skills" / name
    skill.mkdir(parents=True)
    return skill


def fake_framework(base: Path, with_manifest: bool = True) -> Path:
    """A framework tree the script will resolve to instead of this repository.

    The layout is the only thing that matters: the script locates `_root.py` at
    `parents[3] / "scripts"`, and `agents_root()` then answers with `_root.py`'s
    own grandparent. Reproducing both puts `base` where the real repository
    would be, so a subprocess run cannot reach the tracked tree.

    Args:
        base: The directory to build the stand-in framework in.
        with_manifest: Whether to write a manifest listing one knowledge skill.

    Returns:
        Path: The copied script, ready to run.
    """
    (base / "scripts").mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / "scripts" / "_root.py", base / "scripts" / "_root.py")

    script_dir = base / "skills" / "mass-standardizer" / "scripts"
    script_dir.mkdir(parents=True, exist_ok=True)
    script = script_dir / "mass_standardizer.py"
    shutil.copy(SCRIPT, script)

    if with_manifest:
        skill = make_skill(base)
        (skill / "SKILL.md").write_text(scaffold_text(entry()))
        (base / "skills" / "manifest_skills.json").write_text(json.dumps({"skills": [entry()]}))
    return script


def run(script: Path, cwd: Path) -> subprocess.CompletedProcess:
    """Run the stand-in script and capture everything it reports.

    Args:
        script: The copied script.
        cwd: The working directory to run it from.

    Returns:
        subprocess.CompletedProcess: With `stdout` and `returncode` populated.
    """
    return subprocess.run([sys.executable, str(script)], cwd=cwd,
                          capture_output=True, text=True, check=False)


def test_the_manifest_is_found_from_a_foreign_working_directory(tmp_path):
    """The defect, stated as the observation that exposed it.

    Before `C4` this exited `0` from every directory including the repository
    root, having printed that the manifest was missing. The assertion is
    therefore on stdout as much as on the status code: a green exit proves
    nothing here, because the broken version returned one too.
    """
    script = fake_framework(tmp_path)
    foreign = tmp_path / "elsewhere"
    foreign.mkdir()

    result = run(script, cwd=foreign)

    assert result.returncode == 0
    assert "Manifest not found" not in result.stdout
    assert "Starting Mass Standardization" in result.stdout


def test_running_against_a_standardized_library_writes_nothing(tmp_path):
    """Idempotence, and the reason this writer is safe to invoke from a test.

    Every line this script emits for a change is prefixed `[+]` or `[!]`. On a
    library that already satisfies the standard there must be none of either.

    The second assertion is what gives the first one meaning: a script that
    never reached the library writes nothing either, which is exactly how the
    broken version passed this check.
    """
    script = fake_framework(tmp_path)

    result = run(script, cwd=tmp_path)

    changes = [ln for ln in result.stdout.splitlines() if ln.startswith(("  [+]", "  [!]"))]
    assert changes == []
    assert "Standardization complete" in result.stdout


def test_a_missing_manifest_is_a_failing_return_not_a_printed_one(tmp_path, monkeypatch, capsys):
    """A caller that reads the result must learn the run did not happen.

    This is the same class as `C9` and `C10`: a control reporting a
    determination it cannot support. The script knew it had failed and said so
    on stdout, then reported success.

    `raising=False` is load-bearing. Without it this test dies with
    `AttributeError` against the pre-fix module — which had no `agents_root` to
    replace — and an error raised in setup proves nothing about the defect. With
    it, the pre-fix module reaches the assertion and fails on `None == 1`, which
    is the defect itself.
    """
    monkeypatch.setattr(ms, "agents_root", lambda: tmp_path, raising=False)

    assert ms.main() == 1
    assert "Manifest not found" in capsys.readouterr().out


def test_a_missing_manifest_fails_the_process_not_only_the_function(tmp_path):
    """The caller-visible half of the same defect.

    `main()` returning `1` is inert unless `sys.exit` carries it out to the
    shell, and it is the shell that `Makefile` targets and hooks read. Measured
    on both trees: the pre-fix script exits `0` here while printing that the
    manifest is missing.
    """
    script = fake_framework(tmp_path, with_manifest=False)

    result = run(script, cwd=tmp_path)

    assert result.returncode == 1
    assert "Manifest not found" in result.stdout


def test_a_knowledge_skill_is_not_padded_with_scaffolding(tmp_path):
    """`agents.md §3`: a knowledge skill requires a `SKILL.md` and nothing else.

    The previous version called `mkdir()` on `scripts/` before asking, so every
    skill it touched became executable by the act of being audited.
    """
    skill = make_skill(tmp_path)
    (skill / "SKILL.md").write_text("---\nname: my-skill\ndescription: x\n---\n")

    ms.standardize_skill(entry(), tmp_path)

    assert not (skill / "scripts").exists()
    assert not (skill / "README.md").exists()


def test_an_executable_skill_still_gets_its_package_and_readme(tmp_path):
    """The regression the knowledge-skill fix must not cause.

    A skill that ships `/scripts/` is executable by `agents.md §3`'s own
    definition and owes the full Three-File Standard.
    """
    skill = make_skill(tmp_path)
    (skill / "scripts").mkdir()
    (skill / "scripts" / "run.py").touch()

    ms.standardize_skill(entry(), tmp_path)

    assert (skill / "scripts" / "__init__.py").exists()
    assert (skill / "README.md").exists()
    assert (skill / "SKILL.md").exists()


def test_a_vendored_skill_md_is_pointed_at_rather_than_scaffolded_over(tmp_path):
    """The skill's own content must be what the root `SKILL.md` resolves to.

    `generate_manifest.py` reads `<skill>/SKILL.md` and Claude Code discovers by
    the same path, so a stub at the root is what both of them get.
    """
    skill = make_skill(tmp_path)
    (skill / "skills").mkdir()
    (skill / "skills" / "SKILL.md").write_text(VENDORED_BODY)

    ms.standardize_skill(entry(), tmp_path)

    assert (skill / "SKILL.md").is_symlink()
    assert (skill / "SKILL.md").read_text() == VENDORED_BODY


def test_the_pointer_is_relative_so_it_survives_the_bridge(tmp_path):
    """`install_claude.py` links each skill directory into a host's `.claude/`.

    An absolute target would point back into whichever checkout generated it,
    which is precisely the class of leak `RA-15` exists to prevent.
    """
    skill = make_skill(tmp_path)
    (skill / "skills").mkdir()
    (skill / "skills" / "SKILL.md").write_text(VENDORED_BODY)

    ms.standardize_skill(entry(), tmp_path)

    assert not Path((skill / "SKILL.md").readlink()).is_absolute()


def test_untouched_scaffolding_over_a_vendored_skill_is_replaced(tmp_path):
    """Replacement is licensed by byte-equality with the rendered template.

    This is the only shape that qualifies: exactly what this script writes, with
    nothing added to it since.
    """
    skill = make_skill(tmp_path)
    (skill / "skills").mkdir()
    (skill / "skills" / "SKILL.md").write_text(VENDORED_BODY)
    (skill / "SKILL.md").write_text(scaffold_text(entry()))

    ms.standardize_skill(entry(), tmp_path)

    assert (skill / "SKILL.md").is_symlink()
    assert (skill / "SKILL.md").read_text() == VENDORED_BODY


def test_a_root_file_edited_after_scaffolding_is_never_deleted(tmp_path, capsys):
    """`skills/django-expert-3rd/SKILL.md`, and the deletion this unit committed.

    The fixture is that file's shape: scaffolded once, then edited, so it still
    carries the template's `(Automatic scaffolding)` sentence in one section
    while another holds authored governance directives. The first attempt at
    `C4` matched on that sentence and unlinked the file, losing three directives
    including the one `RA-02` mandates. `agents.md §2 destructive_flags` puts
    that decision with a human, and this test is where that is enforced.
    """
    skill = make_skill(tmp_path)
    (skill / "skills").mkdir()
    (skill / "skills" / "SKILL.md").write_text(VENDORED_BODY)
    edited = scaffold_text(entry()).replace(
        "- [ ] Define step-by-step logic here.",
        "- **Signal Implementation**: MANDATORY use of the lazy signal paradigm.")
    assert "(Automatic scaffolding)" in edited, "the fixture must carry the old licence"
    (skill / "SKILL.md").write_text(edited)

    ms.standardize_skill(entry(), tmp_path)

    assert not (skill / "SKILL.md").is_symlink()
    assert (skill / "SKILL.md").read_text() == edited
    assert "left untouched" in capsys.readouterr().out


def test_a_dangling_vendored_symlink_is_not_pointed_at(tmp_path):
    """A pointer to a pointer to nothing, reported as success.

    Without the `is_file()` guard the root becomes a symlink that resolves
    nowhere, `generate_manifest.py` drops the skill from the manifest without
    saying why, and this script prints `[+]` over both.
    """
    skill = make_skill(tmp_path)
    (skill / "skills").mkdir()
    (skill / "skills" / "SKILL.md").symlink_to(Path("no_such_file.md"))

    assert ms.vendored_skill_md(skill) is None


def test_the_shallowest_vendored_file_wins(tmp_path):
    """Vendors nest differently, and repeated runs must agree on which one wins."""
    skill = make_skill(tmp_path)
    for nested in ("reference/deep/SKILL.md", "skills/SKILL.md"):
        target = skill / nested
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(VENDORED_BODY)

    assert ms.vendored_skill_md(skill) == skill / "skills" / "SKILL.md"


@pytest.mark.parametrize("nested", ["skills/SKILL.md", "reference/deep/SKILL.md"])
def test_a_vendored_file_is_found_at_any_depth(tmp_path, nested):
    """`django-expert-3rd` is one shape of vendoring, not the shape."""
    skill = make_skill(tmp_path)
    target = skill / nested
    target.parent.mkdir(parents=True)
    target.write_text(VENDORED_BODY)

    assert ms.vendored_skill_md(skill) == target


def test_the_skills_own_root_skill_md_is_not_mistaken_for_a_vendored_one(tmp_path):
    """The root file is what a nested one shadows — it can never be its own target."""
    skill = make_skill(tmp_path)
    (skill / "SKILL.md").write_text(VENDORED_BODY)

    assert ms.vendored_skill_md(skill) is None
