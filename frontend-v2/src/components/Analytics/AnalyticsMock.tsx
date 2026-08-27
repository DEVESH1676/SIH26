import React from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import HoverBorderCard from "../ui/HoverBorderCard";

const categoryData = [
  { name: 'Network', count: 42, color: '#22d3ee' },
  { name: 'Security', count: 38, color: '#818cf8' },
  { name: 'Infra', count: 25, color: '#a855f7' },
  { name: 'Access', count: 18, color: '#f472b6' },
  { name: 'App', count: 12, color: '#fbbf24' },
];

const AnalyticsMock: React.FC = () => {
  return (
    <HoverBorderCard className="glass rounded-[2rem] p-10 h-full flex flex-col gap-12 relative overflow-hidden">
      {/* Decorative accent */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-purple-500/5 blur-3xl rounded-full" />
      
      <div className="flex items-center justify-between relative z-10">
        <h2 className="text-2xl font-black tracking-tightest text-white/90 uppercase tracking-widest">Analytics</h2>
        <div className="px-5 py-2 rounded-xl bg-white/5 border border-white/10 text-[10px] font-black text-cyan-400 uppercase tracking-[0.3em] shadow-inner">
          30D Operational Delta
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 relative z-10">
        <div className="p-8 rounded-3xl bg-white/[0.03] border border-white/10 shadow-2xl group hover:bg-white/[0.05] transition-all">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-1.5 h-4 bg-emerald-500 rounded-full shadow-[0_0_10px_rgba(16,185,129,0.5)]" />
            <span className="text-[11px] text-zinc-500 uppercase font-black tracking-[0.2em]">Resolution Efficacy</span>
          </div>
          <div className="flex items-end gap-4">
            <span className="text-5xl font-mono font-black text-white/95 leading-none">74%</span>
            <span className="text-xs text-emerald-400 font-black mb-1 bg-emerald-500/10 px-2 py-1 rounded-md">+12.4%</span>
          </div>
        </div>
        
        <div className="p-8 rounded-3xl bg-white/[0.03] border border-white/10 shadow-2xl group hover:bg-white/[0.05] transition-all">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-1.5 h-4 bg-cyan-500 rounded-full shadow-[0_0_10px_rgba(34,211,238,0.5)]" />
            <span className="text-[11px] text-zinc-500 uppercase font-black tracking-[0.2em]">Neural Confidence</span>
          </div>
          <div className="flex items-end gap-4">
            <span className="text-5xl font-mono font-black text-white/95 leading-none">86.2%</span>
            <span className="text-xs text-cyan-400 font-black mb-1 bg-cyan-500/10 px-2 py-1 rounded-md">+2.8%</span>
          </div>
        </div>
      </div>

      <div className="flex-1 min-h-[220px] relative z-10">
        <div className="flex items-center gap-3 mb-8">
           <span className="text-[11px] text-zinc-500 uppercase font-black tracking-[0.2em]">Distribution by Category</span>
           <div className="flex-1 h-px bg-white/5" />
        </div>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={categoryData} layout="vertical" margin={{ left: -10, right: 20 }}>
            <XAxis type="number" hide />
            <YAxis 
              dataKey="name" 
              type="category" 
              axisLine={false} 
              tickLine={false} 
              tick={{ fill: '#94a3b8', fontSize: 11, fontWeight: 700 }} 
              width={80}
            />
            <Tooltip 
              cursor={{ fill: 'rgba(255,255,255,0.03)' }}
              contentStyle={{ 
                backgroundColor: 'rgba(9, 9, 11, 0.95)', 
                border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: '16px',
                backdropFilter: 'blur(12px)',
                boxShadow: '0 20px 50px rgba(0,0,0,0.5)'
              }}
            />
            <Bar dataKey="count" radius={[0, 6, 6, 0]} barSize={16}>
              {categoryData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} fillOpacity={0.7} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="pt-4 border-t border-white/5 flex items-center justify-between text-xs relative z-10">
        <span className="text-zinc-500">Processing Node: <span className="text-zinc-300 font-mono">US-EAST-1</span></span>
        <span className="text-zinc-500">Latency: <span className="text-emerald-400 font-mono">14ms</span></span>
      </div>
    </HoverBorderCard>
  );
};

export default AnalyticsMock;
