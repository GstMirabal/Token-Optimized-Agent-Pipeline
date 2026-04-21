import re
from pathlib import Path
import json

# Paths
ROOT = Path(__file__).parent.parent.parent.parent.parent
AGENTS_MD = ROOT / "agents.md"
PROPOSALS_MD = ROOT / "memory/telemetry/proposals.md"
TELEMETRY_JSON = ROOT / "memory/telemetry/raw_errors.json"

def parse_clauses():
    if not PROPOSALS_MD.exists():
        return []
        
    content = PROPOSALS_MD.read_text()
    # Regex to find clauses: ### Clause J-XX: [TYPE]\n- **Rule**: [RULE] ...
    pattern = r"### (Clause J-\d+: .+?)\n- \*\*Rule\*\*: (.+?)\n- \*\*Source\*\*: (.+?)\n"
    matches = re.finditer(pattern, content)
    
    clauses = []
    for m in matches:
        clauses.append({
            "title": m.group(1),
            "rule": m.group(2),
            "source": m.group(3)
        })
    return clauses

def apply_to_agents_md(clauses):
    if not clauses:
        print("⚪ [JURISPRUDENCE] No clauses found for promotion.")
        return False
        
    content = AGENTS_MD.read_text()
    
    applied = 0
    for c in clauses:
        # Check if already present
        if c['title'] in content:
            continue
            
        # Format the entry
        entry = f"\n#### {c['title']}\n"
        entry += f"- **Heuristic Rule**: {c['rule']}\n"
        entry += f"- **Original Source**: {c['source']}\n"
        entry += f"- **Vetted Date**: {Path(PROPOSALS_MD).stat().st_mtime}\n"
        
        # Append to the end of the file (Section 7)
        content += entry
        applied += 1
        
    if applied > 0:
        AGENTS_MD.write_text(content)
        print(f"✅ [JURISPRUDENCE] Applied {applied} new amendments to agents.md.")
        return True
    else:
        print("⚪ [JURISPRUDENCE] All identified clauses are already constitutionalized.")
        return False

def reset_telemetry():
    """Rule 79: Definitive Amnesia of the logs after constitutionalization."""
    if TELEMETRY_JSON.exists():
        TELEMETRY_JSON.write_text("[]")
        print("🧹 [JURISPRUDENCE] Telemetry logs cleared.")
    if PROPOSALS_MD.exists():
        # Clear the proposals to prevent re-application
        PROPOSALS_MD.write_text("# Governance Heuristic Pulse\n\n_Telemetry reset after jurisprudence application._")

def main():
    print("⚖️ [JURISPRUDENCE] Initiating Constitutional Amendment Cycle...")
    clauses = parse_clauses()
    success = apply_to_agents_md(clauses)
    
    if success:
        reset_telemetry()
    else:
        print("⚖️ [JURISPRUDENCE] No actions taken.")

if __name__ == "__main__":
    main()
