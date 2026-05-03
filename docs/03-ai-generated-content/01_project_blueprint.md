# Project Blueprint — HR Analytics Dashboard

> **Generado automáticamente:** 2026-05-03T16:57:14Z
> **Ejecutado por:** Antigravity Terminal
> **Versión del Pipeline:** Scripts 01-04 + m01-m13 + 90-92

---

## 1. Estructura de Directorios

```
Listado de rutas de carpetas
El n£mero de serie del volumen es 5465-5BCC
E:.
|   .env
|   generate_blueprint.py
|   hr-analytics-dashboard.pbix
|   README.md
|   
+---client
|   |   .env
|   |   eslint.config.js
|   |   index.html
|   |   package-lock.json
|   |   package.json
|   |   prisma.config.ts
|   |   skills-lock.json
|   |   vite.config.js
|   |   
|   +---.agents
|   |   \---skills
|   |       \---supabase-postgres-best-practices
|   |           |   SKILL.md
|   |           |   
|   |           \---references
|   |                   advanced-full-text-search.md
|   |                   advanced-jsonb-indexing.md
|   |                   conn-idle-timeout.md
|   |                   conn-limits.md
|   |                   conn-pooling.md
|   |                   conn-prepared-statements.md
|   |                   data-batch-inserts.md
|   |                   data-n-plus-one.md
|   |                   data-pagination.md
|   |                   data-upsert.md
|   |                   lock-advisory.md
|   |                   lock-deadlock-prevention.md
|   |                   lock-short-transactions.md
|   |                   lock-skip-locked.md
|   |                   monitor-explain-analyze.md
|   |                   monitor-pg-stat-statements.md
|   |                   monitor-vacuum-analyze.md
|   |                   query-composite-indexes.md
|   |                   query-covering-indexes.md
|   |                   query-index-types.md
|   |                   query-missing-indexes.md
|   |                   query-partial-indexes.md
|   |                   schema-constraints.md
|   |                   schema-data-types.md
|   |                   schema-foreign-key-indexes.md
|   |                   schema-lowercase-identifiers.md
|   |                   schema-partitioning.md
|   |                   schema-primary-keys.md
|   |                   security-privileges.md
|   |                   security-rls-basics.md
|   |                   security-rls-performance
...
```

---

## 2. Dependencias y Entorno

### Frontend (Node.js)

| Dependencia | Versión |
|---|---|
| @supabase/supabase-js | ^2.101.1 |
| echarts | ^6.0.0 |
| echarts-for-react | ^3.0.6 |
| echarts-wordcloud | ^2.1.0 |
| lucide-react | ^1.7.0 |
| react | ^19.2.4 |
| react-dom | ^19.2.4 |

### DevDependencies

| Dependencia | Versión |
|---|---|
| @eslint/js | ^9.39.4 |
| @tailwindcss/vite | ^4.2.2 |
| @types/react | ^19.2.14 |
| @types/react-dom | ^19.2.3 |
| @vitejs/plugin-react | ^6.0.1 |
| autoprefixer | ^10.4.27 |
| dotenv | ^17.4.1 |
| eslint | ^9.39.4 |
| eslint-plugin-react-hooks | ^7.0.1 |
| eslint-plugin-react-refresh | ^0.5.2 |
| globals | ^17.4.0 |
| postcss | ^8.5.8 |
| prisma | ^7.6.0 |
| tailwindcss | ^4.2.2 |
| vite | ^8.0.1 |

---

## 3. Arquitectura de Datos

*(Ver documentos detallados: Data Dictionary & Data Lineage)*

---

## 4. Pipeline ETL

*(Ver docs/PIPELINE_ORDER.md)*

---

## 5. Estado del Frontend Modular

| Módulo | Archivos |
|---|---|
| 00-layout | Overview.jsx, SectionLanding.jsx, Sidebar.jsx |
| 01-vision-ejecutiva | AlertasAnomalias.jsx, Benchmarking.jsx |
| 02-reclutamiento | AuditoriaSesgos.jsx, CalidadContratacion.jsx, EficienciaCiclos.jsx, FitScore.jsx, hooks, NpsCandidato.jsx |
| 03-onboarding | hooks, ProcesosActivos.jsx, RotacionTemprana.jsx, TiempoProductividad.jsx |
| 04-ciclo-vida | CausalidadCorrelaciones.jsx, ComportamientoGrupos.jsx, hooks, MapaMomentos.jsx |
| 05-fuerza-laboral | Demographics.jsx, EmployeeTable.jsx, hooks, OrganigramaIntegral.jsx, OrgStructure.jsx |
| 06-nomina-costos | CompaRatio.jsx, Compensations.jsx, EquidadInterna.jsx, ImpactoFinanciero.jsx, MasaSalarial.jsx, SimuladorSalarial.jsx |
| 07-tiempo-asistencia | Ausentismo.jsx, HorasExtra.jsx, MallaVacaciones.jsx, SaludOcupacional.jsx |
| 08-gestion-desempeno | AvanceOKRs.jsx, Evaluacion360.jsx, PlanesMejora.jsx, RankingPerformers.jsx |
| 09-talento-desarrollo | BrechasSkills.jsx, MapaSucesion.jsx, MatrizNineBox.jsx, RoiCapacitacion.jsx |
| 10-engagement-sentimiento | DiversidadInclusion.jsx, EngagementENPS.jsx, HeatmapEngagement.jsx |
| 11-compliance | CumplimientoLaboral.jsx, RelacionesSindicales.jsx |
| 12-retencion | BenchmarkingTurnover.jsx, CorrelacionManager.jsx, ScoreFuga.jsx |
| 13-calidad-datos | DiccionarioDatos.jsx, LogDatosMaestros.jsx |
| 14-administracion |  |
| build_ui.py |  |

---

## 6. Variables de Entorno

| Variable |
|---|
| VITE_SUPABASE_URL |
| VITE_SUPABASE_ANON_KEY |
| SUPABASE_SERVICE_KEY |
| DATABASE_URL |

---

## 7. Score de Madurez del Proyecto

| Métrica | Score |
|---|---|
| Módulos implementados | 13/13 |
| Documentación al día | Sí |
| Pipeline Ejecutando | Sí |
