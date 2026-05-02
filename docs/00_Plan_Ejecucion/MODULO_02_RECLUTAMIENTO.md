# 📋 Módulo 02: Reclutamiento & Selección - Plan de Ejecución Detallado

## 🎯 Objetivo del Módulo
Analizar la eficiencia del proceso de reclutamiento, calidad de contrataciones, y detectar posibles sesgos en la selección de candidatos para optimizar el hiring pipeline.

**Usuarios Objetivo:**
- Recruiting Managers
- HR Business Partners
- Talent Acquisition Team
- Diversity & Inclusion Officers

---

## 📊 Fuentes de Datos

### Tablas Existentes (raw)
- `raw.employee_current` - Para analizar hires convertidos
- `raw.departments` - Para segmentación por departamento

### Nuevas Tablas Raw a Crear
```sql
-- Tabla de ofertas de trabajo publicadas
CREATE TABLE IF NOT EXISTS raw.job_postings (
    posting_id TEXT PRIMARY KEY,
    job_title TEXT NOT NULL,
    department_name TEXT,
    country_iso3 TEXT,
    salary_range_min NUMERIC,
    salary_range_max NUMERIC,
    experience_level TEXT, -- Junior, Mid, Senior, Lead
    employment_type TEXT, -- Full-time, Part-time, Contract
    posted_date DATE,
    closed_date DATE,
    status TEXT, -- Open, Closed, On Hold
    required_skills JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de candidatos en el pipeline
CREATE TABLE IF NOT EXISTS raw.recruitment_pipeline (
    candidate_id TEXT PRIMARY KEY,
    posting_id TEXT REFERENCES raw.job_postings(posting_id),
    full_name TEXT,
    gender TEXT,
    age INTEGER,
    education_level TEXT,
    years_experience INTEGER,
    current_stage TEXT, -- Applied, Screened, Interviewed, Offer, Hired, Rejected
    application_date DATE,
    screen_date DATE,
    interview_date DATE,
    offer_date DATE,
    hire_date DATE,
    rejection_date DATE,
    rejection_reason TEXT,
    interview_score NUMERIC, -- 1-5 escala
    technical_score NUMERIC, -- 1-100
    cultural_fit_score NUMERIC, -- 1-5
    nps_score INTEGER, -- -100 a 100 (si fue contratado y encuestado)
    source_channel TEXT, -- LinkedIn, Referral, Career Site, Agency
    recruiter_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🎨 Vistas/Materialized Views a Implementar

### 1. `business.mv_recruitment_efficiency`
**Objetivo:** Medir eficiencia del funnel de reclutamiento

**Columnas:**
```sql
snapshot_date DATE,
country_iso3 TEXT,
department_name TEXT,
job_level TEXT,
total_applicants INTEGER,
total_screened INTEGER,
total_interviewed INTEGER,
total_offers INTEGER,
total_hires INTEGER,
conversion_rate_application_to_screen NUMERIC, -- screened/applicants
conversion_rate_screen_to_interview NUMERIC, -- interviewed/screened
conversion_rate_interview_to_offer NUMERIC, -- offers/interviewed
conversion_rate_offer_to_hire NUMERIC, -- hires/offers
overall_conversion_rate NUMERIC, -- hires/applicants
avg_time_to_hire_days NUMERIC,
avg_time_to_fill_days NUMERIC,
cost_per_hire_usd NUMERIC
```

**Fórmulas Clave:**
- `conversion_rate_application_to_screen = total_screened * 100.0 / NULLIF(total_applicants, 0)`
- `avg_time_to_hire_days = AVG(hire_date - application_date)`
- `cost_per_hire_usd = (SUM(recruiter_costs + agency_fees + advertising_costs)) / total_hires`

**Índices:**
```sql
CREATE UNIQUE INDEX idx_mv_recruitment_efficiency_main 
ON business.mv_recruitment_efficiency(snapshot_date, country_iso3, department_name, job_level);
```

**Visualizaciones Sugeridas:**
- Funnel Chart (conversión por etapa)
- Line Chart (time to hire trend)
- Bar Chart (cost per hire by department)

---

### 2. `business.mv_hiring_quality`
**Objetivo:** Evaluar calidad de las contrataciones post-hire

**Columnas:**
```sql
snapshot_date DATE,
hire_cohort_month DATE, -- Mes de contratación
country_iso3 TEXT,
department_name TEXT,
job_level TEXT,
source_channel TEXT,
total_hires INTEGER,
performance_rating_6m NUMERIC, -- Avg rating a los 6 meses
performance_rating_12m NUMERIC, -- Avg rating a los 12 meses
retention_rate_6m NUMERIC, -- % aún empleados a los 6 meses
retention_rate_12m NUMERIC, -- % aún empleados a los 12 meses
retention_rate_24m NUMERIC, -- % aún empleados a los 24 meses
quality_of_hire_score NUMERIC, -- Composite score
early_turnover_rate_90d NUMERIC, -- % que se van en primeros 90 días
promotion_rate_12m NUMERIC -- % promovidos en primer año
```

**Fórmulas Clave:**
- `quality_of_hire_score = (performance_rating_6m * 0.4 + retention_rate_12m * 0.4 + promotion_rate_12m * 0.2) * 100`
- `early_turnover_rate_90d = COUNT(CASE WHEN termination_date - hire_date <= 90 THEN 1 END) * 100.0 / total_hires`

**Índices:**
```sql
CREATE UNIQUE INDEX idx_mv_hiring_quality_main 
ON business.mv_hiring_quality(snapshot_date, hire_cohort_month, country_iso3, department_name, job_level, source_channel);
```

**Visualizaciones Sugeridas:**
- Heatmap (quality of hire by source channel)
- Line Chart (retention curves por cohorte)
- Scatter Plot (performance vs tenure)

---

### 3. `business.mv_fit_score_distribution`
**Objetivo:** Analizar distribución de scores de fit cultural y técnico

**Columnas:**
```sql
snapshot_date DATE,
country_iso3 TEXT,
department_name TEXT,
fit_score_bucket TEXT, -- "0-1", "1-2", "2-3", "3-4", "4-5"
candidate_count INTEGER,
hired_count INTEGER,
conversion_rate NUMERIC,
avg_performance_rating_hired NUMERIC,
avg_tenure_months_hired NUMERIC
```

**Fórmulas Clave:**
- `fit_score_bucket = CASE WHEN cultural_fit_score BETWEEN 0 AND 1 THEN '0-1' ... END`
- `conversion_rate = hired_count * 100.0 / NULLIF(candidate_count, 0)`

**Índices:**
```sql
CREATE UNIQUE INDEX idx_mv_fit_score_distribution_main 
ON business.mv_fit_score_distribution(snapshot_date, country_iso3, department_name, fit_score_bucket);
```

**Visualizaciones Sugeridas:**
- Histogram (distribución de fit scores)
- Stacked Bar (hired vs not hired por score bucket)

---

### 4. `business.mv_bias_audit`
**Objetivo:** Detectar posibles sesgos en el proceso de selección (género, edad, etc.)

**Columnas:**
```sql
snapshot_date DATE,
country_iso3 TEXT,
department_name TEXT,
stage_name TEXT, -- Screened, Interviewed, Offered, Hired
gender TEXT,
age_group TEXT, -- "<30", "30-40", "40-50", "50+"
ethnicity TEXT, -- Si disponible
total_candidates INTEGER,
passed_count INTEGER,
pass_rate NUMERIC,
disparity_index NUMERIC, -- pass_rate / avg_pass_rate_all_groups
flag_bias BOOLEAN, -- TRUE si disparity_index < 0.8 o > 1.2
statistical_significance NUMERIC -- p-value del test
```

**Fórmulas Clave:**
- `disparity_index = pass_rate / (SELECT AVG(pass_rate) OVER (PARTITION BY stage_name))`
- `flag_bias = disparity_index < 0.8 OR disparity_index > 1.2`

**Índices:**
```sql
CREATE UNIQUE INDEX idx_mv_bias_audit_main 
ON business.mv_bias_audit(snapshot_date, country_iso3, department_name, stage_name, gender, age_group);
```

**Visualizaciones Sugeridas:**
- Bar Chart (pass rates by demographic group)
- Alert Table (biased stages highlighted)
- Trend Line (bias metrics over time)

---

### 5. `business.mv_candidate_nps`
**Objetivo:** Medir experiencia del candidato mediante Net Promoter Score

**Columnas:**
```sql
snapshot_date DATE,
country_iso3 TEXT,
department_name TEXT,
source_channel TEXT,
recruiter_id TEXT,
total_respondents INTEGER,
promoters_count INTEGER, -- NPS 9-10
passives_count INTEGER, -- NPS 7-8
detractors_count INTEGER, -- NPS 0-6
nps_score INTEGER, -- (promoters - detractors) * 100 / total
avg_nps_score NUMERIC,
response_rate NUMERIC, -- respondents / total_hires
top_positive_themes JSONB,
top_negative_themes JSONB
```

**Fórmulas Clave:**
- `nps_score = (promoters_count - detractors_count) * 100 / NULLIF(total_respondents, 0)`
- `response_rate = total_respondents * 100.0 / NULLIF(total_hires, 0)`

**Índices:**
```sql
CREATE UNIQUE INDEX idx_mv_candidate_nps_main 
ON business.mv_candidate_nps(snapshot_date, country_iso3, department_name, source_channel, recruiter_id);
```

**Visualizaciones Sugeridas:**
- Gauge Chart (NPS score)
- Stacked Bar (promoters/passives/detractors)
- Word Cloud (temas de feedback)

---

## 🐍 Script Python: `m02_reclutamiento.py`

### Estructura del Script
```python
#!/usr/bin/env python3
"""
Módulo 02: Reclutamiento & Selección
Crea 5 Materialized Views para análisis de eficiencia, calidad y equidad en hiring
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
    # SQL para job_postings y recruitment_pipeline
    pass

def create_mv_recruitment_efficiency():
    """Crea MV de eficiencia de reclutamiento"""
    sql = """
    CREATE MATERIALIZED VIEW IF NOT EXISTS business.mv_recruitment_efficiency AS
    WITH recruitment_metrics AS (
        SELECT 
            DATE_TRUNC('month', CURRENT_DATE) AS snapshot_date,
            rp.country_iso3,
            rp.department_name,
            ec.job_level,
            COUNT(DISTINCT rp.candidate_id) AS total_applicants,
            COUNT(DISTINCT CASE WHEN rp.current_stage IN ('Screened', 'Interviewed', 'Offer', 'Hired') THEN rp.candidate_id END) AS total_screened,
            COUNT(DISTINCT CASE WHEN rp.current_stage IN ('Interviewed', 'Offer', 'Hired') THEN rp.candidate_id END) AS total_interviewed,
            COUNT(DISTINCT CASE WHEN rp.current_stage IN ('Offer', 'Hired') THEN rp.candidate_id END) AS total_offers,
            COUNT(DISTINCT CASE WHEN rp.current_stage = 'Hired' THEN rp.candidate_id END) AS total_hires,
            AVG(EXTRACT(DAY FROM (rp.hire_date - rp.application_date))) FILTER (WHERE rp.hire_date IS NOT NULL) AS avg_time_to_hire_days,
            AVG(EXTRACT(DAY FROM (jp.closed_date - jp.posted_date))) FILTER (WHERE jp.closed_date IS NOT NULL) AS avg_time_to_fill_days
        FROM raw.recruitment_pipeline rp
        JOIN raw.job_postings jp ON rp.posting_id = jp.posting_id
        LEFT JOIN raw.employee_current ec ON rp.candidate_id = ec.employee_id
        GROUP BY rp.country_iso3, rp.department_name, ec.job_level
    )
    SELECT 
        *,
        total_screened * 100.0 / NULLIF(total_applicants, 0) AS conversion_rate_application_to_screen,
        total_interviewed * 100.0 / NULLIF(total_screened, 0) AS conversion_rate_screen_to_interview,
        total_offers * 100.0 / NULLIF(total_interviewed, 0) AS conversion_rate_interview_to_offer,
        total_hires * 100.0 / NULLIF(total_offers, 0) AS conversion_rate_offer_to_hire,
        total_hires * 100.0 / NULLIF(total_applicants, 0) AS overall_conversion_rate
    FROM recruitment_metrics;
    
    CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_recruitment_efficiency_main 
    ON business.mv_recruitment_efficiency(snapshot_date, country_iso3, department_name, job_level);
    """
    conn.execute(sql)

def create_mv_hiring_quality():
    """Crea MV de calidad de contrataciones"""
    sql = """
    CREATE MATERIALIZED VIEW IF NOT EXISTS business.mv_hiring_quality AS
    SELECT 
        DATE_TRUNC('month', CURRENT_DATE) AS snapshot_date,
        DATE_TRUNC('month', ec.hire_date) AS hire_cohort_month,
        ec.country_iso3,
        ec.department_name,
        ec.job_level,
        rp.source_channel,
        COUNT(DISTINCT ec.employee_id) AS total_hires,
        AVG(pr.overall_rating) FILTER (WHERE EXTRACT(MONTH FROM AGE(CURRENT_DATE, ec.hire_date)) >= 6) AS performance_rating_6m,
        AVG(pr.overall_rating) FILTER (WHERE EXTRACT(MONTH FROM AGE(CURRENT_DATE, ec.hire_date)) >= 12) AS performance_rating_12m,
        COUNT(DISTINCT CASE WHEN ec.termination_flag = false AND EXTRACT(MONTH FROM AGE(CURRENT_DATE, ec.hire_date)) >= 6 THEN ec.employee_id END) * 100.0 / 
            NULLIF(COUNT(DISTINCT ec.employee_id) FILTER (WHERE EXTRACT(MONTH FROM AGE(CURRENT_DATE, ec.hire_date)) >= 6), 0) AS retention_rate_6m,
        COUNT(DISTINCT CASE WHEN ec.termination_flag = false AND EXTRACT(MONTH FROM AGE(CURRENT_DATE, ec.hire_date)) >= 12 THEN ec.employee_id END) * 100.0 / 
            NULLIF(COUNT(DISTINCT ec.employee_id) FILTER (WHERE EXTRACT(MONTH FROM AGE(CURRENT_DATE, ec.hire_date)) >= 12), 0) AS retention_rate_12m,
        COUNT(DISTINCT CASE WHEN ec.termination_flag = false AND EXTRACT(MONTH FROM AGE(CURRENT_DATE, ec.hire_date)) >= 24 THEN ec.employee_id END) * 100.0 / 
            NULLIF(COUNT(DISTINCT ec.employee_id) FILTER (WHERE EXTRACT(MONTH FROM AGE(CURRENT_DATE, ec.hire_date)) >= 24), 0) AS retention_rate_24m,
        COUNT(DISTINCT CASE WHEN ec.termination_date IS NOT NULL AND EXTRACT(DAY FROM AGE(ec.termination_date, ec.hire_date)) <= 90 THEN ec.employee_id END) * 100.0 / 
            NULLIF(COUNT(DISTINCT ec.employee_id), 0) AS early_turnover_rate_90d,
        COUNT(DISTINCT CASE WHEN pm.promotion_flag = true AND EXTRACT(MONTH FROM AGE(pm.promotion_date, ec.hire_date)) <= 12 THEN ec.employee_id END) * 100.0 / 
            NULLIF(COUNT(DISTINCT ec.employee_id), 0) AS promotion_rate_12m
    FROM raw.employee_current ec
    JOIN raw.recruitment_pipeline rp ON ec.employee_id = rp.candidate_id
    LEFT JOIN raw.performance_reviews pr ON ec.employee_id = pr.employee_id
    LEFT JOIN raw.promotions pm ON ec.employee_id = pm.employee_id
    WHERE ec.hire_date IS NOT NULL
    GROUP BY hire_cohort_month, ec.country_iso3, ec.department_name, ec.job_level, rp.source_channel;
    
    CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_hiring_quality_main 
    ON business.mv_hiring_quality(snapshot_date, hire_cohort_month, country_iso3, department_name, job_level, source_channel);
    """
    conn.execute(sql)

def create_mv_fit_score_distribution():
    """Crea MV de distribución de fit scores"""
    sql = """
    CREATE MATERIALIZED VIEW IF NOT EXISTS business.mv_fit_score_distribution AS
    SELECT 
        DATE_TRUNC('month', CURRENT_DATE) AS snapshot_date,
        jp.country_iso3,
        jp.department_name,
        CASE 
            WHEN rp.cultural_fit_score BETWEEN 0 AND 1 THEN '0-1'
            WHEN rp.cultural_fit_score BETWEEN 1 AND 2 THEN '1-2'
            WHEN rp.cultural_fit_score BETWEEN 2 AND 3 THEN '2-3'
            WHEN rp.cultural_fit_score BETWEEN 3 AND 4 THEN '3-4'
            WHEN rp.cultural_fit_score BETWEEN 4 AND 5 THEN '4-5'
            ELSE 'N/A'
        END AS fit_score_bucket,
        COUNT(DISTINCT rp.candidate_id) AS candidate_count,
        COUNT(DISTINCT CASE WHEN rp.current_stage = 'Hired' THEN rp.candidate_id END) AS hired_count,
        COUNT(DISTINCT CASE WHEN rp.current_stage = 'Hired' THEN rp.candidate_id END) * 100.0 / 
            NULLIF(COUNT(DISTINCT rp.candidate_id), 0) AS conversion_rate,
        AVG(pr.overall_rating) FILTER (WHERE rp.current_stage = 'Hired') AS avg_performance_rating_hired,
        AVG(EXTRACT(MONTH FROM AGE(CURRENT_DATE, ec.hire_date))) FILTER (WHERE rp.current_stage = 'Hired') AS avg_tenure_months_hired
    FROM raw.recruitment_pipeline rp
    JOIN raw.job_postings jp ON rp.posting_id = jp.posting_id
    LEFT JOIN raw.employee_current ec ON rp.candidate_id = ec.employee_id
    LEFT JOIN raw.performance_reviews pr ON rp.candidate_id = pr.employee_id
    GROUP BY snapshot_date, jp.country_iso3, jp.department_name, fit_score_bucket;
    
    CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_fit_score_distribution_main 
    ON business.mv_fit_score_distribution(snapshot_date, country_iso3, department_name, fit_score_bucket);
    """
    conn.execute(sql)

def create_mv_bias_audit():
    """Crea MV de auditoría de sesgos"""
    sql = """
    CREATE MATERIALIZED VIEW IF NOT EXISTS business.mv_bias_audit AS
    WITH stage_pass_rates AS (
        SELECT 
            DATE_TRUNC('month', CURRENT_DATE) AS snapshot_date,
            jp.country_iso3,
            jp.department_name,
            'Screened' AS stage_name,
            rp.gender,
            CASE 
                WHEN rp.age < 30 THEN '<30'
                WHEN rp.age BETWEEN 30 AND 40 THEN '30-40'
                WHEN rp.age BETWEEN 40 AND 50 THEN '40-50'
                ELSE '50+'
            END AS age_group,
            COUNT(DISTINCT rp.candidate_id) AS total_candidates,
            COUNT(DISTINCT CASE WHEN rp.current_stage IN ('Screened', 'Interviewed', 'Offer', 'Hired') THEN rp.candidate_id END) AS passed_count
        FROM raw.recruitment_pipeline rp
        JOIN raw.job_postings jp ON rp.posting_id = jp.posting_id
        GROUP BY snapshot_date, jp.country_iso3, jp.department_name, rp.gender, age_group
    ),
    with_avg AS (
        SELECT 
            *,
            passed_count * 100.0 / NULLIF(total_candidates, 0) AS pass_rate,
            AVG(passed_count * 100.0 / NULLIF(total_candidates, 0)) OVER (PARTITION BY snapshot_date, country_iso3, department_name, stage_name) AS avg_pass_rate
        FROM stage_pass_rates
    )
    SELECT 
        *,
        pass_rate / NULLIF(avg_pass_rate, 0) AS disparity_index,
        CASE WHEN pass_rate / NULLIF(avg_pass_rate, 0) < 0.8 OR pass_rate / NULLIF(avg_pass_rate, 0) > 1.2 THEN true ELSE false END AS flag_bias
    FROM with_avg;
    
    CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_bias_audit_main 
    ON business.mv_bias_audit(snapshot_date, country_iso3, department_name, stage_name, gender, age_group);
    """
    conn.execute(sql)

def create_mv_candidate_nps():
    """Crea MV de NPS de candidatos"""
    sql = """
    CREATE MATERIALIZED VIEW IF NOT EXISTS business.mv_candidate_nps AS
    SELECT 
        DATE_TRUNC('month', CURRENT_DATE) AS snapshot_date,
        jp.country_iso3,
        jp.department_name,
        rp.source_channel,
        rp.recruiter_id,
        COUNT(DISTINCT rp.candidate_id) FILTER (WHERE rp.nps_score IS NOT NULL) AS total_respondents,
        COUNT(DISTINCT rp.candidate_id) FILTER (WHERE rp.nps_score >= 9) AS promoters_count,
        COUNT(DISTINCT rp.candidate_id) FILTER (WHERE rp.nps_score BETWEEN 7 AND 8) AS passives_count,
        COUNT(DISTINCT rp.candidate_id) FILTER (WHERE rp.nps_score <= 6) AS detractors_count,
        (COUNT(DISTINCT rp.candidate_id) FILTER (WHERE rp.nps_score >= 9) - 
         COUNT(DISTINCT rp.candidate_id) FILTER (WHERE rp.nps_score <= 6)) * 100 / 
         NULLIF(COUNT(DISTINCT rp.candidate_id) FILTER (WHERE rp.nps_score IS NOT NULL), 0) AS nps_score,
        AVG(rp.nps_score) FILTER (WHERE rp.nps_score IS NOT NULL) AS avg_nps_score,
        COUNT(DISTINCT rp.candidate_id) FILTER (WHERE rp.nps_score IS NOT NULL) * 100.0 / 
            NULLIF(COUNT(DISTINCT rp.candidate_id) FILTER (WHERE rp.current_stage = 'Hired'), 0) AS response_rate
    FROM raw.recruitment_pipeline rp
    JOIN raw.job_postings jp ON rp.posting_id = jp.posting_id
    GROUP BY snapshot_date, jp.country_iso3, jp.department_name, rp.source_channel, rp.recruiter_id;
    
    CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_candidate_nps_main 
    ON business.mv_candidate_nps(snapshot_date, country_iso3, department_name, source_channel, recruiter_id);
    """
    conn.execute(sql)

def create_rpc_functions():
    """Crea funciones RPC para consultar las MVs"""
    functions = [
        """
        CREATE OR REPLACE FUNCTION business.get_mv_recruitment_efficiency(
            p_department TEXT DEFAULT NULL,
            p_country TEXT DEFAULT NULL
        )
        RETURNS TABLE (...)
        LANGUAGE plpgsql
        AS $$
        BEGIN
            RETURN QUERY
            SELECT * FROM business.mv_recruitment_efficiency
            WHERE (p_department IS NULL OR department_name = p_department)
              AND (p_country IS NULL OR country_iso3 = p_country)
            ORDER BY snapshot_date DESC;
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
        'business.mv_recruitment_efficiency',
        'business.mv_hiring_quality',
        'business.mv_fit_score_distribution',
        'business.mv_bias_audit',
        'business.mv_candidate_nps'
    ]
    for view in views:
        conn.execute(f"REFRESH MATERIALIZED VIEW CONCURRENTLY {view};")
        print(f"✅ {view} refreshed")

def main():
    print("🚀 Iniciando Módulo 02: Reclutamiento & Selección")
    create_raw_tables()
    create_mv_recruitment_efficiency()
    create_mv_hiring_quality()
    create_mv_fit_score_distribution()
    create_mv_bias_audit()
    create_mv_candidate_nps()
    create_rpc_functions()
    refresh_all_views()
    print("✅ Módulo 02 completado exitosamente")

if __name__ == "__main__":
    main()
```

---

## ⚛️ Componentes React a Crear

| Componente | Props Principales | Visualización |
|------------|------------------|---------------|
| `RecruitmentEfficiency.jsx` | department, country, dateRange | FunnelChart, LineChart, KPI cards |
| `HiringQuality.jsx` | cohortMonth, department, sourceChannel | Heatmap, RetentionCurve, ScatterPlot |
| `FitScoreDistribution.jsx` | department, jobLevel | Histogram, StackedBar |
| `BiasAudit.jsx` | department, stageName, demographic | BarChart, AlertTable, TrendLine |
| `CandidateNPS.jsx` | department, recruiterId, dateRange | GaugeChart, StackedBar, WordCloud |

---

## 📈 Estimación de Esfuerzo

| Tarea | Horas Estimadas |
|-------|-----------------|
| Crear tablas raw (job_postings, recruitment_pipeline) | 2h |
| Implementar 5 MVs con SQL complejo | 6h |
| Crear 5 funciones RPC | 2h |
| Implementar 5 componentes React | 8h |
| Testing y validación de datos | 3h |
| Documentación y ajustes | 2h |
| **TOTAL** | **23 horas (~3 días)** |

---

## 🔗 Dependencias Cruzadas

**Depende de:**
- Ninguno (es un módulo fuente)

**Es consumido por:**
- Módulo 04 (Ciclo de Vida): Para análisis de quality of hire
- Módulo 09 (Talento): Para internal mobility desde source channel

---

## ✅ Checklist de Implementación

- [ ] Crear tablas raw `job_postings` y `recruitment_pipeline`
- [ ] Implementar `m02_reclutamiento.py` con 5 MVs
- [ ] Crear 5 funciones RPC
- [ ] Desarrollar 5 componentes React
- [ ] Validar datos con equipo de Recruiting
- [ ] Agregar tests de regresión
- [ ] Documentar en README del módulo

---

**Versión:** 1.0  
**Última Actualización:** 2024  
**Estado:** 🔘 Pendiente de Implementación
