import React, { useState } from 'react';
import * as Icons from 'lucide-react';
import { Grip, UserCircle, ChevronDown, ChevronRight } from 'lucide-react';
import { navigationConfig } from '../../config/navigation';

export default function Sidebar({ vistaActual, setVistaActual }) {
  const [isExpanded, setIsExpanded] = useState(true);
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

  const handleSubItemClick = (subItemId) => {
    setVistaActual(subItemId);
  };

  return (
    <aside 
      className={`flex flex-col h-screen bg-white border-r border-slate-200 transition-all duration-300 z-20 shrink-0 ${
        isExpanded ? 'w-[220px]' : 'w-[72px]'
      }`}
    >
      <div className="h-20 flex items-center px-4 shrink-0">
        <button 
          onClick={() => setIsExpanded(!isExpanded)}
          className="p-2 rounded-xl hover:bg-slate-50 transition-colors flex items-center justify-center text-slate-500 focus:outline-none shrink-0"
        >
          <Grip size={22} />
        </button>
        {isExpanded && (
          <div className="ml-3 flex flex-col justify-center overflow-hidden">
             <span className="font-bold text-slate-800 tracking-tight text-base leading-tight">GDH Analytics</span>
             <span className="text-[10px] uppercase font-bold text-blue-600 tracking-wider">Enterprise</span>
          </div>
        )}
      </div>

      <nav className="flex-1 overflow-y-auto px-3 py-2 space-y-1 [scrollbar-width:none] [-ms-overflow-style:none] [&::-webkit-scrollbar]:hidden">
        {navigationConfig.map((item) => {
          const IconComponent = Icons[item.icon] || Icons.Folder;
          
          const isModuleActive = vistaActual === item.id || item.subItems?.some(sub => sub.id === vistaActual);
          const isModuleOpen = openModules[item.id];

          return (
            <div key={item.id} className="">
              <button 
                onClick={() => handleModuleClick(item.id)}
                className={`w-full flex items-center justify-between px-3 py-2 rounded-xl cursor-pointer transition-all ${
                  isModuleActive 
                    ? 'bg-blue-50/80 text-blue-700 font-semibold' 
                    : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                }`}
              >
                <div className="flex items-center gap-3 overflow-hidden pr-2">
                  <div className={`shrink-0 flex items-center justify-center w-6 h-6`}>
                    <IconComponent size={20} strokeWidth={isModuleActive ? 2.5 : 2} className="text-current" />
                  </div>
                  {isExpanded && (
                    <span className={`text-xs uppercase tracking-wider font-bold text-left leading-snug whitespace-normal break-words ${isModuleActive ? 'text-blue-700' : 'text-slate-400'}`}>
                      {item.title}
                    </span>
                  )}
                </div>
                {isExpanded && item.subItems && item.subItems.length > 0 && (
                  <div className="shrink-0 ml-1">
                    {isModuleOpen ? <ChevronDown size={16} className="text-current opacity-70" /> : <ChevronRight size={16} className="text-current opacity-70" />}
                  </div>
                )}
              </button>
              
              {isExpanded && isModuleOpen && item.subItems && (
                <div className="flex flex-col mt-1 mb-2 ml-1 pl-6 space-y-1">
                  {item.subItems.map(subItem => {
                    const isSubActive = vistaActual === subItem.id;
                    return (
                      <button
                        key={subItem.id}
                        onClick={() => handleSubItemClick(subItem.id)}
                        className={`w-full text-left px-3 py-2 text-sm leading-snug whitespace-normal break-words transition-colors rounded-xl capitalize ${
                          isSubActive
                            ? 'text-blue-700 font-semibold bg-blue-50/80' 
                            : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50 font-medium'
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
        <div className="pt-4 mt-6 border-t border-slate-100">
          {isExpanded && (
            <div className="px-3 mb-2">
              <span className="text-xs uppercase tracking-wider font-bold text-slate-400">
                ADMINISTRACIÓN
              </span>
            </div>
          )}
          
          <div className="flex flex-col space-y-1">
            <button 
              onClick={() => setVistaActual('roles_permisos')}
              className={`w-full flex items-center justify-between px-3 py-2 rounded-xl cursor-pointer transition-all ${
                vistaActual === 'roles_permisos'
                  ? 'bg-blue-50/80 text-blue-700 font-semibold'
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900 font-medium'
              }`}
            >
              <div className="flex items-center gap-3 overflow-hidden pr-2">
                <div className={`shrink-0 flex items-center justify-center w-6 h-6`}>
                  <Icons.Lock size={20} strokeWidth={vistaActual === 'roles_permisos' ? 2.5 : 2} className="text-current" />
                </div>
                {isExpanded && (
                  <span className={`text-sm font-medium text-left leading-snug whitespace-normal break-words capitalize`}>
                    Roles & Permisos (RLS)
                  </span>
                )}
              </div>
            </button>

            <button 
              onClick={() => setVistaActual('conexiones_etl')}
              className={`w-full flex items-center justify-between px-3 py-2 rounded-xl cursor-pointer transition-all ${
                vistaActual === 'conexiones_etl'
                  ? 'bg-blue-50/80 text-blue-700 font-semibold'
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900 font-medium'
              }`}
            >
              <div className="flex items-center gap-3 overflow-hidden pr-2">
                <div className={`shrink-0 flex items-center justify-center w-6 h-6`}>
                  <Icons.Plug size={20} strokeWidth={vistaActual === 'conexiones_etl' ? 2.5 : 2} className="text-current" />
                </div>
                {isExpanded && (
                  <span className={`text-sm font-medium text-left leading-snug whitespace-normal break-words capitalize`}>
                    Conexiones ETL & Fuentes
                  </span>
                )}
              </div>
            </button>
          </div>
        </div>
      </nav>

      <div className="mt-auto border-t border-slate-200 p-4 flex items-center shrink-0 bg-slate-50">
        <div className="shrink-0 flex items-center justify-center w-10 h-10 bg-blue-600 shadow-sm text-white rounded-full">
          <UserCircle size={24} />
        </div>
        {isExpanded && (
          <div className="ml-3 flex flex-col whitespace-normal">
            <span className="font-semibold text-slate-800 text-sm">JESUS VILLEGAS</span>
            <span className="text-[10px] text-slate-500 font-bold uppercase tracking-widest mt-0.5">Data y BI</span>
          </div>
        )}
      </div>
    </aside>
  );
}
