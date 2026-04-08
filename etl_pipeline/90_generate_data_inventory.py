import os
import time
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def run_data_inventory():
    print("\n" + "="*50 + "\n🌐 [ETL 90] ESCANEO TOTAL Y MUESTREO LIMPIO\n" + "="*50)
    
    if not db_url:
        print("❌ Error: DATABASE_URL no encontrada.")
        return

    engine = create_engine(db_url)
    inventory_data = []
    
    # 1. Regla ajustada por Napo: Umbral a 30
    UMBRAL_CARDINALIDAD = 30
    MAX_CARACTERES = 150 # Evita que las tablas Markdown se rompan visualmente

    try:
        with engine.connect() as conn:
            # 2. Excluimos la tabla 'data_inventory' para evitar el auto-escaneo infinito
            objs = conn.execute(text("""
                SELECT n.nspname as schema_name, c.relname as table_name,
                       CASE c.relkind 
                           WHEN 'r' THEN 'Tabla' 
                           WHEN 'v' THEN 'Vista' 
                           WHEN 'm' THEN 'M-View' 
                       END as obj_type
                FROM pg_class c
                JOIN pg_namespace n ON n.oid = c.relnamespace
                WHERE n.nspname IN ('business', 'raw')
                  AND c.relkind IN ('r', 'v', 'm')
                  AND n.nspname NOT IN ('information_schema', 'pg_catalog')
                  AND c.relname != 'data_inventory' 
                ORDER BY n.nspname, c.relname
            """)).fetchall()

            for s_name, t_name, t_type in objs:
                print(f"⏳ Mapeando: {s_name}.{t_name}...")
                
                cols = conn.execute(text(f"""
                    SELECT a.attname AS col, format_type(a.atttypid, a.atttypmod) AS tipo
                    FROM pg_attribute a JOIN pg_class c ON a.attrelid = c.oid
                    JOIN pg_namespace n ON c.relnamespace = n.oid
                    WHERE n.nspname = '{s_name}' AND c.relname = '{t_name}' 
                      AND a.attnum > 0 AND NOT a.attisdropped
                """)).fetchall()

                for c_name, d_type in cols:
                    res = conn.execute(text(f"""
                        SELECT COUNT(*) as total, 
                               COUNT("{c_name}") as no_nulos, 
                               COUNT(DISTINCT "{c_name}"::TEXT) as unicos
                        FROM {s_name}."{t_name}"
                    """)).fetchone()

                    total = res[0]
                    no_nulos = res[1]
                    unicos = res[2]
                    completitud = round((no_nulos / total) * 100, 1) if total > 0 else 0

                    muestra_valores = ""
                    if 'json' in d_type.lower() or 'array' in d_type.lower():
                        muestra_valores = "[Estructura Compleja]"
                    elif unicos == 0:
                        muestra_valores = "[Columna Vacía]"
                    elif unicos <= UMBRAL_CARDINALIDAD:
                        vals = conn.execute(text(f"""
                            SELECT DISTINCT "{c_name}"::TEXT 
                            FROM {s_name}."{t_name}" 
                            WHERE "{c_name}" IS NOT NULL ORDER BY 1
                        """)).fetchall()
                        muestra_valores = ", ".join([str(v[0]) for v in vals])
                    else:
                        vals = conn.execute(text(f"""
                            SELECT DISTINCT "{c_name}"::TEXT 
                            FROM {s_name}."{t_name}" 
                            WHERE "{c_name}" IS NOT NULL LIMIT 3
                        """)).fetchall()
                        ejemplos = ", ".join([str(v[0]) for v in vals])
                        muestra_valores = f"Valores múltiples (+{unicos:,}) | Ej: {ejemplos}..."

                    # 3. Limpieza de formato (Adiós saltos de línea y textos infinitos)
                    muestra_valores = muestra_valores.replace('\n', ' ').replace('\r', '')
                    if len(muestra_valores) > MAX_CARACTERES:
                        muestra_valores = muestra_valores[:MAX_CARACTERES] + "..."

                    inventory_data.append({
                        "Esquema": s_name, 
                        "Objeto": t_name, 
                        "Tipo": t_type, 
                        "Columna": c_name,
                        "Dato": d_type, 
                        "Completitud %": completitud,
                        "Unicos": unicos,
                        "Muestra de Datos": muestra_valores
                    })

        df_inv = pd.DataFrame(inventory_data)
        df_inv.to_sql('data_inventory', engine, schema='business', if_exists='replace', index=False)
        
        with open("../AI_KNOWLEDGE_BASE.md", "w", encoding="utf-8") as f:
            f.write("# 🧠 Catálogo Global de Datos - HR Analytics\n\n")
            for esquema in df_inv['Esquema'].unique():
                f.write(f"# 📂 Esquema: `{esquema}`\n\n")
                df_esq = df_inv[df_inv['Esquema'] == esquema]
                for obj in df_esq['Objeto'].unique():
                    f.write(f"### 📊 {obj}\n\n")
                    f.write(df_esq[df_esq['Objeto'] == obj].drop(columns=['Esquema', 'Objeto']).to_markdown(index=False) + "\n\n")
            
        print(f"✅ ¡Éxito! Archivo generado limpio y sin desbordes de texto.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_data_inventory()