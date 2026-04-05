# 🛠️ Skill: Autoskills (Rule 70)

## Domain
- **Category:** Infrastructure / Automation
- **Origin:** Third-Party Local Arsenal
- **Status:** `ACTIVE_LOCAL`

## Technical Logic
Esta herramienta es el motor de descubrimiento dinámico del Matrix. A pesar de ser una dependencia externa (3rd-party), `autoskills` reside físicamente en el entorno local del proyecto para asegurar la soberanía del código ejecutado. Permite a los subagentes invocar la búsqueda de arsenal externo cuando el `manifest_skills.json` local es insuficiente.

## Commands
```bash
# Ejecución del descubrimiento desde la instalación local
./node_modules/.bin/autoskills --scan . --output .agents/skills/discovery.json
```

## Governance Audit
- **Rule 70 Compliance (Priority #2):** Esta herramienta es el segundo nivel de escalamiento tras el `manifest.json`.
- **Sovereignty Policy:** Se prohíbe el uso de `npx -y`. La herramienta debe estar pre-instalada o clonada en `skills/3rd/autoskills/` y provisionada por el Agente DevOps.
