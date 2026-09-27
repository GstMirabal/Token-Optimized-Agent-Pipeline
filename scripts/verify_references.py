"""Reference-integrity linter — immunizes the framework against the
"Master Ledger class" of inconsistency: normative references whose target
no longer exists or can never be reached.

Checks (run from the .agents root; CI fails the PR on any violation):
  (a) Every rules/*.md is reachable — referenced by name from agents.md,
      a workflow, or a command (lazy-loading requires a pointer somewhere).
  (b) Every *_TEMPLATE.md cited in agents.md/workflows/ exists in
      docs/standards/templates/.
  (c) Every numbered "Rule NN" citation resolves to an entry in
      rules/LEGACY_RULE_CONCORDANCE.md (the numbering system was abolished
      by the tabular refactor; unmapped numbers are phantom references).
  (d) Every workflow, script, executable skill, ``skills/*/scripts/*.py``
      module and ``tests/*.py`` file has a declared invoker, or a declared
      exception (RA-16 INVOCATION_COVERAGE, agents.md §7). ``tests/test_*.py``
      and ``tests/conftest.py`` resolve to pytest collection under
      ``make verify`` (confirmed against the Makefile recipe, not assumed);
      other ``tests/*.py`` files resolve via an import from ``scripts/`` or
      ``hooks/`` or their own ``invoked_by:``. A ``skills/*/scripts/*.py``
      module resolves via its own skill's SKILL.md/README.md naming its
      filename, skill-relative path, or that path as a dotted module
      (``scripts.env``, as in ``python -m scripts.env``) as a whole token
      (never a bare-stem substring), a Makefile recipe, its own
      ``invoked_by:``, or a
      path-resolved import from another file that is itself resolved by one
      of those — computed as a fixpoint closure over ``scripts/``, ``hooks/``
      and ``skills/*/scripts/`` (``tests/`` importers excluded: a test
      importing production code does not invoke it) so two mutually
      -importing orphans never resolve each other (KI-048-1 D9, Sprint 052
      U19; tightened Sprint 052 remediation round 1, F-1/F-2). Every
      ``invoked_by:`` token of the form ``path#fragment`` also resolves its
      ``#fragment`` — a GitHub heading slug, an ``<a id=>`` / ``<a name=>``
      anchor, or a workflow step-id token — in the file ``path`` names
      (Sprint 047 U11, S045-22).
  (e) config/rule_triggers.json mirrors rules/*.md.
  (f) Living docs (guides, decisions, audits) that cite ``path:line`` point at a
      file whose line count is at least that line — Sprint 029 J6. Does **not**
      scan docs/sprints/ or docs/roadmaps/ (historical records).
  (g) Every ``agents/*.md`` with frontmatter ``tier:`` has ``model:`` equal to
      ``config/model_tiers.json`` → ``tiers[tier]["claude_code"]["model"]``
      (Claude Code side only, D15). Plan 035 called this ``(f)``; letter ``(f)``
      is already ``check_file_line_citations`` (Sprint 029), so this is ``(g)``.

invoked_by: Makefile `verify` target (and therefore .github/workflows/ci.yml).
"""
import ast
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root

CONCORDANCE = Path("rules/LEGACY_RULE_CONCORDANCE.md")
TEMPLATES_DIR = Path("docs/standards/templates")
EXCEPTIONS_FILE = Path("config/invocation_exceptions.json")
MODEL_TIERS_FILE = Path("config/model_tiers.json")

# Living documentary corpus for check (f). Historical sprint/roadmap prose is
# excluded by construction — abort criterion 3 of Sprint 029.
FILE_LINE_CORPUS = (
    Path("docs/guides"),
    Path("docs/decisions"),
    Path("docs/audits"),
)

# Leading YAML frontmatter for check (g). Only ``model:`` / ``tier:`` are read.
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
AGENT_TIER_MODEL_RE = re.compile(r"^(model|tier):\s*(\S+)\s*$", re.MULTILINE)

# ``path#fragment`` / ``path.md#fragment`` tokens inside an ``invoked_by:`` line.
# Group 1 (path) is optional: a bare ``#fragment`` inherits the previous token's
# path (e.g. ``start_workflow.md#readiness_probe and #platform_probe``).
INVOKED_TOKEN_RE = re.compile(r"([\w./-]+)?#([\w-]+)")

# ``path/to/file.ext:123`` inside backticks or as a bare token. Requires a
# known text/code suffix so bare ``12:34`` clocks and URL ports do not match.
FILE_LINE_RE = re.compile(
    r"(?<![\w./-])"  # not mid-token
    r"((?:[\w.-]+/)*[\w.-]+\.(?:md|py|json|sh|yml|yaml|toml|txt|mdc))"
    r":(\d+)"
    r"(?![\w./-])"
)
# Reasons an artifact may legitimately have no invoker inside the framework.
# A free-text reason is rejected: an exception nobody can categorise is an
# exception nobody will ever revisit.
VALID_EXCEPTION_REASONS = frozenset({
    "model-invoked",       # Claude invokes it by name from a conversation.
    "vendored-reference",  # Third-party material kept as reference, not wired.
    "human-entry-point",   # A person runs it directly; no framework caller.
    "one-time",            # A migration already consumed; kept for the record.
})

# History is never rewritten — legacy logs keep their citations un-audited.
# Generated/vendored runtime dirs are not normative material (absent in CI
# checkouts, but present locally: venvs, graph output, linked .claude trees).
SCAN_EXCLUDE = ("docs/roadmaps/", "docs/sprints/", "node_modules/", ".git/",
                "venv_skillopt/", "venv/", "graphify-out/", ".claude/",
                "CHANGELOG.md", str(CONCORDANCE))

def loadable() -> list[Path]:
    """Every document a session can load: the ruleset, the protocols, the commands.

    A function rather than a module constant, because the globs used to run at
    import — before `main()` sets the framework root — so the list was built
    against whatever directory the caller was standing in and came back empty
    from anywhere but the repository root.

    Returns:
        list[Path]: Paths relative to the framework root.
    """
    return [Path("agents.md"), *Path("workflows").glob("*.md"), *Path("commands").glob("*.md")]


def loadable_text() -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in loadable())


def scan_files():
    """Yield every tracked markdown/Python file outside `SCAN_EXCLUDE`.

    Returns:
        Iterator[Path]: Markdown files first, then Python files — the same
            order the original two-pattern loop produced.
    """
    candidates = [*Path(".").glob("**/*.md"), *Path(".").glob("**/*.py")]
    for p in candidates:
        if any(x in str(p) for x in SCAN_EXCLUDE):
            continue
        yield p


def check_rules_reachable(corpus: str) -> list[str]:
    errors = []
    for rule in sorted(Path("rules").glob("*.md")):
        if rule.name not in corpus:
            errors.append(f"(a) rules/{rule.name} is unreachable — nothing loadable references it.")
    return errors


# Filenames GitHub defines, which this framework does not own and never ships
# in docs/standards/templates/. Any workflow describing repository setup has to
# name them, and doing so is not a dangling reference.
PLATFORM_TEMPLATES = frozenset({
    "PULL_REQUEST_TEMPLATE.md",
    "ISSUE_TEMPLATE.md",
})


def check_templates_exist(corpus: str) -> list[str]:
    """Every framework template cited in a loadable document must exist.

    Args:
        corpus: Concatenated text of agents.md and every workflow.

    Returns:
        list[str]: One error per template cited without a file behind it.
    """
    errors = []
    for name in set(re.findall(r"([A-Z][A-Z_]*_TEMPLATE\.md)", corpus)):
        if name in PLATFORM_TEMPLATES:
            continue
        if not (TEMPLATES_DIR / name).exists():
            errors.append(f"(b) {name} is cited but missing from {TEMPLATES_DIR}/.")
    return errors


def _rule_citation_errors(path: Path, mapped: set[str]) -> list[str]:
    """(c) Numbered `Rule NN` citations in one file, checked against `mapped`.

    Args:
        path: File to scan for `Rule NN` citations.
        mapped: Rule numbers documented in `rules/LEGACY_RULE_CONCORDANCE.md`.

    Returns:
        list[str]: One error per citation number absent from `mapped`.
    """
    text = path.read_text(encoding="utf-8", errors="ignore")
    errors = []
    # 41 covers 041/41.x style; normalize citations to their integer part.
    for num in re.findall(r"Rule[s]? 0*(\d+)(?:\.\d+)?", text):
        if num not in mapped:
            errors.append(f"(c) {path}: cites Rule {num}, not mapped in the concordance.")
    return errors


def check_rule_citations() -> list[str]:
    if not CONCORDANCE.exists():
        return [f"(c) {CONCORDANCE} missing — numbered citations cannot be resolved."]
    mapped = set(re.findall(r"\*\*Rule (\d+)", CONCORDANCE.read_text(encoding="utf-8")))
    errors: list[str] = []
    for p in scan_files():
        errors += _rule_citation_errors(p, mapped)
    return sorted(set(errors))


def load_exceptions() -> tuple[dict[str, str], list[str]]:
    """Read the declared-exception registry and validate it against the tree.

    Exceptions live in a data file rather than in each artifact's frontmatter
    because vendored skills cannot be edited at all (Skill Documentation Veto,
    rules/skills_and_integrations.md §3).

    Returns:
        tuple[dict[str, str], list[str]]: path -> reason, plus registry errors.
    """
    if not EXCEPTIONS_FILE.exists():
        return {}, [f"(d) {EXCEPTIONS_FILE} missing — RA-16 cannot be evaluated."]

    errors: list[str] = []
    exceptions: dict[str, str] = {}
    for entry in json.loads(EXCEPTIONS_FILE.read_text(encoding="utf-8"))["exceptions"]:
        path, reason = entry["path"], entry["reason"]
        exceptions[path] = reason
        if reason not in VALID_EXCEPTION_REASONS:
            errors.append(
                f"(d) {EXCEPTIONS_FILE}: '{path}' has reason '{reason}', "
                f"not one of {sorted(VALID_EXCEPTION_REASONS)}."
            )
        # A stale exemption is worse than no exemption: it silently excuses an
        # artifact that no longer exists, and hides the next one to take its name.
        if not Path(path).exists():
            errors.append(f"(d) {EXCEPTIONS_FILE}: '{path}' does not exist — stale exemption.")
    return exceptions, errors


def _module_names_imported_by(path: Path) -> set[str]:
    """AST-parse one Python file and return the module names it imports.

    Args:
        path: A first-party `.py` file.

    Returns:
        set[str]: Top-level import names; empty when the file fails to parse.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError:
        return set()
    names: set[str] = set()
    for node in ast.walk(tree):
        # Two sibling `if`s, not `if`/`elif`: `ast.Import` and `ast.ImportFrom`
        # are mutually exclusive types, so this is behaviourally identical —
        # and an `elif` nests one AST level deeper (a nested `If` in the first
        # `If`'s `orelse`), which is what pushed this unit past depth 3.
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        if isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[-1])
    return names


def imported_modules() -> set[str]:
    """Module names imported by any tracked `scripts/` or `hooks/` file.

    A script imported as a module has an invoker even though its filename is
    never written anywhere. Missing this is not theoretical: `merge_json.py`
    looked orphaned to a filename-only scan while `scripts/install.py`
    depends on it, and deleting it would have broken the bridge installer.

    Restored to its original two-tree scope (`ca70bfa`) after Sprint 052
    U19 widened it to also scan `skills/` and `tests/` — which let the
    scripts/hooks invocation loop below treat a script imported only by its
    own test file as invoked (F-2, Sprint 052 remediation round 1: a test
    importing production code does not invoke it in production). Skills
    scripts resolve through `_fixpoint_resolved_skill_scripts` instead, which
    deliberately excludes `tests/` importers for the same reason; test files
    resolve through `check_test_files_invoked`.
    """
    modules: set[str] = set()
    for path in [*Path("scripts").glob("*.py"), *Path("hooks").glob("*.py")]:
        modules |= _module_names_imported_by(path)
    return modules


def _makefile_target_recipe_lines(target: str) -> list[str]:
    """Tab-indented, non-comment recipe lines belonging to one Makefile target.

    Comments and blank lines interleaved in the recipe (this Makefile carries
    several) are skipped rather than treated as the end of the target — only
    a new `name:` rule header ends it. A tab-indented line whose content opens
    with `#` is a shell comment inside the recipe, not a command Make
    executes, so it is excluded too: a script merely mentioned in prose must
    not resolve as invoked (KI-048-1 D9 coordinator extension).

    Args:
        target: The target name, e.g. `"verify"`.

    Returns:
        list[str]: Recipe lines for that target, tab-stripped, in file order.
    """
    makefile = Path("Makefile")
    if not makefile.exists():
        return []
    lines: list[str] = []
    in_target = False
    for line in makefile.read_text(encoding="utf-8").splitlines():
        if re.match(rf"^{re.escape(target)}:", line):
            in_target = True
            continue
        if not in_target:
            continue
        if line.startswith("\t") and not line[1:].strip().startswith("#"):
            lines.append(line[1:])
            continue
        if line.startswith("\t"):
            continue
        if re.match(r"^[\w.-]+:", line):
            break
    return lines


def _makefile_recipe_lines() -> list[str]:
    """Tab-indented, non-comment recipe lines from every Makefile target.

    The "any target" counterpart of `_makefile_target_recipe_lines`: a skill
    script named in a recipe belonging to a target other than `verify` still
    resolves (KI-048-1 D9 coordinator extension).

    Returns:
        list[str]: Recipe lines, tab-stripped, in file order, across the
            whole file.
    """
    makefile = Path("Makefile")
    if not makefile.exists():
        return []
    return [
        line[1:] for line in makefile.read_text(encoding="utf-8").splitlines()
        if line.startswith("\t") and not line[1:].strip().startswith("#")
    ]


def _pytest_covers_tests_dir() -> bool:
    """Confirm the Makefile's `verify` target actually collects `tests/` via pytest.

    `tests/test_*.py` and `tests/conftest.py` are only treated as invoked by
    "make verify" (pytest's own filename-based collection) when this holds —
    the claim is derived from the Makefile recipe rather than hard-coded, so a
    future edit that drops the pytest step re-exposes the whole tree as
    unresolved instead of silently trusting a stale assumption (KI-048-1 D9).

    Returns:
        bool: True when the `verify:` recipe contains a line invoking
            `pytest` over a `tests/` argument.
    """
    return any(
        "pytest" in line and "tests/" in line
        for line in _makefile_target_recipe_lines("verify")
    )


def _skill_script_in_makefile(script: Path) -> bool:
    """(d) True when a Makefile recipe line, any target, names this script.

    Checks both the bare repo-relative form (`skills/<s>/scripts/f.py`) and
    the `$(AGENTS_DIR)/`-prefixed form the Makefile uses for recipes that run
    from the host root rather than the framework root. Reuses
    `_makefile_recipe_lines`, so a comment-only mention (top-level `#` line,
    or a `#`-led line inside a recipe) never counts (KI-048-1 D9 coordinator
    extension).

    Args:
        script: A `skills/<s>/scripts/*.py` path.

    Returns:
        bool: True when a real recipe line contains either form of the path.
    """
    key = str(script)
    prefixed = f"$(AGENTS_DIR)/{key}"
    return any(key in line or prefixed in line for line in _makefile_recipe_lines())


def _skill_doc_text(skill_dir: Path) -> str:
    """Concatenate a skill's SKILL.md and README.md text, if present.

    Args:
        skill_dir: Path to `skills/<name>`.

    Returns:
        str: Combined text of the two documents; empty when neither exists.
    """
    text = ""
    for doc_name in ("SKILL.md", "README.md"):
        doc = skill_dir / doc_name
        if doc.exists():
            text += doc.read_text(encoding="utf-8", errors="ignore")
    return text


def _token_present(text: str, token: str) -> bool:
    """True when `token` occurs in `text` as a whole token, not a substring.

    Bounded on both sides by a character outside `[\\w.-]`, so a script
    filename never matches inside an unrelated longer word — the defect that
    let a SKILL.md containing "environment" satisfy `env.py` (F-1a, Sprint
    052 remediation round 1). A path separator is a legitimate boundary, not
    part of the token: a longer, differently-rooted mention such as
    `.agents/skills/foo/scripts/env.py` still names `scripts/env.py` — only a
    word/dot/hyphen character fusing the token into a longer identifier
    (`environment` around `env`) must block the match.

    Args:
        text: Text to search.
        token: Literal token to find (e.g. a filename or relative path).

    Returns:
        bool: True when `token` appears with a non-token boundary on each side.
    """
    pattern = re.compile(r"(?<![\w.-])" + re.escape(token) + r"(?![\w.-])")
    return bool(pattern.search(text))


def _skill_doc_names_script(script: Path) -> bool:
    """(d)(a) True when the skill's own docs name this script as a whole token.

    Accepts the bare filename (`env.py`), the skill-relative path
    (`scripts/env.py`), or that same path written as a dotted module
    (`scripts.env`, as in `python -m scripts.env`) — never a bare-stem
    substring. The dotted form uses the same whole-token boundary rule as
    the other two: `scripts.env` names `scripts/env.py`, but neither
    `scripts.environment` nor `scripts.env_x` does, because the character
    immediately after `env` is a word character in both.

    Args:
        script: A `skills/<name>/scripts/*.py` path.

    Returns:
        bool: True when any token form is present in SKILL.md/README.md.
    """
    doc_text = _skill_doc_text(script.parent.parent)
    if not doc_text:
        return False
    tokens = (script.name, f"scripts/{script.name}", f"scripts.{script.stem}")
    return any(_token_present(doc_text, token) for token in tokens)


def _import_candidate_paths(importer: Path, node: ast.AST) -> set[Path]:
    """Sibling/dotted candidate paths for one import node, before existence check.

    `import name` and a single-component `from name import x` (no dot) are
    sibling-scoped: they resolve only inside `importer`'s own directory,
    matching the `sys.path.insert(0, ...)` pattern this codebase uses — the
    same reason a bare `import json` must never be credited with resolving
    `skills/foo/scripts/json.py` unless the importer lives in that exact
    directory (F-1c). A relative import (`from .env import x`, `from . import
    x`) is sibling-scoped for the same reason. A dotted `from scripts.env
    import x` is ALSO sibling-scoped when `importer` itself lives in a
    directory literally named `scripts` — the leading component then names
    that directory, not a real top-level package (F-1c's own example) — and
    resolves from the framework root only when it does not.

    Args:
        importer: The file the import statement lives in.
        node: An `ast.Import` or `ast.ImportFrom` node from that file.

    Returns:
        set[Path]: Candidate paths, not yet filtered by existence on disk.
    """
    if isinstance(node, ast.Import):
        return {importer.parent / f"{alias.name.split('.')[0]}.py" for alias in node.names}
    if not isinstance(node, ast.ImportFrom):
        return set()
    if node.module is None:
        return {importer.parent / f"{alias.name}.py" for alias in node.names}
    parts = node.module.split(".")
    if node.level == 0 and len(parts) > 1 and parts[0] != importer.parent.name:
        return {Path(*parts).with_suffix(".py")}
    return {importer.parent / f"{parts[-1]}.py"}


def _resolve_import_target(importer: Path, node: ast.AST) -> set[Path]:
    """Resolve one import node to first-party file paths that exist on disk.

    Args:
        importer: The file the import statement lives in.
        node: An `ast.Import` or `ast.ImportFrom` node from that file.

    Returns:
        set[Path]: Candidate paths from `_import_candidate_paths` that exist.
    """
    return {c for c in _import_candidate_paths(importer, node) if c.is_file()}


def _module_file_imports(path: Path) -> set[Path]:
    """AST-parse one file and resolve its imports to first-party file paths.

    Unlike `_module_names_imported_by` (bare import names, used for the
    original scripts/hooks invocation loop), this resolves each import to an
    actual path on disk, so a stdlib name never matches a same-named file
    outside the importer's own directory (F-1c, Sprint 052 remediation
    round 1).

    Args:
        path: A first-party `.py` file.

    Returns:
        set[Path]: Resolved import targets that exist in the tree.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError:
        return set()
    import_nodes = [n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]
    targets: set[Path] = set()
    for node in import_nodes:
        targets |= _resolve_import_target(path, node)
    return targets


def _skill_universe() -> list[Path]:
    """First-party files eligible to resolve a skills script via import.

    Deliberately excludes `tests/`: a test importing production code does
    not invoke it in production (F-2, Sprint 052 remediation round 1).

    Returns:
        list[Path]: Every `scripts/`, `hooks/` and `skills/*/scripts/` file.
    """
    return [
        *sorted(Path("scripts").glob("*.py")),
        *sorted(Path("hooks").glob("*.py")),
        *sorted(Path("skills").glob("*/scripts/*.py")),
    ]


def _skill_script_directly_resolved(path: Path, exceptions: dict[str, str]) -> bool:
    """Non-import resolution for one file in the skills import universe.

    A `scripts/`/`hooks/` file resolves directly only through its own
    `invoked_by:` — its broader (import-based) resolution is evaluated by
    `check_invocation_coverage`'s own loop, not duplicated here. A
    `skills/*/scripts/*.py` file also resolves via a Makefile recipe or its
    skill's own SKILL.md/README.md naming it as a whole token.

    Args:
        path: A `scripts/`, `hooks/` or `skills/*/scripts/` file.
        exceptions: Declared exception registry (path -> reason).

    Returns:
        bool: True when the file's own declaration resolves it without
            needing the import fixpoint.
    """
    if str(path) in exceptions:
        return True
    if "invoked_by:" in path.read_text(encoding="utf-8"):
        return True
    if "skills/" not in str(path):
        return False
    if _skill_script_in_makefile(path):
        return True
    return _skill_doc_names_script(path)


def _newly_resolved_via(
    importer: Path, graph: dict[Path, set[Path]], universe: set[Path], resolved: set[Path]
) -> set[Path]:
    """Targets of `importer` that enter the resolved set this fixpoint round.

    Args:
        importer: A file already in `resolved`.
        graph: Import edges — `importer` -> the first-party files it imports.
        universe: Every file eligible to be resolved.
        resolved: The resolved set so far (read-only here).

    Returns:
        set[Path]: New targets, inside `universe` and not yet in `resolved`.
    """
    return {t for t in graph.get(importer, set()) if t in universe and t not in resolved}


def _fixpoint_resolved_skill_scripts(exceptions: dict[str, str]) -> set[Path]:
    """Which skills-universe files are invoked, directly or via a resolved import chain.

    Seeds with every file that resolves directly (`invoked_by:`, a Makefile
    recipe, its skill's own docs, or a declared exception), then repeatedly
    adds a file once some already-resolved file imports it via a
    path-resolved edge (F-1b, Sprint 052 remediation round 1) — so two
    mutually-importing orphans, neither directly resolved, never resolve
    each other.

    Args:
        exceptions: Declared exception registry (path -> reason).

    Returns:
        set[Path]: Every universe file reachable from a directly-resolved seed.
    """
    universe = set(_skill_universe())
    graph = {path: _module_file_imports(path) for path in universe}
    resolved = {p for p in universe if _skill_script_directly_resolved(p, exceptions)}
    frontier = set(resolved)
    while frontier:
        next_frontier: set[Path] = set()
        for importer in frontier:
            newly = _newly_resolved_via(importer, graph, universe, resolved)
            resolved |= newly
            next_frontier |= newly
        frontier = next_frontier
    return resolved


def check_skill_scripts_invoked(exceptions: dict[str, str]) -> list[str]:
    """(d) skills/<s>/scripts/*.py resolves via docs, the Makefile, invoked_by,
    or a fixpoint-resolved import chain (D9, tightened F-1/F-2).

    A per-script rule, distinct from the existing per-skill-directory check.
    Resolution is computed once for the whole tree by
    `_fixpoint_resolved_skill_scripts`, so an importer only counts once it is
    itself resolved.

    Args:
        exceptions: Declared exception registry (path -> reason).

    Returns:
        list[str]: One error per script none of the resolutions cover.
    """
    resolved = _fixpoint_resolved_skill_scripts(exceptions)
    errors: list[str] = []
    for script in sorted(Path("skills").glob("*/scripts/*.py")):
        key = str(script)
        if key in exceptions or script.name == "__init__.py":
            continue
        if script in resolved:
            continue
        errors.append(
            f"(d) {key} is named by no SKILL.md/README.md/Makefile recipe, "
            f"imported by no resolved module, and declares no `invoked_by:`."
        )
    return errors


def check_test_files_invoked(exceptions: dict[str, str], modules: set[str]) -> list[str]:
    """(d) tests/*.py resolves via pytest collection, an import, or invoked_by (D9).

    `tests/test_*.py` and `tests/conftest.py` resolve to "make verify" when
    `_pytest_covers_tests_dir` confirms the recipe still runs pytest over that
    directory. Any other `tests/*.py` file (a helper or fixture module) must
    instead be imported by a resolved module or declare its own `invoked_by:`.

    Args:
        exceptions: Declared exception registry (path -> reason).
        modules: Module names imported by any tracked first-party Python file.

    Returns:
        list[str]: One error per test-tree file nothing invokes.
    """
    errors: list[str] = []
    pytest_covers = _pytest_covers_tests_dir()
    for path in sorted(Path("tests").glob("*.py")):
        key = str(path)
        if key in exceptions or path.name == "__init__.py":
            continue
        is_pytest_named = path.name == "conftest.py" or path.name.startswith("test_")
        if is_pytest_named and pytest_covers:
            continue
        if path.stem in modules:
            continue
        if "invoked_by:" in path.read_text(encoding="utf-8"):
            continue
        errors.append(
            f"(d) {key} matches no pytest collection pattern, is imported by "
            f"no resolved module, and declares no `invoked_by:`."
        )
    return errors


def check_invocation_coverage(corpus: str) -> list[str]:
    """(d) Every mechanism declares an invoker, or a typed exception (RA-16).

    Args:
        corpus: Concatenated text of agents.md, workflows and commands.

    Returns:
        list[str]: One error per mechanism nothing invokes and nothing excuses.
    """
    exceptions, errors = load_exceptions()
    governance = corpus + "\n".join(
        p.read_text(encoding="utf-8")
        for p in [*Path("rules").glob("*.md"), *Path("agents").glob("*.md")]
    )
    modules = imported_modules()

    # Workflows, scripts and hooks are framework-owned: they declare their own
    # invoker. Package markers (``__init__.py``) are not mechanisms.
    for path in [
        *sorted(Path("workflows").glob("*.md")),
        *sorted(Path("scripts").glob("*.py")),
        *sorted(Path("hooks").glob("*.py")),
    ]:
        key = str(path)
        if key in exceptions:
            continue
        if path.name == "__init__.py":
            continue
        if path.suffix == ".py" and path.stem in modules:
            continue
        if "invoked_by:" not in path.read_text(encoding="utf-8"):
            errors.append(
                f"(d) {key} declares no `invoked_by:` and has no exception — "
                f"a mechanism nothing calls is a regression, not a pending feature."
            )

    # Skills are not edited here: vendored SKILL.md files are under the
    # Documentation Veto, so a skill counts as invoked when governance names it.
    for skill in sorted(p for p in Path("skills").iterdir() if (p / "scripts").is_dir()):
        key = str(skill)
        if key in exceptions or skill.name in governance:
            continue
        errors.append(f"(d) {key} is an executable skill nothing invokes and nothing excuses.")

    errors += check_skill_scripts_invoked(exceptions)
    errors += check_test_files_invoked(exceptions, modules)
    errors += check_invoked_by_anchors()
    return errors


def github_heading_slug(heading: str) -> str:
    """Convert a Markdown heading's text to its GitHub anchor slug.

    Lowercases, drops every character that is not a word character, whitespace
    or a hyphen, then collapses whitespace runs to single hyphens.

    Args:
        heading: Heading text with the leading ``#`` markers already stripped.

    Returns:
        str: The slug, e.g. ``4-the-double-gate-review-protocol``.
    """
    slug = re.sub(r"[^\w\s-]", "", heading.strip().lower())
    return re.sub(r"\s+", "-", slug).strip("-")


def _heading_slug_matches(text: str, fragment: str) -> bool:
    """True when ``fragment`` equals the slug of some ``#`` heading in ``text``."""
    for line in text.splitlines():
        heading = re.match(r"^#{1,6}\s+(.*)$", line)
        if heading and github_heading_slug(heading.group(1)) == fragment:
            return True
    return False


def fragment_resolves(text: str, fragment: str) -> bool:
    """True when ``fragment`` names a reachable location inside ``text``.

    Accepts a GitHub heading slug, an explicit ``<a id=>`` / ``<a name=>``
    anchor, a backtick or parenthesised step-id token (`` `id` `` / ``(id)``)
    as used in this repository's workflow step tables, or a ``make``-style
    ``target:`` definition for non-Markdown invokers such as the ``Makefile``.

    Args:
        text: Full content of the resolved invoker file.
        fragment: The substring after ``#`` in an ``invoked_by:`` token.

    Returns:
        bool: True if any recognised anchor form matches ``fragment``.
    """
    if _heading_slug_matches(text, fragment):
        return True
    if re.search(rf'<a\s+(?:id|name)=["\']{re.escape(fragment)}["\']', text):
        return True
    if f"`{fragment}`" in text or f"({fragment})" in text:
        return True
    return bool(re.search(rf"^{re.escape(fragment)}\s*:", text, re.MULTILINE))


def resolve_invoker_path(raw: str) -> Path | None:
    """Resolve an ``invoked_by:`` path token to a file under the framework root.

    Tokens are written relative to the root (``rules/qa_and_testing.md``,
    ``Makefile``) or as a bare workflow/script basename (``close_workflow.md``).

    Args:
        raw: The path portion of an ``invoked_by:`` token, without ``#fragment``.

    Returns:
        Path | None: The resolved file, or None when no candidate exists.
    """
    candidates = [Path(raw)]
    if "/" not in raw:
        candidates += [Path("workflows") / raw, Path("scripts") / raw]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def _invoked_by_line(text: str) -> str:
    """Return the ``invoked_by:`` declaration line, or ``""`` when absent.

    Matches the line where ``invoked_by:`` opens the declaration (optionally
    behind a ``#`` comment marker or a ``\"\"\"`` docstring fence), so that a
    prose mention such as ``the ``invoked_by:`` token`` is not mistaken for it.
    """
    for line in text.splitlines():
        if re.match(r'\s*(?:"""|#)?\s*invoked_by:', line):
            return line
    return ""


def _anchor_errors_for(source: Path) -> list[str]:
    """Check the ``#fragment`` of every ``invoked_by:`` token in one file.

    Args:
        source: A workflow, script or hook whose ``invoked_by:`` line may carry
            ``path#fragment`` tokens.

    Returns:
        list[str]: One error per token whose path or fragment does not resolve.
    """
    line = _invoked_by_line(source.read_text(encoding="utf-8"))
    errors: list[str] = []
    last_path: str | None = None
    for match in INVOKED_TOKEN_RE.finditer(line):
        last_path = match.group(1) or last_path
        target = resolve_invoker_path(last_path) if last_path else None
        if target is None:
            errors.append(
                f"(d) {source}: invoked_by token `{match.group(0)}` — "
                f"path `{last_path}` does not resolve to a file."
            )
            continue
        if not fragment_resolves(target.read_text(encoding="utf-8", errors="ignore"), match.group(2)):
            errors.append(
                f"(d) {source}: invoked_by token `{match.group(0)}` — `#{match.group(2)}` "
                f"is not a heading, anchor or step-id in {target}."
            )
    return errors


def check_invoked_by_anchors() -> list[str]:
    """(d) Resolve the ``#fragment`` suffix of every ``invoked_by:`` token.

    An unresolvable fragment takes the same failure path as an unresolvable
    filename (RA-16). A token with no ``#`` is not inspected here.

    Returns:
        list[str]: One error per unresolvable ``invoked_by:`` path or fragment.
    """
    errors: list[str] = []
    for path in [
        *sorted(Path("workflows").glob("*.md")),
        *sorted(Path("scripts").glob("*.py")),
        *sorted(Path("hooks").glob("*.py")),
        *sorted(Path("skills").glob("*/scripts/*.py")),
        *sorted(Path("tests").glob("*.py")),
    ]:
        errors += _anchor_errors_for(path)
    return errors


def check_rule_triggers_sync() -> list[str]:
    """(e) config/rule_triggers.json must mirror rules/*.md exactly."""
    triggers_path = Path("config/rule_triggers.json")
    if not triggers_path.exists():
        return ["(e) config/rule_triggers.json is missing."]
    data = json.loads(triggers_path.read_text(encoding="utf-8"))
    declared = {entry["path"] for entry in data.get("rules", [])}
    on_disk = {f"rules/{p.name}" for p in sorted(Path("rules").glob("*.md"))}
    errors: list[str] = []
    missing = on_disk - declared
    extra = declared - on_disk
    for path in sorted(missing):
        errors.append(f"(e) rules/{Path(path).name} has no entry in config/rule_triggers.json.")
    for path in sorted(extra):
        errors.append(f"(e) config/rule_triggers.json lists {path}, which is not in rules/.")
    return errors


def resolve_cited_path(cited: str) -> Path | None:
    """Map a citation path to a real file under the framework root.

    Bare basenames (``qa_agent.md``) resolve under ``agents/`` when unique there;
    otherwise only an exact relative path that exists is accepted. Missing files
    are skipped — check (f) is a **range** gate, not an existence gate (J6).
    """
    direct = Path(cited)
    if direct.is_file():
        return direct
    matches = list(Path("agents").glob(cited)) if "/" not in cited else []
    if len(matches) == 1 and matches[0].is_file():
        return matches[0]
    return None


def _line_count(target: Path) -> int | None:
    """Count lines in `target`.

    Args:
        target: File to count.

    Returns:
        int | None: Line count, or None on an OS-level read failure.
    """
    try:
        return sum(1 for _ in target.open(encoding="utf-8", errors="ignore"))
    except OSError:
        return None


def _out_of_range_citations(path: Path) -> list[str]:
    """(f) ``path:line`` citations in one living doc, checked against file length.

    Args:
        path: A markdown file under `FILE_LINE_CORPUS`.

    Returns:
        list[str]: One error per citation whose line number falls outside the
            cited file's range.
    """
    text = path.read_text(encoding="utf-8", errors="ignore")
    errors: list[str] = []
    for match in FILE_LINE_RE.finditer(text):
        cited, line_s = match.group(1), match.group(2)
        line_no = int(line_s)
        target = resolve_cited_path(cited)
        if target is None:
            continue
        n_lines = _line_count(target)
        if n_lines is None:
            continue
        if line_no < 1 or line_no > n_lines:
            errors.append(
                f"(f) {path}: cites `{cited}:{line_no}` but "
                f"{target} has {n_lines} lines."
            )
    return errors


def check_file_line_citations() -> list[str]:
    """(f) ``path:line`` citations in living docs must be inside the file.

    Scans only ``docs/guides``, ``docs/decisions``, and ``docs/audits``. Does not
    catch wrong-but-in-range line numbers — that mitigation is T5 (figure +
    command), not this check.
    """
    errors: list[str] = []
    for root in FILE_LINE_CORPUS:
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.md")):
            errors += _out_of_range_citations(path)
    return sorted(set(errors))


def parse_agent_frontmatter_fields(text: str) -> dict[str, str]:
    """Return ``model`` / ``tier`` from the leading ``---`` YAML fence, if any."""
    match = FRONTMATTER_RE.match(text)
    if match is None:
        return {}
    return dict(AGENT_TIER_MODEL_RE.findall(match.group(1)))


def check_agents_model_tier_map() -> list[str]:
    """(g) ``agents/*.md`` frontmatter ``model:`` must match the Claude tier map.

    Plan 035 named this check ``(f)``; letter ``(f)`` is already
    ``check_file_line_citations`` (Sprint 029). Implemented as ``(g)``.
    Claude Code side only (D15) — Cursor cells are not checked.
    """
    if not MODEL_TIERS_FILE.is_file():
        return [f"(g) {MODEL_TIERS_FILE} is missing."]
    tiers = json.loads(MODEL_TIERS_FILE.read_text(encoding="utf-8")).get("tiers", {})
    errors: list[str] = []
    agents_dir = Path("agents")
    if not agents_dir.is_dir():
        return errors
    for path in sorted(agents_dir.glob("*.md")):
        fields = parse_agent_frontmatter_fields(
            path.read_text(encoding="utf-8", errors="ignore")
        )
        tier = fields.get("tier")
        model = fields.get("model")
        if tier is None and model is None:
            continue
        if tier is not None and model is None:
            errors.append(
                f"(g) {path}: has tier `{tier}` but no model: "
                f"(required when tier is present)."
            )
            continue
        if tier is None:
            # model without tier — skip (both required only when tier is set).
            continue
        spec = tiers.get(tier)
        if spec is None:
            errors.append(
                f"(g) {path}: unknown tier `{tier}` "
                f"(not in {MODEL_TIERS_FILE})."
            )
            continue
        expected = spec.get("claude_code", {}).get("model")
        if expected is None:
            errors.append(
                f"(g) {path}: tier `{tier}` has no claude_code.model in "
                f"{MODEL_TIERS_FILE}."
            )
            continue
        if model != expected:
            errors.append(
                f"(g) {path}: frontmatter model `{model}` != map `{expected}` "
                f"for tier `{tier}`."
            )
    return errors


def main() -> int:
    # Framework-scoped: every path below is this repository's. See
    # `scripts/_root.py` — the cwd is set once so the messages stay relative and
    # a path added later cannot silently reintroduce the cwd dependency.
    os.chdir(agents_root())

    corpus = loadable_text()
    errors = (
        check_rules_reachable(corpus)
        + check_templates_exist(corpus)
        + check_rule_citations()
        + check_invocation_coverage(corpus)
        + check_rule_triggers_sync()
        + check_file_line_citations()
        + check_agents_model_tier_map()
    )
    if errors:
        for e in errors:
            print(f"❌ {e}", file=sys.stderr)
        return 2
    print(
        "✅ Reference integrity OK — rules reachable, templates exist, "
        "citations resolve, every mechanism has an invoker whose "
        "invoked_by anchor fragments resolve, "
        "living file:line citations in range, "
        "profile model↔tier map."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
