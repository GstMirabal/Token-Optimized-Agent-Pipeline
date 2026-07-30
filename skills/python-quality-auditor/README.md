<a name="readme-top"></a>

<h3 align="center">Python Quality Auditor</h3>

<p align="center">
  Agnostic Python health-check (Ruff, Mypy, Bandit) to ensure compliance with framework standards.
<br /><br />
<a href="https://github.com/GstMirabal/Token-Optimized-Agent-Pipeline"><strong>Explore the docs »</strong></a>
<br />
·
<a href="https://github.com/GstMirabal/Token-Optimized-Agent-Pipeline/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
·
<a href="https://github.com/GstMirabal/Token-Optimized-Agent-Pipeline/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
</p>

## About The Project

The **Python Quality Auditor** is the health-certification tool for Python projects inside the pipeline. It provides an agnostic, incremental audit through modern tooling (Ruff for linting/formatting, Mypy for static typing, and Bandit for security), ensuring code meets the production standards of **Rule 35**.

**Key Features:**
*   **Agnostic Linting:** Ruff integration unifying 10+ linting tools into one fast run.
*   **Type Certification:** Mypy type auditing to prevent runtime logic errors.
*   **Security Scanning:** Bandit-based detection of known vulnerabilities in packages and source code.

### Built With

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Ruff](https://img.shields.io/badge/Ruff-Linter-black)
![Mypy](https://img.shields.io/badge/Mypy-Types-orange)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Prerequisites

*   **Python 3.x**: The auditor runs on a designated virtual environment interpreter (Rule 37).
*   **Pip Dependencies**: Requires `ruff`, `mypy`, and `bandit` installed in the execution environment.

### Installation & Configuration

1. **Submodule Integration**
   Located at `.agents/skills/python-quality-auditor/`.

2. **Run Certification**
   Can be invoked manually or through the `/agents:audit` workflow.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

Invoked during each Sprint's **Hardening** phase to certify that the code increment complies with governance standards:

```bash
# Example: running the auditor on a specific module
python .agents/skills/python-quality-auditor/scripts/python_quality_auditor.py path/to/module/
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing

1. Fork the Project
2. Create your Feature Branch
3. Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>
