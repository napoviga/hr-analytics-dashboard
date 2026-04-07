import pandas as pd
import os
import time
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def ingest_data():
    start_time = time.time()
    print("\n" + "="*50)
    print("📥 [ETL 02] INICIANDO INGESTA DE DATOS CORE")
    print("="*50)

    # 1. Cargar y Limpiar Nombres
    print("⏳ Cargando y limpiando 'ibm_hr.csv' en memoria...")
    try:
        df = pd.read_csv('../data/ibm_hr.csv')
        df.columns = [col.strip().lower().replace(' ', '_').replace('-', '_') for col in df.columns]
    except FileNotFoundError:
        print("❌ Error: Archivo ibm_hr.csv no encontrado.")
        return
    
    # 2. Conectar e Inyectar
    engine = create_engine(db_url)
    target_table = 'raw.ibm_hr_landing'
    print(f"🚀 Iniciando transferencia a PostgreSQL...")
    
    try:
        df.to_sql(
            name='ibm_hr_landing',
            con=engine,
            schema='raw',
            if_exists='append',
            index=False,
            chunksize=500
        )
    except Exception as e:
        print(f"❌ Error durante la inserción SQL:\n{e}")
        return

    print("\n📌 Resumen de ingesta:")
    print(f"  ➜ Origen:  '../data/ibm_hr.csv'")
    print(f"  ➜ Destino: Tabla [{target_table}]")
    print(f"  ➜ Volumen: {len(df):,} registros")

    elapsed = time.time() - start_time
    print(f"\n✅ ETL 02 completado exitosamente en {elapsed:.2f} segundos.")
    print("="*50 + "\n")

if __name__ == "__main__":
    ingest_data()