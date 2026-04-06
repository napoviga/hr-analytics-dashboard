export default function EmployeeTable({ data }) {
  return (
    <div className="mt-8 overflow-x-auto rounded-lg shadow-2xl border border-gray-700 bg-gray-900">
      <table className="w-full text-left text-sm text-gray-300">
        <thead className="bg-gray-800 text-white uppercase text-xs font-semibold tracking-wider border-b border-gray-700">
          <tr>
            <th className="px-6 py-4">ID</th>
            <th className="px-6 py-4">Edad</th>
            <th className="px-6 py-4">Departamento</th>
            <th className="px-6 py-4">Rol</th>
            <th className="px-6 py-4 text-center">Riesgo Deserción</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-700">
          {data.map((emp) => (
            <tr key={emp.employeenumber} className="hover:bg-gray-800/80 transition-colors">
              <td className="px-6 py-4 font-medium text-gray-100">{emp.employeenumber}</td>
              <td className="px-6 py-4">{emp.age}</td>
              <td className="px-6 py-4">{emp.department}</td>
              <td className="px-6 py-4">{emp.jobrole}</td>
              <td className="px-6 py-4 text-center">
                <span 
                  className={`inline-block px-3 py-1 rounded-full text-xs font-bold shadow-sm ${
                    emp.attrition === 'Yes' 
                      ? 'bg-red-100 text-red-800 border border-red-200' 
                      : 'bg-green-100 text-green-800 border border-green-200'
                  }`}
                >
                  {emp.attrition}
                </span>
              </td>
            </tr>
          ))}
          {data.length === 0 && (
            <tr>
              <td colSpan="5" className="px-6 py-8 text-center text-gray-400 italic">
                Cargando o sin datos en la base...
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
