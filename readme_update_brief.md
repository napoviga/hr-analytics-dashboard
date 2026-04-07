# 📝 Resumen de Actualización para el README (Update Brief)

Este documento contiene el diagnóstico y las novedades arquitectónicas y estructurales detectadas en el proyecto, comparadas contra el `README.md` actual. Sirve como insumo (brief) para que un Technical Writer o IA redacte la versión final del README oficial.

## 1. Nuevos Módulos y Scripts
Se han incorporado nuevos flujos tanto en el backend (ETL) como en el frontend para escalar el alcance del proyecto original:

**En `etl_pipeline/` (Pipeline Potenciado "byNapo"):**
- `04_create_enhanced_dataset_byNapo.py`: Script simulador que crea un set de datos avanzado (`ibm_hr_monthly_snapshot_byNapo.csv`), pasando de tener un snapshot estático a tener información histórica y mensual de los empleados (series de tiempo).
- `05_setup_raw_enhanced_byNapo.py`: Genera las nuevas tablas en el esquema `raw` para aterrizar los nuevos datos generados, incluyendo una tabla de catálogos de motivos de cambio.
- `06_ingest_enhanced_byNapo.py`: Orquesta la ingesta pura de este nuevo gran dataset ampliado (por chunks) dentro de PostgreSQL/Supabase.
- `07_setup_business_enhanced_byNapo.py`: El core transformacional actualizado. Abandona la vista estática e incluye vistas tipadas completas (`v_employee_full_byNapo`), consultas recursivas para árboles organizacionales (`v_org_tree_byNapo`), e incorpora Vistas Materializadas (`mv_monthly_kpis_byNapo`) para mayor performance analítica.

**En Frontend (`client/src/components/`):**
- Incorporación de módulos consolidados y enlazados dinámicamente en el Sidebar:
  - `Overview.jsx` (Visión general de indicadores)
  - `OrgStructure.jsx` y `OrganigramaIntegral.jsx` (Dedicados a Estructura Organizacional)
  - `Compensations.jsx` (Para análisis de compensaciones)
  - `EmployeeTable.jsx` (Auditoría de datos y grids)

## 2. Evolución de la Arquitectura de Datos
El `README.md` actual describe un flujo estático (Medallion en `raw` y `business` simple). La evolución arquitectónica trae cambios importantes que deben ser documentados:
- **De Datos Estáticos a Series de Tiempo y Snapshots:** El modelo migró a soportar lógica de RRHH mensual (`snapshot_date`), permitiendo calcular verdaderas tasas de rotación (Attrition Rate), cambios de puesto/salario y antigüedad dinámica (`tenure_months`).
- **Nuevas Estructuras Nativas de Postgres:** Uso de `WITH RECURSIVE` para calcular de forma backend el árbol de organización (previniendo ciclos), emitiendo de forma nativa nodos JSON listos para gráficas `ECharts`. Adicionalmente, se integró el concepto de Vistas Materializadas para procesar KPIs ejecutivos globales, con índices (`idx_mv_kpis_snapshot`).

## 3. Actualizaciones de la Interfaz (Frontend)
El README menciona módulos que estaban "en construcción", pero ahora el Frontend ha evolucionado:
- **Arquitectura de Interfaz SPA Sin Router:** Se consolidó una navegación centralizada vía `App.jsx` inyectando vistas condicionales (`vistaActual`), descartando librerías complejas como `react-router-dom` para darle un manejo puramente centrado en estado (`useState`).
- **Integración Temática Completa:** Funciones nativas y responsivas apoyadas fuertemente en **Tailwind CSS**.
- **Jerarquía del Sidebar:** Ya controla el enrutamiento oficial y expone el menú y sub-menú real (Acordeones).

## 4. Nuevas Dependencias
Es importante documentar para los próximos desarrolladores la presencia de nuevas librerías utilizadas para soportar el módulo *Enhanced*:

**Backend (Python):**
- `networkx`: Introducida para simulaciones y lógica avanzada en la generación recursiva de grafos/organigramas.
- `numpy`: Añadido al pipeline para rutinas matemáticas y de simulación rápida en combinatoria con Pandas.

**Frontend (React/Vite) - (Ya presentes en package.json actual pero a resaltar):**
- `@supabase/supabase-js` (Confirmado en uso y centralizado)
- `echarts` y `echarts-for-react` para visualizaciones dinámicas de BI (el organigrama JSON nativo viaja a ECharts).
- `lucide-react` para iconografía estandarizada.
