<a name="readme-top"></a>

<h3 align="center">Omni Context Minimizer</h3>

<p align="center">
  Extracts the structural skeleton (AST) of any codebase to avoid massive context bloating.
</p>

## About The Project

The **Omni Context Minimizer** is the pipeline's core efficiency tool. It solves the **Context Bloat** problem by extracting the structural skeleton of large source files (over 200 lines) through an **Abstract Syntax Tree (AST)** approach. This lets the AI understand project topology without consuming a massive amount of tokens.

**Key Features:**
*   **AST Analysis:** Extracts function, class, and method signatures without the weight of the code body.
*   **Token Optimization:** Cuts token consumption by 70-90% on large files.
*   **Cross-Language Support:** Extensible engine for multiple languages (native Python support).

### Built With

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![AST](https://img.shields.io/badge/AST-logic-lightgrey)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Prerequisites

*   **Python 3.x**: The main extraction engine (`omni_minimizer.py`) requires a working Python interpreter (Rule 37).

### Installation & Configuration

1. **Clone/Submodule**
   This skill is part of the core skill library at `.agents/skills/omni-context-minimizer/`.

2. **Setup**
   No heavy external dependencies required — it uses Python's standard `ast` library.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

This skill is triggered automatically by the **Token-Saver Auditor** whenever a file exceeds the 200-line threshold. It can also be invoked manually for quick exploration:

```bash
# Manual invocation to extract the skeleton of a large file
python .agents/skills/omni-context-minimizer/scripts/omni_minimizer.py path/to/file.py
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing

1. Fork the Project
2. Create your Feature Branch
3. Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>
