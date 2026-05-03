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
    print("🚀 [ETL M04] CICLO DE VIDA & CLÚSTERES")
    print("="*50)

    engine = create_engine(db_url)
    
    sql = """
    CREATE SCHEMA IF NOT EXISTS business;

    -- ═══ MV: Cohortes por antigüedad ═══
    DROP MATERIALIZED VIEW IF EXISTS business.mv_lifecycle_cohorts CASCADE;
    CREATE MATERIALIZED VIEW business.mv_lifecycle_cohorts AS
    SELECT 
        snapshot_date, 
        CASE 
            WHEN tenure_months < 6 THEN '0-6 meses'
            WHEN tenure_months < 12 THEN '6-12 meses'
            WHEN tenure_months < 24 THEN '1-2 años'
            WHEN tenure_months < 48 THEN '2-4 años'
            ELSE '4+ años'
        END as tenure_cohort,
        department_name, country_iso3, job_level_1,
        COUNT(*) FILTER (WHERE is_active_at_snapshot) as activos,
        COUNT(*) FILTER (WHERE NOT is_active_at_snapshot) as bajas,
        ROUND((AVG(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot))::NUMERIC, 2) as avg_salary,
        ROUND((100.0 * COUNT(*) FILTER (WHERE NOT is_active_at_snapshot) / NULLIF(COUNT(*),0))::NUMERIC, 1) as tasa_rotacion
    FROM business.v_employee_full_byNapo
    GROUP BY snapshot_date, 2, department_name, country_iso3, job_level_1;

    -- ═══ MV: Momentos Críticos (hazard points) ═══
    DROP MATERIALIZED VIEW IF EXISTS business.mv_critical_moments CASCADE;
    CREATE MATERIALIZED VIEW business.mv_critical_moments AS
    SELECT 
        FLOOR(tenure_months / 3) * 3 as tenure_quarter,
        COUNT(*) FILTER (WHERE NOT is_active_at_snapshot) as exits_at_point,
        COUNT(*) as total_at_point,
        ROUND((100.0 * COUNT(*) FILTER (WHERE NOT is_active_at_snapshot) / NULLIF(COUNT(*),0))::NUMERIC, 2) as hazard_rate
    FROM business.v_employee_full_byNapo
    WHERE tenure_months IS NOT NULL
    GROUP BY 1;

    CREATE INDEX IF NOT EXISTS idx_mv_lc_snap ON business.mv_lifecycle_cohorts(snapshot_date);
    GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
    """

    with engine.begin() as conn:
        print("⏳ Creando MVs de Ciclo de Vida...")
        conn.execute(text(sql))
        
        print("📡 Notificando a PostgREST para recargar schema...")
        conn.execute(text("NOTIFY pgrst, 'reload schema';"))
        
    elapsed = time.time() - start_time
    print(f"\n✅ ETL M04 completado exitosamente en {elapsed:.2f} segundos.")
    print("="*50 + "\n")

if __name__ == "__main__":
    run()
