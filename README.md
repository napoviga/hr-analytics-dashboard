# 📊 Enterprise HR Analytics Dashboard — GDH Analytics

> **Gestión del Desarrollo Humano** | Plataforma Analítica Enterprise de RRHH
>
> **Última actualización:** 2026-04-11 15:37:25 UTC
> **Versión del proyecto:** v0.0.0
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

GDH Analytics es una plataforma analítica integral diseñada para la **Gestión del Desarrollo Humano (GDH)** y operaciones cruzadas de recursos humanos a nivel enterprise. El sistema proporciona una visualización analítica técnica y escalable a los distintos subprocesos de GDH, estructurados a través de **13 módulos funcionales** y **50+ vistas analíticas**.

**Problema que resuelve:** Las organizaciones necesitan una visión unificada, predictiva y accionable del ciclo de vida completo del talento — desde el reclutamiento hasta la retención. Este dashboard centraliza datos demográficos, compensaciones, desempeño, engagement, y calidad de datos en una interfaz corporativa inspirada en Microsoft 365.

**A quién va dirigido:** Equipos de GDH/RRHH, analistas de people analytics, HR Business Partners, directivos (C-Level), y equipos de compliance.

**Datos:** El sistema opera con datos sintéticos basados en el dataset IBM HR Analytics, cubriendo **6 países** (Perú, Chile, Colombia, México, España, USA), **5 departamentos** (IT, Sales, HR, Finance, Operations), **75 meses de datos** (Enero 2020 — Marzo 2026), y **~4,000-6,000 empleados por mes** con rotación natural (~0.5%/mes) y nuevas contrataciones (~1%/mes). Los salarios están ajustados por IPC por país y convertidos a USD con tipo de cambio fijo 3.50.

**Metodología analítica:** Cada vista está etiquetada con su enfoque metodológico: Descriptivo (DESC), Predictivo (PRED), Machine Learning (ML), IA Generativa (IA), Procesamiento de Lenguaje Natural (NLP), Optimización (OPT), e IA Explicable (XAI).

---

## 🛠️ Stack Tecnológico

### Frontend (SPA - React)

| Tecnología | Versión | Propósito |
|-----------|---------|-----------|
| React | 19.2.4 | Framework UI principal |
| Vite | 8.0.1 | Build tool y dev server |
| Tailwind CSS | 4.2.2 | Estilos y design system |
| Apache ECharts | 6.0.0 | Visualización de datos interactiva |
| echarts-for-react | 3.0.6 | Integración ECharts en React |
| @supabase/supabase-js | 2.101.1 | Cliente de base de datos Supabase |
| Lucide-React | 1.7.0 | Iconografía corporativa |

### DevDependencies (Frontend)

| Paquete | Versión | Propósito |
|---------|---------|-----------|
| ESLint | 9.39.4 | Linting de código |
| ESLint React Hooks | 7.0.1 | Reglas React Hooks |
| ESLint React Refresh | 0.5.2 | Reglas Fast Refresh |
| @tailwindcss/vite | 4.2.2 | Plugin Tailwind para Vite |
| @vitejs/plugin-react | 6.0.1 | Plugin React para Vite |
| PostCSS | 8.5.8 | Procesador CSS |
| Autoprefixer | 10.4.27 | Prefijos CSS automáticos |
| Prisma | 7.6.0 | ORM (configurado, uso limitado) |
| dotenv | 17.4.1 | Variables de entorno |
| globals | 17.4.0 | Definiciones de globals ESLint |
| @types/react | 19.2.14 | TypeScript types para React |
| @types/react-dom | 19.2.3 | TypeScript types para React DOM |

### Backend & Data Engineering (Python)

| Tecnología | Propósito | Scripts |
|-----------|-----------|---------|
| Python 3.11+ | Lenguaje ETL | Todos |
| Pandas | Manipulación y transformación de datos | 01, 03, 90 |
| NumPy | Cálculos numéricos y generación de datos | 01 |
| SQLAlchemy | ORM para conexión a Supabase | 02, 03, 04, m05, 90 |
| python-dotenv | Carga de variables de entorno | 02, 03, 04, m05, 90, 91 |
| psycopg2 | Driver PostgreSQL nativo | 91 |

### Base de Datos & Infraestructura

| Tecnología | Propósito |
|-----------|-----------|
| Supabase (PostgreSQL) | Base de datos principal (proyecto `hr-analytics-db`, región São Paulo) |
| PostgREST | API REST automática expuesta por Supabase |
| Materialized Views | Vistas materializadas para optimización de consultas frecuentes |
| Funciones RPC | Funciones PostgreSQL consumibles vía PostgREST |

---

## 🏗️ Arquitectura del Sistema

### Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React 19 + Vite 8)                 │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   Sidebar    │  │   Dashboard  │  │  ECharts Graphs      │  │
│  │  Navigation  │  │   Views      │  │  (Dynamic Binding)   │  │
│  │  (Collaps.)  │  │  (6 active)  │  │  (Zero Hardcoding)   │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│                                                                 │
│  Design System: "Corporate Slate & Blue" (Tailwind CSS 4.2)    │
│  Routing: State-based (vistaActual) — Sin react-router         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ Supabase JS Client
                             │ Direct connection (no backend intermedio)
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              DATABASE (Supabase / PostgreSQL)                    │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  RAW Schema  │  │  Business    │  │   Data Marts         │  │
│  │  (Bronce)    │  │  Schema      │  │   (Gold)             │  │
│  │              │  │  (Silver)    │  │   + 2 RPC Funcs      │  │
│  │ 2 tablas     │  │ 2 vistas     │  │   7 MVs + 1 vista    │  │
│  │ TEXT cols    │  │ Typed views  │  │   Org tree recursive │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│                                                                 │
│  13 objetos totales | 100% completitud en columnas clave       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ Python 3.11 + SQLAlchemy + Pandas
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ETL PIPELINE (8 Scripts Python)               │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Data Gen    │  │  Data Ingest │  │  Transform &         │  │
│  │  (Synthetic) │  │  (CSV→Raw)   │  │  Business Logic      │  │
│  │  Script 01   │  │  Scripts 02  │  │  Scripts 04+m05      │  │
│  │              │  │  03          │  │                      │  │
│  │ 4,000-6,000  │  │ Raw tables   │  │ 7 MVs + 2 vistas     │  │
│  │ employees/mo │  │ (TEXT cols)  │  │ + 2 RPC functions    │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│                                                                 │
│  Orquestador: 00_full_run_pipeline.py (secuencial)             │
│  Post-pipeline: Scripts 90-91 (metadata + samples docs)        │
└─────────────────────────────────────────────────────────────────┘
```

### Patrones de Arquitectura

| Patrón | Implementación |
|--------|---------------|
| **Medallion Architecture** | Capas Raw (Bronce/TEXT) → Business (Silver/Typed) → Data Marts (Gold/Specialized) |
| **Separation of Concerns** | ETL, Frontend, y Base de Datos como capas completamente independientes |
| **Direct Database Connection** | Frontend conecta directamente a Supabase sin backend API intermedio |
| **Materialized Views** | 7 MVs para optimización de consultas analíticas frecuentes |
| **Recursive CTEs** | Vista `v_org_tree_bynapo` usa CTE recursivo para jerarquía organizacional (depth ≤ 10) |
| **Universal Filters** | `mv_ui_global_filters` expone 6 dimensiones como JSON para dropdowns del frontend |
| **Zero Hardcoding** | ECharts genera ejes/series dinámicamente — cero categorías quemadas en código |

---

## 📦 Módulos Funcionales

El sistema cuenta con **13 módulos principales** y **50+ vistas analíticas**. Cada vista está etiquetada con su enfoque metodológico:

### Estado de Implementación

| # | Módulo | Vistas | Estado | Tags |
|---|--------|--------|--------|------|
| 01 | **Visión Ejecutiva** | Dashboard C-Level, Alertas & Anomalías, Benchmarking de Mercado | 🟡 Parcial (1/3) | DESC, PRED, ML |
| 02 | **Reclutamiento & Selección** | Eficiencia & Ciclos, Calidad, Fit Score Predictivo, Auditoría de Sesgos, NPS | 🔘 Pendiente | DESC, PRED, ML |
| 03 | **Onboarding & Integración** | Procesos Activos, Tiempo a Productividad, Rotación Temprana (<90d) | 🔘 Pendiente | DESC, PRED |
| 04 | **Análisis de Ciclo de Vida & Clústeres** | Comportamiento de Grupos, Causalidad & Correlaciones, Mapa Momentos Críticos | 🔘 Pendiente | DESC, PRED, ML |
| 05 | **Fuerza Laboral & Estructura** | Demografía, Organigrama Integral, Posiciones, Costos, Distribución Geográfica, Forecast | ✅ Implementado (6/6) | DESC, PRED |
| 06 | **Nómina, Costos & Equity** | Bandas Salariales, Equidad Interna, Compa-Ratio, Masa Salarial, Impacto Rotación, Simulador | 🟡 Parcial (1/6) | DESC, PRED |
| 07 | **Tiempo, Asistencia & Bienestar** | Ausentismo, Horas Extra, Vacaciones, SST, Bienestar, Optimización de Turnos | 🔘 Pendiente | DESC, PRED, ML, OPT |
| 08 | **Gestión del Desempeño** | Evaluación 360°, OKRs/KPIs, Planes de Mejora (PIP), Ranking | 🔘 Pendiente | DESC, IA, NLP |
| 09 | **Talento & Desarrollo** | Matriz 9-Box, Sucesión, Movilidad Interna, L&D, ROI Capacitación | 🔘 Pendiente | DESC, PRED, ML |
| 10 | **Engagement & Sentimiento** | eNPS, Heatmap de Engagement, Diversidad & Inclusión (DEI) | 🔘 Pendiente | DESC, NLP |
| 11 | **Compliance & Relaciones Laborales** | Cumplimiento Laboral, Relaciones Sindicales | 🔘 Pendiente | DESC |
| 12 | **Retención & Riesgo de Fuga** | Score Predictivo de Fuga, Benchmarking Turnover, Correlación Manager-Fuga | 🔘 Pendiente | DESC, ML, XAI |
| 13 | **Calidad de Datos** | Integridad & Auditoría, Log Maestros, Diccionario de Datos | 🟡 Parcial (1/3) | DESC |

### Vistas Implementadas Detalladamente

| Módulo | Vista | Componente | Datos | Descripción |
|--------|-------|-----------|-------|-------------|
| 05 | Demografía & Headcount | `Demographics.jsx` | Supabase RPC | KPI cards (fuerza laboral, altas, bajas) + 4 gráficos avanzados (pirámide, heatmap, distribución, burbujas) |
| 05 | Organigrama Integral | `OrganigramaIntegral.jsx` | ⚠️ Mock | Visualización jerárquica interactiva (pendiente conectar a `v_org_tree_bynapo`) |
| 05 | Organigrama de Posiciones | `OrgStructure.jsx` | Supabase | Mapeo de capacidad instalada con botones de navegación |
| 06 | Equidad Interna | `Compensations.jsx` | Supabase | Scatter plot: edad vs tarifa diaria, coloreado por attrition |
| 13 | Auditoría de Datos | `EmployeeTable.jsx` | Supabase | Data grid para auditoría de registros en crudo |
| 01 | Dashboard C-Level | `Overview.jsx` | Supabase | KPI cards + gráfico de barras por departamento |

### Leyenda de Tags Metodológicos

| Tag | Significado | Descripción |
|-----|------------|-------------|
| **DESC** | Descriptivo | Análisis descriptivo y visualización de datos históricos |
| **PRED** | Predictivo | Modelos predictivos, forecasting y proyecciones |
| **ML** | Machine Learning | Algoritmos de aprendizaje automático |
| **IA** | Generative AI | Inteligencia artificial generativa (resúmenes, NLP) |
| **NLP** | Natural Language Processing | Procesamiento de lenguaje natural |
| **OPT** | Optimization | Optimización de procesos y recursos |
| **XAI** | Explainable AI | IA explicable e interpretable (SHAP) |

---

## 🚀 Inicio Rápido

### Prerrequisitos

- **Node.js** >= 18.0.0
- **Python** >= 3.11
- **Supabase Project** (cuenta gratuita en [supabase.com](https://supabase.com))
- **Git**

### Instalación en 3 Pasos

#### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd hr-analytics-dashboard
```

#### 2. Configurar variables de entorno

```bash
# Root .env (para ETL)
echo "DATABASE_URL=postgresql://user:password@host:port/dbname" > .env

# Client .env (para Frontend)
echo "VITE_SUPABASE_URL=https://your-project.supabase.co" > client/.env
echo "VITE_SUPABASE_ANON_KEY=your-anon-key-here" >> client/.env
```

#### 3. Ejecutar pipeline ETL y frontend

```bash
# Terminal 1: Ejecutar ETL Pipeline
cd etl_pipeline
python 00_full_run_pipeline.py

# Terminal 2: Iniciar Frontend (en otro terminal)
cd client
npm install
npm run dev
```

### Verificación

| Servicio | URL | Estado |
|----------|-----|--------|
| Frontend | http://localhost:5173 | ✅ Debe cargar con Sidebar + Dashboard |
| Supabase Dashboard | https://app.supabase.com/project/YOUR_PROJECT | ✅ Verificar esquemas `raw` y `business` |
| Pipeline ETL | Logs en consola | ✅ 8 scripts completados con ✅ |

---

## 📥 Instalación y Configuración

### Instalación Detallada

#### Backend (ETL Pipeline)

```bash
# Crear entorno virtual (recomendado)
cd etl_pipeline
python -m venv .venv

# Activar entorno
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instalar dependencias Python
pip install pandas numpy sqlalchemy python-dotenv psycopg2-binary
```

#### Frontend (React SPA)

```bash
cd client
npm install

# Scripts disponibles:
npm run dev      # Desarrollo (con hot reload) en localhost:5173
npm run build    # Build de producción → dist/
npm run preview  # Preview del build de producción
npm run lint     # Linting con ESLint
```

### Variables de Entorno

#### Root `.env` (ETL Pipeline)

| Variable | Descripción | Ejemplo |
|----------|------------|---------|
| `DATABASE_URL` | URL de conexión PostgreSQL a Supabase | `postgresql://postgres:***@db.your-project.supabase.co:5432/postgres` |

#### Client `.env` o `.env.local` (Frontend)

| Variable | Descripción | Ejemplo |
|----------|------------|---------|
| `VITE_SUPABASE_URL` | URL del proyecto Supabase | `https://xyzcompany.supabase.co` |
| `VITE_SUPABASE_ANON_KEY` | Clave pública anon de Supabase | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` |

> ⚠️ **Importante:** Nunca commitear archivos `.env` al repositorio. Usar `.env.example` como plantilla. El blueprint detectó que `client/.env` podría estar expuesto — verificar `.gitignore`.

### Configuración de Supabase

1. Crear proyecto en [Supabase](https://supabase.com) (región recomendada: São Paulo)
2. Copiar `Project URL` y `anon public key` de Settings > API
3. Ejecutar ETL pipeline (`python 00_full_run_pipeline.py`) para crear esquemas y vistas automáticamente
4. Verificar en SQL Editor que existen los esquemas: `raw` (2 tablas), `business` (11 objetos: 2 vistas + 7 MVs + 2 funciones RPC)

---

## 🔄 Pipeline ETL

El pipeline de datos se ejecuta con un solo comando y sigue un orden estricto de dependencias:

```bash
cd etl_pipeline
python 00_full_run_pipeline.py
```

### Secuencia de Ejecución

| Paso | Script | Función | Output | Depende de |
|------|--------|---------|--------|-----------|
| 01 | `generate_synthetic_data.py` | Genera datos sintéticos HR (IBM HR style, 6 países, 75 meses) | CSVs en `/data` | Nada |
| 02 | `setup_raw_layer.py` | Crea tablas raw en Supabase (columnas TEXT) | `raw."ibm_hr_monthly_snapshot_byNapo"`, `raw."ibm_hr_change_reasons_byNapo"` | 01 |
| 03 | `ingest_data.py` | Carga CSV → raw tables vía Pandas + SQLAlchemy | Datos en `raw.*` | 02 |
| 04 | `setup_business_core.py` | Crea vistas business con tipos correctos y columnas calculadas | `business.v_employee_full_bynapo`, `business.mv_ui_global_filters` | 03 |
| m05 | `m05_fuerza_laboral.py` | Data mart fuerza laboral (7 MVs + 1 vista recursiva + 2 RPCs) | 10 objetos en `business.*` | 04 |
| 90 | `generate_data_inventory.py` | Inventario de metadatos de todas las tablas/vistas | `docs/02-data-governance/02_supabase_metadata_inventory.md` | m05 |
| 91 | `export_data_samples.py` | Export de muestras de datos reales | `docs/02-data-governance/03_data_samples.md` | m05 |

### Dependencias del Pipeline

```
01 (DataGen) → 02 (Raw Schema) → 03 (Ingest) → 04 (Business Views) → m05 (Data Marts) → 90/91 (Docs)
```

### Reglas de Nomenclatura

| Prefijo | Significado | Ejemplo |
|---------|------------|---------|
| `00` | Orquestador / Master | `00_full_run_pipeline.py` |
| `01-04` | Core del pipeline | `01_generate_synthetic_data.py` |
| `m05+` | Módulos de dominio (data marts) | `m05_fuerza_laboral.py` |
| `90-99` | Post-pipeline / Metadata / Docs | `90_generate_data_inventory.py` |

> 📋 Para detalle completo de dependencias y reglas: Ver [`docs/PIPELINE_ORDER.md`](docs/PIPELINE_ORDER.md)

---

## 📁 Estructura del Proyecto

```
hr-analytics-dashboard/
│
├── 📂 client/                          # Frontend SPA (React 19 + Vite 8)
│   ├── 📂 src/
│   │   ├── 📂 modules/                 # Módulos por funcionalidad (14 carpetas)
│   │   │   ├── 00-layout/              # Componentes de layout (3 archivos)
│   │   │   │   ├── Sidebar.jsx         # Navegación colapsable estilo M365
│   │   │   │   ├── SectionLanding.jsx  # Landing page por módulo
│   │   │   │   └── Overview.jsx        # Dashboard C-Level (KPIs + barras)
│   │   │   ├── 05-fuerza-laboral/      # ✅ Módulo implementado (5 archivos)
│   │   │   │   ├── Demographics.jsx    # KPI cards + 4 gráficos (RPC)
│   │   │   │   ├── OrganigramaIntegral.jsx # Org chart (⚠️ mock)
│   │   │   │   ├── OrgStructure.jsx    # Posiciones (Supabase)
│   │   │   │   ├── EmployeeTable.jsx   # Auditoría de datos
│   │   │   │   └── hooks/
│   │   │   │       └── useDemographicsData.js  # Hook con filtros + RPC
│   │   │   ├── 06-nomina-costos/       # 🟡 Parcial (1 archivo)
│   │   │   │   └── Compensations.jsx   # Scatter plot (age vs daily rate)
│   │   │   └── [01-04, 07-13, 14]/     # 🔘 Pendientes (carpetas vacías)
│   │   ├── 📂 config/
│   │   │   └── navigation.js           # Configuración de navegación (13 módulos)
│   │   ├── 📂 lib/
│   │   │   └── supabaseClient.js       # Cliente Supabase inicializado
│   │   ├── App.jsx                     # Componente principal (routing por estado)
│   │   ├── main.jsx                    # Entry point de React
│   │   └── index.css                   # Tailwind CSS import
│   ├── 📂 public/                      # Assets estáticos (favicon, icons)
│   ├── package.json                    # 6 prod deps, 14 dev deps
│   ├── vite.config.js                  # Config con Tailwind + React plugins
│   ├── eslint.config.js                # Flat ESLint config
│   └── prisma.config.ts                # Prisma config (uso limitado)
│
├── 📂 etl_pipeline/                    # Scripts ETL (Python 3.11+)
│   ├── 00_full_run_pipeline.py         # Orquestador maestro secuencial
│   ├── 01_generate_synthetic_data.py   # Genera datos sintéticos (seed 42)
│   ├── 02_setup_raw_layer.py           # Crea schema raw (tablas TEXT)
│   ├── 03_ingest_data.py               # Ingesta CSV → raw tables
│   ├── 04_setup_business_core.py       # Vistas typed + filtros universales
│   ├── m05_fuerza_laboral.py           # Data mart: 7 MVs + 1 vista + 2 RPCs
│   ├── 90_generate_data_inventory.py   # Inventario de metadatos → MD
│   └── 91_export_data_samples.py       # Muestras de datos → MD
│
├── 📂 data/                            # Datos crudos (gitignored)
│   ├── ibm_hr_monthly_snapshot_byNapo.csv  # ~4K-6K rows × 36 cols
│   └── ibm_hr_change_reasons_byNapo.csv    # 4 rows (catálogo de razones)
│
├── 📂 docs/                            # Documentación (3 pilares)
│   ├── 📂 01-product-specs/            # Especificaciones de producto (manuales)
│   │   ├── 01_navigation_sitemap.md    # Árbol de navegación (13 módulos, 50+ vistas)
│   │   ├── 02_view_logic_specs.md      # Specs por vista con tags metodológicos
│   │   └── 03_design_system.md         # Design system: Corporate Slate & Blue
│   ├── 📂 02-data-governance/          # Gobernanza de datos (auto-generada)
│   │   ├── 02_supabase_metadata_inventory.md  # Metadata de 13 objetos DB
│   │   └── 03_data_samples.md                 # Muestras de datos reales
│   ├── 📂 03-ai-generated-content/     # Contenido generado por Qwen Code
│   │   ├── 01_project_blueprint.md     # Contexto maestro del proyecto
│   │   ├── 02_data_dictionary.md       # Diccionario de datos + linaje
│   │   └── 03_audit_report.md          # Auditoría completa de código
│   ├── 📂 prompts/                     # Prompts para Qwen Code Terminal
│   │   ├── 00. Blueprint & Context.md
│   │   ├── 01. Data Dictionary.md
│   │   ├── 02. Audit & Linting.md
│   │   └── 90_Update_README.md
│   └── PIPELINE_ORDER.md               # Orden de ejecución y dependencias
│
├── .gitignore                          # Reglas de exclusión (.env, CSVs, node_modules)
├── .env                                # Variables de entorno (gitignored)
└── README.md                           # Este documento
```

**Total: 48+ archivos** (excluyendo `node_modules`, `.git`, `dist`, `__pycache__`)

---

## 🗄️ Base de Datos

### Arquitectura Medallion

El pipeline implementa una arquitectura **Medallion** (Bronce → Plata → Oro) con 13 objetos de base de datos:

```
CSV Files → RAW (Bronce/TEXT) → BUSINESS (Silver/Typed) → DATA MARTS (Gold/Specialized)
```

### Capa RAW (Bronce — Aterrizaje)

**Propósito:** Landing de datos crudos sin transformación. Todas las columnas en formato `TEXT` para evitar format lock-in durante la ingesta CSV. La tipificación se aplica en la capa Business.

| Tabla | Columnas | Completitud | Descripción |
|-------|----------|-------------|-------------|
| `raw."ibm_hr_monthly_snapshot_byNapo"` | 36 (incl. `created_at`) | 100% en columnas clave | Snapshots mensuales IBM HR (employee_id, snapshot_date como PK compuesta) |
| `raw."ibm_hr_change_reasons_byNapo"` | 7 (incl. `created_at`) | 100% | Catálogo de razones de cambio (SAL-IPC, TER-VOL, TER-INV, TER-RET) |

**Columnas principales de la tabla principal:** `snapshot_date`, `employee_id`, `employee_code`, `full_name`, `gender`, `country_iso3`, `department_name`, `job_role`, `job_level_1`, `job_level_2`, `employment_status`, `hire_date`, `termination_date`, `monthly_salary_local`, `currency_iso3`, `fx_rate_to_usd`, `monthly_salary_usd`, `manager_employee_id`, `work_center_id`, `work_modality`, `education_level`, `marital_status`, `dependents_count`

### Capa BUSINESS (Silver — Transformación)

**Propósito:** Vistas transformadas con tipos de datos correctos y reglas de negocio aplicadas. Única fuente de verdad para consumo analítico.

| Vista | Columnas | Descripción |
|-------|----------|-------------|
| `business.v_employee_full_bynapo` | 22 (19 fuente + 3 calculadas) | Vista maestra de empleados con tipos: DATE, INTEGER, NUMERIC(12,2), BOOLEAN |
| `business.mv_ui_global_filters` | 1 (JSON) | 6 filtros universales como JSON: periods, countries, departments, job_levels_1/2, work_centers |

**Reglas de negocio aplicadas en `v_employee_full_bynapo`:**

| Columna | Tipo | Regla |
|---------|------|-------|
| `tenure_months` | INTEGER | `EXTRACT(YEAR FROM AGE(snapshot_date, hire_date)) * 12 + EXTRACT(MONTH FROM AGE(...))` |
| `is_active_at_snapshot` | BOOLEAN | TRUE si `employment_status='Active'` O `termination_date IS NULL` O `termination_date >= snapshot_date` |
| `processed_at` | TIMESTAMP | `NOW()` — timestamp de procesamiento |

### Capa DATA MARTS (Gold — Especialización)

**Propósito:** Vistas materializadas y vistas especializadas por módulo funcional para consumo analítico directo del frontend.

#### Módulo Fuerza Laboral (m05)

| Vista/MV | Tipo | Métricas | Gráfico Frontend | Filtrado por |
|----------|------|----------|-----------------|-------------|
| `mv_monthly_kpis_bynapo` | MV | headcount_active, headcount_terminated, avg_salary_usd, avg_tenure | Tendencia mensual por país | 6 filtros universales |
| `mv_demographics_agg` | MV | total_hc, altas, bajas | Tarjetas KPI principales | 6 filtros universales |
| `mv_diversity_pyramid` | MV | count por género | Pirámide de diversidad | gender + job_level_1 |
| `mv_bajas_heatmap` | MV | count (bajas) | Heatmap de rotación | snapshot × department |
| `mv_country_dist` | MV | value (count) | Distribución geográfica | country_iso3 |
| `mv_experience_bubbles` | MV | avg_salary, emp_count, tenure_bucket | Burbujas experiencia/salario | tenure_bucketed (<1, 1-3, 3-6, 6+ años) |
| `v_org_tree_bynapo` | Vista Recursiva | Jerarquía con depth ≤ 10 | Organigrama ECharts | Recursive CTE desde CEO |

**Todas las MVs tienen 100% de completitud** y están filtradas por 6 dimensiones universales: `snapshot_date`, `country_iso3`, `department_name`, `job_level_1`, `job_level_2`, `work_center_id`.

#### Funciones RPC

| Función | Parámetros (6) | Retorno | Componente Frontend |
|---------|---------------|---------|---------------------|
| `get_demographics_dashboard` | p_period_date, p_country, p_department, p_job_level_1, p_job_level_2, p_work_center | JSON (3 KPI cards + sparklines) | `Demographics.jsx` — Cards principales |
| `get_advanced_demographics` | (mismos 6 parámetros) | JSON (4 gráficos: pyramid, heatmap, distribution, bubbles) | `Demographics.jsx` — Gráficos avanzados |

**Permisos:** `GRANT EXECUTE ON FUNCTION ... TO anon` en ambas funciones.

### Inventario Completo de Objetos de Base de Datos

| # | Esquema | Objeto | Tipo | Script Origen |
|---|---------|--------|------|--------------|
| 1 | `raw` | `ibm_hr_monthly_snapshot_byNapo` | TABLE | 02 |
| 2 | `raw` | `ibm_hr_change_reasons_byNapo` | TABLE | 02 |
| 3 | `business` | `v_employee_full_bynapo` | VIEW | 04 |
| 4 | `business` | `mv_ui_global_filters` | MATERIALIZED VIEW | 04 |
| 5 | `business` | `v_org_tree_bynapo` | VIEW (Recursive CTE) | m05 |
| 6 | `business` | `mv_monthly_kpis_bynapo` | MATERIALIZED VIEW | m05 |
| 7 | `business` | `mv_demographics_agg` | MATERIALIZED VIEW | m05 |
| 8 | `business` | `mv_diversity_pyramid` | MATERIALIZED VIEW | m05 |
| 9 | `business` | `mv_bajas_heatmap` | MATERIALIZED VIEW | m05 |
| 10 | `business` | `mv_country_dist` | MATERIALIZED VIEW | m05 |
| 11 | `business` | `mv_experience_bubbles` | MATERIALIZED VIEW | m05 |
| 12 | `business` | `get_demographics_dashboard` | FUNCTION (RPC) | m05 |
| 13 | `business` | `get_advanced_demographics` | FUNCTION (RPC) | m05 |

**Total: 13 objetos** (2 tablas + 2 vistas + 7 vistas materializadas + 2 funciones RPC)

### Datos Sintéticos — Reglas de Negocio

| Parámetro | Valor | Detalle |
|-----------|-------|---------|
| **Países** | 6 | PER, CHL, COL, MEX, ESP, USA |
| **Departamentos** | 5 | IT, Sales, HR, Finance, Operations |
| **Período** | 75 meses | Enero 2020 — Marzo 2026 |
| **Empleados iniciales** | 4,000 | Pool seed con random seed 42 |
| **Empleados/mes** | ~4,000-6,000 | Con rotación y nuevas contrataciones |
| **Rotación mensual** | 0.5% | 70% voluntaria, 20% involuntaria, 10% jubilación |
| **Nuevas contrataciones** | 1% del pool base (~40/mes) | Individual Contributor / Junior |
| **FX rate** | 3.50 (fijo para todos) | `monthly_salary_usd = monthly_salary_local / 3.50` |
| **IPC PER** | +4% en febrero | `salary_change_flag = 1`, reason = `SAL-IPC` |
| **IPC ESP** | +3% en enero | Igual |
| **IPC CHL** | +3.5% en julio | Igual |
| **Monedas** | 6 | PEN, CLP, COP, MXN, EUR, USD |
| **Job Levels 1** | 2 | Management, Individual Contributor |
| **Job Levels 2** | 3 | Junior, Senior, Lead |
| **Roles** | 17 | CEO, CFO, CTO, Manager, HR Specialist, Data Analyst, DevOps, etc. |
| **Coordenadas** | País central ± 0.05° jitter | Lat/Lon por país |

---

## 🏆 Calidad del Código

> **Fuente:** `docs/03-ai-generated-content/03_audit_report.md` (generado automáticamente 2026-04-11)

### Score de Calidad: 76/100

| Pilar | Score | Detalle |
|-------|-------|---------|
| **Seguridad** | 18/25 | `.env` posible expuesto, falta RLS awareness, riesgo XSS en tooltip ECharts |
| **Limpieza de Código** | 20/25 | `OrganigramaIntegral.jsx` 100% mock, imports React no usados |
| **Buenas Prácticas** | 17/25 | CERO `aria-label` en íconos Lucide (~30+), fetch eager sin lazy loading |
| **Consistencia** | 21/25 | Naming español/inglés mezclado, temas visuales mixtos, IDs de vistas hardcodeados |

### Hallazgos por Severidad

| Severidad | Count | Top Issues |
|-----------|-------|-----------|
| 🔴 Crítico | 3 | `.env` expuesto, `OrganigramaIntegral` mock completo, accesibilidad (0 aria-labels) |
| 🟡 Moderado | 10 | Imports React no usados, botón a ruta inexistente, nombre hardcodeado en footer, fetch eager |
| 🟢 Menor | 5 | Doble import lucide-react, key posible duplicada, sin PropTypes, mezcla de idiomas |

### Top 3 Prioridades de Corrección

1. **Proteger `.env`** — Agregar a `.gitignore` del client, crear `.env.example`, rotar anon key expuesta
2. **Conectar `OrganigramaIntegral` a datos reales** — Usar `business.v_org_tree_bynapo` o marcar como placeholder
3. **Agregar `aria-hidden="true"` a todos los íconos** — 30+ cambios en 5 archivos para accesibilidad WCAG 2.1

---

## 📚 Documentación

El proyecto sigue un modelo de documentación de **3 pilares** con generación automática:

### Pilar 1: Especificaciones de Producto (Manuales)

| Documento | Ubicación | Descripción |
|-----------|----------|-------------|
| Navegación & Sitemap | [`docs/01-product-specs/01_navigation_sitemap.md`](docs/01-product-specs/01_navigation_sitemap.md) | Árbol completo de 13 módulos y 50+ vistas con iconos |
| Lógica de Vistas | [`docs/01-product-specs/02_view_logic_specs.md`](docs/01-product-specs/02_view_logic_specs.md) | Specs detalladas por vista con tags metodológicos (DESC, PRED, ML, IA, NLP, OPT, XAI) |
| Design System | [`docs/01-product-specs/03_design_system.md`](docs/01-product-specs/03_design_system.md) | Guía completa: paleta Corporate Slate & Blue, tipografía, arquitectura de vistas, reglas ECharts |

### Pilar 2: Gobernanza de Datos (Auto-generada por scripts Python)

| Documento | Generado Por | Descripción |
|-----------|-------------|-------------|
| Metadata Inventory | Script 90 (`generate_data_inventory.py`) | Inventario completo de 13 objetos DB: columnas, tipos, completitud %, valores únicos, muestras |
| Data Samples | Script 91 (`export_data_samples.py`) | Muestras reales de datos de las vistas business |

### Pilar 3: Contenido Generado por IA (Qwen Code Terminal)

| Documento | Prompt | Descripción |
|-----------|--------|-------------|
| Project Blueprint | Prompt 00 | Contexto maestro: estructura, dependencias, arquitectura de datos, pipeline ETL, estado frontend, variables de entorno, score de madurez |
| Data Dictionary | Prompt 01 | Diccionario de datos completo: linaje, capas raw/business/data marts, funciones RPC, reglas de simulación, diagrama ER |
| Audit Report | Prompt 02 | Auditoría completa: hallazgos (18), score de calidad (76/100), seguridad, limpieza de código, buenas prácticas, correcciones con diffs |

### Ejecutar Prompts de Documentación

```bash
# Desde la terminal de Qwen Code:
"Ejecuta el prompt 00 para generar el Blueprint"
"Ejecuta el prompt 01 para generar el Data Dictionary"
"Ejecuta el prompt 02 para generar el Audit Report"
"Ejecuta el prompt 90 para actualizar el README"  # ← Este prompt
```

> 📋 Para orden de ejecución completo, dependencias cruzadas y reglas de oro: Ver [`docs/PIPELINE_ORDER.md`](docs/PIPELINE_ORDER.md)

---

## 🤝 Contribuir

### Flujo de Trabajo

1. Fork el repositorio
2. Crear rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add: AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

### Estándares de Código

- **Frontend:** ESLint configurado con react-hooks y react-refresh plugins. Tailwind CSS 4.2.
- **Backend:** Python 3.11+ con type hints donde sea posible. Pandas + SQLAlchemy.
- **Commits:** Mensajes descriptivos y concisos.
- **Documentación:** Actualizar README y docs cuando se agreguen features. Ejecutar Prompt 90 al finalizar.

### Design System — Reglas Clave

El proyecto usa el design system **"Corporate Slate & Blue"**:

- 🚫 **Prohibido:** `text-black`, `text-gray-900`, `indigo`, `purple`, `violet`, `fuchsia`, `red` puro
- ✅ Textos principales: `text-slate-800`
- ✅ Textos secundarios: `text-slate-500`
- ✅ Acentos: `text-blue-700`
- ✅ Fondos de tarjetas: `bg-white border-slate-200`
- ✅ Badges: `bg-blue-50`

> Para guía completa: Ver [`docs/01-product-specs/03_design_system.md`](docs/01-product-specs/03_design_system.md)

### Agregar Nuevo Módulo

1. Crear carpeta en `client/src/modules/XX-nombre-modulo/`
2. Crear componente principal (ej. `Dashboard.jsx`) — ir directo al contenido (sin títulos introductorios)
3. Actualizar `client/src/config/navigation.js` con nueva entrada (id, title, icon, description, tags)
4. Importar y rutear en `client/src/App.jsx` (agregar a `vistaActual` conditional)
5. Crear script ETL en `etl_pipeline/mXX_nombre_modulo.py` si requiere vistas nuevas en BD
6. Ejecutar pipeline: `python etl_pipeline/00_full_run_pipeline.py`
7. Actualizar este README ejecutando: `"Ejecuta el prompt 90 para actualizar el README"`

### Reglas ECharts

- **Cero hardcoding:** Prohibido quemar categorías, meses o departamentos (ej. `['IT', 'Sales']`) en opciones de ECharts
- Todos los ejes (`xAxis`/`yAxis`) y series deben generarse dinámicamente mapeando la respuesta del backend
- Usar paleta apastelada o escala de azules/pizarras corporativos — evitar colores primarios puros

---

## 📄 Licencia

[ESPECIFICAR LICENCIA — MIT, Apache 2.0, etc.]

> ⚠️ La licencia del proyecto aún no ha sido definida. Se recomienda definir una antes de hacer el repositorio público.

---

## 👨‍💻 Sobre el Desarrollador

**Jesús Napoleón "Napo" Villegas Gálvez**
*Data Engineer & AI Specialist | Corporate Data Architect*

Profesional híbrido especializado en traducir operaciones de negocio complejas en arquitecturas de datos escalables. Con formación en gestión corporativa y actualmente cursando una Maestría en Data Analytics & Inteligencia Artificial (ESAN), diseño soluciones integrales (Data Mesh, ETL, predicción ML) que impactan directamente en la rentabilidad de las empresas.

---

## 📞 Soporte

| Canal | Enlace |
|-------|--------|
| **Issues** | `<repository-url>/issues` |
| **Discusiones** | `<repository-url>/discussions` |
| **Documentación Completa** | Carpeta `docs/` (3 pilares, 8+ documentos) |
| **Supabase Dashboard** | https://app.supabase.com/project/YOUR_PROJECT |

---

## 📊 Métricas del Proyecto

### Alcance Funcional

| Métrica | Valor | Fuente |
|---------|-------|--------|
| **Módulos Totales** | 13 | `docs/01-product-specs/01_navigation_sitemap.md` |
| **Módulos Implementados** | 2 de 14 (14%) | `client/src/App.jsx` + `docs/03-ai-generated-content/01_project_blueprint.md` |
| **Vistas Totales** | 50+ | `docs/01-product-specs/01_navigation_sitemap.md` |
| **Vistas Implementadas** | 6 de 50+ (~12%) | `client/src/App.jsx` (routing real) |
| **Vistas en Progreso** | 44+ | Blueprint + navigation.js |
| **Panel de Administración** | 2 vistas (roles_permisos, conexiones_etl) | `navigation.js` |
| **Tags Utilizados** | DESC, PRED, ML, IA, NLP, OPT, XAI | `docs/01-product-specs/02_view_logic_specs.md` |

### Pipeline ETL

| Métrica | Valor | Fuente |
|---------|-------|--------|
| **Scripts ETL** | 8 (01-04, m05, 90-91 + orquestador 00) | `etl_pipeline/` + `docs/PIPELINE_ORDER.md` |
| **Capas de Datos** | 3 (Raw, Business, Data Marts) | `docs/03-ai-generated-content/02_data_dictionary.md` |
| **Tablas Raw** | 2 | `docs/02-data-governance/02_supabase_metadata_inventory.md` |
| **Vistas Business** | 2 (1 vista + 1 MV) | metadata_inventory |
| **Data Marts (m05)** | 8 (7 MVs + 1 vista recursiva) | metadata_inventory + data_dictionary |
| **Funciones RPC** | 2 | data_dictionary |
| **Objetos DB Totales** | 13 | data_dictionary |
| **Completitud de Datos** | 100% en columnas clave | metadata_inventory |
| **Países** | 6 (PER, CHL, COL, MEX, ESP, USA) | `docs/03-ai-generated-content/01_project_blueprint.md` |
| **Departamentos** | 5 (IT, Sales, HR, Finance, Operations) | blueprint |
| **Período de Datos** | Ene 2020 — Mar 2026 (75 meses) | blueprint |
| **Empleados/Mes** | ~4,000-6,000 | blueprint |

### Stack Tecnológico

| Métrica | Valor | Fuente |
|---------|-------|--------|
| **Dependencias Frontend (prod)** | 6 | `client/package.json` |
| **Dependencias Frontend (dev)** | 14 | `client/package.json` |
| **Dependencias Backend (Python)** | 5 (Pandas, NumPy, SQLAlchemy, python-dotenv, psycopg2) | blueprint + scripts |
| **Framework UI** | React 19.2.4 + Vite 8.0.1 | package.json |
| **Estilos** | Tailwind CSS 4.2.2 | package.json |
| **Visualización** | Apache ECharts 6.0.0 + echarts-for-react 3.0.6 | package.json |
| **Iconos** | Lucide React 1.7.0 | package.json |
| **Database** | Supabase (PostgreSQL) — proyecto `hr-analytics-db`, región São Paulo | blueprint |

### Calidad del Código

| Métrica | Valor | Fuente |
|---------|-------|--------|
| **Score de Calidad** | 76/100 | `docs/03-ai-generated-content/03_audit_report.md` |
| **Hallazgos Críticos** | 3 🔴 | audit_report |
| **Advertencias** | 10 🟡 | audit_report |
| **Sugerencias** | 5 🟢 | audit_report |
| **Total Hallazgos** | 18 | audit_report |
| **Accesibilidad** | ⚠️ 0 aria-labels en ~30+ íconos | audit_report |

### Cobertura de Documentación

| Métrica | Valor | Fuente |
|---------|-------|--------|
| **Product Specs** | ✅ 3/3 completos | `docs/01-product-specs/` |
| **Data Governance** | ✅ 2/2 generados | `docs/02-data-governance/` |
| **AI-Generated Content** | ✅ 3/3 generados | `docs/03-ai-generated-content/` |
| **Blueprint** | ✅ 2026-04-11T06:30:00Z | `01_project_blueprint.md` |
| **Data Dictionary** | ✅ 2026-04-11T06:32:00Z | `02_data_dictionary.md` |
| **Audit Report** | ✅ 2026-04-11T06:35:00Z | `03_audit_report.md` |
| **Metadata Inventory** | ✅ 2026-04-11T06:25:54Z | `02_supabase_metadata_inventory.md` |
| **Data Samples** | ✅ 2026-04-11T06:15:50Z | `03_data_samples.md` |
| **Pipeline Order** | ✅ Actualizado | `docs/PIPELINE_ORDER.md` |
| **Prompts Disponibles** | 4 (00, 01, 02, 90) | `docs/prompts/` |

### Última Actualización

| Métrica | Valor |
|---------|-------|
| **README** | 2026-04-11 15:37:25 UTC |
| **Versión del Proyecto** | v0.0.0 (de package.json) |
| **Estado del Proyecto** | 🟡 En desarrollo activo (2 módulos implementados, 12 pendientes) |

---

## 📝 Historial de Actualizaciones

| Fecha | Versión | Cambios Principales | Autor |
|-------|---------|---------------------|-------|
| 2026-04-11 15:37:25 UTC | v0.0.0 | README actualizado via Prompt 90. Sección "Sobre el Desarrollador" agregada. Timestamp actualizado. | Qwen Code Terminal (Prompt 90) |
| 2026-04-11 14:47:25 UTC | v0.0.0 | README actualizado (Prompt 90). Re-ejecución tras cambios manuales del usuario. Fuentes: 8 documentos + código fuente verificado. | Qwen Code Terminal (Prompt 90) |
| 2026-04-11 14:10:27 UTC | v0.0.0 | README re-escrito completamente con mejores prácticas 2024-2025. Fuentes: 8 documentos + código. Métricas cruzadas, DB documentada, audit score incluido. | Qwen Code Terminal (Prompt 90) |

> 💡 **Nota:** Este README se actualiza automáticamente con cada ejecución del Prompt 90.
> Incluye métricas frescas del proyecto, estado de módulos, documentación completa de base de datos,
> score de calidad de código, y toda la información recopilada de **8+ fuentes documentales**.

---

## 🔗 Flujo Completo de Documentación y Ejecución

```
FASE 0: PIPELINE ETL
  python etl_pipeline/00_full_run_pipeline.py
  └─ Genera: datos + vistas DB + docs de gobernanza (scripts 90-91)

FASE 1: PROMPTS DE CONTEXTO (Qwen Code Terminal)
  "Ejecuta el prompt 00" → docs/03-ai-generated-content/01_project_blueprint.md
  "Ejecuta el prompt 01" → docs/03-ai-generated-content/02_data_dictionary.md
  "Ejecuta el prompt 02" → docs/03-ai-generated-content/03_audit_report.md

FASE 2: ACTUALIZACIÓN README
  "Ejecuta el prompt 90" → README.md (este documento)
  └─ Consume: product-specs + data-governance + ai-content + pipeline-order + código

FASE 3: DESARROLLO FRONTEND
  cd client && npm run dev
  └─ Agregar módulos nuevos siguiendo guía de Contribución
```

---

<div align="center">

**Hecho con ❤️ por Jesús "Napo" Villegas**

[⬆️ Volver al inicio](#-enterprise-hr-analytics-dashboard--gdh-analytics)

</div>
