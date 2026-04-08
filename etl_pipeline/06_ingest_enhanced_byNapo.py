import pandas as pd
import os
import time
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def ingest_enhanced_data():
    start_time = time.time()
    print("\n" + "="*50)
    print("📥 [ETL 06] INGESTA DE DATOS POTENCIADOS (byNapo)")
    print("="*50)
    
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
            df = pd.read_csv(filepath, dtype=str)
            # Normalizar nombres de columnas para match exacto
            df.columns = [col.strip().lower() for col in df.columns]
            # Reemplazar NaN por None (NULL en SQL) — todo entra como TEXT
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