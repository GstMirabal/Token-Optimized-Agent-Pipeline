import json
from collections import Counter
from datetime import datetime
from pathlib import Path

# This file lives at <AGENTS_ROOT>/skills/compliance-checker/scripts/distill.py,
# so 4 parents reach AGENTS_ROOT. Telemetry, though, lives at the *host's* root,
# not inside .agents/ (submodule_purity — .agents/memory/ must never exist as a
# host artifact). In nucleus mode AGENTS_ROOT already *is* the host (real .git
# dir, same detection install.py/render_readme.py already use); in a
# normal host install, AGENTS_ROOT is the `.agents/` submodule and the real
# root is one level up. The previous unconditional 4-parent count always
# landed inside .agents/ for a host install, so this script had never once
# found real telemetry on any host.
AGENTS_ROOT = Path(__file__).resolve().parent.parent.parent.parent
ROOT = AGENTS_ROOT if (AGENTS_ROOT / ".git").is_dir() else AGENTS_ROOT.parent
TELEMETRY_PATH = ROOT / "memory/telemetry/raw_errors.json"
OUTPUT_PATH = ROOT / "memory/telemetry/proposals.md"

def load_telemetry():
    if not TELEMETRY_PATH.exists():
        return []
    with open(TELEMETRY_PATH, "r") as f:
        return json.load(f)

PROMOTION_THRESHOLD = 5

def analyze_patterns(data):
    """Identifies recurring friction points."""
    patterns = Counter([(d['hook'], d['type']) for d in data])
    return patterns

def _status_label(promoted: bool, threshold_met: bool) -> str:
    """Renders the frequency-table status marker for one pattern.

    Args:
        promoted: Whether the pattern count reached PROMOTION_THRESHOLD.
        threshold_met: Whether the pattern count reached the 3-occurrence floor.

    Returns:
        The emoji-prefixed status label for the frequency table row.
    """
    if promoted:
        return "🔴 PROMOTED"
    if threshold_met:
        return "🟡 ACTION REQUIRED"
    return "⚪ MONITORING"


def _build_clause(clause_count: int, hook: str, err_type: str, count: int) -> str:
    """Builds the Markdown block for one promoted Formal Clause.

    Args:
        clause_count: The 1-based sequence number of this clause.
        hook: The hook identifier that produced the pattern.
        err_type: The error type of the pattern.
        count: The occurrence count of the pattern.

    Returns:
        The Markdown block describing the promoted clause.
    """
    # Simple heuristic mapping for now
    rule_text = (
        "The agent MUST trigger a Manual Correction Alert and stop execution "
        "until the environment is restored (Manual Task)."
        if err_type == "ENVIRONMENT_VIOLATION"
        else "The agent MUST perform a structural audit before commit."
    )
    return (
        f"### Clause RA-{clause_count:02d}: {err_type}\n"
        f"- **Rule**: {rule_text}\n"
        f"- **Source**: `{hook}`\n"
        f"- **Frequency**: {count} occurrences\n"
        "- **Status**: `PENDING_PROMOTION`\n\n"
    )


def _build_proposal_entry(proposed_count: int, hook: str, err_type: str, count: int) -> str:
    """Builds the Markdown block for one proposed Rule Amendment.

    Args:
        proposed_count: The 1-based sequence number of this proposal.
        hook: The hook identifier that produced the pattern.
        err_type: The error type of the pattern.
        count: The occurrence count of the pattern.

    Returns:
        The Markdown block describing the proposed amendment.
    """
    return (
        f"### Proposal P-{proposed_count:02d}: {err_type} Mitigation\n"
        f"**Detected in**: `{hook}`\n"
        f"**Reasoning**: High frequency of this violation ({count} occurrences) "
        "suggests a need for automated remediation or governance clarification.\n"
        "**Proposed Clause**: *Pending heuristic distillation logic refinement.*\n\n"
    )


def _classify_pattern(
    hook: str, err_type: str, count: int, clause_count: int, proposed_count: int
) -> tuple[str, str, int, int]:
    """Classifies one pattern and renders its Markdown contribution.

    Args:
        hook: The hook identifier that produced the pattern.
        err_type: The error type of the pattern.
        count: The occurrence count of the pattern.
        clause_count: The number of clauses already promoted.
        proposed_count: The number of proposals already recorded.

    Returns:
        A 4-tuple of (clause_markdown, proposal_markdown, new_clause_count,
        new_proposed_count); at most one of the two Markdown strings is
        non-empty, matching the original if/elif exclusivity.
    """
    promoted = count >= PROMOTION_THRESHOLD
    threshold_met = count >= 3
    if promoted:
        clause_count += 1
        return _build_clause(clause_count, hook, err_type, count), "", clause_count, proposed_count
    if threshold_met:
        proposed_count += 1
        return "", _build_proposal_entry(proposed_count, hook, err_type, count), clause_count, proposed_count
    return "", "", clause_count, proposed_count


def generate_proposal(patterns):
    header = f"# Governance Heuristic Pulse ({datetime.now().astimezone().strftime('%Y-%m-%d')})\n\n"
    header += "This report identifies recurrent friction points detected by pipeline hooks. Patterns exceeding the threshold are promoted to Formal Clauses.\n\n"

    body = "## Frequency Analysis\n\n"
    body += "| Hook | Error Type | Frequency | Status |\n"
    body += "| :--- | :--- | :--- | :--- |\n"

    clauses = "\n## Formal Clauses (Promoted)\n\n"
    proposals = "\n## Proposed Amendments (Rule Amendments)\n\n"

    proposed_count = 0
    clause_count = 0

    for (hook, err_type), count in patterns.items():
        promoted = count >= PROMOTION_THRESHOLD
        threshold_met = count >= 3
        body += f"| `{hook}` | `{err_type}` | {count} | {_status_label(promoted, threshold_met)} |\n"

        clause_md, proposal_md, clause_count, proposed_count = _classify_pattern(
            hook, err_type, count, clause_count, proposed_count
        )
        clauses += clause_md
        proposals += proposal_md

    if clause_count == 0:
        clauses += "_No clauses have reached the promotion threshold yet._\n"
    if proposed_count == 0:
        proposals += "_No critical patterns detected. Pipeline health is nominal._\n"

    return header + body + clauses + proposals

def main():
    print("🧠 [COMPLIANCE CHECKER] Distilling Pipeline Telemetry...")
    data = load_telemetry()

    if not data:
        print("✅ [COMPLIANCE CHECKER] No telemetry found. Pipeline is silent.")
        return

    patterns = analyze_patterns(data)
    report = generate_proposal(patterns)

    with open(OUTPUT_PATH, "w") as f:
        f.write(report)

    print(f"📄 [COMPLIANCE CHECKER] Heuristic Pulse updated at {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
