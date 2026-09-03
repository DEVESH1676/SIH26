import React from 'react';
import HoverBorderCard from '../ui/HoverBorderCard';

const SystemReadiness: React.FC = () => {
  return (
    <HoverBorderCard className="h-full w-full rounded-2xl flex flex-col items-center justify-center glass relative overflow-hidden p-8">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(34,211,238,0.03),transparent_70%)]" />
      
      <div className="w-full max-w-2xl space-y-8 relative z-10">
        <div className="flex flex-col items-center gap-4 text-center">
          <div className="relative">
            <div className="w-16 h-16 rounded-2xl bg-cyan-500/5 border border-cyan-500/20 flex items-center justify-center text-cyan-400 shadow-2xl">
              <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div className="absolute -inset-4 bg-cyan-500/10 blur-xl rounded-full animate-pulse" />
          </div>
          <div className="space-y-1">
            <h3 className="text-xl font-black text-white/95 tracking-tight">System Readiness Report</h3>
            <p className="text-xs text-[#94a3b8] font-bold uppercase tracking-widest">Autonomous Core: Standby</p>
          </div>
        </div>

        {/* Mocked Readiness Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="glass p-5 rounded-xl border-white/5 space-y-4">
            <div className="flex justify-between items-center text-[10px] font-black uppercase tracking-widest text-[#94a3b8]">
                <span>Neural Path Integrity</span>
                <span className="text-emerald-400 text-xs">99.8%</span>
            </div>
            <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden">
                <div className="h-full w-[99.8%] bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.3)]" />
            </div>
          </div>
          <div className="glass p-5 rounded-xl border-white/5 space-y-4">
            <div className="flex justify-between items-center text-[10px] font-black uppercase tracking-widest text-[#94a3b8]">
                <span>KB Sync Latency</span>
                <span className="text-cyan-400 text-xs">14ms</span>
            </div>
            <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden">
                <div className="h-full w-[14%] bg-cyan-500 shadow-[0_0_10px_rgba(34,211,238,0.3)]" />
            </div>
          </div>
        </div>

        <div className="p-6 glass rounded-xl border-cyan-500/20 bg-cyan-500/[0.02] text-center">
          <p className="text-[10px] text-[#94a3b8] leading-relaxed font-bold uppercase tracking-[0.15em]">
            Awaiting telemetry input from <span className="text-white">Command Center</span> to initiate resolution synthesis.
          </p>
        </div>
      </div>
    </HoverBorderCard>
  );
};

export default SystemReadiness;
