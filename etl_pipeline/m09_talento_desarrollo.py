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
    print("🚀 [ETL M09] TALENTO & DESARROLLO")
    print("="*50)

    engine = create_engine(db_url)
    
    sql = """
    CREATE SCHEMA IF NOT EXISTS business;

    -- ═══ MV: Nine Box ═══
    DROP MATERIALIZED VIEW IF EXISTS business.mv_nine_box CASCADE;
    CREATE MATERIALIZED VIEW business.mv_nine_box AS
    SELECT n.box_category as nine_box_quadrant, e.department_name,
        COUNT(*) as employee_count,
        ROUND((AVG(n.performance_rating::NUMERIC))::NUMERIC, 1) as avg_performance,
        ROUND((AVG(n.potential_rating::NUMERIC))::NUMERIC, 1) as avg_potential
    FROM raw."nine_box_grid_byNapo" n
    JOIN business.v_employee_full_byNapo e ON n.employee_id = e.employee_id::TEXT AND e.is_active_at_snapshot = TRUE
    GROUP BY n.box_category, e.department_name;

    -- ═══ MV: Training ROI ═══
    DROP MATERIALIZED VIEW IF EXISTS business.mv_training_roi CASCADE;
    CREATE MATERIALIZED VIEW business.mv_training_roi AS
    SELECT c.category, c.course_name as program_name,
        COUNT(e.enrollment_id) as enrolled,
        COUNT(e.enrollment_id) FILTER (WHERE e.status = 'Completed') as completed,
        ROUND((100.0 * COUNT(e.enrollment_id) FILTER (WHERE e.status = 'Completed') / NULLIF(COUNT(e.enrollment_id), 0))::NUMERIC, 1) as completion_rate,
        ROUND((AVG(e.score::NUMERIC))::NUMERIC, 1) as avg_post_training_score,
        SUM(c.cost_usd::NUMERIC) as costo_total
    FROM raw."training_courses_byNapo" c
    LEFT JOIN raw."training_enrollments_byNapo" e ON c.course_id = e.course_id
    GROUP BY c.category, c.course_name;

    GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
    """

    with engine.begin() as conn:
        print("⏳ Creando MVs de Talento y Desarrollo...")
        conn.execute(text(sql))
        conn.execute(text("NOTIFY pgrst, 'reload schema';"))
        
    elapsed = time.time() - start_time
    print(f"\n✅ ETL M09 completado exitosamente en {elapsed:.2f} segundos.")

if __name__ == "__main__":
    run()
