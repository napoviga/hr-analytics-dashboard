import React from 'react';
import { Network, Users, CircleDollarSign, ArrowRight } from 'lucide-react';

export default function OrgStructure({ setVistaActual }) {
  return (
    <div className="max-w-5xl">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Card 1: Org Integral */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 flex flex-col hover:shadow-md transition-shadow">
          <div className="w-12 h-12 bg-blue-50 text-blue-600 rounded-lg flex items-center justify-center mb-6">
            <Network size={28} />
          </div>
          <h3 className="text-xl font-semibold text-gray-800 mb-3">Organigrama Integral</h3>
          <p className="text-gray-500 mb-8 flex-1">
            Visión completa de la jerarquía, roles y departamentos de la compañía.
          </p>
          <button 
            onClick={() => setVistaActual('org_integral')}
            className="flex items-center text-blue-600 font-medium hover:text-blue-700 transition-colors mt-auto"
          >
            Explorar <ArrowRight size={18} className="ml-2" />
          </button>
        </div>

        {/* Card 2: Dotación */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 flex flex-col hover:shadow-md transition-shadow">
          <div className="w-12 h-12 bg-emerald-50 text-emerald-600 rounded-lg flex items-center justify-center mb-6">
            <Users size={28} />
          </div>
          <h3 className="text-xl font-semibold text-gray-800 mb-3">Organigrama de Dotación</h3>
          <p className="text-gray-500 mb-8 flex-1">
            Enfoque en el conteo de personas (Headcount), vacantes y capacidad operativa por área.
          </p>
          <button 
            onClick={() => setVistaActual('org_dotacion')}
            className="flex items-center text-emerald-600 font-medium hover:text-emerald-700 transition-colors mt-auto"
          >
            Explorar <ArrowRight size={18} className="ml-2" />
          </button>
        </div>

        {/* Card 3: Costos */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 flex flex-col hover:shadow-md transition-shadow">
          <div className="w-12 h-12 bg-purple-50 text-purple-600 rounded-lg flex items-center justify-center mb-6">
            <CircleDollarSign size={28} />
          </div>
          <h3 className="text-xl font-semibold text-gray-800 mb-3">Organigrama de Costos</h3>
          <p className="text-gray-500 mb-8 flex-1">
            Análisis del presupuesto salarial, beneficios y eficiencia financiera por nivel jerárquico.
          </p>
          <button 
            onClick={() => setVistaActual('org_costos')}
            className="flex items-center text-purple-600 font-medium hover:text-purple-700 transition-colors mt-auto"
          >
            Explorar <ArrowRight size={18} className="ml-2" />
          </button>
        </div>
      </div>
    </div>
  );
}