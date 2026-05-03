# 📑 Inventario Técnico de Metadatos (Supabase)

> **Última sincronización:** 2026-05-03T16:56:13Z
> **Alcance:** Esquemas `raw` y `business`. Reporte generado automáticamente por el script 90.

## 📂 Esquema: `business`

### 📊 ibm_hr

| Tipo   | Columna           | Dato    |   Completitud % |   Unicos | Muestra                                                                                                                                                |
|:-------|:------------------|:--------|----------------:|---------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
| Vista  | id                | integer |             100 |     1470 | Valores múltiples (+1,470) | Ej: 1318, 1562, 551...                                                                                                    |
| Vista  | age               | integer |             100 |       43 | Valores múltiples (+43) | Ej: 54, 47, 28...                                                                                                            |
| Vista  | department        | text    |             100 |        3 | Human Resources, Research & Development, Sales                                                                                                         |
| Vista  | jobrole           | text    |             100 |        9 | Healthcare Representative, Human Resources, Laboratory Technician, Manager, Manufacturing Director, Research Director, Research Scientist, Sales Execu |
| Vista  | attrition         | text    |             100 |        2 | No, Yes                                                                                                                                                |
| Vista  | gender            | text    |             100 |        2 | Female, Male                                                                                                                                           |
| Vista  | dailyrate         | integer |             100 |      886 | Valores múltiples (+886) | Ej: 461, 711, 791...                                                                                                        |
| Vista  | monthlyincome     | integer |             100 |     1349 | Valores múltiples (+1,349) | Ej: 2571, 10048, 2585...                                                                                                  |
| Vista  | totalworkingyears | integer |             100 |       40 | Valores múltiples (+40) | Ej: 8, 12, 10...                                                                                                             |
| Vista  | yearsatcompany    | integer |             100 |       37 | Valores múltiples (+37) | Ej: 8, 12, 10...                                                                                                             |
| Vista  | distancefromhome  | integer |             100 |       29 | 1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 2, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 3, 4, 5, 6, 7, 8, 9                                              |

### 📊 mv_absenteeism

| Tipo   | Columna             | Dato    |   Completitud % |   Unicos | Muestra                                                                  |
|:-------|:--------------------|:--------|----------------:|---------:|:-------------------------------------------------------------------------|
| M-View | periodo             | date    |             100 |       75 | Valores múltiples (+75) | Ej: 2025-06-01, 2024-11-01, 2024-10-01...      |
| M-View | department_name     | text    |             100 |        5 | Finance, HR, IT, Operations, Sales                                       |
| M-View | country_iso3        | text    |             100 |        6 | CHL, COL, ESP, MEX, PER, USA                                             |
| M-View | total_dias          | bigint  |             100 |       93 | Valores múltiples (+93) | Ej: 176, 173, 129...                           |
| M-View | dias_ausencia       | bigint  |             100 |       21 | 0, 1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 2, 21, 3, 4, 5, 6, 7, 8, 9 |
| M-View | tasa_ausentismo     | numeric |             100 |       96 | Valores múltiples (+96) | Ej: 10.2, 1.6, 9.3...                          |
| M-View | total_minutos_tarde | bigint  |             100 |      603 | Valores múltiples (+603) | Ej: 845, 537, 354...                          |

### 📊 mv_alerts_anomalies

| Tipo   | Columna         | Dato    |   Completitud % |   Unicos | Muestra                                                             |
|:-------|:----------------|:--------|----------------:|---------:|:--------------------------------------------------------------------|
| M-View | snapshot_date   | date    |           100   |       75 | Valores múltiples (+75) | Ej: 2020-12-31, 2023-04-30, 2025-04-30... |
| M-View | country_iso3    | text    |           100   |        6 | CHL, COL, ESP, MEX, PER, USA                                        |
| M-View | department_name | text    |           100   |        5 | Finance, HR, IT, Operations, Sales                                  |
| M-View | headcount       | bigint  |           100   |       95 | Valores múltiples (+95) | Ej: 119, 198, 133...                      |
| M-View | bajas           | bigint  |           100   |        5 | 0, 1, 2, 3, 4                                                       |
| M-View | prev_headcount  | bigint  |            98.7 |       94 | Valores múltiples (+94) | Ej: 119, 198, 133...                      |
| M-View | z_score_hc      | numeric |            98   |      330 | Valores múltiples (+330) | Ej: 0.70, 0.43, 2.35...                  |
| M-View | z_score_bajas   | numeric |            97.8 |      354 | Valores múltiples (+354) | Ej: 0.70, 0.43, -1.32...                 |
| M-View | status_hc       | text    |           100   |        3 | ALERTA, ATENCION, NORMAL                                            |
| M-View | status_bajas    | text    |           100   |        3 | ALERTA, ATENCION, NORMAL                                            |

### 📊 mv_bajas_heatmap

| Tipo   | Columna         | Dato   |   Completitud % |   Unicos | Muestra                                                             |
|:-------|:----------------|:-------|----------------:|---------:|:--------------------------------------------------------------------|
| M-View | snapshot_date   | date   |             100 |       75 | Valores múltiples (+75) | Ej: 2020-12-31, 2023-04-30, 2025-04-30... |
| M-View | country_iso3    | text   |             100 |        6 | CHL, COL, ESP, MEX, PER, USA                                        |
| M-View | department_name | text   |             100 |        5 | Finance, HR, IT, Operations, Sales                                  |
| M-View | job_level_1     | text   |             100 |        2 | Individual Contributor, Management                                  |
| M-View | job_level_2     | text   |             100 |        3 | Junior, Lead, Senior                                                |
| M-View | work_center_id  | text   |             100 |        6 | WC-CHL, WC-COL, WC-ESP, WC-MEX, WC-PER, WC-USA                      |
| M-View | count           | bigint |             100 |        4 | 1, 2, 3, 4                                                          |

### 📊 mv_compa_ratio

| Tipo   | Columna            | Dato             |   Completitud % |   Unicos | Muestra                                                                                                                                                |
|:-------|:-------------------|:-----------------|----------------:|---------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
| M-View | snapshot_date      | date             |             100 |       75 | Valores múltiples (+75) | Ej: 2020-01-31, 2020-02-29, 2020-03-31...                                                                                    |
| M-View | employee_id        | integer          |             100 |     7000 | Valores múltiples (+7,000) | Ej: 1, 10, 100...                                                                                                         |
| M-View | full_name          | text             |             100 |       56 | Valores múltiples (+56) | Ej: Ana Gomez, Ana Lopez, Ana Martinez...                                                                                    |
| M-View | department_name    | text             |             100 |        5 | Finance, HR, IT, Operations, Sales                                                                                                                     |
| M-View | job_role           | text             |             100 |       17 | Account Manager, Accountant, CEO, CFO, CTO, Data Analyst, DevOps, Financial Analyst, HR Manager, HR Specialist, Logistics Coord, Operator, Ops Directo |
| M-View | job_level_1        | text             |             100 |        2 | Individual Contributor, Management                                                                                                                     |
| M-View | job_level_2        | text             |             100 |        3 | Junior, Lead, Senior                                                                                                                                   |
| M-View | country_iso3       | text             |             100 |        6 | CHL, COL, ESP, MEX, PER, USA                                                                                                                           |
| M-View | monthly_salary_usd | numeric(12,2)    |             100 |    20445 | Valores múltiples (+20,445) | Ej: 1000.06, 1000.09, 1000.10...                                                                                         |
| M-View | band_median        | double precision |             100 |     4984 | Valores múltiples (+4,984) | Ej: 1000.09, 1000.1, 1000.74...                                                                                           |
| M-View | compa_ratio_pct    | numeric          |             100 |     2444 | Valores múltiples (+2,444) | Ej: 100.0, 100.1, 100.2...                                                                                                |
| M-View | range_status       | text             |             100 |        3 | Above Range, Below Range, In Range                                                                                                                     |

### 📊 mv_compliance_dashboard

| Tipo   | Columna           | Dato   |   Completitud % |   Unicos | Muestra                      |
|:-------|:------------------|:-------|----------------:|---------:|:-----------------------------|
| M-View | country_iso3      | text   |             100 |        6 | CHL, COL, ESP, MEX, PER, USA |
| M-View | obligation_type   | text   |             100 |        1 | Labor Law                    |
| M-View | status            | text   |             100 |        1 | Compliant                    |
| M-View | risk_level        | text   |             100 |        1 | High                         |
| M-View | total_obligations | bigint |             100 |        1 | 1                            |
| M-View | overdue_count     | bigint |             100 |        1 | 0                            |

### 📊 mv_country_dist

| Tipo   | Columna         | Dato   |   Completitud % |   Unicos | Muestra                                                             |
|:-------|:----------------|:-------|----------------:|---------:|:--------------------------------------------------------------------|
| M-View | snapshot_date   | date   |             100 |       75 | Valores múltiples (+75) | Ej: 2020-12-31, 2023-04-30, 2025-04-30... |
| M-View | country_iso3    | text   |             100 |        6 | CHL, COL, ESP, MEX, PER, USA                                        |
| M-View | department_name | text   |             100 |        5 | Finance, HR, IT, Operations, Sales                                  |
| M-View | job_level_1     | text   |             100 |        2 | Individual Contributor, Management                                  |
| M-View | job_level_2     | text   |             100 |        3 | Junior, Lead, Senior                                                |
| M-View | work_center_id  | text   |             100 |        6 | WC-CHL, WC-COL, WC-ESP, WC-MEX, WC-PER, WC-USA                      |
| M-View | value           | bigint |             100 |      129 | Valores múltiples (+129) | Ej: 71, 118, 123...                      |

### 📊 mv_critical_moments

| Tipo   | Columna        | Dato    |   Completitud % |   Unicos | Muestra                                             |
|:-------|:---------------|:--------|----------------:|---------:|:----------------------------------------------------|
| M-View | tenure_quarter | numeric |             100 |       47 | Valores múltiples (+47) | Ej: 75, 96, 129...        |
| M-View | exits_at_point | bigint  |             100 |       46 | Valores múltiples (+46) | Ej: 576, 2, 261...        |
| M-View | total_at_point | bigint  |             100 |       47 | Valores múltiples (+47) | Ej: 1944, 10425, 13177... |
| M-View | hazard_rate    | numeric |             100 |       47 | Valores múltiples (+47) | Ej: 5.81, 12.56, 19.83... |

### 📊 mv_demographics_agg

| Tipo   | Columna         | Dato   |   Completitud % |   Unicos | Muestra                                                             |
|:-------|:----------------|:-------|----------------:|---------:|:--------------------------------------------------------------------|
| M-View | snapshot_date   | date   |             100 |       75 | Valores múltiples (+75) | Ej: 2020-12-31, 2023-04-30, 2025-04-30... |
| M-View | country_iso3    | text   |             100 |        6 | CHL, COL, ESP, MEX, PER, USA                                        |
| M-View | department_name | text   |             100 |        5 | Finance, HR, IT, Operations, Sales                                  |
| M-View | job_level_1     | text   |             100 |        2 | Individual Contributor, Management                                  |
| M-View | job_level_2     | text   |             100 |        3 | Junior, Lead, Senior                                                |
| M-View | work_center_id  | text   |             100 |        6 | WC-CHL, WC-COL, WC-ESP, WC-MEX, WC-PER, WC-USA                      |
| M-View | total_hc        | bigint |             100 |      144 | Valores múltiples (+144) | Ej: 71, 118, 123...                      |
| M-View | altas           | bigint |             100 |        8 | 0, 1, 2, 3, 4, 5, 6, 7                                              |
| M-View | bajas           | bigint |             100 |        5 | 0, 1, 2, 3, 4                                                       |

### 📊 mv_diversity_pyramid

| Tipo   | Columna         | Dato   |   Completitud % |   Unicos | Muestra                                                             |
|:-------|:----------------|:-------|----------------:|---------:|:--------------------------------------------------------------------|
| M-View | snapshot_date   | date   |             100 |       75 | Valores múltiples (+75) | Ej: 2020-12-31, 2023-04-30, 2025-04-30... |
| M-View | country_iso3    | text   |             100 |        6 | CHL, COL, ESP, MEX, PER, USA                                        |
| M-View | department_name | text   |             100 |        5 | Finance, HR, IT, Operations, Sales                                  |
| M-View | job_level_1     | text   |             100 |        2 | Individual Contributor, Management                                  |
| M-View | job_level_2     | text   |             100 |        3 | Junior, Lead, Senior                                                |
| M-View | work_center_id  | text   |             100 |        6 | WC-CHL, WC-COL, WC-ESP, WC-MEX, WC-PER, WC-USA                      |
| M-View | gender          | text   |             100 |        2 | Female, Male                                                        |
| M-View | value           | bigint |             100 |       73 | Valores múltiples (+73) | Ej: 13, 28, 39...                         |

### 📊 mv_early_turnover

| Tipo   | Columna                | Dato    |   Completitud % |   Unicos | Muestra                                                             |
|:-------|:-----------------------|:--------|----------------:|---------:|:--------------------------------------------------------------------|
| M-View | snapshot_date          | date    |           100   |       75 | Valores múltiples (+75) | Ej: 2020-12-31, 2023-04-30, 2025-04-30... |
| M-View | department_name        | text    |           100   |        5 | Finance, HR, IT, Operations, Sales                                  |
| M-View | country_iso3           | text    |           100   |        6 | CHL, COL, ESP, MEX, PER, USA                                        |
| M-View | bajas_tempranas        | bigint  |           100   |        6 | 0, 1, 2, 3, 4, 5                                                    |
| M-View | total_nuevos           | bigint  |           100   |       17 | 0, 1, 10, 11, 12, 13, 15, 16, 17, 2, 3, 4, 5, 6, 7, 8, 9            |
| M-View | tasa_rotacion_temprana | numeric |            98.8 |       37 | Valores múltiples (+37) | Ej: 16.7, 62.5, 11.8...                   |

### 📊 mv_enps_trend

| Tipo   | Columna         | Dato    |   Completitud % |   Unicos | Muestra                                                                                                                                                |
|:-------|:----------------|:--------|----------------:|---------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
| M-View | periodo         | date    |             100 |        1 | 2024-01-01                                                                                                                                             |
| M-View | department_name | text    |             100 |        5 | Finance, HR, IT, Operations, Sales                                                                                                                     |
| M-View | country_iso3    | text    |             100 |        6 | CHL, COL, ESP, MEX, PER, USA                                                                                                                           |
| M-View | promoters       | bigint  |             100 |       30 | 1056, 1140, 1297, 1439, 1462, 1577, 1581, 1696, 1705, 1718, 1734, 1786, 1787, 1828, 1833, 1861, 1882, 1924, 1928, 1951, 1955, 1977, 2048, 2078, 2104,  |
| M-View | detractors      | bigint  |             100 |       30 | 4201, 4581, 4617, 4758, 4933, 4957, 4959, 4967, 5064, 5153, 5360, 5522, 5696, 5706, 5762, 5813, 5934, 5980, 6001, 6026, 6082, 6095, 6250, 6295, 6388,  |
| M-View | total_responses | bigint  |             100 |       30 | 10030, 10109, 10227, 10851, 10873, 10879, 11131, 11310, 7682, 7777, 8019, 8367, 8388, 8559, 8669, 8735, 8854, 8868, 8912, 9028, 9360, 9412, 9425, 9574 |
| M-View | enps_score      | numeric |             100 |       28 | -27.9, -28.1, -29.6, -35.7, -36.0, -36.2, -36.6, -36.7, -36.8, -37.3, -37.4, -37.7, -39.6, -40.0, -40.3, -42.2, -42.7, -43.6, -44.0, -44.2, -45.4, -45 |

### 📊 mv_experience_bubbles

| Tipo   | Columna         | Dato    |   Completitud % |   Unicos | Muestra                                                                                             |
|:-------|:----------------|:--------|----------------:|---------:|:----------------------------------------------------------------------------------------------------|
| M-View | snapshot_date   | date    |             100 |       75 | Valores múltiples (+75) | Ej: 2020-12-31, 2023-04-30, 2025-04-30...                                 |
| M-View | country_iso3    | text    |             100 |        6 | CHL, COL, ESP, MEX, PER, USA                                                                        |
| M-View | department_name | text    |             100 |        5 | Finance, HR, IT, Operations, Sales                                                                  |
| M-View | job_level_1     | text    |             100 |        2 | Individual Contributor, Management                                                                  |
| M-View | job_level_2     | text    |             100 |        3 | Junior, Lead, Senior                                                                                |
| M-View | work_center_id  | text    |             100 |        6 | WC-CHL, WC-COL, WC-ESP, WC-MEX, WC-PER, WC-USA                                                      |
| M-View | generation      | text    |             100 |        4 | < 1 año, 1-3 años, 3-6 años, 6+ años                                                                |
| M-View | tenure_bucket   | integer |             100 |       24 | 0, 102, 108, 114, 12, 120, 126, 132, 138, 18, 24, 30, 36, 42, 48, 54, 6, 60, 66, 72, 78, 84, 90, 96 |
| M-View | avg_salary      | numeric |             100 |     1395 | Valores múltiples (+1,395) | Ej: 1597, 1487, 791...                                                 |
| M-View | emp_count       | bigint  |             100 |       20 | 1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 2, 20, 3, 4, 5, 6, 7, 8, 9                               |

### 📊 mv_lifecycle_cohorts

| Tipo   | Columna         | Dato    |   Completitud % |   Unicos | Muestra                                                             |
|:-------|:----------------|:--------|----------------:|---------:|:--------------------------------------------------------------------|
| M-View | snapshot_date   | date    |           100   |       75 | Valores múltiples (+75) | Ej: 2020-12-31, 2023-04-30, 2025-04-30... |
| M-View | tenure_cohort   | text    |           100   |        5 | 0-6 meses, 1-2 años, 2-4 años, 4+ años, 6-12 meses                  |
| M-View | department_name | text    |           100   |        5 | Finance, HR, IT, Operations, Sales                                  |
| M-View | country_iso3    | text    |           100   |        6 | CHL, COL, ESP, MEX, PER, USA                                        |
| M-View | job_level_1     | text    |           100   |        2 | Individual Contributor, Management                                  |
| M-View | activos         | bigint  |           100   |      125 | Valores múltiples (+125) | Ej: 71, 118, 123...                      |
| M-View | bajas           | bigint  |           100   |       40 | Valores múltiples (+40) | Ej: 8, 12, 10...                          |
| M-View | avg_salary      | numeric |            91.7 |     9614 | Valores múltiples (+9,614) | Ej: 567.61, 657.70, 906.60...          |
| M-View | tasa_rotacion   | numeric |           100   |      386 | Valores múltiples (+386) | Ej: 21.4, 35.0, 5.7...                   |

### 📊 mv_manager_turnover

| Tipo   | Columna               | Dato    |   Completitud % |   Unicos | Muestra                                                                    |
|:-------|:----------------------|:--------|----------------:|---------:|:---------------------------------------------------------------------------|
| M-View | snapshot_date         | date    |             100 |       75 | Valores múltiples (+75) | Ej: 2020-12-31, 2023-04-30, 2025-04-30...        |
| M-View | manager_employee_id   | integer |             100 |      605 | Valores múltiples (+605) | Ej: 909, 2042, 1968...                          |
| M-View | manager_name          | text    |             100 |       56 | Valores múltiples (+56) | Ej: Juan Rodriguez, Lucia Torres, Sofia Gomez... |
| M-View | department_name       | text    |             100 |        5 | Finance, HR, IT, Operations, Sales                                         |
| M-View | subordinates_lost     | bigint  |             100 |       10 | 0, 1, 2, 3, 4, 5, 6, 7, 8, 9                                               |
| M-View | total_subordinates    | bigint  |             100 |       37 | Valores múltiples (+37) | Ej: 8, 12, 10...                                 |
| M-View | manager_turnover_rate | numeric |             100 |      111 | Valores múltiples (+111) | Ej: 10.5, 10.3, 21.1...                         |

### 📊 mv_monthly_kpis_bynapo

| Tipo   | Columna              | Dato    |   Completitud % |   Unicos | Muestra                                                             |
|:-------|:---------------------|:--------|----------------:|---------:|:--------------------------------------------------------------------|
| M-View | snapshot_date        | date    |             100 |       75 | Valores múltiples (+75) | Ej: 2020-12-31, 2023-04-30, 2025-04-30... |
| M-View | country_iso3         | text    |             100 |        6 | CHL, COL, ESP, MEX, PER, USA                                        |
| M-View | headcount_active     | bigint  |             100 |      221 | Valores múltiples (+221) | Ej: 862, 716, 780...                     |
| M-View | headcount_terminated | bigint  |             100 |      242 | Valores múltiples (+242) | Ej: 75, 247, 13...                       |
| M-View | avg_salary_usd       | numeric |             100 |      443 | Valores múltiples (+443) | Ej: 812.54, 888.69, 796.42...            |
| M-View | avg_tenure           | numeric |             100 |      287 | Valores múltiples (+287) | Ej: 48.3, 59.1, 52.5...                  |

### 📊 mv_nine_box

| Tipo   | Columna           | Dato    |   Completitud % |   Unicos | Muestra                            |
|:-------|:------------------|:--------|----------------:|---------:|:-----------------------------------|
| M-View | nine_box_quadrant | text    |             100 |        1 | Core Player                        |
| M-View | department_name   | text    |             100 |        5 | Finance, HR, IT, Operations, Sales |
| M-View | employee_count    | bigint  |             100 |        5 | 67517, 69807, 71074, 71742, 73374  |
| M-View | avg_performance   | numeric |             100 |        1 | 2.0                                |
| M-View | avg_potential     | numeric |             100 |        1 | 2.0                                |

### 📊 mv_onboarding_status

| Tipo   | Columna         | Dato    |   Completitud % |   Unicos | Muestra                                                             |
|:-------|:----------------|:--------|----------------:|---------:|:--------------------------------------------------------------------|
| M-View | snapshot_date   | date    |             100 |       75 | Valores múltiples (+75) | Ej: 2020-12-31, 2023-04-30, 2025-04-30... |
| M-View | department_name | text    |             100 |        5 | Finance, HR, IT, Operations, Sales                                  |
| M-View | country_iso3    | text    |             100 |        6 | CHL, COL, ESP, MEX, PER, USA                                        |
| M-View | total_procesos  | bigint  |             100 |       16 | 1, 10, 11, 12, 13, 14, 15, 16, 2, 3, 4, 5, 6, 7, 8, 9               |
| M-View | completados     | bigint  |             100 |       16 | 1, 10, 11, 12, 13, 14, 15, 16, 2, 3, 4, 5, 6, 7, 8, 9               |
| M-View | vencidos        | bigint  |             100 |       13 | 0, 1, 10, 11, 12, 2, 3, 4, 5, 6, 7, 8, 9                            |
| M-View | pct_completado  | numeric |             100 |       82 | Valores múltiples (+82) | Ej: 85.5, 76.7, 83.6...                   |

### 📊 mv_overtime_summary

| Tipo   | Columna             | Dato    |   Completitud % |   Unicos | Muestra                                                                                                                                                |
|:-------|:--------------------|:--------|----------------:|---------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
| M-View | periodo             | date    |             100 |        1 | 2024-02-01                                                                                                                                             |
| M-View | department_name     | text    |             100 |        5 | Finance, HR, IT, Operations, Sales                                                                                                                     |
| M-View | country_iso3        | text    |             100 |        6 | CHL, COL, ESP, MEX, PER, USA                                                                                                                           |
| M-View | total_horas_extra   | numeric |             100 |       30 | 10660, 10888, 11726, 12968, 13037, 13275, 13498, 13709, 13729, 13841, 13955, 14050, 14427, 14748, 14901, 15072, 15718, 15835, 16085, 16319, 16615, 167 |
| M-View | costo_total_extra   | numeric |             100 |       30 | 255402, 268122, 273126, 275807, 277698, 299041, 301630, 302034, 306978, 309127, 327280, 330137, 332208, 333418, 352145, 356101, 357285, 359122, 367664 |
| M-View | empleados_con_extra | bigint  |             100 |       17 | 36, 37, 38, 42, 43, 44, 46, 47, 49, 50, 51, 52, 53, 54, 56, 62, 64                                                                                     |

### 📊 mv_payroll_mass

| Tipo   | Columna           | Dato          |   Completitud % |   Unicos | Muestra                                                             |
|:-------|:------------------|:--------------|----------------:|---------:|:--------------------------------------------------------------------|
| M-View | snapshot_date     | date          |             100 |       75 | Valores múltiples (+75) | Ej: 2020-12-31, 2023-04-30, 2025-04-30... |
| M-View | department_name   | text          |             100 |        5 | Finance, HR, IT, Operations, Sales                                  |
| M-View | country_iso3      | text          |             100 |        6 | CHL, COL, ESP, MEX, PER, USA                                        |
| M-View | job_level_1       | text          |             100 |        2 | Individual Contributor, Management                                  |
| M-View | total_payroll_usd | numeric(14,2) |             100 |     2284 | Valores múltiples (+2,284) | Ej: 112538.79, 110996.74, 10351.00...  |
| M-View | headcount         | bigint        |             100 |      120 | Valores múltiples (+120) | Ej: 118, 123, 8...                       |
| M-View | avg_salary_usd    | numeric(12,2) |             100 |     2199 | Valores múltiples (+2,199) | Ej: 729.96, 904.54, 842.78...          |

### 📊 mv_performance_summary

| Tipo   | Columna         | Dato    |   Completitud % |   Unicos | Muestra                                                                                                                                                |
|:-------|:----------------|:--------|----------------:|---------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
| M-View | review_cycle    | text    |             100 |        1 | 2024-Q1                                                                                                                                                |
| M-View | department_name | text    |             100 |        5 | Finance, HR, IT, Operations, Sales                                                                                                                     |
| M-View | country_iso3    | text    |             100 |        6 | CHL, COL, ESP, MEX, PER, USA                                                                                                                           |
| M-View | total_reviews   | bigint  |             100 |       30 | 10165, 10234, 10439, 10537, 10553, 10564, 10649, 11307, 11374, 11498, 11551, 11585, 11596, 11733, 11752, 11758, 11859, 11873, 11879, 11967, 12041, 120 |
| M-View | avg_rating      | numeric |             100 |        4 | 3.6, 3.7, 3.8, 3.9                                                                                                                                     |
| M-View | high_performers | bigint  |             100 |       30 | 3993, 4115, 4237, 4248, 4366, 4389, 4405, 4512, 4532, 4587, 4613, 4647, 4686, 4692, 4742, 4882, 4942, 4956, 4968, 5042, 5092, 5244, 5258, 5438, 5459,  |
| M-View | low_performers  | bigint  |             100 |        1 | 0                                                                                                                                                      |

### 📊 mv_recruitment_funnel

| Tipo   | Columna             | Dato    |   Completitud % |   Unicos | Muestra                                                                                                           |
|:-------|:--------------------|:--------|----------------:|---------:|:------------------------------------------------------------------------------------------------------------------|
| M-View | periodo             | date    |             100 |      138 | Valores múltiples (+138) | Ej: 2017-06-01, 2016-06-01, 2024-05-01...                                              |
| M-View | department_name     | text    |             100 |        5 | Finance, HR, IT, Operations, Sales                                                                                |
| M-View | country_iso3        | text    |             100 |        6 | CHL, COL, ESP, MEX, PER, USA                                                                                      |
| M-View | applied             | bigint  |             100 |       41 | Valores múltiples (+41) | Ej: 15, 47, 28...                                                                       |
| M-View | screened            | bigint  |             100 |       35 | Valores múltiples (+35) | Ej: 12, 10, 13...                                                                       |
| M-View | interviewed         | bigint  |             100 |       30 | 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 33, 35, 36, 38, 5, 6, 7, 8, 9 |
| M-View | offered             | bigint  |             100 |       26 | 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28, 3, 30, 4, 5, 6, 7, 8, 9                   |
| M-View | hired               | bigint  |             100 |       25 | 1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 2, 20, 21, 22, 23, 26, 27, 3, 4, 5, 6, 7, 8, 9                         |
| M-View | avg_interview_score | numeric |             100 |      512 | Valores múltiples (+512) | Ej: 74.15, 77.59, 85.00...                                                             |
| M-View | avg_nps             | numeric |             100 |      178 | Valores múltiples (+178) | Ej: 5.81, 6.82, 5.41...                                                                |

### 📊 mv_salary_bands

| Tipo   | Columna         | Dato             |   Completitud % |   Unicos | Muestra                                                                                                                                                |
|:-------|:----------------|:-----------------|----------------:|---------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
| M-View | snapshot_date   | date             |           100   |       75 | Valores múltiples (+75) | Ej: 2020-12-31, 2023-04-30, 2025-04-30...                                                                                    |
| M-View | department_name | text             |           100   |        5 | Finance, HR, IT, Operations, Sales                                                                                                                     |
| M-View | job_level_1     | text             |           100   |        2 | Individual Contributor, Management                                                                                                                     |
| M-View | job_level_2     | text             |           100   |        3 | Junior, Lead, Senior                                                                                                                                   |
| M-View | job_role        | text             |           100   |       17 | Account Manager, Accountant, CEO, CFO, CTO, Data Analyst, DevOps, Financial Analyst, HR Manager, HR Specialist, Logistics Coord, Operator, Ops Directo |
| M-View | country_iso3    | text             |           100   |        6 | CHL, COL, ESP, MEX, PER, USA                                                                                                                           |
| M-View | p10             | double precision |           100   |     5885 | Valores múltiples (+5,885) | Ej: 419.909, 440.825, 368.15...                                                                                           |
| M-View | p25             | double precision |           100   |     5679 | Valores múltiples (+5,679) | Ej: 971.795, 858.87, 938.385...                                                                                           |
| M-View | p50_median      | double precision |           100   |     4984 | Valores múltiples (+4,984) | Ej: 734.32, 823.43, 778.17...                                                                                             |
| M-View | p75             | double precision |           100   |     5661 | Valores múltiples (+5,661) | Ej: 758.955, 1226.19, 1232.185...                                                                                         |
| M-View | p90             | double precision |           100   |     5853 | Valores múltiples (+5,853) | Ej: 806.943, 1188.524, 895.72...                                                                                          |
| M-View | avg_salary      | numeric(12,2)    |           100   |     6032 | Valores múltiples (+6,032) | Ej: 1058.90, 748.44, 681.00...                                                                                            |
| M-View | stddev_salary   | numeric(12,2)    |            84.8 |     5267 | Valores múltiples (+5,267) | Ej: 160.69, 113.63, 278.01...                                                                                             |
| M-View | employee_count  | bigint           |           100   |       39 | Valores múltiples (+39) | Ej: 8, 12, 10...                                                                                                             |

### 📊 mv_sentiment_summary

| Tipo   | Columna         | Dato    |   Completitud % |   Unicos | Muestra                     |
|:-------|:----------------|:--------|----------------:|---------:|:----------------------------|
| M-View | periodo         | date    |             100 |        1 | 2024-01-01                  |
| M-View | sentiment_label | text    |             100 |        3 | Negative, Neutral, Positive |
| M-View | total_comments  | bigint  |             100 |        3 | 1299, 216, 628              |
| M-View | avg_sentiment   | numeric |             100 |        3 | 0.20, 0.50, 0.80            |

### 📊 mv_sst_incidents

| Tipo   | Columna          | Dato   |   Completitud % |   Unicos | Muestra         |
|:-------|:-----------------|:-------|----------------:|---------:|:----------------|
| M-View | periodo          | date   |             100 |        1 | 2024-03-01      |
| M-View | severity         | text   |             100 |        2 | Minor, Moderate |
| M-View | incident_type    | text   |             100 |        1 | Slip            |
| M-View | total_incidentes | bigint |             100 |        2 | 167, 171        |
| M-View | dias_perdidos    | bigint |             100 |        2 | 308, 347        |

### 📊 mv_time_to_fill

| Tipo   | Columna          | Dato             |   Completitud % |   Unicos | Muestra                                                              |
|:-------|:-----------------|:-----------------|----------------:|---------:|:---------------------------------------------------------------------|
| M-View | department_name  | text             |             100 |        5 | Finance, HR, IT, Operations, Sales                                   |
| M-View | country_iso3     | text             |             100 |        6 | CHL, COL, ESP, MEX, PER, USA                                         |
| M-View | periodo          | date             |             100 |      138 | Valores múltiples (+138) | Ej: 2017-06-01, 2016-06-01, 2024-05-01... |
| M-View | avg_days_to_fill | numeric          |             100 |       47 | Valores múltiples (+47) | Ej: 36.00, 30.00, 51.00...                 |
| M-View | median_days      | double precision |             100 |       47 | Valores múltiples (+47) | Ej: 54, 55.5, 47...                        |
| M-View | total_postings   | bigint           |             100 |        2 | 1, 2                                                                 |

### 📊 mv_training_roi

| Tipo   | Columna                 | Dato    |   Completitud % |   Unicos | Muestra        |
|:-------|:------------------------|:--------|----------------:|---------:|:---------------|
| M-View | category                | text    |             100 |        1 | Soft Skills    |
| M-View | program_name            | text    |             100 |        1 | Leadership 101 |
| M-View | enrolled                | bigint  |             100 |        1 | 7000           |
| M-View | completed               | bigint  |             100 |        1 | 7000           |
| M-View | completion_rate         | numeric |             100 |        1 | 100.0          |
| M-View | avg_post_training_score | numeric |             100 |        1 | 84.6           |
| M-View | costo_total             | numeric |             100 |        1 | 0              |

### 📊 mv_turnover_analysis

| Tipo   | Columna               | Dato    |   Completitud % |   Unicos | Muestra                                                             |
|:-------|:----------------------|:--------|----------------:|---------:|:--------------------------------------------------------------------|
| M-View | snapshot_date         | date    |             100 |       75 | Valores múltiples (+75) | Ej: 2020-12-31, 2023-04-30, 2025-04-30... |
| M-View | department_name       | text    |             100 |        5 | Finance, HR, IT, Operations, Sales                                  |
| M-View | country_iso3          | text    |             100 |        6 | CHL, COL, ESP, MEX, PER, USA                                        |
| M-View | job_level_1           | text    |             100 |        2 | Individual Contributor, Management                                  |
| M-View | activos               | bigint  |             100 |      120 | Valores múltiples (+120) | Ej: 118, 123, 8...                       |
| M-View | bajas                 | bigint  |             100 |        5 | 0, 1, 2, 3, 4                                                       |
| M-View | tasa_rotacion_mensual | numeric |             100 |      174 | Valores múltiples (+174) | Ej: 1.83, 1.43, 0.62...                  |

### 📊 mv_turnover_cost

| Tipo   | Columna                  | Dato          |   Completitud % |   Unicos | Muestra                                                             |
|:-------|:-------------------------|:--------------|----------------:|---------:|:--------------------------------------------------------------------|
| M-View | snapshot_date            | date          |           100   |       75 | Valores múltiples (+75) | Ej: 2020-12-31, 2023-04-30, 2025-04-30... |
| M-View | department_name          | text          |           100   |        5 | Finance, HR, IT, Operations, Sales                                  |
| M-View | country_iso3             | text          |           100   |        6 | CHL, COL, ESP, MEX, PER, USA                                        |
| M-View | bajas_mes                | bigint        |           100   |        5 | 0, 1, 2, 3, 4                                                       |
| M-View | costo_bajas_usd          | numeric(14,2) |            53.6 |     1202 | Valores múltiples (+1,202) | Ej: 1661.47, 3208.48, 524.24...        |
| M-View | costo_reemplazo_estimado | numeric(14,2) |            53.6 |     1202 | Valores múltiples (+1,202) | Ej: 2662.68, 1312.80, 3612.00...       |

### 📊 mv_ui_global_filters

| Tipo   | Columna        | Dato   |   Completitud % |   Unicos | Muestra                                                                                                                                                |
|:-------|:---------------|:-------|----------------:|---------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
| M-View | filter_options | json   |             100 |        1 | {"periods" : ["2026-03-31", "2026-02-28", "2026-01-31", "2025-12-31", "2025-11-30", "2025-10-31", "2025-09-30", "2025-08-31", "2025-07-31", "2025-06-3 |

### 📊 v_data_quality_metrics

| Tipo   | Columna              | Dato    |   Completitud % |   Unicos | Muestra                |
|:-------|:---------------------|:--------|----------------:|---------:|:-----------------------|
| Vista  | source_table         | text    |             100 |        1 | v_employee_full_byNapo |
| Vista  | total_records        | bigint  |             100 |        1 | 414000                 |
| Vista  | unique_employees     | bigint  |             100 |        1 | 7000                   |
| Vista  | total_snapshots      | bigint  |             100 |        1 | 75                     |
| Vista  | completeness_salary  | numeric |             100 |        1 | 100.00                 |
| Vista  | completeness_manager | numeric |             100 |        1 | 99.98                  |
| Vista  | completeness_country | numeric |             100 |        1 | 100.00                 |

### 📊 v_employee_full_bynapo

| Tipo   | Columna               | Dato                     |   Completitud % |   Unicos | Muestra                                                                                                                                                |
|:-------|:----------------------|:-------------------------|----------------:|---------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
| Vista  | snapshot_date         | date                     |             100 |       75 | Valores múltiples (+75) | Ej: 2020-01-31, 2020-02-29, 2020-03-31...                                                                                    |
| Vista  | employee_id           | integer                  |             100 |     7000 | Valores múltiples (+7,000) | Ej: 1, 10, 100...                                                                                                         |
| Vista  | employee_code         | text                     |             100 |     7000 | Valores múltiples (+7,000) | Ej: EMP-00001, EMP-00002, EMP-00003...                                                                                    |
| Vista  | full_name             | text                     |             100 |       56 | Valores múltiples (+56) | Ej: Ana Gomez, Ana Lopez, Ana Martinez...                                                                                    |
| Vista  | gender                | text                     |             100 |        2 | Female, Male                                                                                                                                           |
| Vista  | country_iso3          | text                     |             100 |        6 | CHL, COL, ESP, MEX, PER, USA                                                                                                                           |
| Vista  | department_name       | text                     |             100 |        5 | Finance, HR, IT, Operations, Sales                                                                                                                     |
| Vista  | job_role              | text                     |             100 |       17 | Account Manager, Accountant, CEO, CFO, CTO, Data Analyst, DevOps, Financial Analyst, HR Manager, HR Specialist, Logistics Coord, Operator, Ops Directo |
| Vista  | job_level_1           | text                     |             100 |        2 | Individual Contributor, Management                                                                                                                     |
| Vista  | job_level_2           | text                     |             100 |        3 | Junior, Lead, Senior                                                                                                                                   |
| Vista  | employment_status     | text                     |             100 |        2 | Active, Terminated                                                                                                                                     |
| Vista  | hire_date             | date                     |             100 |     1734 | Valores múltiples (+1,734) | Ej: 2014-07-12, 2014-07-13, 2014-07-14...                                                                                 |
| Vista  | termination_date      | date                     |              15 |       75 | Valores múltiples (+75) | Ej: 2020-01-31, 2020-02-29, 2020-03-31...                                                                                    |
| Vista  | monthly_salary_local  | numeric(12,2)            |             100 |    21794 | Valores múltiples (+21,794) | Ej: 1000.74, 1002.12, 1002.24...                                                                                         |
| Vista  | currency_iso3         | text                     |             100 |        6 | CLP, COP, EUR, MXN, PEN, USD                                                                                                                           |
| Vista  | fx_rate_to_usd        | numeric(10,4)            |             100 |        1 | 3.5000                                                                                                                                                 |
| Vista  | monthly_salary_usd    | numeric(12,2)            |             100 |    20445 | Valores múltiples (+20,445) | Ej: 1000.06, 1000.09, 1000.10...                                                                                         |
| Vista  | work_center_id        | text                     |             100 |        6 | WC-CHL, WC-COL, WC-ESP, WC-MEX, WC-PER, WC-USA                                                                                                         |
| Vista  | manager_employee_id   | integer                  |             100 |      605 | Valores múltiples (+605) | Ej: 1, 1005, 1011...                                                                                                        |
| Vista  | tenure_months         | numeric                  |             100 |      141 | Valores múltiples (+141) | Ej: 0, 1, 10...                                                                                                             |
| Vista  | is_active_at_snapshot | boolean                  |             100 |        2 | false, true                                                                                                                                            |
| Vista  | processed_at          | timestamp with time zone |             100 |        1 | 2026-05-03 16:52:33.641047+00                                                                                                                          |

### 📊 v_org_tree_bynapo

| Tipo   | Columna      | Dato    |   Completitud % |   Unicos | Muestra                                                                                                                                                |
|:-------|:-------------|:--------|----------------:|---------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
| Vista  | employee_id  | integer |             100 |      298 | Valores múltiples (+298) | Ej: 6470, 6635, 6107...                                                                                                     |
| Vista  | full_name    | text    |             100 |       56 | Valores múltiples (+56) | Ej: Juan Martinez, Ana Gomez, Luis Torres...                                                                                 |
| Vista  | job_role     | text    |             100 |       17 | Account Manager, Accountant, CEO, CFO, CTO, Data Analyst, DevOps, Financial Analyst, HR Manager, HR Specialist, Logistics Coord, Operator, Ops Directo |
| Vista  | job_level_1  | text    |             100 |        2 | Individual Contributor, Management                                                                                                                     |
| Vista  | depth        | integer |             100 |       11 | 0, 1, 10, 2, 3, 4, 5, 6, 7, 8, 9                                                                                                                       |
| Vista  | echarts_node | json    |             100 |      298 | Valores múltiples (+298) | Ej: {"id" : 1312, "name" : "Luis Lopez", "value" : "Individual Contributor", "children" : null}, {"id" : 3448, "name" : "Pe |

## 📂 Esquema: `raw`

### 📊 attendance_records_byNapo

| Tipo   | Columna         | Dato                     |   Completitud % |   Unicos | Muestra                                                                                            |
|:-------|:----------------|:-------------------------|----------------:|---------:|:---------------------------------------------------------------------------------------------------|
| Tabla  | record_id       | text                     |             100 |   351798 | Valores múltiples (+351,798) | Ej: ATT-2490-2020-01-31, ATT-3101-2020-02-29, ATT-100-2020-02-29... |
| Tabla  | employee_id     | text                     |             100 |     6981 | Valores múltiples (+6,981) | Ej: 1, 10, 100...                                                     |
| Tabla  | work_date       | text                     |             100 |       75 | Valores múltiples (+75) | Ej: 2020-01-31, 2020-02-29, 2020-03-31...                                |
| Tabla  | check_in_time   | text                     |             100 |        1 | 09:00                                                                                              |
| Tabla  | check_out_time  | text                     |             100 |        1 | 18:00                                                                                              |
| Tabla  | scheduled_hours | text                     |             100 |        1 | 160                                                                                                |
| Tabla  | worked_hours    | text                     |             100 |       16 | 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160                     |
| Tabla  | absence_type    | text                     |             100 |        3 | Present, Sick, Vacation                                                                            |
| Tabla  | late_minutes    | text                     |             100 |       60 | Valores múltiples (+60) | Ej: 0, 1, 10...                                                          |
| Tabla  | work_modality   | text                     |             100 |        1 | Remote                                                                                             |
| Tabla  | created_at      | timestamp with time zone |             100 |        1 | 2026-05-03 16:49:49.334063+00                                                                      |

### 📊 compliance_obligations_byNapo

| Tipo   | Columna           | Dato                     |   Completitud % |   Unicos | Muestra                                                                                                                      |
|:-------|:------------------|:-------------------------|----------------:|---------:|:-----------------------------------------------------------------------------------------------------------------------------|
| Tabla  | obligation_id     | text                     |             100 |        6 | COMP-CHL-01, COMP-COL-01, COMP-ESP-01, COMP-MEX-01, COMP-PER-01, COMP-USA-01                                                 |
| Tabla  | obligation_type   | text                     |             100 |        1 | Labor Law                                                                                                                    |
| Tabla  | description       | text                     |             100 |        6 | Annual HR Audit CHL, Annual HR Audit COL, Annual HR Audit ESP, Annual HR Audit MEX, Annual HR Audit PER, Annual HR Audit USA |
| Tabla  | country_iso3      | text                     |             100 |        6 | CHL, COL, ESP, MEX, PER, USA                                                                                                 |
| Tabla  | due_date          | text                     |             100 |        1 | 2024-12-31                                                                                                                   |
| Tabla  | frequency         | text                     |             100 |        1 | Annual                                                                                                                       |
| Tabla  | responsible_party | text                     |             100 |        1 | HR Director                                                                                                                  |
| Tabla  | status            | text                     |             100 |        1 | Compliant                                                                                                                    |
| Tabla  | risk_level        | text                     |             100 |        1 | High                                                                                                                         |
| Tabla  | created_at        | timestamp with time zone |             100 |        1 | 2026-05-03 16:50:48.325202+00                                                                                                |

### 📊 continuous_feedback_byNapo

| Tipo   | Columna     | Dato                     |   Completitud % |   Unicos | Muestra         |
|:-------|:------------|:-------------------------|----------------:|---------:|:----------------|
| Tabla  | feedback_id | text                     |               0 |        0 | [Columna Vacía] |
| Tabla  | employee_id | text                     |               0 |        0 | [Columna Vacía] |
| Tabla  | created_at  | timestamp with time zone |               0 |        0 | [Columna Vacía] |

### 📊 feedback_comments_byNapo

| Tipo   | Columna         | Dato                     |   Completitud % |   Unicos | Muestra                                                                     |
|:-------|:----------------|:-------------------------|----------------:|---------:|:----------------------------------------------------------------------------|
| Tabla  | feedback_id     | text                     |             100 |     2143 | Valores múltiples (+2,143) | Ej: FB-2039-2024, FB-2586-2024, FB-881-2024... |
| Tabla  | employee_id     | text                     |             100 |     2143 | Valores múltiples (+2,143) | Ej: 5797, 4905, 3542...                        |
| Tabla  | feedback_date   | text                     |             100 |        1 | 2024-03-15                                                                  |
| Tabla  | source_channel  | text                     |             100 |        1 | Pulse Survey                                                                |
| Tabla  | sentiment_label | text                     |             100 |        3 | Negative, Neutral, Positive                                                 |
| Tabla  | sentiment_score | text                     |             100 |        3 | 0.2, 0.5, 0.8                                                               |
| Tabla  | key_topics      | text                     |             100 |        1 | Work-Life Balance                                                           |
| Tabla  | created_at      | timestamp with time zone |             100 |        1 | 2026-05-03 16:50:47.4253+00                                                 |

### 📊 goals_okrs_byNapo

| Tipo   | Columna     | Dato                     |   Completitud % |   Unicos | Muestra         |
|:-------|:------------|:-------------------------|----------------:|---------:|:----------------|
| Tabla  | goal_id     | text                     |               0 |        0 | [Columna Vacía] |
| Tabla  | employee_id | text                     |               0 |        0 | [Columna Vacía] |
| Tabla  | created_at  | timestamp with time zone |               0 |        0 | [Columna Vacía] |

### 📊 ibm_hr_change_reasons_byNapo

| Tipo   | Columna        | Dato                     |   Completitud % |   Unicos | Muestra                                                                            |
|:-------|:---------------|:-------------------------|----------------:|---------:|:-----------------------------------------------------------------------------------|
| Tabla  | reason_code    | text                     |             100 |        4 | SAL-IPC, TER-INV, TER-RET, TER-VOL                                                 |
| Tabla  | reason_name_es | text                     |             100 |        4 | Ajuste por Inflación (IPC), Despido Injustificado, Jubilación, Renuncia Voluntaria |
| Tabla  | reason_name_en | text                     |             100 |        4 | Inflation Adjustment, Involuntary Termination, Retirement, Voluntary Resignation   |
| Tabla  | affects_salary | text                     |             100 |        2 | N, Y                                                                               |
| Tabla  | affects_job    | text                     |             100 |        2 | N, Y                                                                               |
| Tabla  | active_flag    | text                     |             100 |        1 | Y                                                                                  |
| Tabla  | created_at     | timestamp with time zone |             100 |        1 | 2026-05-03 16:49:35.694479+00                                                      |

### 📊 ibm_hr_landing

| Tipo   | Columna                  | Dato                     |   Completitud % |   Unicos | Muestra                                                                                                                                                |
|:-------|:-------------------------|:-------------------------|----------------:|---------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
| Tabla  | age                      | text                     |             100 |       43 | Valores múltiples (+43) | Ej: 54, 47, 28...                                                                                                            |
| Tabla  | attrition                | text                     |             100 |        2 | No, Yes                                                                                                                                                |
| Tabla  | businesstravel           | text                     |             100 |        3 | Non-Travel, Travel_Frequently, Travel_Rarely                                                                                                           |
| Tabla  | dailyrate                | text                     |             100 |      886 | Valores múltiples (+886) | Ej: 461, 711, 791...                                                                                                        |
| Tabla  | department               | text                     |             100 |        3 | Human Resources, Research & Development, Sales                                                                                                         |
| Tabla  | distancefromhome         | text                     |             100 |       29 | 1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 2, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 3, 4, 5, 6, 7, 8, 9                                              |
| Tabla  | education                | text                     |             100 |        5 | 1, 2, 3, 4, 5                                                                                                                                          |
| Tabla  | educationfield           | text                     |             100 |        6 | Human Resources, Life Sciences, Marketing, Medical, Other, Technical Degree                                                                            |
| Tabla  | employeecount            | text                     |             100 |        1 | 1                                                                                                                                                      |
| Tabla  | employeenumber           | text                     |             100 |     1470 | Valores múltiples (+1,470) | Ej: 1318, 1562, 551...                                                                                                    |
| Tabla  | environmentsatisfaction  | text                     |             100 |        4 | 1, 2, 3, 4                                                                                                                                             |
| Tabla  | gender                   | text                     |             100 |        2 | Female, Male                                                                                                                                           |
| Tabla  | hourlyrate               | text                     |             100 |       71 | Valores múltiples (+71) | Ej: 75, 96, 39...                                                                                                            |
| Tabla  | jobinvolvement           | text                     |             100 |        4 | 1, 2, 3, 4                                                                                                                                             |
| Tabla  | joblevel                 | text                     |             100 |        5 | 1, 2, 3, 4, 5                                                                                                                                          |
| Tabla  | jobrole                  | text                     |             100 |        9 | Healthcare Representative, Human Resources, Laboratory Technician, Manager, Manufacturing Director, Research Director, Research Scientist, Sales Execu |
| Tabla  | jobsatisfaction          | text                     |             100 |        4 | 1, 2, 3, 4                                                                                                                                             |
| Tabla  | maritalstatus            | text                     |             100 |        3 | Divorced, Married, Single                                                                                                                              |
| Tabla  | monthlyincome            | text                     |             100 |     1349 | Valores múltiples (+1,349) | Ej: 2571, 10048, 2585...                                                                                                  |
| Tabla  | monthlyrate              | text                     |             100 |     1427 | Valores múltiples (+1,427) | Ej: 7172, 4905, 20165...                                                                                                  |
| Tabla  | numcompaniesworked       | text                     |             100 |       10 | 0, 1, 2, 3, 4, 5, 6, 7, 8, 9                                                                                                                           |
| Tabla  | over18                   | text                     |             100 |        1 | Y                                                                                                                                                      |
| Tabla  | overtime                 | text                     |             100 |        2 | No, Yes                                                                                                                                                |
| Tabla  | percentsalaryhike        | text                     |             100 |       15 | 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25                                                                                             |
| Tabla  | performancerating        | text                     |             100 |        2 | 3, 4                                                                                                                                                   |
| Tabla  | relationshipsatisfaction | text                     |             100 |        4 | 1, 2, 3, 4                                                                                                                                             |
| Tabla  | standardhours            | text                     |             100 |        1 | 80                                                                                                                                                     |
| Tabla  | stockoptionlevel         | text                     |             100 |        4 | 0, 1, 2, 3                                                                                                                                             |
| Tabla  | totalworkingyears        | text                     |             100 |       40 | Valores múltiples (+40) | Ej: 8, 12, 10...                                                                                                             |
| Tabla  | trainingtimeslastyear    | text                     |             100 |        7 | 0, 1, 2, 3, 4, 5, 6                                                                                                                                    |
| Tabla  | worklifebalance          | text                     |             100 |        4 | 1, 2, 3, 4                                                                                                                                             |
| Tabla  | yearsatcompany           | text                     |             100 |       37 | Valores múltiples (+37) | Ej: 8, 12, 10...                                                                                                             |
| Tabla  | yearsincurrentrole       | text                     |             100 |       19 | 0, 1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 2, 3, 4, 5, 6, 7, 8, 9                                                                                       |
| Tabla  | yearssincelastpromotion  | text                     |             100 |       16 | 0, 1, 10, 11, 12, 13, 14, 15, 2, 3, 4, 5, 6, 7, 8, 9                                                                                                   |
| Tabla  | yearswithcurrmanager     | text                     |             100 |       18 | 0, 1, 10, 11, 12, 13, 14, 15, 16, 17, 2, 3, 4, 5, 6, 7, 8, 9                                                                                           |
| Tabla  | created_at               | timestamp with time zone |             100 |        1 | 2026-04-08 22:15:23.287671+00                                                                                                                          |

### 📊 ibm_hr_monthly_snapshot_byNapo

| Tipo   | Columna                         | Dato                     |   Completitud % |   Unicos | Muestra                                                                                                                                                |
|:-------|:--------------------------------|:-------------------------|----------------:|---------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
| Tabla  | snapshot_date                   | text                     |           100   |       75 | Valores múltiples (+75) | Ej: 2020-01-31, 2020-02-29, 2020-03-31...                                                                                    |
| Tabla  | employee_id                     | text                     |           100   |     7000 | Valores múltiples (+7,000) | Ej: 1, 10, 100...                                                                                                         |
| Tabla  | employee_code                   | text                     |           100   |     7000 | Valores múltiples (+7,000) | Ej: EMP-00001, EMP-00002, EMP-00003...                                                                                    |
| Tabla  | full_name                       | text                     |           100   |       56 | Valores múltiples (+56) | Ej: Ana Gomez, Ana Lopez, Ana Martinez...                                                                                    |
| Tabla  | gender                          | text                     |           100   |        2 | Female, Male                                                                                                                                           |
| Tabla  | nationality_iso3                | text                     |           100   |        6 | CHL, COL, ESP, MEX, PER, USA                                                                                                                           |
| Tabla  | country_iso3                    | text                     |           100   |        6 | CHL, COL, ESP, MEX, PER, USA                                                                                                                           |
| Tabla  | department_name                 | text                     |           100   |        5 | Finance, HR, IT, Operations, Sales                                                                                                                     |
| Tabla  | job_role                        | text                     |           100   |       17 | Account Manager, Accountant, CEO, CFO, CTO, Data Analyst, DevOps, Financial Analyst, HR Manager, HR Specialist, Logistics Coord, Operator, Ops Directo |
| Tabla  | job_level_1                     | text                     |           100   |        2 | Individual Contributor, Management                                                                                                                     |
| Tabla  | job_level_2                     | text                     |           100   |        3 | Junior, Lead, Senior                                                                                                                                   |
| Tabla  | employment_status               | text                     |           100   |        2 | Active, Terminated                                                                                                                                     |
| Tabla  | hire_date                       | text                     |           100   |     1734 | Valores múltiples (+1,734) | Ej: 2014-07-12, 2014-07-13, 2014-07-14...                                                                                 |
| Tabla  | termination_date                | text                     |            15   |       75 | Valores múltiples (+75) | Ej: 2020-01-31, 2020-02-29, 2020-03-31...                                                                                    |
| Tabla  | termination_reason_legal        | text                     |            15   |        3 | TER-INV, TER-RET, TER-VOL                                                                                                                              |
| Tabla  | turnover_classification_company | text                     |            15   |        2 | Non-Regrettable, Regrettable                                                                                                                           |
| Tabla  | monthly_salary_local            | text                     |           100   |    22343 | Valores múltiples (+22,343) | Ej: 1183.0524622411729, 3323.3042200612495, 1600.8089334835083...                                                        |
| Tabla  | currency_iso3                   | text                     |           100   |        6 | CLP, COP, EUR, MXN, PEN, USD                                                                                                                           |
| Tabla  | fx_rate_to_usd                  | text                     |           100   |        1 | 3.5                                                                                                                                                    |
| Tabla  | monthly_salary_usd              | text                     |           100   |    20445 | Valores múltiples (+20,445) | Ej: 1035.69, 520.67, 1750.12...                                                                                          |
| Tabla  | manager_employee_id             | text                     |           100   |      605 | Valores múltiples (+605) | Ej: 1, 1005, 1011...                                                                                                        |
| Tabla  | dotted_line_manager_id          | text                     |             0   |        0 | [Columna Vacía]                                                                                                                                        |
| Tabla  | work_center_id                  | text                     |           100   |        6 | WC-CHL, WC-COL, WC-ESP, WC-MEX, WC-PER, WC-USA                                                                                                         |
| Tabla  | home_lat                        | text                     |           100   |     7000 | Valores múltiples (+7,000) | Ej: -11.99640006859341, -11.996508745968951, -11.996525048834043...                                                       |
| Tabla  | home_lon                        | text                     |           100   |     7000 | Valores múltiples (+7,000) | Ej: -3.653817624980314, -3.653907184068688, -3.6539728899878536...                                                        |
| Tabla  | work_modality                   | text                     |           100   |        3 | Hybrid, On-Site, Remote                                                                                                                                |
| Tabla  | education_level                 | text                     |           100   |        4 | Bachelor, Master, PhD, Technical                                                                                                                       |
| Tabla  | education_status                | text                     |           100   |        1 | Graduated                                                                                                                                              |
| Tabla  | marital_status                  | text                     |           100   |        3 | Divorced, Married, Single                                                                                                                              |
| Tabla  | dependents_count                | text                     |           100   |        4 | 0, 1, 2, 3                                                                                                                                             |
| Tabla  | salary_change_flag              | text                     |           100   |        2 | 0, 1                                                                                                                                                   |
| Tabla  | salary_change_reason_code       | text                     |             3.9 |        1 | SAL-IPC                                                                                                                                                |
| Tabla  | job_change_flag                 | text                     |           100   |        1 | 0                                                                                                                                                      |
| Tabla  | exit_interview_completed        | text                     |            15   |        2 | N, Y                                                                                                                                                   |
| Tabla  | regrettable_loss_flag           | text                     |            15   |        2 | N, Y                                                                                                                                                   |
| Tabla  | created_at                      | timestamp with time zone |           100   |        1 | 2026-05-03 16:47:19.050552+00                                                                                                                          |

### 📊 incidents_sst_byNapo

| Tipo   | Columna              | Dato                     |   Completitud % |   Unicos | Muestra                                                                   |
|:-------|:---------------------|:-------------------------|----------------:|---------:|:--------------------------------------------------------------------------|
| Tabla  | incident_id          | text                     |             100 |      338 | Valores múltiples (+338) | Ej: INC-6451-920, INC-333-463, INC-4178-548... |
| Tabla  | employee_id          | text                     |             100 |      338 | Valores múltiples (+338) | Ej: 4924, 2571, 1318...                        |
| Tabla  | incident_date        | text                     |             100 |        1 | 2024-03-15                                                                |
| Tabla  | incident_type        | text                     |             100 |        1 | Slip                                                                      |
| Tabla  | severity             | text                     |             100 |        2 | Minor, Moderate                                                           |
| Tabla  | body_part_affected   | text                     |             100 |        1 | Leg                                                                       |
| Tabla  | location             | text                     |             100 |        1 | Office                                                                    |
| Tabla  | lost_days            | text                     |             100 |        5 | 0, 1, 2, 3, 4                                                             |
| Tabla  | investigation_status | text                     |             100 |        1 | Closed                                                                    |
| Tabla  | created_at           | timestamp with time zone |             100 |        1 | 2026-05-03 16:50:39.804498+00                                             |

### 📊 job_postings_byNapo

| Tipo   | Columna             | Dato                     |   Completitud % |   Unicos | Muestra                                                                                              |
|:-------|:--------------------|:-------------------------|----------------:|---------:|:-----------------------------------------------------------------------------------------------------|
| Tabla  | posting_id          | text                     |             100 |      690 | Valores múltiples (+690) | Ej: POST-2024-12-FIN-4828, POST-2016-10-IT-4181, POST-2025-02-SAL-4950... |
| Tabla  | job_title           | text                     |             100 |        5 | Specialist Finance, Specialist HR, Specialist IT, Specialist Operations, Specialist Sales            |
| Tabla  | department_name     | text                     |             100 |        5 | Finance, HR, IT, Operations, Sales                                                                   |
| Tabla  | country_iso3        | text                     |             100 |        6 | CHL, COL, ESP, MEX, PER, USA                                                                         |
| Tabla  | job_level_1         | text                     |             100 |        1 | Individual Contributor                                                                               |
| Tabla  | job_level_2         | text                     |             100 |        1 | Junior                                                                                               |
| Tabla  | salary_range_min    | text                     |             100 |        1 | 1000                                                                                                 |
| Tabla  | salary_range_max    | text                     |             100 |        1 | 3000                                                                                                 |
| Tabla  | posting_date        | text                     |             100 |      648 | Valores múltiples (+648) | Ej: 2022-11-17, 2017-11-14, 2021-08-17...                                 |
| Tabla  | closing_date        | text                     |             100 |      619 | Valores múltiples (+619) | Ej: 2022-09-05, 2025-10-15, 2023-01-14...                                 |
| Tabla  | status              | text                     |             100 |        1 | Closed                                                                                               |
| Tabla  | positions_available | text                     |             100 |       24 | 1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 2, 20, 21, 22, 23, 27, 3, 4, 5, 6, 7, 8, 9                |
| Tabla  | created_at          | timestamp with time zone |             100 |        1 | 2026-05-03 16:49:36.212279+00                                                                        |

### 📊 leave_requests_byNapo

| Tipo   | Columna         | Dato                     |   Completitud % |   Unicos | Muestra                                                                   |
|:-------|:----------------|:-------------------------|----------------:|---------:|:--------------------------------------------------------------------------|
| Tabla  | leave_id        | text                     |             100 |     7000 | Valores múltiples (+7,000) | Ej: LV-1742-673, LV-4404-654, LV-1083-190... |
| Tabla  | employee_id     | text                     |             100 |     7000 | Valores múltiples (+7,000) | Ej: 2571, 3542, 3226...                      |
| Tabla  | leave_type      | text                     |             100 |        1 | Vacation                                                                  |
| Tabla  | start_date      | text                     |             100 |        1 | 2024-01-10                                                                |
| Tabla  | end_date        | text                     |             100 |        1 | 2024-01-20                                                                |
| Tabla  | total_days      | text                     |             100 |        1 | 10                                                                        |
| Tabla  | balance_before  | text                     |             100 |        1 | 30                                                                        |
| Tabla  | balance_after   | text                     |             100 |        1 | 20                                                                        |
| Tabla  | approval_status | text                     |             100 |        1 | Approved                                                                  |
| Tabla  | created_at      | timestamp with time zone |             100 |        1 | 2026-05-03 16:50:38.435862+00                                             |

### 📊 nine_box_grid_byNapo

| Tipo   | Columna            | Dato                     |   Completitud % |   Unicos | Muestra                                                                      |
|:-------|:-------------------|:-------------------------|----------------:|---------:|:-----------------------------------------------------------------------------|
| Tabla  | grid_id            | text                     |             100 |     7000 | Valores múltiples (+7,000) | Ej: 9B-2250-2024, 9B-2696-2024, 9B-5066-2024... |
| Tabla  | employee_id        | text                     |             100 |     7000 | Valores múltiples (+7,000) | Ej: 2571, 3542, 3226...                         |
| Tabla  | assessment_date    | text                     |             100 |        1 | 2024-01-01                                                                   |
| Tabla  | performance_rating | text                     |             100 |        3 | 1, 2, 3                                                                      |
| Tabla  | potential_rating   | text                     |             100 |        3 | 1, 2, 3                                                                      |
| Tabla  | box_category       | text                     |             100 |        1 | Core Player                                                                  |
| Tabla  | created_at         | timestamp with time zone |             100 |        1 | 2026-05-03 16:50:44.862912+00                                                |

### 📊 onboarding_checklist_byNapo

| Tipo   | Columna         | Dato                     |   Completitud % |   Unicos | Muestra                                                                      |
|:-------|:----------------|:-------------------------|----------------:|---------:|:-----------------------------------------------------------------------------|
| Tabla  | onboarding_id   | text                     |             100 |    35000 | Valores múltiples (+35,000) | Ej: ONB-6208-COM, ONB-5526-MAN, ONB-534-COM... |
| Tabla  | employee_id     | text                     |             100 |     7000 | Valores múltiples (+7,000) | Ej: 2571, 3542, 3226...                         |
| Tabla  | checklist_item  | text                     |             100 |        5 | Compliance Training, Equipment Setup, IT Access, Manager Meet, Orientation   |
| Tabla  | category        | text                     |             100 |        1 | General                                                                      |
| Tabla  | due_date        | text                     |             100 |     1734 | Valores múltiples (+1,734) | Ej: 2017-08-10, 2016-01-05, 2019-07-25...       |
| Tabla  | completion_date | text                     |              85 |     2883 | Valores múltiples (+2,883) | Ej: 2022-02-11, 2015-05-05, 2016-09-24...       |
| Tabla  | status          | text                     |             100 |        2 | Completed, Overdue                                                           |
| Tabla  | created_at      | timestamp with time zone |             100 |        1 | 2026-05-03 16:49:40.539739+00                                                |

### 📊 overtime_logs_byNapo

| Tipo   | Columna         | Dato                     |   Completitud % |   Unicos | Muestra                                                                   |
|:-------|:----------------|:-------------------------|----------------:|---------:|:--------------------------------------------------------------------------|
| Tabla  | overtime_id     | text                     |             100 |     1414 | Valores múltiples (+1,414) | Ej: OT-3337-805, OT-6492-932, OT-6311-252... |
| Tabla  | employee_id     | text                     |             100 |     1414 | Valores múltiples (+1,414) | Ej: 1337, 4946, 4924...                      |
| Tabla  | date_from       | text                     |             100 |        1 | 2024-02-01                                                                |
| Tabla  | date_to         | text                     |             100 |        1 | 2024-02-07                                                                |
| Tabla  | hours_overtime  | text                     |             100 |        8 | 2, 3, 4, 5, 6, 7, 8, 9                                                    |
| Tabla  | overtime_type   | text                     |             100 |        1 | Weekend                                                                   |
| Tabla  | approval_status | text                     |             100 |        1 | Approved                                                                  |
| Tabla  | cost_usd        | text                     |             100 |      150 | Valores múltiples (+150) | Ej: 198, 71, 118...                            |
| Tabla  | created_at      | timestamp with time zone |             100 |        1 | 2026-05-03 16:50:37.75247+00                                              |

### 📊 performance_reviews_byNapo

| Tipo   | Columna           | Dato                     |   Completitud % |   Unicos | Muestra                                                                                                                          |
|:-------|:------------------|:-------------------------|----------------:|---------:|:---------------------------------------------------------------------------------------------------------------------------------|
| Tabla  | review_id         | text                     |             100 |     7000 | Valores múltiples (+7,000) | Ej: REV-6999-2024, REV-1781-2024, REV-4734-2024...                                                  |
| Tabla  | employee_id       | text                     |             100 |     7000 | Valores múltiples (+7,000) | Ej: 2571, 3542, 3226...                                                                             |
| Tabla  | review_period     | text                     |             100 |        1 | 2024-Q1                                                                                                                          |
| Tabla  | reviewer_id       | text                     |             100 |      605 | Valores múltiples (+605) | Ej: 2532.0, 2099.0, 2254.0...                                                                         |
| Tabla  | overall_score     | text                     |             100 |       26 | 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0 |
| Tabla  | potential_score   | text                     |             100 |        3 | 1, 2, 3                                                                                                                          |
| Tabla  | performance_score | text                     |             100 |        3 | 1, 2, 3                                                                                                                          |
| Tabla  | status            | text                     |             100 |        1 | Completed                                                                                                                        |
| Tabla  | created_at        | timestamp with time zone |             100 |        1 | 2026-05-03 16:50:40.345934+00                                                                                                    |

### 📊 productivity_milestones_byNapo

| Tipo   | Columna            | Dato                     |   Completitud % |   Unicos | Muestra                                                                    |
|:-------|:-------------------|:-------------------------|----------------:|---------:|:---------------------------------------------------------------------------|
| Tabla  | milestone_id       | text                     |             100 |    21000 | Valores múltiples (+21,000) | Ej: MIL-1769-30, MIL-1002-30, MIL-4831-30... |
| Tabla  | employee_id        | text                     |             100 |     7000 | Valores múltiples (+7,000) | Ej: 2571, 3542, 3226...                       |
| Tabla  | milestone_name     | text                     |             100 |        3 | First Project, Full Productivity, Independent Work                         |
| Tabla  | expected_days      | text                     |             100 |        3 | 30, 60, 90                                                                 |
| Tabla  | actual_days        | text                     |             100 |       90 | Valores múltiples (+90) | Ej: 50, 89, 90...                                |
| Tabla  | achievement_date   | text                     |             100 |     4243 | Valores múltiples (+4,243) | Ej: 2019-01-22, 2022-08-18, 2017-05-09...     |
| Tabla  | performance_rating | text                     |             100 |        3 | 3, 4, 5                                                                    |
| Tabla  | manager_id         | text                     |             100 |      605 | Valores múltiples (+605) | Ej: 2532.0, 2099.0, 2254.0...                   |
| Tabla  | created_at         | timestamp with time zone |             100 |        1 | 2026-05-03 16:49:45.760005+00                                              |

### 📊 recruitment_pipeline_byNapo

| Tipo   | Columna           | Dato                     |   Completitud % |   Unicos | Muestra                                                                                                        |
|:-------|:------------------|:-------------------------|----------------:|---------:|:---------------------------------------------------------------------------------------------------------------|
| Tabla  | candidate_id      | text                     |           100   |    20848 | Valores múltiples (+20,848) | Ej: CAND-3611B8, CAND-4CF0EB, CAND-364794...                                     |
| Tabla  | posting_id        | text                     |           100   |      690 | Valores múltiples (+690) | Ej: POST-2024-12-FIN-4828, POST-2016-10-IT-4181, POST-2025-02-SAL-4950...           |
| Tabla  | full_name         | text                     |           100   |     7137 | Valores múltiples (+7,137) | Ej: Cand 9595, Cand 2381, Cand 4033...                                            |
| Tabla  | gender            | text                     |           100   |        2 | Female, Male                                                                                                   |
| Tabla  | age               | text                     |           100   |       28 | 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49 |
| Tabla  | education_level   | text                     |           100   |        4 | Bachelor, Master, PhD, Technical                                                                               |
| Tabla  | years_experience  | text                     |           100   |       10 | 0, 1, 2, 3, 4, 5, 6, 7, 8, 9                                                                                   |
| Tabla  | application_date  | text                     |           100   |      648 | Valores múltiples (+648) | Ej: 2022-11-17, 2017-11-14, 2021-08-17...                                           |
| Tabla  | stage             | text                     |           100   |        5 | Applied, Hired, Interview, Offer, Screening                                                                    |
| Tabla  | stage_change_date | text                     |           100   |     2095 | Valores múltiples (+2,095) | Ej: 2019-06-26, 2017-08-10, 2016-01-05...                                         |
| Tabla  | interview_score   | text                     |            53.8 |       60 | Valores múltiples (+60) | Ej: 61.0, 97.0, 53.0...                                                              |
| Tabla  | rejection_reason  | text                     |            66.4 |        2 | Not a fit, Offer Rejected                                                                                      |
| Tabla  | hired_employee_id | text                     |            33.6 |     7000 | Valores múltiples (+7,000) | Ej: 4584.0, 6016.0, 2099.0...                                                     |
| Tabla  | nps_score         | text                     |           100   |        8 | 10, 3, 4, 5, 6, 7, 8, 9                                                                                        |
| Tabla  | created_at        | timestamp with time zone |           100   |        1 | 2026-05-03 16:49:36.795217+00                                                                                  |

### 📊 succession_plans_byNapo

| Tipo   | Columna     | Dato                     |   Completitud % |   Unicos | Muestra         |
|:-------|:------------|:-------------------------|----------------:|---------:|:----------------|
| Tabla  | plan_id     | text                     |               0 |        0 | [Columna Vacía] |
| Tabla  | employee_id | text                     |               0 |        0 | [Columna Vacía] |
| Tabla  | created_at  | timestamp with time zone |               0 |        0 | [Columna Vacía] |

### 📊 survey_responses_byNapo

| Tipo   | Columna          | Dato                     |   Completitud % |   Unicos | Muestra                                                                        |
|:-------|:-----------------|:-------------------------|----------------:|---------:|:-------------------------------------------------------------------------------|
| Tabla  | response_id      | text                     |             100 |     5617 | Valores múltiples (+5,617) | Ej: SUR-3621-2024, SUR-2833-2024, SUR-130-2024... |
| Tabla  | employee_id      | text                     |             100 |     5617 | Valores múltiples (+5,617) | Ej: 2571, 3542, 247...                            |
| Tabla  | survey_id        | text                     |             100 |        1 | ENPS-2024                                                                      |
| Tabla  | survey_type      | text                     |             100 |        1 | eNPS                                                                           |
| Tabla  | survey_date      | text                     |             100 |        1 | 2024-03-01                                                                     |
| Tabla  | score_normalized | text                     |             100 |       10 | 1, 10, 2, 3, 4, 5, 6, 7, 8, 9                                                  |
| Tabla  | comments         | text                     |             100 |        2 | Could be better, Great place to work                                           |
| Tabla  | created_at       | timestamp with time zone |             100 |        1 | 2026-05-03 16:50:46.178371+00                                                  |

### 📊 training_courses_byNapo

| Tipo   | Columna        | Dato                     |   Completitud % |   Unicos | Muestra                       |
|:-------|:---------------|:-------------------------|----------------:|---------:|:------------------------------|
| Tabla  | course_id      | text                     |             100 |        1 | CRS-101                       |
| Tabla  | course_name    | text                     |             100 |        1 | Leadership 101                |
| Tabla  | category       | text                     |             100 |        1 | Soft Skills                   |
| Tabla  | duration_hours | text                     |             100 |        1 | 10                            |
| Tabla  | provider       | text                     |             100 |        1 | Internal                      |
| Tabla  | cost_usd       | text                     |             100 |        1 | 0                             |
| Tabla  | created_at     | timestamp with time zone |             100 |        1 | 2026-05-03 16:50:42.586876+00 |

### 📊 training_enrollments_byNapo

| Tipo   | Columna         | Dato                     |   Completitud % |   Unicos | Muestra                                                                                                                |
|:-------|:----------------|:-------------------------|----------------:|---------:|:-----------------------------------------------------------------------------------------------------------------------|
| Tabla  | enrollment_id   | text                     |             100 |     7000 | Valores múltiples (+7,000) | Ej: ENR-1827, ENR-3668, ENR-2343...                                                       |
| Tabla  | employee_id     | text                     |             100 |     7000 | Valores múltiples (+7,000) | Ej: 2571, 3542, 3226...                                                                   |
| Tabla  | course_id       | text                     |             100 |        1 | CRS-101                                                                                                                |
| Tabla  | enrollment_date | text                     |             100 |        1 | 2024-02-01                                                                                                             |
| Tabla  | completion_date | text                     |             100 |        1 | 2024-02-15                                                                                                             |
| Tabla  | status          | text                     |             100 |        1 | Completed                                                                                                              |
| Tabla  | score           | text                     |             100 |       30 | 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99 |
| Tabla  | feedback_rating | text                     |             100 |        1 | 4                                                                                                                      |
| Tabla  | created_at      | timestamp with time zone |             100 |        1 | 2026-05-03 16:50:43.102908+00                                                                                          |

### 📊 union_agreements_byNapo

| Tipo   | Columna            | Dato                     |   Completitud % |   Unicos | Muestra                                                                        |
|:-------|:-------------------|:-------------------------|----------------:|---------:|:-------------------------------------------------------------------------------|
| Tabla  | agreement_id       | text                     |             100 |        4 | UAG-CHL, UAG-ESP, UAG-MEX, UAG-PER                                             |
| Tabla  | union_name         | text                     |             100 |        4 | National Union CHL, National Union ESP, National Union MEX, National Union PER |
| Tabla  | country_iso3       | text                     |             100 |        4 | CHL, ESP, MEX, PER                                                             |
| Tabla  | effective_date     | text                     |             100 |        1 | 2023-01-01                                                                     |
| Tabla  | expiry_date        | text                     |             100 |        1 | 2025-12-31                                                                     |
| Tabla  | coverage_employees | text                     |             100 |        4 | 233, 270, 353, 431                                                             |
| Tabla  | negotiation_status | text                     |             100 |        1 | Active                                                                         |
| Tabla  | created_at         | timestamp with time zone |             100 |        1 | 2026-05-03 16:50:48.834343+00                                                  |

