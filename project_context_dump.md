# 📦 Project Context Dump — HR Analytics Dashboard

> **Generado:** 2026-04-07  
> **Propósito:** Blueprint técnico completo para sincronización de contexto con equipos o agentes de IA.  
> **Pipeline Status:** ✅ Todos los scripts (00–07) ejecutan sin errores.

---

## 1. Estructura de Directorios (Tree)

```
hr-analytics-dashboard/
├── .env                                    # Variables de entorno (backend + Supabase)
├── DATA_DICTIONARY.md                      # Diccionario de datos por capa
├── README.md                               # Documentación general del proyecto
├── project_context_dump.md                 # << ESTE ARCHIVO >>
├── readme_update_brief.md                  # Brief para actualización del README
│
├── data/
│   ├── ibm_hr.csv                          # Dataset original IBM (1,470 registros)
│   └── ibm_hr_monthly_snapshot_byNapo.csv  # Dataset potenciado (528K+ registros)
│
├── etl_pipeline/
│   ├── 00_full_run_pipeline.py             # 🎯 Orquestador maestro (ejecuta 01–07)
│   ├── 01_setup_raw.py                     # DDL: Crea esquema raw + tabla landing
│   ├── 02_ingest_data.py                   # Ingesta: ibm_hr.csv → raw.ibm_hr_landing
│   ├── 03_setup_business.py                # DDL: Vista base business.ibm_hr
│   ├── 04_create_enhanced_dataset_byNapo.py # Generador: Simulación mensual 2020–2026
│   ├── 05_setup_raw_enhanced_byNapo.py     # DDL: Tablas raw para el dataset potenciado
│   ├── 06_ingest_enhanced_byNapo.py        # Ingesta: CSV potenciado → raw (528K registros)
│   └── 07_setup_business_enhanced_byNapo.py # DDL: Capa Business Oro (vistas tipadas + MatView)
│
├── client/
│   ├── .env                                # Variables de entorno frontend (Vite)
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   ├── public/
│   │   ├── favicon.svg
│   │   └── icons.svg
│   ├── docs/
│   │   └── prompts/
│   │       ├── context_dump.md
│   │       └── readme_update_brief.md
│   └── src/
│       ├── main.jsx                        # Entry point React
│       ├── App.jsx                         # Enrutador principal (renderizado condicional)
│       ├── index.css.md
│       ├── lib/
│       │   └── supabaseClient.js           # Configuración del cliente Supabase
│       └── components/
│           ├── Sidebar.jsx                 # Navegación lateral colapsable + acordeón
│           ├── Overview.jsx                # Dashboard: KPIs + gráfico por departamento
│           ├── Compensations.jsx           # Análisis: Scatter plot edad vs tarifa
│           ├── EmployeeTable.jsx           # Auditoría: Tabla cruda con flag de deserción
│           ├── OrgStructure.jsx            # Landing: Estructura organizacional (3 cards)
│           └── OrganigramaIntegral.jsx     # Organigrama: Jerarquía visual estática
```

---

## 2. Dependencias y Entorno

### 2.1 Python (Backend / ETL Pipeline)

> **⚠️ No existe `requirements.txt` formal.** Las siguientes librerías se infieren del código:

| Librería | Uso |
|----------|-----|
| `pandas` | Lectura CSV, transformación de DataFrames, `to_sql` |
| `numpy` | Generación aleatoria de datos, arrays |
| `sqlalchemy` | Conexión a PostgreSQL, ejecución de SQL (`create_engine`, `text`) |
| `psycopg2` | Driver PostgreSQL (dependencia de SQLAlchemy) |
| `python-dotenv` | Lectura de variables de entorno desde `.env` |
| `networkx` | Importado en ETL 04 (validación de grafos, uso reservado) |

### 2.2 Node.js (Frontend — `client/package.json`)

**dependencies:**
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

**devDependencies:**
```json
{
  "@eslint/js": "^9.39.4",
  "@tailwindcss/vite": "^4.2.2",
  "@types/react": "^19.2.14",
  "@types/react-dom": "^19.2.3",
  "@vitejs/plugin-react": "^6.0.1",
  "eslint-plugin-react-hooks": "^7.0.1",
  "eslint-plugin-react-refresh": "^0.5.2",
  "tailwindcss": "^4.2.2",
  "vite": "^8.0.1"
}
```

---

## 3. Modelado de Base de Datos y Arquitectura de Datos

### 3.1 Arquitectura Medallion (3 Capas)

```
┌────────────────────┐    ┌────────────────────┐    ┌───────────────────────────┐
│   📂 data/ (CSV)   │ →  │  🥉 raw (Bronce)   │ →  │   🥇 business (Oro)       │
│   Archivos planos  │    │  Todo en TEXT       │    │   Vistas tipadas + KPIs   │
└────────────────────┘    └────────────────────┘    └───────────────────────────┘
```

### 3.2 Esquema `raw` — Tablas de Ingestión Cruda

#### `raw.ibm_hr_landing`
> Creada por: ETL 01 (dinámico, 35 columnas detectadas del CSV). Columnas como TEXT.

| Columna (muestra) | Tipo | Notas |
|--------------------|------|-------|
| `employeenumber` | TEXT | ID original IBM |
| `age` | TEXT | Edad |
| `department` | TEXT | Departamento |
| `jobrole` | TEXT | Rol |
| `monthlyincome` | TEXT | Ingreso mensual |
| `attrition` | TEXT | Yes/No |
| _(+ 29 columnas más)_ | TEXT | Auto-detectadas del CSV |
| `created_at` | TIMESTAMPTZ | Default NOW() |

#### `raw."ibm_hr_monthly_snapshot_byNapo"`
> Creada por: ETL 05. **Nombre citado** para preservar case (fix de PostgreSQL identifier folding).

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `snapshot_date` | TEXT | Fecha de corte mensual |
| `employee_id` | TEXT | ID del empleado |
| `employee_code` | TEXT | Código EMP-XXXXX |
| `full_name` | TEXT | Nombre sintético |
| `gender` | TEXT | Male/Female |
| `nationality_iso3` | TEXT | ISO3 nacionalidad |
| `country_iso3` | TEXT | ISO3 país de operación |
| `department_name` | TEXT | IT, Sales, HR, Finance, Operations |
| `job_role` | TEXT | Rol según departamento |
| `job_level_1` | TEXT | Management / Individual Contributor |
| `job_level_2` | TEXT | Senior / Junior / Lead |
| `employment_status` | TEXT | Active / Terminated |
| `hire_date` | TEXT | Fecha de contratación |
| `termination_date` | TEXT | Fecha de cese (NULL si activo) |
| `termination_reason_legal` | TEXT | Reservado |
| `turnover_classification_company` | TEXT | Reservado |
| `monthly_salary_local` | TEXT | Salario moneda local |
| `currency_iso3` | TEXT | PEN, EUR, USD, CLP, COP, MXN |
| `fx_rate_to_usd` | TEXT | Tipo de cambio simulado |
| `monthly_salary_usd` | TEXT | Salario en USD |
| `manager_employee_id` | TEXT | ID del jefe directo |
| `dotted_line_manager_id` | TEXT | Reservado |
| `work_center_id` | TEXT | Reservado |
| `home_lat` / `home_lon` | TEXT | Reservado |
| `work_modality` | TEXT | Reservado |
| `education_level` / `education_status` | TEXT | Reservado |
| `marital_status` / `dependents_count` | TEXT | Reservado |
| `salary_change_flag` | TEXT | 0/1 |
| `salary_change_reason_code` | TEXT | Reservado |
| `job_change_flag` | TEXT | 0/1 |
| `exit_interview_completed` | TEXT | Reservado |
| `regrettable_loss_flag` | TEXT | Reservado |
| `created_at` | TIMESTAMPTZ | Default NOW() |

#### `raw."ibm_hr_change_reasons_byNapo"`
> Catálogo de motivos (reservado para uso futuro).

| Columna | Tipo |
|---------|------|
| `reason_code` | TEXT |
| `reason_name_es` | TEXT |
| `reason_name_en` | TEXT |
| `affects_salary` | TEXT |
| `affects_job` | TEXT |
| `active_flag` | TEXT |
| `created_at` | TIMESTAMPTZ |

### 3.3 Esquema `business` — Vistas Analíticas (Oro)

> **Estrategia Clean Slate:** ETL 07 ejecuta `DROP SCHEMA IF EXISTS business CASCADE` + `CREATE SCHEMA business` en cada corrida para garantizar idempotencia.

#### Vista: `business.v_employee_full_byNapo`
> Vista maestra que transforma TEXT → tipos nativos + campos calculados.

| Columna | Tipo Casteado | Origen / Lógica |
|---------|---------------|-----------------|
| `snapshot_date` | DATE | `snapshot_date::DATE` |
| `employee_id` | INTEGER | `employee_id::INTEGER` |
| `employee_code` | TEXT | Directo |
| `full_name` | TEXT | Directo |
| `gender` | TEXT | Directo |
| `country_iso3` | TEXT | Directo |
| `department_name` | TEXT | Directo |
| `job_role` | TEXT | Directo |
| `job_level_1` | TEXT | Directo |
| `job_level_2` | TEXT | Directo |
| `employment_status` | TEXT | Directo |
| `hire_date` | DATE | `hire_date::DATE` |
| `termination_date` | DATE | `termination_date::DATE` |
| `monthly_salary_local` | NUMERIC(12,2) | Cast |
| `currency_iso3` | TEXT | Directo |
| `fx_rate_to_usd` | NUMERIC(10,4) | Cast |
| `monthly_salary_usd` | NUMERIC(12,2) | Cast |
| `manager_employee_id` | INTEGER | `NULLIF(..., '')::INTEGER` |
| `tenure_months` | NUMERIC | **Calculado:** `AGE(termination_date \|\| snapshot_date, hire_date)` en meses |
| `is_active_at_snapshot` | BOOLEAN | **Calculado:** Lógica de corte por status + fecha |
| `processed_at` | TIMESTAMPTZ | `NOW()` |

#### Vista: `business.v_org_tree_byNapo`
> CTE recursiva para organigrama (ECharts). Filtra por último snapshot, empleados activos.

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `employee_id` | INTEGER | Nodo actual |
| `full_name` | TEXT | Nombre |
| `job_role` | TEXT | Rol |
| `job_level_1` | TEXT | Nivel jerárquico |
| `depth` | INTEGER | Profundidad (0 = raíz, max 10) |
| `echarts_node` | JSON | `json_build_object(id, name, value, children)` |

#### Vista Materializada: `business.mv_monthly_kpis_byNapo`
> KPIs pre-calculados. Índice único: `(snapshot_date, country_iso3)`.

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `snapshot_date` | DATE | Mes de referencia |
| `country_iso3` | TEXT | País |
| `headcount_active` | BIGINT | `COUNT(*) FILTER (WHERE is_active_at_snapshot)` |
| `headcount_terminated` | BIGINT | `COUNT(*) FILTER (WHERE NOT is_active_at_snapshot)` |
| `avg_salary_usd` | NUMERIC | `AVG(monthly_salary_usd)` activos |
| `avg_tenure` | NUMERIC | `AVG(tenure_months)` activos |

#### Vista: `business.ibm_hr`
> Vista base del dataset original IBM (ETL 03).

| Columna | Tipo | Origen |
|---------|------|--------|
| `id` | INTEGER | `employeenumber::INTEGER` |
| `age` | INTEGER | `age::INTEGER` |
| `department` | TEXT | Directo |
| `jobrole` | TEXT | Directo |
| `attrition` | TEXT | Directo |
| `gender` | TEXT | Directo |
| `dailyrate` | INTEGER | `dailyrate::INTEGER` |
| `monthlyincome` | INTEGER | `monthlyincome::INTEGER` |
| `totalworkingyears` | INTEGER | `totalworkingyears::INTEGER` |
| `yearsatcompany` | INTEGER | `yearsatcompany::INTEGER` |
| `distancefromhome` | INTEGER | `distancefromhome::INTEGER` |

### 3.4 Permisos Supabase

```sql
GRANT USAGE ON SCHEMA business TO anon;
GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
```

---

## 4. Scripts Críticos del Backend / Pipeline ETL

### 4.0 `00_full_run_pipeline.py` — Orquestador Maestro

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

### 4.1 `01_setup_raw.py` — Preparación Capa RAW

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

### 4.2 `02_ingest_data.py` — Ingesta Datos Core

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

### 4.3 `03_setup_business.py` — Capa Business Base

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

### 4.4 `04_create_enhanced_dataset_byNapo.py` — Generador de Dataset Potenciado

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
    "EMPLOYEES_PER_MONTH": {"min": 4000, "max": 6000},
    "OUTPUT_DIR": "../data/",
    
    "IPC_CONFIG": {
        "PER": {"rate": 0.04, "month": 2},
        "ESP": {"rate": 0.03, "month": 1},
        "CHL": {"rate": 0.035, "month": 7},
    },
    
    "COUNTRIES": ["PER", "CHL", "COL", "MEX", "ESP", "USA"],
    "DEPARTMENTS": ["IT", "Sales", "HR", "Finance", "Operations"],
    "ROLES_BY_DEPT": {
        "IT": ["Software Engineer", "DevOps", "Data Analyst", "CTO"],
        "Sales": ["Sales Rep", "Account Manager", "Sales Director"],
        "HR": ["HR Specialist", "HR Manager", "Recruiter"],
        "Finance": ["Accountant", "Financial Analyst", "CFO"],
        "Operations": ["Operator", "Logistics Coord", "Ops Director"]
    }
}

def generate_dataset():
    start_time = time.time()
    print("\n" + "="*50)
    print("🧬 [ETL 04] GENERACIÓN DE DATASET POTENCIADO (byNapo)")
    print("="*50)
    
    start = pd.to_datetime(CONFIG["DATE_RANGE"]["start"])
    end = pd.to_datetime(CONFIG["DATE_RANGE"]["end"])
    dates = pd.date_range(start=start, end=end, freq="ME")
    
    n_seed = CONFIG["EMPLOYEES_PER_MONTH"]["min"]
    
    first_names = ["Juan", "Maria", "Carlos", "Ana", "Luis", "Sofia", "Pedro", "Lucia"]
    last_names = ["Perez", "Gomez", "Rodriguez", "Lopez", "Martinez", "Silva", "Torres"]
    
    data = {
        "employee_id": range(1, n_seed + 1),
        "employee_code": [f"EMP-{i:05d}" for i in range(1, n_seed + 1)],
        "full_name": [f"{np.random.choice(first_names)} {np.random.choice(last_names)}" for _ in range(n_seed)],
        "gender": np.random.choice(["Male", "Female"], n_seed),
        "country_iso3": np.random.choice(CONFIG["COUNTRIES"], n_seed),
        "department_name": np.random.choice(CONFIG["DEPARTMENTS"], n_seed),
        "job_role": ["Role"] * n_seed,
        "job_level_1": np.random.choice(["Management", "Individual Contributor"], n_seed),
        "job_level_2": np.random.choice(["Senior", "Junior", "Lead"], n_seed),
        "employment_status": "Active",
        "hire_date": [(start - pd.Timedelta(days=int(d))).strftime("%Y-%m-%d") for d in np.random.randint(100, 2000, n_seed)],
        "termination_date": None,
        "monthly_salary_local": np.random.uniform(1500, 5000, n_seed).round(2),
        "currency_iso3": "PEN",
        "manager_employee_id": None
    }
    
    df = pd.DataFrame(data)
    df["job_role"] = df.apply(lambda row: np.random.choice(CONFIG["ROLES_BY_DEPT"].get(row["department_name"], ["General"])), axis=1)
    
    currency_map = {"PER": "PEN", "ESP": "EUR", "USA": "USD", "CHL": "CLP", "COL": "COP", "MEX": "MXN"}
    df["currency_iso3"] = df["country_iso3"].map(currency_map)
    
    managers = df[df["job_level_1"] == "Management"]["employee_id"].tolist()
    df["manager_employee_id"] = df["employee_id"].apply(
        lambda x: np.random.choice(managers) if x not in managers else None
    )
    
    monthly_snapshots = []
    
    print(f"📅 Iniciando simulación desde {start.strftime('%Y-%m')}...")
    
    for date in dates:
        current_month_str = date.strftime("%Y-%m-%d")
        
        # A. Ajuste Salarial por IPC
        for country, config in CONFIG["IPC_CONFIG"].items():
            if date.month == config["month"]:
                mask = (df["country_iso3"] == country) & (df["employment_status"] == "Active")
                df.loc[mask, "monthly_salary_local"] *= (1 + config["rate"])
                print(f"   📈 IPC aplicado a {country}: +{config['rate']*100}%")
        
        # B. Rotación (Bajas aleatorias 1%)
        attrition_rate = 0.01
        active_employees = df[df["employment_status"] == "Active"]
        leaving_ids = np.random.choice(active_employees["employee_id"], size=int(len(active_employees) * attrition_rate), replace=False)
        df.loc[df["employee_id"].isin(leaving_ids), "employment_status"] = "Terminated"
        df.loc[df["employee_id"].isin(leaving_ids), "termination_date"] = current_month_str
        
        # C. Contrataciones (2% nueva contratación)
        n_new = int(CONFIG["EMPLOYEES_PER_MONTH"]["min"] * 0.02)
        for i in range(n_new):
            new_id = df["employee_id"].max() + 1
            country = np.random.choice(CONFIG["COUNTRIES"])
            new_row = {
                "employee_id": new_id,
                "employee_code": f"EMP-{new_id:05d}",
                "full_name": f"{np.random.choice(first_names)} {np.random.choice(last_names)}",
                "gender": np.random.choice(["Male", "Female"]),
                "country_iso3": country,
                "department_name": np.random.choice(CONFIG["DEPARTMENTS"]),
                "job_role": np.random.choice(CONFIG["ROLES_BY_DEPT"].get("IT", ["General"])),
                "job_level_1": "Individual Contributor",
                "job_level_2": "Junior",
                "employment_status": "Active",
                "hire_date": current_month_str,
                "termination_date": None,
                "monthly_salary_local": np.random.uniform(1000, 3000),
                "currency_iso3": currency_map[country],
                "manager_employee_id": np.random.choice(managers)
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # Validación de Organigrama
        valid_ids = set(df[df["employment_status"] == "Active"]["employee_id"])
        for idx, row in df.iterrows():
            if row["employment_status"] == "Active" and row["manager_employee_id"] is not None:
                if row["manager_employee_id"] not in valid_ids:
                    df.at[idx, "manager_employee_id"] = np.random.choice(managers)
        
        # Guardar Snapshot
        snapshot_df = df.copy()
        snapshot_df["snapshot_date"] = current_month_str
        snapshot_df["fx_rate_to_usd"] = 3.50 
        snapshot_df["monthly_salary_usd"] = (snapshot_df["monthly_salary_local"] / snapshot_df["fx_rate_to_usd"]).round(2)
        snapshot_df["salary_change_flag"] = 0
        snapshot_df["job_change_flag"] = 0
        monthly_snapshots.append(snapshot_df)
    
    final_df = pd.concat(monthly_snapshots, ignore_index=True)
    
    os.makedirs(CONFIG["OUTPUT_DIR"], exist_ok=True)
    output_path = os.path.join(CONFIG["OUTPUT_DIR"], "ibm_hr_monthly_snapshot_byNapo.csv")
    final_df.to_csv(output_path, index=False)
    
    elapsed = time.time() - start_time
    print(f"\n✅ Dataset guardado en: {output_path}")
    print(f"📊 Total registros generados: {len(final_df):,}")
    print(f"⏱️ Tiempo: {elapsed:.2f} segundos")

if __name__ == "__main__":
    generate_dataset()
```

### 4.5 `05_setup_raw_enhanced_byNapo.py` — DDL Tablas Potenciadas

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

    -- Limpiar versiones anteriores (ambas variantes de casing por seguridad)
    DROP TABLE IF EXISTS raw."ibm_hr_monthly_snapshot_byNapo" CASCADE;
    DROP TABLE IF EXISTS raw."ibm_hr_monthly_snapshot_bynapo" CASCADE;

    -- Tabla Principal: Snapshot Mensual (nombre citado para preservar case)
    CREATE TABLE raw."ibm_hr_monthly_snapshot_byNapo" (
        snapshot_date TEXT, employee_id TEXT, employee_code TEXT,
        full_name TEXT, gender TEXT, nationality_iso3 TEXT,
        country_iso3 TEXT, department_name TEXT, job_role TEXT,
        job_level_1 TEXT, job_level_2 TEXT, employment_status TEXT,
        hire_date TEXT, termination_date TEXT,
        termination_reason_legal TEXT, turnover_classification_company TEXT,
        monthly_salary_local TEXT, currency_iso3 TEXT,
        fx_rate_to_usd TEXT, monthly_salary_usd TEXT,
        manager_employee_id TEXT, dotted_line_manager_id TEXT,
        work_center_id TEXT, home_lat TEXT, home_lon TEXT,
        work_modality TEXT, education_level TEXT, education_status TEXT,
        marital_status TEXT, dependents_count TEXT,
        salary_change_flag TEXT, salary_change_reason_code TEXT,
        job_change_flag TEXT, exit_interview_completed TEXT,
        regrettable_loss_flag TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    -- Tabla de Catálogo de Motivos
    DROP TABLE IF EXISTS raw."ibm_hr_change_reasons_byNapo" CASCADE;
    DROP TABLE IF EXISTS raw."ibm_hr_change_reasons_bynapo" CASCADE;
    CREATE TABLE raw."ibm_hr_change_reasons_byNapo" (
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

### 4.6 `06_ingest_enhanced_byNapo.py` — Ingesta Masiva

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
            df = pd.read_csv(filepath, dtype=str)
            df.columns = [col.strip().lower() for col in df.columns]
            df = df.where(df.notna(), None)
            
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

### 4.7 `07_setup_business_enhanced_byNapo.py` — Capa Business Oro

```python
import os
import time
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def setup_business_enhanced():
    """
    🏗️ Crea la capa Business (Oro) con vistas tipadas y analíticas.
    """
    start_time = time.time()
    print("\n" + "="*50)
    print("🏢 [ETL 07] CONSTRUYENDO CAPA BUSINESS ENHANCED (byNapo)")
    print("="*50)
    
    if not db_url:
        print("❌ Error: DATABASE_URL no encontrada en .env")
        return

    print("⏳ Ejecutando sentencias SQL en Supabase...")
    engine = create_engine(db_url)

    sql_queries = """
    -- 0. CLEAN SLATE (Reconstrucción total para idempotencia)
    DROP SCHEMA IF EXISTS business CASCADE;

    -- 1. Crear esquema
    CREATE SCHEMA business;

    -- 2. VISTA MAESTRA (Tipada y Enriquecida)
    CREATE OR REPLACE VIEW business.v_employee_full_byNapo AS
    SELECT 
        snapshot_date::DATE as snapshot_date,
        employee_id::INTEGER as employee_id,
        employee_code, full_name, gender, country_iso3,
        department_name, job_role, job_level_1, job_level_2,
        employment_status,
        hire_date::DATE as hire_date,
        termination_date::DATE as termination_date,
        monthly_salary_local::NUMERIC(12,2) as monthly_salary_local,
        currency_iso3,
        fx_rate_to_usd::NUMERIC(10,4) as fx_rate_to_usd,
        monthly_salary_usd::NUMERIC(12,2) as monthly_salary_usd,
        NULLIF(manager_employee_id, '')::INTEGER as manager_employee_id,
        
        -- Antigüedad en meses
        CASE 
            WHEN termination_date::DATE IS NOT NULL THEN 
                EXTRACT(YEAR FROM AGE(termination_date::DATE, hire_date::DATE)) * 12 + 
                EXTRACT(MONTH FROM AGE(termination_date::DATE, hire_date::DATE))
            ELSE 
                EXTRACT(YEAR FROM AGE(snapshot_date::DATE, hire_date::DATE)) * 12 + 
                EXTRACT(MONTH FROM AGE(snapshot_date::DATE, hire_date::DATE))
        END as tenure_months,
        
        -- Flag Activo
        CASE 
            WHEN employment_status = 'Active' THEN TRUE
            WHEN termination_date::DATE IS NULL THEN TRUE
            WHEN termination_date::DATE >= snapshot_date::DATE THEN TRUE
            ELSE FALSE
        END as is_active_at_snapshot,
        
        NOW() as processed_at
    FROM raw."ibm_hr_monthly_snapshot_byNapo";

    -- 3. VISTA DE ORGANIGRAMA (Recursiva para ECharts)
    CREATE OR REPLACE VIEW business.v_org_tree_byNapo AS
    WITH RECURSIVE org_hierarchy AS (
        SELECT employee_id, full_name, job_role, job_level_1,
               department_name, manager_employee_id,
               0 as depth, ARRAY[employee_id] as path
        FROM business.v_employee_full_byNapo
        WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM business.v_employee_full_byNapo)
          AND is_active_at_snapshot = TRUE
          AND (manager_employee_id IS NULL OR manager_employee_id NOT IN (
              SELECT employee_id FROM business.v_employee_full_byNapo 
              WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM business.v_employee_full_byNapo)
          ))
        UNION ALL
        SELECT emp.employee_id, emp.full_name, emp.job_role, emp.job_level_1,
               emp.department_name, emp.manager_employee_id,
               oh.depth + 1, oh.path || emp.employee_id
        FROM business.v_employee_full_byNapo emp
        INNER JOIN org_hierarchy oh ON emp.manager_employee_id = oh.employee_id
        WHERE emp.snapshot_date = (SELECT MAX(snapshot_date) FROM business.v_employee_full_byNapo)
          AND emp.is_active_at_snapshot = TRUE
          AND NOT emp.employee_id = ANY(oh.path)
          AND oh.depth < 10
    )
    SELECT employee_id, full_name, job_role, job_level_1, depth,
        json_build_object('id', employee_id, 'name', full_name, 'value', job_level_1, 'children', NULL) as echarts_node
    FROM org_hierarchy
    ORDER BY depth, employee_id;

    -- 4. VISTA MATERIALIZADA DE KPIs
    CREATE MATERIALIZED VIEW IF NOT EXISTS business.mv_monthly_kpis_byNapo AS
    SELECT snapshot_date, country_iso3,
        COUNT(*) FILTER (WHERE is_active_at_snapshot = TRUE) as headcount_active,
        COUNT(*) FILTER (WHERE is_active_at_snapshot = FALSE) as headcount_terminated,
        ROUND(AVG(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE), 2) as avg_salary_usd,
        ROUND(AVG(tenure_months) FILTER (WHERE is_active_at_snapshot = TRUE), 1) as avg_tenure
    FROM business.v_employee_full_byNapo
    GROUP BY snapshot_date, country_iso3;

    CREATE UNIQUE INDEX IF NOT EXISTS idx_kpis_unique 
      ON business.mv_monthly_kpis_byNapo (snapshot_date, country_iso3);

    -- 5. PERMISOS
    GRANT USAGE ON SCHEMA business TO anon;
    GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
    """

    try:
        with engine.connect() as conn:
            conn.execute(text(sql_queries))
            conn.commit()
            print("✅ Vistas creadas exitosamente.")
        with engine.connect() as conn:
            conn.execute(text("REFRESH MATERIALIZED VIEW business.mv_monthly_kpis_byNapo;"))
            conn.commit()
            print("🔄 Vista materializada refrescada.")
    except Exception as e:
        print(f"❌ Error en SQL: {e}")
        return

    elapsed = time.time() - start_time
    print(f"\n🎉 [ETL 07] Completado en {elapsed:.2f} segundos.")

if __name__ == "__main__":
    setup_business_enhanced()
```

---

## 5. Estado del Frontend (React/Vite)

### 5.1 Componentes Activos

| Archivo | Propósito | Datos consumidos |
|---------|-----------|-----------------|
| `Sidebar.jsx` | Navegación lateral colapsable con acordeón para Estructura Org. | Estado: `vistaActual` |
| `Overview.jsx` | Dashboard: KPI cards + gráfico de barras por departamento | `business.ibm_hr` (legacy) |
| `Compensations.jsx` | Scatter plot: Edad vs Tarifa Diaria con flag de fuga | `business.ibm_hr` (legacy) |
| `EmployeeTable.jsx` | Tabla cruda con indicadores de riesgo de deserción | `business.ibm_hr` (legacy) |
| `OrgStructure.jsx` | Landing page del módulo Estructura Org. (3 cards) | Navegación pura |
| `OrganigramaIntegral.jsx` | Organigrama jerárquico visual (estático, pendiente integración con `v_org_tree_byNapo`) | Datos hardcodeados |

### 5.2 Enrutamiento — `App.jsx`

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
        {/* Renderizado condicional por estado */}
        {vistaActual === 'vision_general' && <Overview data={empleados} />}
        {vistaActual === 'estructura' && <OrgStructure setVistaActual={setVistaActual} />} 
        {vistaActual === 'org_integral' && <OrganigramaIntegral />}
        {vistaActual === 'compensaciones' && <Compensaciones data={empleados} />}
        {vistaActual === 'auditoria' && <EmployeeTable data={empleados} />}

        {/* Placeholders para módulos futuros */}
        {['fuga_talento', 'desempeno', 'turnos', 'reclutamiento', 
          'capacitacion', 'clima', 'diversidad', 'org_dotacion', 'org_costos'
        ].includes(vistaActual) && (
          <div>Módulo en Construcción 🚀</div>
        )}
      </main>
    </div>
  )
}
```

### 5.3 Cliente Supabase — `supabaseClient.js`

```javascript
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
```

---

## 6. Variables de Entorno (.env)

### 6.1 Root `.env` (Backend / ETL Pipeline)

```
VITE_SUPABASE_URL=***
VITE_SUPABASE_ANON_KEY=***
SUPABASE_SERVICE_KEY=***
DATABASE_URL=***
```

### 6.2 `client/.env` (Frontend / Vite)

```
VITE_SUPABASE_URL=***
VITE_SUPABASE_ANON_KEY=***
```

> **Nota de seguridad:** Los scripts ETL consumen `DATABASE_URL` via `python-dotenv`. El frontend consume `VITE_SUPABASE_URL` y `VITE_SUPABASE_ANON_KEY` via `import.meta.env` (Vite).

---

## 🧠 Notas Técnicas Importantes

1. **Case-Sensitivity PostgreSQL:** Los nombres de tabla `byNapo` deben citarse con comillas dobles (`"ibm_hr_monthly_snapshot_byNapo"`) en todo SQL manual. PostgreSQL foldea identificadores sin comillas a lowercase. Pandas `to_sql` siempre cita los nombres automáticamente.

2. **Ingesta como TEXT:** ETL 06 lee el CSV con `dtype=str` y usa `df.where(df.notna(), None)` para enviar todo como TEXT puro a la capa raw, evitando conflictos de tipo con PostgreSQL.

3. **Clean Slate:** ETL 07 destruye y recrea el esquema `business` en cada ejecución (`DROP SCHEMA CASCADE`). Esto garantiza idempotencia y evita conflictos con vistas materializadas previas.

4. **REFRESH sin CONCURRENTLY:** La vista materializada se refresca sin `CONCURRENTLY` para evitar el error de prerequisito (requiere un UNIQUE INDEX preexistente en la primera ejecución).

5. **Frontend pendiente:** Los componentes activos (`Overview`, `Compensations`, `EmployeeTable`) consumen el dataset legacy `business.ibm_hr`. La integración con las vistas potenciadas (`v_employee_full_byNapo`, `mv_monthly_kpis_byNapo`) está pendiente.
