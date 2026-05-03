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
    print("🚀 [ETL M13] CALIDAD DE DATOS")
    print("="*50)

    engine = create_engine(db_url)
    
    sql = """
    CREATE SCHEMA IF NOT EXISTS business;

    -- ═══ Vista: Métricas de calidad ═══
    CREATE OR REPLACE VIEW business.v_data_quality_metrics AS
    SELECT 
        'v_employee_full_byNapo' as source_table,
        COUNT(*) as total_records,
        COUNT(DISTINCT employee_id) as unique_employees,
        COUNT(DISTINCT snapshot_date) as total_snapshots,
        ROUND((100.0 * COUNT(monthly_salary_usd) / NULLIF(COUNT(*),0))::NUMERIC, 2) as completeness_salary,
        ROUND((100.0 * COUNT(manager_employee_id) / NULLIF(COUNT(*),0))::NUMERIC, 2) as completeness_manager,
        ROUND((100.0 * COUNT(country_iso3) / NULLIF(COUNT(*),0))::NUMERIC, 2) as completeness_country
    FROM business.v_employee_full_byNapo;

    GRANT SELECT ON business.v_data_quality_metrics TO anon;
    """

    with engine.begin() as conn:
        print("⏳ Creando Vista: Métricas de calidad...")
        conn.execute(text(sql))
        
        print("📡 Notificando a PostgREST para recargar schema...")
        conn.execute(text("NOTIFY pgrst, 'reload schema';"))
        
    elapsed = time.time() - start_time
    print(f"\n✅ ETL M13 completado exitosamente en {elapsed:.2f} segundos.")
    print("="*50 + "\n")

if __name__ == "__main__":
    run()
