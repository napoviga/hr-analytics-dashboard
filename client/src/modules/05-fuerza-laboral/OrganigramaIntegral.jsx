import React from 'react';
import { Users, Building2, CircleDollarSign, Briefcase, TrendingDown } from 'lucide-react';

export default function OrganigramaIntegral() {
  return (
    <div className="p-2 min-h-screen">
      
      {/* Panel Superior: KPIs */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-slate-800 mb-6">Organigrama Integral</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex items-center gap-4">
            <div className="bg-blue-100 p-3 rounded-lg text-blue-600"><Users size={24} /></div>
            <div>
              <p className="text-sm text-slate-500 font-medium">Total Empleados</p>
              <p className="text-2xl font-bold text-slate-800">1,470</p>
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex items-center gap-4">
            <div className="bg-indigo-100 p-3 rounded-lg text-indigo-600"><Building2 size={24} /></div>
            <div>
              <p className="text-sm text-slate-500 font-medium">Departamentos Activos</p>
              <p className="text-2xl font-bold text-slate-800">3</p>
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex items-center gap-4">
            <div className="bg-emerald-100 p-3 rounded-lg text-emerald-600"><CircleDollarSign size={24} /></div>
            <div>
              <p className="text-sm text-slate-500 font-medium">Costo Salarial Promedio</p>
              <p className="text-2xl font-bold text-slate-800">$6,500</p>
            </div>
          </div>

        </div>
      </div>

      {/* Área Central: Organigrama */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-12 flex flex-col items-center overflow-x-auto">
        
        {/* Nodo Principal: Dirección General */}
        <div className="bg-slate-800 text-white p-5 rounded-xl shadow-lg w-72 text-center relative z-10">
          <h3 className="font-bold text-lg tracking-wide">Dirección General</h3>
          <p className="text-slate-300 text-sm mt-1">Nivel Ejecutivo</p>
          {/* Línea vertical hacia abajo */}
          <div className="absolute w-0.5 h-12 bg-slate-300 left-1/2 -translate-x-1/2 -bottom-12"></div>
        </div>

        {/* Línea Horizontal conectora */}
        <div className="w-full max-w-3xl h-0.5 bg-slate-300 relative mt-12 mb-8">
            {/* Líneas verticales hacia los nodos hijos */}
            <div className="absolute w-0.5 h-8 bg-slate-300 left-0 top-0"></div>
            <div className="absolute w-0.5 h-8 bg-slate-300 left-1/2 -translate-x-1/2 top-0"></div>
            <div className="absolute w-0.5 h-8 bg-slate-300 right-0 top-0"></div>
        </div>

        {/* Nodos de Departamentos */}
        <div className="w-full max-w-4xl flex justify-between gap-6">
          
          {/* Sales */}
          <div className="bg-slate-50 border border-slate-200 p-5 rounded-xl w-72 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex justify-between items-start mb-4">
              <div className="bg-blue-600 text-white p-2.5 rounded-lg"><Briefcase size={20} /></div>
              <span className="bg-red-100 text-red-700 text-xs font-bold px-2.5 py-1 rounded-full flex items-center gap-1">
                <TrendingDown size={14}/> 20.6% ATR
              </span>
            </div>
            <h4 className="font-bold text-slate-800 text-lg">Ventas (Sales)</h4>
            <p className="text-sm text-slate-500 mt-2 font-medium flex items-center gap-2">
              <Users size={16} className="text-slate-400"/> 446 Empleados
            </p>
          </div>

          {/* R&D */}
          <div className="bg-slate-50 border border-slate-200 p-5 rounded-xl w-72 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex justify-between items-start mb-4">
              <div className="bg-blue-600 text-white p-2.5 rounded-lg"><Building2 size={20} /></div>
              <span className="bg-yellow-100 text-yellow-700 text-xs font-bold px-2.5 py-1 rounded-full flex items-center gap-1">
                <TrendingDown size={14}/> 13.8% ATR
              </span>
            </div>
            <h4 className="font-bold text-slate-800 text-lg">Investigación y Des.</h4>
            <p className="text-sm text-slate-500 mt-2 font-medium flex items-center gap-2">
              <Users size={16} className="text-slate-400"/> 961 Empleados
            </p>
          </div>

          {/* HR */}
          <div className="bg-slate-50 border border-slate-200 p-5 rounded-xl w-72 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex justify-between items-start mb-4">
              <div className="bg-blue-600 text-white p-2.5 rounded-lg"><Users size={20} /></div>
              <span className="bg-green-100 text-green-700 text-xs font-bold px-2.5 py-1 rounded-full flex items-center gap-1">
                <TrendingDown size={14}/> 19.0% ATR
              </span>
            </div>
            <h4 className="font-bold text-slate-800 text-lg">Recursos Humanos</h4>
            <p className="text-sm text-slate-500 mt-2 font-medium flex items-center gap-2">
              <Users size={16} className="text-slate-400"/> 63 Empleados
            </p>
          </div>

        </div>
      </div>
    </div>
  );
}
