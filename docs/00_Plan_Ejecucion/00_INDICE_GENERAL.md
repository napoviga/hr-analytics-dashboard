# 📋 Plan Maestro de Ejecución - GDH Analytics Pipeline

> **Fecha de creación:** 2026-04-11  
> **Última actualización:** 2026-04-11  
> **Propósito:** Guía detallada de implementación del pipeline ETL modular para los 13 módulos del dashboard GDH Analytics  
> **Estado del proyecto:** 🟡 En desarrollo activo (17% completitud - 9/52 vistas implementadas)

---

## 🎯 Visión General del Pipeline

### Arquitectura Modular

El pipeline sigue una arquitectura modular donde cada módulo es independiente pero puede depender de infraestructura común creada en módulos anteriores:

```
┌─────────────────────────────────────────────────────────────────┐
│                    PIPELINE ETL - SECUENCIA DE EJECUCIÓN        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FASE 0: INFRAESTRUCTURA BASE (Scripts 00-04)                  │
│  ├── 00_full_run_pipeline.py      → Orquestador principal      │
│  ├── 01_generate_synthetic_data.py → Generación datos sintéticos│
│  ├── 02_setup_raw_layer.py         → Tablas RAW (Bronce)       │
│  ├── 03_ingest_data.py             → Carga CSV → RAW           │
│  └── 04_setup_business_core.py     → Vistas BUSINESS (Silver)  │
│                                                                 │
│  FASE 1: MÓDULOS FUNCIONALES (Scripts m01-m13)                 │
│  ├── m05_fuerza_laboral.py        → ✅ COMPLETO (6/6 vistas)   │
│  ├── m06_nomina_costos.py         → 🟡 PARCIAL (1/6 vistas)    │
│  ├── m01_vision_ejecutiva.py      → 🔘 PENDIENTE               │
│  ├── m02_reclutamiento.py         → 🔘 PENDIENTE               │
│  ├── m03_onboarding.py            → 🔘 PENDIENTE               │
│  ├── m04_ciclo_vida.py            → 🔘 PENDIENTE               │
│  ├── m07_tiempo_bienestar.py      → 🔘 PENDIENTE               │
│  ├── m08_desempeno.py             → 🔘 PENDIENTE               │
│  ├── m09_talento_desarrollo.py    → 🔘 PENDIENTE               │
│  ├── m10_engagement.py            → 🔘 PENDIENTE               │
│  ├── m11_compliance.py            → 🔘 PENDIENTE               │
│  ├── m12_retencion.py             → 🔘 PENDIENTE               │
│  └── m13_calidad_datos.py         → 🟡 PARCIAL (1/3 vistas)    │
│                                                                 │
│  FASE 2: POST-PROCESAMIENTO (Scripts 90-91)                    │
│  ├── 90_generate_data_inventory.py → Inventario de metadata    │
│  └── 91_export_data_samples.py     → Exportación muestras docs │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Dependencias entre Módulos

| Módulo | Depende de | Puede ejecutarse sin |
|--------|-----------|---------------------|
| m01 | m05 (MVs demográficas) | m06-m13 |
| m02 | m05 (empleados activos) | m03, m04, m06-m13 |
| m03 | m02 (hire_date), m05 | m04, m06-m13 |
| m04 | m05 + todos los módulos anteriores | m06-m13 |
| m05 | m04 (business core) | NINGUNO modular (es base) |
| m06 | m05 (salary data) | m07-m13 |
| m07 | m05 (employee_id) | m08-m13 |
| m08 | m05, m07 (attendance) | m09-m13 |
| m09 | m05, m08 (performance) | m10-m13 |
| m10 | m05 (survey responses) | m11-m13 |
| m11 | m05 (compliance data) | m12-m13 |
| m12 | m05, m08, m10 (ml features) | m13 |
| m13 | TODOS (auditoría transversal) | NINGUNO |

---

## 📊 Estado de Implementación por Módulo

### Resumen Ejecutivo

| # | Módulo | Script Python | Vistas Totales | Implementadas | % Completitud | Prioridad | Estado |
|---|--------|--------------|----------------|---------------|---------------|-----------|--------|
| 01 | Visión Ejecutiva | `m01_vision_ejecutiva.py` | 3 | 1 | 33% | ALTA | 🟡 Parcial |
| 02 | Reclutamiento & Selección | `m02_reclutamiento.py` | 5 | 0 | 0% | MEDIA | 🔘 Pendiente |
| 03 | Onboarding & Integración | `m03_onboarding.py` | 3 | 0 | 0% | MEDIA | 🔘 Pendiente |
| 04 | Análisis de Ciclo de Vida | `m04_ciclo_vida.py` | 3 | 0 | 0% | BAJA | 🔘 Pendiente |
| 05 | Fuerza Laboral & Estructura | `m05_fuerza_laboral.py` | 6 | 6 | ✅ 100% | ✅ COMPLETO | ✅ Completo |
| 06 | Nómina, Costos & Equity | `m06_nomina_costos.py` | 6 | 1 | 17% | ALTA | 🟡 Parcial |
| 07 | Tiempo, Asistencia & Bienestar | `m07_tiempo_bienestar.py` | 6 | 0 | 0% | MEDIA | 🔘 Pendiente |
| 08 | Gestión del Desempeño | `m08_desempeno.py` | 4 | 0 | 0% | MEDIA | 🔘 Pendiente |
| 09 | Talento & Desarrollo | `m09_talento_desarrollo.py` | 5 | 0 | 0% | BAJA | 🔘 Pendiente |
| 10 | Engagement & Sentimiento | `m10_engagement.py` | 3 | 0 | 0% | BAJA | 🔘 Pendiente |
| 11 | Compliance & Relaciones Laborales | `m11_compliance.py` | 2 | 0 | 0% | BAJA | 🔘 Pendiente |
| 12 | Retención & Riesgo de Fuga | `m12_retencion.py` | 3 | 0 | 0% | MEDIA | 🔘 Pendiente |
| 13 | Calidad de Datos | `m13_calidad_datos.py` | 3 | 1 | 33% | BAJA | 🟡 Parcial |
| **TOTAL** | **13 Módulos** | **13 scripts** | **52** | **9** | **17%** | - | - |

---

## 🗺️ Documentos Detallados por Módulo

Cada módulo tiene su propio documento detallado en esta carpeta:

| Documento | Módulo | Contenido |
|-----------|--------|-----------|
| [MODULO_01_VISION_EJECUTIVA.md](./MODULO_01_VISION_EJECUTIVA.md) | 01 | Dashboard C-Level, Alertas, Benchmarking |
| [MODULO_02_RECLUTAMIENTO.md](./MODULO_02_RECLUTAMIENTO.md) | 02 | Eficiencia, Calidad, Fit Score, Bias Audit |
| [MODULO_03_ONBOARDING.md](./MODULO_03_ONBOARDING.md) | 03 | Onboarding Activo, Time to Productivity, Early Turnover |
| [MODULO_04_CICLO_VIDA.md](./MODULO_04_CICLO_VIDA.md) | 04 | Clústeres, Causalidad, Momentos Críticos |
| [MODULO_05_FUERZA_LABORAL.md](./MODULO_05_FUERZA_LABORAL.md) | 05 | ✅ COMPLETO - Demografía, Organigrama, Forecast |
| [MODULO_06_NOMINA_COSTOS.md](./MODULO_06_NOMINA_COSTOS.md) | 06 | Bandas Salariales, Compa-Ratio, Impacto Rotación |
| [MODULO_07_TIEMPO_BIENESTAR.md](./MODULO_07_TIEMPO_BIENESTAR.md) | 07 | Ausentismo, Horas Extra, SST, Wellbeing |
| [MODULO_08_DESEMPENO.md](./MODULO_08_DESEMPENO.md) | 08 | 360°, OKRs, PIPs, Top Performers |
| [MODULO_09_TALENTO DesarrOLLO.md](./MODULO_09_TALENTO DesarrOLLO.md) | 09 | 9-Box, Sucesión, Movilidad, L&D, ROI |
| [MODULO_10_ENGAGEMENT.md](./MODULO_10_ENGAGEMENT.md) | 10 | eNPS, Heatmap, DEI |
| [MODULO_11_COMPLIANCE.md](./MODULO_11_COMPLIANCE.md) | 11 | Cumplimiento, Relaciones Sindicales |
| [MODULO_12_RETENCION.md](./MODULO_12_RETENCION.md) | 12 | Churn Prediction, Benchmarking, Manager Correlation |
| [MODULO_13_CALIDAD_DATOS.md](./MODULO_13_CALIDAD_DATOS.md) | 13 | Auditoría, Log, Diccionario de Datos |

---

## 🔄 Ruta Crítica de Implementación

### Fase 1: ✅ COMPLETADA
- **Objetivo:** Establecer infraestructura base y módulo fundamental
- **Scripts:** 00-05
- **Entregables:** Datos sintéticos, tablas RAW, vistas BUSINESS, módulo 05 completo
- **Estado:** ✅ 100% completado

### Fase 2: 🔄 EN CURSO (Prioridad Actual)
- **Objetivo:** Completar visión ejecutiva y compensaciones
- **Scripts:** m06, m01
- **Entregables:** 
  - `m06_nomina_costos.py` (5 MVs faltantes + RPCs)
  - `m01_vision_ejecutiva.py` (2 MVs de alertas y benchmarking)
- **Estado:** 🟡 25% completado (1/4 vistas)
- **Tiempo estimado:** 2-3 días

### Fase 3: Operaciones RRHH (Próxima)
- **Objetivo:** Cubrir procesos operativos de RRHH
- **Scripts:** m02, m03, m07
- **Entregables:** 14 vistas nuevas + 4 tablas RAW adicionales
- **Tiempo estimado:** 5-7 días

### Fase 4: Talento y Desempeño
- **Objetivo:** Gestión del desempeño y desarrollo de talento
- **Scripts:** m08, m09, m04
- **Entregables:** 12 vistas nuevas + 5 tablas RAW adicionales
- **Tiempo estimado:** 5-7 días

### Fase 5: Advanced Analytics
- **Objetivo:** ML, NLP, optimización y calidad de datos
- **Scripts:** m10, m11, m12, m13
- **Entregables:** 11 vistas nuevas + 3 tablas RAW adicionales
- **Tiempo estimado:** 7-10 días (incluye modelos ML)

---

## 📝 Convenciones de Nomenclatura

### Scripts Python
```
m{NN}_{dominio}.py
Ejemplo: m05_fuerza_laboral.py, m06_nomina_costos.py
```

### Tablas RAW
```
raw.{nombre_tabla}
Ejemplo: raw.job_postings, raw.attendance_records
```

### Vistas BUSINESS
```
business.v_{nombre_vista}          → Vistas simples
business.mv_{nombre_mv}            → Materialized Views
business.get_{nombre_funcion}()    → Funciones RPC
```

### Componentes React
```
{NombreDominio}.jsx
Ejemplo: Demographics.jsx, Compensations.jsx, RecruitmentEfficiency.jsx
```

### Rutas en Frontend
```
/modules/{NN}-{dominio}/{Componente}.jsx
Ejemplo: /modules/05-fuerza-laboral/Demographics.jsx
```

---

## 🧠 Patrones de Diseño del Pipeline

### 1. Patrón de Transformación en Capas
```python
# Todos los scripts siguen este patrón:
def setup_{modulo}():
    # 1. Conexión a DB
    engine = create_engine(db_url)
    
    # 2. DROP de objetos existentes (idempotencia)
    DROP VIEW IF EXISTS business.mv_xxx CASCADE;
    
    # 3. CREATE de vistas/MVs
    CREATE MATERIALIZED VIEW business.mv_xxx AS ...
    
    # 4. CREATE de índices
    CREATE INDEX idx_mv_xxx ON business.mv_xxx (columna);
    
    # 5. CREATE de funciones RPC
    CREATE OR REPLACE FUNCTION business.get_xxx() RETURNS JSON AS $$ ...
    
    # 6. GRANT de permisos
    GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
    GRANT EXECUTE ON FUNCTION business.get_xxx() TO anon;
    
    # 7. REFRESH de MVs
    REFRESH MATERIALIZED VIEW business.mv_xxx;
```

### 2. Patrón de RPC para Frontend
```sql
-- Todas las funciones RPC retornan JSON para consumo directo del frontend
CREATE OR REPLACE FUNCTION business.get_{vista}(
    p_period_date DATE,
    p_country TEXT DEFAULT NULL,
    p_department TEXT DEFAULT NULL,
    -- ... más filtros universales
) RETURNS JSON AS $$
DECLARE result JSON;
BEGIN
    SELECT json_build_object(
        'serie_datos', (SELECT COALESCE(json_agg(t), '[]'::json) FROM (...) t),
        'kpi_principal', (SELECT json_build_object(...) FROM ...)
    ) INTO result;
    RETURN result;
END;
$$ LANGUAGE plpgsql;
```

### 3. Patrón de Filtros Universales
Todos los módulos soportan estos 6 filtros:
- `p_country` → country_iso3 (TEXT)
- `p_department` → department_name (TEXT)
- `p_job_level_1` → job_level_1 (TEXT)
- `p_job_level_2` → job_level_2 (TEXT)
- `p_work_center` → work_center_id (TEXT)
- `p_period_date` → snapshot_date (DATE)

---

## 📈 Métricas de Progreso

### Por Tipo de Objeto

| Tipo de Objeto | Total Esperado | Creados | Pendientes | % |
|---------------|----------------|---------|------------|---|
| Scripts Python | 13 | 1 (m05) + 2 parciales | 10 | 23% |
| Tablas RAW nuevas | 15 | 2 (base) | 13 | 13% |
| Vistas/MVs | 43 | 9 | 34 | 21% |
| Funciones RPC | 20 | 2 | 18 | 10% |
| Componentes React | 40+ | 6 | 34+ | 15% |

### Por Complejidad Técnica

| Nivel | Vistas Totales | Implementadas | % |
|-------|---------------|---------------|---|
| Baja (DESC puro) | 25 | 7 | 28% |
| Media (PRED, agregaciones) | 18 | 2 | 11% |
| Alta (ML, NLP, OPT) | 9 | 0 | 0% |

---

## 🚀 Próximos Pasos Inmediatos

### Esta Semana (Sprint 1)
1. ✅ Revisar y aprobar este plan maestro
2. 🔲 Crear `m06_nomina_costos.py` con 5 MVs faltantes:
   - `mv_salary_bands`
   - `mv_compa_ratio`
   - `mv_payroll_mass`
   - `mv_turnover_financial_impact`
   - `mv_salary_simulator`
3. 🔲 Crear componentes React para Módulo 06:
   - `SalaryBands.jsx`
   - `CompaRatio.jsx`
   - `PayrollMass.jsx`
   - `TurnoverImpact.jsx`
   - `SalarySimulator.jsx`

### Próxima Semana (Sprint 2)
1. 🔲 Completar Módulo 01 con alertas y benchmarking
2. 🔲 Iniciar Módulo 02 (Reclutamiento) con tablas RAW nuevas
3. 🔲 Conectar `OrganigramaIntegral.jsx` a `v_org_tree_byNapo`

---

## 📞 Soporte y Contacto

Para dudas sobre la implementación de algún módulo específico, revisar el documento detallado correspondiente en esta carpeta.

**Documentación adicional:**
- Especificaciones de navegación: `/docs/01-product-specs/01_navigation_sitemap.md`
- Lógica de vistas: `/docs/01-product-specs/02_view_logic_specs.md`
- Design system: `/docs/01-product-specs/03_design_system.md`
- Plan de conversión original: `/docs/01-product-specs/PLAN_CONVERSION_DATOS.md`

---

*Documento generado automáticamente como parte del pipeline de documentación GDH Analytics*
