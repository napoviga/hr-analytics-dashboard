import os
import time
from pathlib import Path
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

ETL_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ETL_DIR.parent
load_dotenv(PROJECT_ROOT / ".env")
db_url = os.getenv("DATABASE_URL")

def run():
    start_time = time.time()
    print("\n" + "="*50)
    print("🚀 [ETL M01] VISIÓN EJECUTIVA")
    print("="*50)

    engine = create_engine(db_url)
    
    sql = """
    CREATE SCHEMA IF NOT EXISTS business;

    -- ═══ MV: Alertas & Anomalías (Z-Score) ═══
    DROP MATERIALIZED VIEW IF EXISTS business.mv_alerts_anomalies CASCADE;
    CREATE MATERIALIZED VIEW business.mv_alerts_anomalies AS
    WITH metricas AS (
        SELECT snapshot_date, country_iso3, department_name,
            COUNT(*) FILTER (WHERE is_active_at_snapshot) as headcount,
            COUNT(*) FILTER (WHERE termination_date BETWEEN DATE_TRUNC('month', snapshot_date) AND snapshot_date) as bajas
        FROM business.v_employee_full_byNapo
        GROUP BY snapshot_date, country_iso3, department_name
    ),
    con_stats AS (
        SELECT *, 
            AVG(headcount) OVER w as avg_hc, STDDEV(headcount) OVER w as std_hc,
            AVG(bajas) OVER w as avg_bajas, STDDEV(bajas) OVER w as std_bajas,
            LAG(headcount) OVER w as prev_headcount
        FROM metricas
        WINDOW w AS (PARTITION BY country_iso3, department_name ORDER BY snapshot_date)
    )
    SELECT snapshot_date, country_iso3, department_name,
        headcount, bajas, prev_headcount,
        ROUND(((headcount - avg_hc) / NULLIF(std_hc, 0))::NUMERIC, 2) as z_score_hc,
        ROUND(((bajas - avg_bajas) / NULLIF(std_bajas, 0))::NUMERIC, 2) as z_score_bajas,
        CASE WHEN ABS((headcount - avg_hc) / NULLIF(std_hc,0)) > 2 THEN 'ALERTA'
             WHEN ABS((headcount - avg_hc) / NULLIF(std_hc,0)) > 1.5 THEN 'ATENCION'
             ELSE 'NORMAL' END as status_hc,
        CASE WHEN ABS((bajas - avg_bajas) / NULLIF(std_bajas,0)) > 2 THEN 'ALERTA'
             WHEN ABS((bajas - avg_bajas) / NULLIF(std_bajas,0)) > 1.5 THEN 'ATENCION'
             ELSE 'NORMAL' END as status_bajas
    FROM con_stats;

    CREATE INDEX IF NOT EXISTS idx_mv_alerts_snap ON business.mv_alerts_anomalies(snapshot_date);
    GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
    """

    with engine.begin() as conn:
        print("⏳ Creando MV: Alertas & Anomalías...")
        conn.execute(text(sql))
        
        print("🔄 Refrescando vistas...")
        conn.execute(text("REFRESH MATERIALIZED VIEW business.mv_alerts_anomalies;"))
        
        print("📡 Notificando a PostgREST para recargar schema...")
        conn.execute(text("NOTIFY pgrst, 'reload schema';"))
        
    elapsed = time.time() - start_time
    print(f"\n✅ ETL M01 completado exitosamente en {elapsed:.2f} segundos.")
    print("="*50 + "\n")

if __name__ == "__main__":
    run()
