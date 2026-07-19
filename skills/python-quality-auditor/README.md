<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

</div>

<a name="readme-top"></a>

<h3 align="center">Python Quality Auditor</h3>

<p align="center">
  Agnostic Python health-check (Ruff, Mypy, Bandit) to ensure compliance with framework standards.
<br /><br />
<a href="https://github.com/GstMirabal/.agents"><strong>Explore the docs »</strong></a>
<br />
·
<a href="https://github.com/GstMirabal/.agents/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
·
<a href="https://github.com/GstMirabal/.agents/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
</p>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul><li><a href="#built-with">Built With</a></li></ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation & Configuration</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About The Project

The **Python Quality Auditor** is the health-certification tool for Python projects inside the Matrix. It provides an agnostic, incremental audit through modern tooling (Ruff for linting/formatting, Mypy for static typing, and Bandit for security), ensuring code meets the production standards of **Rule 35**.

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

Invoked during each Sprint's **Hardening** phase to certify that the code increment complies with institutional standards:

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

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

Gustavo Mirabal Suarez - gst.mirabal@gmail.com

Project Link: [https://github.com/GstMirabal/.agents](https://github.com/GstMirabal/.agents)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/GstMirabal/.agents.svg?style=for-the-badge
[contributors-url]: https://github.com/GstMirabal/.agents/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/GstMirabal/.agents.svg?style=for-the-badge
[forks-url]: https://github.com/GstMirabal/.agents/network/members
[stars-shield]: https://img.shields.io/github/stars/GstMirabal/.agents.svg?style=for-the-badge
[stars-url]: https://github.com/GstMirabal/.agents/stargazers
[issues-shield]: https://img.shields.io/github/issues/GstMirabal/.agents.svg?style=for-the-badge
[issues-url]: https://github.com/GstMirabal/.agents/issues
[license-shield]: https://img.shields.io/github/license/GstMirabal/.agents.svg?style=for-the-badge
[license-url]: https://github.com/GstMirabal/.agents/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/gstmirabal/
