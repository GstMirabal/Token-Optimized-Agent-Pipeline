"""
🛡️ Universal-Agents: JS/TS Standardizer (Native)
Agnostic health-check script for JS/TS repositories to ensure framework compliance.
"""

import os
import json
import subprocess

def check_jsdoc(directory):
    print("🔍 Auditing JSDoc Compliance...")
    # Basic heuristic: check if functions in .js/.ts files have @param or @returns
    jsdoc_found = False
    for root, _, files in os.walk(directory):
        if any(x in root for x in ["node_modules", ".git", ".agents", "dist", "build"]):
            continue
        for file in files:
            if file.endswith((".js", ".ts")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        if "@param" in content or "@returns" in content:
                            jsdoc_found = True
                            print(f"✅ Found JSDoc in: {file}")
                except:
                    pass
    return jsdoc_found

def main():
    root_path = os.getcwd()
    print(f"🚀 Initializing JS/TS Standardization Audit...")

    # Ecosystem Discovery
    ecosystem = {
        "ESLint": [".eslintrc", ".eslintrc.json", ".eslintrc.js", "eslint.config.js"],
        "Prettier": [".prettierrc", "prettier.config.js"],
        "TypeScript": ["tsconfig.json"],
        "Biome": ["biome.json"]
    }

    found = []
    for name, files in ecosystem.items():
        if any(os.path.exists(f) for f in files):
            found.append(name)
    
    print(f"📁 Metadata Discovery: {found}")

    # JSDoc Check (Governance Rule)
    has_jsdoc = check_jsdoc(".")
    
    print("\n🏁 --- [Final JS/TS Summary] ---")
    if found:
        print(f"✅ Tools configured: {', '.join(found)}")
    else:
        print("⚠️ No standard JS linting tools found.")

    if has_jsdoc:
        print("✅ JSDoc implementation detected (Compliance OK).")
    else:
        print("❌ FAIL: No JSDoc patterns found. Governance Phase 1 requires JSDoc/@param usage.")

if __name__ == "__main__":
    main()
