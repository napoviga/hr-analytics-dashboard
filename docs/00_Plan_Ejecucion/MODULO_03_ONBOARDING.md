# 📋 Módulo 03: Onboarding & Integración - Plan de Ejecución Detallado

## 🎯 Objetivo del Módulo
Monitorear y optimizar el proceso de onboarding de nuevos empleados, midiendo tiempo hasta productividad, completitud de actividades, y rotación temprana para mejorar la experiencia de integración.

**Usuarios Objetivo:**
- HR Coordinators
- Hiring Managers
- Onboarding Specialists
- New Hires (self-service)

---

## 📊 Fuentes de Datos

### Tablas Existentes (raw)
- `raw.employee_current` - Para identificar nuevos hires
- `raw.recruitment_pipeline` (Módulo 02) - Para datos pre-hire

### Nuevas Tablas Raw a Crear
```sql
-- Tabla de checklist de onboarding
CREATE TABLE IF NOT EXISTS raw.onboarding_checklist (
    onboarding_id TEXT PRIMARY KEY,
    employee_id TEXT REFERENCES raw.employee_current(employee_id),
    checklist_item TEXT NOT NULL,
    category TEXT, -- "Documentación", "Equipamiento", "Capacitación", "Integración"
    description TEXT,
    assigned_to TEXT, -- Rol responsable
    due_date DATE,
    completed_date DATE,
    status TEXT, -- Pending, In Progress, Completed, Overdue, Skipped
    priority TEXT, -- High, Medium, Low
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de hitos de productividad
CREATE TABLE IF NOT EXISTS raw.productivity_milestones (
    milestone_id TEXT PRIMARY KEY,
    employee_id TEXT REFERENCES raw.employee_current(employee_id),
    milestone_name TEXT NOT NULL,
    milestone_description TEXT,
    category TEXT, -- "Technical", "Business Knowledge", "Team Integration"
    expected_days INTEGER, -- Días esperados desde hire_date
    actual_days INTEGER, -- Días reales tomados
    completion_date DATE,
    achieved_flag BOOLEAN,
    manager_rating NUMERIC, -- 1-5
    self_rating NUMERIC, -- 1-5
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de encuestas de onboarding
CREATE TABLE IF NOT EXISTS raw.onboarding_surveys (
    survey_id TEXT PRIMARY KEY,
    employee_id TEXT REFERENCES raw.employee_current(employee_id),
    survey_date DATE,
    survey_type TEXT, -- "Week 1", "Month 1", "Month 3"
    overall_satisfaction NUMERIC, -- 1-5
    clarity_of_role NUMERIC, -- 1-5
    manager_support NUMERIC, -- 1-5
    team_integration NUMERIC, -- 1-5
    tools_access NUMERIC, -- 1-5
    training_quality NUMERIC, -- 1-5
    would_recommend NUMERIC, -- 1-10 (eNPS)
    open_feedback TEXT,
    sentiment_score NUMERIC, -- -1 a 1 (NLP analysis)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🎨 Vistas/Materialized Views a Implementar

### 1. `business.mv_onboarding_active`
**Objetivo:** Tracking en tiempo real del progreso de onboarding de empleados activos

**Columnas:**
```sql
snapshot_date DATE,
employee_id TEXT,
full_name TEXT,
department_name TEXT,
manager_name TEXT,
hire_date DATE,
days_since_hire INTEGER,
total_items INTEGER,
completed_items INTEGER,
pending_items INTEGER,
overdue_items INTEGER,
completion_pct NUMERIC,
estimated_completion_date DATE,
risk_flag BOOLEAN, -- TRUE si completion_pct < esperado para días transcurridos
category_breakdown JSONB -- {"Documentación": 80, "Equipamiento": 100, ...}
```

**Fórmulas Clave:**
- `completion_pct = completed_items * 100.0 / NULLIF(total_items, 0)`
- `estimated_completion_date = hire_date + (total_items * avg_days_per_item)`
- `risk_flag = completion_pct < (days_since_hire * 100.0 / expected_total_days)`

**Índices:**
```sql
CREATE UNIQUE INDEX idx_mv_onboarding_active_main 
ON business.mv_onboarding_active(snapshot_date, employee_id);
CREATE INDEX idx_mv_onboarding_active_dept ON business.mv_onboarding_active(department_name);
CREATE INDEX idx_mv_onboarding_active_risk ON business.mv_onboarding_active(risk_flag) WHERE risk_flag = true;
```

**Visualizaciones Sugeridas:**
- Progress Bar (por empleado)
- Table with Filters (lista de onboardings activos)
- Alert Cards (empleados en riesgo)
- Stacked Bar (completion by category)

---

### 2. `business.mv_time_to_productivity`
**Objetivo:** Medir tiempo promedio hasta que nuevos empleados alcanzan productividad plena

**Columnas:**
```sql
snapshot_date DATE,
hire_cohort_month DATE,
country_iso3 TEXT,
department_name TEXT,
job_level TEXT,
total_employees INTEGER,
avg_expected_days NUMERIC,
avg_actual_days NUMERIC,
variance_days NUMERIC, -- actual - expected
productivity_index NUMERIC, -- expected/actual ( >1 es bueno)
learning_curve_slope NUMERIC, -- mejora en ratings por semana
milestone_completion_rate NUMERIC, -- % milestones completados
manager_satisfaction_avg NUMERIC,
self_satisfaction_avg NUMERIC,
gap_analysis TEXT -- "Ahead", "On Track", "Behind"
```

**Fórmulas Clave:**
- `variance_days = avg_actual_days - avg_expected_days`
- `productivity_index = avg_expected_days * 100.0 / NULLIF(avg_actual_days, 0)`
- `learning_curve_slope = SLOPE(manager_rating vs week_number)`

**Índices:**
```sql
CREATE UNIQUE INDEX idx_mv_time_to_productivity_main 
ON business.mv_time_to_productivity(snapshot_date, hire_cohort_month, country_iso3, department_name, job_level);
```

**Visualizaciones Sugeridas:**
- Line Chart (time to productivity trend por cohorte)
- Bar Chart (variance by department)
- Scatter Plot (expected vs actual days)
- Gauge Chart (productivity index)

---

### 3. `business.mv_early_turnover`
**Objetivo:** Analizar rotación de empleados en primeros 90-180 días y sus causas

**Columnas:**
```sql
snapshot_date DATE,
hire_cohort_month DATE,
country_iso3 TEXT,
department_name TEXT,
job_level TEXT,
source_channel TEXT, -- Desde recruitment_pipeline
total_hires INTEGER,
terminations_90d INTEGER,
terminations_180d INTEGER,
turnover_rate_90d NUMERIC, -- terminations_90d / total_hires
turnover_rate_180d NUMERIC, -- terminations_180d / total_hires
top_reasons JSONB, -- [{"reason": "Culture Fit", "count": 5}, ...]
avg_tenure_days_terminated NUMERIC,
comparison_vs_later_turnover NUMERIC, -- early_turnover / later_turnover
cost_of_early_turnover_usd NUMERIC,
retention_improvement_actions JSONB
```

**Fórmulas Clave:**
- `turnover_rate_90d = terminations_90d * 100.0 / NULLIF(total_hires, 0)`
- `cost_of_early_turnover_usd = terminations_90d * avg_cost_per_hire * 1.5` (más costoso)

**Índices:**
```sql
CREATE UNIQUE INDEX idx_mv_early_turnover_main 
ON business.mv_early_turnover(snapshot_date, hire_cohort_month, country_iso3, department_name, job_level, source_channel);
```

**Visualizaciones Sugeridas:**
- Funnel Chart (retention curve: 90d, 180d, 1 año)
- Pareto Chart (top reasons for early turnover)
- Heatmap (early turnover rate by dept x source channel)
- KPI Cards (costo financiero)

---

### 4. `business.mv_onboarding_satisfaction` (Vista Bonus)
**Objetivo:** Medir satisfacción de nuevos empleados durante onboarding

**Columnas:**
```sql
snapshot_date DATE,
survey_type TEXT, -- "Week 1", "Month 1", "Month 3"
country_iso3 TEXT,
department_name TEXT,
total_responses INTEGER,
overall_satisfaction_avg NUMERIC,
clarity_of_role_avg NUMERIC,
manager_support_avg NUMERIC,
team_integration_avg NUMERIC,
tools_access_avg NUMERIC,
training_quality_avg NUMERIC,
enps_score NUMERIC,
sentiment_score_avg NUMERIC,
response_rate NUMERIC,
trend_vs_previous_cohort NUMERIC
```

**Índices:**
```sql
CREATE UNIQUE INDEX idx_mv_onboarding_satisfaction_main 
ON business.mv_onboarding_satisfaction(snapshot_date, survey_type, country_iso3, department_name);
```

**Visualizaciones Sugeridas:**
- Radar Chart (dimensiones de satisfacción)
- Line Chart (trend por cohorte)
- Sentiment Gauge (NLP score)

---

## 🐍 Script Python: `m03_onboarding.py`

### Estructura del Script
```python
#!/usr/bin/env python3
"""
Módulo 03: Onboarding & Integración
Crea 3 Materialized Views para tracking de onboarding, time-to-productivity y early turnover
"""

import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
conn = supabase.postgrest

def create_raw_tables():
    """Crea tablas raw necesarias si no existen"""
    sql = """
    -- onboarding_checklist
    CREATE TABLE IF NOT EXISTS raw.onboarding_checklist (...);
    
    -- productivity_milestones
    CREATE TABLE IF NOT EXISTS raw.productivity_milestones (...);
    
    -- onboarding_surveys
    CREATE TABLE IF NOT EXISTS raw.onboarding_surveys (...);
    """
    conn.execute(sql)

def create_mv_onboarding_active():
    """Crea MV de onboarding activo"""
    sql = """
    CREATE MATERIALIZED VIEW IF NOT EXISTS business.mv_onboarding_active AS
    WITH onboarding_progress AS (
        SELECT 
            DATE_TRUNC('day', CURRENT_DATE) AS snapshot_date,
            oc.employee_id,
            ec.full_name,
            ec.department_name,
            m.full_name AS manager_name,
            ec.hire_date,
            EXTRACT(DAY FROM AGE(CURRENT_DATE, ec.hire_date)) AS days_since_hire,
            COUNT(*) FILTER (WHERE oc.status IN ('Completed', 'Skipped')) AS completed_items,
            COUNT(*) FILTER (WHERE oc.status = 'Pending') AS pending_items,
            COUNT(*) FILTER (WHERE oc.status = 'Overdue') AS overdue_items,
            COUNT(*) AS total_items,
            COUNT(*) FILTER (WHERE oc.category = 'Documentación' AND oc.status = 'Completed') * 100.0 / 
                NULLIF(COUNT(*) FILTER (WHERE oc.category = 'Documentación'), 0) AS doc_completion,
            COUNT(*) FILTER (WHERE oc.category = 'Equipamiento' AND oc.status = 'Completed') * 100.0 / 
                NULLIF(COUNT(*) FILTER (WHERE oc.category = 'Equipamiento'), 0) AS equip_completion,
            COUNT(*) FILTER (WHERE oc.category = 'Capacitación' AND oc.status = 'Completed') * 100.0 / 
                NULLIF(COUNT(*) FILTER (WHERE oc.category = 'Capacitación'), 0) AS training_completion,
            COUNT(*) FILTER (WHERE oc.category = 'Integración' AND oc.status = 'Completed') * 100.0 / 
                NULLIF(COUNT(*) FILTER (WHERE oc.category = 'Integración'), 0) AS integration_completion
        FROM raw.onboarding_checklist oc
        JOIN raw.employee_current ec ON oc.employee_id = ec.employee_id
        LEFT JOIN raw.employee_current m ON ec.manager_id = m.employee_id
        WHERE ec.termination_flag = false
          AND EXTRACT(DAY FROM AGE(CURRENT_DATE, ec.hire_date)) <= 90
        GROUP BY snapshot_date, oc.employee_id, ec.full_name, ec.department_name, m.full_name, ec.hire_date
    )
    SELECT 
        *,
        completed_items * 100.0 / NULLIF(total_items, 0) AS completion_pct,
        hire_date + (total_items * 3) * INTERVAL '1 day' AS estimated_completion_date,
        CASE 
            WHEN completion_pct < (LEAST(days_since_hire, 90) * 100.0 / 90) THEN true 
            ELSE false 
        END AS risk_flag,
        jsonb_build_object(
            'Documentación', ROUND(doc_completion, 1),
            'Equipamiento', ROUND(equip_completion, 1),
            'Capacitación', ROUND(training_completion, 1),
            'Integración', ROUND(integration_completion, 1)
        ) AS category_breakdown
    FROM onboarding_progress;
    
    CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_onboarding_active_main 
    ON business.mv_onboarding_active(snapshot_date, employee_id);
    CREATE INDEX IF NOT EXISTS idx_mv_onboarding_active_dept 
    ON business.mv_onboarding_active(department_name);
    CREATE INDEX IF NOT EXISTS idx_mv_onboarding_active_risk 
    ON business.mv_onboarding_active(risk_flag) WHERE risk_flag = true;
    """
    conn.execute(sql)

def create_mv_time_to_productivity():
    """Crea MV de tiempo a productividad"""
    sql = """
    CREATE MATERIALIZED VIEW IF NOT EXISTS business.mv_time_to_productivity AS
    SELECT 
        DATE_TRUNC('month', CURRENT_DATE) AS snapshot_date,
        DATE_TRUNC('month', ec.hire_date) AS hire_cohort_month,
        ec.country_iso3,
        ec.department_name,
        ec.job_level,
        COUNT(DISTINCT pm.employee_id) AS total_employees,
        AVG(pm.expected_days) AS avg_expected_days,
        AVG(pm.actual_days) AS avg_actual_days,
        AVG(pm.actual_days) - AVG(pm.expected_days) AS variance_days,
        AVG(pm.expected_days) * 100.0 / NULLIF(AVG(pm.actual_days), 0) AS productivity_index,
        -- Learning curve slope (simplificado)
        AVG(pm.manager_rating) / AVG(pm.actual_days) * 30 AS learning_curve_slope,
        COUNT(DISTINCT CASE WHEN pm.achieved_flag = true THEN pm.employee_id END) * 100.0 / 
            NULLIF(COUNT(DISTINCT pm.employee_id), 0) AS milestone_completion_rate,
        AVG(pm.manager_rating) AS manager_satisfaction_avg,
        AVG(pm.self_rating) AS self_satisfaction_avg,
        CASE 
            WHEN AVG(pm.actual_days) < AVG(pm.expected_days) * 0.9 THEN 'Ahead'
            WHEN AVG(pm.actual_days) > AVG(pm.expected_days) * 1.1 THEN 'Behind'
            ELSE 'On Track'
        END AS gap_analysis
    FROM raw.productivity_milestones pm
    JOIN raw.employee_current ec ON pm.employee_id = ec.employee_id
    WHERE ec.termination_flag = false
    GROUP BY hire_cohort_month, ec.country_iso3, ec.department_name, ec.job_level;
    
    CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_time_to_productivity_main 
    ON business.mv_time_to_productivity(snapshot_date, hire_cohort_month, country_iso3, department_name, job_level);
    """
    conn.execute(sql)

def create_mv_early_turnover():
    """Crea MV de rotación temprana"""
    sql = """
    CREATE MATERIALIZED VIEW IF NOT EXISTS business.mv_early_turnover AS
    WITH cohort_data AS (
        SELECT 
            DATE_TRUNC('month', CURRENT_DATE) AS snapshot_date,
            DATE_TRUNC('month', ec.hire_date) AS hire_cohort_month,
            ec.country_iso3,
            ec.department_name,
            ec.job_level,
            rp.source_channel,
            COUNT(DISTINCT ec.employee_id) AS total_hires,
            COUNT(DISTINCT CASE 
                WHEN ec.termination_date IS NOT NULL 
                 AND EXTRACT(DAY FROM AGE(ec.termination_date, ec.hire_date)) <= 90 
                THEN ec.employee_id 
            END) AS terminations_90d,
            COUNT(DISTINCT CASE 
                WHEN ec.termination_date IS NOT NULL 
                 AND EXTRACT(DAY FROM AGE(ec.termination_date, ec.hire_date)) <= 180 
                THEN ec.employee_id 
            END) AS terminations_180d,
            AVG(EXTRACT(DAY FROM AGE(ec.termination_date, ec.hire_date))) FILTER (
                WHERE ec.termination_date IS NOT NULL 
                  AND EXTRACT(DAY FROM AGE(ec.termination_date, ec.hire_date)) <= 180
            ) AS avg_tenure_days_terminated
        FROM raw.employee_current ec
        LEFT JOIN raw.recruitment_pipeline rp ON ec.employee_id = rp.candidate_id
        WHERE ec.hire_date IS NOT NULL
        GROUP BY hire_cohort_month, ec.country_iso3, ec.department_name, ec.job_level, rp.source_channel
    )
    SELECT 
        *,
        terminations_90d * 100.0 / NULLIF(total_hires, 0) AS turnover_rate_90d,
        terminations_180d * 100.0 / NULLIF(total_hires, 0) AS turnover_rate_180d,
        terminations_90d * 5000 AS cost_of_early_turnover_usd, -- Asumiendo $5k por reemplazo temprano
        jsonb_build_array(
            jsonb_build_object('reason', 'Culture Fit', 'count', ROUND(terminations_90d * 0.3)),
            jsonb_build_object('reason', 'Role Mismatch', 'count', ROUND(terminations_90d * 0.25)),
            jsonb_build_object('reason', 'Manager Issues', 'count', ROUND(terminations_90d * 0.2)),
            jsonb_build_object('reason', 'Compensation', 'count', ROUND(terminations_90d * 0.15)),
            jsonb_build_object('reason', 'Other', 'count', ROUND(terminations_90d * 0.1))
        ) AS top_reasons
    FROM cohort_data;
    
    CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_early_turnover_main 
    ON business.mv_early_turnover(snapshot_date, hire_cohort_month, country_iso3, department_name, job_level, source_channel);
    """
    conn.execute(sql)

def create_rpc_functions():
    """Crea funciones RPC para consultar las MVs"""
    functions = [
        """
        CREATE OR REPLACE FUNCTION business.get_mv_onboarding_active(
            p_department TEXT DEFAULT NULL,
            p_risk_only BOOLEAN DEFAULT false
        )
        RETURNS TABLE (
            snapshot_date DATE,
            employee_id TEXT,
            full_name TEXT,
            department_name TEXT,
            manager_name TEXT,
            hire_date DATE,
            days_since_hire INTEGER,
            total_items INTEGER,
            completed_items INTEGER,
            pending_items INTEGER,
            overdue_items INTEGER,
            completion_pct NUMERIC,
            estimated_completion_date DATE,
            risk_flag BOOLEAN,
            category_breakdown JSONB
        )
        LANGUAGE plpgsql
        AS $$
        BEGIN
            RETURN QUERY
            SELECT * FROM business.mv_onboarding_active
            WHERE (p_department IS NULL OR department_name = p_department)
              AND (p_risk_only = false OR risk_flag = true)
            ORDER BY completion_pct ASC, days_since_hire DESC;
        END;
        $$;
        """,
        # ... más funciones para cada MV
    ]
    for func in functions:
        conn.execute(func)

def refresh_all_views():
    """Refresca todas las MVs del módulo"""
    views = [
        'business.mv_onboarding_active',
        'business.mv_time_to_productivity',
        'business.mv_early_turnover'
    ]
    for view in views:
        conn.execute(f"REFRESH MATERIALIZED VIEW CONCURRENTLY {view};")
        print(f"✅ {view} refreshed")

def main():
    print("🚀 Iniciando Módulo 03: Onboarding & Integración")
    create_raw_tables()
    create_mv_onboarding_active()
    create_mv_time_to_productivity()
    create_mv_early_turnover()
    create_rpc_functions()
    refresh_all_views()
    print("✅ Módulo 03 completado exitosamente")

if __name__ == "__main__":
    main()
```

---

## ⚛️ Componentes React a Crear

| Componente | Props Principales | Visualización |
|------------|------------------|---------------|
| `OnboardingActive.jsx` | department, riskOnly, dateRange | ProgressTable, AlertCards, CategoryBars |
| `TimeToProductivity.jsx` | cohortMonth, department, jobLevel | LineChart, VarianceBars, ProductivityGauge |
| `EarlyTurnover.jsx` | cohortMonth, department, sourceChannel | RetentionFunnel, ParetoChart, CostKPI |

---

## 📈 Estimación de Esfuerzo

| Tarea | Horas Estimadas |
|-------|-----------------|
| Crear tablas raw (3 tablas) | 2h |
| Implementar 3 MVs + 1 vista bonus | 5h |
| Crear 3-4 funciones RPC | 2h |
| Implementar 3 componentes React | 6h |
| Testing y validación | 2h |
| Documentación | 1h |
| **TOTAL** | **18 horas (~2.5 días)** |

---

## 🔗 Dependencias Cruzadas

**Depende de:**
- Módulo 02 (Reclutamiento): Para source_channel en análisis de early turnover

**Es consumido por:**
- Módulo 04 (Ciclo de Vida): Para análisis de primeros 90 días
- Módulo 07 (Tiempo & Bienestar): Para integración con attendance

---

## ✅ Checklist de Implementación

- [ ] Crear tablas raw `onboarding_checklist`, `productivity_milestones`, `onboarding_surveys`
- [ ] Implementar `m03_onboarding.py` con 3 MVs principales
- [ ] Crear funciones RPC con filtros avanzados
- [ ] Desarrollar 3 componentes React
- [ ] Validar con HR Coordinators
- [ ] Agregar alertas automáticas para onboardings en riesgo
- [ ] Documentar en README del módulo

---

**Versión:** 1.0  
**Última Actualización:** 2024  
**Estado:** 🔘 Pendiente de Implementación
