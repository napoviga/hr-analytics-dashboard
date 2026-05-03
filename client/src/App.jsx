import { useState, useEffect } from 'react'
import { useEmpleados } from './hooks/useEmpleados'
import Sidebar from './modules/00-layout/Sidebar'
import SectionLanding from './modules/00-layout/SectionLanding'
import { navigationConfig } from './config/navigation'

// Componentes
import EmployeeTable from './modules/05-fuerza-laboral/EmployeeTable'
import Overview from './modules/00-layout/Overview'
import Compensaciones from './modules/06-nomina-costos/Compensations'
import OrgStructure from './modules/05-fuerza-laboral/OrgStructure'
import OrganigramaIntegral from './modules/05-fuerza-laboral/OrganigramaIntegral'
import Demographics from './modules/05-fuerza-laboral/Demographics'
import EquidadInterna from './modules/06-nomina-costos/EquidadInterna'
import CompaRatio from './modules/06-nomina-costos/CompaRatio'
import MasaSalarial from './modules/06-nomina-costos/MasaSalarial'
import ImpactoFinanciero from './modules/06-nomina-costos/ImpactoFinanciero'
import SimuladorSalarial from './modules/06-nomina-costos/SimuladorSalarial'
import AlertasAnomalias from './modules/01-vision-ejecutiva/AlertasAnomalias'
import Benchmarking from './modules/01-vision-ejecutiva/Benchmarking'
import LogDatosMaestros from './modules/13-calidad-datos/LogDatosMaestros'
import DiccionarioDatos from './modules/13-calidad-datos/DiccionarioDatos'

// Fase 3 Components
import EficienciaCiclos from './modules/02-reclutamiento/EficienciaCiclos'
import CalidadContratacion from './modules/02-reclutamiento/CalidadContratacion'
import FitScore from './modules/02-reclutamiento/FitScore'
import AuditoriaSesgos from './modules/02-reclutamiento/AuditoriaSesgos'
import NpsCandidato from './modules/02-reclutamiento/NpsCandidato'
import ProcesosActivos from './modules/03-onboarding/ProcesosActivos'
import TiempoProductividad from './modules/03-onboarding/TiempoProductividad'
import RotacionTemprana from './modules/03-onboarding/RotacionTemprana'
import ComportamientoGrupos from './modules/04-ciclo-vida/ComportamientoGrupos'
import CausalidadCorrelaciones from './modules/04-ciclo-vida/CausalidadCorrelaciones'
import MapaMomentos from './modules/04-ciclo-vida/MapaMomentos'

// Fase 4 Components
import Ausentismo from './modules/07-tiempo-asistencia/Ausentismo'
import HorasExtra from './modules/07-tiempo-asistencia/HorasExtra'
import MallaVacaciones from './modules/07-tiempo-asistencia/MallaVacaciones'
import SaludOcupacional from './modules/07-tiempo-asistencia/SaludOcupacional'
import Evaluacion360 from './modules/08-gestion-desempeno/Evaluacion360'
import AvanceOKRs from './modules/08-gestion-desempeno/AvanceOKRs'
import PlanesMejora from './modules/08-gestion-desempeno/PlanesMejora'
import RankingPerformers from './modules/08-gestion-desempeno/RankingPerformers'
import MatrizNineBox from './modules/09-talento-desarrollo/MatrizNineBox'
import MapaSucesion from './modules/09-talento-desarrollo/MapaSucesion'
import BrechasSkills from './modules/09-talento-desarrollo/BrechasSkills'
import RoiCapacitacion from './modules/09-talento-desarrollo/RoiCapacitacion'

// Fase 5 Components
import EngagementENPS from './modules/10-engagement-sentimiento/EngagementENPS'
import HeatmapEngagement from './modules/10-engagement-sentimiento/HeatmapEngagement'
import DiversidadInclusion from './modules/10-engagement-sentimiento/DiversidadInclusion'
import CumplimientoLaboral from './modules/11-compliance/CumplimientoLaboral'
import RelacionesSindicales from './modules/11-compliance/RelacionesSindicales'
import ScoreFuga from './modules/12-retencion/ScoreFuga'
import BenchmarkingTurnover from './modules/12-retencion/BenchmarkingTurnover'
import CorrelacionManager from './modules/12-retencion/CorrelacionManager'

function App() {
  const { empleados, errorBd } = useEmpleados()
  
  // Por defecto iniciamos en el primer módulo
  const [vistaActual, setVistaActual] = useState('01-vision-ejecutiva')

  // Lógica Breadcrumbs y Mapeo de Vista
  let activeModuleName = '';
  let activeSubName = '';
  let activeModuleObj = null;

  for (const module of navigationConfig) {
    if (module.id === vistaActual) {
      activeModuleName = module.title;
      activeModuleObj = module;
      break;
    }
    const sub = module.subItems?.find(s => s.id === vistaActual);
    if (sub) {
      activeModuleName = module.title;
      activeSubName = sub.title;
      break;
    }
  }

  // Soporte a módulos de Administración no mapeados en navigationConfig principal
  if (!activeModuleName && vistaActual === 'roles_permisos') { activeModuleName = 'Administración'; activeSubName = 'Roles & Permisos (RLS)'; }
  if (!activeModuleName && vistaActual === 'conexiones_etl') { activeModuleName = 'Administración'; activeSubName = 'Conexiones ETL & Fuentes'; }

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden text-slate-800">
      <Sidebar vistaActual={vistaActual} setVistaActual={setVistaActual} />

      <main className="flex-1 overflow-y-auto p-10">
        {errorBd ? (
          <div className="bg-red-900 text-red-200 p-4 rounded-lg mt-4 text-sm font-mono shadow-md max-w-7xl mx-auto">
            <strong>🚨 Error de Conexión:</strong> {errorBd}
          </div>
        ) : (
          <div className="h-full">
            {/* Si estamos en la raíz del módulo, mostramos la Landing Section de ese módulo */}
            {activeModuleObj ? (
              <SectionLanding module={activeModuleObj} onNavigate={setVistaActual} />
            ) : (
              /* Si estamos dentro de un sub-item, mostramos su gráfico correspondiente con el Header Breadcrumb */
              <div className="max-w-7xl mx-auto">
                <header className="mb-8">
                  <div className="flex flex-col gap-1">
                    {activeModuleName && activeModuleName.toLowerCase() !== (activeSubName || '').toLowerCase() && (
                      <span className="text-sm font-bold uppercase tracking-wider text-slate-500 mb-1">
                        {activeModuleName}
                      </span>
                    )}
                    <h1 className="text-3xl font-extrabold text-slate-800 tracking-tight">
                      {activeSubName || 'GDH Analytics'}
                    </h1>
                  </div>
                </header>

                {/* Vistas Específicas */}
                {vistaActual === 'vision_general' && <Overview data={empleados} />}
                {vistaActual === 'demografia' && <Demographics />} 
                {vistaActual === 'org_posiciones' && <OrgStructure setVistaActual={setVistaActual} />} 
                {vistaActual === 'org_integral' && <OrganigramaIntegral />}
                {vistaActual === 'compensaciones' && <Compensaciones data={empleados} />}
                {vistaActual === 'auditoria' && <EmployeeTable data={empleados} />}
                {vistaActual === 'alertas-anomalias' && <AlertasAnomalias />}
                {vistaActual === 'benchmarking' && <Benchmarking />}
                {vistaActual === 'equidad-interna' && <EquidadInterna />}
                {vistaActual === 'compa-ratio' && <CompaRatio />}
                {vistaActual === 'masa-salarial' && <MasaSalarial />}
                {vistaActual === 'impacto-financiero' && <ImpactoFinanciero />}
                {vistaActual === 'simulador-salarial' && <SimuladorSalarial />}
                {vistaActual === 'log-datos-maestros' && <LogDatosMaestros />}
                {vistaActual === 'diccionario-datos' && <DiccionarioDatos />}
                {vistaActual === 'eficiencia-ciclos' && <EficienciaCiclos />}
                {vistaActual === 'calidad-contratacion' && <CalidadContratacion />}
                {vistaActual === 'fit-score' && <FitScore />}
                {vistaActual === 'auditoria-sesgos' && <AuditoriaSesgos />}
                {vistaActual === 'nps-candidato' && <NpsCandidato />}
                {vistaActual === 'procesos-activos' && <ProcesosActivos />}
                {vistaActual === 'tiempo-productividad' && <TiempoProductividad />}
                {vistaActual === 'rotacion-temprana' && <RotacionTemprana />}
                {vistaActual === 'comportamiento-grupos' && <ComportamientoGrupos />}
                {vistaActual === 'causalidad-correlaciones' && <CausalidadCorrelaciones />}
                {vistaActual === 'mapa-momentos' && <MapaMomentos />}
                {vistaActual === 'ausentismo' && <Ausentismo />}
                {vistaActual === 'horas-extra' && <HorasExtra />}
                {vistaActual === 'optimizacion-turnos' && <MallaVacaciones />}
                {vistaActual === 'indice-bienestar' && <SaludOcupacional />}
                {vistaActual === 'evaluacion-360' && <Evaluacion360 />}
                {vistaActual === 'avance-okrs' && <AvanceOKRs />}
                {vistaActual === 'planes-mejora' && <PlanesMejora />}
                {vistaActual === 'ranking' && <RankingPerformers />}
                {vistaActual === 'matriz-9box' && <MatrizNineBox />}
                {vistaActual === 'continuidad-liderazgo' && <MapaSucesion />}
                {vistaActual === 'movilidad-interna' && <BrechasSkills />}
                {vistaActual === 'ejecucion-ld' && <RoiCapacitacion />}
                {vistaActual === 'roi-capacitacion' && <RoiCapacitacion />}
                {vistaActual === 'engagement-enps' && <EngagementENPS />}
                {vistaActual === 'heatmap-engagement' && <HeatmapEngagement />}
                {vistaActual === 'diversidad-inclusion' && <DiversidadInclusion />}
                {vistaActual === 'cumplimiento-laboral' && <CumplimientoLaboral />}
                {vistaActual === 'relaciones-sindicales' && <RelacionesSindicales />}
                {vistaActual === 'score-fuga' && <ScoreFuga />}
                {vistaActual === 'benchmarking-turnover' && <BenchmarkingTurnover />}
                {vistaActual === 'correlacion-manager' && <CorrelacionManager />}

                {/* Placeholder Dinámico si la vista aún no está construida */}
                {![
                  'vision_general', 'demografia', 'org_posiciones', 'org_integral', 'compensaciones', 'auditoria',
                  'alertas-anomalias', 'benchmarking', 'equidad-interna', 'compa-ratio', 'masa-salarial', 'impacto-financiero', 
                  'simulador-salarial', 'log-datos-maestros', 'diccionario-datos',
                  'eficiencia-ciclos', 'calidad-contratacion', 'fit-score', 'auditoria-sesgos', 'nps-candidato',
                  'procesos-activos', 'tiempo-productividad', 'rotacion-temprana',
                  'comportamiento-grupos', 'causalidad-correlaciones', 'mapa-momentos',
                  'ausentismo', 'horas-extra', 'malla-vacaciones', 'salud-ocupacional',
                  'evaluacion-360', 'avance-okrs', 'planes-mejora', 'ranking',
                  'matriz-9box', 'continuidad-liderazgo', 'movilidad-interna', 'ejecucion-ld', 'roi-capacitacion',
                  'engagement-enps', 'heatmap-engagement', 'diversidad-inclusion',
                  'cumplimiento-laboral', 'relaciones-sindicales',
                  'score-fuga', 'benchmarking-turnover', 'correlacion-manager', 'optimizacion-turnos', 'indice-bienestar'
                ].includes(vistaActual) && (
                  <div className="flex flex-col items-center justify-center p-24 bg-white shadow-sm border border-slate-100 rounded-2xl mt-8">
                    <div className="w-16 h-16 bg-blue-50 text-blue-500 rounded-full flex flex-col items-center justify-center mb-6">
                       <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" /></svg>
                    </div>
                    <h3 className="text-xl font-bold text-slate-800 mb-2">Desarrollo en Progreso 🚀</h3>
                    <p className="text-slate-500">Estamos conectando los flujos de datos para esta perspectiva de análisis.</p>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  )
}

export default App