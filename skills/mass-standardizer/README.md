# 🏭 Mass Standardizer

Automated engine for the batch normalization of the Universal-Agents technical arsenal.

## About The Project

El **Mass Standardizer** es el brazo ejecutor del reforzamiento de soberanía técnica. Su objetivo es eliminar la deuda arquitectónica mediante la inyección automatizada de los estándares de documentación y estructura definidos por el `skill-creator`.

**Key Features:**
- **Audit & Detect**: Identifica carpetas de habilidades que carecen de la estructura oficial.
- **Template Synthesis**: Inyecta `README.md` y `SKILL.md` estandarizados.
- **Topological Enforcement**: Asegura la presencia del directorio `/scripts/` y `__init__.py`.

## Getting Started

### Prerequisites
- Acceso a `manifest_skills.json`.
- Permisos de escritura en las carpetas `core/` y `local/`.

## Usage

Invocado durante sprints de refactorización o unificación total del Matrix:

```bash
python skills/core/mass-standardizer/scripts/mass_standardizer.py --all
```

## License
Distributed under the MIT License.
