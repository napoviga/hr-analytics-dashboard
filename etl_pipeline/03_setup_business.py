import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def setup_business():
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
    
    with engine.connect() as conn:
        conn.execute(text(sql_query))
        conn.commit()
    print("✅ Capa BUSINESS preparada: Vista core.ibm_hr lista y con permisos otorgados.")

if __name__ == "__main__":
    setup_business()