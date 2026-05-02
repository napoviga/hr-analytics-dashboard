# 📋 Plan Maestro de Conversión de Datos - GDH Analytics

> **Fecha de creación:** 2026-04-11  
> **Propósito:** Documentar el estado actual de conversión de datos y definir la ruta crítica para completar los 13 módulos del dashboard  
> **Estado del proyecto:** 🟡 En desarrollo activo (Módulos 05 y 06 parcialmente implementados)

---

## 🎯 Resumen Ejecutivo

### Estado Actual de Implementación

| Módulo | Nombre | Vistas Totales | Implementadas | Pendientes | % Completitud |
|--------|--------|----------------|---------------|------------|---------------|
| 01 | Visión Ejecutiva | 3 | 1 | 2 | 33% |
| 02 | Reclutamiento & Selección | 5 | 0 | 5 | 0% |
| 03 | Onboarding & Integración | 3 | 0 | 3 | 0% |
| 04 | Análisis de Ciclo de Vida | 3 | 0 | 3 | 0% |
| 05 | Fuerza Laboral & Estructura | 6 | 6 | 0 | ✅ 100% |
| 06 | Nómina, Costos & Equity | 6 | 1 | 5 | 17% |
| 07 | Tiempo, Asistencia & Bienestar | 6 | 0 | 6 | 0% |
| 08 | Gestión del Desempeño | 4 | 0 | 4 | 0% |
| 09 | Talento & Desarrollo | 5 | 0 | 5 | 0% |
| 10 | Engagement & Sentimiento | 3 | 0 | 3 | 0% |
| 11 | Compliance & Relaciones Laborales | 2 | 0 | 2 | 0% |
| 12 | Retención & Riesgo de Fuga | 3 | 0 | 3 | 0% |
| 13 | Calidad de Datos | 3 | 1 | 2 | 33% |
| **TOTAL** | **13 Módulos** | **52** | **9** | **43** | **17%** |

---

## 📊 Arquitectura de Datos Actual

### Capas Implementadas

```
┌─────────────────────────────────────────────────────────────┐
│ CAPA RAW (Bronce) - 2 tablas                                │
├─────────────────────────────────────────────────────────────┤
│ ✓ raw.ibm_hr_monthly_snapshot_byNapo (35 columnas TEXT)    │
│ ✓ raw.ibm_hr_change_reasons_byNapo (6 columnas TEXT)       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ CAPA BUSINESS (Silver) - 2 vistas                           │
├─────────────────────────────────────────────────────────────┤
│ ✓ business.v_employee_full_byNapo (tipificada)             │
│ ✓ business.mv_ui_global_filters (filtros universales)      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ DATA MARTS (Gold) - Módulo 05 completo                      │
├─────────────────────────────────────────────────────────────┤
│ ✓ business.v_org_tree_byNapo (organigrama recursivo)       │
│ ✓ business.mv_monthly_kpis_byNapo                          │
│ ✓ business.mv_demographics_agg                             │
│ ✓ business.mv_diversity_pyramid                            │
│ ✓ business.mv_bajas_heatmap                                │
│ ✓ business.mv_country_dist                                 │
│ ✓ business.mv_experience_bubbles                           │
│ ✓ business.get_demographics_dashboard() RPC                │
│ ✓ business.get_advanced_demographics() RPC                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔍 Análisis Detallado por Módulo

### MÓDULO 01: Visión Ejecutiva 🟡 Parcial (1/3)

#### Fuente de Datos
- **Origen:** `business.v_employee_full_byNapo` + MVs del módulo 05
- **Tablas necesarias:** Ninguna adicional (usa infraestructura existente)

#### Vistas a Implementar

| # | Vista | Tipo | Fuente de Datos | Visualización Sugerida | Complejidad |
|---|-------|------|-----------------|------------------------|-------------|
| 1 | Dashboard C-Level | ✅ IMPLEMENTADA | `business.get_demographics_dashboard()` | KPI Cards + Gráfico Barras | Baja |
| 2 | Alertas & Anomalías | 🔘 PENDIENTE | `business.v_employee_full_byNapo` + Z-Score | Tabla anomalías + Heatmap desviaciones | Media-Alta (ML) |
| 3 | Benchmarking de Mercado | 🔘 PENDIENTE | Datos externos (CSV/JSON) | Radar chart comparativo | Media |

#### Transformaciones Necesarias
```sql
-- Vista sugerida para alertas (Z-Score > 2 o < -2)
CREATE MATERIALIZED VIEW business.mv_alerts_anomalies AS
SELECT 
    snapshot_date,
    country_iso3,
    department_name,
    metric_name,
    metric_value,
    metric_avg,
    metric_stddev,
    z_score,
    CASE WHEN ABS(z_score) > 2 THEN 'ALERTA' ELSE 'NORMAL' END as status
FROM (
    SELECT 
        snapshot_date, country_iso3, department_name,
        'headcount' as metric_name,
        COUNT(*) as metric_value,
        AVG(COUNT(*)) OVER (PARTITION BY country_iso3) as metric_avg,
        STDDEV(COUNT(*)) OVER (PARTITION BY country_iso3) as metric_stddev,
        (COUNT(*) - AVG(COUNT(*)) OVER (PARTITION BY country_iso3)) / 
            NULLIF(STDDEV(COUNT(*)) OVER (PARTITION BY country_iso3), 0) as z_score
    FROM business.v_employee_full_byNapo
    WHERE is_active_at_snapshot = TRUE
    GROUP BY snapshot_date, country_iso3, department_name
) subq;
```

---

### MÓDULO 02: Reclutamiento & Selección 🔘 Pendiente (0/5)

#### Fuente de Datos Requerida
- **Nueva tabla necesaria:** `raw.recruitment_pipeline` (seguimiento de candidatos)
- **Nueva tabla necesaria:** `raw.job_postings` (vacantes publicadas)

#### Esquema Propuesto para Nuevas Tablas

```sql
-- Tabla: raw.job_postings
CREATE TABLE raw.job_postings (
    posting_id TEXT,
    job_title TEXT,
    department_name TEXT,
    country_iso3 TEXT,
    job_level_1 TEXT,
    job_level_2 TEXT,
    required_skills JSONB,
    salary_range_min NUMERIC,
    salary_range_max NUMERIC,
    posting_date TEXT,
    closing_date TEXT,
    status TEXT, -- 'Open', 'Closed', 'On Hold'
    positions_available INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla: raw.recruitment_pipeline
CREATE TABLE raw.recruitment_pipeline (
    candidate_id TEXT,
    posting_id TEXT,
    full_name TEXT,
    gender TEXT,
    age INTEGER,
    education_level TEXT,
    years_experience INTEGER,
    application_date TEXT,
    stage TEXT, -- 'Applied', 'Screening', 'Interview', 'Offer', 'Hired', 'Rejected'
    stage_change_date TEXT,
    interviewer_id TEXT,
    interview_score NUMERIC,
    fit_score_predicted NUMERIC, -- ML output
    bias_audit_flag TEXT, -- 'Y', 'N'
    nps_score INTEGER, -- -100 to 100
    rejection_reason TEXT,
    hired_employee_id TEXT, -- FK a employee_id si fue contratado
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Vistas a Implementar

| # | Vista | Tipo | Fuente | Visualización | Tags |
|---|-------|------|--------|---------------|------|
| 1 | Eficiencia & Ciclos | DESC | `raw.recruitment_pipeline` | Funnel chart + Box plot tiempos | DESC |
| 2 | Calidad de Contratación | DESC/PRED | `raw.recruitment_pipeline` + `v_employee_full_byNapo` | Scatter plot QoH vs tiempo | DESC, PRED |
| 3 | Fit Score Predictivo | ML | ML Model Output | Histograma scores + Top candidatos | ML |
| 4 | Auditoría de Sesgos | ML | `raw.recruitment_pipeline` | Matriz disparidades por демография | ML |
| 5 | NPS Candidato | DESC | `raw.recruitment_pipeline` | Gauge chart + Trend line | DESC |

#### Scripts Python Necesarios
- `m02_reclutamiento.py` - Crear vistas y MVs del módulo 02
- `ml_fit_score.py` - Modelo predictivo de fit score (opcional, fase 2)

---

### MÓDULO 03: Onboarding & Integración 🔘 Pendiente (0/3)

#### Fuente de Datos Requerida
- **Nueva tabla necesaria:** `raw.onboarding_checklist`
- **Nueva tabla necesaria:** `raw.training_completion`

#### Esquema Propuesto

```sql
-- Tabla: raw.onboarding_checklist
CREATE TABLE raw.onboarding_checklist (
    onboarding_id TEXT,
    employee_id TEXT, -- FK a v_employee_full_byNapo
    checklist_item TEXT,
    category TEXT, -- 'Documentación', 'Equipamiento', 'Capacitación', 'Presentaciones'
    assigned_to TEXT,
    due_date TEXT,
    completion_date TEXT,
    status TEXT, -- 'Pending', 'Completed', 'Overdue'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla: raw.productivity_milestones
CREATE TABLE raw.productivity_milestones (
    milestone_id TEXT,
    employee_id TEXT,
    milestone_name TEXT,
    expected_days INTEGER,
    actual_days INTEGER,
    achievement_date TEXT,
    performance_rating NUMERIC,
    manager_id TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Vistas a Implementar

| # | Vista | Tipo | Fuente | Visualización | Tags |
|---|-------|------|--------|---------------|------|
| 1 | Procesos Activos | DESC | `raw.onboarding_checklist` | Gantt chart + Progress bars | DESC |
| 2 | Tiempo a Productividad | DESC/PRED | `raw.productivity_milestones` | Curvas aprendizaje + Forecast | DESC, PRED |
| 3 | Rotación Temprana (<90d) | DESC/PRED | `v_employee_full_byNapo` filtrado | Cohort analysis heatmap | DESC, PRED |

---

### MÓDULO 04: Análisis de Ciclo de Vida & Clústeres 🔘 Pendiente (0/3)

#### Fuente de Datos
- **Principal:** `business.v_employee_full_byNapo` (datos históricos)
- **Complementaria:** MVs existentes del módulo 05

#### Vistas a Implementar

| # | Vista | Tipo | Fuente | Visualización | Tags |
|---|-------|------|--------|---------------|------|
| 1 | Comportamiento de Grupos | DESC/ML | `v_employee_full_byNapo` + K-Means | Cluster scatter plot + PCA | DESC, ML |
| 2 | Causalidad & Correlaciones | ML | Todas las tablas | Network graph correlaciones | ML |
| 3 | Mapa Momentos Críticos | PRED | `v_employee_full_byNapo` + Survival Analysis | Hazard curve + Timeline | PRED |

#### Transformaciones Necesarias (Python/ML)
```python
# Script sugerido: m04_ciclo_vida.py
# - K-Means clustering para segmentación de empleados
# - Análisis de supervivencia (Kaplan-Meier) para rotación
# - Matriz de correlaciones multivariadas
```

---

### MÓDULO 05: Fuerza Laboral & Estructura ✅ COMPLETO (6/6)

#### Estado: ✅ 100% Implementado

| Vista | Objeto DB | Componente React | Estado |
|-------|-----------|------------------|--------|
| Demografía & Headcount | `business.get_demographics_dashboard()` RPC | `Demographics.jsx` | ✅ |
| Organigrama Integral | `business.v_org_tree_byNapo` | `OrganigramaIntegral.jsx` | ⚠️ Mock (conectar) |
| Organigrama Posiciones | Múltiples queries | `OrgStructure.jsx` | ✅ |
| Organigrama Costos | (Incluido en MVs) | Pendiente frontend | 🔘 |
| Distribución Geográfica | `business.mv_country_dist` | (En Demographics.jsx) | ✅ |
| Forecast Dotación | (Incluido en MVs) | Pendiente frontend | 🔘 |

#### No requiere acción adicional - Módulo base para otros módulos

---

### MÓDULO 06: Nómina, Costos & Equity 🟡 Parcial (1/6)

#### Fuente de Datos
- **Principal:** `business.v_employee_full_byNapo` (columnas salariales)
- **Complementaria:** `raw.ibm_hr_change_reasons_byNapo`

#### Vistas a Implementar

| # | Vista | Tipo | Fuente | Visualización | Tags | Estado |
|---|-------|------|--------|---------------|------|--------|
| 1 | Bandas Salariales | DESC | `v_employee_full_byNapo` | Box plot por job_level | DESC | 🔘 |
| 2 | Equidad Interna | DESC/ML | `v_employee_full_byNapo` | Scatter ajustado por variables | DESC, ML | ✅ (`Compensations.jsx`) |
| 3 | Compa-Ratio vs Mercado | DESC | `v_employee_full_byNapo` + benchmarks | Histograma compa-ratio | DESC | 🔘 |
| 4 | Masa Salarial & Presupuesto | DESC | `v_employee_full_byNapo` | Waterfall chart + variance | DESC | 🔘 |
| 5 | Impacto Financiero Rotación | DESC/PRED | `v_employee_full_byNapo` + costos | Sankey diagram costos | DESC, PRED | 🔘 |
| 6 | Simulador Escenarios | PRED | Input usuario + MVs | What-if analysis dashboard | PRED | 🔘 |

#### Transformaciones Necesarias
```sql
-- Vista sugerida: Bandas Salariales
CREATE MATERIALIZED VIEW business.mv_salary_bands AS
SELECT 
    department_name,
    job_level_1,
    job_level_2,
    job_role,
    country_iso3,
    PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY monthly_salary_usd) as p10,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY monthly_salary_usd) as p25,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY monthly_salary_usd) as p50,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY monthly_salary_usd) as p75,
    PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY monthly_salary_usd) as p90,
    AVG(monthly_salary_usd) as avg_salary,
    STDDEV(monthly_salary_usd) as stddev_salary,
    COUNT(*) as employee_count
FROM business.v_employee_full_byNapo
WHERE is_active_at_snapshot = TRUE AND monthly_salary_usd IS NOT NULL
GROUP BY department_name, job_level_1, job_level_2, job_role, country_iso3;

-- Vista sugerida: Compa-Ratio
CREATE MATERIALIZED VIEW business.mv_compa_ratio AS
SELECT 
    employee_id,
    full_name,
    department_name,
    job_role,
    monthly_salary_usd,
    band_median,
    ROUND((monthly_salary_usd / NULLIF(band_median, 0)) * 100, 1) as compa_ratio_pct,
    CASE 
        WHEN monthly_salary_usd / band_median < 0.8 THEN 'Below Range'
        WHEN monthly_salary_usd / band_median > 1.2 THEN 'Above Range'
        ELSE 'In Range'
    END as range_status
FROM business.v_employee_full_byNapo emp
JOIN business.mv_salary_bands band 
    ON emp.department_name = band.department_name 
    AND emp.job_role = band.job_role
    AND emp.country_iso3 = band.country_iso3
WHERE is_active_at_snapshot = TRUE;
```

#### Scripts Python Necesarios
- `m06_nomina_costos.py` - Crear MVs restantes del módulo 06

---

### MÓDULO 07: Tiempo, Asistencia & Bienestar 🔘 Pendiente (0/6)

#### Fuente de Datos Requerida
- **Nueva tabla necesaria:** `raw.attendance_records`
- **Nueva tabla necesaria:** `raw.overtime_logs`
- **Nueva tabla necesaria:** `raw.leave_requests`
- **Nueva tabla necesaria:** `raw.incidents_sst`

#### Esquema Propuesto

```sql
-- Tabla: raw.attendance_records
CREATE TABLE raw.attendance_records (
    record_id TEXT,
    employee_id TEXT,
    work_date TEXT,
    check_in_time TEXT,
    check_out_time TEXT,
    scheduled_hours NUMERIC,
    worked_hours NUMERIC,
    absence_type TEXT, -- 'Present', 'Sick Leave', 'Vacation', 'Unpaid', etc.
    late_minutes INTEGER,
    work_modality TEXT, -- 'Remote', 'Hybrid', 'On-Site'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla: raw.overtime_logs
CREATE TABLE raw.overtime_logs (
    overtime_id TEXT,
    employee_id TEXT,
    date_from TEXT,
    date_to TEXT,
    hours_overtime NUMERIC,
    overtime_type TEXT, -- 'Regular', 'Holiday', 'Weekend'
    approval_status TEXT,
    cost_usd NUMERIC,
    reason TEXT,
    manager_approval_id TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla: raw.leave_requests
CREATE TABLE raw.leave_requests (
    leave_id TEXT,
    employee_id TEXT,
    leave_type TEXT, -- 'Vacation', 'Sick', 'Personal', 'Maternity', etc.
    start_date TEXT,
    end_date TEXT,
    total_days NUMERIC,
    balance_before NUMERIC,
    balance_after NUMERIC,
    approval_status TEXT,
    approved_by TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla: raw.incidents_sst
CREATE TABLE raw.incidents_sst (
    incident_id TEXT,
    employee_id TEXT,
    incident_date TEXT,
    incident_type TEXT, -- 'Accident', 'Near Miss', 'Illness'
    severity TEXT, -- 'Minor', 'Moderate', 'Severe', 'Fatal'
    body_part_affected TEXT,
    location TEXT,
    lost_days INTEGER,
    investigation_status TEXT,
    corrective_actions JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Vistas a Implementar

| # | Vista | Tipo | Fuente | Visualización | Tags |
|---|-------|------|--------|---------------|------|
| 1 | Ausentismo & Permisos | DESC/PRED/ML | `raw.attendance_records` | Heatmap calendario + Forecast | DESC, PRED, ML |
| 2 | Horas Extra & Jornada | DESC | `raw.overtime_logs` | Stacked area chart + Alerts | DESC |
| 3 | Malla Vacaciones | DESC | `raw.leave_requests` | Calendar view + Balance bars | DESC |
| 4 | Salud Ocupacional (SST) | DESC | `raw.incidents_sst` | Pyramid gravedad + Trend | DESC |
| 5 | Índice Bienestar & Burnout | DESC/ML | ML Model (encuestas + ops data) | Risk gauge + Heatmap | DESC, ML |
| 6 | Optimización Turnos | ML/OPT | Algoritmo genético + LSTM | Roster optimizer UI | ML, OPT |

#### Scripts Python Necesarios
- `m07_tiempo_bienestar.py` - Crear MVs del módulo 07
- `ml_burnout_prediction.py` - Modelo predictivo de burnout (fase 2)
- `opt_turnos.py` - Optimizador de turnos (fase 2)

---

### MÓDULO 08: Gestión del Desempeño 🔘 Pendiente (0/4)

#### Fuente de Datos Requerida
- **Nueva tabla necesaria:** `raw.performance_reviews`
- **Nueva tabla necesaria:** `raw.goals_okrs`
- **Nueva tabla necesaria:** `raw.pip_plans`

#### Esquema Propuesto

```sql
-- Tabla: raw.performance_reviews
CREATE TABLE raw.performance_reviews (
    review_id TEXT,
    employee_id TEXT,
    review_date TEXT,
    review_cycle TEXT, -- 'Q1 2025', 'Annual 2024'
    reviewer_id TEXT,
    review_type TEXT, -- 'Self', 'Manager', 'Peer', '360'
    overall_rating NUMERIC, -- 1-5 scale
    competencies_scores JSONB, -- {"Leadership": 4, "Communication": 3, ...}
    strengths_summary TEXT,
    improvement_areas TEXT,
    ai_generated_summary TEXT, -- IA Generativa output
    sentiment_score NUMERIC, -- NLP analysis
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla: raw.goals_okrs
CREATE TABLE raw.goals_okrs (
    goal_id TEXT,
    employee_id TEXT,
    goal_type TEXT, -- 'OKR', 'KPI', 'Development Goal'
    goal_description TEXT,
    target_value NUMERIC,
    current_value NUMERIC,
    unit TEXT,
    start_date TEXT,
    end_date TEXT,
    progress_pct NUMERIC,
    status TEXT, -- 'On Track', 'At Risk', 'Off Track', 'Completed'
    parent_goal_id TEXT, -- For hierarchical OKRs
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla: raw.pip_plans
CREATE TABLE raw.pip_plans (
    pip_id TEXT,
    employee_id TEXT,
    start_date TEXT,
    end_date TEXT,
    manager_id TEXT,
    performance_issues TEXT,
    goals_json JSONB,
    weekly_checkins JSONB,
    final_outcome TEXT, -- 'Improved', 'Terminated', 'Extended'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Vistas a Implementar

| # | Vista | Tipo | Fuente | Visualización | Tags |
|---|-------|------|--------|---------------|------|
| 1 | Evaluación 360° | DESC/IA/NLP | `raw.performance_reviews` | Radar chart competencias + AI summary | DESC, IA, NLP |
| 2 | Avance OKRs/KPIs | DESC | `raw.goals_okrs` | Progress bars + Forecast cierre | DESC |
| 3 | Planes de Mejora (PIP) | DESC | `raw.pip_plans` | Timeline progreso + Status table | DESC |
| 4 | Ranking & Top Performers | DESC | `raw.performance_reviews` | Leaderboard + Distribution histogram | DESC |

#### Scripts Python Necesarios
- `m08_desempeno.py` - Crear MVs del módulo 08
- `nlp_review_summaries.py` - IA generativa para resúmenes de reviews

---

### MÓDULO 09: Talento & Desarrollo 🔘 Pendiente (0/5)

#### Fuente de Datos Requerida
- **Nueva tabla necesaria:** `raw.employee_skills`
- **Nueva tabla necesaria:** `raw.succession_plans`
- **Nueva tabla necesaria:** `raw.internal_postings`
- **Nueva tabla necesaria:** `raw.training_programs`

#### Esquema Propuesto

```sql
-- Tabla: raw.employee_skills
CREATE TABLE raw.employee_skills (
    skill_id TEXT,
    employee_id TEXT,
    skill_name TEXT,
    proficiency_level TEXT, -- 'Beginner', 'Intermediate', 'Advanced', 'Expert'
    years_experience NUMERIC,
    last_used_date TEXT,
    certification_name TEXT,
    certification_expiry TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla: raw.nine_box_matrix
CREATE TABLE raw.nine_box_matrix (
    assessment_id TEXT,
    employee_id TEXT,
    assessment_date TEXT,
    performance_score NUMERIC, -- 1-5
    potential_score NUMERIC, -- 1-5
    nine_box_quadrant TEXT, -- Calculated field
    assessor_id TEXT,
    development_recommendations TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla: raw.succession_plans
CREATE TABLE raw.succession_plans (
    succession_id TEXT,
    position_id TEXT,
    incumbent_employee_id TEXT,
    successor_employee_id TEXT,
    readiness_level TEXT, -- 'Ready Now', 'Ready 1-2 yrs', 'Ready 3-5 yrs'
    development_gaps JSONB,
    risk_if_vacant TEXT, -- 'Critical', 'High', 'Medium', 'Low'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla: raw.training_programs
CREATE TABLE raw.training_programs (
    training_id TEXT,
    program_name TEXT,
    category TEXT, -- 'Technical', 'Leadership', 'Compliance', etc.
    delivery_mode TEXT, -- 'Online', 'In-Person', 'Blended'
    cost_per_employee NUMERIC,
    duration_hours NUMERIC,
    employees_enrolled INTEGER,
    employees_completed INTEGER,
    avg_post_training_score NUMERIC,
    roi_calculated NUMERIC,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Vistas a Implementar

| # | Vista | Tipo | Fuente | Visualización | Tags |
|---|-------|------|--------|---------------|------|
| 1 | Matriz 9-Box | DESC/ML | `raw.nine_box_matrix` | 9-box grid interactive | DESC, ML |
| 2 | Continuidad & Sucesión | DESC | `raw.succession_plans` | Org chart con readiness | DESC |
| 3 | Movilidad Interna | ML | `raw.internal_postings` + skills | Job matching recommendations | ML |
| 4 | Ejecución L&D | DESC/ML | `raw.training_programs` | Completion funnel + Skills gap | DESC, ML |
| 5 | ROI Capacitación | DESC/PRED | `raw.training_programs` + performance | Correlation scatter + ROI calc | DESC, PRED |

#### Scripts Python Necesarios
- `m09_talento_desarrollo.py` - Crear MVs del módulo 09
- `ml_skills_matching.py` - Algoritmo de matching skills-vacantes

---

### MÓDULO 10: Engagement & Sentimiento 🔘 Pendiente (0/3)

#### Fuente de Datos Requerida
- **Nueva tabla necesaria:** `raw.survey_responses`
- **Nueva tabla necesaria:** `raw.feedback_comments`

#### Esquema Propuesto

```sql
-- Tabla: raw.survey_responses
CREATE TABLE raw.survey_responses (
    response_id TEXT,
    employee_id TEXT,
    survey_date TEXT,
    survey_type TEXT, -- 'eNPS', 'Engagement', 'Pulse', 'Exit'
    question_id TEXT,
    question_text TEXT,
    response_type TEXT, -- 'Scale', 'Multiple Choice', 'Text'
    response_value TEXT,
    score_normalized NUMERIC, -- 0-100 for calculations
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla: raw.feedback_comments
CREATE TABLE raw.feedback_comments (
    comment_id TEXT,
    employee_id TEXT,
    feedback_date TEXT,
    feedback_type TEXT, -- 'Survey Open Text', 'Suggestion Box', 'Recognition'
    comment_text TEXT,
    sentiment_label TEXT, -- 'Positive', 'Neutral', 'Negative'
    sentiment_score NUMERIC, -- -1 to 1
    topics_extracted JSONB, -- NLP topic modeling
    urgency_flag TEXT, -- 'Y', 'N'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Vistas a Implementar

| # | Vista | Tipo | Fuente | Visualización | Tags |
|---|-------|------|--------|---------------|------|
| 1 | Engagement & Sentimiento (eNPS) | DESC/NLP | `raw.survey_responses` + `feedback_comments` | Gauge eNPS + Word cloud | DESC, NLP |
| 2 | Heatmap Engagement | DESC | `raw.survey_responses` | Matrix heatmap por dept/país | DESC |
| 3 | Diversidad & Inclusión (DEI) | DESC | `v_employee_full_byNapo` + surveys | Representation bars + Pay equity | DESC |

#### Scripts Python Necesarios
- `m10_engagement.py` - Crear MVs del módulo 10
- `nlp_sentiment_analysis.py` - Procesamiento NLP de comentarios

---

### MÓDULO 11: Compliance & Relaciones Laborales 🔘 Pendiente (0/2)

#### Fuente de Datos Requerida
- **Nueva tabla necesaria:** `raw.compliance_obligations`
- **Nueva tabla necesaria:** `raw.union_agreements`

#### Esquema Propuesto

```sql
-- Tabla: raw.compliance_obligations
CREATE TABLE raw.compliance_obligations (
    obligation_id TEXT,
    obligation_type TEXT, -- 'Legal', 'Contractual', 'Policy'
    description TEXT,
    country_iso3 TEXT,
    due_date TEXT,
    frequency TEXT, -- 'One-time', 'Monthly', 'Quarterly', 'Annual'
    responsible_party TEXT,
    status TEXT, -- 'Compliant', 'Due Soon', 'Overdue', 'Not Applicable'
    last_review_date TEXT,
    risk_level TEXT, -- 'Critical', 'High', 'Medium', 'Low'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla: raw.union_agreements
CREATE TABLE raw.union_agreements (
    agreement_id TEXT,
    union_name TEXT,
    country_iso3 TEXT,
    effective_date TEXT,
    expiry_date TEXT,
    coverage_employees INTEGER,
    key_terms JSONB,
    negotiation_status TEXT, -- 'Active', 'Expiring', 'In Negotiation'
    last_incident_date TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Vistas a Implementar

| # | Vista | Tipo | Fuente | Visualización | Tags |
|---|-------|------|--------|---------------|------|
| 1 | Cumplimiento Laboral | DESC | `raw.compliance_obligations` | Compliance dashboard + Alerts | DESC |
| 2 | Relaciones Sindicales | DESC | `raw.union_agreements` | Timeline acuerdos + Coverage | DESC |

#### Scripts Python Necesarios
- `m11_compliance.py` - Crear MVs del módulo 11

---

### MÓDULO 12: Retención & Riesgo de Fuga 🔘 Pendiente (0/3)

#### Fuente de Datos
- **Principal:** `business.v_employee_full_byNapo` (histórico de bajas)
- **Complementaria:** MVs de múltiples módulos

#### Vistas a Implementar

| # | Vista | Tipo | Fuente | Visualización | Tags |
|---|-------|------|--------|---------------|------|
| 1 | Score Predictivo de Fuga | ML/XAI | ML Model (XGBoost/Random Forest) | Risk distribution + SHAP values | ML, XAI |
| 2 | Benchmarking Turnover | DESC | `v_employee_full_byNapo` + benchmarks | Bar chart comparativo | DESC |
| 3 | Correlación Manager-Fuga | ML | `v_employee_full_byNapo` + análisis estadístico | Heatmap managers vs turnover | ML |

#### Transformaciones Necesarias (Python/ML)
```python
# Script sugerido: m12_retencion.py + ml_churn_prediction.py
# Features para el modelo:
# - tenure_months
# - time_since_last_promotion
# - salary_vs_band_median
# - department_turnover_rate
# - manager_tenure
# - overtime_hours_avg
# - performance_rating_trend
# - engagement_score (si disponible)
```

#### Scripts Python Necesarios
- `m12_retencion.py` - Crear MVs del módulo 12
- `ml_churn_prediction.py` - Modelo predictivo de fuga con XAI

---

### MÓDULO 13: Calidad de Datos 🟡 Parcial (1/3)

#### Fuente de Datos
- **Principal:** Metadatos de todas las tablas y vistas
- **Herramientas:** Funciones de PostgreSQL para profiling

#### Vistas a Implementar

| # | Vista | Tipo | Fuente | Visualización | Tags | Estado |
|---|-------|------|--------|---------------|------|--------|
| 1 | Integridad & Auditoría | DESC | Data profiling queries | Data quality dashboard | DESC | ✅ (`EmployeeTable.jsx`) |
| 2 | Log Maestros | DESC | `raw.audit_log` (nueva tabla) | Timeline cambios críticos | DESC | 🔘 |
| 3 | Diccionario de Datos | DESC | Information schema + metadata | Searchable catalog | DESC | 🔘 |

#### Esquema Propuesto

```sql
-- Tabla: raw.audit_log
CREATE TABLE raw.audit_log (
    log_id TEXT,
    table_name TEXT,
    record_id TEXT,
    action_type TEXT, -- 'INSERT', 'UPDATE', 'DELETE'
    changed_columns JSONB, -- {"old": {...}, "new": {...}}
    changed_by TEXT,
    change_timestamp TEXT,
    ip_address TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Vista: business.data_quality_metrics
CREATE OR REPLACE VIEW business.data_quality_metrics AS
SELECT 
    'ibm_hr_monthly_snapshot_byNapo' as table_name,
    COUNT(*) as total_records,
    COUNT(*) FILTER (WHERE employee_id IS NULL) as null_employee_id,
    COUNT(*) FILTER (WHERE full_name IS NULL) as null_full_name,
    COUNT(*) FILTER (WHERE monthly_salary_usd IS NULL) as null_salary,
    ROUND(100.0 * COUNT(*) FILTER (WHERE employee_id IS NOT NULL) / COUNT(*), 2) as completeness_employee_id,
    ROUND(100.0 * COUNT(*) FILTER (WHERE monthly_salary_usd IS NOT NULL) / COUNT(*), 2) as completeness_salary
FROM raw."ibm_hr_monthly_snapshot_byNapo";
```

#### Scripts Python Necesarios
- `m13_calidad_datos.py` - Crear vista de audit log y métricas de calidad

---

## 🗺️ Ruta Crítica de Implementación

### Fase 1: Fundamentos (SEMANA 1-2) ✅ COMPLETADA
- [x] Módulo 05: Fuerza Laboral (100%)
- [x] Pipeline ETL base (scripts 01-04, m05, 90-91)

### Fase 2: Compensaciones y Visión Ejecutiva (SEMANA 3-4) 🔄 EN PROGRESO
- [ ] Módulo 06: Nómina, Costos & Equity (5/6 vistas pendientes)
- [ ] Módulo 01: Visión Ejecutiva (2/3 vistas pendientes)
- [ ] Módulo 13: Calidad de Datos (2/3 vistas pendientes)

### Fase 3: Operaciones RRHH (SEMANA 5-7)
- [ ] Módulo 02: Reclutamiento & Selección (requiere nuevas tablas)
- [ ] Módulo 03: Onboarding & Integración (requiere nuevas tablas)
- [ ] Módulo 07: Tiempo, Asistencia & Bienestar (requiere nuevas tablas)

### Fase 4: Talento y Desempeño (SEMANA 8-10)
- [ ] Módulo 08: Gestión del Desempeño (requiere nuevas tablas)
- [ ] Módulo 09: Talento & Desarrollo (requiere nuevas tablas)
- [ ] Módulo 04: Análisis de Ciclo de Vida (ML básico)

### Fase 5: Advanced Analytics (SEMANA 11-14)
- [ ] Módulo 10: Engagement & Sentimiento (NLP)
- [ ] Módulo 12: Retención & Riesgo de Fuga (ML/XAI)
- [ ] Módulo 11: Compliance & Relaciones Laborales
- [ ] Módulo 07 avanzado: Optimización de Turnos (OPT)

---

## 📁 Estructura de Archivos Propuesta

### Nuevos Scripts ETL a Crear

```
etl_pipeline/
├── 00_full_run_pipeline.py (actualizar para incluir nuevos módulos)
├── 01_generate_synthetic_data.py ✅
├── 02_setup_raw_layer.py ✅
├── 03_ingest_data.py ✅
├── 04_setup_business_core.py ✅
├── m05_fuerza_laboral.py ✅
├── m06_nomina_costos.py 🔘 NUEVO
├── m02_reclutamiento.py 🔘 NUEVO
├── m03_onboarding.py 🔘 NUEVO
├── m07_tiempo_bienestar.py 🔘 NUEVO
├── m08_desempeno.py 🔘 NUEVO
├── m09_talento_desarrollo.py 🔘 NUEVO
├── m10_engagement.py 🔘 NUEVO
├── m11_compliance.py 🔘 NUEVO
├── m12_retencion.py 🔘 NUEVO
├── m13_calidad_datos.py 🔘 NUEVO
├── m04_ciclo_vida.py 🔘 NUEVO
├── ml_fit_score.py 🔘 NUEVO (Fase 2)
├── ml_burnout_prediction.py 🔘 NUEVO (Fase 2)
├── ml_churn_prediction.py 🔘 NUEVO (Fase 2)
├── nlp_sentiment_analysis.py 🔘 NUEVO (Fase 2)
├── nlp_review_summaries.py 🔘 NUEVO (Fase 2)
├── opt_turnos.py 🔘 NUEVO (Fase 2)
├── 90_generate_data_inventory.py ✅
└── 91_export_data_samples.py ✅
```

### Nuevos Componentes React a Crear

```
client/src/modules/
├── 00-layout/ ✅
├── 01-vision-ejecutiva/
│   ├── Overview.jsx ✅
│   ├── AlertsAnomalies.jsx 🔘 NUEVO
│   └── Benchmarking.jsx 🔘 NUEVO
├── 02-reclutamiento/
│   ├── RecruitmentEfficiency.jsx 🔘 NUEVO
│   ├── HiringQuality.jsx 🔘 NUEVO
│   ├── FitScore.jsx 🔘 NUEVO
│   ├── BiasAudit.jsx 🔘 NUEVO
│   └── CandidateNPS.jsx 🔘 NUEVO
├── 03-onboarding/
│   ├── OnboardingActive.jsx 🔘 NUEVO
│   ├── TimeToProductivity.jsx 🔘 NUEVO
│   └── EarlyTurnover.jsx 🔘 NUEVO
├── 04-ciclo-vida/
│   ├── LifecycleClusters.jsx 🔘 NUEVO
│   ├── CausalAnalysis.jsx 🔘 NUEVO
│   └── CriticalMoments.jsx 🔘 NUEVO
├── 05-fuerza-laboral/ ✅
│   ├── Demographics.jsx ✅
│   ├── OrganigramaIntegral.jsx ⚠️
│   └── OrgStructure.jsx ✅
├── 06-nomina-costos/
│   ├── Compensations.jsx ✅
│   ├── SalaryBands.jsx 🔘 NUEVO
│   ├── CompaRatio.jsx 🔘 NUEVO
│   ├── PayrollMass.jsx 🔘 NUEVO
│   ├── TurnoverImpact.jsx 🔘 NUEVO
│   └── SalarySimulator.jsx 🔘 NUEVO
├── 07-tiempo-bienestar/
│   ├── Absenteeism.jsx 🔘 NUEVO
│   ├── Overtime.jsx 🔘 NUEVO
│   ├── VacationPlanner.jsx 🔘 NUEVO
│   ├── OccupationalHealth.jsx 🔘 NUEVO
│   ├── WellbeingIndex.jsx 🔘 NUEVO
│   └── ShiftOptimizer.jsx 🔘 NUEVO
├── 08-desempeno/
│   ├── Performance360.jsx 🔘 NUEVO
│   ├── OKRTracker.jsx 🔘 NUEVO
│   ├── PIPPlans.jsx 🔘 NUEVO
│   └── TopPerformers.jsx 🔘 NUEVO
├── 09-talento-desarrollo/
│   ├── NineBox.jsx 🔘 NUEVO
│   ├── SuccessionPlanning.jsx 🔘 NUEVO
│   ├── InternalMobility.jsx 🔘 NUEVO
│   ├── LearningDevelopment.jsx 🔘 NUEVO
│   └── TrainingROI.jsx 🔘 NUEVO
├── 10-engagement/
│   ├── eNPS.jsx 🔘 NUEVO
│   ├── EngagementHeatmap.jsx 🔘 NUEVO
│   └── DEI.jsx 🔘 NUEVO
├── 11-compliance/
│   ├── ComplianceDashboard.jsx 🔘 NUEVO
│   └── UnionRelations.jsx 🔘 NUEVO
├── 12-retencion/
│   ├── ChurnPrediction.jsx 🔘 NUEVO
│   ├── TurnoverBenchmark.jsx 🔘 NUEVO
│   └── ManagerCorrelation.jsx 🔘 NUEVO
└── 13-calidad-datos/
    ├── EmployeeTable.jsx ✅
    ├── AuditLog.jsx 🔘 NUEVO
    └── DataDictionary.jsx 🔘 NUEVO
```

---

## 📊 Matriz de Dependencias entre Módulos

| Módulo | Depende de | Proporciona datos a |
|--------|-----------|---------------------|
| 01 Visión Ejecutiva | 05, 06, 12 | - |
| 02 Reclutamiento | - | 03, 05, 09 |
| 03 Onboarding | 02 | 04, 05, 08 |
| 04 Ciclo de Vida | 03, 05, 08, 12 | 01, 09, 12 |
| 05 Fuerza Laboral | - | TODOS (base) |
| 06 Nómina | 05 | 01, 09, 12 |
| 07 Tiempo | - | 04, 08, 10, 12 |
| 08 Desempeño | 03, 07 | 04, 09, 12 |
| 09 Talento | 02, 06, 08 | 04, 12 |
| 10 Engagement | 07, 08 | 04, 12 |
| 11 Compliance | - | - |
| 12 Retención | 04, 06, 07, 08, 09, 10 | 01 |
| 13 Calidad | TODAS las tablas | - |

---

## 🎯 Próximos Pasos Inmediatos

### Prioridad 1 (Esta Semana)
1. **Completar Módulo 06:**
   - Crear `m06_nomina_costos.py` con MVs faltantes
   - Desarrollar componentes React: `SalaryBands.jsx`, `CompaRatio.jsx`, `PayrollMass.jsx`

2. **Completar Módulo 01:**
   - Crear vista `business.mv_alerts_anomalies`
   - Desarrollar componente `AlertsAnomalies.jsx`

3. **Conectar Organigrama:**
   - Actualizar `OrganigramaIntegral.jsx` para usar `v_org_tree_byNapo`

### Prioridad 2 (Próxima Semana)
1. **Definir esquemas de nuevas tablas** para módulos 02, 03, 07
2. **Generar datos sintéticos** para estas nuevas tablas (extender script 01)
3. **Crear scripts ETL** para módulos prioritarios

### Prioridad 3 (Largo Plazo)
1. **Implementar modelos ML** para predicción de fuga, fit score, burnout
2. **Integrar NLP** para análisis de sentimiento y resúmenes automáticos
3. **Desarrollar optimizador** de turnos con algoritmos genéticos

---

## 📈 Métricas de Éxito

| Métrica | Objetivo | Actual | Target Q2 | Target Año |
|---------|----------|--------|-----------|------------|
| Módulos completados | 13 | 1 (05) | 5 | 13 |
| Vistas implementadas | 52 | 9 | 25 | 52 |
| Cobertura ETL | 100% | 20% | 60% | 100% |
| Componentes React | 52 | 6 | 25 | 52 |
| Modelos ML implementados | 5 | 0 | 2 | 5 |

---

## 📝 Notas Importantes

1. **Orden de ejecución:** Los módulos deben implementarse en orden de dependencia (05 → 06 → 01 → otros)
2. **Datos sintéticos:** Cada nuevo módulo requiere extensión del script `01_generate_synthetic_data.py`
3. **Performance:** Usar materialized views siempre que sea posible para dashboards
4. **Frontend:** Mantener patrón de "Zero Hardcoding" - todo dinámico desde BD
5. **Documentación:** Actualizar README.md después de cada módulo completado (Prompt 90)

---

## ✅ Checklist de Validación por Módulo

Para cada módulo nuevo, verificar:
- [ ] Script ETL creado (`mXX_nombre.py`)
- [ ] Vistas/MVs creadas en esquema `business`
- [ ] Funciones RPC creadas (si aplica)
- [ ] Índices agregados para performance
- [ ] Componentes React desarrollados
- [ ] Conexión a Supabase verificada
- [ ] Tests manuales completados
- [ ] Documentación actualizada

---

*Documento generado como parte del plan de conversión de datos - GDH Analytics v0.0.0*
