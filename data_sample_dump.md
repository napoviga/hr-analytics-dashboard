# 📊 Data Sample — `business.v_employee_full_byNapo`

> **Generado:** 2026-04-07 17:28  
> **Registros:** 50 (muestra aleatoria)  
> **Columnas:** 21

## Columnas y tipos detectados

| Columna | Tipo (PostgreSQL → Pandas) |
|---------|---------------------------|
| `snapshot_date` | `object` |
| `employee_id` | `int64` |
| `employee_code` | `str` |
| `full_name` | `str` |
| `gender` | `str` |
| `country_iso3` | `str` |
| `department_name` | `str` |
| `job_role` | `str` |
| `job_level_1` | `str` |
| `job_level_2` | `str` |
| `employment_status` | `str` |
| `hire_date` | `object` |
| `termination_date` | `object` |
| `monthly_salary_local` | `float64` |
| `currency_iso3` | `str` |
| `fx_rate_to_usd` | `float64` |
| `monthly_salary_usd` | `float64` |
| `manager_employee_id` | `int64` |
| `tenure_months` | `float64` |
| `is_active_at_snapshot` | `bool` |
| `processed_at` | `datetime64[us, UTC]` |

## Muestra de datos (50 registros)

| snapshot_date | employee_id | employee_code | full_name | gender | country_iso3 | department_name | job_role | job_level_1 | job_level_2 | employment_status | hire_date | termination_date | monthly_salary_local | currency_iso3 | fx_rate_to_usd | monthly_salary_usd | manager_employee_id | tenure_months | is_active_at_snapshot | processed_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024-08-31 | 747 | EMP-00747 | Ana Torres | Female | CHL | Operations | Ops Director | Individual Contributor | Junior | Terminated | 2016-12-21 | 2022-04-30 | 4559.55 | CLP | 3.5 | 1302.73 | 3860 | 64.0 | False | 2026-04-07 22:28:03.410288+00:00 |
| 2024-05-31 | 8021 | EMP-08021 | Maria Torres | Female | ESP | Finance | Software Engineer | Individual Contributor | Junior | Active | 2024-03-31 | None | 2139.24 | EUR | 3.5 | 611.21 | 2514 | 2.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2024-01-31 | 2246 | EMP-02246 | Sofia Lopez | Female | USA | Sales | Sales Rep | Individual Contributor | Junior | Terminated | 2016-02-26 | 2021-08-31 | 1603.2 | USD | 3.5 | 458.06 | 2323 | 66.0 | False | 2026-04-07 22:28:03.410288+00:00 |
| 2020-10-31 | 2905 | EMP-02905 | Ana Martinez | Male | MEX | Operations | Ops Director | Management | Junior | Active | 2019-04-25 | None | 3578.99 | MXN | 3.5 | 1022.57 | 290 | 18.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2023-09-30 | 3929 | EMP-03929 | Ana Rodriguez | Female | USA | Operations | Ops Director | Management | Lead | Terminated | 2015-12-20 | 2023-06-30 | 4420.22 | USD | 3.5 | 1262.92 | 2740 | 90.0 | False | 2026-04-07 22:28:03.410288+00:00 |
| 2025-11-30 | 7647 | EMP-07647 | Carlos Martinez | Female | CHL | Operations | CTO | Individual Contributor | Junior | Active | 2023-10-31 | None | 1678.35 | CLP | 3.5 | 479.53 | 828 | 24.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2025-01-31 | 8192 | EMP-08192 | Pedro Torres | Female | CHL | IT | CTO | Individual Contributor | Junior | Active | 2024-05-31 | None | 2028.64 | CLP | 3.5 | 579.61 | 142 | 8.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2023-04-30 | 3434 | EMP-03434 | Sofia Lopez | Male | MEX | Sales | Sales Director | Management | Junior | Terminated | 2016-04-28 | 2020-07-31 | 2230.03 | MXN | 3.5 | 637.15 | 2547 | 51.0 | False | 2026-04-07 22:28:03.410288+00:00 |
| 2020-03-31 | 351 | EMP-00351 | Maria Gomez | Female | USA | Finance | Financial Analyst | Individual Contributor | Lead | Active | 2016-03-02 | None | 4644.77 | USD | 3.5 | 1327.08 | 1055 | 48.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2026-03-31 | 7394 | EMP-07394 | Juan Rodriguez | Male | COL | Finance | Data Analyst | Individual Contributor | Junior | Active | 2023-07-31 | None | 1668.13 | COP | 3.5 | 476.61 | 2785 | 32.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2020-12-31 | 1459 | EMP-01459 | Carlos Gomez | Male | MEX | IT | Data Analyst | Individual Contributor | Senior | Terminated | 2018-01-19 | 2020-05-31 | 3872.21 | MXN | 3.5 | 1106.35 | 26 | 28.0 | False | 2026-04-07 22:28:03.410288+00:00 |
| 2025-03-31 | 8856 | EMP-08856 | Ana Perez | Female | ESP | Sales | Data Analyst | Individual Contributor | Junior | Active | 2025-01-31 | None | 1639.27 | EUR | 3.5 | 468.36 | 3018 | 2.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2024-06-30 | 6210 | EMP-06210 | Carlos Lopez | Female | CHL | Operations | Software Engineer | Individual Contributor | Junior | Active | 2022-04-30 | None | 1690.71 | CLP | 3.5 | 483.06 | 2408 | 26.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2020-07-31 | 3789 | EMP-03789 | Pedro Silva | Male | MEX | Operations | Logistics Coord | Management | Junior | Active | 2018-11-23 | None | 3206.42 | MXN | 3.5 | 916.12 | 3584 | 20.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2023-07-31 | 3604 | EMP-03604 | Pedro Martinez | Female | MEX | Sales | Account Manager | Individual Contributor | Junior | Terminated | 2018-12-27 | 2023-03-31 | 3887.83 | MXN | 3.5 | 1110.81 | 1267 | 51.0 | False | 2026-04-07 22:28:03.410288+00:00 |
| 2024-05-31 | 4450 | EMP-04450 | Pedro Silva | Male | USA | HR | Software Engineer | Individual Contributor | Junior | Active | 2020-06-30 | None | 2704.57 | USD | 3.5 | 772.73 | 3295 | 47.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2021-10-31 | 4570 | EMP-04570 | Sofia Torres | Female | PER | Finance | Software Engineer | Individual Contributor | Junior | Active | 2020-08-31 | None | 1725.93 | PEN | 3.5 | 493.12 | 1323 | 14.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2021-06-30 | 1298 | EMP-01298 | Luis Torres | Male | MEX | Sales | Account Manager | Individual Contributor | Junior | Active | 2017-12-17 | None | 2825.81 | MXN | 3.5 | 807.37 | 1270 | 42.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2023-04-30 | 2428 | EMP-02428 | Ana Lopez | Female | COL | Finance | Financial Analyst | Management | Lead | Active | 2019-06-19 | None | 3371.26 | COP | 3.5 | 963.22 | 2843 | 46.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2025-12-31 | 3848 | EMP-03848 | Luis Lopez | Female | PER | Finance | Accountant | Management | Lead | Active | 2017-10-01 | None | 2582.12 | PEN | 3.5 | 737.75 | 2529 | 98.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2024-01-31 | 3445 | EMP-03445 | Lucia Silva | Female | CHL | HR | HR Manager | Management | Junior | Terminated | 2015-10-14 | 2020-02-29 | 1730.78 | CLP | 3.5 | 494.51 | 3473 | 52.0 | False | 2026-04-07 22:28:03.410288+00:00 |
| 2020-06-30 | 410 | EMP-00410 | Carlos Perez | Male | PER | HR | HR Specialist | Management | Lead | Active | 2017-07-01 | None | 4197.27 | PEN | 3.5 | 1199.22 | 532 | 35.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2021-04-30 | 359 | EMP-00359 | Juan Silva | Female | MEX | HR | HR Manager | Individual Contributor | Junior | Terminated | 2018-06-19 | 2021-03-31 | 2616.46 | MXN | 3.5 | 747.56 | 2242 | 33.0 | False | 2026-04-07 22:28:03.410288+00:00 |
| 2025-06-30 | 8996 | EMP-08996 | Juan Perez | Male | USA | HR | DevOps | Individual Contributor | Junior | Active | 2025-03-31 | None | 2736.05 | USD | 3.5 | 781.73 | 3704 | 2.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2025-01-31 | 5613 | EMP-05613 | Pedro Gomez | Female | USA | Sales | Software Engineer | Individual Contributor | Junior | Active | 2021-09-30 | None | 2907.92 | USD | 3.5 | 830.84 | 700 | 40.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2022-07-31 | 2147 | EMP-02147 | Ana Perez | Female | PER | Finance | Accountant | Individual Contributor | Junior | Active | 2016-07-26 | None | 2218.34 | PEN | 3.5 | 633.81 | 2236 | 72.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2026-01-31 | 7057 | EMP-07057 | Luis Martinez | Male | PER | IT | Software Engineer | Individual Contributor | Junior | Active | 2023-03-31 | None | 2248.77 | PEN | 3.5 | 642.5 | 869 | 34.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2023-11-30 | 1792 | EMP-01792 | Juan Perez | Male | PER | HR | HR Manager | Individual Contributor | Senior | Terminated | 2018-08-18 | 2021-11-30 | 5043.17 | PEN | 3.5 | 1440.9 | 2069 | 39.0 | False | 2026-04-07 22:28:03.410288+00:00 |
| 2021-12-31 | 5581 | EMP-05581 | Juan Perez | Female | USA | Sales | DevOps | Individual Contributor | Junior | Active | 2021-08-31 | None | 2275.7 | USD | 3.5 | 650.2 | 3911 | 4.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2025-10-31 | 9229 | EMP-09229 | Sofia Torres | Male | USA | IT | CTO | Individual Contributor | Junior | Active | 2025-06-30 | None | 2002.68 | USD | 3.5 | 572.19 | 2835 | 4.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2020-10-31 | 4148 | EMP-04148 | Juan Gomez | Male | CHL | Finance | Data Analyst | Individual Contributor | Junior | Active | 2020-02-29 | None | 1914.37 | CLP | 3.5 | 546.96 | 3304 | 8.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2022-11-30 | 6721 | EMP-06721 | Luis Torres | Female | COL | Sales | Data Analyst | Individual Contributor | Junior | Active | 2022-11-30 | None | 2205.59 | COP | 3.5 | 630.17 | 3705 | 0.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2020-03-31 | 2404 | EMP-02404 | Luis Gomez | Female | PER | Sales | Account Manager | Individual Contributor | Lead | Active | 2017-10-26 | None | 4306.33 | PEN | 3.5 | 1230.38 | 2323 | 29.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2024-11-30 | 1952 | EMP-01952 | Juan Lopez | Male | COL | Operations | Ops Director | Individual Contributor | Senior | Active | 2015-02-11 | None | 3113.29 | COP | 3.5 | 889.51 | 1171 | 117.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2025-10-31 | 9254 | EMP-09254 | Luis Silva | Male | PER | IT | CTO | Individual Contributor | Junior | Active | 2025-06-30 | None | 2106.05 | PEN | 3.5 | 601.73 | 104 | 4.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2024-11-30 | 7381 | EMP-07381 | Lucia Silva | Female | USA | Finance | DevOps | Individual Contributor | Junior | Active | 2023-07-31 | None | 2457.51 | USD | 3.5 | 702.15 | 1076 | 15.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2025-10-31 | 7768 | EMP-07768 | Sofia Rodriguez | Female | ESP | Operations | Software Engineer | Individual Contributor | Junior | Active | 2023-12-31 | None | 1573.3 | EUR | 3.5 | 449.52 | 2525 | 22.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2024-05-31 | 5861 | EMP-05861 | Sofia Torres | Male | USA | HR | Data Analyst | Individual Contributor | Junior | Active | 2021-12-31 | None | 2106.9 | USD | 3.5 | 601.97 | 3405 | 29.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2020-04-30 | 2410 | EMP-02410 | Sofia Torres | Male | COL | HR | Recruiter | Management | Junior | Active | 2018-03-22 | None | 3508.02 | COP | 3.5 | 1002.29 | 2905 | 25.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2024-09-30 | 529 | EMP-00529 | Lucia Silva | Female | CHL | HR | HR Manager | Individual Contributor | Junior | Active | 2016-08-19 | None | 2163.23 | CLP | 3.5 | 618.07 | 286 | 97.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2023-10-31 | 5171 | EMP-05171 | Carlos Martinez | Female | PER | Finance | Data Analyst | Individual Contributor | Junior | Active | 2021-03-31 | None | 3118.21 | PEN | 3.5 | 890.92 | 3289 | 31.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2023-08-31 | 1744 | EMP-01744 | Pedro Lopez | Male | ESP | Operations | Operator | Management | Lead | Terminated | 2015-05-08 | 2022-02-28 | 1648.93 | EUR | 3.5 | 471.12 | 784 | 81.0 | False | 2026-04-07 22:28:03.410288+00:00 |
| 2021-08-31 | 3205 | EMP-03205 | Maria Gomez | Male | COL | HR | HR Manager | Individual Contributor | Junior | Active | 2018-11-03 | None | 3069.43 | COP | 3.5 | 876.98 | 1091 | 33.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2024-04-30 | 7343 | EMP-07343 | Ana Gomez | Male | USA | IT | CTO | Individual Contributor | Junior | Active | 2023-06-30 | None | 1967.6 | USD | 3.5 | 562.17 | 384 | 10.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2022-03-31 | 2820 | EMP-02820 | Luis Gomez | Female | COL | Sales | Sales Rep | Management | Senior | Active | 2017-10-21 | None | 3295.45 | COP | 3.5 | 941.56 | 91 | 53.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2022-11-30 | 1647 | EMP-01647 | Carlos Torres | Female | CHL | HR | Recruiter | Management | Senior | Active | 2018-06-02 | None | 3675.37 | CLP | 3.5 | 1050.1 | 1984 | 53.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2024-02-29 | 7324 | EMP-07324 | Luis Lopez | Male | ESP | IT | Data Analyst | Individual Contributor | Junior | Active | 2023-06-30 | None | 2541.77 | EUR | 3.5 | 726.22 | 1926 | 7.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2021-12-31 | 675 | EMP-00675 | Maria Silva | Female | USA | Finance | Accountant | Individual Contributor | Lead | Terminated | 2014-12-25 | 2020-01-31 | 3619.13 | USD | 3.5 | 1034.04 | 3151 | 61.0 | False | 2026-04-07 22:28:03.410288+00:00 |
| 2020-06-30 | 1819 | EMP-01819 | Pedro Rodriguez | Male | ESP | Sales | Account Manager | Management | Senior | Active | 2019-02-18 | None | 4558.78 | EUR | 3.5 | 1302.51 | 3105 | 16.0 | True | 2026-04-07 22:28:03.410288+00:00 |
| 2025-11-30 | 3484 | EMP-03484 | Sofia Martinez | Male | CHL | Sales | Sales Director | Individual Contributor | Senior | Terminated | 2018-07-31 | 2023-02-28 | 2032.65 | CLP | 3.5 | 580.76 | 2020 | 54.0 | False | 2026-04-07 22:28:03.410288+00:00 |
