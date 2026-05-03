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
    print("🚀 [ETL M03] ONBOARDING & INTEGRACIÓN")
    print("="*50)

    engine = create_engine(db_url)
    
    sql = """
    CREATE SCHEMA IF NOT EXISTS business;

    -- ═══ MV: Estado de Onboarding ═══
    DROP MATERIALIZED VIEW IF EXISTS business.mv_onboarding_status CASCADE;
    CREATE MATERIALIZED VIEW business.mv_onboarding_status AS
    SELECT 
        e.snapshot_date, e.department_name, e.country_iso3,
        COUNT(DISTINCT o.employee_id) as total_procesos,
        COUNT(DISTINCT o.employee_id) FILTER (WHERE o.status = 'Completed') as completados,
        COUNT(DISTINCT o.employee_id) FILTER (WHERE o.status = 'Overdue') as vencidos,
        ROUND((AVG(CASE WHEN o.status='Completed' THEN 1 ELSE 0 END) * 100)::NUMERIC, 1) as pct_completado
    FROM business.v_employee_full_byNapo e
    JOIN raw."onboarding_checklist_byNapo" o ON e.employee_id::TEXT = o.employee_id
    WHERE e.is_active_at_snapshot AND e.tenure_months <= 3
    GROUP BY e.snapshot_date, e.department_name, e.country_iso3;

    -- ═══ MV: Rotación Temprana (<90 días) ═══
    DROP MATERIALIZED VIEW IF EXISTS business.mv_early_turnover CASCADE;
    CREATE MATERIALIZED VIEW business.mv_early_turnover AS
    SELECT 
        snapshot_date, department_name, country_iso3,
        COUNT(*) FILTER (WHERE NOT is_active_at_snapshot AND tenure_months < 3) as bajas_tempranas,
        COUNT(*) FILTER (WHERE tenure_months < 3) as total_nuevos,
        ROUND((100.0 * COUNT(*) FILTER (WHERE NOT is_active_at_snapshot AND tenure_months < 3) 
            / NULLIF(COUNT(*) FILTER (WHERE tenure_months < 3), 0))::NUMERIC, 1) as tasa_rotacion_temprana
    FROM business.v_employee_full_byNapo
    GROUP BY snapshot_date, department_name, country_iso3;

    CREATE INDEX IF NOT EXISTS idx_mv_onb_snap ON business.mv_onboarding_status(snapshot_date);
    CREATE INDEX IF NOT EXISTS idx_mv_early_snap ON business.mv_early_turnover(snapshot_date);
    GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
    """

    with engine.begin() as conn:
        print("⏳ Creando MVs de Onboarding...")
        conn.execute(text(sql))
        
        print("📡 Notificando a PostgREST para recargar schema...")
        conn.execute(text("NOTIFY pgrst, 'reload schema';"))
        
    elapsed = time.time() - start_time
    print(f"\n✅ ETL M03 completado exitosamente en {elapsed:.2f} segundos.")
    print("="*50 + "\n")

if __name__ == "__main__":
    run()
