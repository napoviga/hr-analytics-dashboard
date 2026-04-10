export const navigationConfig = [
  {
    id: '01-vision-ejecutiva',
    title: 'VISION EJECUTIVA',
    icon: 'LayoutDashboard',
    description: 'Panel de mando para monitoreo general, anomalías y posicionamiento estratégico.',
    subItems: [
      {
        id: 'vision_general',
        title: 'Dashboard C-Level',
        description: 'Panel de mando estratégico con KPIs de GDH en tiempo real. Monitorea métricas consolidadas permitiendo profundizar dinámicamente mediante dimensiones de segmentación.',
        icon: 'BarChart2',
        tags: ['DESC']
      },
      {
        id: 'alertas-anomalias',
        title: 'Alertas & Anomalías',
        description: 'Motor predictivo de desviaciones estadísticas. Identifica quiebres en métricas clave a nivel individual o agrupado y sugiere acciones preventivas.',
        icon: 'AlertTriangle',
        tags: ['PRED', 'ML']
      },
      {
        id: 'benchmarking',
        title: 'Benchmarking de Mercado',
        description: 'Comparativa de indicadores clave frente a estándares externos para asegurar competitividad y posicionamiento sectorial.',
        icon: 'Globe',
        tags: ['DESC']
      }
    ]
  },
  {
    id: '02-reclutamiento',
    title: 'RECLUTAMIENTO & SELECCION',
    icon: 'Users',
    description: 'Métricas de eficiencia, calidad predictiva y experiencia en los procesos de adquisición diferencial de talento.',
    subItems: [
      {
        id: 'eficiencia-ciclos',
        title: 'Eficiencia & Ciclos de Contratación',
        description: 'Medición de flujo e inversión de tiempo por etapa y cobertura de vacantes. Identifica cuellos de botella mediante el análisis de la data histórica del proceso.',
        icon: 'Timer',
        tags: ['DESC']
      },
      {
        id: 'calidad-contratacion',
        title: 'Calidad de Contratación',
        description: 'Evaluación de éxito a mediano y largo plazo (QoH), cruzando el desempeño con el perfil de ingreso individual o por cohortes de contratación.',
        icon: 'Award',
        tags: ['DESC', 'PRED']
      },
      {
        id: 'fit-score',
        title: 'Fit Score Predictivo',
        description: 'Motor algorítmico que calcula la compatibilidad candidato-cargo, aprendiendo de perfiles exitosos para optimizar la selección masiva.',
        icon: 'Target',
        tags: ['ML']
      },
      {
        id: 'auditoria-sesgos',
        title: 'Auditoría de Sesgos',
        description: 'Análisis estadístico para detectar y mitigar disparidades de avance en la selección según cualquier dimensión demográfica o clúster.',
        icon: 'Scale',
        tags: ['ML']
      },
      {
        id: 'nps-candidato',
        title: 'NPS del Candidato',
        description: 'Medición de la experiencia del postulante (Candidate Experience) para optimizar la marca empleadora y los procesos de atracción.',
        icon: 'MessageSquare',
        tags: ['DESC']
      }
    ]
  },
  {
    id: '03-onboarding',
    title: 'ONBOARDING & INTEGRACION',
    icon: 'Rocket',
    description: 'Asegure la inserción exitosa del talento disminuyendo tiempos de productividad y riesgo de abandono.',
    subItems: [
      {
        id: 'procesos-activos',
        title: 'Procesos Activos',
        description: 'Control de integraciones en curso. Monitorea avance de checklists y activa alertas tempranas sobre hitos críticos de adaptación.',
        icon: 'ListChecks',
        tags: ['DESC']
      },
      {
        id: 'tiempo-productividad',
        title: 'Tiempo a Productividad',
        description: 'Medición del tiempo requerido para alcanzar el estándar de desempeño, proyectando curvas de aprendizaje según el perfil de ingreso.',
        icon: 'LineChart',
        tags: ['DESC', 'PRED']
      },
      {
        id: 'rotacion-temprana',
        title: 'Rotación Temprana (<90 días)',
        description: 'Análisis de desvinculaciones prematuras para intervenir preventivamente en grupos con alto riesgo de abandono inicial.',
        icon: 'UserMinus',
        tags: ['DESC', 'PRED']
      }
    ]
  },
  {
    id: '04-ciclo-vida',
    title: 'CICLO DE VIDA & CLUSTERES',
    icon: 'Repeat',
    description: 'Análisis comportamental y seguimiento longitudinal para descubrir hitos que impactan el desempeño.',
    subItems: [
      {
        id: 'comportamiento-grupos',
        title: 'Comportamiento de Grupos',
        description: 'Seguimiento longitudinal del personal para detectar patrones de retención y curvas de aprendizaje mediante filtros multidimensionales.',
        icon: 'UsersIcon', // Changed to UsersIcon to differentiate in lucide-react (Users is used) wait, 'Users' works. we will map.
        tags: ['DESC', 'ML']
      },
      {
        id: 'causalidad-correlaciones',
        title: 'Causalidad & Correlaciones',
        description: 'Análisis de impacto cruzado. Determina si variables previas explican resultados futuros en el ciclo de vida del colaborador.',
        icon: 'Link',
        tags: ['ML']
      },
      {
        id: 'mapa-momentos',
        title: 'Mapa de Momentos Críticos',
        description: 'Identificación de hitos donde la probabilidad de desvinculación o caída de desempeño aumenta, facilitando intervenciones.',
        icon: 'AlertCircle',
        tags: ['PRED']
      }
    ]
  },
  {
    id: '05-fuerza-laboral',
    title: 'FUERZA LABORAL & ESTRUCTURA',
    icon: 'Network',
    description: 'Seleccione una perspectiva para explorar la jerarquía, distribución y métricas de nuestra organización.',
    subItems: [
      {
        id: 'demografia',
        title: 'Demografía & Headcount',
        description: 'Evolución de la dotación activa con capacidad de segmentación dinámica bajo cualquier atributo o dimensión del modelo de datos de GDH.',
        icon: 'PieChart',
        tags: ['DESC']
      },
      {
        id: 'org_integral',
        title: 'Organigrama Integral',
        description: 'Visualización jerárquica interactiva que muestra la relación entre posiciones y personas en toda la estructura.',
        icon: 'GitMerge',
        tags: ['DESC']
      },
      {
        id: 'org_posiciones',
        title: 'Organigrama de Posiciones',
        description: 'Mapeo de capacidad instalada, identificando vacantes, posiciones congeladas y excedentes por nodo organizacional.',
        icon: 'Briefcase',
        tags: ['DESC']
      },
      {
        id: 'org_costos',
        title: 'Organigrama de Costos',
        description: 'Distribución del presupuesto salarial sobre el árbol jerárquico basado en el costo real de las posiciones activas.',
        icon: 'CircleDollarSign',
        tags: ['DESC']
      },
      {
        id: 'distribucion-geografica',
        title: 'Distribución Geográfica',
        description: 'Análisis de densidad laboral bajo atributos geo-organizativos, contrastando la capacidad instalada frente a sedes o regiones.',
        icon: 'Map',
        tags: ['DESC']
      },
      {
        id: 'forecast-dotacion',
        title: 'Forecast de Dotación',
        description: 'Proyección predictiva de requerimientos de personal integrando vacantes aprobadas y tendencias de salidas naturales.',
        icon: 'TrendingUp',
        tags: ['PRED']
      }
    ]
  },
  {
    id: '06-nomina-costos',
    title: 'NOMINA, COSTOS & EQUIDAD',
    icon: 'Wallet',
    description: 'Auditoría y análisis presupuestario, equidad interna e impacto monetario de la fuerza laboral.',
    subItems: [
      {
        id: 'compensaciones',
        title: 'Estructura & Bandas Salariales',
        description: 'Visualización de la posición de pago individual y agrupada frente a bandas establecidas para detectar desviaciones u outliers.',
        icon: 'Layers',
        tags: ['DESC']
      },
      {
        id: 'equidad-interna',
        title: 'Equidad Interna',
        description: 'Auditoría salarial ajustada por variables de control para aislar brechas de compensación no justificadas objetivamente.',
        icon: 'Scale',
        tags: ['DESC', 'ML']
      },
      {
        id: 'compa-ratio',
        title: 'Compa-Ratio vs. Mercado',
        description: 'Análisis de competitividad salarial frente a referencias externas para identificar riesgos de fuga por desajuste económico.',
        icon: 'Percent',
        tags: ['DESC']
      },
      {
        id: 'masa-salarial',
        title: 'Masa Salarial & Presupuesto',
        description: 'Ejecución financiera mensual de la nómina comparada con el presupuesto asignado en las diferentes agrupaciones de la compañía.',
        icon: 'Calculator',
        tags: ['DESC']
      },
      {
        id: 'impacto-financiero',
        title: 'Impacto Financiero de Rotación',
        description: 'Cuantificación económica de desvinculaciones, integrando costos de indemnización y duplicidad de gasto por reemplazos vs presupuesto anual.',
        icon: 'TrendingDown',
        tags: ['DESC', 'PRED']
      },
      {
        id: 'simulador-salarial',
        title: 'Simulador de Escenarios Salariales',
        description: 'Herramienta para modelar el impacto presupuestario de ajustes, cambios de bandas o nuevas políticas de compensación.',
        icon: 'SlidersHorizontal',
        tags: ['PRED']
      }
    ]
  },
  {
    id: '07-tiempo-asistencia',
    title: 'TIEMPO, ASISTENCIA & BIENESTAR',
    icon: 'Clock',
    description: 'Gestione ausentismos, horas extras, turnos y evalúe la carga y el agotamiento operativo.',
    subItems: [
      {
        id: 'ausentismo',
        title: 'Ausentismo & Permisos',
        description: 'Mapa de calor y modelos predictivos para anticipar ausencias, analizando el comportamiento individual frente a la tendencia del clúster.',
        icon: 'CalendarMinus',
        tags: ['DESC', 'PRED', 'ML']
      },
      {
        id: 'horas-extra',
        title: 'Horas Extra & Jornada',
        description: 'Control de sobretiempos e ineficiencias de costo entre horas normales y extras frente a umbrales legales.',
        icon: 'Watch',
        tags: ['DESC']
      },
      {
        id: 'malla-vacaciones',
        title: 'Malla de Vacaciones',
        description: 'Planificación visual y control de saldos acumulados para mitigar sobrecostos por penalidades y asegurar continuidad operativa.',
        icon: 'Palmtree',
        tags: ['DESC']
      },
      {
        id: 'salud-ocupacional',
        title: 'Salud Ocupacional (SST)',
        description: 'Monitoreo de siniestralidad, accidentes y seguimiento de planes de acción correctiva bajo cumplimiento normativo.',
        icon: 'ShieldPlus',
        tags: ['DESC']
      },
      {
        id: 'indice-bienestar',
        title: 'Índice de Bienestar & Burnout',
        description: 'Modelo algorítmico de riesgo de agotamiento basado en señales operativas y comportamentales para intervenciones preventivas.',
        icon: 'HeartPulse',
        tags: ['DESC', 'ML']
      },
      {
        id: 'optimizacion-turnos',
        title: 'Optimización de Turnos',
        description: 'Motor prescriptivo (LSTM + Algoritmos Genéticos) para la planificación de mallas horarias minimizando costos de horas extra.',
        icon: 'Settings2',
        tags: ['ML', 'OPT']
      }
    ]
  },
  {
    id: '08-gestion-desempeno',
    title: 'GESTION DEL DESEMPEÑO',
    icon: 'Target',
    description: 'Evaluación y trazabilidad del rendimiento y aportes de cada colaborador en la organización.',
    subItems: [
      {
        id: 'evaluacion-360',
        title: 'Evaluación 360°',
        description: 'Feedback multifuente sintetizado por IA Generativa para obtener resúmenes ejecutivos de fortalezas y brechas por colaborador.',
        icon: 'RefreshCw',
        tags: ['DESC', 'IA', 'NLP']
      },
      {
        id: 'avance-okrs',
        title: 'Avance de OKRs / KPIs',
        description: 'Seguimiento del cumplimiento de metas individuales y colectivas, proyectando la brecha al cierre del ciclo.',
        icon: 'CheckSquare',
        tags: ['DESC']
      },
      {
        id: 'planes-mejora',
        title: 'Planes de Mejora (PIP)',
        description: 'Trazabilidad de compromisos y resultados de colaboradores en programas de recuperación de rendimiento.',
        icon: 'TrendingUp',
        tags: ['DESC']
      },
      {
        id: 'ranking',
        title: 'Ranking & Top Performers',
        description: 'Identificación de talento superior sostenido para priorizar acciones de reconocimiento y retención estratégica.',
        icon: 'Trophy',
        tags: ['DESC']
      }
    ]
  },
  {
    id: '09-talento-desarrollo',
    title: 'TALENTO & DESARROLLO',
    icon: 'BookOpen',
    description: 'Gestione planes de carrera, ROI formativo, movilidad y asegure la continuidad del negocio.',
    subItems: [
      {
        id: 'matriz-9box',
        title: 'Matriz 9-Box',
        description: 'Visualización estratégica de potencial vs. desempeño para orientar la inversión en desarrollo y planes de carrera.',
        icon: 'Grid',
        tags: ['DESC', 'ML']
      },
      {
        id: 'continuidad-liderazgo',
        title: 'Continuidad & Sucesión',
        description: 'Gestión estratégica de cuadros directivos y posiciones críticas: evaluación de sucesores y niveles de preparación.',
        icon: 'Users',
        tags: ['DESC']
      },
      {
        id: 'movilidad-interna',
        title: 'Movilidad Interna',
        description: 'Matching algorítmico entre vacantes y colaboradores basado en skills, trayectoria y aspiraciones para fomentar la retención.',
        icon: 'ArrowRightLeft',
        tags: ['ML']
      },
      {
        id: 'ejecucion-ld',
        title: 'Ejecución de L&D',
        description: 'Monitoreo de adopción de programas formativos y cumplimiento de rutas de aprendizaje a nivel corporativo.',
        icon: 'BookMarked',
        tags: ['DESC', 'ML']
      },
      {
        id: 'roi-capacitacion',
        title: 'ROI de Capacitación',
        description: 'Medición del impacto de la formación relacionando costos con mejoras en desempeño, retención y productividad.',
        icon: 'LineChart',
        tags: ['DESC', 'PRED']
      }
    ]
  },
  {
    id: '10-engagement-sentimiento',
    title: 'ENGAGEMENT & SENTIMIENTO',
    icon: 'Smile',
    description: 'Auditoría cultural, eNPS, y procesamiento NLP para detectar la temperatura organizacional y DEI.',
    subItems: [
      {
        id: 'engagement-enps',
        title: 'Engagement & Sentimiento (eNPS)',
        description: 'Consolidado de percepción y procesamiento NLP de feedback cualitativo para detectar tópicos y sentimientos emergentes.',
        icon: 'Heart',
        tags: ['DESC', 'NLP']
      },
      {
        id: 'heatmap-engagement',
        title: 'Heatmap de Engagement',
        description: 'Matriz multidimensional para identificar clústeres organizativos con mayor riesgo de desconexión cultural.',
        icon: 'Thermometer',
        tags: ['DESC']
      },
      {
        id: 'diversidad-inclusion',
        title: 'Diversidad & Inclusión (DEI)',
        description: 'Auditoría de representatividad y equidad en procesos de promoción y desarrollo bajo dimensiones demográficas diversas.',
        icon: 'Globe',
        tags: ['DESC']
      }
    ]
  },
  {
    id: '11-compliance',
    title: 'COMPLIANCE & RELACIONES',
    icon: 'Shield',
    description: 'Control de riesgos normativos, relaciones laborales y obligaciones legales a nivel corporativo.',
    subItems: [
      {
        id: 'cumplimiento-laboral',
        title: 'Cumplimiento Laboral',
        description: 'Panel de control de obligaciones legales, contratos y semáforos de riesgo normativo por fecha.',
        icon: 'FileText',
        tags: ['DESC']
      },
      {
        id: 'relaciones-sindicales',
        title: 'Relaciones Sindicales',
        description: 'Monitoreo de afiliaciones, desafiliaciones y seguimiento de acuerdos colectivos vigentes.',
        icon: 'Handshake',
        tags: ['DESC']
      }
    ]
  },
  {
    id: '12-retencion',
    title: 'RETENCION & RIESGO DE FUGA',
    icon: 'UserMinus',
    description: 'Análisis y prevención de la pérdida de talento, scores predictivos y comparativas de turnover.',
    subItems: [
      {
        id: 'score-fuga',
        title: 'Score Predictivo de Fuga',
        description: 'Segmentación de riesgo de renuncia individual (0-100) basada en señales de desempeño, clima, compensación y ausentismo.',
        icon: 'Activity',
        tags: ['ML', 'XAI']
      },
      {
        id: 'benchmarking-turnover',
        title: 'Benchmarking de Turnover',
        description: 'Comparativa de tasas de rotación internas frente a promedios del mercado e industria.',
        icon: 'BarChart',
        tags: ['DESC']
      },
      {
        id: 'correlacion-manager',
        title: 'Correlación Manager-Fuga',
        description: 'Detección estadística de patrones de rotación atípicos vinculados a liderazgos específicos para intervenciones focalizadas.',
        icon: 'Users',
        tags: ['ML']
      }
    ]
  },
  {
    id: '13-calidad-datos',
    title: 'CALIDAD DE DATOS',
    icon: 'Database',
    description: 'Audite la integridad y salud del modelo de datos e infraestructura para confianza analítica.',
    subItems: [
      {
        id: 'auditoria',
        title: 'Integridad de Sistemas & Auditoría',
        description: 'Monitoreo de la confiabilidad de la información, identificando campos inconsistentes o vacíos.',
        icon: 'Search',
        tags: ['DESC']
      },
      {
        id: 'log-datos-maestros',
        title: 'Log de Datos Maestros',
        description: 'Trazabilidad de modificaciones críticas en salarios, posiciones y estructura organizacional.',
        icon: 'History',
        tags: ['DESC']
      },
      {
        id: 'diccionario-datos',
        title: 'Diccionario de Datos',
        description: 'Repositorio centralizado de reglas de negocio, fórmulas y definiciones estandarizadas de métricas de GDH.',
        icon: 'Book',
        tags: ['DESC']
      }
    ]
  }
];
