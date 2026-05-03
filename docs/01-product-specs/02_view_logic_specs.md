# GDH Analytics — Especificaciones de Interfaz y Descripciones

**01. VISIÓN EJECUTIVA**

- **Dashboard C-Level:** Panel de mando estratégico con KPIs de GDH en tiempo real. Monitorea métricas consolidadas permitiendo profundizar dinámicamente mediante dimensiones de segmentación. **[DESC]**
- **Alertas & Anomalías:** Motor predictivo de desviaciones estadísticas. Identifica quiebres en métricas clave a nivel individual o agrupado y sugiere acciones preventivas. **[PRED] [ML]**
- **Benchmarking de Mercado:** Comparativa de indicadores clave frente a estándares externos para asegurar competitividad y posicionamiento sectorial. **[DESC]**

**02. RECLUTAMIENTO & SELECCIÓN**

- **Eficiencia & Ciclos de Contratación:** Medición de flujo e inversión de tiempo por etapa y cobertura de vacantes. Identifica cuellos de botella mediante el análisis de la data histórica del proceso. **[DESC]**
- **Calidad de Contratación:** Evaluación de éxito a mediano y largo plazo (QoH), cruzando el desempeño con el perfil de ingreso individual o por cohortes de contratación. **[DESC] [PRED]**
- **Fit Score Predictivo:** Motor algorítmico que calcula la compatibilidad candidato-cargo, aprendiendo de perfiles exitosos para optimizar la selección masiva. **[ML]**
- **Auditoría de Sesgos:** Análisis estadístico para detectar y mitigar disparidades de avance en la selección según cualquier dimensión demográfica o clúster. **[ML]**
- **NPS del Candidato:** Medición de la experiencia del postulante (Candidate Experience) para optimizar la marca empleadora y los procesos de atracción. **[DESC]**

**03. ONBOARDING & INTEGRACIÓN**

- **Procesos Activos:** Control de integraciones en curso. Monitorea avance de checklists y activa alertas tempranas sobre hitos críticos de adaptación. **[DESC]**
- **Tiempo a Productividad:** Medición del tiempo requerido para alcanzar el estándar de desempeño, proyectando curvas de aprendizaje según el perfil de ingreso. **[DESC] [PRED]**
- **Rotación Temprana (<90 días):** Análisis de desvinculaciones prematuras para intervenir preventivamente en grupos con alto riesgo de abandono inicial. **[DESC] [PRED]**

**04. ANÁLISIS DE CICLO DE VIDA & CLÚSTERES**

- **Comportamiento de Grupos & Ciclo de Vida:** Seguimiento longitudinal del personal para detectar patrones de retención y curvas de aprendizaje mediante filtros multidimensionales aplicados a clústeres. **[DESC] [ML]**
- **Causalidad & Correlaciones:** Análisis de impacto cruzado. Determina si variables de procesos previos (ej. selección) explican resultados futuros en el ciclo de vida del colaborador. **[ML]**
- **Mapa de Momentos Críticos:** Identificación de hitos donde la probabilidad de desvinculación o caída de desempeño aumenta, facilitando la planificación de intervenciones. **[PRED]**

**05. FUERZA LABORAL & ESTRUCTURA**

- **Demografía & Headcount:** Evolución de la dotación activa con capacidad de segmentación dinámica bajo cualquier atributo o dimensión del modelo de datos de GDH. **[DESC]**
- **Organigrama Integral:** Visualización jerárquica interactiva que muestra la relación entre posiciones y personas en toda la estructura. **[DESC]**
- **Organigrama de Posiciones:** Mapeo de capacidad instalada, identificando vacantes, posiciones congeladas y excedentes por nodo organizacional. **[DESC]**
- **Organigrama de Costos:** Distribución del presupuesto salarial sobre el árbol jerárquico basado en el costo real de las posiciones activas. **[DESC]**
- **Distribución Geográfica:** Análisis de densidad laboral bajo atributos geo-organizativos, contrastando la capacidad instalada frente a sedes o regiones. **[DESC]**
- **Forecast de Dotación:** Proyección predictiva de requerimientos de personal integrando vacantes aprobadas y tendencias de salidas naturales. **[PRED]**

**06. NÓMINA, COSTOS & EQUIDAD**

- **Estructura & Bandas Salariales:** Visualización de la posición de pago individual y agrupada frente a bandas establecidas para detectar desviaciones u outliers. **[DESC]**
- **Equidad Interna:** Auditoría salarial ajustada por variables de control para aislar brechas de compensación no justificadas objetivamente. **[DESC] [ML]**
- **Compa-Ratio vs. Mercado:** Análisis de competitividad salarial frente a referencias externas para identificar riesgos de fuga por desajuste económico. **[DESC]**
- **Masa Salarial & Presupuesto:** Ejecución financiera mensual de la nómina comparada con el presupuesto asignado en las diferentes agrupaciones de la compañía. **[DESC]**
- **Impacto Financiero de la Rotación:** Cuantificación económica de desvinculaciones, integrando costos de indemnización y duplicidad de gasto por reemplazos vs. presupuesto anual. **[DESC] [PRED]**
- **Simulador de Escenarios Salariales:** Herramienta para modelar el impacto presupuestario de ajustes, cambios de bandas o nuevas políticas de compensación. **[PRED]**

**07. TIEMPO, ASISTENCIA & BIENESTAR**

- **Ausentismo & Permisos:** Mapa de calor y modelos predictivos para anticipar ausencias, analizando el comportamiento individual frente a la tendencia del clúster. **[DESC] [PRED] [ML]**
- **Horas Extra & Jornada:** Control de sobretiempos e ineficiencias de costo entre horas normales y extras frente a umbrales legales. **[DESC]**
- **Malla de Vacaciones:** Planificación visual y control de saldos acumulados para mitigar sobrecostos por penalidades y asegurar continuidad operativa. **[DESC]**
- **Salud Ocupacional (SST):** Monitoreo de siniestralidad, accidentes y seguimiento de planes de acción correctiva bajo cumplimiento normativo. **[DESC]**
- **Índice de Bienestar & Burnout:** Modelo algorítmico de riesgo de agotamiento basado en señales operativas y comportamentales para intervenciones preventivas. **[DESC] [ML]**
- **Optimización de Turnos:** Motor prescriptivo (LSTM + Algoritmos Genéticos) para la planificación de mallas horarias minimizando costos de horas extra. **[ML] [OPT]**

**08. GESTIÓN DEL DESEMPEÑO**

- **Evaluación 360°:** Feedback multifuente sintetizado por IA Generativa para obtener resúmenes ejecutivos de fortalezas y brechas por colaborador. **[DESC] [IA] [NLP]**
- **Avance de OKRs / KPIs:** Seguimiento del cumplimiento de metas individuales y colectivas, proyectando la brecha al cierre del ciclo. **[DESC]**
- **Planes de Mejora (PIP):** Trazabilidad de compromisos y resultados de colaboradores en programas de recuperación de rendimiento. **[DESC]**
- **Ranking & Top Performers:** Identificación de talento superior sostenido para priorizar acciones de reconocimiento y retención estratégica. **[DESC]**

**09. TALENTO & DESARROLLO**

- **Matriz 9-Box:** Visualización estratégica de potencial vs. desempeño para orientar la inversión en desarrollo y planes de carrera. **[DESC] [ML]**
- **Continuidad & Sucesión de Liderazgo:** Gestión estratégica de cuadros directivos y posiciones críticas: evaluación de sucesores y niveles de preparación. **[DESC]**
- **Movilidad Interna:** Matching algorítmico entre vacantes y colaboradores basado en skills, trayectoria y aspiraciones para fomentar la retención. **[ML]**
- **Ejecución de L&D:** Monitoreo de adopción de programas formativos y cumplimiento de rutas de aprendizaje a nivel corporativo. **[DESC] [ML]**
- **ROI de Capacitación:** Medición del impacto de la formación relacionando costos con mejoras en desempeño, retención y productividad. **[DESC] [PRED]**

**10. ENGAGEMENT & SENTIMIENTO ORGANIZACIONAL**

- **Engagement & Sentimiento (eNPS):** Consolidado de percepción y procesamiento NLP de feedback cualitativo para detectar tópicos y sentimientos emergentes. **[DESC] [NLP]**
- **Heatmap de Engagement:** Matriz multidimensional para identificar clústeres organizativos con mayor riesgo de desconexión cultural. **[DESC]**
- **Diversidad & Inclusión (DEI):** Auditoría de representatividad y equidad en procesos de promoción y desarrollo bajo dimensiones demográficas diversas. **[DESC]**

**11. COMPLIANCE & RELACIONES LABORALES**

- **Cumplimiento Laboral:** Panel de control de obligaciones legales, contratos y semáforos de riesgo normativo por fecha. **[DESC]**
- **Relaciones Sindicales:** Monitoreo de afiliaciones, desafiliaciones y seguimiento de acuerdos colectivos vigentes. **[DESC]**

**12. RETENCIÓN & RIESGO DE FUGA**

- **Score Predictivo de Fuga:** Segmentación de riesgo de renuncia individual (0-100) basada en señales de desempeño, clima, compensación y ausentismo. **[ML] [XAI]**
- **Benchmarking de Turnover:** Comparativa de tasas de rotación internas frente a promedios del mercado e industria. **[DESC]**
- **Correlación Manager-Fuga:** Detección estadística de patrones de rotación atípicos vinculados a liderazgos específicos para intervenciones focalizadas. **[ML]**

**13. CALIDAD DE DATOS**

- **Integridad de Sistemas & Auditoría:** Monitoreo de la confiabilidad de la información, identificando campos inconsistentes o vacíos. **[DESC]**
- **Log de Datos Maestros:** Trazabilidad de modificaciones críticas en salarios, posiciones y estructura organizacional. **[DESC]**
- **Diccionario de Datos:** Repositorio centralizado de reglas de negocio, fórmulas y definiciones estandarizadas de métricas de GDH. **[DESC]**

---

**Leyenda Metodológica:**

- `[DESC]` Descriptivo
- `[PRED]` Predictivo
- `[ML]` Machine Learning
- `[IA]` IA Generativa
- `[NLP]` Lenguaje Natural
- `[OPT]` Optimización
- `[XAI]` Explicabilidad (SHAP / Interpretabilidad)
