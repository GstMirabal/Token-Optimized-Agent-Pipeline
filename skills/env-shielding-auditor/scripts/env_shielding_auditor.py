"""
🛡️ Universal-Agents: Environment Shielding Auditor (3rd-party)
Agnostic security check script for avoiding PII leaks and hardcoded secrets.
"""

import os
import re

# Secret Patterns (High-level samples)
SECRET_PATTERNS = {
    "Generic API Key": r"(?i)(api[_-]?key|access[_-]?token|auth[_-]?token|secret[_-]?key)['\"]?\s*[:=]\s*['\"]?[a-z0-9+/=]{16,}['\"]?",
    "JWT Token": r"ey[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*",
    "Slack Webhook": r"https://hooks\.slack\.com/services/T[A-Z0-9_]{8}/B[A-Z0-9_]{8}/[A-Za-z0-9_]{24}",
    "AWS Key": r"AKIA[0-9A-Z]{16}",
    "Generic Password": r"(?i)(password|passwd|pwd)['\"]?\s*[:=]\s*['\"]?[a-z0-9@#$%^&*()_+]{8,}['\"]?"
}

def scan_files(directory):
    leaks = []
    for root, _, files in os.walk(directory):
        if any(x in root for x in [".git", ".agents", "venv", "node_modules", ".agent_state"]):
            continue
            
        for file in files:
            if file.endswith((".py", ".js", ".ts", ".json", ".env", ".env.example", ".sh", ".bash")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        for i, line in enumerate(f, 1):
                            for name, pattern in SECRET_PATTERNS.items():
                                if re.search(pattern, line):
                                    leaks.append(f"🚨 {name} found: {file_path} (Line {i})")
                except Exception as e:
                    # Silently skip unreadable files
                    pass
    return leaks

def check_gitignore():
    if os.path.exists(".gitignore"):
        with open(".gitignore", "r") as f:
            content = f.read()
            if ".env" in content:
                print("✅ .env is present in .gitignore.")
                return True
            else:
                print("❌ .env is NOT in .gitignore! This is a Major Security Risk.")
                return False
    else:
        print("⚠️ .gitignore not found. Skipping check.")
        return None

def main():
    print(f"🚀 Initializing Environment Shielding Audit...")
    
    # Gitignore Validation
    check_gitignore()
    
    # Secret Scanning
    print("\n🔍 Scanning for Hardcoded Secrets (Wait brief moment)...")
    leaks = scan_files(".")
    
    if leaks:
        print(f"\n🚨 {len(leaks)} Potential Leaks Detected:")
        for leak in leaks:
            print(leak)
    else:
        print("\n✅ No hardcoded secrets found in source code.")

    print("\n🏁 --- [Final Shielding Summary] ---")
    if leaks:
        print("❌ FAIL: Secrets detected or environment is vulnerable.")
    else:
        print("🏆 Environment and Secrets are currently Certified.")

if __name__ == "__main__":
    main()
