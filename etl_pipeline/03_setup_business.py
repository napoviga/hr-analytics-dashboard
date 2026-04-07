import os
import time
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def setup_business():
    start_time = time.time()
    print("\n" + "="*50)
    print("🏢 [ETL 03] CONSTRUYENDO CAPA BUSINESS (BASE)")
    print("="*50)

    engine = create_engine(db_url)
    
    sql_query = """
    CREATE SCHEMA IF NOT EXISTS business;
    
    CREATE OR REPLACE VIEW business.ibm_hr AS
    SELECT 
        employeenumber::INTEGER as id,
        age::INTEGER,
        department,
        jobrole,
        attrition,
        gender,
        dailyrate::INTEGER,
        monthlyincome::INTEGER,
        totalworkingyears::INTEGER,
        yearsatcompany::INTEGER,
        distancefromhome::INTEGER
    FROM raw.ibm_hr_landing;

    -- Permisos para el Dashboard
    GRANT USAGE ON SCHEMA business TO anon;
    GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
    """
    
    print("⏳ Ejecutando sentencias analíticas en la base de datos...")
    try:
        with engine.connect() as conn:
            conn.execute(text(sql_query))
            conn.commit()
    except Exception as e:
        print(f"❌ Error en la base de datos:\n{e}")
        return

    print("\n📌 Enumerando artefactos creados:")
    print("  1. Esquema: [business]")
    print("  2. Vista:   [business.ibm_hr] (tipada)")
    print("  🔑 Permisos [anon] asignados a toda la capa oro.")

    elapsed = time.time() - start_time
    print(f"\n✅ ETL 03 completado exitosamente en {elapsed:.2f} segundos.")
    print("="*50 + "\n")

if __name__ == "__main__":
    setup_business()