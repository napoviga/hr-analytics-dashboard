# 📊 Módulo 01: Visión Ejecutiva - Plan Detallado

> **Script Python:** `m01_vision_ejecutiva.py`  
> **Prioridad:** ALTA  
> **Estado:** 🟡 Parcial (1/3 vistas implementadas)  
> **Dependencias:** m05_fuerza_laboral (MVs demográficas)  
> **Tags Metodológicos:** DESC, PRED, ML

---

## 🎯 Objetivo del Módulo

Proporcionar una visión estratégica de alto nivel para C-Level y directivos, consolidando KPIs críticos, detectando anomalías automáticamente y comparando métricas clave contra benchmarks de mercado.

**Usuarios objetivo:** CEO, CHRO, CFO, VP de RRHH, Directores de Negocio

**Frecuencia de actualización:** Diaria (MVs), Tiempo real (alerts)

---

## 📁 Fuentes de Datos

### Existentes (no requiere tablas nuevas)
- `business.v_employee_full_byNapo` → Datos base de empleados
- `business.mv_demographics_agg` → Agregados demográficos mensuales
- `business.mv_monthly_kpis_byNapo` → KPIs mensuales por país

### Nuevas (a crear en este módulo)
- **NO REQUIERE TABLAS RAW ADICIONALES** → Todo se deriva de datos existentes

---

## 🗂️ Vistas Detalladas

### 1. Dashboard C-Level ✅ IMPLEMENTADA

**Objeto:** `business.get_demographics_dashboard()` (Función RPC)

**Columnas de entrada (parámetros):**
| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| p_period_date | DATE | - | Fecha de corte para el dashboard |
| p_country | TEXT | NULL | Filtro por país (ISO3) |
| p_department | TEXT | NULL | Filtro por departamento |
| p_job_level_1 | TEXT | NULL | Filtro por nivel jerárquico 1 |
| p_job_level_2 | TEXT | NULL | Filtro por nivel jerárquico 2 |
| p_work_center | TEXT | NULL | Filtro por centro de trabajo |

**Estructura de salida (JSON):**
```json
{
  "total_activos_card": {
    "title": "FUERZA LABORAL",
    "current_month": "2026.03",
    "current_value": 4850,
    "previous_month": "2026.02",
    "previous_value": 4780,
    "diff_abs": 70,
    "diff_pct": 1.46,
    "yoy_month": "2025.03",
    "yoy_value": 4320,
    "yoy_diff_abs": 530,
    "yoy_diff_pct": 12.27,
    "sparkline_data": [
      {"label": "2025.10", "value": 4650},
      {"label": "2025.11", "value": 4690},
      {"label": "2025.12", "value": 4720},
      {"label": "2026.01", "value": 4750},
      {"label": "2026.02", "value": 4780},
      {"label": "2026.03", "value": 4850}
    ]
  },
  "altas_card": { ... estructura similar ... },
  "bajas_card": { ... estructura similar ... }
}
```

**Visualizaciones asociadas:**
- 3 KPI Cards (Fuerza Laboral, Altas, Bajas) con:
  - Valor actual vs mes anterior (diff absoluto y %)
  - Valor YoY (Year-over-Year)
  - Sparkline de últimos 6 meses
- Componente React: `Overview.jsx` (ya implementado)

**SQL de referencia:** Ya implementado en `m05_fuerza_laboral.py`

---

### 2. Alertas & Anomalías 🔘 PENDIENTE

**Objeto:** `business.mv_alerts_anomalies` (Materialized View)

**Propósito:** Detectar automáticamente desviaciones estadísticas significativas (Z-Score > 2) en métricas clave de RRHH.

**Columnas:**
| Columna | Tipo | Descripción | Ejemplo |
|---------|------|-------------|---------|
| snapshot_date | DATE | Fecha de corte | 2026-03-31 |
| country_iso3 | TEXT | Código ISO del país | PER, CHL, COL |
| department_name | TEXT | Departamento | IT, Sales, HR |
| metric_name | TEXT | Nombre de la métrica | turnover_rate, avg_salary |
| metric_value | NUMERIC | Valor observado | 3.5 |
| metric_avg | NUMERIC | Promedio histórico (últimos 12 meses) | 2.1 |
| metric_stddev | NUMERIC | Desviación estándar histórica | 0.4 |
| z_score | NUMERIC | Puntaje Z (desviaciones estándar) | 3.5 |
| status | TEXT | Estado de alerta | ALERTA, NORMAL |
| severity | TEXT | Severidad | CRÍTICA, MEDIA, BAJA |
| recommended_action | TEXT | Acción recomendada | Investigar rotación en IT |

**SQL de creación:**
```sql
CREATE MATERIALIZED VIEW business.mv_alerts_anomalies AS
WITH metricas_base AS (
    SELECT 
        snapshot_date,
        country_iso3,
        department_name,
        'turnover_rate' as metric_name,
        ROUND(COUNT(*) FILTER (WHERE termination_date BETWEEN DATE_TRUNC('month', snapshot_date) AND snapshot_date)::NUMERIC / 
              NULLIF(COUNT(*) FILTER (WHERE is_active_at_snapshot = TRUE OR termination_date BETWEEN DATE_TRUNC('month', snapshot_date) AND snapshot_date), 0) * 100, 2) as metric_value
    FROM business.v_employee_full_byNapo
    GROUP BY snapshot_date, country_iso3, department_name
    
    UNION ALL
    
    SELECT 
        snapshot_date,
        country_iso3,
        department_name,
        'avg_salary_usd' as metric_name,
        ROUND(AVG(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE), 2) as metric_value
    FROM business.v_employee_full_byNapo
    GROUP BY snapshot_date, country_iso3, department_name
    
    UNION ALL
    
    SELECT 
        snapshot_date,
        country_iso3,
        department_name,
        'headcount_growth' as metric_name,
        ROUND(COUNT(*) FILTER (WHERE is_active_at_snapshot = TRUE)::NUMERIC / 
              LAG(COUNT(*) FILTER (WHERE is_active_at_snapshot = TRUE)) OVER (PARTITION BY country_iso3, department_name ORDER BY snapshot_date) * 100 - 100, 2) as metric_value
    FROM business.v_employee_full_byNapo
    GROUP BY snapshot_date, country_iso3, department_name
),
estadisticas_historicas AS (
    SELECT 
        country_iso3,
        department_name,
        metric_name,
        AVG(metric_value) as metric_avg,
        STDDEV(metric_value) as metric_stddev
    FROM metricas_base
    WHERE snapshot_date >= (SELECT MAX(snapshot_date) - INTERVAL '12 months' FROM metricas_base)
    GROUP BY country_iso3, department_name, metric_name
)
SELECT 
    mb.snapshot_date,
    mb.country_iso3,
    mb.department_name,
    mb.metric_name,
    mb.metric_value,
    eh.metric_avg,
    eh.metric_stddev,
    ROUND((mb.metric_value - eh.metric_avg) / NULLIF(eh.metric_stddev, 0), 2) as z_score,
    CASE WHEN ABS((mb.metric_value - eh.metric_avg) / NULLIF(eh.metric_stddev, 0)) > 2 THEN 'ALERTA' ELSE 'NORMAL' END as status,
    CASE 
        WHEN ABS((mb.metric_value - eh.metric_avg) / NULLIF(eh.metric_stddev, 0)) > 3 THEN 'CRÍTICA'
        WHEN ABS((mb.metric_value - eh.metric_avg) / NULLIF(eh.metric_stddev, 0)) > 2 THEN 'MEDIA'
        ELSE 'BAJA'
    END as severity,
    CASE 
        WHEN mb.metric_name = 'turnover_rate' AND (mb.metric_value - eh.metric_avg) / eh.metric_stddev > 2 THEN 'Investigar causas de rotación inusual en ' || mb.department_name
        WHEN mb.metric_name = 'avg_salary_usd' AND (mb.metric_value - eh.metric_avg) / eh.metric_stddev < -2 THEN 'Revisar equidad salarial en ' || mb.department_name
        ELSE 'Monitorear continuamente'
    END as recommended_action
FROM metricas_base mb
JOIN estadisticas_historicas eh 
    ON mb.country_iso3 = eh.country_iso3 
    AND mb.department_name = eh.department_name 
    AND mb.metric_name = eh.metric_name
WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM metricas_base);

CREATE INDEX idx_mv_alerts_snap_m01 ON business.mv_alerts_anomalies (snapshot_date);
CREATE INDEX idx_mv_alerts_status_m01 ON business.mv_alerts_anomalies (status);
CREATE INDEX idx_mv_alerts_severity_m01 ON business.mv_alerts_anomalies (severity);
```

**Visualizaciones sugeridas:**
1. **Tabla de Alertas:** Listado filtrable por severidad (CRÍTICA, MEDIA, BAJA)
2. **Heatmap de Desviaciones:** Eje X = Departamentos, Eje Y = Métricas, Color = Z-Score
3. **Timeline de Alertas:** Línea de tiempo con eventos de alerta marcados

**Componente React a crear:** `AlertsAnomalies.jsx`

**RPC sugerida:**
```sql
CREATE OR REPLACE FUNCTION business.get_alerts_dashboard(
    p_period_date DATE,
    p_severity TEXT DEFAULT NULL
) RETURNS JSON AS $$
-- Retorna: alertas_agrupadas, top_5_metricas_anomalias, timeline_alertas
$$ LANGUAGE plpgsql;
```

---

### 3. Benchmarking de Mercado 🔘 PENDIENTE

**Objeto:** `business.mv_benchmarking_mercado` (Materialized View)

**Propósito:** Comparar métricas internas contra benchmarks externos de la industria.

**Fuente de datos externa:** CSV/JSON que debe cargarse periódicamente (ej: datos de Mercer, Willis Towers Watson, encuestas salariales)

**Columnas:**
| Columna | Tipo | Descripción | Ejemplo |
|---------|------|-------------|---------|
| benchmark_date | DATE | Fecha del benchmark | 2026-03-31 |
| metric_name | TEXT | Nombre de la métrica | avg_salary_it, turnover_rate_sales |
| our_company_value | NUMERIC | Nuestro valor | 4500 |
| market_avg | NUMERIC | Promedio de mercado | 4200 |
| market_p25 | NUMERIC | Percentil 25 mercado | 3800 |
| market_p75 | NUMERIC | Percentil 75 mercado | 4800 |
| percentile_rank | INTEGER | En qué percentil estamos | 65 |
| gap_vs_market | NUMERIC | Diferencia vs mercado (%) | 7.14 |
| status | TEXT | Estado | SUPERIOR, EN_PROMEDIO, INFERIOR |

**Datos de ejemplo (a cargar desde CSV externo):**
```csv
benchmark_date,metric_name,our_company_value,market_avg,market_p25,market_p75
2026-03-31,avg_salary_it_usd,4500,4200,3800,4800
2026-03-31,avg_salary_sales_usd,3200,3100,2800,3500
2026-03-31,turnover_rate_it_pct,2.1,2.5,1.8,3.2
2026-03-31,turnover_rate_sales_pct,3.8,3.2,2.5,4.0
2026-03-31,benefits_cost_pct,18.5,17.0,15.0,20.0
```

**SQL de creación:**
```sql
CREATE MATERIALIZED VIEW business.mv_benchmarking_mercado AS
SELECT 
    b.benchmark_date,
    b.metric_name,
    b.our_company_value,
    b.market_avg,
    b.market_p25,
    b.market_p75,
    -- Calcular percentile rank aproximado
    CASE 
        WHEN b.our_company_value <= b.market_p25 THEN 25
        WHEN b.our_company_value >= b.market_p75 THEN 75
        ELSE ROUND(25 + ((b.our_company_value - b.market_p25) / NULLIF(b.market_p75 - b.market_p25, 0)) * 50)::INTEGER
    END as percentile_rank,
    ROUND((b.our_company_value - b.market_avg) / NULLIF(b.market_avg, 0) * 100, 2) as gap_vs_market,
    CASE 
        WHEN b.our_company_value > b.market_p75 THEN 'SUPERIOR'
        WHEN b.our_company_value < b.market_p25 THEN 'INFERIOR'
        ELSE 'EN_PROMEDIO'
    END as status
FROM raw.benchmark_external b
WHERE b.benchmark_date = (SELECT MAX(benchmark_date) FROM raw.benchmark_external);

CREATE INDEX idx_mv_benchmark_date_m01 ON business.mv_benchmarking_mercado (benchmark_date);
CREATE INDEX idx_mv_benchmark_metric_m01 ON business.mv_benchmarking_mercado (metric_name);
```

**Nota:** Requiere crear tabla `raw.benchmark_external` para cargar datos externos.

**Visualizaciones sugeridas:**
1. **Radar Chart:** Comparación múltiple de métricas (nosotros vs mercado)
2. **Bullet Charts:** Cada métrica con rango P25-P75 y nuestra posición
3. **Tabla de Brechas:** Top 5 métricas donde estamos por encima/debajo del mercado

**Componente React a crear:** `Benchmarking.jsx`

---

## 🐍 Script Python: `m01_vision_ejecutiva.py`

### Estructura esperada:

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

def setup_vision_ejecutiva():
    start_time = time.time()
    print("\n" + "="*50)
    print("🧠 [ETL M01] CONFIGURANDO DOMINIO: VISIÓN EJECUTIVA")
    print("="*50)
    
    if not db_url:
        print("❌ Error: DATABASE_URL no encontrada en .env")
        return

    engine = create_engine(db_url)

    sql_views = """
    -- ==========================================
    -- 1. VISTAS DE ALERTAS Y ANOMALÍAS
    -- ==========================================
    DROP MATERIALIZED VIEW IF EXISTS business.mv_alerts_anomalies CASCADE;
    
    -- [INSERTAR SQL DE mv_alerts_anomalies aquí]
    
    -- ==========================================
    -- 2. VISTAS DE BENCHMARKING
    -- ==========================================
    DROP MATERIALIZED VIEW IF EXISTS business.mv_benchmarking_mercado CASCADE;
    
    -- [INSERTAR SQL DE mv_benchmarking_mercado aquí]
    
    -- Permisos
    GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
    """

    sql_rpcs = """
    -- ==========================================
    -- 3. FUNCIONES RPC PARA FRONTEND
    -- ==========================================
    DROP FUNCTION IF EXISTS business.get_alerts_dashboard(DATE, TEXT);
    
    CREATE OR REPLACE FUNCTION business.get_alerts_dashboard(
        p_period_date DATE,
        p_severity TEXT DEFAULT NULL
    ) RETURNS JSON AS $$
    DECLARE result JSON;
    BEGIN
        SELECT json_build_object(
            'alertas_agrupadas', (SELECT COALESCE(json_agg(t), '[]'::json) FROM (
                SELECT severity, COUNT(*) as count, array_agg(DISTINCT metric_name) as metrics
                FROM business.mv_alerts_anomalies
                WHERE snapshot_date = p_period_date
                  AND (p_severity IS NULL OR severity = p_severity)
                GROUP BY severity
            ) t),
            'top_5_metricas_anomalias', (SELECT COALESCE(json_agg(t), '[]'::json) FROM (
                SELECT metric_name, severity, z_score, recommended_action
                FROM business.mv_alerts_anomalies
                WHERE snapshot_date = p_period_date
                ORDER BY ABS(z_score) DESC
                LIMIT 5
            ) t),
            'timeline_alertas', (SELECT COALESCE(json_agg(t), '[]'::json) FROM (
                SELECT TO_CHAR(snapshot_date, 'YYYY.MM') as month_lbl, 
                       COUNT(*) FILTER (WHERE status = 'ALERTA') as alert_count
                FROM business.mv_alerts_anomalies
                WHERE snapshot_date >= (p_period_date - INTERVAL '12 months')
                GROUP BY snapshot_date
                ORDER BY snapshot_date
            ) t)
        ) INTO result;
        RETURN result;
    END;
    $$ LANGUAGE plpgsql;
    
    GRANT EXECUTE ON FUNCTION business.get_alerts_dashboard(DATE, TEXT) TO anon;
    """

    try:
        with engine.begin() as conn:
            print("⏳ Creando Vistas de Visión Ejecutiva (M01)...")
            conn.execute(text(sql_views))
            
            print("⏳ Creando Funciones RPC (M01)...")
            conn.execute(text(sql_rpcs))
            
            print("⏳ Refrescando Materialized Views...")
            conn.execute(text("REFRESH MATERIALIZED VIEW business.mv_alerts_anomalies;"))
            conn.execute(text("REFRESH MATERIALIZED VIEW business.mv_benchmarking_mercado;"))
            
        elapsed = time.time() - start_time
        print(f"\n✅ Módulo 01 completado en {elapsed:.2f} segundos")
        
    except Exception as e:
        print(f"\n❌ Error en Módulo 01: {str(e)}")
        raise

if __name__ == "__main__":
    setup_vision_ejecutiva()
```

---

## 📊 Resumen de Implementación

### Objetos a crear:
- [ ] 2 Materialized Views (`mv_alerts_anomalies`, `mv_benchmarking_mercado`)
- [ ] 1 Función RPC (`get_alerts_dashboard`)
- [ ] 1 Tabla RAW opcional (`benchmark_external` para datos de mercado)

### Componentes React a crear:
- [ ] `AlertsAnomalies.jsx`
- [ ] `Benchmarking.jsx`

### Archivos a modificar:
- [ ] `etl_pipeline/00_full_run_pipeline.py` → Agregar `m01_vision_ejecutiva.py`
- [ ] `client/src/App.jsx` → Registrar nuevas rutas
- [ ] `client/src/modules/01-vision-ejecutiva/` → Crear carpeta con componentes

### Estimación de esfuerzo:
- **Backend (SQL + Python):** 4-6 horas
- **Frontend (React + ECharts):** 6-8 horas
- **Testing + QA:** 2-3 horas
- **Total:** 12-17 horas (~1.5-2 días)

---

## 🔗 Dependencias Cruzadas

### Este módulo depende de:
- ✅ `business.v_employee_full_byNapo` (m05)
- ✅ `business.mv_demographics_agg` (m05)
- ✅ `business.mv_monthly_kpis_byNapo` (m05)

### Otros módulos dependen de este:
- 🔲 Módulo 12 (Retención) → Usará alertas de turnover anómalo
- 🔲 Módulo 06 (Nómina) → Usará benchmarking salarial

---

*Documento generado como parte del pipeline de documentación GDH Analytics*
