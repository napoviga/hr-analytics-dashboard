# 🎨 GDH Analytics - Design System & UI Guidelines

Este documento es la **fuente de la verdad** para todas las decisiones de UI/UX y Tailwind CSS del proyecto. CUALQUIER componente nuevo o refactorizado debe obedecer estas reglas estrictamente para garantizar la ergonomía visual y la consistencia corporativa.

## 1. Paleta de Colores (Ergonomía Visual)
Para evitar la fatiga visual (Eye Strain) y la aberración cromática, se utiliza la paleta "Corporate Slate & Blue". 
* 🚫 **ESTRICTAMENTE PROHIBIDO:** Usar `text-black`, `text-gray-900`, `indigo`, `purple`, `violet`, `fuchsia` o `red` puro en textos de lectura o fondos estructurales.
* ✅ **Textos Principales (Títulos):** `text-slate-800`
* ✅ **Textos Secundarios (Descripciones):** `text-slate-500`
* ✅ **Acentos y Botones:** `text-blue-600` o `text-blue-700`
* ✅ **Fondos de Tarjetas:** `bg-white border-slate-200`
* ✅ **Fondos Resaltados (Soft Pills/Badges):** `bg-blue-50`

## 2. Jerarquía Tipográfica y Casing
* **Nivel 1 (Migas de Pan / Categorías del Menú):** ALL CAPS y sin tildes. Clases: `text-sm font-bold uppercase tracking-wider text-slate-500`.
* **Nivel 2 (Títulos de Página H1 / Submenús):** Title Case (Primera letra en mayúscula). Clases: `text-2xl font-bold text-slate-800 tracking-tight`. ¡Prohibido usar `uppercase` aquí!
* **Nivel 3 (Tarjetas y KPIs):** Títulos en `text-lg font-semibold text-slate-800`.
* **Nivel 4 (Párrafos):** Sentence case. Clases: `text-sm text-slate-500 leading-relaxed`.

## 3. Arquitectura de Vistas (Cero Redundancia)
* **Layout Principal:** Es el único responsable de renderizar el Título de la Página (H1) y la Miga de Pan. (La Miga de Pan se oculta si la vista actual es una Landing Page general).
* **Componentes Internos:** Está **PROHIBIDO** incluir títulos introductorios (ej. `<h2>Organigrama</h2>`) o párrafos de bienvenida genéricos dentro de los componentes de las vistas (`src/modules/...`). Los componentes deben ir directo al contenido (Filtros, Tarjetas, Gráficos) para maximizar el espacio vertical.

## 4. Visualización de Datos (ECharts)
* **Cero Hardcoding:** Está prohibido quemar categorías, meses o departamentos (ej. `['IT', 'Sales']`) en las opciones de ECharts. Todos los ejes (`xAxis`/`yAxis`) y series deben generarse dinámicamente mapeando la respuesta del backend.
* **Paleta de Gráficos:** Evitar colores primarios puros. Utilizar tonos apastelados o la escala de azules/pizarras corporativos.

---
*Nota para la IA: Antes de crear o modificar cualquier componente visual de React, DEBES leer este documento para alinear tu código a este estándar.*
