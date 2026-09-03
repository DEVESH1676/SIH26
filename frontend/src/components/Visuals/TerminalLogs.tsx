import React, { useEffect, useRef } from 'react';
import { usePipeline } from '../../hooks/usePipeline';
import { Terminal } from 'lucide-react';
import HoverBorderCard from '../ui/HoverBorderCard';

const TerminalLogs: React.FC = () => {
  const { state } = usePipeline();
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [state.logs]);

  return (
    <HoverBorderCard className="flex flex-col h-full glass rounded-xl overflow-hidden font-mono shadow-2xl relative">
      <div className="flex items-center justify-between px-4 py-2 bg-white/5 border-b border-white/10 relative z-10">
        <div className="flex items-center gap-2">
          <Terminal className="w-4 h-4 text-emerald-400" />
          <span className="text-[10px] font-bold text-slate-300 uppercase tracking-widest">Autonomous Reasoning</span>
        </div>
        <div className="flex gap-1.5">
          <div className="w-2 h-2 rounded-full bg-red-500/20 border border-red-500/40" />
          <div className="w-2 h-2 rounded-full bg-yellow-500/20 border border-yellow-500/40" />
          <div className="w-2 h-2 rounded-full bg-emerald-500/20 border border-emerald-500/40" />
        </div>
      </div>
      
      <div 
        ref={scrollRef}
        className="flex-1 p-6 overflow-y-auto space-y-2 no-scrollbar scroll-smooth relative z-10"
        style={{ fontFamily: "'JetBrains Mono', 'Fira Code', monospace" }}
      >
        {state.logs.length === 0 ? (
          <div className="text-slate-400 text-[13px] font-bold uppercase tracking-widest italic px-2">Awaiting telemetry...</div>
        ) : (
          state.logs.map((log, index) => (
            <div key={index} className="flex gap-4 text-[13px] leading-relaxed group">
              <span className="text-emerald-500/40 shrink-0 select-none font-black opacity-40 group-hover:opacity-100 transition-opacity">
                {index.toString().padStart(3, '0')}
              </span>
              <span className="text-slate-100 font-medium whitespace-pre-wrap tracking-normal">
                {log}
              </span>
            </div>
          ))
        )}
        {state.stage !== 'idle' && state.stage !== 'complete' && state.stage !== 'error' && (
          <div className="flex gap-3 text-xs items-center">
             <span className="text-emerald-500/50 shrink-0 select-none">[{state.logs.length.toString().padStart(3, '0')}]</span>
             <span className="w-2 h-4 bg-emerald-500/50 animate-pulse" />
          </div>
        )}
      </div>
      
      <div className="px-4 py-1.5 bg-black/20 border-t border-white/5 flex items-center justify-between relative z-10">
        <div className="flex items-center gap-2">
          <div className={state.stage !== 'idle' && state.stage !== 'complete' ? "w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" : "w-1.5 h-1.5 rounded-full bg-slate-700"} />
          <span className="text-[9px] text-slate-500 uppercase tracking-tighter">
            {state.stage === 'idle' ? 'Ready' : state.stage === 'complete' ? 'Process Terminated' : 'Streaming...'}
          </span>
        </div>
        <span className="text-[9px] text-slate-600 font-mono">
          UTF-8
        </span>
      </div>
    </HoverBorderCard>
  );
};

export default TerminalLogs;
