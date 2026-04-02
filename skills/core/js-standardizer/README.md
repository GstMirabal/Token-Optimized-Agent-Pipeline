<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

</div>

<a name="readme-top"></a>

<h3 align="center">JS-Standardizer</h3>

<p align="center">
  Universal alignment for JS/TS projects (ESLint, Prettier, JSDoc) ensuring legal governance compliance.
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

El **JS-Standardizer** es la herramienta de alineación universal para proyectos Javascript y Typescript del Matrix. Asegura que el código cumpla con los estándares de calidad del framework (ESLint, Prettier) y que la documentación interna mantenga la coherencia legal mediante JSDoc obligatorios.

**Key Features:**
*   **Linter Automation:** Configuración lista para usar de ESLint y Prettier alineada con la **Regla 35**.
*   **TS Support:** Integración nativa con Typescript para arquitecturas modernas.
*   **JSDoc Guard:** Valida la presencia de firmas de documentación en todas las funciones nucleares.

### Built With

![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white)
![ESLint](https://img.shields.io/badge/eslint-3A33D1?style=for-the-badge&logo=eslint&logoColor=white)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Prerequisites

*   **Node.js**: Requerido para ejecutar los linters y standardizers.

### Installation & Configuration

1. **Integrated in Core**
   Ubicado en `.agents/skills/core/js-standardizer/`.

2. **Link local project**
   Asegúrese de que el proyecto raíz tenga un `package.json` para facilitar la inyección de reglas.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

Invocado automáticamente durante las fases de auditoría incremental (`/certification_audit`):

```bash
# Ejemplo: Estandarización de archivos en src/
npx eslint src/ --fix
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
