# 📘 Prompt 90 — Actualizar README.md del Proyecto

## Instrucciones de Ejecución

> "Ejecuta el prompt 90 para actualizar el README"

---

## ⚠️ RESTRICCIÓN CRÍTICA: REGENERACIÓN COMPLETA

**NO edites el README existente. Regenera TODO desde cero usando el template de abajo.**

- No copies contenido del README actual.
- No asumas que una sección "ya está bien".
- Genera cada sección leyendo las fuentes documentales listadas abajo.
- Las secciones marcadas con 🔒 **DEBEN copiarse literalmente**, sin modificar una sola palabra.

---

## Fuentes Obligatorias (lee TODAS antes de generar)

| Carpeta                         | Archivos                                   | Qué extraer                                        |
| ------------------------------- | ------------------------------------------ | -------------------------------------------------- |
| `docs/01-product-specs/`        | 3 archivos                                 | Navegación, descripciones de vistas, design system |
| `docs/02-data-governance/`      | 2 archivos                                 | Metadata de DB, samples                            |
| `docs/03-ai-generated-content/` | 3 archivos                                 | Blueprint, data dictionary, audit report           |
| `docs/`                         | `PIPELINE_ORDER.md`                        | Orden de ejecución ETL                             |
| `client/`                       | `package.json`, `App.jsx`, `navigation.js` | Dependencias, routing, módulos                     |
| `etl_pipeline/`                 | Todos los `.py`                            | Scripts y pipeline                                 |

---

## Template del README

Copia la estructura siguiente. Las secciones con `{...}` se generan leyendo las fuentes. Las secciones con 🔒 son texto estático.

```markdown
# 📊 Enterprise HR Analytics Dashboard — GDH Analytics

> **Gestión del Desarrollo Humano** | Plataforma Analítica Enterprise de RRHH
>
> **Última actualización:** {fecha actual YYYY-MM-DD HH:mm:ss UTC}
> **Versión del proyecto:** v 2.0.0
> **Estado:** 🟡 En desarrollo activo

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
- [Calidad del Código](#-calidad-del-código)
- [Documentación](#-documentación)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)
- [Sobre el Desarrollador](#-sobre-el-desarrollador)
- [Soporte](#-soporte)
- [Métricas del Proyecto](#-métricas-del-proyecto)
- [Historial de Actualizaciones](#-historial-de-actualizaciones)

---

## 🎯 Visión General

{2-3 párrafos basados en view_logic_specs.md + blueprint}

---

## 🛠️ Stack Tecnológico

{Tablas de Frontend, DevDependencies, Backend Python, DB — versiones de package.json + blueprint}

---

## 🏗️ Arquitectura del Sistema

{Diagrama ASCII + patrones de arquitectura — basado en data_dictionary.md}

---

## 📦 Módulos Funcionales

{Tabla de 13 módulos con estado real verificado en App.jsx + blueprint}

---

## 🚀 Inicio Rápido

{3 pasos: clone, env, run}

---

## 📥 Instalación y Configuración

{Variables de entorno + configuración Supabase}

---

## 🔄 Pipeline ETL

{Tabla de scripts 01-04, m01-m13, 90-92 con dependencias — de PIPELINE_ORDER.md}

---

## 📁 Estructura del Proyecto

{Árbol real de directorios — generado con list_directory}

---

## 🗄️ Base de Datos

{Arquitectura Medallion: Raw, Business, Data Marts — de data_dictionary.md + metadata_inventory.md}

---

## 📚 Documentación

{Tabla de 3 pilares con links}

---

## 🤝 Contribuir

{Flujo de trabajo + design system + cómo agregar módulos}

---

## 📜 Licencia

> ⚠️ INSTRUCCIÓN PARA EL AGENTE: Copia el siguiente texto literalmente sin modificar.

Este proyecto es de código abierto bajo la Licencia MIT.

---

> ⚠️ INSTRUCCIÓN PARA EL AGENTE: Copia la siguiente sección palabra por palabra. NO incluyas esta instrucción en el README de salida.

## 👨‍💻 Sobre el Desarrollador

**Jesús Napoleón Villegas Gálvez**
Data & Analytics Specialist | Transversal Analytics (People, Finance, Manufacturing) | Power BI | Python | SAP ERP (FI, CO, PP, MM, HCM)

Profesional híbrido especializado en traducir operaciones de negocio complejas en arquitecturas de datos escalables. Con formación en gestión corporativa y actualmente cursando una Maestría en Data Analytics & Inteligencia Artificial (ESAN), diseño soluciones integrales (Data Mesh, ETL, predicción ML) que impactan directamente en la rentabilidad de las empresas.

Aunque este proyecto es un _showcase_ aplicado a People Analytics, mi trayectoria abarca el diseño de pipelines y modelos analíticos para operaciones críticas a nivel LatAm en sectores como **Finanzas, Contabilidad, Producción y Energía**. Mi enfoque es entender la lógica del negocio desde adentro para construir herramientas Full-Stack que transformen datos crudos en decisiones ejecutivas de alto impacto.

- 📍 **Ubicación:** Lima, Perú
- 💼 **Rol Actual:** Especialista de Datos Corporativo en SMI (Grupo Intercorp)
- ✉️ **Contacto:** [EMAIL_ADDRESS]
- 🔗 **LinkedIn:** [jesusvillegasg](https://www.linkedin.com/in/jesusvillegasg/)
- 🛠️ **Stack Técnico:** Python, SQL, React, Power BI, GCP, Supabase, automatización RPA y SAP.

---

## 📊 Métricas del Proyecto

{6 tablas con métricas cruzadas de todas las fuentes — cada tabla con columna "Fuente"}

---

## 📝 Historial de Actualizaciones

{Leer el historial existente del README actual y agregar una nueva fila al inicio con la fecha actual. NO eliminar filas anteriores.}

---

> _"Tienes más datos de los que crees. El reto no es recolectarlos, es perderles el miedo y saber hacerles la pregunta correcta."_
>
> **— Construido por Jesús "Napo" Villegas**

<div align="center">
  <blockquote>
    "Tienes más datos de los que crees. El reto no es recolectarlos, es perderles el miedo y saber hacerles la pregunta correcta."<br>
    — Construido por Jesús "Napo" Villegas
  </blockquote>
  <a href="#-enterprise-hr-analytics-dashboard--gdh-analytics">⬆️ Volver al inicio</a>
</div>
```

---

## Reglas Finales

1. **Archivo de salida:** `README.md` en la raíz del proyecto.
2. **Fecha:** Formato `YYYY-MM-DD HH:mm:ss UTC` en el header.
3. **Historial:** Leer el README actual SOLO para preservar las filas del historial. Agregar nueva fila al inicio.
4. **Secciones 🔒:** Copiarlas palabra por palabra. No resumir, no omitir, no modificar.
5. **No commitear:** El operador revisa y hace commit manualmente.
