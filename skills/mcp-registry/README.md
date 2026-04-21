<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

</div>

<a name="readme-top"></a>

<h3 align="center">MCP Registry & Manager</h3>

<p align="center">
  Registry and configuration manager for Model Context Protocol servers to maximize data utility.
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

El **MCP Registry & Manager** es el sistema de descubrimiento de datos externos del Matrix. Gestiona la configuración y el enrutamiento de servidores Model Context Protocol (MCP) locales y remotos (e.g. CoinGecko, FRED, Yahoo Finance), permitiendo a los subagentes expandir su frontera de conocimiento de forma segura y auditada.

**Key Features:**
*   **Centralized Registry:** Un único punto de verdad en `registry.json` para todas las conexiones externas.
*   **Zero-Trust Routing:** Asegura que solo los MCPs autorizados en el registro puedan ser invocados por el Orchestrator.
*   **Dynamic Provisioning:** Capacidad de inyectar variables de entorno y secretos de API de forma segura.

### Built With

![JSON](https://img.shields.io/badge/json-5E5E5E?style=for-the-badge&logo=json&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-Registry-brightgreen)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Prerequisites

*   **Claude / Gemini / LLM Platform**: Capacidad del modelo para interactuar con servidores MCP.
*   **MCP Server Configuration**: Ubicación persistente de sus binarios en `.env` o el archivo de configuración global.

### Installation & Configuration

1. **Integrated in Core**
   Ubicado en `.agents/skills/core/mcp-registry/`.

2. **Register a Server**
   Añada su nuevo servidor a `registry.json` siguiendo el esquema de metadatos oficial.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

El **Orchestrator** consulta el registro antes de cada tarea que requiera datos en tiempo real (Trading, Macro, Sentiment). Si el servidor no está en el `registry.json`, se bloquea el acceso externo. De conformidad con las reglas de **Survival Mode**, prioriza el uso de créditos gratuitos de APIs externas.

```bash
# Ejemplo: Visualización de servidores activos en el registro
cat .agents/skills/core/mcp-registry/registry.json
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
