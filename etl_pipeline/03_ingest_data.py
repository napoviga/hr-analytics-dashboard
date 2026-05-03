import pandas as pd
import os
import time
from pathlib import Path
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Resolver ruta absoluta al .env
ETL_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ETL_DIR.parent
env_path = PROJECT_ROOT / ".env"
load_dotenv(env_path)
db_url = os.getenv("DATABASE_URL")

def ingest_enhanced_data():
    start_time = time.time()
    print("\n" + "="*50)
    print("📥 [ETL 03] INGESTA DE DATOS (byNapo)")
    print("="*50)
    
    engine = create_engine(db_url)
    data_dir = "../data/"
    
    # FIX: ¡Descomentamos la tabla maestra para que suba a la BD!
    files_to_ingest = {
        "ibm_hr_monthly_snapshot_byNapo.csv": "raw.ibm_hr_monthly_snapshot_byNapo",
        "ibm_hr_change_reasons_byNapo.csv": "raw.ibm_hr_change_reasons_byNapo",
        "job_postings_byNapo.csv": "raw.job_postings_byNapo",
        "recruitment_pipeline_byNapo.csv": "raw.recruitment_pipeline_byNapo",
        "onboarding_checklist_byNapo.csv": "raw.onboarding_checklist_byNapo",
        "productivity_milestones_byNapo.csv": "raw.productivity_milestones_byNapo",
        "attendance_records_byNapo.csv": "raw.attendance_records_byNapo",
        "overtime_logs_byNapo.csv": "raw.overtime_logs_byNapo",
        "leave_requests_byNapo.csv": "raw.leave_requests_byNapo",
        "incidents_sst_byNapo.csv": "raw.incidents_sst_byNapo",
        "performance_reviews_byNapo.csv": "raw.performance_reviews_byNapo",
        "goals_okrs_byNapo.csv": "raw.goals_okrs_byNapo",
        "continuous_feedback_byNapo.csv": "raw.continuous_feedback_byNapo",
        "training_courses_byNapo.csv": "raw.training_courses_byNapo",
        "training_enrollments_byNapo.csv": "raw.training_enrollments_byNapo",
        "succession_plans_byNapo.csv": "raw.succession_plans_byNapo",
        "nine_box_grid_byNapo.csv": "raw.nine_box_grid_byNapo",
        "survey_responses_byNapo.csv": "raw.survey_responses_byNapo",
        "feedback_comments_byNapo.csv": "raw.feedback_comments_byNapo",
        "compliance_obligations_byNapo.csv": "raw.compliance_obligations_byNapo",
        "union_agreements_byNapo.csv": "raw.union_agreements_byNapo"
    }
    
    for filename, table_name in files_to_ingest.items():
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            df = pd.read_csv(filepath, dtype=str)
            df.columns = [col.strip().lower() for col in df.columns]
            df = df.where(df.notna(), None)
            
            print(f"⏳ Subiendo lote de [{len(df):,}] registros a [{table_name}]...")
            try:
                df.to_sql(
                    name=table_name.split('.')[1],
                    schema=table_name.split('.')[0],
                    con=engine,
                    if_exists='append',
                    index=False,
                    chunksize=1000
                )
                print(f"  ➜ ✅ {filename} ingestado con éxito.")
            except Exception as e:
                print(f"  ➜ ❌ Error al ingestar {filename}:\n{e}")
        else:
            print(f"⚠️  Advertencia: Archivo local no encontrado: {filepath}")

    elapsed = time.time() - start_time
    print(f"\n✅ ETL 06 completado exitosamente en {elapsed:.2f} segundos.")
    print("="*50 + "\n")

if __name__ == "__main__":
    ingest_enhanced_data()