# 🗺️ Dashboard Lineage — GDH Analytics
> **Auto-generado por `92_generate_lineage.py`** · Última ejecución: `2026-05-03 12:09`
> Ejecutar `00_full_run_pipeline.py` para actualizar los row counts en tiempo real.

---

## 📊 Sección 1 — Salud del Pipeline

| 🟢 Datos OK (≥100 rows) | 🟡 Escasas (1–99 rows) | 🔴 Críticas (0 rows) | Total MVs |
|------------------------|------------------------|----------------------|-----------|
| **19** | **10** | **0** | **29** |

### 🚨 Prioridades de Enriquecimiento (ordenadas por urgencia)

| # | MV | Rows | Módulo | Script a Intervenir |
|---|-----|------|--------|---------------------|
| 1 | `mv_training_roi` | 🔴 1 | M09 | `m09_talento_desarrollo.py` |
| 2 | `mv_ui_global_filters` | 🔴 1 | M13 | `m13_calidad_datos.py` |
| 3 | `mv_sst_incidents` | 🔴 2 | M07 | `m07_tiempo_bienestar.py` |
| 4 | `mv_sentiment_summary` | 🔴 3 | M10 | `m10_engagement.py` |
| 5 | `mv_nine_box` | 🔴 5 | M09 | `m09_talento_desarrollo.py` |
| 6 | `mv_compliance_dashboard` | 🔴 6 | M11 | `m11_compliance.py` |
| 7 | `mv_enps_trend` | 🟡 30 | M10 | `m10_engagement.py` |
| 8 | `mv_overtime_summary` | 🟡 30 | M07 | `m07_tiempo_bienestar.py` |
| 9 | `mv_performance_summary` | 🟡 30 | M08 | `m08_desempeno.py` |
| 10 | `mv_critical_moments` | 🟡 47 | M04 | `m04_ciclo_vida.py` |

---

## 📋 Sección 2 — Linaje por Módulo (Orden del Menú)

> *Nota: Algunos componentes .jsx listados aquí son aspiracionales/planeados y pueden no existir aún en la carpeta client/src/modules/.*

### M01 · Visión Ejecutiva

| Submenú | Gráficas | MV Fuente | Rows | Script ETL |
|---------|----------|-----------|------|------------|
| Alertas & Anomalías | Bar distribución, Pie concentración, Area tendencia… | `mv_alerts_anomalies` | 🟢 2,250 | `m01_vision_ejecutiva.py` |
| Benchmarking de Mercado | Boxplot, Scatter salario/antigüedad, Radar benchmark… | `mv_salary_bands` | 🟢 46,146 | `m06_nomina_costos.py` |
| Equidad Interna |  |  |  |  |
| Estructura & Bandas Salariales |  |  |  |  |

### M02 · Reclutamiento & Selección

| Submenú | Gráficas | MV Fuente | Rows | Script ETL |
|---------|----------|-----------|------|------------|
| Eficiencia & Ciclos | Funnel, Gauge SLA, Bar horizontal… | `mv_recruitment_funnel` | 🟢 683 | `m02_reclutamiento.py` |
| Fit Score Predictivo |  |  |  |  |
| Auditoría de Sesgos |  |  |  |  |
| NPS del Candidato |  |  |  |  |
| Calidad de Contratación | Scatter fit score, Radar competencias, Bar retención… | `mv_time_to_fill` | 🟢 683 | `m02_reclutamiento.py` |

### M03 · Onboarding & Integración

| Submenú | Gráficas | MV Fuente | Rows | Script ETL |
|---------|----------|-----------|------|------------|
| Procesos Activos | Bar, Pie, Area… | `mv_onboarding_status` | 🟢 2,231 | `m03_onboarding.py` |
| Tiempo a Productividad |  |  |  |  |
| Rotación Temprana (<90d) | Line cohortes, Bar causas, Heatmap dept/mes… | `mv_early_turnover` | 🟢 2,250 | `m03_onboarding.py` |

### M04 · Ciclo de Vida & Clústeres

| Submenú | Gráficas | MV Fuente | Rows | Script ETL |
|---------|----------|-----------|------|------------|
| Comportamiento de Grupos | Bar, Pie, Area… | `mv_lifecycle_cohorts` | 🟢 16,818 | `m04_ciclo_vida.py` |
| Causalidad & Correlaciones |  |  |  |  |
| Mapa de Momentos Críticos | Bar, Pie, Area… | `mv_critical_moments` | 🟡 47 | `m04_ciclo_vida.py` |

### M05 · Fuerza Laboral & Estructura

| Submenú | Gráficas | MV Fuente | Rows | Script ETL |
|---------|----------|-----------|------|------------|
| Demografía & Headcount | Pirámide, Heatmap bajas, Mapa países… | `mv_demographics_agg` | 🟢 13,500 | `m05_fuerza_laboral.py` |
| Demografía & Headcount | Pirámide | `mv_diversity_pyramid` | 🟢 25,818 | `m05_fuerza_laboral.py` |
| Demografía & Headcount | Heatmap | `mv_bajas_heatmap` | 🟢 1,514 | `m05_fuerza_laboral.py` |
| Demografía & Headcount | Mapa geográfico | `mv_country_dist` | 🟢 13,500 | `m05_fuerza_laboral.py` |
| Demografía & Headcount | Bubble chart | `mv_experience_bubbles` | 🟢 123,873 | `m05_fuerza_laboral.py` |

### M06 · Nómina, Costos & Equidad

| Submenú | Gráficas | MV Fuente | Rows | Script ETL |
|---------|----------|-----------|------|------------|
| Benchmarking de Mercado | Boxplot, Scatter salario/antigüedad, Radar benchmark… | `mv_salary_bands` | 🟢 46,146 | `m06_nomina_costos.py` |
| Equidad Interna |  |  |  |  |
| Estructura & Bandas Salariales |  |  |  |  |
| Compa-Ratio vs. Mercado | Gauge, Area histórico, Bar stacked… | `mv_compa_ratio` | 🟢⚠️ 1,566,995 | `m06_nomina_costos.py` |
| Simulador de Escenarios |  |  |  |  |
| Masa Salarial & Presupuesto | Treemap, Bar payroll, Doughnut fijo/variable | `mv_payroll_mass` | 🟢 4,500 | `m06_nomina_costos.py` |
| Impacto Financiero de Rotación | Bar, Pie, Area… | `mv_turnover_cost` | 🟢 2,250 | `m06_nomina_costos.py` |

### M07 · Tiempo, Asistencia & Bienestar

| Submenú | Gráficas | MV Fuente | Rows | Script ETL |
|---------|----------|-----------|------|------------|
| Ausentismo & Permisos | Bar, Pie, Area… | `mv_absenteeism` | 🟢 2,250 | `m07_tiempo_bienestar.py` |
| Malla de Vacaciones |  |  |  |  |
| Optimización de Turnos |  |  |  |  |
| Horas Extra & Jornada | Bar, Pie, Area… | `mv_overtime_summary` | 🟡 30 | `m07_tiempo_bienestar.py` |
| Salud Ocupacional (SST) | Bar, Pie, Area… | `mv_sst_incidents` | 🔴 2 | `m07_tiempo_bienestar.py` |
| Índice de Bienestar & Burnout |  |  |  |  |

### M08 · Gestión del Desempeño

| Submenú | Gráficas | MV Fuente | Rows | Script ETL |
|---------|----------|-----------|------|------------|
| Evaluación 360° | Bar stacked, Treemap, Radar competencias… | `mv_performance_summary` | 🟡 30 | `m08_desempeno.py` |
| Avance de OKRs |  |  |  |  |
| Planes de Mejora (PIP) |  |  |  |  |
| Ranking & Top Performers |  |  |  |  |

### M09 · Talento & Desarrollo

| Submenú | Gráficas | MV Fuente | Rows | Script ETL |
|---------|----------|-----------|------|------------|
| Matriz 9-Box | Heatmap 3x3, Scatter, Bar por área… | `mv_nine_box` | 🔴 5 | `m09_talento_desarrollo.py` |
| Continuidad & Sucesión |  |  |  |  |
| Movilidad Interna |  |  |  |  |
| ROI de Capacitación | Bar, Pie, Area… | `mv_training_roi` | 🔴 1 | `m09_talento_desarrollo.py` |
| Ejecución de L&D |  |  |  |  |

### M10 · Engagement & Sentimiento

| Submenú | Gráficas | MV Fuente | Rows | Script ETL |
|---------|----------|-----------|------|------------|
| Engagement & eNPS | Gauge score, WordCloud, Line histórico… | `mv_enps_trend` | 🟡 30 | `m10_engagement.py` |
| Diversidad & Inclusión (DEI) |  |  |  |  |
| Heatmap de Engagement | Bar, Pie, Area… | `mv_sentiment_summary` | 🔴 3 | `m10_engagement.py` |

### M11 · Compliance & Relaciones

| Submenú | Gráficas | MV Fuente | Rows | Script ETL |
|---------|----------|-----------|------|------------|
| Cumplimiento Laboral | Bar, Pie, Area… | `mv_compliance_dashboard` | 🔴 6 | `m11_compliance.py` |
| Relaciones Sindicales |  |  |  |  |

### M12 · Retención & Riesgo de Fuga

| Submenú | Gráficas | MV Fuente | Rows | Script ETL |
|---------|----------|-----------|------|------------|
| Score Predictivo de Fuga | Heatmap dept/nivel, Scatter riesgo/impacto, Treemap causas | `mv_turnover_analysis` | 🟢 4,500 | `m12_retencion.py` |
| Benchmarking de Turnover |  |  |  |  |
| Correlación Manager-Fuga | Bar, Pie, Area… | `mv_manager_turnover` | 🟢 42,071 | `m12_retencion.py` |

### M13 · Calidad de Datos

| Submenú | Gráficas | MV Fuente | Rows | Script ETL |
|---------|----------|-----------|------|------------|
| Log de Datos Maestros | Bar, Pie, Area… | `mv_monthly_kpis_bynapo` | 🟢 450 | `m13_calidad_datos.py` |
| Diccionario de Datos | Bar, Pie | `mv_ui_global_filters` | 🔴 1 | `m13_calidad_datos.py` |

---

## 🔗 Sección 3 — Lineage Inverso: MV → Submenús

| MV | Rows | Script Creador | Submenús | Componentes .jsx (Planeados/Reales) |
|----|------|---------------|----------|---------------------------------------|
| `mv_absenteeism` | 🟢 2,250 | `m07_tiempo_bienestar.py` | Ausentismo & Permisos, Malla de Vacaciones, Optimización de Turnos | Ausentismo.jsx, MallaVacaciones.jsx |
| `mv_alerts_anomalies` | 🟢 2,250 | `m01_vision_ejecutiva.py` | Alertas & Anomalías | AlertasAnomalias.jsx |
| `mv_bajas_heatmap` | 🟢 1,514 | `m05_fuerza_laboral.py` | Demografía & Headcount | Demographics.jsx |
| `mv_compa_ratio` | 🟢⚠️ 1,566,995 | `m06_nomina_costos.py` | Compa-Ratio vs. Mercado, Simulador de Escenarios | CompaRatio.jsx, SimuladorSalarial.jsx |
| `mv_compliance_dashboard` | 🔴 6 | `m11_compliance.py` | Cumplimiento Laboral, Relaciones Sindicales | CumplimientoLaboral.jsx, RelacionesSindicales.jsx |
| `mv_country_dist` | 🟢 13,500 | `m05_fuerza_laboral.py` | Demografía & Headcount | Demographics.jsx |
| `mv_critical_moments` | 🟡 47 | `m04_ciclo_vida.py` | Mapa de Momentos Críticos | MapaMomentos.jsx |
| `mv_demographics_agg` | 🟢 13,500 | `m05_fuerza_laboral.py` | Demografía & Headcount | Demographics.jsx |
| `mv_diversity_pyramid` | 🟢 25,818 | `m05_fuerza_laboral.py` | Demografía & Headcount | Demographics.jsx |
| `mv_early_turnover` | 🟢 2,250 | `m03_onboarding.py` | Rotación Temprana (<90d) | RotacionTemprana.jsx |
| `mv_enps_trend` | 🟡 30 | `m10_engagement.py` | Engagement & eNPS, Diversidad & Inclusión (DEI) | EngagementENPS.jsx, DiversidadInclusion.jsx |
| `mv_experience_bubbles` | 🟢 123,873 | `m05_fuerza_laboral.py` | Demografía & Headcount | Demographics.jsx |
| `mv_lifecycle_cohorts` | 🟢 16,818 | `m04_ciclo_vida.py` | Comportamiento de Grupos, Causalidad & Correlaciones | ComportamientoGrupos.jsx, CausalidadCorrelaciones.jsx |
| `mv_manager_turnover` | 🟢 42,071 | `m12_retencion.py` | Correlación Manager-Fuga | CorrelacionManager.jsx |
| `mv_monthly_kpis_bynapo` | 🟢 450 | `m13_calidad_datos.py` | Log de Datos Maestros | LogDatosMaestros.jsx |
| `mv_nine_box` | 🔴 5 | `m09_talento_desarrollo.py` | Matriz 9-Box, Continuidad & Sucesión, Movilidad Interna | MatrizNineBox.jsx, MapaSucesion.jsx, BrechasSkills.jsx |
| `mv_onboarding_status` | 🟢 2,231 | `m03_onboarding.py` | Procesos Activos, Tiempo a Productividad | ProcesosActivos.jsx, TiempoProductividad.jsx |
| `mv_overtime_summary` | 🟡 30 | `m07_tiempo_bienestar.py` | Horas Extra & Jornada | HorasExtra.jsx |
| `mv_payroll_mass` | 🟢 4,500 | `m06_nomina_costos.py` | Masa Salarial & Presupuesto | MasaSalarial.jsx |
| `mv_performance_summary` | 🟡 30 | `m08_desempeno.py` | Evaluación 360°, Avance de OKRs, Planes de Mejora (PIP), Ranking & Top Performers | Evaluacion360.jsx, AvanceOKRs.jsx, PlanesMejora.jsx, RankingPerformers.jsx |
| `mv_recruitment_funnel` | 🟢 683 | `m02_reclutamiento.py` | Eficiencia & Ciclos, Fit Score Predictivo, Auditoría de Sesgos, NPS del Candidato | EficienciaCiclos.jsx, FitScore.jsx, AuditoriaSesgos.jsx, NpsCandidato.jsx |
| `mv_salary_bands` | 🟢 46,146 | `m06_nomina_costos.py` | Benchmarking de Mercado, Equidad Interna, Estructura & Bandas Salariales | Benchmarking.jsx, EquidadInterna.jsx, Compensations.jsx |
| `mv_sentiment_summary` | 🔴 3 | `m10_engagement.py` | Heatmap de Engagement | HeatmapEngagement.jsx |
| `mv_sst_incidents` | 🔴 2 | `m07_tiempo_bienestar.py` | Salud Ocupacional (SST), Índice de Bienestar & Burnout | SaludOcupacional.jsx |
| `mv_time_to_fill` | 🟢 683 | `m02_reclutamiento.py` | Calidad de Contratación | CalidadContratacion.jsx |
| `mv_training_roi` | 🔴 1 | `m09_talento_desarrollo.py` | ROI de Capacitación, Ejecución de L&D | RoiCapacitacion.jsx |
| `mv_turnover_analysis` | 🟢 4,500 | `m12_retencion.py` | Score Predictivo de Fuga, Benchmarking de Turnover | ScoreFuga.jsx, BenchmarkingTurnover.jsx |
| `mv_turnover_cost` | 🟢 2,250 | `m06_nomina_costos.py` | Impacto Financiero de Rotación | ImpactoFinanciero.jsx |
| `mv_ui_global_filters` | 🔴 1 | `m13_calidad_datos.py` | Diccionario de Datos | DiccionarioDatos.jsx |

---

## ⚪ Sección 4 — Submenús Sin Componente (Pendientes)

| Submenú | Módulo | ID Router | Acción Requerida |
|---------|--------|-----------|-----------------|
| Organigrama de Costos | M05 | org_costos | Crear OrgCostos.jsx usando mv_payroll_mass |
| Distribución Geográfica | M05 | distribucion-geografica | Crear componente usando mv_country_dist |
| Forecast de Dotación | M05 | forecast-dotacion | Crear MV predictiva en m05 + componente |

---
*Auto-generado: 2026-05-03 12:09 · Fuente: Supabase schema `business`*