# 📋 Project Context Dump — HR Analytics Dashboard
> **Generado:** 2026-04-07 | **Autor:** Technical Architecture Agent
> **Propósito:** Documentación completa de arquitectura, datos y código fuente para sincronización entre equipos y agentes de IA.

---

## 1. Estructura de Directorios (Tree)

```
hr-analytics-dashboard/
├── .env                                          # Variables de entorno (Backend + Supabase)
├── .gitignore
├── README.md
├── project_context_dump.md                       # ← Este archivo
├── readme_update_brief.md                        # Brief para actualizar el README
│
├── data/
│   ├── ibm_hr.csv                                # Dataset original IBM (1,470 registros, estático)
│   └── ibm_hr_monthly_snapshot_byNapo.csv        # Dataset mejorado (~450K registros, 75 meses)
│
├── etl_pipeline/
│   ├── 00_full_run_pipeline.py                   # Orquestador maestro (ejecuta 01→07)
│   ├── 01_setup_raw.py                           # Crea esquema raw + tabla ibm_hr_landing
│   ├── 02_ingest_data.py                         # Ingesta ibm_hr.csv → raw.ibm_hr_landing
│   ├── 03_setup_business.py                      # Vista business.ibm_hr (base)
│   ├── 04_create_enhanced_dataset_byNapo.py      # Genera dataset de series temporales
│   ├── 05_setup_raw_enhanced_byNapo.py           # DDL tablas raw mejoradas (byNapo)
│   ├── 06_ingest_enhanced_byNapo.py              # Ingesta masiva del snapshot mensual
│   └── 07_setup_business_enhanced_byNapo.py      # Capa business mejorada (Clean Slate)
│
└── client/                                       # Frontend React + Vite
    ├── .env                                      # Variables Supabase (VITE_*)
    ├── index.html
    ├── package.json
    ├── vite.config.js
    ├── eslint.config.js
    ├── prisma.config.ts
    ├── docs/
    │   └── prompts/                              # Prompts de documentación
    │       ├── context_dump.md
    │       └── readme_update_brief.md
    ├── public/
    │   ├── favicon.svg
    │   └── icons.svg
    └── src/
        ├── main.jsx                              # Entry point React
        ├── App.jsx                               # Router/renderizado condicional
        ├── index.css
        ├── lib/
        │   └── supabaseClient.js                 # Configuración Supabase SDK
        └── components/
            ├── Sidebar.jsx                       # Menú lateral colapsable (MS365 style)
            ├── Overview.jsx                      # Dashboard principal con KPIs + ECharts
            ├── OrgStructure.jsx                  # Landing Estructura Organizativa
            ├── OrganigramaIntegral.jsx           # Organigrama jerárquico visual
            ├── Compensations.jsx                 # Análisis de compensaciones (Scatter)
            └── EmployeeTable.jsx                 # Tabla de auditoría de datos
```

> **Excluidos del árbol:** `node_modules/`, `.git/`, `venv/`, `__pycache__/`, `package-lock.json`

---

## 2. Dependencias y Entorno

### 2.1 Python (Backend / ETL Pipeline)

> ⚠️ **No existe `requirements.txt` formal.** Dependencias inferidas del código fuente:

| Librería | Usada en | Propósito |
|----------|----------|-----------|
| `pandas` | 01, 02, 04, 06 | Manipulación de DataFrames y lectura/escritura CSV |
| `numpy` | 04 | Generación de datos aleatorios (distribuciones) |
| `sqlalchemy` | 01–03, 05–07 | Conexión ORM a PostgreSQL/Supabase |
| `psycopg2` | (dep. de SQLAlchemy) | Driver nativo PostgreSQL |
| `python-dotenv` | 01–03, 05–07 | Lectura de variables `.env` |
| `networkx` | 04 (importado, uso futuro) | Validación de grafos dirigidos acíclicos |

### 2.2 Node.js / React (Frontend)

**`dependencies`** (producción):
```json
{
  "@supabase/supabase-js": "^2.101.1",
  "echarts": "^6.0.0",
  "echarts-for-react": "^3.0.6",
  "lucide-react": "^1.7.0",
  "react": "^19.2.4",
  "react-dom": "^19.2.4"
}
```

**`devDependencies`** (desarrollo):
```json
{
  "@eslint/js": "^9.39.4",
  "@tailwindcss/vite": "^4.2.2",
  "@types/react": "^19.2.14",
  "@types/react-dom": "^19.2.3",
  "@vitejs/plugin-react": "^6.0.1",
  "autoprefixer": "^10.4.27",
  "dotenv": "^17.4.1",
  "eslint": "^9.39.4",
  "eslint-plugin-react-hooks": "^7.0.1",
  "eslint-plugin-react-refresh": "^0.5.2",
  "globals": "^17.4.0",
  "postcss": "^8.5.8",
  "prisma": "^7.6.0",
  "tailwindcss": "^4.2.2",
  "vite": "^8.0.1"
}
```

---

## 3. Modelado de Base de Datos y Arquitectura de Datos

### 3.1 Arquitectura Medallion

```
              ┌─────────────────────────────────────────────────┐
              │              SUPABASE (PostgreSQL)              │
              │                                                 │
  CSV files   │  ┌──────────┐         ┌────────────────────┐   │
  ─────────►  │  │  raw     │ ──────► │     business       │   │  ──► React/ECharts
              │  │ (Bronce) │  Vistas │      (Oro)         │   │
              │  └──────────┘         └────────────────────┘   │
              └─────────────────────────────────────────────────┘
```

### 3.2 Esquema `raw` — Tablas

#### Tabla: `raw.ibm_hr_landing` (Creada por ETL 01)
> Dataset IBM original. Columnas dinámicas detectadas desde CSV headers.

| Columna | Tipo | Notas |
|---------|------|-------|
| `employeenumber` | TEXT | ID del empleado (se castea a INT en capa business) |
| `age` | TEXT | Edad |
| `department` | TEXT | Departamento |
| `jobrole` | TEXT | Rol |
| `attrition` | TEXT | 'Yes' / 'No' |
| `gender` | TEXT | Género |
| `dailyrate` | TEXT | Tarifa diaria |
| `monthlyincome` | TEXT | Ingreso mensual |
| `totalworkingyears` | TEXT | Años laborados totales |
| `yearsatcompany` | TEXT | Años en la empresa |
| `distancefromhome` | TEXT | Distancia al trabajo |
| *(+24 columnas adicionales)* | TEXT | Todas como TEXT para ingesta segura |
| `created_at` | TIMESTAMPTZ | Default `NOW()` |

#### Tabla: `raw.ibm_hr_monthly_snapshot_byNapo` (Creada por ETL 05)
> Dataset mejorado con series de tiempo mensuales.

| Columna | Tipo | Notas |
|---------|------|-------|
| `snapshot_date` | TEXT | Fecha del snapshot mensual (YYYY-MM-DD) |
| `employee_id` | TEXT | ID numérico del empleado |
| `employee_code` | TEXT | Código alfanumérico (EMP-XXXXX) |
| `full_name` | TEXT | Nombre completo |
| `gender` | TEXT | Male / Female |
| `nationality_iso3` | TEXT | ISO 3166-1 alpha-3 |
| `country_iso3` | TEXT | País de trabajo ISO3 |
| `department_name` | TEXT | Departamento |
| `job_role` | TEXT | Rol laboral |
| `job_level_1` | TEXT | Nivel jerárquico 1 (Individual Contributor / Management) |
| `job_level_2` | TEXT | Nivel jerárquico 2 (Junior / Senior / Lead) |
| `employment_status` | TEXT | Active / Terminated |
| `hire_date` | TEXT | Fecha de ingreso |
| `termination_date` | TEXT | Fecha de cese (nullable) |
| `termination_reason_legal` | TEXT | Motivo legal de cese |
| `turnover_classification_company` | TEXT | Clasificación interna de rotación |
| `monthly_salary_local` | TEXT | Salario en moneda local |
| `currency_iso3` | TEXT | Código de moneda ISO |
| `fx_rate_to_usd` | TEXT | Tipo de cambio a USD |
| `monthly_salary_usd` | TEXT | Salario convertido a USD |
| `manager_employee_id` | TEXT | ID del jefe directo |
| `dotted_line_manager_id` | TEXT | ID del jefe funcional |
| `work_center_id` | TEXT | Centro de trabajo |
| `home_lat` | TEXT | Latitud del domicilio |
| `home_lon` | TEXT | Longitud del domicilio |
| `work_modality` | TEXT | Presencial / Remoto / Hybrid |
| `education_level` | TEXT | Nivel educativo |
| `education_status` | TEXT | Estado de estudios |
| `marital_status` | TEXT | Estado civil |
| `dependents_count` | TEXT | Número de dependientes |
| `salary_change_flag` | TEXT | Flag de cambio salarial |
| `salary_change_reason_code` | TEXT | Código de motivo de cambio |
| `job_change_flag` | TEXT | Flag de cambio de puesto |
| `exit_interview_completed` | TEXT | Entrevista de salida completada |
| `regrettable_loss_flag` | TEXT | Pérdida lamentable |
| `created_at` | TIMESTAMPTZ | Default `NOW()` |

#### Tabla: `raw.ibm_hr_change_reasons_byNapo` (Creada por ETL 05)
> Catálogo de motivos de cambio (actualmente vacía, lista para ingesta futura).

| Columna | Tipo |
|---------|------|
| `reason_code` | TEXT |
| `reason_name_es` | TEXT |
| `reason_name_en` | TEXT |
| `affects_salary` | TEXT |
| `affects_job` | TEXT |
| `active_flag` | TEXT |
| `created_at` | TIMESTAMPTZ |

### 3.3 Esquema `business` — Vistas Analíticas

> El esquema `business` se reconstruye desde cero con `DROP SCHEMA ... CASCADE` en cada ejecución (estrategia Clean Slate).

#### Vista: `business.ibm_hr` (Creada por ETL 03)
> Vista simple sobre el dataset IBM original con casting de tipos.

| Columna resultante | Tipo casteado | Origen |
|--------------------|---------------|--------|
| `id` | INTEGER | `employeenumber` |
| `age` | INTEGER | `age` |
| `department` | TEXT | `department` |
| `jobrole` | TEXT | `jobrole` |
| `attrition` | TEXT | `attrition` |
| `gender` | TEXT | `gender` |
| `dailyrate` | INTEGER | `dailyrate` |
| `monthlyincome` | INTEGER | `monthlyincome` |
| `totalworkingyears` | INTEGER | `totalworkingyears` |
| `yearsatcompany` | INTEGER | `yearsatcompany` |
| `distancefromhome` | INTEGER | `distancefromhome` |

#### Vista: `business.v_employee_full_byNapo` (Creada por ETL 07)
> Vista maestra tipada con casting defensivo (`NULLIF`) y campos calculados.

| Columna | Tipo | Notas |
|---------|------|-------|
| `snapshot_date` | DATE | Casteado desde TEXT |
| `employee_id` | INTEGER | Casteado desde TEXT |
| `employee_code` | TEXT | — |
| `full_name` | TEXT | — |
| `gender` | TEXT | — |
| `nationality_iso3` | TEXT | — |
| `country_iso3` | TEXT | — |
| `home_lat` | NUMERIC(10,6) | Con `NULLIF('', '')` |
| `home_lon` | NUMERIC(10,6) | Con `NULLIF('', '')` |
| `work_center_id` | TEXT | — |
| `work_modality` | TEXT | — |
| `department_name` | TEXT | — |
| `job_role` | TEXT | — |
| `job_level_1` | TEXT | — |
| `job_level_2` | TEXT | — |
| `employment_status` | TEXT | — |
| `hire_date` | DATE | Con `NULLIF` |
| `termination_date` | DATE | Con `NULLIF` |
| `termination_reason_legal` | TEXT | — |
| `turnover_classification_company` | TEXT | — |
| `monthly_salary_local` | NUMERIC(12,2) | Con `NULLIF` |
| `currency_iso3` | TEXT | — |
| `fx_rate_to_usd` | NUMERIC(10,6) | Con `NULLIF` |
| `monthly_salary_usd` | NUMERIC(12,2) | Con `NULLIF` |
| `manager_employee_id` | INTEGER | Con `NULLIF` |
| `dotted_line_manager_id` | INTEGER | Con `NULLIF` |
| `education_level` | TEXT | — |
| `education_status` | TEXT | — |
| `marital_status` | TEXT | — |
| `dependents_count` | INTEGER | Con `NULLIF` |
| `salary_change_flag` | BOOLEAN | Calculado: `'1'` o `'true'` |
| `salary_change_reason_code` | TEXT | — |
| `job_change_flag` | BOOLEAN | Calculado: `'1'` o `'true'` |
| `exit_interview_completed` | BOOLEAN | Calculado |
| `regrettable_loss_flag` | BOOLEAN | Calculado |
| `tenure_months` | NUMERIC | **Calculado:** Antigüedad en meses |
| `is_active_at_snapshot` | BOOLEAN | **Calculado:** Flag de actividad |
| `processed_at` | TIMESTAMPTZ | `NOW()` |

#### Vista: `business.v_org_tree_byNapo` (Creada por ETL 07)
> CTE recursiva para organigramas con prevención de ciclos y profundidad máxima 10.

| Columna | Tipo | Notas |
|---------|------|-------|
| `employee_id` | INTEGER | — |
| `full_name` | TEXT | — |
| `job_role` | TEXT | — |
| `job_level_1` | TEXT | — |
| `job_level_2` | TEXT | — |
| `department_name` | TEXT | — |
| `country_iso3` | TEXT | — |
| `work_center_id` | TEXT | — |
| `manager_employee_id` | INTEGER | — |
| `depth` | INTEGER | Nivel jerárquico (0 = raíz) |
| `path_ids` | INTEGER[] | Camino de IDs desde raíz |
| `path_names` | TEXT[] | Camino de nombres desde raíz |
| `echarts_node` | JSON | Nodo preformateado para ECharts |

#### Vista Materializada: `business.mv_monthly_kpis_byNapo` (Creada por ETL 07)
> KPIs mensuales agrupados. Índice único para soporte de `REFRESH CONCURRENTLY`.

| Columna | Tipo | Notas |
|---------|------|-------|
| `snapshot_date` | DATE | PK compuesta (parte del UNIQUE INDEX) |
| `country_iso3` | TEXT | PK compuesta |
| `department_name` | TEXT | PK compuesta |
| `job_level_1` | TEXT | PK compuesta |
| `headcount_active` | BIGINT | Empleados activos |
| `headcount_terminated` | BIGINT | Empleados cesados |
| `headcount_total` | BIGINT | Total |
| `avg_salary_usd` | NUMERIC | Promedio salario USD |
| `min_salary_usd` | NUMERIC | Mínimo |
| `max_salary_usd` | NUMERIC | Máximo |
| `salary_changes_count` | BIGINT | Cambios salariales |
| `job_changes_count` | BIGINT | Cambios de puesto |
| `undesired_turnovers` | BIGINT | Rotación no deseada |
| `regrettable_losses` | BIGINT | Pérdidas lamentables |
| `attrition_rate_monthly_pct` | NUMERIC | % rotación mensual |
| `salary_change_rate_pct` | NUMERIC | % cambios salariales |
| `generated_at` | TIMESTAMPTZ | Timestamp de generación |

#### Vista: `business.v_kpi_summary_byNapo` (Creada por ETL 07)
> Resumen global por snapshot para tarjetas KPI del dashboard.

#### Vista: `business.v_compensation_analysis_byNapo` (Creada por ETL 07)
> Análisis de compensación por empleado activo. Nota: `compa_ratio` y `band_penetration_pct` omitidos temporalmente (dependen de tabla de bandas salariales futura).

### 3.4 Permisos

```sql
GRANT USAGE ON SCHEMA business TO anon;
GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
ALTER DEFAULT PRIVILEGES IN SCHEMA business GRANT SELECT ON TABLES TO anon;
GRANT SELECT ON business.mv_monthly_kpis_byNapo TO anon;
```

---

## 4. Scripts Críticos del Backend / Pipeline ETL

### 4.1 `00_full_run_pipeline.py` — Orquestador Maestro

```python
import subprocess
import time
import sys
import os

# Lista asegurando el orden estricto de ejecución
SCRIPTS = [
    "01_setup_raw.py",
    "02_ingest_data.py",
    "03_setup_business.py",
    "04_create_enhanced_dataset_byNapo.py",
    "05_setup_raw_enhanced_byNapo.py",
    "06_ingest_enhanced_byNapo.py",
    "07_setup_business_enhanced_byNapo.py"
]

def print_banner():
    print("\n" + "="*60)
    print("🚀 HR ANALYTICS DASHBOARD - FULL PIPELINE EXECUTION 🚀")
    print("="*60)

def run_pipeline():
    print_banner()
    start_time = time.time()
    
    for idx, script in enumerate(SCRIPTS, 1):
        script_path = os.path.join(os.path.dirname(__file__), script)
        print(f"\n[{idx}/{len(SCRIPTS)}] Ejecutando: {script}")
        print("-" * 50)
        
        if not os.path.exists(script_path):
            print(f"❌ Error: No se encontró el archivo {script} en {script_path}")
            sys.exit(1)
            
        try:
            result = subprocess.run(
                [sys.executable, script_path],
                check=True,
                text=True,
                capture_output=False
            )
        except subprocess.CalledProcessError as e:
            print("\n❌ [" + script + "] Falló con código de salida: " + str(e.returncode))
            print("🛑 Interrumpiendo el flujo del pipeline.")
            sys.exit(1)
            
        print("-" * 50)
        print(f"✅ {script} completado.")
        
    total_time = time.time() - start_time
    print("\n" + "="*60)
    print(f"🎉 EJECUCIÓN DEL PIPELINE FINALIZADA EXITOSAMENTE")
    print(f"⏱️  Tiempo Total: {total_time:.2f} segundos")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_pipeline()
```

### 4.2 `01_setup_raw.py` — Preparación Capa Raw

```python
import pandas as pd
import os
import time
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def setup_raw():
    start_time = time.time()
    print("\n" + "="*50)
    print("🛠️  [ETL 01] INICIANDO PREPARACIÓN CAPA RAW")
    print("="*50)

    print("⏳ Leyendo metadatos de '../data/ibm_hr.csv'...")
    try:
        df = pd.read_csv('../data/ibm_hr.csv', nrows=0) 
        columns = [col.strip().lower().replace(' ', '_').replace('-', '_') for col in df.columns]
    except FileNotFoundError:
        print("❌ Error: Archivo ibm_hr.csv no encontrado.")
        return

    table_name = "raw.ibm_hr_landing"
    cols_query = ", ".join([f"{col} TEXT" for col in columns])
    
    sql_query = f"""
    CREATE SCHEMA IF NOT EXISTS raw;
    DROP TABLE IF EXISTS {table_name} CASCADE;
    CREATE TABLE {table_name} (
        {cols_query},
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """
    
    print("⏳ Ejecutando comandos en la base de datos...")
    engine = create_engine(db_url)
    try:
        with engine.connect() as conn:
            conn.execute(text(sql_query))
            conn.commit()
    except Exception as e:
        print(f"❌ Error en la base de datos:\n{e}")
        return

    print("\n📌 Enumerando artefactos creados:")
    print("  1. Esquema: [raw]")
    print(f"  2. Tabla:   [{table_name}] (con {len(columns)} columnas)")
    
    elapsed = time.time() - start_time
    print(f"\n✅ ETL 01 completado exitosamente en {elapsed:.2f} segundos.")
    print("="*50 + "\n")

if __name__ == "__main__":
    setup_raw()
```

### 4.3 `02_ingest_data.py` — Ingesta de Datos Core

```python
import pandas as pd
import os
import time
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def ingest_data():
    start_time = time.time()
    print("\n" + "="*50)
    print("📥 [ETL 02] INICIANDO INGESTA DE DATOS CORE")
    print("="*50)

    print("⏳ Cargando y limpiando 'ibm_hr.csv' en memoria...")
    try:
        df = pd.read_csv('../data/ibm_hr.csv')
        df.columns = [col.strip().lower().replace(' ', '_').replace('-', '_') for col in df.columns]
    except FileNotFoundError:
        print("❌ Error: Archivo ibm_hr.csv no encontrado.")
        return
    
    engine = create_engine(db_url)
    target_table = 'raw.ibm_hr_landing'
    print(f"🚀 Iniciando transferencia a PostgreSQL...")
    
    try:
        df.to_sql(
            name='ibm_hr_landing',
            con=engine,
            schema='raw',
            if_exists='append',
            index=False,
            chunksize=500
        )
    except Exception as e:
        print(f"❌ Error durante la inserción SQL:\n{e}")
        return

    print("\n📌 Resumen de ingesta:")
    print(f"  ➜ Origen:  '../data/ibm_hr.csv'")
    print(f"  ➜ Destino: Tabla [{target_table}]")
    print(f"  ➜ Volumen: {len(df):,} registros")

    elapsed = time.time() - start_time
    print(f"\n✅ ETL 02 completado exitosamente en {elapsed:.2f} segundos.")
    print("="*50 + "\n")

if __name__ == "__main__":
    ingest_data()
```

### 4.4 `03_setup_business.py` — Capa Business Base

```python
import os
import time
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def setup_business():
    start_time = time.time()
    print("\n" + "="*50)
    print("🏢 [ETL 03] CONSTRUYENDO CAPA BUSINESS (BASE)")
    print("="*50)

    engine = create_engine(db_url)
    
    sql_query = """
    CREATE SCHEMA IF NOT EXISTS business;
    
    CREATE OR REPLACE VIEW business.ibm_hr AS
    SELECT 
        employeenumber::INTEGER as id,
        age::INTEGER,
        department,
        jobrole,
        attrition,
        gender,
        dailyrate::INTEGER,
        monthlyincome::INTEGER,
        totalworkingyears::INTEGER,
        yearsatcompany::INTEGER,
        distancefromhome::INTEGER
    FROM raw.ibm_hr_landing;

    GRANT USAGE ON SCHEMA business TO anon;
    GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
    """
    
    print("⏳ Ejecutando sentencias analíticas en la base de datos...")
    try:
        with engine.connect() as conn:
            conn.execute(text(sql_query))
            conn.commit()
    except Exception as e:
        print(f"❌ Error en la base de datos:\n{e}")
        return

    print("\n📌 Enumerando artefactos creados:")
    print("  1. Esquema: [business]")
    print("  2. Vista:   [business.ibm_hr] (tipada)")
    print("  🔑 Permisos [anon] asignados a toda la capa oro.")

    elapsed = time.time() - start_time
    print(f"\n✅ ETL 03 completado exitosamente en {elapsed:.2f} segundos.")
    print("="*50 + "\n")

if __name__ == "__main__":
    setup_business()
```

### 4.5 `04_create_enhanced_dataset_byNapo.py` — Generador de Dataset Mejorado

```python
import pandas as pd
import numpy as np
import os
import time
from datetime import datetime, timedelta
import networkx as nx

CONFIG = {
    "RANDOM_SEED": 42,
    "DATE_RANGE": {"start": "2020-01-01", "end": "2026-03-31"},
    "EMPLOYEES_PER_MONTH": {"min": 4000, "max": 8000},
    "OUTPUT_DIR": "../data/",
    "LOG_LEVEL": "INFO"
}

def generate_dataset():
    start_time = time.time()
    print("\n" + "="*50)
    print("🧬 [ETL 04] GENERACIÓN DE DATASET MEJORADO (byNapo)")
    print("="*50)
    print("⏳ Configurando rangos de fecha y simulando datos...")
    start = pd.to_datetime(CONFIG["DATE_RANGE"]["start"])
    end = pd.to_datetime(CONFIG["DATE_RANGE"]["end"])
    dates = pd.date_range(start=start, end=end, freq="ME")
    
    cols_snapshot = [
        "snapshot_date", "employee_id", "employee_code", "full_name", "gender", 
        "nationality_iso3", "country_iso3", "department_name", "job_role", 
        "job_level_1", "job_level_2", "employment_status", "hire_date", 
        "termination_date", "termination_reason_legal", "turnover_classification_company",
        "monthly_salary_local", "currency_iso3", "fx_rate_to_usd", "monthly_salary_usd",
        "manager_employee_id", "dotted_line_manager_id", "work_center_id", 
        "home_lat", "home_lon", "work_modality", "education_level", 
        "education_status", "marital_status", "dependents_count", 
        "salary_change_flag", "salary_change_reason_code", "job_change_flag", 
        "exit_interview_completed", "regrettable_loss_flag"
    ]
    
    monthly_data = []
    
    print(f"📅 Generando snapshots desde {start.strftime('%Y-%m')} hasta {end.strftime('%Y-%m')}...")
    
    for date in dates:
        n_emp = np.random.randint(CONFIG["EMPLOYEES_PER_MONTH"]["min"], CONFIG["EMPLOYEES_PER_MONTH"]["max"])
        
        data = {
            "snapshot_date": date.strftime("%Y-%m-%d"),
            "employee_id": range(1, n_emp + 1),
            "employee_code": [f"EMP-{i:05d}" for i in range(1, n_emp + 1)],
            "full_name": ["Empleado Generado" for _ in range(n_emp)],
            "gender": np.random.choice(["Male", "Female"], n_emp),
            "nationality_iso3": np.random.choice(["PER", "CHL", "COL", "MEX", "USA", "ESP"], n_emp),
            "country_iso3": np.random.choice(["PER", "CHL", "COL", "MEX", "USA", "ESP"], n_emp),
            "department_name": np.random.choice(["Sales", "IT", "HR", "Operations"], n_emp),
            "job_role": np.random.choice(["Analyst", "Manager", "Director"], n_emp),
            "job_level_1": np.random.choice(["Individual Contributor", "Management"], n_emp),
            "job_level_2": np.random.choice(["Junior", "Senior", "Lead"], n_emp),
            "employment_status": np.random.choice(["Active", "Terminated"], n_emp, p=[0.9, 0.1]),
            "hire_date": (date - pd.Timedelta(days=np.random.randint(1, 3650))).strftime("%Y-%m-%d"),
            "termination_date": [None] * n_emp,
            "termination_reason_legal": [None] * n_emp,
            "turnover_classification_company": [None] * n_emp,
            "monthly_salary_local": np.random.uniform(1000, 5000, n_emp).round(2),
            "currency_iso3": "PEN",
            "fx_rate_to_usd": 3.70,
            "monthly_salary_usd": 0.0,
            "manager_employee_id": [None] * n_emp,
            "dotted_line_manager_id": [None] * n_emp,
            "work_center_id": np.random.choice(["WC-001", "WC-002"], n_emp),
            "home_lat": np.random.uniform(-12.0, -11.0, n_emp),
            "home_lon": np.random.uniform(-77.0, -76.0, n_emp),
            "work_modality": "Hybrid",
            "education_level": "Bachelor",
            "education_status": "Complete",
            "marital_status": "Single",
            "dependents_count": 0,
            "salary_change_flag": 0,
            "salary_change_reason_code": None,
            "job_change_flag": 0,
            "exit_interview_completed": False,
            "regrettable_loss_flag": False
        }
        
        df = pd.DataFrame(data)
        df["monthly_salary_usd"] = (df["monthly_salary_local"] / df["fx_rate_to_usd"]).round(2)
        monthly_data.append(df)

    final_df = pd.concat(monthly_data, ignore_index=True)
    
    output_path = os.path.join(CONFIG["OUTPUT_DIR"], "ibm_hr_monthly_snapshot_byNapo.csv")
    try:
        final_df.to_csv(output_path, index=False)
    except Exception as e:
        print(f"❌ Error al guardar CSV:\n{e}")
        return

    print("\n📌 Resumen de Generación:")
    print(f"  ➜ Archivo CSV:    {output_path}")
    print(f"  ➜ Total Meses:    {len(dates)}")
    print(f"  ➜ Total Registros:{len(final_df):,}")

    elapsed = time.time() - start_time
    print(f"\n✅ ETL 04 completado exitosamente en {elapsed:.2f} segundos.")
    print("="*50 + "\n")

if __name__ == "__main__":
    generate_dataset()
```

### 4.6 `05_setup_raw_enhanced_byNapo.py` — DDL Capa Raw Mejorada

```python
import os
import time
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def setup_raw_enhanced():
    start_time = time.time()
    print("\n" + "="*50)
    print("🛠️  [ETL 05] CONSTRUYENDO CAPA RAW (byNapo)")
    print("="*50)

    print("⏳ Ejecutando DDL sobre esquema [raw]...")
    engine = create_engine(db_url)
    
    sql_queries = """
    CREATE SCHEMA IF NOT EXISTS raw;

    CREATE TABLE IF NOT EXISTS raw.ibm_hr_monthly_snapshot_byNapo (
        snapshot_date TEXT, employee_id TEXT, employee_code TEXT, full_name TEXT,
        gender TEXT, nationality_iso3 TEXT, country_iso3 TEXT, department_name TEXT,
        job_role TEXT, job_level_1 TEXT, job_level_2 TEXT, employment_status TEXT,
        hire_date TEXT, termination_date TEXT, termination_reason_legal TEXT,
        turnover_classification_company TEXT, monthly_salary_local TEXT,
        currency_iso3 TEXT, fx_rate_to_usd TEXT, monthly_salary_usd TEXT,
        manager_employee_id TEXT, dotted_line_manager_id TEXT, work_center_id TEXT,
        home_lat TEXT, home_lon TEXT, work_modality TEXT, education_level TEXT,
        education_status TEXT, marital_status TEXT, dependents_count TEXT,
        salary_change_flag TEXT, salary_change_reason_code TEXT, job_change_flag TEXT,
        exit_interview_completed TEXT, regrettable_loss_flag TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS raw.ibm_hr_change_reasons_byNapo (
        reason_code TEXT, reason_name_es TEXT, reason_name_en TEXT,
        affects_salary TEXT, affects_job TEXT, active_flag TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """

    try:
        with engine.connect() as conn:
            conn.execute(text(sql_queries))
            conn.commit()
    except Exception as e:
        print(f"❌ Error en base de datos:\n{e}")
        return
        
    print("\n📌 Enumerando artefactos creados:")
    print("  1. Tabla: [raw.ibm_hr_monthly_snapshot_byNapo]")
    print("  2. Tabla: [raw.ibm_hr_change_reasons_byNapo]")

    elapsed = time.time() - start_time
    print(f"\n✅ ETL 05 completado exitosamente en {elapsed:.2f} segundos.")
    print("="*50 + "\n")

if __name__ == "__main__":
    setup_raw_enhanced()
```

### 4.7 `06_ingest_enhanced_byNapo.py` — Ingesta Masiva Mejorada

```python
import pandas as pd
import os
import time
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def ingest_enhanced_data():
    start_time = time.time()
    print("\n" + "="*50)
    print("📥 [ETL 06] INGESTA DE DATOS POTENCIADOS (byNapo)")
    print("="*50)
    
    engine = create_engine(db_url)
    data_dir = "../data/"
    
    files_to_ingest = {
        "ibm_hr_monthly_snapshot_byNapo.csv": "raw.ibm_hr_monthly_snapshot_byNapo",
    }
    
    for filename, table_name in files_to_ingest.items():
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            df.columns = [col.strip().lower() for col in df.columns]
            
            print(f"⏳ Subiendo lote de [{len(df):,}] registros a [{table_name}]...")
            try:
                df.to_sql(
                    name=table_name.split('.')[1],
                    schema=table_name.split('.')[0],
                    con=engine,
                    if_exists='append',
                    index=False,
                    chunksize=1000
                )
                print(f"  ➜ ✅ {filename} ingestado con éxito.")
            except Exception as e:
                print(f"  ➜ ❌ Error al ingestar {filename}:\n{e}")
        else:
            print(f"⚠️  Advertencia: Archivo local no encontrado: {filepath}")

    elapsed = time.time() - start_time
    print(f"\n✅ ETL 06 completado exitosamente en {elapsed:.2f} segundos.")
    print("="*50 + "\n")

if __name__ == "__main__":
    ingest_enhanced_data()
```

### 4.8 `07_setup_business_enhanced_byNapo.py` — Capa Business Mejorada

> ⚠️ Este es el script más extenso (~365 líneas). Contiene todo el SQL de la capa analítica.
> Consultar archivo fuente completo en: `etl_pipeline/07_setup_business_enhanced_byNapo.py`

**Resumen de operaciones SQL ejecutadas (en orden):**

1. `DROP SCHEMA IF EXISTS business CASCADE` — Clean Slate
2. `CREATE SCHEMA business`
3. `CREATE VIEW business.v_employee_full_byNapo` — Vista maestra tipada (35+ columnas)
4. `CREATE VIEW business.v_org_tree_byNapo` — CTE recursiva de organigrama
5. `CREATE MATERIALIZED VIEW business.mv_monthly_kpis_byNapo` — KPIs mensuales
6. `CREATE UNIQUE INDEX idx_mv_kpis_snapshot_unique` — Índice para REFRESH CONCURRENTLY
7. `CREATE VIEW business.v_kpi_summary_byNapo` — Resumen rápido para KPI cards
8. `CREATE VIEW business.v_compensation_analysis_byNapo` — Análisis compensaciones
9. `GRANT` statements para rol `anon` en Supabase

**Post-SQL (Python):**
- `REFRESH MATERIALIZED VIEW business.mv_monthly_kpis_byNapo`
- `SELECT COUNT(*) FROM business.v_employee_full_byNapo` — Validación

---

## 5. Estado del Frontend (React/Vite)

### 5.1 Componentes Activos

| Archivo | Propósito | Datos que consume |
|---------|-----------|-------------------|
| `Sidebar.jsx` | Menú lateral colapsable con acordeón para submenús. Estilo MS365. | `vistaActual` (state) |
| `Overview.jsx` | KPIs: Total Colaboradores + Alertas de Fuga. Gráfico ECharts (barras por departamento). | `business.ibm_hr` via prop `data` |
| `OrgStructure.jsx` | Landing page del módulo Estructura Org. con 3 tarjetas de navegación. | Ninguno (estático) |
| `OrganigramaIntegral.jsx` | Organigrama jerárquico visual con KPIs y nodos por departamento. | Ninguno (hardcoded, pendiente integrar vista `v_org_tree_byNapo`) |
| `Compensations.jsx` | KPIs: Promedio Tarifa Diaria + Edad Promedio. Scatter plot Edad vs Tarifa. | `business.ibm_hr` via prop `data` |
| `EmployeeTable.jsx` | Tabla de auditoría de datos crudos (ID, Edad, Dept, Rol, Attrition). | `business.ibm_hr` via prop `data` |

### 5.2 Renderizado Condicional (`App.jsx`)

```jsx
import { useState, useEffect } from 'react'
import { supabase } from './lib/supabaseClient'
import Sidebar from './components/Sidebar'
import EmployeeTable from './components/EmployeeTable'
import Overview from './components/Overview'
import Compensaciones from './components/Compensations'
import OrgStructure from './components/OrgStructure'
import OrganigramaIntegral from './components/OrganigramaIntegral'

function App() {
  const [empleados, setEmpleados] = useState([])
  const [errorBd, setErrorBd] = useState(null)
  const [vistaActual, setVistaActual] = useState('vision_general')

  useEffect(() => {
    async function fetchEmpleados() {
      const { data, error } = await supabase
        .schema('business')
        .from('ibm_hr')
        .select('*')

      if (error) {
        setErrorBd(error.message)
        console.error("Error de Supabase:", error)
      } else {
        setEmpleados(data)
      }
    }
    fetchEmpleados()
  }, [])

  return (
    <div className="flex h-screen bg-gray-50 overflow-hidden">
      <Sidebar vistaActual={vistaActual} setVistaActual={setVistaActual} />
      <main className="flex-1 overflow-y-auto p-8">
        <div className="max-w-7xl mx-auto">
          <header className="mb-8 border-b border-gray-200 pb-4">
            <h1 className="text-3xl font-semibold text-gray-800 mb-8">HR Analytics</h1>
          </header>

          {errorBd ? (
            <div className="bg-red-900 text-red-200 p-4 rounded-lg mt-4 text-sm font-mono shadow-md">
              <strong>🚨 Error de Conexión:</strong> {errorBd}
            </div>
          ) : (
            <div className="mt-8">
              {vistaActual === 'vision_general' && <Overview data={empleados} />}
              {vistaActual === 'estructura' && <OrgStructure setVistaActual={setVistaActual} />}
              {vistaActual === 'org_integral' && <OrganigramaIntegral />}
              {vistaActual === 'compensaciones' && <Compensaciones data={empleados} />}
              {vistaActual === 'auditoria' && <EmployeeTable data={empleados} />}

              {/* Placeholders para módulos futuros */}
              {['fuga_talento', 'desempeno', 'turnos', 'reclutamiento',
                'capacitacion', 'clima', 'diversidad', 'org_dotacion',
                'org_costos'].includes(vistaActual) && (
                <div className="flex flex-col items-center justify-center p-20 text-gray-400
                  border-2 border-dashed border-gray-300 rounded-xl mt-10">
                  <h3 className="text-2xl font-bold text-gray-500 mb-2">
                    Módulo en Construcción 🚀
                  </h3>
                  <p>Pronto conectaremos los datos para esta sección.</p>
                </div>
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

export default App
```

### 5.3 Cliente Supabase (`lib/supabaseClient.js`)

```javascript
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
```

---

## 6. Variables de Entorno (.env)

### 6.1 Backend (Raíz del proyecto: `/.env`)

```env
VITE_SUPABASE_URL=***
VITE_SUPABASE_ANON_KEY=***
SUPABASE_SERVICE_KEY=***
DATABASE_URL=***
```

### 6.2 Frontend (`/client/.env`)

```env
VITE_SUPABASE_URL=***
```

> **Nota:** El frontend también requiere `VITE_SUPABASE_ANON_KEY` (referenciado en `supabaseClient.js`), pero esta clave se resuelve desde el `.env` raíz o debe duplicarse en `/client/.env`.

---

*Fin del Project Context Dump. Archivo generado para sincronización entre equipos y agentes de IA.*
