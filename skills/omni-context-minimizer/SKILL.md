---
name: omni-context-minimizer
description: Use this Skill imperatively BEFORE reading any code file containing more than 200 lines. This script extracts and returns a tactical skeleton (Imports, Class Names, and Function Signatures) discarding all internal logic, thus preventing massive context window consumption. Works for NodeJS, Python, Go, Rust, and Java.
---

# 🪙 Skill: Omni Context Minimizer

## ⚠️ When to Trigger this Skill?
As a Subagent, you are PROHIBITED from reading massive code files (`.js`, `.py`, `.go`, `.ts`) with a full-file `Read` without first going through this minimizer, unless you already know exactly the line number or range you are going to inspect.

If you are tasked to "Analyze how the API is structured" or "Review the large `views.py` file":
1.  YOU CANNOT LOAD THE ENTIRE FILE INTO YOUR MEMORY.
2.  EXECUTE THIS SKILL IMMEDIATELY.

## 🛠️ How it Works (Instructions)
This repository contains a Python script called `omni_minimizer.py` in the `scripts/` folder. This script scrutinizes the lexical DOM of the target file and returns only the lines that declare Functions, Classes, or Imports via the terminal.

**Step 1:** Locate the absolute path of the heavy file you need to analyze (e.g., `/path/to/my_project/src/app.js`).

**Step 2:** Run the minimizer passing that path as an argument (the Python script must be executed from the Skill's path in the submodule):
```bash
python .agents/skills/omni-context-minimizer/scripts/omni_minimizer.py /path/to/heavy/file
```

**Step 3:** The console will return the skeleton. For example:
```text
Line 1: import express from 'express';
Line 4: const app = express();
Line 10: export const loginController = async (req, res) => {
Line 45: class DatabaseService {
...
--- [OPTIMIZATION]: The file was reduced to 8 lines of pure structure. ---
```

**Step 4:** Now that you have the "map", **if you decide you need to see how the logic of `loginController` at line 10 works**, you can use a targeted `Read` (offset/limit) or `ripgrep` focusing your shot STRICTLY on line 10, saving all the remaining context.

## 🔴 Token-Saver Authorization
If you are sending an `implementation_plan.md` to the Orchestrator and it includes the heuristic scanning of an entire `/src` folder, you **MUST** specify in your MD: *"The `omni-context-minimizer` will be used to map the 5 base files, preventing context drowning"*.
Otherwise, the Token-Saver Auditor will reject the plan.
