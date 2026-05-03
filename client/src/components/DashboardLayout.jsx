import React from 'react';

export function DashboardLayout({ title, description, children, kpiCards }) {
  return (
    <div className="flex flex-col h-full bg-slate-50/50 pb-12">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-slate-800">{title}</h1>
        {description && <p className="text-sm text-slate-500 mt-1">{description}</p>}
      </div>
      
      {/* KPI Cards Area */}
      {kpiCards && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          {kpiCards}
        </div>
      )}
      
      {/* Main Content Area */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {children}
      </div>
    </div>
  );
}

export function KpiCard({ title, value, subtitle, trend, trendPositive }) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
      <h3 className="text-sm font-medium text-slate-500 mb-1">{title}</h3>
      <div className="flex items-baseline gap-2">
        <span className="text-2xl font-semibold text-slate-800">{value}</span>
        {trend && (
          <span className={`text-xs font-medium ${trendPositive ? 'text-emerald-600 bg-emerald-50' : 'text-rose-600 bg-rose-50'} px-2 py-0.5 rounded-full`}>
            {trend}
          </span>
        )}
      </div>
      {subtitle && <p className="text-xs text-slate-400 mt-2">{subtitle}</p>}
    </div>
  );
}

export function ChartCard({ title, subtitle, children, fullWidth = false }) {
  return (
    <div className={`bg-white rounded-xl border border-slate-200 p-5 shadow-sm ${fullWidth ? 'lg:col-span-2' : ''}`}>
      <div className="mb-4">
        <h3 className="text-base font-semibold text-slate-800">{title}</h3>
        {subtitle && <p className="text-sm text-slate-500">{subtitle}</p>}
      </div>
      <div className="h-[320px] w-full">
        {children}
      </div>
    </div>
  );
}
