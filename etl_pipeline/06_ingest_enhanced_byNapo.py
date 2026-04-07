import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def ingest_enhanced_data():
    print("📥 Iniciando ingesta de datos potenciados (byNapo)...")
    
    engine = create_engine(db_url)
    data_dir = "../data/"
    
    files_to_ingest = {
        "ibm_hr_monthly_snapshot_byNapo.csv": "raw.ibm_hr_monthly_snapshot_byNapo",
        # Agrega aquí los otros CSVs si los generas:
        # "ibm_hr_change_reasons_byNapo.csv": "raw.ibm_hr_change_reasons_byNapo"
    }
    
    for filename, table_name in files_to_ingest.items():
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            # Normalizar nombres de columnas para match exacto
            df.columns = [col.strip().lower() for col in df.columns]
            
            print(f"🚀 Subiendo {len(df)} registros a {table_name}...")
            df.to_sql(
                name=table_name.split('.')[1],
                schema=table_name.split('.')[0],
                con=engine,
                if_exists='append',
                index=False,
                chunksize=1000
            )
            print(f"✅ {filename} ingestado exitosamente.")
        else:
            print(f"⚠️ Archivo no encontrado: {filepath}")

if __name__ == "__main__":
    ingest_enhanced_data()