Generador de Actualización para Documentación (README Update Brief)

Actúa como un Technical Writer y Analista de Software. Necesito que escanees el proyecto actual y lo compares con el contenido que ya tenemos escrito en el archivo README.md.

Tu objetivo es generar un archivo temporal llamado readme_update_brief.md en la raíz del proyecto, que contenga un resumen estructurado de todo lo nuevo o modificado para que otro agente pueda redactar la versión final del README.

Por favor, incluye exactamente estas secciones:

1. Nuevos Módulos y Scripts:
   Lista cualquier archivo nuevo que se haya creado en etl_pipeline (ej. los pasos 04, 05, 06, 07) o en el frontend (client/src/components). Agrega una línea explicando qué hace cada uno.

2. Evolución de la Arquitectura de Datos:
   Detalla si se han creado nuevos esquemas, nuevas tablas en Supabase, o si la lógica de ingesta ha cambiado (ej. pasar de datos estáticos a series de tiempo mensuales).

3. Actualizaciones de la Interfaz (Frontend):
   Enumera las nuevas vistas, submenús, o cambios de diseño importantes que se hayan integrado en la UI de React.

4. Nuevas Dependencias:
   Menciona si se instaló alguna librería nueva en Python (requirements.txt) o en React (package.json) que deba documentarse.

Nota: Si el archivo readme_update_brief.md ya existe, sobrescribe todo su contenido con esta nueva evaluación.
