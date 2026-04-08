# 🧠 Catálogo Global de Datos - HR Analytics

# 📂 Esquema: `business`

### 📊 ibm_hr

| Tipo   | Columna           | Dato    |   Completitud % |   Unicos | Muestra de Datos                                                                                                                                          |
|:-------|:------------------|:--------|----------------:|---------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------|
| Vista  | id                | integer |             100 |     1470 | Valores múltiples (+1,470) | Ej: 1318, 1562, 551...                                                                                                       |
| Vista  | age               | integer |             100 |       43 | Valores múltiples (+43) | Ej: 54, 47, 28...                                                                                                               |
| Vista  | department        | text    |             100 |        3 | Human Resources, Research & Development, Sales                                                                                                            |
| Vista  | jobrole           | text    |             100 |        9 | Healthcare Representative, Human Resources, Laboratory Technician, Manager, Manufacturing Director, Research Director, Research Scientist, Sales Execu... |
| Vista  | attrition         | text    |             100 |        2 | No, Yes                                                                                                                                                   |
| Vista  | gender            | text    |             100 |        2 | Female, Male                                                                                                                                              |
| Vista  | dailyrate         | integer |             100 |      886 | Valores múltiples (+886) | Ej: 461, 711, 791...                                                                                                           |
| Vista  | monthlyincome     | integer |             100 |     1349 | Valores múltiples (+1,349) | Ej: 2571, 10048, 2585...                                                                                                     |
| Vista  | totalworkingyears | integer |             100 |       40 | Valores múltiples (+40) | Ej: 8, 12, 10...                                                                                                                |
| Vista  | yearsatcompany    | integer |             100 |       37 | Valores múltiples (+37) | Ej: 8, 12, 10...                                                                                                                |
| Vista  | distancefromhome  | integer |             100 |       29 | 1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 2, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 3, 4, 5, 6, 7, 8, 9                                                 |

### 📊 mv_monthly_kpis_bynapo

| Tipo   | Columna              | Dato    |   Completitud % |   Unicos | Muestra de Datos                                                    |
|:-------|:---------------------|:--------|----------------:|---------:|:--------------------------------------------------------------------|
| M-View | snapshot_date        | date    |             100 |       75 | Valores múltiples (+75) | Ej: 2020-12-31, 2023-04-30, 2025-04-30... |
| M-View | country_iso3         | text    |             100 |        6 | CHL, COL, ESP, MEX, PER, USA                                        |
| M-View | headcount_active     | bigint  |             100 |      273 | Valores múltiples (+273) | Ej: 1026, 862, 1046...                   |
| M-View | headcount_terminated | bigint  |             100 |      330 | Valores múltiples (+330) | Ej: 123, 537, 75...                      |
| M-View | avg_salary_usd       | numeric |             100 |      446 | Valores múltiples (+446) | Ej: 798.63, 797.67, 734.18...            |
| M-View | avg_tenure           | numeric |             100 |      201 | Valores múltiples (+201) | Ej: 51.1, 45.5, 55.2...                  |

### 📊 mv_ui_global_filters

| Tipo   | Columna        | Dato   |   Completitud % |   Unicos | Muestra de Datos      |
|:-------|:---------------|:-------|----------------:|---------:|:----------------------|
| M-View | filter_options | json   |             100 |        1 | [Estructura Compleja] |

### 📊 v_employee_full_bynapo

| Tipo   | Columna               | Dato                     |   Completitud % |   Unicos | Muestra de Datos                                                                                                                                          |
|:-------|:----------------------|:-------------------------|----------------:|---------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------|
| Vista  | snapshot_date         | date                     |           100   |       75 | Valores múltiples (+75) | Ej: 2020-01-31, 2020-02-29, 2020-03-31...                                                                                       |
| Vista  | employee_id           | integer                  |           100   |    10000 | Valores múltiples (+10,000) | Ej: 1, 10, 100...                                                                                                           |
| Vista  | employee_code         | text                     |           100   |    10000 | Valores múltiples (+10,000) | Ej: EMP-00001, EMP-00002, EMP-00003...                                                                                      |
| Vista  | full_name             | text                     |           100   |       56 | Valores múltiples (+56) | Ej: Ana Gomez, Ana Lopez, Ana Martinez...                                                                                       |
| Vista  | gender                | text                     |           100   |        2 | Female, Male                                                                                                                                              |
| Vista  | country_iso3          | text                     |           100   |        6 | CHL, COL, ESP, MEX, PER, USA                                                                                                                              |
| Vista  | department_name       | text                     |           100   |        5 | Finance, HR, IT, Operations, Sales                                                                                                                        |
| Vista  | job_role              | text                     |           100   |       16 | Account Manager, Accountant, CFO, CTO, Data Analyst, DevOps, Financial Analyst, HR Manager, HR Specialist, Logistics Coord, Operator, Ops Director, Re... |
| Vista  | job_level_1           | text                     |           100   |        2 | Individual Contributor, Management                                                                                                                        |
| Vista  | job_level_2           | text                     |           100   |        3 | Junior, Lead, Senior                                                                                                                                      |
| Vista  | employment_status     | text                     |           100   |        2 | Active, Terminated                                                                                                                                        |
| Vista  | hire_date             | date                     |           100   |     1713 | Valores múltiples (+1,713) | Ej: 2014-07-12, 2014-07-13, 2014-07-14...                                                                                    |
| Vista  | termination_date      | date                     |            25.9 |       75 | Valores múltiples (+75) | Ej: 2020-01-31, 2020-02-29, 2020-03-31...                                                                                       |
| Vista  | monthly_salary_local  | numeric(12,2)            |           100   |    25267 | Valores múltiples (+25,267) | Ej: 1000.50, 1000.52, 1000.83...                                                                                            |
| Vista  | currency_iso3         | text                     |           100   |        6 | CLP, COP, EUR, MXN, PEN, USD                                                                                                                              |
| Vista  | fx_rate_to_usd        | numeric(10,4)            |           100   |        1 | 3.5000                                                                                                                                                    |
| Vista  | monthly_salary_usd    | numeric(12,2)            |           100   |    23196 | Valores múltiples (+23,196) | Ej: 1000.03, 1000.06, 1000.23...                                                                                            |
| Vista  | manager_employee_id   | integer                  |            99.7 |     2007 | Valores múltiples (+2,007) | Ej: 1, 10, 100...                                                                                                            |
| Vista  | tenure_months         | numeric                  |           100   |      141 | Valores múltiples (+141) | Ej: 0, 1, 10...                                                                                                                |
| Vista  | is_active_at_snapshot | boolean                  |           100   |        2 | false, true                                                                                                                                               |
| Vista  | processed_at          | timestamp with time zone |           100   |        1 | 2026-04-08 20:46:50.08367+00                                                                                                                              |

### 📊 v_org_tree_bynapo

| Tipo   | Columna      | Dato    |   Completitud % |   Unicos | Muestra de Datos                                                                                                                                          |
|:-------|:-------------|:--------|----------------:|---------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------|
| Vista  | employee_id  | integer |             100 |      415 | Valores múltiples (+415) | Ej: 9183, 9818, 8954...                                                                                                        |
| Vista  | full_name    | text    |             100 |       56 | Valores múltiples (+56) | Ej: Juan Martinez, Ana Gomez, Luis Torres...                                                                                    |
| Vista  | job_role     | text    |             100 |       16 | Account Manager, Accountant, CFO, CTO, Data Analyst, DevOps, Financial Analyst, HR Manager, HR Specialist, Logistics Coord, Operator, Ops Director, Re... |
| Vista  | job_level_1  | text    |             100 |        2 | Individual Contributor, Management                                                                                                                        |
| Vista  | depth        | integer |             100 |       10 | 0, 1, 2, 3, 4, 5, 6, 7, 8, 9                                                                                                                              |
| Vista  | echarts_node | json    |             100 |      415 | [Estructura Compleja]                                                                                                                                     |

# 📂 Esquema: `raw`

### 📊 ibm_hr_change_reasons_byNapo

| Tipo   | Columna        | Dato                     |   Completitud % |   Unicos | Muestra de Datos   |
|:-------|:---------------|:-------------------------|----------------:|---------:|:-------------------|
| Tabla  | reason_code    | text                     |               0 |        0 | [Columna Vacía]    |
| Tabla  | reason_name_es | text                     |               0 |        0 | [Columna Vacía]    |
| Tabla  | reason_name_en | text                     |               0 |        0 | [Columna Vacía]    |
| Tabla  | affects_salary | text                     |               0 |        0 | [Columna Vacía]    |
| Tabla  | affects_job    | text                     |               0 |        0 | [Columna Vacía]    |
| Tabla  | active_flag    | text                     |               0 |        0 | [Columna Vacía]    |
| Tabla  | created_at     | timestamp with time zone |               0 |        0 | [Columna Vacía]    |

### 📊 ibm_hr_landing

| Tipo   | Columna                  | Dato                     |   Completitud % |   Unicos | Muestra de Datos                                                                                                                                          |
|:-------|:-------------------------|:-------------------------|----------------:|---------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------|
| Tabla  | age                      | text                     |             100 |       43 | Valores múltiples (+43) | Ej: 54, 47, 28...                                                                                                               |
| Tabla  | attrition                | text                     |             100 |        2 | No, Yes                                                                                                                                                   |
| Tabla  | businesstravel           | text                     |             100 |        3 | Non-Travel, Travel_Frequently, Travel_Rarely                                                                                                              |
| Tabla  | dailyrate                | text                     |             100 |      886 | Valores múltiples (+886) | Ej: 461, 711, 791...                                                                                                           |
| Tabla  | department               | text                     |             100 |        3 | Human Resources, Research & Development, Sales                                                                                                            |
| Tabla  | distancefromhome         | text                     |             100 |       29 | 1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 2, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 3, 4, 5, 6, 7, 8, 9                                                 |
| Tabla  | education                | text                     |             100 |        5 | 1, 2, 3, 4, 5                                                                                                                                             |
| Tabla  | educationfield           | text                     |             100 |        6 | Human Resources, Life Sciences, Marketing, Medical, Other, Technical Degree                                                                               |
| Tabla  | employeecount            | text                     |             100 |        1 | 1                                                                                                                                                         |
| Tabla  | employeenumber           | text                     |             100 |     1470 | Valores múltiples (+1,470) | Ej: 1318, 1562, 551...                                                                                                       |
| Tabla  | environmentsatisfaction  | text                     |             100 |        4 | 1, 2, 3, 4                                                                                                                                                |
| Tabla  | gender                   | text                     |             100 |        2 | Female, Male                                                                                                                                              |
| Tabla  | hourlyrate               | text                     |             100 |       71 | Valores múltiples (+71) | Ej: 75, 96, 39...                                                                                                               |
| Tabla  | jobinvolvement           | text                     |             100 |        4 | 1, 2, 3, 4                                                                                                                                                |
| Tabla  | joblevel                 | text                     |             100 |        5 | 1, 2, 3, 4, 5                                                                                                                                             |
| Tabla  | jobrole                  | text                     |             100 |        9 | Healthcare Representative, Human Resources, Laboratory Technician, Manager, Manufacturing Director, Research Director, Research Scientist, Sales Execu... |
| Tabla  | jobsatisfaction          | text                     |             100 |        4 | 1, 2, 3, 4                                                                                                                                                |
| Tabla  | maritalstatus            | text                     |             100 |        3 | Divorced, Married, Single                                                                                                                                 |
| Tabla  | monthlyincome            | text                     |             100 |     1349 | Valores múltiples (+1,349) | Ej: 2571, 10048, 2585...                                                                                                     |
| Tabla  | monthlyrate              | text                     |             100 |     1427 | Valores múltiples (+1,427) | Ej: 7172, 4905, 20165...                                                                                                     |
| Tabla  | numcompaniesworked       | text                     |             100 |       10 | 0, 1, 2, 3, 4, 5, 6, 7, 8, 9                                                                                                                              |
| Tabla  | over18                   | text                     |             100 |        1 | Y                                                                                                                                                         |
| Tabla  | overtime                 | text                     |             100 |        2 | No, Yes                                                                                                                                                   |
| Tabla  | percentsalaryhike        | text                     |             100 |       15 | 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25                                                                                                |
| Tabla  | performancerating        | text                     |             100 |        2 | 3, 4                                                                                                                                                      |
| Tabla  | relationshipsatisfaction | text                     |             100 |        4 | 1, 2, 3, 4                                                                                                                                                |
| Tabla  | standardhours            | text                     |             100 |        1 | 80                                                                                                                                                        |
| Tabla  | stockoptionlevel         | text                     |             100 |        4 | 0, 1, 2, 3                                                                                                                                                |
| Tabla  | totalworkingyears        | text                     |             100 |       40 | Valores múltiples (+40) | Ej: 8, 12, 10...                                                                                                                |
| Tabla  | trainingtimeslastyear    | text                     |             100 |        7 | 0, 1, 2, 3, 4, 5, 6                                                                                                                                       |
| Tabla  | worklifebalance          | text                     |             100 |        4 | 1, 2, 3, 4                                                                                                                                                |
| Tabla  | yearsatcompany           | text                     |             100 |       37 | Valores múltiples (+37) | Ej: 8, 12, 10...                                                                                                                |
| Tabla  | yearsincurrentrole       | text                     |             100 |       19 | 0, 1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 2, 3, 4, 5, 6, 7, 8, 9                                                                                          |
| Tabla  | yearssincelastpromotion  | text                     |             100 |       16 | 0, 1, 10, 11, 12, 13, 14, 15, 2, 3, 4, 5, 6, 7, 8, 9                                                                                                      |
| Tabla  | yearswithcurrmanager     | text                     |             100 |       18 | 0, 1, 10, 11, 12, 13, 14, 15, 16, 17, 2, 3, 4, 5, 6, 7, 8, 9                                                                                              |
| Tabla  | created_at               | timestamp with time zone |             100 |        1 | 2026-04-08 19:46:19.610529+00                                                                                                                             |

### 📊 ibm_hr_monthly_snapshot_byNapo

| Tipo   | Columna                         | Dato                     |   Completitud % |   Unicos | Muestra de Datos                                                                                                                                          |
|:-------|:--------------------------------|:-------------------------|----------------:|---------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------|
| Tabla  | snapshot_date                   | text                     |           100   |       75 | Valores múltiples (+75) | Ej: 2020-01-31, 2020-02-29, 2020-03-31...                                                                                       |
| Tabla  | employee_id                     | text                     |           100   |    10000 | Valores múltiples (+10,000) | Ej: 1, 10, 100...                                                                                                           |
| Tabla  | employee_code                   | text                     |           100   |    10000 | Valores múltiples (+10,000) | Ej: EMP-00001, EMP-00002, EMP-00003...                                                                                      |
| Tabla  | full_name                       | text                     |           100   |       56 | Valores múltiples (+56) | Ej: Ana Gomez, Ana Lopez, Ana Martinez...                                                                                       |
| Tabla  | gender                          | text                     |           100   |        2 | Female, Male                                                                                                                                              |
| Tabla  | nationality_iso3                | text                     |             0   |        0 | [Columna Vacía]                                                                                                                                           |
| Tabla  | country_iso3                    | text                     |           100   |        6 | CHL, COL, ESP, MEX, PER, USA                                                                                                                              |
| Tabla  | department_name                 | text                     |           100   |        5 | Finance, HR, IT, Operations, Sales                                                                                                                        |
| Tabla  | job_role                        | text                     |           100   |       16 | Account Manager, Accountant, CFO, CTO, Data Analyst, DevOps, Financial Analyst, HR Manager, HR Specialist, Logistics Coord, Operator, Ops Director, Re... |
| Tabla  | job_level_1                     | text                     |           100   |        2 | Individual Contributor, Management                                                                                                                        |
| Tabla  | job_level_2                     | text                     |           100   |        3 | Junior, Lead, Senior                                                                                                                                      |
| Tabla  | employment_status               | text                     |           100   |        2 | Active, Terminated                                                                                                                                        |
| Tabla  | hire_date                       | text                     |           100   |     1713 | Valores múltiples (+1,713) | Ej: 2014-07-12, 2014-07-13, 2014-07-14...                                                                                    |
| Tabla  | termination_date                | text                     |            25.9 |       75 | Valores múltiples (+75) | Ej: 2020-01-31, 2020-02-29, 2020-03-31...                                                                                       |
| Tabla  | termination_reason_legal        | text                     |             0   |        0 | [Columna Vacía]                                                                                                                                           |
| Tabla  | turnover_classification_company | text                     |             0   |        0 | [Columna Vacía]                                                                                                                                           |
| Tabla  | monthly_salary_local            | text                     |           100   |    26074 | Valores múltiples (+26,074) | Ej: 1000.4995947041089, 1000.5220664215142, 1000.8267149983348...                                                           |
| Tabla  | currency_iso3                   | text                     |           100   |        6 | CLP, COP, EUR, MXN, PEN, USD                                                                                                                              |
| Tabla  | fx_rate_to_usd                  | text                     |           100   |        1 | 3.5                                                                                                                                                       |
| Tabla  | monthly_salary_usd              | text                     |           100   |    23196 | Valores múltiples (+23,196) | Ej: 1000.03, 1000.06, 1000.23...                                                                                            |
| Tabla  | manager_employee_id             | text                     |            99.7 |     2007 | Valores múltiples (+2,007) | Ej: 1.0, 10.0, 100.0...                                                                                                      |
| Tabla  | dotted_line_manager_id          | text                     |             0   |        0 | [Columna Vacía]                                                                                                                                           |
| Tabla  | work_center_id                  | text                     |             0   |        0 | [Columna Vacía]                                                                                                                                           |
| Tabla  | home_lat                        | text                     |             0   |        0 | [Columna Vacía]                                                                                                                                           |
| Tabla  | home_lon                        | text                     |             0   |        0 | [Columna Vacía]                                                                                                                                           |
| Tabla  | work_modality                   | text                     |             0   |        0 | [Columna Vacía]                                                                                                                                           |
| Tabla  | education_level                 | text                     |             0   |        0 | [Columna Vacía]                                                                                                                                           |
| Tabla  | education_status                | text                     |             0   |        0 | [Columna Vacía]                                                                                                                                           |
| Tabla  | marital_status                  | text                     |             0   |        0 | [Columna Vacía]                                                                                                                                           |
| Tabla  | dependents_count                | text                     |             0   |        0 | [Columna Vacía]                                                                                                                                           |
| Tabla  | salary_change_flag              | text                     |           100   |        1 | 0                                                                                                                                                         |
| Tabla  | salary_change_reason_code       | text                     |             0   |        0 | [Columna Vacía]                                                                                                                                           |
| Tabla  | job_change_flag                 | text                     |           100   |        1 | 0                                                                                                                                                         |
| Tabla  | exit_interview_completed        | text                     |             0   |        0 | [Columna Vacía]                                                                                                                                           |
| Tabla  | regrettable_loss_flag           | text                     |             0   |        0 | [Columna Vacía]                                                                                                                                           |
| Tabla  | created_at                      | timestamp with time zone |           100   |        1 | 2026-04-08 19:46:55.130418+00                                                                                                                             |

