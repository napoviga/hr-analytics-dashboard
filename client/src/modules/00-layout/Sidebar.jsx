import React, { useState } from 'react';
import * as Icons from 'lucide-react';
import { Grip, UserCircle, ChevronDown, ChevronRight } from 'lucide-react';
import { navigationConfig } from '../../config/navigation';

export default function Sidebar({ vistaActual, setVistaActual }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [openModules, setOpenModules] = useState({});

  const handleModuleClick = (moduleId) => {
    setVistaActual(moduleId);
    if (!isExpanded) {
      setIsExpanded(true);
      setOpenModules({ [moduleId]: true });
    } else {
      setOpenModules(prev => ({ ...prev, [moduleId]: !prev[moduleId] }));
    }
  };

  const handleSubItemClick = (subItemId, moduleId) => {
    setVistaActual(subItemId);
  };

  return (
    <aside 
      className={`flex flex-col h-screen bg-white border-r border-gray-200 transition-all duration-300 z-20 shrink-0 ${
        isExpanded ? 'w-80' : 'w-20'
      }`}
    >
      <div className="h-20 flex items-center px-4 border-b border-gray-100 shrink-0">
        <button 
          onClick={() => setIsExpanded(!isExpanded)}
          className="p-3 rounded-lg hover:bg-gray-100 transition-colors flex items-center justify-center text-gray-600 focus:outline-none shrink-0"
        >
          <Grip size={24} />
        </button>
        {isExpanded && (
          <div className="ml-4 flex flex-col justify-center overflow-hidden">
             <span className="font-bold text-gray-900 tracking-tight text-lg">GDH Analytics</span>
             <span className="text-[10px] uppercase font-bold text-blue-600 tracking-wider">Enterprise Edition</span>
          </div>
        )}
      </div>

      <nav className="flex-1 overflow-y-auto py-4 space-y-2">
        {navigationConfig.map((item) => {
          const IconComponent = Icons[item.icon] || Icons.Folder;
          
          const isModuleActive = vistaActual === item.id || item.subItems?.some(sub => sub.id === vistaActual);
          const isModuleOpen = openModules[item.id];

          return (
            <div key={item.id} className="px-3">
              <button 
                onClick={() => handleModuleClick(item.id)}
                className={`w-full flex items-center justify-between px-3 py-3 rounded-xl cursor-pointer transition-all ${
                  isModuleActive 
                    ? 'bg-blue-50 text-blue-700 shadow-sm border border-blue-100/50' 
                    : 'text-gray-600 hover:bg-gray-50 border border-transparent'
                }`}
              >
                <div className="flex items-center gap-3 overflow-hidden pr-2">
                  <div className={`shrink-0 flex items-center justify-center w-8 h-8 rounded-lg ${isModuleActive ? 'bg-white shadow-sm text-blue-600' : 'text-gray-500'}`}>
                    <IconComponent size={20} strokeWidth={isModuleActive ? 2.5 : 2} />
                  </div>
                  {isExpanded && (
                    <span className={`text-sm text-left leading-snug whitespace-normal break-words ${isModuleActive ? 'font-bold' : 'font-medium'}`}>
                      {item.title}
                    </span>
                  )}
                </div>
                {isExpanded && item.subItems && item.subItems.length > 0 && (
                  <div className="shrink-0 ml-1">
                    {isModuleOpen ? <ChevronDown size={18} className="text-gray-400" /> : <ChevronRight size={18} className="text-gray-400" />}
                  </div>
                )}
              </button>
              
              {isExpanded && isModuleOpen && item.subItems && (
                <div className="flex flex-col mt-2 mb-3 ml-[1.60rem] pl-4 border-l-2 border-gray-100 space-y-1">
                  {item.subItems.map(subItem => {
                    const isSubActive = vistaActual === subItem.id;
                    return (
                      <button
                        key={subItem.id}
                        onClick={() => handleSubItemClick(subItem.id, item.id)}
                        className={`w-full text-left px-3 py-2.5 text-sm leading-snug whitespace-normal break-words transition-colors rounded-lg ${
                          isSubActive
                            ? 'text-blue-700 font-bold bg-blue-50/50' 
                            : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50 font-medium'
                        }`}
                      >
                        {subItem.title}
                      </button>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}
        
        {/* Panel de Administración */}
        <div className="pt-4 mt-6 border-t border-gray-100 mx-3">
          {isExpanded && (
            <div className="px-3 mb-3">
              <span className="text-[11px] font-bold text-gray-400 uppercase tracking-wider">
                Administración
              </span>
            </div>
          )}
          
          <div className="space-y-1">
            <button 
              onClick={() => setVistaActual('roles_permisos')}
              className={`w-full flex items-center justify-between px-3 py-3 rounded-xl cursor-pointer transition-all ${
                vistaActual === 'roles_permisos'
                  ? 'bg-gray-100 text-gray-800 font-bold shadow-sm'
                  : 'text-gray-500 hover:bg-gray-50 border border-transparent'
              }`}
            >
              <div className="flex items-center gap-3 overflow-hidden pr-2">
                <div className={`shrink-0 flex items-center justify-center w-8 h-8 rounded-lg ${vistaActual === 'roles_permisos' ? 'text-gray-700' : 'text-gray-500'}`}>
                  <Icons.Lock size={20} strokeWidth={vistaActual === 'roles_permisos' ? 2.5 : 2} />
                </div>
                {isExpanded && (
                  <span className={`text-sm text-left leading-snug whitespace-normal break-words ${vistaActual === 'roles_permisos' ? 'font-bold' : 'font-medium'}`}>
                    Roles & Permisos (RLS)
                  </span>
                )}
              </div>
            </button>

            <button 
              onClick={() => setVistaActual('conexiones_etl')}
              className={`w-full flex items-center justify-between px-3 py-3 rounded-xl cursor-pointer transition-all ${
                vistaActual === 'conexiones_etl'
                  ? 'bg-gray-100 text-gray-800 font-bold shadow-sm'
                  : 'text-gray-500 hover:bg-gray-50 border border-transparent'
              }`}
            >
              <div className="flex items-center gap-3 overflow-hidden pr-2">
                <div className={`shrink-0 flex items-center justify-center w-8 h-8 rounded-lg ${vistaActual === 'conexiones_etl' ? 'text-gray-700' : 'text-gray-500'}`}>
                  <Icons.Plug size={20} strokeWidth={vistaActual === 'conexiones_etl' ? 2.5 : 2} />
                </div>
                {isExpanded && (
                  <span className={`text-sm text-left leading-snug whitespace-normal break-words ${vistaActual === 'conexiones_etl' ? 'font-bold' : 'font-medium'}`}>
                    Conexiones ETL & Fuentes
                  </span>
                )}
              </div>
            </button>
          </div>
        </div>
      </nav>

      <div className="mt-auto border-t border-gray-100 p-4 flex items-center shrink-0 bg-gray-50/50">
        <div className="shrink-0 flex items-center justify-center w-10 h-10 bg-gradient-to-tr from-blue-700 to-blue-500 shadow-sm text-white rounded-xl">
          <UserCircle size={24} />
        </div>
        {isExpanded && (
          <div className="ml-3 flex flex-col whitespace-normal">
            <span className="font-bold text-gray-900 text-sm">JESUS VILLEGAS</span>
            <span className="text-[11px] text-gray-500 font-bold uppercase tracking-wide mt-0.5">Especialista de Data y BI</span>
          </div>
        )}
      </div>
    </aside>
  );
}
