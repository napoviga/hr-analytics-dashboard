import pandas as pd
import os
import time
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def setup_raw():
    start_time = time.time()
    print("\n" + "="*50)
    print("🛠️  [ETL 01] INICIANDO PREPARACIÓN CAPA RAW")
    print("="*50)

    # 1. Leer CSV para detectar cabeceras
    print("⏳ Leyendo metadatos de '../data/ibm_hr.csv'...")
    try:
        df = pd.read_csv('../data/ibm_hr.csv', nrows=0) 
        columns = [col.strip().lower().replace(' ', '_').replace('-', '_') for col in df.columns]
    except FileNotFoundError:
        print("❌ Error: Archivo ibm_hr.csv no encontrado.")
        return

    # 2. Construir el SQL Dinámico
    table_name = "raw.ibm_hr_landing"
    cols_query = ", ".join([f"{col} TEXT" for col in columns])
    
    sql_query = f"""
    CREATE SCHEMA IF NOT EXISTS raw;
    DROP TABLE IF EXISTS {table_name} CASCADE;
    CREATE TABLE {table_name} (
        {cols_query},
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """
    
    # 3. Ejecutar en la Base de Datos
    print("⏳ Ejecutando comandos en la base de datos...")
    engine = create_engine(db_url)
    try:
        with engine.connect() as conn:
            conn.execute(text(sql_query))
            conn.commit()
    except Exception as e:
        print(f"❌ Error en la base de datos:\n{e}")
        return

    print("\n📌 Enumerando artefactos creados:")
    print("  1. Esquema: [raw]")
    print(f"  2. Tabla:   [{table_name}] (con {len(columns)} columnas)")
    
    elapsed = time.time() - start_time
    print(f"\n✅ ETL 01 completado exitosamente en {elapsed:.2f} segundos.")
    print("="*50 + "\n")

if __name__ == "__main__":
    setup_raw()