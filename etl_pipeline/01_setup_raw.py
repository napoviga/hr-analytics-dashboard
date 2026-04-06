import pandas as pd
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def setup_raw():
    # 1. Leer CSV para detectar cabeceras
    df = pd.read_csv('../data/ibm_hr.csv', nrows=0) 
    columns = [col.strip().lower().replace(' ', '_').replace('-', '_') for col in df.columns]
    
    # 2. Construir el SQL Dinámico
    table_name = "raw.ibm_hr_landing"
    cols_query = ", ".join([f"{col} TEXT" for col in columns])
    sql_query = f"""
    CREATE SCHEMA IF NOT EXISTS raw;
    DROP TABLE IF EXISTS {table_name};
    CREATE TABLE {table_name} (
        {cols_query},
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """
    
    # 3. Ejecutar en la Base de Datos
    engine = create_engine(db_url)
    with engine.connect() as conn:
        conn.execute(text(sql_query))
        conn.commit()
    print(f"✅ Capa RAW preparada: Tabla {table_name} creada con {len(columns)} columnas.")

if __name__ == "__main__":
    setup_raw()