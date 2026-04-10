import React from 'react';
import * as Icons from 'lucide-react';

const tagColors = {
  DESC: 'bg-slate-100 text-slate-600',
  PRED: 'bg-emerald-50 text-emerald-600',
  ML: 'bg-emerald-50 text-emerald-600',
  IA: 'bg-emerald-50 text-emerald-600',
  NLP: 'bg-emerald-50 text-emerald-600',
  OPT: 'bg-emerald-50 text-emerald-600',
  XAI: 'bg-emerald-50 text-emerald-600'
};

export default function SectionLanding({ module, onNavigate }) {
  if (!module) return null;

  return (
    <div className="animate-fade-in max-w-7xl mx-auto">
      <div className="mb-10 flex flex-col gap-1">
        <h1 className="text-3xl font-extrabold text-slate-800 tracking-tight capitalize">
          {module.title.toLowerCase()}
        </h1>
        <p className="text-base text-slate-500 mt-2">{module.description}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {module.subItems?.map(item => {
          const IconComponent = Icons[item.icon] || Icons.Folder; 
          
          return (
            <div 
              key={item.id} 
              className="bg-white rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow duration-200 p-6 cursor-pointer flex flex-col h-full group"
              onClick={() => onNavigate(item.id)}
            >
              <div>
                <div className="p-2.5 bg-blue-50 text-blue-600 rounded-lg inline-flex mb-4 group-hover:scale-110 transition-transform">
                  <IconComponent size={24} />
                </div>
              </div>
              <h3 className="text-lg font-semibold text-slate-800 mb-3">{item.title}</h3>
              <p className="text-sm text-slate-500 leading-relaxed flex-1">{item.description}</p>
              
              <div className="mt-8 flex items-center justify-between pt-5 border-t border-slate-50">
                <span className="text-sm font-semibold text-blue-600 hover:text-blue-700">Explorar &rarr;</span>
                <div className="flex gap-2 flex-wrap justify-end">
                  {item.tags?.map(tag => (
                    <span 
                      key={tag} 
                      className={`text-xs font-medium px-2.5 py-0.5 rounded-full ${tagColors[tag] || 'bg-slate-100 text-slate-600'}`}
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
