import React from "react";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import HoverBorderCard from "../ui/HoverBorderCard";

const data = [
  { time: '10:00', load: 40, latency: 240 },
  { time: '11:00', load: 30, latency: 138 },
  { time: '12:00', load: 20, latency: 980 },
  { time: '13:00', load: 27, latency: 390 },
  { time: '14:00', load: 18, latency: 480 },
  { time: '15:00', load: 23, latency: 380 },
  { time: '16:00', load: 34, latency: 430 },
];

const HealthPulse: React.FC = () => {
  return (
    <HoverBorderCard className="glass rounded-[2rem] p-10 h-full flex flex-col gap-10 relative overflow-hidden group">
       {/* High-tech accent lines */}
      <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-cyan-500/20 to-transparent" />
      
      <div className="flex items-center justify-between relative z-10">
        <h2 className="text-2xl font-black tracking-tightest text-white/95 uppercase tracking-widest flex items-center gap-3">
          <div className="relative">
            <div className="w-3 h-3 rounded-full bg-cyan-400" />
            <div className="absolute inset-0 w-3 h-3 rounded-full bg-cyan-400 animate-ping opacity-40" />
          </div>
          Health Pulse
        </h2>
        <div className="flex gap-6 text-[10px] font-black text-zinc-400 uppercase tracking-[0.3em]">
          <span className="flex items-center gap-2">
            <div className="relative flex h-1.5 w-1.5">
              <div className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></div>
              <div className="relative inline-flex rounded-full h-1.5 w-1.5 bg-cyan-500 shadow-[0_0_8px_rgba(34,211,238,0.5)]"></div>
            </div> Realtime Load
          </span>
          <span className="flex items-center gap-2">
            <div className="w-1.5 h-1.5 rounded-full bg-purple-500 shadow-[0_0_8px_rgba(168,85,247,0.5)]" /> Latency MS
          </span>
        </div>
      </div>

      <div className="flex-1 min-h-[220px] w-full relative z-10">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="colorLoad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#22d3ee" stopOpacity={0.4}/>
                <stop offset="95%" stopColor="#22d3ee" stopOpacity={0}/>
              </linearGradient>
              <linearGradient id="colorLatency" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#a855f7" stopOpacity={0.4}/>
                <stop offset="95%" stopColor="#a855f7" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="4 4" vertical={false} stroke="rgba(255,255,255,0.03)" />
            <XAxis 
              dataKey="time" 
              axisLine={false} 
              tickLine={false} 
              tick={{ fill: '#71717a', fontSize: 11, fontWeight: 700 }} 
            />
            <YAxis 
              axisLine={false} 
              tickLine={false} 
              tick={{ fill: '#71717a', fontSize: 11, fontWeight: 700 }} 
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: 'rgba(9, 9, 11, 0.95)', 
                border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: '16px',
                backdropFilter: 'blur(12px)',
                boxShadow: '0 20px 50px rgba(0,0,0,0.5)'
              }}
              itemStyle={{ fontSize: '13px', fontWeight: 800, textTransform: 'uppercase' }}
            />
            <Area 
              type="stepAfter" 
              dataKey="load" 
              stroke="#22d3ee" 
              fillOpacity={1} 
              fill="url(#colorLoad)" 
              strokeWidth={3}
            />
            <Area 
              type="stepAfter" 
              dataKey="latency" 
              stroke="#a855f7" 
              fillOpacity={1} 
              fill="url(#colorLatency)" 
              strokeWidth={3}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-3 gap-8 pt-8 border-t border-white/5 relative z-10">
        <div className="flex flex-col gap-2">
          <span className="text-[10px] text-zinc-600 uppercase font-black tracking-[0.3em]">Core Models</span>
          <span className="text-base font-mono font-black text-cyan-400 tracking-tighter">ONLINE [3]</span>
        </div>
        <div className="flex flex-col gap-2">
          <span className="text-[10px] text-zinc-600 uppercase font-black tracking-[0.3em]">Processing</span>
          <span className="text-base font-mono font-black text-white/95 tracking-tighter">1.24k REQ</span>
        </div>
        <div className="flex flex-col gap-2">
          <span className="text-[10px] text-zinc-600 uppercase font-black tracking-[0.3em]">Session Uptime</span>
          <span className="text-base font-mono font-black text-white/95 tracking-tighter">99.98%</span>
        </div>
      </div>
    </HoverBorderCard>
  );
};

export default HealthPulse;
