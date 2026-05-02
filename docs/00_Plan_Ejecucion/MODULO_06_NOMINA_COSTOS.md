# 📊 Módulo 06: Nómina, Costos & Equity - Plan Detallado

> **Script Python:** `m06_nomina_costos.py`  
> **Prioridad:** ALTA  
> **Estado:** 🟡 Parcial (1/6 vistas implementadas)  
> **Dependencias:** m05_fuerza_laboral (datos salariales)  
> **Tags Metodológicos:** DESC, PRED

---

## 🎯 Objetivo del Módulo

Gestionar y analizar todos los aspectos relacionados con compensaciones, nómina, equidad salarial y el impacto financiero de la rotación. Proporciona herramientas para simulación de escenarios salariales y benchmarking interno.

**Usuarios objetivo:** Compensation & Benefits Manager, CFO, HR Finance Partner, Payroll Manager

**Frecuencia de actualización:** Mensual (MVs), Tiempo real (simulador)

---

## 📁 Fuentes de Datos

### Existentes (ya disponibles)
- `business.v_employee_full_byNapo` → Contiene `monthly_salary_usd`, `department_name`, `country_iso3`, etc.
- `business.mv_monthly_kpis_byNapo` → KPIs mensuales con salario promedio

### Nuevas (NO requiere tablas RAW adicionales)
- Todo se deriva de datos existentes en el módulo 05

---

## 🗂️ Vistas Detalladas

### 1. Equidad Interna ✅ IMPLEMENTADA

**Objeto:** Ya existe consulta directa desde frontend (sin MV dedicada)

**Componente React:** `Compensations.jsx`

**Visualización actual:** Scatter plot edad vs tarifa diaria, coloreado por attrition

**Mejora sugerida:** Crear MV para optimizar consulta:
```sql
CREATE MATERIALIZED VIEW business.mv_pay_equity_scatter AS
SELECT 
    snapshot_date,
    employee_id,
    age,
    monthly_salary_usd,
    ROUND(monthly_salary_usd / 22, 2) as daily_rate_usd,
    attrition,
    gender,
    department_name,
    job_level_1
FROM business.v_employee_full_byNapo
WHERE is_active_at_snapshot = TRUE OR termination_date IS NOT NULL;

CREATE INDEX idx_mv_equity_snap_m06 ON business.mv_pay_equity_scatter (snapshot_date);
```

---

### 2. Bandas Salariales 🔘 PENDIENTE

**Objeto:** `business.mv_salary_bands` (Materialized View)

**Propósito:** Definir rangos salariales (P10, P25, P50, P75, P90) por puesto, departamento y país para establecer políticas de compensación competitivas.

**Columnas:**
| Columna | Tipo | Descripción | Ejemplo |
|---------|------|-------------|---------|
| snapshot_date | DATE | Fecha de corte | 2026-03-31 |
| country_iso3 | TEXT | Código ISO del país | PER, CHL, COL |
| department_name | TEXT | Departamento | IT, Sales, HR |
| job_role | TEXT | Rol específico | Software Engineer, Sales Manager |
| job_level_1 | TEXT | Nivel jerárquico | Manager, Senior, Junior |
| employee_count | INTEGER | Número de empleados en la banda | 45 |
| p10 | NUMERIC | Percentil 10 (mínimo del mercado) | 2800 |
| p25 | NUMERIC | Percentil 25 (Q1) | 3200 |
| p50 | NUMERIC | Percentil 50 (mediana) | 3800 |
| p75 | NUMERIC | Percentil 75 (Q3) | 4500 |
| p90 | NUMERIC | Percentil 90 (máximo del mercado) | 5200 |
| avg_salary | NUMERIC | Salario promedio | 3950 |
| min_salary | NUMERIC | Salario mínimo observado | 2500 |
| max_salary | NUMERIC | Salario máximo observado | 6000 |
| salary_range_pct | NUMERIC | Rango salarial (%) | 140.0 |

**SQL de creación:**
```sql
CREATE MATERIALIZED VIEW business.mv_salary_bands AS
SELECT 
    snapshot_date,
    country_iso3,
    department_name,
    job_role,
    job_level_1,
    COUNT(*) FILTER (WHERE is_active_at_snapshot = TRUE AND monthly_salary_usd IS NOT NULL) as employee_count,
    PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE) as p10,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE) as p25,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE) as p50,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE) as p75,
    PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE) as p90,
    ROUND(AVG(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE), 2) as avg_salary,
    MIN(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE) as min_salary,
    MAX(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE) as max_salary,
    ROUND((MAX(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE) / 
           NULLIF(MIN(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE), 0) * 100) - 100, 1) as salary_range_pct
FROM business.v_employee_full_byNapo
WHERE monthly_salary_usd IS NOT NULL
GROUP BY snapshot_date, country_iso3, department_name, job_role, job_level_1;

CREATE INDEX idx_mv_salary_bands_snap_m06 ON business.mv_salary_bands (snapshot_date);
CREATE INDEX idx_mv_salary_bands_role_m06 ON business.mv_salary_bands (job_role);
CREATE INDEX idx_mv_salary_bands_dept_m06 ON business.mv_salary_bands (department_name);
```

**Visualizaciones sugeridas:**
1. **Box Plot:** Distribución salarial por job role (mostrando P25, P50, P75, outliers)
2. **Tabla de Bandas:** Listado filtrable con todas las bandas salariales
3. **Curva de Progresión:** Línea que muestra progresión salarial por nivel (Junior → Senior → Manager)

**Componente React a crear:** `SalaryBands.jsx`

**RPC sugerida:**
```sql
CREATE OR REPLACE FUNCTION business.get_salary_bands(
    p_period_date DATE,
    p_country TEXT DEFAULT NULL,
    p_department TEXT DEFAULT NULL,
    p_job_role TEXT DEFAULT NULL
) RETURNS JSON AS $$
-- Retorna: bands_summary, boxplot_data, progression_curve
$$ LANGUAGE plpgsql;
```

---

### 3. Compa-Ratio 🔘 PENDIENTE

**Objeto:** `business.mv_compa_ratio` (Materialized View)

**Propósito:** Calcular el Compa-Ratio (salario real vs punto medio de la banda) para evaluar equidad interna y posicionar a cada empleado en su rango salarial.

**Fórmula:** `Compa-Ratio = (Salario Empleado / Punto Medio de Banda) × 100`

**Columnas:**
| Columna | Tipo | Descripción | Ejemplo |
|---------|------|-------------|---------|
| snapshot_date | DATE | Fecha de corte | 2026-03-31 |
| employee_id | TEXT | ID del empleado | E12345 |
| full_name | TEXT | Nombre completo | Juan Pérez |
| job_role | TEXT | Rol | Software Engineer |
| department_name | TEXT | Departamento | IT |
| country_iso3 | TEXT | País | PER |
| monthly_salary_usd | NUMERIC | Salario mensual | 4200 |
| band_p50 | NUMERIC | Punto medio de banda (P50) | 3800 |
| compa_ratio_pct | NUMERIC | Compa-Ratio (%) | 110.5 |
| range_status | TEXT | Estado en el rango | SOBRE_P50, EN_RANGO, BAJO_P50 |
| quartile | INTEGER | Cuartil donde se ubica (1-4) | 3 |
| recommended_action | TEXT | Acción recomendada | Considerar ajuste, Mantener, Revisar |

**SQL de creación:**
```sql
CREATE MATERIALIZED VIEW business.mv_compa_ratio AS
WITH bandas AS (
    SELECT 
        snapshot_date,
        country_iso3,
        department_name,
        job_role,
        job_level_1,
        p50 as band_midpoint,
        p25 as band_min,
        p75 as band_max
    FROM business.mv_salary_bands
    WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM business.mv_salary_bands)
)
SELECT 
    e.snapshot_date,
    e.employee_id,
    e.full_name,
    e.job_role,
    e.department_name,
    e.country_iso3,
    e.monthly_salary_usd,
    b.band_midpoint,
    ROUND((e.monthly_salary_usd / NULLIF(b.band_midpoint, 0)) * 100, 1) as compa_ratio_pct,
    CASE 
        WHEN e.monthly_salary_usd > b.band_max THEN 'SOBRE_MAXIMO'
        WHEN e.monthly_salary_usd > b.band_midpoint THEN 'SOBRE_P50'
        WHEN e.monthly_salary_usd >= b.band_min THEN 'EN_RANGO'
        ELSE 'BAJO_MINIMO'
    END as range_status,
    CASE 
        WHEN e.monthly_salary_usd <= b.band_min THEN 1
        WHEN e.monthly_salary_usd <= b.band_midpoint THEN 2
        WHEN e.monthly_salary_usd <= b.band_max THEN 3
        ELSE 4
    END as quartile,
    CASE 
        WHEN e.monthly_salary_usd < b.band_min THEN 'Revisar ajuste urgente'
        WHEN e.monthly_salary_usd > b.band_max THEN 'Evaluar promoción o congelamiento'
        WHEN (e.monthly_salary_usd / b.band_midpoint) * 100 < 90 THEN 'Considerar ajuste por mérito'
        ELSE 'Mantener - dentro de rango competitivo'
    END as recommended_action
FROM business.v_employee_full_byNapo e
LEFT JOIN bandas b 
    ON e.job_role = b.job_role 
    AND e.department_name = b.department_name 
    AND e.country_iso3 = b.country_iso3
    AND e.job_level_1 = b.job_level_1
WHERE e.snapshot_date = (SELECT MAX(snapshot_date) FROM business.v_employee_full_byNapo)
  AND e.monthly_salary_usd IS NOT NULL;

CREATE INDEX idx_mv_compa_snap_m06 ON business.mv_compa_ratio (snapshot_date);
CREATE INDEX idx_mv_compa_emp_m06 ON business.mv_compa_ratio (employee_id);
CREATE INDEX idx_mv_compa_status_m06 ON business.mv_compa_ratio (range_status);
```

**Visualizaciones sugeridas:**
1. **Histograma:** Distribución de empleados por Compa-Ratio (rangos de 10%)
2. **Scatter Plot:** Salario vs Compa-Ratio, coloreado por departamento
3. **Tabla de Acciones:** Listado de empleados que requieren acción (fuera de rango)

**Componente React a crear:** `CompaRatio.jsx`

**RPC sugerida:**
```sql
CREATE OR REPLACE FUNCTION business.get_compa_ratio_dashboard(
    p_period_date DATE,
    p_department TEXT DEFAULT NULL,
    p_range_status TEXT DEFAULT NULL
) RETURNS JSON AS $$
-- Retorna: distribution_histogram, employees_out_of_range, summary_stats
$$ LANGUAGE plpgsql;
```

---

### 4. Masa Salarial 🔘 PENDIENTE

**Objeto:** `business.mv_payroll_mass` (Materialized View)

**Propósito:** Analizar la evolución de la nómina total, crecimiento mes a mes (MoM) y año a año (YoY), desglosado por dimensiones organizacionales.

**Columnas:**
| Columna | Tipo | Descripción | Ejemplo |
|---------|------|-------------|---------|
| snapshot_date | DATE | Fecha de corte | 2026-03-31 |
| country_iso3 | TEXT | Código ISO del país | PER |
| department_name | TEXT | Departamento | IT |
| job_level_1 | TEXT | Nivel jerárquico | Manager |
| headcount_active | INTEGER | Empleados activos | 125 |
| total_monthly_payroll | NUMERIC | Nómina mensual total (USD) | 485000 |
| avg_salary_per_employee | NUMERIC | Salario promedio | 3880 |
| payroll_growth_mom | NUMERIC | Crecimiento vs mes anterior (%) | 2.3 |
| payroll_growth_yoy | NUMERIC | Crecimiento vs mismo mes año anterior (%) | 8.5 |
| headcount_growth_mom | NUMERIC | Crecimiento HC vs mes anterior (%) | 1.8 |
| payroll_as_pct_of_total | NUMERIC | % de la nómina total de la empresa | 12.5 |

**SQL de creación:**
```sql
CREATE MATERIALIZED VIEW business.mv_payroll_mass AS
WITH payroll_base AS (
    SELECT 
        snapshot_date,
        country_iso3,
        department_name,
        job_level_1,
        COUNT(*) FILTER (WHERE is_active_at_snapshot = TRUE) as headcount_active,
        SUM(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE) as total_monthly_payroll,
        AVG(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE) as avg_salary_per_employee
    FROM business.v_employee_full_byNapo
    WHERE monthly_salary_usd IS NOT NULL
    GROUP BY snapshot_date, country_iso3, department_name, job_level_1
),
payroll_con_total AS (
    SELECT 
        snapshot_date,
        SUM(total_monthly_payroll) as company_total_payroll
    FROM payroll_base
    GROUP BY snapshot_date
)
SELECT 
    pb.snapshot_date,
    pb.country_iso3,
    pb.department_name,
    pb.job_level_1,
    pb.headcount_active,
    pb.total_monthly_payroll,
    pb.avg_salary_per_employee,
    ROUND(
        (pb.total_monthly_payroll - LAG(pb.total_monthly_payroll) OVER (
            PARTITION BY pb.country_iso3, pb.department_name, pb.job_level_1 
            ORDER BY pb.snapshot_date
        )) / NULLIF(LAG(pb.total_monthly_payroll) OVER (
            PARTITION BY pb.country_iso3, pb.department_name, pb.job_level_1 
            ORDER BY pb.snapshot_date
        ), 0) * 100, 2
    ) as payroll_growth_mom,
    ROUND(
        (pb.total_monthly_payroll - LAG(pb.total_monthly_payroll, 12) OVER (
            PARTITION BY pb.country_iso3, pb.department_name, pb.job_level_1 
            ORDER BY pb.snapshot_date
        )) / NULLIF(LAG(pb.total_monthly_payroll, 12) OVER (
            PARTITION BY pb.country_iso3, pb.department_name, pb.job_level_1 
            ORDER BY pb.snapshot_date
        ), 0) * 100, 2
    ) as payroll_growth_yoy,
    ROUND(
        (pb.headcount_active - LAG(pb.headcount_active) OVER (
            PARTITION BY pb.country_iso3, pb.department_name, pb.job_level_1 
            ORDER BY pb.snapshot_date
        )) / NULLIF(LAG(pb.headcount_active) OVER (
            PARTITION BY pb.country_iso3, pb.department_name, pb.job_level_1 
            ORDER BY pb.snapshot_date
        ), 0) * 100, 2
    ) as headcount_growth_mom,
    ROUND(
        pb.total_monthly_payroll / NULLIF(pct.company_total_payroll, 0) * 100, 2
    ) as payroll_as_pct_of_total
FROM payroll_base pb
JOIN payroll_con_total pct ON pb.snapshot_date = pct.snapshot_date;

CREATE INDEX idx_mv_payroll_snap_m06 ON business.mv_payroll_mass (snapshot_date);
CREATE INDEX idx_mv_payroll_dept_m06 ON business.mv_payroll_mass (department_name);
CREATE INDEX idx_mv_payroll_country_m06 ON business.mv_payroll_mass (country_iso3);
```

**Visualizaciones sugeridas:**
1. **Línea de Tendencia:** Evolución de masa salarial últimos 12 meses (total + desglose por dept)
2. **Waterfall Chart:** Desglose de variación MoM (altas, bajas, aumentos, promociones)
3. **Treemap:** Distribución de masa salarial por departamento/país

**Componente React a crear:** `PayrollMass.jsx`

**RPC sugerida:**
```sql
CREATE OR REPLACE FUNCTION business.get_payroll_mass_dashboard(
    p_period_date DATE,
    p_country TEXT DEFAULT NULL,
    p_department TEXT DEFAULT NULL
) RETURNS JSON AS $$
-- Retorna: trend_12m, waterfall_data, treemap_data, kpi_summary
$$ LANGUAGE plpgsql;
```

---

### 5. Impacto Financiero de Rotación 🔘 PENDIENTE

**Objeto:** `business.mv_turnover_financial_impact` (Materialized View)

**Propósito:** Calcular el costo financiero total de la rotación de personal, incluyendo costos de reclutamiento, onboarding, pérdida de productividad y costos de salida.

**Fórmulas clave:**
- **Costo de Reemplazo:** 50%-200% del salario anual (dependiendo del nivel)
- **Costo de Reclutamiento:** $3,000-$10,000 por posición (promedio)
- **Pérdida de Productividad:** 30%-50% durante primeros 3 meses

**Columnas:**
| Columna | Tipo | Descripción | Ejemplo |
|---------|------|-------------|---------|
| snapshot_date | DATE | Fecha de corte | 2026-03-31 |
| country_iso3 | TEXT | País | PER |
| department_name | TEXT | Departamento | IT |
| job_level_1 | TEXT | Nivel | Senior |
| terminations_count | INTEGER | Número de bajas en el mes | 8 |
| avg_salary_annual | NUMERIC | Salario anual promedio de quienes salieron | 54000 |
| replacement_cost_estimate | NUMERIC | Costo estimado de reemplazo (75% salario anual) | 324000 |
| recruitment_cost | NUMERIC | Costo de reclutamiento ($5k × bajas) | 40000 |
| productivity_loss | NUMERIC | Pérdida de productividad estimada | 81000 |
| total_impact | NUMERIC | Impacto financiero total | 445000 |
| impact_per_termination | NUMERIC | Impacto promedio por baja | 55625 |
| turnover_rate_pct | NUMERIC | Tasa de rotación (%) | 2.8 |

**SQL de creación:**
```sql
CREATE MATERIALIZED VIEW business.mv_turnover_financial_impact AS
WITH terminations AS (
    SELECT 
        snapshot_date,
        country_iso3,
        department_name,
        job_level_1,
        COUNT(*) FILTER (WHERE termination_date BETWEEN DATE_TRUNC('month', snapshot_date) AND snapshot_date) as terminations_count,
        AVG(monthly_salary_usd) FILTER (WHERE termination_date BETWEEN DATE_TRUNC('month', snapshot_date) AND snapshot_date) as avg_salary_monthly,
        COUNT(*) FILTER (WHERE is_active_at_snapshot = TRUE OR termination_date BETWEEN DATE_TRUNC('month', snapshot_date) AND snapshot_date) as headcount_total
    FROM business.v_employee_full_byNapo
    GROUP BY snapshot_date, country_iso3, department_name, job_level_1
)
SELECT 
    snapshot_date,
    country_iso3,
    department_name,
    job_level_1,
    terminations_count,
    ROUND(avg_salary_monthly * 12, 2) as avg_salary_annual,
    -- Costo de reemplazo: 75% del salario anual (ajustable por nivel)
    ROUND(terminations_count * avg_salary_monthly * 12 * 
        CASE 
            WHEN job_level_1 LIKE '%Manager%' OR job_level_1 LIKE '%Director%' THEN 1.5
            WHEN job_level_1 LIKE '%Senior%' THEN 1.0
            ELSE 0.75
        END, 2) as replacement_cost_estimate,
    -- Costo de reclutamiento: $5,000 por posición
    ROUND(terminations_count * 5000, 2) as recruitment_cost,
    -- Pérdida de productividad: 40% del salario mensual × 3 meses
    ROUND(terminations_count * avg_salary_monthly * 3 * 0.40, 2) as productivity_loss,
    -- Impacto total
    ROUND(
        terminations_count * avg_salary_monthly * 12 * 
        CASE 
            WHEN job_level_1 LIKE '%Manager%' OR job_level_1 LIKE '%Director%' THEN 1.5
            WHEN job_level_1 LIKE '%Senior%' THEN 1.0
            ELSE 0.75
        END +
        terminations_count * 5000 +
        terminations_count * avg_salary_monthly * 3 * 0.40, 2
    ) as total_impact,
    ROUND(
        (terminations_count * avg_salary_monthly * 12 * 
        CASE 
            WHEN job_level_1 LIKE '%Manager%' OR job_level_1 LIKE '%Director%' THEN 1.5
            WHEN job_level_1 LIKE '%Senior%' THEN 1.0
            ELSE 0.75
        END +
        terminations_count * 5000 +
        terminations_count * avg_salary_monthly * 3 * 0.40) / NULLIF(terminations_count, 0), 2
    ) as impact_per_termination,
    ROUND(terminations_count::NUMERIC / NULLIF(headcount_total, 0) * 100, 2) as turnover_rate_pct
FROM terminations
WHERE terminations_count > 0;

CREATE INDEX idx_mv_turnover_impact_snap_m06 ON business.mv_turnover_financial_impact (snapshot_date);
CREATE INDEX idx_mv_turnover_impact_dept_m06 ON business.mv_turnover_financial_impact (department_name);
```

**Visualizaciones sugeridas:**
1. **KPI Cards:** Impacto total del mes, impacto por baja, tendencia YoY
2. **Gráfico de Barras Apiladas:** Desglose de costos (reemplazo + reclutamiento + productividad)
3. **Trend Line:** Evolución del impacto financiero últimos 12 meses

**Componente React a crear:** `TurnoverImpact.jsx`

**RPC sugerida:**
```sql
CREATE OR REPLACE FUNCTION business.get_turnover_impact_dashboard(
    p_period_date DATE,
    p_country TEXT DEFAULT NULL,
    p_department TEXT DEFAULT NULL
) RETURNS JSON AS $$
-- Retorna: kpi_summary, cost_breakdown, trend_12m, top_departments_by_impact
$$ LANGUAGE plpgsql;
```

---

### 6. Simulador Salarial 🔘 PENDIENTE

**Objeto:** `business.mv_salary_simulator` (Vista o Función)

**Propósito:** Permitir simular el impacto financiero de diferentes escenarios de ajustes salariales (aumento general, aumento por desempeño, promociones).

**Columnas:**
| Columna | Tipo | Descripción | Ejemplo |
|---------|------|-------------|---------|
| scenario_name | TEXT | Nombre del escenario | "Aumento General 5%", "Promociones Q2" |
| simulation_date | DATE | Fecha de simulación | 2026-03-31 |
| affected_employees | INTEGER | Número de empleados afectados | 450 |
| current_payroll | NUMERIC | Nómina actual | 1850000 |
| new_payroll | NUMERIC | Nueva nómina proyectada | 1942500 |
| incremental_cost_monthly | NUMERIC | Costo incremental mensual | 92500 |
| incremental_cost_annual | NUMERIC | Costo incremental anual | 1110000 |
| impact_on_compa_ratio | NUMERIC | Impacto promedio en Compa-Ratio (%) | 4.8 |
| budget_required | NUMERIC | Presupuesto requerido | 1110000 |
| roi_estimate | NUMERIC | ROI estimado (si aplica) | NULL |

**SQL de creación (vista base para simulaciones):**
```sql
CREATE OR REPLACE VIEW business.v_salary_simulator_base AS
SELECT 
    snapshot_date,
    employee_id,
    full_name,
    department_name,
    job_role,
    job_level_1,
    country_iso3,
    monthly_salary_usd as current_salary,
    compa_ratio_pct as current_compa_ratio
FROM business.v_employee_full_byNapo
WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM business.v_employee_full_byNapo)
  AND is_active_at_snapshot = TRUE
  AND monthly_salary_usd IS NOT NULL;
```

**Funciones de simulación (ejemplos):**
```sql
-- Escenario 1: Aumento general porcentual
CREATE OR REPLACE FUNCTION business.simulate_general_increase(
    p_period_date DATE,
    p_increase_pct NUMERIC
) RETURNS JSON AS $$
DECLARE result JSON;
BEGIN
    SELECT json_build_object(
        'scenario_name', 'Aumento General ' || p_increase_pct || '%',
        'affected_employees', COUNT(*),
        'current_payroll', SUM(current_salary),
        'new_payroll', SUM(current_salary * (1 + p_increase_pct / 100)),
        'incremental_cost_monthly', SUM(current_salary * p_increase_pct / 100),
        'incremental_cost_annual', SUM(current_salary * p_increase_pct / 100 * 12),
        'impact_on_compa_ratio', p_increase_pct,
        'budget_required', SUM(current_salary * p_increase_pct / 100 * 12)
    ) INTO result
    FROM business.v_salary_simulator_base
    WHERE snapshot_date = p_period_date;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- Escenario 2: Aumento por percentil de desempeño (requiere módulo 08)
-- Escenario 3: Promociones a siguiente nivel
```

**Visualizaciones sugeridas:**
1. **Formulario de Simulación:** Inputs para % aumento, filtro por departamento/nivel
2. **Comparativo Before/After:** Tabla comparativa de escenarios
3. **Sensitivity Analysis:** Gráfico de tornado mostrando impacto de diferentes variables

**Componente React a crear:** `SalarySimulator.jsx`

**RPCs sugeridas:**
```sql
-- Múltiples funciones según tipo de escenario
business.simulate_general_increase(DATE, NUMERIC)
business.simulate_promotion_scenario(DATE, TEXT[])
business.simulate_market_adjustment(DATE, NUMERIC, TEXT)
```

---

## 🐍 Script Python: `m06_nomina_costos.py`

### Estructura completa:

```python
import os
import time
from pathlib import Path
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Resolver ruta absoluta al .env
ETL_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ETL_DIR.parent
env_path = PROJECT_ROOT / ".env"
load_dotenv(env_path)
db_url = os.getenv("DATABASE_URL")

def setup_nomina_costos():
    start_time = time.time()
    print("\n" + "="*50)
    print("💰 [ETL M06] CONFIGURANDO DOMINIO: NÓMINA, COSTOS & EQUITY")
    print("="*50)
    
    if not db_url:
        print("❌ Error: DATABASE_URL no encontrada en .env")
        return

    engine = create_engine(db_url)

    sql_views = """
    -- ==========================================
    -- 1. VISTAS DE BANDAS SALARIALES
    -- ==========================================
    DROP MATERIALIZED VIEW IF EXISTS business.mv_salary_bands CASCADE;
    
    CREATE MATERIALIZED VIEW business.mv_salary_bands AS
    SELECT 
        snapshot_date,
        country_iso3,
        department_name,
        job_role,
        job_level_1,
        COUNT(*) FILTER (WHERE is_active_at_snapshot = TRUE AND monthly_salary_usd IS NOT NULL) as employee_count,
        PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE) as p10,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE) as p25,
        PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE) as p50,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE) as p75,
        PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE) as p90,
        ROUND(AVG(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE), 2) as avg_salary,
        MIN(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE) as min_salary,
        MAX(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE) as max_salary,
        ROUND((MAX(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE) / 
               NULLIF(MIN(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE), 0) * 100) - 100, 1) as salary_range_pct
    FROM business.v_employee_full_byNapo
    WHERE monthly_salary_usd IS NOT NULL
    GROUP BY snapshot_date, country_iso3, department_name, job_role, job_level_1;

    CREATE INDEX idx_mv_salary_bands_snap_m06 ON business.mv_salary_bands (snapshot_date);
    CREATE INDEX idx_mv_salary_bands_role_m06 ON business.mv_salary_bands (job_role);

    -- ==========================================
    -- 2. VISTAS DE COMPA-RATIO
    -- ==========================================
    DROP MATERIALIZED VIEW IF EXISTS business.mv_compa_ratio CASCADE;
    
    CREATE MATERIALIZED VIEW business.mv_compa_ratio AS
    WITH bandas AS (
        SELECT 
            snapshot_date, country_iso3, department_name, job_role, job_level_1,
            p50 as band_midpoint, p25 as band_min, p75 as band_max
        FROM business.mv_salary_bands
        WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM business.mv_salary_bands)
    )
    SELECT 
        e.snapshot_date, e.employee_id, e.full_name, e.job_role, e.department_name,
        e.country_iso3, e.monthly_salary_usd, b.band_midpoint,
        ROUND((e.monthly_salary_usd / NULLIF(b.band_midpoint, 0)) * 100, 1) as compa_ratio_pct,
        CASE 
            WHEN e.monthly_salary_usd > b.band_max THEN 'SOBRE_MAXIMO'
            WHEN e.monthly_salary_usd > b.band_midpoint THEN 'SOBRE_P50'
            WHEN e.monthly_salary_usd >= b.band_min THEN 'EN_RANGO'
            ELSE 'BAJO_MINIMO'
        END as range_status,
        CASE 
            WHEN e.monthly_salary_usd <= b.band_min THEN 1
            WHEN e.monthly_salary_usd <= b.band_midpoint THEN 2
            WHEN e.monthly_salary_usd <= b.band_max THEN 3
            ELSE 4
        END as quartile,
        CASE 
            WHEN e.monthly_salary_usd < b.band_min THEN 'Revisar ajuste urgente'
            WHEN e.monthly_salary_usd > b.band_max THEN 'Evaluar promoción o congelamiento'
            WHEN (e.monthly_salary_usd / b.band_midpoint) * 100 < 90 THEN 'Considerar ajuste por mérito'
            ELSE 'Mantener - dentro de rango competitivo'
        END as recommended_action
    FROM business.v_employee_full_byNapo e
    LEFT JOIN bandas b 
        ON e.job_role = b.job_role AND e.department_name = b.department_name 
        AND e.country_iso3 = b.country_iso3 AND e.job_level_1 = b.job_level_1
    WHERE e.snapshot_date = (SELECT MAX(snapshot_date) FROM business.v_employee_full_byNapo)
      AND e.monthly_salary_usd IS NOT NULL;

    CREATE INDEX idx_mv_compa_snap_m06 ON business.mv_compa_ratio (snapshot_date);
    CREATE INDEX idx_mv_compa_emp_m06 ON business.mv_compa_ratio (employee_id);

    -- ==========================================
    -- 3. VISTAS DE MASA SALARIAL
    -- ==========================================
    DROP MATERIALIZED VIEW IF EXISTS business.mv_payroll_mass CASCADE;
    
    CREATE MATERIALIZED VIEW business.mv_payroll_mass AS
    WITH payroll_base AS (
        SELECT 
            snapshot_date, country_iso3, department_name, job_level_1,
            COUNT(*) FILTER (WHERE is_active_at_snapshot = TRUE) as headcount_active,
            SUM(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE) as total_monthly_payroll,
            AVG(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE) as avg_salary_per_employee
        FROM business.v_employee_full_byNapo
        WHERE monthly_salary_usd IS NOT NULL
        GROUP BY snapshot_date, country_iso3, department_name, job_level_1
    ),
    payroll_con_total AS (
        SELECT snapshot_date, SUM(total_monthly_payroll) as company_total_payroll
        FROM payroll_base GROUP BY snapshot_date
    )
    SELECT 
        pb.snapshot_date, pb.country_iso3, pb.department_name, pb.job_level_1,
        pb.headcount_active, pb.total_monthly_payroll, pb.avg_salary_per_employee,
        ROUND(
            (pb.total_monthly_payroll - LAG(pb.total_monthly_payroll) OVER (
                PARTITION BY pb.country_iso3, pb.department_name, pb.job_level_1 ORDER BY pb.snapshot_date
            )) / NULLIF(LAG(pb.total_monthly_payroll) OVER (
                PARTITION BY pb.country_iso3, pb.department_name, pb.job_level_1 ORDER BY pb.snapshot_date
            ), 0) * 100, 2
        ) as payroll_growth_mom,
        ROUND(
            (pb.total_monthly_payroll - LAG(pb.total_monthly_payroll, 12) OVER (
                PARTITION BY pb.country_iso3, pb.department_name, pb.job_level_1 ORDER BY pb.snapshot_date
            )) / NULLIF(LAG(pb.total_monthly_payroll, 12) OVER (
                PARTITION BY pb.country_iso3, pb.department_name, pb.job_level_1 ORDER BY pb.snapshot_date
            ), 0) * 100, 2
        ) as payroll_growth_yoy,
        ROUND(pb.total_monthly_payroll / NULLIF(pct.company_total_payroll, 0) * 100, 2) as payroll_as_pct_of_total
    FROM payroll_base pb
    JOIN payroll_con_total pct ON pb.snapshot_date = pct.snapshot_date;

    CREATE INDEX idx_mv_payroll_snap_m06 ON business.mv_payroll_mass (snapshot_date);

    -- ==========================================
    -- 4. VISTAS DE IMPACTO DE ROTACIÓN
    -- ==========================================
    DROP MATERIALIZED VIEW IF EXISTS business.mv_turnover_financial_impact CASCADE;
    
    CREATE MATERIALIZED VIEW business.mv_turnover_financial_impact AS
    WITH terminations AS (
        SELECT 
            snapshot_date, country_iso3, department_name, job_level_1,
            COUNT(*) FILTER (WHERE termination_date BETWEEN DATE_TRUNC('month', snapshot_date) AND snapshot_date) as terminations_count,
            AVG(monthly_salary_usd) FILTER (WHERE termination_date BETWEEN DATE_TRUNC('month', snapshot_date) AND snapshot_date) as avg_salary_monthly,
            COUNT(*) FILTER (WHERE is_active_at_snapshot = TRUE OR termination_date BETWEEN DATE_TRUNC('month', snapshot_date) AND snapshot_date) as headcount_total
        FROM business.v_employee_full_byNapo
        GROUP BY snapshot_date, country_iso3, department_name, job_level_1
    )
    SELECT 
        snapshot_date, country_iso3, department_name, job_level_1,
        terminations_count,
        ROUND(avg_salary_monthly * 12, 2) as avg_salary_annual,
        ROUND(terminations_count * avg_salary_monthly * 12 * 
            CASE 
                WHEN job_level_1 LIKE '%Manager%' OR job_level_1 LIKE '%Director%' THEN 1.5
                WHEN job_level_1 LIKE '%Senior%' THEN 1.0
                ELSE 0.75
            END, 2) as replacement_cost_estimate,
        ROUND(terminations_count * 5000, 2) as recruitment_cost,
        ROUND(terminations_count * avg_salary_monthly * 3 * 0.40, 2) as productivity_loss,
        ROUND(
            terminations_count * avg_salary_monthly * 12 * 
            CASE 
                WHEN job_level_1 LIKE '%Manager%' OR job_level_1 LIKE '%Director%' THEN 1.5
                WHEN job_level_1 LIKE '%Senior%' THEN 1.0
                ELSE 0.75
            END +
            terminations_count * 5000 +
            terminations_count * avg_salary_monthly * 3 * 0.40, 2
        ) as total_impact,
        ROUND(terminations_count::NUMERIC / NULLIF(headcount_total, 0) * 100, 2) as turnover_rate_pct
    FROM terminations
    WHERE terminations_count > 0;

    CREATE INDEX idx_mv_turnover_impact_snap_m06 ON business.mv_turnover_financial_impact (snapshot_date);

    -- ==========================================
    -- 5. VISTA BASE PARA SIMULADOR
    -- ==========================================
    DROP VIEW IF EXISTS business.v_salary_simulator_base CASCADE;
    
    CREATE OR REPLACE VIEW business.v_salary_simulator_base AS
    SELECT 
        snapshot_date, employee_id, full_name, department_name, job_role,
        job_level_1, country_iso3, monthly_salary_usd as current_salary
    FROM business.v_employee_full_byNapo
    WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM business.v_employee_full_byNapo)
      AND is_active_at_snapshot = TRUE
      AND monthly_salary_usd IS NOT NULL;

    -- Permisos
    GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
    """

    sql_rpcs = """
    -- ==========================================
    -- 6. FUNCIONES RPC PARA FRONTEND
    -- ==========================================
    
    -- RPC: Bandas Salariales
    DROP FUNCTION IF EXISTS business.get_salary_bands(DATE, TEXT, TEXT, TEXT);
    
    CREATE OR REPLACE FUNCTION business.get_salary_bands(
        p_period_date DATE,
        p_country TEXT DEFAULT NULL,
        p_department TEXT DEFAULT NULL,
        p_job_role TEXT DEFAULT NULL
    ) RETURNS JSON AS $$
    DECLARE result JSON;
    BEGIN
        SELECT json_build_object(
            'bands_summary', (SELECT COALESCE(json_agg(t), '[]'::json) FROM (
                SELECT job_role, job_level_1, employee_count, p25, p50, p75, avg_salary
                FROM business.mv_salary_bands
                WHERE snapshot_date = p_period_date
                  AND (p_country IS NULL OR country_iso3 = p_country)
                  AND (p_department IS NULL OR department_name = p_department)
                  AND (p_job_role IS NULL OR job_role = p_job_role)
                ORDER BY job_level_1, job_role
            ) t),
            'boxplot_data', (SELECT COALESCE(json_agg(t), '[]'::json) FROM (
                SELECT job_role, p25 as q1, p50 as median, p75 as q3, min_salary as min, max_salary as max
                FROM business.mv_salary_bands
                WHERE snapshot_date = p_period_date
                ORDER BY job_role
            ) t)
        ) INTO result;
        RETURN result;
    END;
    $$ LANGUAGE plpgsql;
    
    -- RPC: Compa-Ratio
    DROP FUNCTION IF EXISTS business.get_compa_ratio_dashboard(DATE, TEXT, TEXT);
    
    CREATE OR REPLACE FUNCTION business.get_compa_ratio_dashboard(
        p_period_date DATE,
        p_department TEXT DEFAULT NULL,
        p_range_status TEXT DEFAULT NULL
    ) RETURNS JSON AS $$
    DECLARE result JSON;
    BEGIN
        SELECT json_build_object(
            'distribution_histogram', (SELECT COALESCE(json_agg(t), '[]'::json) FROM (
                SELECT 
                    CASE 
                        WHEN compa_ratio_pct < 80 THEN '<80%'
                        WHEN compa_ratio_pct < 90 THEN '80-90%'
                        WHEN compa_ratio_pct < 100 THEN '90-100%'
                        WHEN compa_ratio_pct < 110 THEN '100-110%'
                        WHEN compa_ratio_pct < 120 THEN '110-120%'
                        ELSE '>120%'
                    END as bucket,
                    COUNT(*) as employee_count
                FROM business.mv_compa_ratio
                WHERE snapshot_date = p_period_date
                  AND (p_department IS NULL OR department_name = p_department)
                  AND (p_range_status IS NULL OR range_status = p_range_status)
                GROUP BY bucket
                ORDER BY bucket
            ) t),
            'employees_out_of_range', (SELECT COALESCE(json_agg(t), '[]'::json) FROM (
                SELECT employee_id, full_name, job_role, compa_ratio_pct, range_status, recommended_action
                FROM business.mv_compa_ratio
                WHERE snapshot_date = p_period_date
                  AND range_status IN ('BAJO_MINIMO', 'SOBRE_MAXIMO')
                LIMIT 50
            ) t)
        ) INTO result;
        RETURN result;
    END;
    $$ LANGUAGE plpgsql;
    
    -- RPC: Masa Salarial
    DROP FUNCTION IF EXISTS business.get_payroll_mass_dashboard(DATE, TEXT, TEXT);
    
    -- RPC: Impacto de Rotación
    DROP FUNCTION IF EXISTS business.get_turnover_impact_dashboard(DATE, TEXT, TEXT);
    
    -- RPC: Simulador (aumento general)
    DROP FUNCTION IF EXISTS business.simulate_general_increase(DATE, NUMERIC);
    
    CREATE OR REPLACE FUNCTION business.simulate_general_increase(
        p_period_date DATE,
        p_increase_pct NUMERIC
    ) RETURNS JSON AS $$
    DECLARE result JSON;
    BEGIN
        SELECT json_build_object(
            'scenario_name', 'Aumento General ' || p_increase_pct || '%',
            'affected_employees', COUNT(*),
            'current_payroll', SUM(current_salary),
            'new_payroll', SUM(current_salary * (1 + p_increase_pct / 100)),
            'incremental_cost_monthly', SUM(current_salary * p_increase_pct / 100),
            'incremental_cost_annual', SUM(current_salary * p_increase_pct / 100 * 12),
            'impact_on_compa_ratio', p_increase_pct,
            'budget_required', SUM(current_salary * p_increase_pct / 100 * 12)
        ) INTO result
        FROM business.v_salary_simulator_base
        WHERE snapshot_date = p_period_date;
        
        RETURN result;
    END;
    $$ LANGUAGE plpgsql;
    
    GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA business TO anon;
    """

    try:
        with engine.begin() as conn:
            print("⏳ Creando Vistas de Nómina y Costos (M06)...")
            conn.execute(text(sql_views))
            
            print("⏳ Creando Funciones RPC (M06)...")
            conn.execute(text(sql_rpcs))
            
            print("⏳ Refrescando Materialized Views...")
            conn.execute(text("REFRESH MATERIALIZED VIEW business.mv_salary_bands;"))
            conn.execute(text("REFRESH MATERIALIZED VIEW business.mv_compa_ratio;"))
            conn.execute(text("REFRESH MATERIALIZED VIEW business.mv_payroll_mass;"))
            conn.execute(text("REFRESH MATERIALIZED VIEW business.mv_turnover_financial_impact;"))
            
        elapsed = time.time() - start_time
        print(f"\n✅ Módulo 06 completado en {elapsed:.2f} segundos")
        
    except Exception as e:
        print(f"\n❌ Error en Módulo 06: {str(e)}")
        raise

if __name__ == "__main__":
    setup_nomina_costos()
```

---

## 📊 Resumen de Implementación

### Objetos a crear:
- [ ] 5 Materialized Views (`mv_salary_bands`, `mv_compa_ratio`, `mv_payroll_mass`, `mv_turnover_financial_impact`)
- [ ] 1 Vista simple (`v_salary_simulator_base`)
- [ ] 5+ Funciones RPC (`get_salary_bands`, `get_compa_ratio_dashboard`, `get_payroll_mass_dashboard`, `get_turnover_impact_dashboard`, `simulate_general_increase`)

### Componentes React a crear:
- [ ] `SalaryBands.jsx`
- [ ] `CompaRatio.jsx`
- [ ] `PayrollMass.jsx`
- [ ] `TurnoverImpact.jsx`
- [ ] `SalarySimulator.jsx`

### Archivos a modificar:
- [ ] `etl_pipeline/00_full_run_pipeline.py` → Agregar `m06_nomina_costos.py`
- [ ] `client/src/App.jsx` → Registrar nuevas rutas
- [ ] `client/src/modules/06-nomina-costos/` → Crear carpeta con componentes

### Estimación de esfuerzo:
- **Backend (SQL + Python):** 8-10 horas
- **Frontend (React + ECharts):** 12-15 horas
- **Testing + QA:** 3-4 horas
- **Total:** 23-29 horas (~3-4 días)

---

## 🔗 Dependencias Cruzadas

### Este módulo depende de:
- ✅ `business.v_employee_full_byNapo` (m05)
- ✅ `business.mv_monthly_kpis_byNapo` (m05)

### Otros módulos dependen de este:
- 🔲 Módulo 01 (Visión Ejecutiva) → Usará benchmarking salarial
- 🔲 Módulo 08 (Desempeño) → Vinculará compensación con performance
- 🔲 Módulo 10 (Engagement) → Correlacionará equidad con engagement

---

*Documento generado como parte del pipeline de documentación GDH Analytics*
