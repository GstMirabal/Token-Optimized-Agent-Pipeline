<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

</div>

<a name="readme-top"></a>

<h3 align="center">Skill Creator</h3>

<p align="center">
  Assists in the creation of new atomic skills following global governance rules (Rule 71).
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

El **Skill Creator** es la herramienta de andamiaje y automatización para la expansión del arsenal del Matrix. Asegura que cada nueva habilidad atómica herede los protocolos de seguridad, eficiencia y documentación institucional, de conformidad con la bisección obligatoria en `/core/` o `/3rd/` (**Regla 71**).

**Key Features:**
*   **Atomic Scaffolding:** Generación automática de directorios `scripts/` y archivos `SKILL.md` / `README.md`.
*   **Audit Integration:** Vincula automáticamente la nueva herramienta con el `python-quality-auditor`.
*   **Governance Guard:** Valida que el nombre y la categoría de la skill cumplan con la taxonomía oficial del framework.

### Built With

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Automation](https://img.shields.io/badge/Automation-Project-blue)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Prerequisites

*   **Universal-Agents Submodule**: Se requiere acceso a las plantillas de andamiaje globales del framework.

### Installation & Configuration

1. **Integrated in Core**
   Ubicado en `.agents/skills/core/skill-creator/`.

2. **Template access**
   Utiliza las plantillas maestras definidas en los assets del framework para inyectar las reglas atomizadas en cada nueva skill.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

Invocado cuando el **Orchestrator** o el usuario detecta la necesidad de una nueva capacidad técnica que debe ser persistida en el Matrix:

```bash
# Ejemplo: Creación de una nueva skill atómica de scraping
python .agents/skills/core/skill-creator/scripts/create_skill.py "web-scraper" "Expertise"
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
