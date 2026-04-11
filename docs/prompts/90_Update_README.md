# 📘 Prompt 90 — Actualizar README.md del Proyecto (Qwen Code Terminal)

## Instrucciones de Ejecución

Este prompt está diseñado para ser ejecutado por **Qwen Code** desde la terminal. El operador debe decir:

> "Ejecuta el prompt 90 para actualizar el README"

Qwen Code debe seguir las instrucciones abajo y actualizar el archivo `README.md` en la raíz del proyecto.

---

## Tarea para Qwen Code

Analiza TODO el proyecto y genera una versión actualizada, completa y profesional del `README.md` siguiendo las mejores prácticas de documentación técnica 2024-2025.

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

---

## Formato del README de Salida

El README debe seguir esta estructura profesional basada en mejores prácticas 2024-2025:

```markdown
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

{Descripción concisa de 2-3 párrafos explicando:}

- Qué es este proyecto (plataforma analítica de RRHH enterprise - GDH Analytics)
- Qué problema resuelve (visualización y análisis integral de datos de recursos humanos)
- A quién va dirigido (equipos de GDH, analistas, directivos, HR Business Partners)
- Principales características (13 módulos, 50+ vistas, dashboards interactivos)
- Datos sintéticos basados en IBM HR Analytics dataset (6 países, 6+ años, 4000-6000 empleados/mes)

{Extraer de docs/01-product-specs/02_view_logic_specs.md las descripciones oficiales de cada módulo}
{Extraer de docs/03-ai-generated-content/01_project_blueprint.md el objetivo de negocio}

---

## 🛠️ Stack Tecnológico

### Frontend (SPA - React)

| Tecnología            | Versión   | Propósito                |
| --------------------- | --------- | ------------------------ |
| React                 | {versión} | Framework UI             |
| Vite                  | {versión} | Build tool               |
| Tailwind CSS          | {versión} | Estilos                  |
| Apache ECharts        | {versión} | Visualización de datos   |
| @supabase/supabase-js | {versión} | Cliente de base de datos |
| Lucide-React          | {versión} | Iconografía corporativa  |

### Backend & Data Engineering (Python)

| Tecnología | Versión   | Propósito             |
| ---------- | --------- | --------------------- |
| Python     | 3.11+     | Lenguaje ETL          |
| Pandas     | {versión} | Manipulación de datos |
| SQLAlchemy | {versión} | ORM para Supabase     |
| NumPy      | {versión} | Cálculos numéricos    |

### Base de Datos & Infraestructura

| Tecnología            | Propósito                              |
| --------------------- | -------------------------------------- |
| Supabase (PostgreSQL) | Base de datos principal                |
| PostgREST             | API automática                         |
| Materialized Views    | Vistas materializadas para rendimiento |

---

## 🏗️ Arquitectura del Sistema

### Diagrama de Arquitectura

\`\`\`
┌─────────────────────────────────────────────────────────────┐
│ FRONTEND (React + Vite) │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐ │
│ │ Sidebar │ │ Dashboard │ │ ECharts Graphs │ │
│ │ Navigation │ │ Views │ │ Visualizations │ │
│ └──────────────┘ └──────────────┘ └──────────────────┘ │
└────────────────────────────┬────────────────────────────────┘
│
│ Supabase JS Client
│ (Direct connection)
▼
┌─────────────────────────────────────────────────────────────┐
│ DATABASE (Supabase/PostgreSQL) │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐ │
│ │ RAW Schema │ │ Business │ │ Data Marts │ │
│ │ (Bronze) │ │ Schema │ │ (Gold) │ │
│ │ │ │ (Silver) │ │ + RPC Funcs │ │
│ └──────────────┘ └──────────────┘ └──────────────────┘ │
└────────────────────────────┬────────────────────────────────┘
│
│ Python + SQLAlchemy
▼
┌─────────────────────────────────────────────────────────────┐
│ ETL PIPELINE (Python) │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐ │
│ │ Data Gen │ │ Data Ingest │ │ Transform & │ │
│ │ (Synthetic) │ │ (CSV→Raw) │ │ Business Logic │ │
│ └──────────────┘ └──────────────┘ └──────────────────┘ │
└─────────────────────────────────────────────────────────────┘
\`\`\`

### Patrones de Arquitectura

- **Medallion Architecture:** Capas Raw (Bronze) → Business (Silver) → Data Marts (Gold)
- **Separation of Concerns:** ETL, Frontend, y Base de Datos como capas independientes
- **Direct Database Connection:** Frontend conecta directamente a Supabase sin backend intermedio
- **Materialized Views:** Para optimización de consultas frecuentes

---

## 📦 Módulos Funcionales

El sistema cuenta con **13 módulos principales** y **50+ vistas analíticas**:

### Estado de Implementación

{Generar tabla completa con TODOS los módulos y vistas del sitemap}
{Cruzar con App.jsx y blueprint para verificar qué está realmente implementado}
{Usar tags de view_logic_specs.md para cada vista}

| #   | Módulo                    | Vistas Implementadas                           | Estado       | Tags           |
| --- | ------------------------- | ---------------------------------------------- | ------------ | -------------- |
| 01  | Visión Ejecutiva          | Dashboard C-Level, Alertas, Benchmarking       | 🟡 Parcial   | DESC, PRED, ML |
| 02  | Reclutamiento & Selección | Eficiencia, Calidad, Fit Score, Auditoría, NPS | 🔘 Pendiente | DESC, PRED, ML |
| ... | ...                       | ...                                            | ...          | ...            |

{NOTA: Extraer TODAS las vistas de docs/01-product-specs/01_navigation_sitemap.md}
{NOTA: Verificar estado real en docs/03-ai-generated-content/01_project_blueprint.md}
{NOTA: Agregar tags de docs/01-product-specs/02_view_logic_specs.md}

### Leyenda de Tags

| Tag  | Significado                 | Descripción                          |
| ---- | --------------------------- | ------------------------------------ |
| DESC | Descriptivo                 | Análisis descriptivo y visualización |
| PRED | Predictivo                  | Modelos predictivos y forecasting    |
| ML   | Machine Learning            | Algoritmos de aprendizaje automático |
| IA   | Generative AI               | Inteligencia artificial generativa   |
| NLP  | Natural Language Processing | Procesamiento de lenguaje natural    |
| OPT  | Optimization                | Optimización de procesos             |
| XAI  | Explainable AI              | IA explicable y transparente         |

{Tags completos de docs/01-product-specs/02_view_logic_specs.md}

---

## 🚀 Inicio Rápido

### Prerrequisitos

- **Node.js** >= 18.0.0
- **Python** >= 3.11
- **Supabase Project** (cuenta gratuita en supabase.com)
- **Git**

### Instalación en 3 Pasos

#### 1. Clonar el repositorio

\`\`\`bash
git clone <repository-url>
cd hr-analytics-dashboard
\`\`\`

#### 2. Configurar variables de entorno

\`\`\`bash

# Root .env (para ETL)

echo "DATABASE_URL=postgresql://user:password@host:port/dbname" > .env

# Client .env (para Frontend)

echo "VITE_SUPABASE_URL=[https://your-project.supabase.co](https://your-project.supabase.co)" > client/.env
echo "VITE_SUPABASE_ANON_KEY=your-anon-key-here" >> client/.env
\`\`\`

#### 3. Ejecutar pipeline ETL y frontend

\`\`\`bash

# Terminal 1: Ejecutar ETL Pipeline

cd etl_pipeline
python 00_full_run_pipeline.py

# Terminal 2: Iniciar Frontend (en otro terminal)

cd client
npm install
npm run dev
\`\`\`

### Verificación

- **Frontend:** http://localhost:5173
- **Supabase Dashboard:** [https://app.supabase.com/project/YOUR_PROJECT](https://app.supabase.com/project/YOUR_PROJECT)
- **Estado del Pipeline:** Verificar logs en consola con ✅ completado

---

## 📥 Instalación y Configuración

### Instalación Detallada

#### Backend (ETL Pipeline)

\`\`\`bash

# Crear entorno virtual (recomendado)

cd etl_pipeline
python -m venv .venv

# Activar entorno

# Windows:

.venv\Scripts\activate

# Linux/Mac:

source .venv/bin/activate

# Instalar dependencias Python

pip install pandas numpy sqlalchemy python-dotenv
\`\`\`

#### Frontend (React SPA)

\`\`\`bash
cd client
npm install

# Scripts disponibles:

npm run dev # Desarrollo (con hot reload)
npm run build # Build de producción
npm run preview # Preview del build
npm run lint # Linting con ESLint
\`\`\`

### Variables de Entorno

#### Root `.env` (ETL Pipeline)

| Variable       | Descripción                | Ejemplo                                               |
| -------------- | -------------------------- | ----------------------------------------------------- |
| `DATABASE_URL` | URL de conexión a Supabase | `postgresql://user:pass@db.supabase.co:5432/postgres` |

#### Client `.env` o `.env.local` (Frontend)

| Variable                 | Descripción               | Ejemplo                   |
| ------------------------ | ------------------------- | ------------------------- |
| `VITE_SUPABASE_URL`      | URL del proyecto Supabase | `https://xyz.supabase.co` |
| `VITE_SUPABASE_ANON_KEY` | Clave pública de Supabase | `eyJ...`                  |

> ⚠️ **Importante:** Nunca commitear archivos `.env` al repositorio. Usar `.env.example` como plantilla.

### Configuración de Supabase

1. Crear proyecto en [Supabase](https://supabase.com)
2. Copiar `Project URL` y `anon public key` de Settings > API
3. Ejecutar ETL pipeline para crear esquemas y vistas automáticamente
4. Verificar en SQL Editor que existen esquemas: `raw`, `business`

---

## 🔄 Pipeline ETL

El pipeline de datos se ejecuta con un solo comando y sigue un orden estricto:

\`\`\`bash
cd etl_pipeline
python 00_full_run_pipeline.py
\`\`\`

### Secuencia de Ejecución

| Paso | Script                       | Función                    | Output                                   |
| ---- | ---------------------------- | -------------------------- | ---------------------------------------- |
| 01   | `generate_synthetic_data.py` | Genera datos sintéticos HR | CSVs en `/data`                          |
| 02   | `setup_raw_layer.py`         | Crea tablas raw            | `raw.*` en Supabase                      |
| 03   | `ingest_data.py`             | Carga CSV a raw            | Datos en `raw.*`                         |
| 04   | `setup_business_core.py`     | Crea vistas business       | `business.v_employee_*`, `business.mv_*` |
| m05  | `m05_fuerza_laboral.py`      | Data mart fuerza laboral   | 6 MVs + 1 vista + 2 RPCs                 |
| 90   | `generate_data_inventory.py` | Inventario de metadatos    | `docs/02-data-governance/*.md`           |
| 91   | `export_data_samples.py`     | Export de muestras         | `docs/02-data-governance/*.md`           |

### Dependencias del Pipeline

\`\`\`
01 (DataGen) → 02 (Raw Schema) → 03 (Ingest) → 04 (Business Views) → m05 (Data Marts) → 90/91 (Docs)
\`\`\`

> 📋 Para más detalles: Ver `docs/PIPELINE_ORDER.md`

---

## 📁 Estructura del Proyecto

\`\`\`
hr-analytics-dashboard/
│
├── 📂 client/ # Frontend SPA (React + Vite)
│ ├── 📂 src/
│ │ ├── 📂 modules/ # Módulos por funcionalidad
│ │ │ ├── 00-layout/ # Componentes de layout
│ │ │ ├── 05-fuerza-laboral/ # Módulo fuerza laboral
│ │ │ ├── 06-nomina-costos/ # Módulo nómina
│ │ │ └── ... # Otros módulos
│ │ ├── 📂 config/
│ │ │ └── navigation.js # Configuración de navegación
│ │ ├── 📂 lib/
│ │ │ └── supabaseClient.js # Cliente Supabase
│ │ ├── App.jsx # Componente principal
│ │ └── main.jsx # Entry point
│ ├── 📂 public/ # Assets estáticos
│ ├── package.json
│ ├── vite.config.js
│ └── eslint.config.js
│
├── 📂 etl_pipeline/ # Scripts ETL (Python)
│ ├── 00_full_run_pipeline.py # Orquestador maestro
│ ├── 01_generate_synthetic_data.py # Generación de datos
│ ├── 02_setup_raw_layer.py # Schema raw
│ ├── 03_ingest_data.py # Ingesta de datos
│ ├── 04_setup_business_core.py # Vistas business
│ ├── m05_fuerza_laboral.py # Data mart
│ ├── 90_generate_data_inventory.py # Metadata inventory
│ └── 91_export_data_samples.py # Data samples
│
├── 📂 data/ # Datos crudos (gitignored)
│ └── \*.csv
│
├── 📂 docs/ # Documentación
│ ├── 📂 01-product-specs/ # Especificaciones de producto
│ │ ├── 01_navigation_sitemap.md
│ │ ├── 02_view_logic_specs.md
│ │ └── 03_design_system.md
│ ├── 📂 02-data-governance/ # Gobernanza de datos
│ │ ├── 02_supabase_metadata_inventory.md
│ │ └── 03_data_samples.md
│ ├── 📂 03-ai-generated-content/ # Contenido generado por IA
│ │ ├── 01_project_blueprint.md
│ │ ├── 02_data_dictionary.md
│ │ └── 03_audit_report.md
│ ├── 📂 prompts/ # Prompts para Qwen Code
│ │ ├── 00. Blueprint & Context.md
│ │ ├── 01. Data Dictionary.md
│ │ └── 02. Audit & Linting.md
│ └── PIPELINE_ORDER.md
│
├── .gitignore # Reglas de exclusión
├── .env # Variables de entorno (gitignored)
└── README.md # Este documento
\`\`\`

---

## 🗄️ Base de Datos

### Arquitectura Medallion

{Extraer información de: docs/03-ai-generated-content/02_data_dictionary.md}
{Extraer información de: docs/02-data-governance/02_supabase_metadata_inventory.md}

#### Capa RAW (Bronce)

- **Propósito:** Almacenamiento crudo de datos sin transformación (evitar format lock-in)
- **Tablas:**
  - `raw."ibm_hr_monthly_snapshot_byNapo"` — Snapshot mensual IBM HR
  - `raw."ibm_hr_change_reasons_byNapo"` — Razones de cambio
- **Características:** Todas las columnas en formato TEXT para evitar lock-in de formato
- **{Extraer columnas principales y % completitud de metadata_inventory.md}**

#### Capa BUSINESS (Silver)

- **Propósito:** Vistas transformadas con tipos de datos correctos y reglas de negocio
- **Vistas Principales:**
  - `business.v_employee_full_byNapo` — Vista maestra de empleados (con tipos: DATE, INTEGER, NUMERIC, BOOLEAN)
  - `business.mv_ui_global_filters` — Filtros universales para UI (6 dimensiones: periodos, países, departamentos, job levels, work centers)
- **{Extraer reglas de negocio aplicadas: tenure_months, is_active_at_snapshot, etc.}**

#### Capa DATA MARTS (Gold)

- **Propósito:** Vistas especializadas por módulo funcional para consumo analítico

**Módulo Fuerza Laboral (m05):**
| Vista/MV | Métricas | Gráfico Frontend | Descripción |
|----------|----------|-----------------|-------------|
| mv_monthly_kpis_bynapo | Headcount, avg salary, avg tenure | KPIs mensuales por país | ... |
| mv_demographics_agg | Headcount, hires, terminations | Agregados demográficos | ... |
| mv_diversity_pyramid | Gender diversity by job level | Pirámide de diversidad | ... |
| mv_bajas_heatmap | Attrition by dept and month | Mapa de calor de bajas | ... |
| mv_country_dist | Employee distribution by country | Distribución por país | ... |
| mv_experience_bubbles | Salary/tenure bubble data | Burbujas de experiencia | ... |
| v_org_tree_bynapo | Recursive org hierarchy | Organigrama integral | ... |

**Funciones RPC:**
| Función | Parámetros | Retorno | Componente Frontend |
|---------|-----------|---------|---------------------|
| get_demographics_dashboard() | JSON | Datos para cards y gráficos | Demographics.jsx |
| get_advanced_demographics() | JSON | Datos avanzados | Demographics.jsx |

{Extraer TODAS las vistas y funciones de docs/03-ai-generated-content/02_data_dictionary.md}
{Extraer descripciones de columnas de docs/02-data-governance/02_supabase_metadata_inventory.md}

### Datos Sintéticos

- **Cobertura:** 6 países (PER, CHL, COL, MEX, ESP, USA)
- **Departamentos:** IT, Sales, HR, Finance, Operations
- **Período:** Enero 2020 — Marzo 2026 (75 snapshots mensuales)
- **Empleados:** ~4,000-6,000 por mes con rotación (~0.5%/mes) y nuevas contrataciones (~1%/mes)
- **Monedas:** PEN, CLP, COP, MXN, EUR, USD (con ajuste por IPC y FX rate a USD 3.50)
- **IPC por País:** PER (4%), ESP (3%), CHL (3.5%)
- **Change Reasons Catalog:** SAL-IPC (inflación), TER-VOL (voluntaria), TER-INV (involuntaria), TER-RET (jubilación)

{Extraer reglas de simulación de docs/03-ai-generated-content/02_data_dictionary.md}

### Calidad de Datos

{Si existe docs/02-data-governance/02_supabase_metadata_inventory.md, agregar:}

- **Tablas/Vistas documentadas:** {X}
- **Columnas con completitud >90%:** {X}%
- **Columnas con valores únicos destacados:** {X}
- **Muestras de datos verificadas:** Sí/No

{Si existe docs/02-data-governance/03_data_samples.md, mencionar:}

- **Muestras de datos exportadas:** Sí (ver archivo de samples)

---

## 📚 Documentación

### Documentación del Producto (Manual)

| Documento            | Ubicación                                        | Descripción                                                                                        |
| -------------------- | ------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| Navegación & Sitemap | `docs/01-product-specs/01_navigation_sitemap.md` | Árbol completo de 13 módulos y 50+ vistas                                                          |
| Lógica de Vistas     | `docs/01-product-specs/02_view_logic_specs.md`   | Specs detalladas por vista con tags (DESC, PRED, ML, etc.)                                         |
| Design System        | `docs/01-product-specs/03_design_system.md`      | Guía de estilos: paleta Corporate Slate & Blue, tipografía, arquitectura de vistas, reglas ECharts |

### Gobernanza de Datos (Auto-generada por scripts Python)

| Documento          | Generado Por                             | Descripción                                                                                                  |
| ------------------ | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Metadata Inventory | Script 90 (`generate_data_inventory.py`) | Inventario completo de tablas/vistas: columnas, tipos, descripciones, completitud %, valores únicos, samples |
| Data Samples       | Script 91 (`export_data_samples.py`)     | Muestras reales de datos de las vistas business                                                              |

### Contenido Generado por IA (Qwen Code Terminal)

| Documento         | Prompt    | Descripción                                                                                                                              |
| ----------------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Project Blueprint | Prompt 00 | Contexto maestro: estructura, dependencias, arquitectura de datos, pipeline ETL, estado frontend, variables de entorno, score de madurez |
| Data Dictionary   | Prompt 01 | Diccionario de datos completo: linaje, capas raw/business/data marts, funciones RPC, reglas de simulación, diagrama ER                   |
| Audit Report      | Prompt 02 | Auditoría completa: hallazgos, score de calidad, seguridad, limpieza de código, buenas prácticas, correcciones                           |

### Ejecutar Prompts de Documentación

\`\`\`bash

# Desde la terminal de Qwen Code:

"Ejecuta el prompt 00 para generar el Blueprint"
"Ejecuta el prompt 01 para generar el Data Dictionary"
"Ejecuta el prompt 02 para generar el Audit Report"
"Ejecuta el prompt 90 para actualizar el README" # ← Este prompt
\`\`\`

> 📋 Para orden de ejecución completo y dependencias: Ver `docs/PIPELINE_ORDER.md`

---

## 🤝 Contribuir

### Flujo de Trabajo

1. Fork el repositorio
2. Crear rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add: AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

### Estándares de Código

- **Frontend:** ESLint + Prettier configurados
- **Backend:** Python con type hints donde sea posible
- **Commits:** Mensajes descriptivos y concisos
- **Documentación:** Actualizar README y docs cuando se agreguen features

### Agregar Nuevo Módulo

1. Crear carpeta en `client/src/modules/XX-nombre-modulo/`
2. Agentar componente principal (ej. `Dashboard.jsx`)
3. Actualizar `client/src/config/navigation.js` con nueva entrada
4. Importar y rutear en `client/src/App.jsx`
5. Crear script ETL en `etl_pipeline/mXX_nombre_modulo.py` si requiere vistas nuevas
6. Actualizar este README si el módulo es significativo

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

[ESPECIFICAR LICENCIA — MIT, Apache 2.0, etc.]

---

## 📞 Soporte

- **Issues:** [GitHub Issues](<repository-url>/issues)
- **Discusiones:** [GitHub Discussions](<repository-url>/discussions)
- **Documentación Completa:** `docs/` folder

---

## 📊 Métricas del Proyecto

{Calcular TODAS las métricas cruzando múltiples fuentes}

### Alcance Funcional

| Métrica                   | Valor                             | Fuente                                                                        |
| ------------------------- | --------------------------------- | ----------------------------------------------------------------------------- |
| **Módulos Totales**       | 13                                | `docs/01-product-specs/01_navigation_sitemap.md`                              |
| **Módulos Implementados** | {X}                               | `client/src/App.jsx` + `docs/03-ai-generated-content/01_project_blueprint.md` |
| **Vistas Totales**        | {50+}                             | `docs/01-product-specs/01_navigation_sitemap.md`                              |
| **Vistas Implementadas**  | {X}                               | `client/src/App.jsx` + blueprint                                              |
| **Vistas en Progreso**    | {X}                               | blueprint                                                                     |
| **Tags Utilizados**       | DESC, PRED, ML, IA, NLP, OPT, XAI | `docs/01-product-specs/02_view_logic_specs.md`                                |

### Pipeline ETL

| Métrica              | Valor                                  | Fuente                                                      |
| -------------------- | -------------------------------------- | ----------------------------------------------------------- |
| **Scripts ETL**      | {8}                                    | `etl_pipeline/` + `docs/PIPELINE_ORDER.md`                  |
| **Capas de Datos**   | 3 (Raw, Business, Data Marts)          | `docs/03-ai-generated-content/02_data_dictionary.md`        |
| **Tablas Raw**       | {2}                                    | `docs/02-data-governance/02_supabase_metadata_inventory.md` |
| **Vistas Business**  | {2}                                    | metadata_inventory                                          |
| **Data Marts (m05)** | {7 MVs + 1 vista + 2 RPCs}             | metadata_inventory + data_dictionary                        |
| **Países**           | 6 (PER, CHL, COL, MEX, ESP, USA)       | `docs/03-ai-generated-content/01_project_blueprint.md`      |
| **Departamentos**    | 5 (IT, Sales, HR, Finance, Operations) | blueprint                                                   |
| **Período de Datos** | Ene 2020 — Mar 2026 (75 meses)         | blueprint                                                   |
| **Empleados/Mes**    | ~4,000-6,000                           | blueprint                                                   |

### Stack Tecnológico

| Métrica                           | Valor                            | Fuente                |
| --------------------------------- | -------------------------------- | --------------------- |
| **Dependencias Frontend (prod)**  | {X}                              | `client/package.json` |
| **Dependencias Frontend (dev)**   | {Y}                              | `client/package.json` |
| **Dependencias Backend (Python)** | Pandas, NumPy, SQLAlchemy        | blueprint + scripts   |
| **Framework UI**                  | React {versión} + Vite {versión} | package.json          |
| **Visualización**                 | Apache ECharts {versión}         | package.json          |
| **Database**                      | Supabase (PostgreSQL)            | blueprint             |

### Calidad del Código

{Si existe docs/03-ai-generated-content/03_audit_report.md, agregar:}

| Métrica                | Valor    | Fuente                                            |
| ---------------------- | -------- | ------------------------------------------------- |
| **Score de Calidad**   | {XX/100} | `docs/03-ai-generated-content/03_audit_report.md` |
| **Hallazgos Críticos** | {X} 🔴   | audit_report                                      |
| **Advertencias**       | {Y} 🟡   | audit_report                                      |
| **Sugerencias**        | {Z} 🟢   | audit_report                                      |
| **Issues Resuueltos**  | {X}      | audit_report                                      |

### Cobertura de Documentación

| Métrica                  | Valor          | Fuente                                           |
| ------------------------ | -------------- | ------------------------------------------------ |
| **Product Specs**        | ✅ Completos   | `docs/01-product-specs/` (3 archivos)            |
| **Data Governance**      | ✅ Generada    | `docs/02-data-governance/` (2 archivos)          |
| **AI-Generated Content** | {✅/⚠️}        | `docs/03-ai-generated-content/` ({X}/3 archivos) |
| **Blueprint**            | {✅/⚠️}        | {fecha si existe}                                |
| **Data Dictionary**      | {✅/⚠️}        | {fecha si existe}                                |
| **Audit Report**         | {✅/⚠️}        | {fecha si existe}                                |
| **Pipeline Order**       | ✅ Actualizado | `docs/PIPELINE_ORDER.md`                         |

### Última Actualización

| Métrica                  | Valor                                          |
| ------------------------ | ---------------------------------------------- |
| **README**               | {fecha y hora actual: YYYY-MM-DD HH:mm:ss UTC} |
| **Versión del Proyecto** | {detectar de package.json o asignar 1.0.0}     |
| **Estado del Proyecto**  | 🟢 Activo / 🟡 En desarrollo / 🔴 Experimental |

---

## 📝 Historial de Actualizaciones

| Fecha          | Versión   | Cambios Principales                                | Autor              |
| -------------- | --------- | -------------------------------------------------- | ------------------ |
| {fecha actual} | {versión} | README actualizado con mejores prácticas 2024-2025 | Qwen Code Terminal |
| ...            | ...       | ...                                                | ...                |

> 💡 **Nota:** Este README se actualiza automáticamente con cada ejecución del Prompt 90.
> Incluye métricas frescas del proyecto, estado de módulos, y documentación al día.

---

> _"Tienes más datos de los que crees. El reto no es recolectarlos, es perderles el miedo y saber hacerles la pregunta correcta."_
>
> **— Construido por Jesús "Napo" Villegas**

<div align="center">
[⬆️ Volver al inicio](#-enterprise-hr-analytics-dashboard--gdh-analytics)
</div>
```
