# 🛠️ Skill Bridge: Autoskills (Rule 70)

## Domain
- **Category:** Infrastructure / Automation
- **Origin:** External NPM Arsenal (`npx -y autoskills`)
- **Status:** `ACTIVE_BRIDGE`

## Technical Logic
Este bridge actúa como el punto de anclaje para la herramienta de descubrimiento dinámico `autoskills`. Permite a los subagentes invocar la búsqueda de arsenal externo cuando el `manifest.json` local es insuficiente.

## Commands
```bash
# Ejecución directa del descubrimiento dinámico
npx -y autoskills@latest --scan .
```

## Governance Audit
- **Rule 70 Compliance:** Cada uso de esta herramienta debe ser técnicamente justificado y sus resultados deben ser permanentemente biseccionados en `/core/` o `/3rd/`.
- **Minimalist Policy:** No requiere instalación física en `./venv/` dado su naturaleza de ejecución efímera vía `npx`.
