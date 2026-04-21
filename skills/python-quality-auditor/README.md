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

El **Python Quality Auditor** es la herramienta de certificación de salud para proyectos Python dentro del Matrix. Proporciona una auditoría agnóstica e incremental mediante herramientas modernas (Ruff para linting/formato, Mypy para tipado estático y Bandit para seguridad), asegurando que el código cumpla con los estándares de producción de la **Regla 35**.

**Key Features:**
*   **Agnostic Linting:** Integración con Ruff para unificar más de 10 herramientas de linting en una ejecución rápida.
*   **Type Certification:** Auditoría de tipos mediante Mypy para prevenir errores lógicos en tiempo de ejecución.
*   **Security Scanning:** Identificación de vulnerabilidades conocidas en paquetes y código fuente mediante Bandit.

### Built With

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Ruff](https://img.shields.io/badge/Ruff-Linter-black)
![Mypy](https://img.shields.io/badge/Mypy-Types-orange)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Prerequisites

*   **Python 3.x**: El auditor se ejecuta sobre el intérprete de sistema o un entorno virtual designado (Rule 37).
*   **Pip Dependencies**: Requiere la instalación de `ruff`, `mypy` y `bandit` en el entorno de ejecución.

### Installation & Configuration

1. **Submodule Integration**
   Ubicado en `.agents/skills/core/python-quality-auditor/`.

2. **Run Certification**
   Puede ser invocado manualmente o mediante el workflow `/certification_audit`.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

Invocado durante la fase de **Hardenning** de cada Sprint para certificar que el incremento de código es conforme a los estándares institucionales:

```bash
# Ejemplo: Ejecución del auditor sobre un módulo específico
python .agents/skills/core/python-quality-auditor/scripts/python_quality_auditor.py path/to/module/
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
