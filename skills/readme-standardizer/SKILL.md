---
name: readme-standardizer
description: Utiliza esta Skill SIEMPRE que se te pida crear, generar, estandarizar o actualizar el README.md de un proyecto. Nunca generes un README desde cero con una estructura improvisada. 
---

# 📝 Skill: README Gold Standardizer

## ⚠️ ¿Cuándo Triggerar este Skill?
Si el Director (usuario) pide **"crea el readme"**, **"actualiza el readme"** o **"aplica la plantilla al proyecto"**:
1. Tienes **PROHIBIDO** inventarte la estructura del Markdown.
2. Debes ejecutar OBLIGATORIAMENTE este proceso utilizando la plantilla arquitectónica maestra alojada en este Submódulo.

## 🛠️ Cómo Funciona (Instrucciones)

**Paso 1: Comprensión del Proyecto (Brain Drain)**
Antes de generar texto a ciegas, analiza el contexto del repositorio actual:
- ¿Qué lenguajes usa? (Para rellenar `{{TECH_STACK_BADGES}}`).
- ¿Cuáles son los pasos de ejecución? (Docker, npm, venv) para `{{INSTALLATION_xx}}`.
- ¿Cuál es el nombre del proyecto y URL de GitHub esperada? (Suele ser `https://github.com/GstMirabal/[Nombre-Directorio]`).

**Paso 2: Lectura de la Plantilla Maestra**
Abre y lee el archivo estático de la plantilla usando tu herramienta base:
`[directorio-raiz-submodulo]/.agents/skills/readme-standardizer/assets/template.md`

**Paso 3: Fusión y Sobreescritura (Render)**
Reemplaza mentalmente todos los delimitadores `{{VARIABLES_EN_MAYUSCULAS}}` de la plantilla con la información real del proyecto local que has extraído en el Paso 1. 
Mantén ABSOLUTAMENTE intacta la estructura HMTL, los `<p align="center">`, los escudos (Shields.io), los anclajes de navegación (`<a name="readme-top"></a>`), y la sección de "Contact" al final.

**Paso 4: Inyección**
- Si el `README.md` no existe en la raíz del proyecto local, créalo usando el contenido procesado.
- Si el `README.md` ya existe, **SOBREESCRIBE** su contenido por completo aplicando primero la nueva plantilla y trasladando cualquier información vieja útil hacia los apartados de "About the Project" o "Usage".

> **Nota para el Token-Saver:** Escribir el README con la herramienta `write_to_file` o `replace_file_content` es una operación aprobada y obligatoria.
