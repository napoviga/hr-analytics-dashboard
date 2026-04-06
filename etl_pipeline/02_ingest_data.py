import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def ingest_data():
    # 1. Cargar y Limpiar Nombres
    df = pd.read_csv('../data/ibm_hr.csv')
    df.columns = [col.strip().lower().replace(' ', '_').replace('-', '_') for col in df.columns]
    
    # 2. Conectar e Inyectar
    engine = create_engine(db_url)
    print(f"🚀 Iniciando ingesta de {len(df)} registros...")
    
    df.to_sql(
        name='ibm_hr_landing',
        con=engine,
        schema='raw',
        if_exists='append',
        index=False,
        chunksize=500 # Sube de 500 en 500 para mayor estabilidad
    )
    print("✅ Ingesta completada con éxito en raw.ibm_hr_landing.")

if __name__ == "__main__":
    ingest_data()