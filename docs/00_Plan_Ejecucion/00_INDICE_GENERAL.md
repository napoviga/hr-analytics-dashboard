# 📋 PLAN MAESTRO DE EJECUCIÓN - PIPELINE HR ANALYTICS

## 🎯 Propósito de este Documento
Este plan está diseñado para ser **ejecutado paso a paso con asistencia de IA**. Cada módulo contiene instrucciones secuenciales completas desde la creación de datos hasta la visualización final.

**Importante:** Una vez ejecutado cada módulo, estos documentos pueden ser eliminados. Son guías temporales de implementación.

---

## 📁 Estructura del Plan

Cada módulo tiene su propio archivo `.md` con:
1. **Tablas Raw necesarias** (si aplican)
2. **Vistas Materializadas** (SQL completo)
3. **Script Python** (código listo para copiar)
4. **Funciones RPC** (para interacción frontend)
5. **Componentes React** (con rutas exactas)
6. **Tests de validación**

---

## 🗂️ Módulos del Pipeline

| # | Módulo | Archivo | Vistas | Estado | Prioridad |
|---|--------|---------|--------|--------|-----------|
| 01 | Visión Ejecutiva | `MODULO_01_VISION_EJECUTIVA.md` | 3 | 🔴 33% | ALTA |
| 02 | Reclutamiento & Selección | `MODULO_02_RECLUTAMIENTO.md` | 5 | ⚪ 0% | MEDIA |
| 03 | Onboarding & Integración | `MODULO_03_ONBOARDING.md` | 3 | ⚪ 0% | MEDIA |
| 04 | Ciclo de Vida | `MODULO_04_CICLO_VIDA.md` | 3 | ⚪ 0% | BAJA |
| 05 | Fuerza Laboral | `MODULO_05_FUERZA_LABORAL.md` | 6 | 🟢 100% | COMPLETO |
| 06 | Nómina & Costos | `MODULO_06_NOMINA_COSTOS.md` | 6 | 🔴 17% | ALTA |
| 07 | Tiempo & Bienestar | `MODULO_07_TIEMPO_BIENESTAR.md` | 6 | ⚪ 0% | MEDIA |
| 08 | Gestión del Desempeño | `MODULO_08_DESEMPENO.md` | 4 | ⚪ 0% | MEDIA |
| 09 | Talento & Desarrollo | `MODULO_09_TALENTO.md` | 5 | ⚪ 0% | BAJA |
| 10 | Engagement & Sentimiento | `MODULO_10_ENGAGEMENT.md` | 3 | ⚪ 0% | BAJA |
| 11 | Compliance & Legal | `MODULO_11_COMPLIANCE.md` | 2 | ⚪ 0% | BAJA |
| 12 | Retención & Riesgo | `MODULO_12_RETENCION.md` | 3 | ⚪ 0% | MEDIA |
| 13 | Calidad de Datos | `MODULO_13_CALIDAD_DATOS.md` | 3 | 🟡 33% | BAJA |

**Total:** 52 vistas | **Completitud:** 17% (9/52)

---

## 🚀 Ruta Crítica de Implementación

### FASE 1: ✅ COMPLETADA
- [x] Módulo 05: Fuerza Laboral (base del sistema)

### FASE 2: 🔄 PRIORIDAD ACTUAL (Semana 1-2)
1. **Módulo 06**: Nómina & Costos → `m06_nomina_costos.py` + 5 componentes React
2. **Módulo 01**: Visión Ejecutiva → Completar alertas y benchmarking

### FASE 3: Operaciones RRHH (Semana 3-4)
3. **Módulo 02**: Reclutamiento
4. **Módulo 03**: Onboarding
5. **Módulo 07**: Tiempo & Bienestar

### FASE 4: Talento & Desempeño (Semana 5-6)
6. **Módulo 08**: Gestión del Desempeño
7. **Módulo 09**: Talento & Desarrollo
8. **Módulo 04**: Ciclo de Vida

### FASE 5: Analytics Avanzados (Semana 7-8)
9. **Módulo 10**: Engagement
10. **Módulo 11**: Compliance
11. **Módulo 12**: Retención
12. **Módulo 13**: Calidad de Datos (completar)

---

## 📝 Convenciones de Nomenclatura

### Tablas Raw
```sql
raw.<tabla_descriptiva>
-- Ejemplo: raw.job_postings, raw.attendance_records
```

### Vistas Materializadas
```sql
business.mv_<modulo>_<metrica_principal>
-- Ejemplo: business.mv_salary_bands, business.mv_absenteeism
```

### Scripts Python
```bash
scripts/m<numero>_<nombre_modulo>.py
-- Ejemplo: scripts/m06_nomina_costos.py
```

### Componentes React
```bash
src/components/hr-modules/<ModuloNombre>/<ComponenteSpecific>.jsx
-- Ejemplo: src/components/hr-modules/NominaCostos/SalaryBands.jsx
```

### Funciones RPC
```sql
business.rpc_<accion>_<entidad>()
-- Ejemplo: business.rpc_get_salary_simulator(), business.rpc_alert_threshold()
```

---

## 🔧 Patrón de Pipeline (Para IA)

Cada ejecución sigue esta secuencia:

```bash
# PASO 1: Crear tablas raw (si existen nuevas fuentes)
psql -h <host> -U <user> -d <db> -f scripts/sql/raw_tables_mXX.sql

# PASO 2: Ejecutar script Python para crear MVs
python scripts/mXX_nombre_modulo.py

# PASO 3: Validar que las vistas se crearon
psql -h <host> -U <user> -d <db> -c "SELECT COUNT(*) FROM business.mv_<nombre>;"

# PASO 4: Crear componente React
# (Copiar plantilla del .md a src/components/hr-modules/)

# PASO 5: Registrar ruta en App.jsx o router

# PASO 6: Testear endpoint y visualización
curl http://localhost:8000/rest/v1/business.mv_<nombre>?select=*&limit=5
```

---

## 📊 Dependencias Cruzadas entre Módulos

```
Módulo 01 (Visión Ejecutiva)
  ← Depende de: 05, 06, 08, 10, 12
  → Usado por: Dashboard C-Level

Módulo 06 (Nómina)
  ← Depende de: 05 (employee_base)
  → Usado por: 01, 08, 10

Módulo 08 (Desempeño)
  ← Depende de: 05, 06
  → Usado por: 01, 04, 09, 12

Módulo 12 (Retención)
  ← Depende de: 05, 06, 08, 10
  → Usado por: 01, 04
```

---

## ✅ Checklist por Módulo

Para cada módulo, verificar:

- [ ] Tablas raw creadas (si aplican)
- [ ] Script Python ejecutado sin errores
- [ ] Todas las MVs creadas en schema `business`
- [ ] Índices agregados para performance
- [ ] Grants de lectura otorgados
- [ ] Componentes React creados
- [ ] Rutas registradas en el router
- [ ] Tests de validación pasados
- [ ] Documentación actualizada en README

---

## 🎯 Próximo Paso Inmediato

**Ejecutar Módulo 06 (Nómina & Costos)**

```bash
# 1. Revisar MODULO_06_NOMINA_COSTOS.md
# 2. Ejecutar script: python scripts/m06_nomina_costos.py
# 3. Validar MVs creadas
# 4. Crear 5 componentes React faltantes
# 5. Testear endpoints
```

---

## 📞 Soporte para Ejecución con IA

Cada archivo de módulo incluye prompts listos para copiar y pegar en tu asistente de IA:

```
"IA, por favor ejecuta el PASO 1 del Módulo 06:
Crear las tablas raw según el esquema proporcionado..."
```

---

**Última actualización:** 2025-01-03  
**Responsable:** Equipo HR Analytics  
**Estado:** Listo para ejecución
