---
name: omni-context-minimizer
description: Utiliza este Skill imperativamente ANTES de leer cualquier archivo de código que contenga más de 200 líneas. Este script extrae y te devuelve un esqueleto táctico (Imports, Nombres de Clases y Firmas de Funciones) descartando toda la lógica interna, previniendo así un consumo brutal de ventana de contexto. Funciona para NodeJS, Python, Go, Rust y Java.
---

# 🪙 Skill: Omni Context Minimizer

## ⚠️ ¿Cuándo Triggerar este Skill?
Como Subagente, TIENES PROHIBIDO leer archivos masivos de código (`.js`, `.py`, `.go`, `.ts`) usando tu herramienta estándar `view_file` sin antes pasar por este minimizador, a menos que ya sepas exactamente el número o rango de líneas que vas a inspeccionar.

Si te mandan a "Analizar cómo está estructurada la API" o "Revisar el archivo `views.py` grande":
1.  NO PUEDES METER EL ARCHIVO ENTERO EN TU MEMORIA.
2.  EJECUTA ESTE SKILL INMEDIATAMENTE.

## 🛠️ Cómo Funciona (Instrucciones)
Este repositorio contiene un script de Python llamado `omni_minimizer.py` en la carpeta `scripts/`. Este script escudriña el DOM léxico del archivo destino y devuelve únicamente por terminal las líneas que declaran Funciones, Clases, o Importaciones.

**Paso 1:** Localiza la ruta absoluta del archivo pesado que necesitas analizar (ej: `/ruta/a/mi_proyecto/src/app.js`).

**Paso 2:** Ejecuta el minimizador pasando esa ruta como argumento (el script Python debe ejecutarse desde la ruta de la Skill en el submódulo):
```bash
python .agents/skills/omni-context-minimizer/scripts/omni_minimizer.py /ruta/al/archivo/pesado
```

**Paso 3:** La consola te devolverá el esqueleto. Por ejemplo:
```text
Línea 1: import express from 'express';
Línea 4: const app = express();
Línea 10: export const loginController = async (req, res) => {
Línea 45: class DatabaseService {
...
--- [OPTIMIZACIÓN]: Se redujo el archivo a 8 líneas de estructura pura. ---
```

**Paso 4:** Ahora que tienes el "mapa", **si decides que necesitas ver cómo funciona la lógica** de `loginController` que está en la línea 10, puedes usar `view_file` o `grep_search` centrando tu tiro ESTRICTAMENTE en la línea 10, ahorrando todo el contexto restante.

## 🔴 Autorización del Token-Saver
Si estás enviando un `implementation_plan.md` al Orquestador e incluye el escaneo heurístico de toda una carpeta `/src`, **DEBES** especificar en tu MD: *"Se utilizará el `omni-context-minimizer` para mapear los 5 archivos base, previniendo el ahogamiento por contexto"*. 
De lo contrario, el Agente Auditor rechazará el plan.
