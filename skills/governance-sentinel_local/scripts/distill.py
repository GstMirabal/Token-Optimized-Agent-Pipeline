import json
from pathlib import Path
from collections import Counter
from datetime import datetime

# Paths
ROOT = Path(__file__).parent.parent.parent.parent.parent
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
    from collections import Counter
    patterns = Counter([(d['hook'], d['type']) for d in data])
    return patterns

def generate_proposal(patterns):
    header = f"# Governance Heuristic Pulse ({datetime.now().strftime('%Y-%m-%d')})\n\n"
    header += "This report identifies recurrent friction points detected by Matrix hooks. Patterns exceeding the threshold are promoted to Formal Clauses.\n\n"
    
    body = "## Frequency Analysis\n\n"
    body += "| Hook | Error Type | Frequency | Status |\n"
    body += "| :--- | :--- | :--- | :--- |\n"
    
    clauses = "\n## Formal Clauses (Promoted)\n\n"
    proposals = "\n## Proposed Amendments (Jurisprudence)\n\n"
    
    proposed_count = 0
    clause_count = 0
    
    for (hook, err_type), count in patterns.items():
        promoted = count >= PROMOTION_THRESHOLD
        threshold_met = count >= 3
        status = "🔴 PROMOTED" if promoted else ("🟡 ACTION REQUIRED" if threshold_met else "⚪ MONITORING")
        body += f"| `{hook}` | `{err_type}` | {count} | {status} |\n"
        
        if promoted:
            clause_count += 1
            # Simple heuristic mapping for now
            rule_text = "The agent MUST trigger a Manual Correction Alert and stop execution until the environment is restored (Manual Task)." if err_type == "ENVIRONMENT_VIOLATION" else "The agent MUST perform a structural audit before commit."
            
            clauses += f"### Clause J-{clause_count:02d}: {err_type}\n"
            clauses += f"- **Rule**: {rule_text}\n"
            clauses += f"- **Source**: `{hook}`\n"
            clauses += f"- **Frequency**: {count} occurrences\n"
            clauses += "- **Status**: `PENDING_PROMOTION`\n\n"
            
        elif threshold_met:
            proposed_count += 1
            proposals += f"### Proposal P-{proposed_count:02d}: {err_type} Mitigation\n"
            proposals += f"**Detected in**: `{hook}`\n"
            proposals += f"**Reasoning**: High frequency of this violation ({count} occurrences) suggests a need for automated remediation or constitutional clarification.\n"
            proposals += "**Proposed Clause**: *Pending heuristic distillation logic refinement.*\n\n"
            
    if clause_count == 0:
        clauses += "_No clauses have reached the promotion threshold yet._\n"
    if proposed_count == 0:
        proposals += "_No critical patterns detected. Matrix health is nominal._\n"
        
    return header + body + clauses + proposals

def main():
    print("🧠 [GOVERNANCE SENTINEL] Distilling Matrix Telemetry...")
    data = load_telemetry()
    
    if not data:
        print("✅ [GOVERNANCE SENTINEL] No telemetry found. Matrix is silent.")
        return
        
    patterns = analyze_patterns(data)
    report = generate_proposal(patterns)
    
    with open(OUTPUT_PATH, "w") as f:
        f.write(report)
        
    print(f"📄 [GOVERNANCE SENTINEL] Heuristic Pulse updated at {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
