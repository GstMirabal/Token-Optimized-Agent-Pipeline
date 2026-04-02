<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

</div>

<a name="readme-top"></a>

<h3 align="center">Autoskills Bridge</h3>

<p align="center">
  Rule 70 Gatekeeper: Bridge for dynamic tool discovery and on-the-fly arsenal orchestration.
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

El **Autoskills Bridge** es un componente del Matrix diseñado para cumplir con la **Regla 70** de gobernanza. Actúa como el punto de anclaje para herramientas externas que no residen permanentemente en el disco, permitiendo a los subagentes descubrir y ejecutar nuevos skills efímeramente vía `npx`.

**Key Features:**
*   **Discovery Automation:** Orquestación dinámica de herramientas mediante `npx autoskills`.
*   **Arsenal Hardening:** Mantiene el submódulo ligero al evitar dependencias locales redundantes.
*   **Governance Bridge:** Sincronización automática de resultados externos con la jerarquía local.

### Built With

![Bash](https://img.shields.io/badge/bash-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)
![NodeJS](https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white)
![Markdown](https://img.shields.io/badge/markdown-%23000000.svg?style=for-the-badge&logo=markdown&logoColor=white)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Prerequisites

*   **Node.js / npm / npx**: Requisito nuclear para la ejecución efímera del arsenal externo.

### Installation & Configuration

1. **Integrated in Core**
   Este bridge ya se encuentra pre-configurado dentro de `skills/core/autoskills-bridge/`. 

2. **Verification**
   Asegúrese de que su entorno permite la ejecución de binarios `npx` (Rule 37).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

Esta herramienta se invoca automáticamente por el **Orchestrator** cuando el `manifest.json` local no contiene el skill necesario para cumplir una tarea específica:

```bash
# Ejemplo: Escaneo dinámico de arsenal para hallar un validador de prisma
npx -y autoskills@latest --scan . --query "prisma validator"
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

Gustavo Mirabal Suarez - gst.mirabal@gmail.com

- LinkedIn: [@Gustavo-Mirabal](https://www.linkedin.com/in/gstmirabal/)
- GitHub: [@GstMirabal](https://github.com/GstMirabal)
- Twitter: [@GstMirabal](https://x.com/gst_mirabal)

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
