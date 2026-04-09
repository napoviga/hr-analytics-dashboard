import React from 'react';
import * as Icons from 'lucide-react';

const tagColors = {
  DESC: 'bg-blue-100 text-blue-700',
  PRED: 'bg-emerald-100 text-emerald-700',
  ML: 'bg-purple-100 text-purple-700',
  IA: 'bg-amber-100 text-amber-700',
  NLP: 'bg-pink-100 text-pink-700',
  OPT: 'bg-orange-100 text-orange-700',
  XAI: 'bg-indigo-100 text-indigo-700'
};

export default function SectionLanding({ module, onNavigate }) {
  if (!module) return null;

  return (
    <div className="animate-fade-in max-w-7xl mx-auto">
      <div className="mb-10">
        <h2 className="text-3xl font-bold text-gray-800">{module.title}</h2>
        <p className="text-gray-500 mt-3 text-lg max-w-3xl leading-relaxed">{module.description}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {module.subItems?.map(item => {
          const IconComponent = Icons[item.icon] || Icons.Folder; 
          
          return (
            <div 
              key={item.id} 
              className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-md hover:-translate-y-1 transition-all duration-200 cursor-pointer flex flex-col h-full group"
              onClick={() => onNavigate(item.id)}
            >
              <div className="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center mb-5 group-hover:scale-110 transition-transform">
                <IconComponent size={24} />
              </div>
              <h3 className="font-bold text-gray-800 mb-3 text-lg leading-tight">{item.title}</h3>
              <p className="text-gray-500 text-sm flex-1 leading-relaxed">{item.description}</p>
              
              <div className="mt-8 flex items-center justify-between pt-5 border-t border-gray-50">
                <span className="text-sm font-semibold text-blue-600 group-hover:underline">Explorar &rarr;</span>
                <div className="flex gap-2 flex-wrap justify-end">
                  {item.tags?.map(tag => (
                    <span 
                      key={tag} 
                      className={`text-xs font-bold px-2.5 py-1 rounded-full ${tagColors[tag] || 'bg-gray-100 text-gray-700'}`}
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
