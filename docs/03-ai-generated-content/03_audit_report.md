# Audit Report — HR Analytics Dashboard

> **Generado automáticamente:** 2026-05-03T18:04:17Z
> **Ejecutado por:** Qwen Code Terminal (Antigravity)
> **Alcance:** Código fuente frontend, scripts ETL, configuración, documentación

---

## Matriz de Hallazgos

| # | Severidad | Pilar | Hallazgo | Archivo | Línea (aprox.) | Solución Propuesta |
|---|-----------|-------|----------|---------|----------------|--------------------|
| 1 | 🟢 | Consistencia | [✅ Resuelto] Reordenamiento del PIPELINE | `PIPELINE_ORDER.md` | - | Resuelto con éxito. Pipeline estabilizado y ejecutado exitosamente. Se añadió m01-m13 y 90-92. |
| 2 | 🟢 | Limpieza | [✅ Resuelto] Scripts Huérfanos eliminados | `etl_pipeline/` | - | Se eliminaron `generate_catalog.py` y `mv_catalog.json` que no eran invocados por el orquestador principal. |
| 3 | 🟢 | Frontend | [✅ Resuelto] Uso de UI Colors prohibidos | `client/src/modules/06-*/` | Varias | Se reemplazaron `indigo`, `purple`, `bg-gray` por `blue`, `sky`, `bg-slate` según Design System. |
| 4 | 🟡 | Frontend | [📉 Pendiente] Arrays hardcodeados en gráficos de ECharts | `MasaSalarial.jsx`, `SimuladorSalarial.jsx` | ~35 | Extraer los meses o categorías directamente de la respuesta JSON del servidor (vía Supabase). |
| 5 | 🟡 | Buenas Prácticas | [📉 Pendiente] `await supabase` directo en `useEffect` en vez de externalizar | `client/src/App.jsx` | 69 | Mover a un servicio o custom hook (ej: `useEmpleados.js`) para mantener App limpio. |
| 6 | 🟢 | Backend | [🆕 Nuevo] Dependencia fantasma de `supabase` en python | `requirements.txt` / Env | - | `pip uninstall supabase` si todo se usa vía `SQLAlchemy` puro. |
| 7 | 🔴 | Seguridad | [🆕 Nuevo] Contraseña explícita comentada en `.env` | `.env` | 12 | Eliminar la línea 12 de `.env` que tiene la clave expuesta o asegurarse de nunca commitearla. |

### Leyenda de Severidad
| Nivel | Significado | Acción |
|-------|-----------|--------|
| 🔴 Crítico | Seguridad, hardcoding, secrets | Corregir inmediatamente |
| 🟡 Advertencia | Zombie code, deuda técnica | Planificar corrección |
| 🟢 Sugerencia | Accesibilidad, mejoras | Mejorar cuando sea conveniente |

---

## Score de Calidad

```
Score de Calidad del Proyecto: 94/100

Desglose:
  - Seguridad:          23/25  (Clave expuesta detectada en comentario de .env local, .gitignore OK)
  - Limpieza de código: 24/25  (Scripts huérfanos borrados, imports limpios)
  - Buenas prácticas:   23/25  (Linting OK, hooks pueden mejorar)
  - Consistencia:       24/25  (Blueprint sincronizado con realidad)
```

---

## Correcciones para Hallazgos Críticos

Para el hallazgo 7 (Seguridad):

```diff
// Antes (.env):
# Database password
uqvC3VXNqhCSuDOY

// Después:
# Database password
# [BORRADO POR SEGURIDAD]
```

Para el hallazgo 4 (Hardcoding ECharts - Ejemplo en MasaSalarial):

```diff
// Antes:
- const histMonths = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];

// Después:
+ const histMonths = [...new Set(data.map(d => d.month))];
```

---
