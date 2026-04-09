import { useState, useEffect } from 'react'
import { supabase } from './lib/supabaseClient'
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

function App() {
  const [empleados, setEmpleados] = useState([])
  const [errorBd, setErrorBd] = useState(null)
  
  // Por defecto iniciamos en el primer módulo
  const [vistaActual, setVistaActual] = useState('01-vision-ejecutiva')

  useEffect(() => {
    async function fetchEmpleados() {
      const { data, error } = await supabase
        .schema('business')
        .from('ibm_hr')
        .select('*')

      if (error) {
        setErrorBd(error.message)
        console.error("Error de Supabase:", error)
      } else {
        setEmpleados(data)
      }
    }

    fetchEmpleados()
  }, [])

  // Revisamos si la vista actual corresponde a la raíz de uno de nuestros 13 módulos
  const activeModule = navigationConfig.find(mod => mod.id === vistaActual);

  return (
    <div className="flex h-screen bg-gray-50 overflow-hidden text-gray-800">
      <Sidebar vistaActual={vistaActual} setVistaActual={setVistaActual} />

      <main className="flex-1 overflow-y-auto p-10">
        {errorBd ? (
          <div className="bg-red-900 text-red-200 p-4 rounded-lg mt-4 text-sm font-mono shadow-md max-w-7xl mx-auto">
            <strong>🚨 Error de Conexión:</strong> {errorBd}
          </div>
        ) : (
          <div className="h-full">
            {/* Si estamos en la raíz del módulo, mostramos la Landing Section de ese módulo */}
            {activeModule ? (
              <SectionLanding module={activeModule} onNavigate={setVistaActual} />
            ) : (
              /* Si estamos dentro de un sub-item, mostramos su gráfico correspondiente */
              <div className="max-w-7xl mx-auto">
                <header className="mb-6 border-b border-gray-200 pb-4">
                  <div className="flex items-center gap-3">
                    <h1 className="text-2xl font-bold text-gray-800 tracking-tight">GDH Analytics</h1>
                  </div>
                </header>

                {/* Vistas Específicas */}
                {vistaActual === 'vision_general' && <Overview data={empleados} />}
                {vistaActual === 'demografia' && <Demographics />} 
                {vistaActual === 'org_posiciones' && <OrgStructure setVistaActual={setVistaActual} />} 
                {vistaActual === 'org_integral' && <OrganigramaIntegral />}
                {vistaActual === 'compensaciones' && <Compensaciones data={empleados} />}
                {vistaActual === 'auditoria' && <EmployeeTable data={empleados} />}

                {/* Placeholder Dinámico si la vista aún no está construida */}
                {![
                  'vision_general', 'demografia', 'org_posiciones', 'org_integral', 'compensaciones', 'auditoria'
                ].includes(vistaActual) && (
                  <div className="flex flex-col items-center justify-center p-24 bg-white shadow-sm border border-gray-100 rounded-2xl mt-8">
                    <div className="w-16 h-16 bg-blue-50 text-blue-500 rounded-full flex flex-col items-center justify-center mb-6">
                       <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" /></svg>
                    </div>
                    <h3 className="text-xl font-bold text-gray-800 mb-2">Desarrollo en Progreso 🚀</h3>
                    <p className="text-gray-500">Estamos conectando los flujos de datos para esta perspectiva de análisis.</p>
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