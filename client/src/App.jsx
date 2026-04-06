import { useState, useEffect } from 'react'
import { supabase } from './lib/supabaseClient'
import Sidebar from './components/Sidebar'
import EmployeeTable from './components/EmployeeTable'
import Overview from './components/Overview'
import Compensaciones from './components/Compensations'
import OrgStructure from './components/OrgStructure'
import OrganigramaIntegral from './components/OrganigramaIntegral'

function App() {
  const [empleados, setEmpleados] = useState([])
  const [errorBd, setErrorBd] = useState(null)
  const [vistaActual, setVistaActual] = useState('vision_general')

  useEffect(() => {
    async function fetchEmpleados() {
      // Intentamos traer los datos
      const { data, error } = await supabase
        .schema('business')
        .from('ibm_hr')
        .select('*')

      // Si hay un error, lo guardamos para verlo en pantalla
      if (error) {
        setErrorBd(error.message)
        console.error("Error de Supabase:", error)
      } else {
        setEmpleados(data)
      }
    }

    fetchEmpleados()
  }, [])

  return (
    <div className="flex h-screen bg-gray-50 overflow-hidden">
      <Sidebar vistaActual={vistaActual} setVistaActual={setVistaActual} />

      <main className="flex-1 overflow-y-auto p-8">
        <div className="max-w-7xl mx-auto">
          <header className="mb-8 border-b border-gray-200 pb-4">
            <h1 className="text-3xl font-semibold text-gray-800 mb-8">HR Analytics</h1>
          </header>
        
        {errorBd ? (
          <div className="bg-red-900 text-red-200 p-4 rounded-lg mt-4 text-sm font-mono shadow-md">
            <strong>🚨 Error de Conexión:</strong> {errorBd}
          </div>
        ) : (
          <div className="mt-8">
            {/* Vistas Activas */}
            {vistaActual === 'vision_general' && <Overview data={empleados} />}
            {vistaActual === 'estructura' && <OrgStructure setVistaActual={setVistaActual} />} 
            {vistaActual === 'org_integral' && <OrganigramaIntegral />}
            {vistaActual === 'compensaciones' && <Compensaciones data={empleados} />}
            {vistaActual === 'auditoria' && <EmployeeTable data={empleados} />}

            {/* Placeholder para los módulos que construiremos después */}
            {['fuga_talento', 'desempeno', 'turnos', 'reclutamiento', 'capacitacion', 'clima', 'diversidad', 'org_dotacion', 'org_costos'].includes(vistaActual) && (
              <div className="flex flex-col items-center justify-center p-20 text-gray-400 border-2 border-dashed border-gray-300 rounded-xl mt-10">
                <h3 className="text-2xl font-bold text-gray-500 mb-2">Módulo en Construcción 🚀</h3>
                <p>Pronto conectaremos los datos para esta sección.</p>
              </div>
            )}
          </div>
        )}
        </div>
      </main>
    </div>
  )
}

export default App