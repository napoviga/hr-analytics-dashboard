import os
import time
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def run_data_inventory():
    print("\n" + "="*50 + "\n🌐 [ETL 90] ACTUALIZANDO INVENTARIO DE METADATOS\n" + "="*50)
    
    if not db_url:
        print("❌ Error: DATABASE_URL no encontrada.")
        return

    engine = create_engine(db_url)
    inventory_data = []
    UMBRAL_CARDINALIDAD = 30
    MAX_CARACTERES = 150 

    # --- NUEVA RUTA DE DOCUMENTACIÓN (Docs as Code) ---
    md_path = "../docs/02-data-governance/02_supabase_metadata_inventory.md"
    os.makedirs(os.path.dirname(md_path), exist_ok=True)

    try:
        with engine.connect() as conn:
            # Escaneo de tablas, vistas y materializadas
            objs = conn.execute(text("""
                SELECT n.nspname as schema_name, c.relname as table_name,
                       CASE c.relkind WHEN 'r' THEN 'Tabla' WHEN 'v' THEN 'Vista' WHEN 'm' THEN 'M-View' END as obj_type
                FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
                WHERE n.nspname IN ('business', 'raw') AND c.relkind IN ('r', 'v', 'm')
                  AND n.nspname NOT IN ('information_schema', 'pg_catalog')
                  AND c.relname != 'data_inventory' 
                ORDER BY n.nspname, c.relname
            """)).fetchall()

            for s_name, t_name, t_type in objs:
                print(f"⏳ Mapeando metadatos de: {s_name}.{t_name}...")
                
                cols = conn.execute(text(f"""
                    SELECT a.attname AS col, format_type(a.atttypid, a.atttypmod) AS tipo
                    FROM pg_attribute a JOIN pg_class c ON a.attrelid = c.oid
                    JOIN pg_namespace n ON c.relnamespace = n.oid
                    WHERE n.nspname = '{s_name}' AND c.relname = '{t_name}' 
                      AND a.attnum > 0 AND NOT a.attisdropped
                """)).fetchall()

                for c_name, d_type in cols:
                    res = conn.execute(text(f"""
                        SELECT COUNT(*) as total, COUNT("{c_name}") as no_nulos, COUNT(DISTINCT "{c_name}"::TEXT) as unicos
                        FROM {s_name}."{t_name}"
                    """)).fetchone()

                    total, no_nulos, unicos = res[0], res[1], res[2]
                    completitud = round((no_nulos / total) * 100, 1) if total > 0 else 0

                    muestra_valores = ""
                    if unicos == 0:
                        muestra_valores = "[Columna Vacía]"
                    elif unicos <= UMBRAL_CARDINALIDAD:
                        vals = conn.execute(text(f"SELECT DISTINCT \"{c_name}\"::TEXT FROM {s_name}.\"{t_name}\" WHERE \"{c_name}\" IS NOT NULL ORDER BY 1")).fetchall()
                        muestra_valores = ", ".join([str(v[0]) for v in vals])
                    else:
                        vals = conn.execute(text(f"SELECT DISTINCT \"{c_name}\"::TEXT FROM {s_name}.\"{t_name}\" WHERE \"{c_name}\" IS NOT NULL LIMIT 3")).fetchall()
                        muestra_valores = f"Valores múltiples (+{unicos:,}) | Ej: {', '.join([str(v[0]) for v in vals])}..."

                    muestra_valores = muestra_valores.replace('\n', ' ').replace('\r', '')[:MAX_CARACTERES]

                    inventory_data.append({
                        "Esquema": s_name, "Objeto": t_name, "Tipo": t_type, "Columna": c_name,
                        "Dato": d_type, "Completitud %": completitud, "Unicos": unicos, "Muestra": muestra_valores
                    })

        df_inv = pd.DataFrame(inventory_data)
        df_inv.to_sql('data_inventory', engine, schema='business', if_exists='replace', index=False)
        
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("# 📑 Inventario Técnico de Metadatos (Supabase)\n\n")
            f.write(f"> **Última sincronización:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("> **Alcance:** Esquemas `raw` y `business`. Reporte generado automáticamente por el script 90.\n\n")
            for esquema in df_inv['Esquema'].unique():
                f.write(f"## 📂 Esquema: `{esquema}`\n\n")
                df_esq = df_inv[df_inv['Esquema'] == esquema]
                for obj in df_esq['Objeto'].unique():
                    f.write(f"### 📊 {obj}\n\n")
                    f.write(df_esq[df_esq['Objeto'] == obj].drop(columns=['Esquema', 'Objeto']).to_markdown(index=False) + "\n\n")
            
        print(f"✅ Catálogo de metadatos actualizado en: {md_path}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_data_inventory()