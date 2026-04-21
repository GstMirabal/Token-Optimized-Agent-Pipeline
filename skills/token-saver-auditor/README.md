<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

</div>

<a name="readme-top"></a>

<h3 align="center">Token-Saver Auditor (CFO)</h3>

<p align="center">
  Audits the economic efficiency of agent plans and execution logs to minimize API costs.
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

El **Token-Saver Auditor (CFO)** actúa como el supervisor financiero del Matrix. Es un "Kill Switch" económico que analiza los planes de implementación para asegurar el consumo mínimo de tokens, priorizando el uso del `omni-context-minimizer` y evitando escaneos de contexto redundantes.

**Key Features:**
*   **Economic Oversight:** Análisis de costos previo a la ejecución masiva de tareas.
*   **Context Optimization:** Obliga al uso de esqueletos AST en archivos grandes.
*   **Budget Guard:** Previene bucles de razonamiento infinitos que agotan cuotas de API.

### Built With

![Governance](https://img.shields.io/badge/governance-logic-blue)
![CFO](https://img.shields.io/badge/CFO-audit-orange)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Prerequisites

*   **Universal-Agents Core**: Requiere que las reglas de gobernanza (Rules 1-78) estén activas.

### Installation & Configuration

1. **Submodule Integration**
   Ubicado en `.agents/skills/core/token-saver-auditor/`.

2. **Activation**
   Se activa automáticamente durante la fase de planificación táctica (Orchestration Phase).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

El Auditor revisa cada propuesta del **Orchestrator** antes de que el **Agente DevOps** pueda ejecutar cambios físicos. Si el plan es ineficiente (e.g. escaneo recursivo sin minimizer), el Auditor bloquea la ejecución.

```bash
# Ejemplo: Activación del Auditor durante la fase de debate
Agente Principal: "El Auditor debe certificar este plan de Phase 2 antes de proceder."
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
