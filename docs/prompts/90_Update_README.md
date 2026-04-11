# 📘 Prompt 90 — Actualizar README.md del Proyecto (Qwen Code Terminal)

## Instrucciones de Ejecución

Este prompt está diseñado para ser ejecutado por **Qwen Code** desde la terminal. El operador debe decir:

> "Ejecuta el prompt 90 prestando especial atención a copiar exactamente la sección del desarrollador (Paso 10)"

Qwen Code debe seguir las instrucciones abajo y actualizar el archivo `README.md` en la raíz del proyecto.

---

## Tarea para Qwen Code

### ⚠️ RESTRICCIÓN CRÍTICA: REGENERACIÓN COMPLETA (NO EDICIÓN)

**ESTE PROMPT REQUIERE REGENERAR EL README COMPLETAMENTE DESDE CERO.**

- **NO leas el README existente** para copiar o preservar contenido.
- **NO asumas que una sección "ya está bien"** porque existe en el archivo actual.
- **NO hagas edición mínima** (solo cambiar números o timestamps).
- **SÍ genera TODO el contenido desde cero** siguiendo exactamente el template definido abajo.
- **SÍ reemplaza CADA sección** con el contenido fresco del template, aunque ya exista.
- **SÍ usa TODAS las fuentes documentales** para generar cada sección nueva.

> **Analogía:** No estás "editando" un README. Estás "compilando" uno nuevo desde las fuentes. El archivo anterior es solo un placeholder que será sobrescrito por completo.

### Pasos de Ejecución

1. **Lee TODA la documentación de producto (obligatorio):**

   **Especificaciones de Producto (`docs/01-product-specs/`):**
   - `01_navigation_sitemap.md` → Árbol completo de navegación con los 13 módulos y 50+ vistas
   - `02_view_logic_specs.md` → Descripción detallada de CADA vista con su metodología (DESC, PRED, ML, etc.)
   - `03_design_system.md` → Paleta de colores, tipografía, arquitectura de vistas, reglas de ECharts

   **Propósito:** Extraer la arquitectura de navegación completa, descripciones de negocio de cada vista, y especificaciones de diseño para documentar en el README.

2. **Lee TODA la gobernanza de datos (obligatorio):**

   **Gobernanza de Datos (`docs/02-data-governance/`):**
   - `02_supabase_metadata_inventory.md` → Inventario completo de tablas/vistas con columnas, tipos, descripciones, completitud %, valores únicos, sample values
   - `03_data_samples.md` → Muestras reales de datos de las vistas business

   **Propósito:** Documentar la arquitectura de base de datos real, columnas principales, calidad de datos, y ejemplos concretos en el README.

3. **Lee TODO el contexto generado por IA (obligatorio):**

   **Contenido AI-Generated (`docs/03-ai-generated-content/`):**
   - `01_project_blueprint.md` → Contexto maestro: estructura de directorios, dependencias, arquitectura de datos, pipeline ETL, estado del frontend, variables de entorno, score de madurez
   - `02_data_dictionary.md` → Diccionario de datos completo: linaje, capas raw/business/data marts, funciones RPC, reglas de simulación, diagrama ER
   - `03_audit_report.md` → Reporte de auditoría: hallazgos, score de calidad, seguridad, limpieza de código, buenas prácticas

   **Propósito:** Extraer métricas del proyecto, dependencias verificadas, estado real de implementación, y cualquier hallazgo relevante.

4. **Lee el pipeline orden (obligatorio):**
   - `docs/PIPELINE_ORDER.md` → Orden de ejecución, dependencias cruzadas, comandos, reglas de oro, nomenclatura

   **Propósito:** Documentar correctamente el flujo ETL y las dependencias entre scripts.

5. **Lee archivos de configuración:**
   - `client/package.json` → dependencias y scripts con versiones exactas
   - `client/vite.config.js` → configuración de build
   - `etl_pipeline/00_full_run_pipeline.py` → scripts del pipeline y orden de ejecución
   - `.gitignore` (raíz y client) → qué se excluye del repo

6. **Analiza la estructura del proyecto:**
   - Usa `list_directory` recursivamente o `glob` para generar un árbol completo
   - Excluye: `node_modules`, `.git`, `.venv`, `__pycache__`, `dist`, `build`, `.turbo`, `*.log`
   - Identifica módulos implementados vs placeholders en `client/src/modules/`

7. **Lee componentes frontend implementados:**
   - `client/src/App.jsx` → sistema de routing y qué vistas tienen componentes reales
   - `client/src/config/navigation.js` → módulos, sub-vistas, iconos, tags
   - Componentes en `client/src/modules/` que tienen implementación real (no placeholders)
   - `client/src/lib/supabaseClient.js` → conexión a base de datos

8. **Lee scripts ETL (al menos los headers y funciones principales):**
   - `01_generate_synthetic_data.py` → generación de datos sintéticos
   - `02_setup_raw_layer.py` → capa raw
   - `03_ingest_data.py` → ingesta
   - `04_setup_business_core.py` → vistas business
   - `m05_fuerza_laboral.py` → data marts
   - `90_generate_data_inventory.py` → metadata
   - `91_export_data_samples.py` → samples

9. **Genera métricas del proyecto cruzando TODAS las fuentes:**
   - Número de módulos implementados vs totales (de navigation.js + blueprint)
   - Número de vistas implementadas vs totales (de view_logic_specs + blueprint)
   - Número de scripts ETL funcionales (de pipeline_order + archivos reales)
   - Dependencias de frontend y backend con versiones exactas (de package.json + blueprint)
   - Variables de entorno requeridas (de blueprint + archivos .env si existen)
   - Cobertura de documentación (qué archivos existen en docs/ vs qué debería existir)
   - Estado de calidad del código (de audit_report si existe)
   - Arquitectura de datos real (de data_dictionary + metadata_inventory)

10. **INSERCIÓN ESTÁTICA OBLIGATORIA:** Debes copiar EXACTAMENTE, palabra por palabra, la sección "Sobre el Desarrollador", "Licencia" y la frase final en cursiva ("> Tienes más datos...") tal como aparecen en la plantilla de este prompt (sección `Formato del README de Salida`). ESTÁ ESTRICTAMENTE PROHIBIDO omitir, resumir o modificar el perfil del desarrollador.

---

## Formato del README de Salida

El README debe seguir esta estructura profesional basada en mejores prácticas 2024-2025:

# 📊 Enterprise HR Analytics Dashboard — GDH Analytics

> **Gestión del Desarrollo Humano** | Plataforma Analítica Enterprise de RRHH
>
> **Última actualización:** {fecha y hora actual en formato: YYYY-MM-DD HH:mm:ss UTC}
> **Versión del proyecto:** v{detectar de package.json o asignar 1.0.0}
> **Estado:** 🟢 Activo / 🟡 En desarrollo / 🔴 Experimental

---

## 📑 Tabla de Contenidos

- [Visión General](#-visión-general)
- [Stack Tecnológico](#-stack-tecnológico)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Módulos Funcionales](#-módulos-funcionales)
- [Inicio Rápido](#-inicio-rápido)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Pipeline ETL](#-pipeline-etl)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Base de Datos](#-base-de-datos)
- [Documentación](#-documentación)
- [Contribuir](#-contribuir)
- [Sobre el Desarrollador](#-sobre-el-desarrollador)
- [Licencia](#-licencia)
- [Historial de Actualizaciones](#-historial-de-actualizaciones)

---

## 🎯 Visión General

{Descripción concisa basada en el proyecto}

---

## 🛠️ Stack Tecnológico

{Generar tablas de Frontend, Backend, Database}

---

## 🏗️ Arquitectura del Sistema

{Generar diagrama y patrones}

---

## 📦 Módulos Funcionales

{Generar tabla de implementación}

---

## 🚀 Inicio Rápido

{Generar pasos}

---

## 📥 Instalación y Configuración

{Generar variables de entorno}

---

## 🔄 Pipeline ETL

{Generar tabla de ejecución}

---

## 📁 Estructura del Proyecto

{Generar árbol real de carpetas}

---

## 🗄️ Base de Datos

{Generar esquemas Medallion}

---

## 📚 Documentación

{Generar tabla de links a docs}

---

## 🤝 Contribuir

{Generar reglas}

---

## 👨‍💻 Sobre el Desarrollador

**Jesús Napoleón "Napo" Villegas Gálvez**
_Data Engineer & AI Specialist | Corporate Data Architect_

Profesional híbrido especializado en traducir operaciones de negocio complejas en arquitecturas de datos escalables. Con formación en gestión corporativa y actualmente cursando una Maestría en Data Analytics & Inteligencia Artificial (ESAN), diseño soluciones integrales (Data Mesh, ETL, predicción ML) que impactan directamente en la rentabilidad de las empresas.

Aunque este proyecto es un _showcase_ aplicado a People Analytics, mi trayectoria abarca el diseño de pipelines y modelos analíticos para operaciones críticas a nivel LatAm en sectores como **Finanzas, Contabilidad, Producción y Energía**. Mi enfoque es entender la lógica del negocio desde adentro para construir herramientas Full-Stack que transformen datos crudos en decisiones ejecutivas de alto impacto.

- 📍 **Ubicación:** Lima, Perú
- 💼 **Rol Actual:** Especialista de Datos Corporativo en SMI (Grupo Intercorp)
- ✉️ **Contacto:** jesus.villegas@outlook.com
- 🔗 **LinkedIn:** [jesusvillegasg](https://www.linkedin.com/in/jesusvillegasg/)
- 🛠️ **Stack Técnico:** Python, SQL, React, Power BI, GCP, Supabase, automatización RPA y SAP.

---

## 📄 Licencia

Este proyecto es de código abierto bajo la Licencia MIT.

---

## 📊 Métricas del Proyecto

{Calcular TODAS las métricas cruzando las fuentes de docs/}

---

## 📝 Historial de Actualizaciones

| Fecha          | Versión   | Cambios Principales                                | Autor              |
| -------------- | --------- | -------------------------------------------------- | ------------------ |
| {fecha actual} | {versión} | README actualizado con mejores prácticas 2024-2025 | Qwen Code Terminal |

> 💡 **Nota:** Este README se actualiza automáticamente con cada ejecución del Prompt 90.

---

> _"Tienes más datos de los que crees. El reto no es recolectarlos, es perderles el miedo y saber hacerles la pregunta correcta."_
>
> **— Construido por Jesús "Napo" Villegas**

<div align="center">
[⬆️ Volver al inicio](#-enterprise-hr-analytics-dashboard--gdh-analytics)
</div>

---

## Reglas de Actualización (Internas para Qwen Code)

1. Lee TODAS las fuentes documentales en `docs/`.
2. Actualiza la fecha a formato `YYYY-MM-DD HH:mm:ss UTC`.
3. Calcula métricas precisas.
4. NO alteres las secciones estáticas indicadas en el Paso 10.
