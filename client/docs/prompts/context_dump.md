Generación de Contexto Maestro (Project Context Dump)

Actúa como un Arquitecto de Datos y Tech Lead. Necesito que analices el estado actual de todo este proyecto y generes un archivo en la raíz llamado project_context_dump.md. Este archivo lo usaré para documentar la arquitectura y sincronizar el contexto con otro equipo o agente de IA.

Por favor, escanea el proyecto y estructura el archivo Markdown exactamente con estas secciones:

1. Estructura de Directorios (Tree):
   Genera un árbol completo del proyecto. Excluye explícitamente directorios pesados o irrelevantes como node_modules, .git, venv, .venv, y **pycache**.

2. Dependencias y Entorno:

Extrae el contenido completo de requirements.txt (o lista las librerías de Python usadas si no existe).

Extrae las dependencias (dependencies y devDependencies) del archivo package.json de la carpeta client (o la carpeta del frontend).

3. Modelado de Base de Datos y Arquitectura de Datos:
   Analiza los scripts de la carpeta etl_pipeline (o donde resida la lógica de BD) y documenta:

Las tablas creadas en los diferentes esquemas (ej. raw, business, public).

Lista las columnas principales, sus tipos de datos y si son claves primarias/foráneas (deducidos de los queries SQL o de SQLAlchemy dentro de los scripts).

4. Scripts Críticos del Backend / Pipeline ETL:
   Necesito tener a la mano el código clave. Copia e inserta el código fuente completo de los scripts de Python que gestionan la ingesta, transformación y carga de datos (ej. los scripts dentro de etl_pipeline). Usa bloques de código de Python debidamente etiquetados y ordenados por su secuencia de ejecución.

5. Estado del Frontend (React/Vite):

Lista los archivos principales dentro de client/src/components o tu directorio de vistas.

Copia el bloque de rutas o renderizado condicional actual (usualmente en App.jsx o tu enrutador principal) para mapear qué vistas y componentes están activos en la interfaz.

6. Variables de Entorno (.env):
   Analiza los archivos .env (del backend y frontend) y muestra únicamente las claves (keys) que se están utilizando, ocultando estrictamente los valores reales por seguridad (ej. VITE_SUPABASE_URL=\*\*\*).

Si el archivo project_context_dump.md ya existe en la raíz, sobrescribe todo su contenido con esta nueva versión para tener el contexto 100% actualizado.

Por favor, genera el archivo project_context_dump.md en la raíz del proyecto y confírmame cuando esté listo.
