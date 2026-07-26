import os
import sys
import json
import subprocess
from pathlib import Path

# 🧪 Hybrid Coverage Auditor (Project & Repo Mode)
# Version: 2.0.0

MIN_DOC_COVERAGE = 100.0 # Repository requirement
MIN_CODE_COVERAGE = 90.0 # Project requirement

def detect_context():
    if os.path.exists("backend") or os.path.exists("manage.py"):
        return "PROJECT"
    return "REPO"

def audit_code_coverage():
    print("🧪 [COVERAGE AUDITOR] STARTING PROJECT CODE AUDIT...")
    try:
        subprocess.run(["pytest", "--cov=backend/apps", "--cov-report=json"], capture_output=True)
        if os.path.exists("coverage.json"):
            with open("coverage.json") as f:
                data = json.load(f)
            total_pct = data.get("totals", {}).get("percent_covered", 0.0)
            print(f"📈 CODE COVERAGE: {total_pct}%")
            return total_pct >= MIN_CODE_COVERAGE
    except Exception as e:
        print(f"🚨 Error during pytest: {e}")
    return False

def audit_doc_coverage():
    print("🧪 [COVERAGE AUDITOR] STARTING REPO DOCUMENTARY AUDIT...")
    manifest_path = Path("skills/manifest_skills.json")
    if not manifest_path.exists():
        print("🚨 Error: manifest_skills.json not found.")
        return 0.0

    with open(manifest_path, "r") as f:
        manifest = json.load(f)
    
    total_skills = len(manifest["skills"])
    compliant_skills = 0
    
    for skill in manifest["skills"]:
        skill_path = Path("skills") / skill["path"]
        # Three-File Skill Standard: README, SKILL, scripts/
        has_readme = (skill_path / "README.md").exists()
        has_skill_md = (skill_path / "SKILL.md").exists()
        has_scripts = (skill_path / "scripts").is_dir()
        
        if has_readme and has_skill_md and has_scripts:
            compliant_skills += 1
        else:
            missing = []
            if not has_readme: missing.append("README.md")
            if not has_skill_md: missing.append("SKILL.md")
            if not has_scripts: missing.append("scripts/")
            print(f"❌ [DOCUMENTATION GAP]: Skill '{skill['name']}' is missing: {', '.join(missing)}")

    coverage = (compliant_skills / total_skills) * 100 if total_skills > 0 else 100
    print(f"📊 DOCUMENTARY COVERAGE: {coverage:.2f}% ({compliant_skills}/{total_skills} skills compliant)")
    return coverage >= MIN_DOC_COVERAGE

def main():
    context = detect_context()
    if context == "PROJECT":
        success = audit_code_coverage()
        target = MIN_CODE_COVERAGE
    else:
        success = audit_doc_coverage()
        target = MIN_DOC_COVERAGE
        
    if not success:
        print(f"🚨 [AUDIT REJECTED]: Coverage is below {target}%.")
        sys.exit(1)
    
    print("✨ [AUDIT PASSED]: Coverage requirements met.")
    sys.exit(0)

if __name__ == "__main__":
    main()
