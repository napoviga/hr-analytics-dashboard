# 📂 Enterprise HR Analytics Dashboard - Master Documentation (Documentación Maestra)

## 1. Overview (Visión General y Objetivos)

Desarrollo de una plataforma analítica integral (Modern Data Stack) para la Gestión del Desarrollo Humano (GDH) y operaciones cruzadas. El objetivo del sistema es proporcionar una visualización analítica técnica y escalable a los distintos subprocesos de GDH, estructurados a través de los siguientes módulos:

- Visión General
- Estructura Organizativa (Organigrama Integral, Dotación y Costos)
- Compensaciones
- Fuga de Talento
- Desempeño
- Gestión de Turnos
- Reclutamiento
- Capacitación
- Clima Laboral
- Diversidad (DEI)
- Auditoría de Datos

* **UI/UX Vision:** Interfaz de usuario diseñada con estándares corporativos sobrios (inspiración Microsoft 365), utilizando un Sidebar colapsable dinámico y navegación por submenús para una experiencia de usuario fluida y escalable.

---

## 2. Architecture & Tech Stack (Arquitectura y Stack Tecnológico)

### Backend & Data Engineering (Fase 1 - Completada)

- **Database (Base de Datos):** Supabase (PostgreSQL) - Proyecto `hr-analytics-db` (Región: São Paulo).
- **Data Architecture (Arquitectura de Datos):** Modelo Medallion implementado y automatizado.
  - **Capa `raw` (Bronce):** Ingesta cruda en formato texto (`TEXT`) para evitar bloqueos por formato.
  - **Capa `business` (Oro):** Vistas transformadas dinámicamente con tipos de datos correctos (`INTEGER`, `REAL`), listas para consumo analítico.
- **ETL Pipeline:** Python 3.11, Pandas, SQLAlchemy para conexión nativa y Supabase ORM.

### Frontend & UI Development (Fase 2 - En proceso)

- **Web Framework:** React.js + Vite (Single Page Application).
- **AI Tools (Herramientas IA):** Google Antigravity (IDE de orquestación de agentes) y Google Stitch (Generación UI).
- **Styling & Components (Estilos):** Tailwind CSS, Headless UI (menús dinámicos), y Lucide-React (Iconografía corporativa).
- **Data Visualization (Visualización):** Apache ECharts y componentes funcionales nativos de React.
- **Data Grids (Tablas Dinámicas):** TanStack Table.

---

## 3. Directory Structure & Terminology (Diccionario de Estructura y Entorno)

### 3.1. Folder Structure (Estructura de Carpetas - Separation of Concerns)

- `/data`: Insumos crudos y datasets estáticos (ej. `ibm_hr.csv`).
- `/etl_pipeline`: Scripts secuenciales de Python para limpieza y subida de datos a la nube:
  - `01_setup_raw.py`: Crea la estructura base de aterrizaje.
  - `02_ingest_data.py`: Ejecuta la carga masiva (batch) a la base de datos.
  - `03_setup_business.py`: Genera la capa de vistas analíticas y permisos.
- `/client`: Aplicación web interactiva (React / Vite).
- `.env`: Credenciales seguras (excluido del control de versiones).
- `.gitignore`: Reglas de seguridad para no subir archivos sensibles al repositorio.
- `README.md`: Este documento maestro.

---

## 4. Scope & Business Modules (Alcance Funcional y Módulos)

El dashboard cuenta con un menú lateral (`Sidebar` desplegable estilo Microsoft 365) estructurado en los siguientes módulos:

1. **Organizational Structure (Estructura Organizativa) [✅ En Producción]**
   - Panel interactivo con KPIs ejecutivos y navegación por submenús (Acordeón).
   - **Organigrama Integral:** Vista de la jerarquía empresarial (Dirección, Ventas, I&D, RRHH).
   - **Organigrama de Dotación & Costos:** (En construcción).

2. **Compensations & Salary Bands (Compensaciones y Bandas Salariales) [✅ En Producción]**
   - Análisis de equidad interna conectando directamente a la vista `business`.
   - Visualización de Tarifa Diaria Promedio vs Edad.

3. **Talent Lifecycle (Ciclo de Vida del Talento - Core GDH)**
   - Atracción, Formación, Gestión del Desempeño y Comunicación Interna.

4. **HR Attrition & Demographics (Deserción y Demografía)**
   - Basado en el dataset base (IBM HR Analytics).

5. **Workforce Optimization & Scheduling (Optimización de Fuerza Laboral)**
   - Espacio analítico para optimización de turnos.

6. **Operations & Integral Indicators (Operaciones e Indicadores Integrales)**
   - Cruce de parámetros operativos con costos de personal.

7. **IT Services & SLA Tracker (Servicios IT y SLAs)**
   - Monitoreo de servicios internos y KPIs de atención.

8. **Data Management (Auditoría de Datos) [✅ En Producción]**
   - Vista de tabla dinámica para auditoría de registros en crudo.

---

## 5. Development Environment (Entorno de Desarrollo - Setup Local)

Extensiones clave instaladas en el IDE (Google Antigravity) para garantizar la calidad del código:

- **Python Backend:** `ms-python.python`, `ms-python.debugpy`, `ms-python.vscode-python-envs`, `meta.pyrefly`.
- **Frontend React:** `bradlc.vscode-tailwindcss`, `esbenp.prettier-vscode`, `dbaeumer.vscode-eslint`, `dsznajder.es7-react-js-snippets`.
- **Security:** `mikestead.dotenv` (para lectura segura de variables de entorno).

---

## 6. Installation & Deployment Guide (Guía de Instalación y Despliegue)

Para levantar el proyecto en un entorno local, sigue esta secuencia de comandos:

### 1. Ingesta de Datos (ETL)

Asegúrate de configurar tu archivo `.env` en la raíz con la `DATABASE_URL` del ORM de Supabase.

```bash
cd etl_pipeline
python 01_setup_raw.py
python 02_ingest_data.py
python 03_setup_business.py
cd ..
```
