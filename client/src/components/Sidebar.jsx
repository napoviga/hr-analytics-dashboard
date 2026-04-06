import React, { useState } from 'react';
import { 
  LayoutDashboard, 
  Network, 
  CircleDollarSign, 
  Database,
  UserMinus, 
  Target, 
  Clock, 
  Users, 
  BookOpen, 
  Smile, 
  Globe,
  Grip,
  UserCircle,
  ChevronDown,
  ChevronRight
} from 'lucide-react';

export default function Sidebar({ vistaActual, setVistaActual }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [isOrgExpanded, setIsOrgExpanded] = useState(false);

  // Arreglo con todos los módulos planificados
  const menuItems = [
    { id: 'vision_general', label: 'Visión General', icon: LayoutDashboard },
    { id: 'estructura', label: 'Estructura Org.', icon: Network },
    { id: 'compensaciones', label: 'Compensaciones', icon: CircleDollarSign },
    { id: 'fuga_talento', label: 'Fuga de Talento', icon: UserMinus },
    { id: 'desempeno', label: 'Desempeño', icon: Target },
    { id: 'turnos', label: 'Gestión de Turnos', icon: Clock },
    { id: 'reclutamiento', label: 'Reclutamiento', icon: Users },
    { id: 'capacitacion', label: 'Capacitación', icon: BookOpen },
    { id: 'clima', label: 'Clima Laboral', icon: Smile },
    { id: 'diversidad', label: 'Diversidad (DEI)', icon: Globe },
    { id: 'auditoria', label: 'Auditoría de Datos', icon: Database }
  ];

  return (
    <aside 
      className={`flex flex-col h-screen bg-white border-r border-gray-200 transition-all duration-300 z-20 ${
        isExpanded ? 'w-64' : 'w-20'
      }`}
    >
      {/* Cabecera (Top) */}
      <div className="h-16 flex items-center px-4 border-b border-gray-100">
        <button 
          onClick={() => setIsExpanded(!isExpanded)}
          className="p-2 rounded-md hover:bg-gray-100 transition-colors flex items-center justify-center text-gray-600 focus:outline-none flex-shrink-0"
        >
          <Grip size={24} />
        </button>
        {isExpanded && (
          <span className="ml-4 font-semibold text-gray-800 whitespace-nowrap overflow-hidden">
            GDH Analytics
          </span>
        )}
      </div>

      {/* Menú (Centro) */}
      <nav className="flex-1 overflow-y-auto py-4 space-y-1">
        {menuItems.map((item) => {
          const IconComponent = item.icon;
          const isActive = vistaActual === item.id;
          
          if (item.id === 'estructura') {
            const isEstActive = vistaActual.startsWith('org_') || vistaActual === 'estructura';
            return (
              <div key={item.id}>
                <button 
                  onClick={() => {
                    setVistaActual('estructura');
                    if (!isExpanded) {
                      setIsExpanded(true);
                      setIsOrgExpanded(true);
                    } else {
                      setIsOrgExpanded(!isOrgExpanded);
                    }
                  }}
                  className={`w-full flex items-center justify-between px-4 py-3 cursor-pointer transition-colors whitespace-nowrap overflow-hidden ${
                    isEstActive 
                      ? 'bg-blue-50 text-blue-700 border-l-4 border-blue-600' 
                      : 'text-gray-600 hover:bg-gray-100 border-l-4 border-transparent'
                  }`}
                >
                  <div className="flex items-center gap-4">
                    <div className="shrink-0 flex items-center justify-center w-8">
                      <IconComponent size={20} className={isEstActive ? 'text-blue-600' : 'text-gray-500'} />
                    </div>
                    {isExpanded && (
                      <span className="font-medium text-sm">
                        {item.label}
                      </span>
                    )}
                  </div>
                  {isExpanded && (
                    isOrgExpanded ? <ChevronDown size={16} className="text-gray-500" /> : <ChevronRight size={16} className="text-gray-400" />
                  )}
                </button>
                
                {/* Submenús */}
                {isExpanded && isOrgExpanded && (
                  <div className="flex flex-col mt-1 mb-1 space-y-1">
                    {[
                      { id: 'org_integral', label: 'Organigrama Integral' },
                      { id: 'org_dotacion', label: 'Organigrama de Dotación' },
                      { id: 'org_costos', label: 'Organigrama de Costos' },
                    ].map(subItem => (
                      <button
                        key={subItem.id}
                        onClick={() => setVistaActual(subItem.id)}
                        className={`w-full text-left pl-12 pr-4 py-2 text-sm transition-colors whitespace-nowrap overflow-hidden ${
                          vistaActual === subItem.id 
                            ? 'text-blue-700 font-medium' 
                            : 'text-gray-500 hover:text-blue-600 hover:bg-gray-50'
                        }`}
                      >
                        {subItem.label}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            );
          }

          return (
            <button 
              key={item.id} 
              onClick={() => setVistaActual(item.id)}
              className={`w-full flex items-center gap-4 px-4 py-3 cursor-pointer transition-colors whitespace-nowrap overflow-hidden ${
                isActive 
                  ? 'bg-blue-50 text-blue-700 border-l-4 border-blue-600' 
                  : 'text-gray-600 hover:bg-gray-100 border-l-4 border-transparent'
              }`}
            >
              <div className="shrink-0 flex items-center justify-center w-8">
                <IconComponent size={20} className={isActive ? 'text-blue-600' : 'text-gray-500'} />
              </div>
              {isExpanded && (
                <span className="font-medium text-sm">
                  {item.label}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Perfil (Bottom) */}
      <div className="mt-auto border-t border-gray-200 p-4 flex items-center overflow-hidden">
        <div className="flex-shrink-0 flex items-center justify-center w-10 h-10 bg-gray-800 text-white rounded-md">
          {/* Avatar genérico */}
          <UserCircle size={24} />
        </div>
        {isExpanded && (
          <div className="ml-3 flex flex-col whitespace-nowrap overflow-hidden">
            <span className="font-bold text-gray-900 text-sm">Ricardo Sandoval</span>
            <span className="text-xs text-gray-500">CHRO - Global Ops</span>
          </div>
        )}
      </div>
    </aside>
  );
}
