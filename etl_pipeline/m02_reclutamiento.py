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
    print("🚀 [ETL M02] RECLUTAMIENTO & SELECCIÓN")
    print("="*50)

    engine = create_engine(db_url)
    
    sql = """
    CREATE SCHEMA IF NOT EXISTS business;

    -- ═══ MV: Funnel de Reclutamiento ═══
    DROP MATERIALIZED VIEW IF EXISTS business.mv_recruitment_funnel CASCADE;
    CREATE MATERIALIZED VIEW business.mv_recruitment_funnel AS
    SELECT 
        DATE_TRUNC('month', j.posting_date::DATE)::DATE as periodo,
        j.department_name, j.country_iso3,
        COUNT(DISTINCT p.candidate_id) FILTER (WHERE p.stage IN ('Applied','Screening','Interview','Offer','Hired')) as applied,
        COUNT(DISTINCT p.candidate_id) FILTER (WHERE p.stage IN ('Screening','Interview','Offer','Hired')) as screened,
        COUNT(DISTINCT p.candidate_id) FILTER (WHERE p.stage IN ('Interview','Offer','Hired')) as interviewed,
        COUNT(DISTINCT p.candidate_id) FILTER (WHERE p.stage IN ('Offer','Hired')) as offered,
        COUNT(DISTINCT p.candidate_id) FILTER (WHERE p.stage = 'Hired') as hired,
        ROUND(AVG(p.interview_score::NUMERIC) FILTER (WHERE p.interview_score IS NOT NULL), 2) as avg_interview_score,
        ROUND(AVG(p.nps_score::NUMERIC) FILTER (WHERE p.nps_score IS NOT NULL), 2) as avg_nps
    FROM raw."recruitment_pipeline_byNapo" p
    JOIN raw."job_postings_byNapo" j ON p.posting_id = j.posting_id
    GROUP BY 1, j.department_name, j.country_iso3;

    CREATE INDEX IF NOT EXISTS idx_mv_recruit_periodo ON business.mv_recruitment_funnel(periodo);

    -- ═══ MV: Tiempo de Cobertura ═══
    DROP MATERIALIZED VIEW IF EXISTS business.mv_time_to_fill CASCADE;
    CREATE MATERIALIZED VIEW business.mv_time_to_fill AS
    SELECT 
        j.department_name, j.country_iso3,
        DATE_TRUNC('month', j.posting_date::DATE)::DATE as periodo,
        ROUND(AVG(j.closing_date::DATE - j.posting_date::DATE), 2) as avg_days_to_fill,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY j.closing_date::DATE - j.posting_date::DATE) as median_days,
        COUNT(*) as total_postings
    FROM raw."job_postings_byNapo" j
    WHERE j.status = 'Closed'
    GROUP BY j.department_name, j.country_iso3, 3;

    CREATE INDEX IF NOT EXISTS idx_mv_ttf_periodo ON business.mv_time_to_fill(periodo);
    GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
    """

    with engine.begin() as conn:
        print("⏳ Creando MVs de Reclutamiento...")
        conn.execute(text(sql))
        
        print("📡 Notificando a PostgREST para recargar schema...")
        conn.execute(text("NOTIFY pgrst, 'reload schema';"))
        
    elapsed = time.time() - start_time
    print(f"\n✅ ETL M02 completado exitosamente en {elapsed:.2f} segundos.")
    print("="*50 + "\n")

if __name__ == "__main__":
    run()
