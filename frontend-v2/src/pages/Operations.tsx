import React from 'react';
import IntelligenceFeed from '../components/Pipeline/IntelligenceFeed';
import SystemReadiness from '../components/Pipeline/SystemReadiness';
import ProfileForm from "../components/Command/ProfileForm";
import GlowingProgressBar from "../components/Command/GlowingProgressBar";
import TerminalLogs from "../components/Visuals/TerminalLogs";
import LearnerHistory from "../components/History/LearnerHistory";
import AdminAnalytics from "../components/Analytics/AdminAnalytics";
import { usePipeline } from '../hooks/usePipeline';
import HoverBorderCard from '../components/ui/HoverBorderCard';

const Operations: React.FC = () => {
  const { state, startPipeline } = usePipeline();
  const isPipelineActive = state.stage !== 'idle' && state.stage !== 'complete' && state.stage !== 'error';

  return (
    <div className="space-y-16">
      
      {/* ROW 1: ACTIVE OPERATIONS */}
      <div id="classify" className="grid grid-cols-1 xl:grid-cols-12 gap-8 items-start">
        
        {/* LEFT: Command & Logs */}
        <div className="xl:col-span-4 flex flex-col gap-6 xl:sticky xl:top-32">
          <HoverBorderCard className="glass rounded-2xl p-6 lg:p-8 border-white/10 shadow-[0_20px_50px_rgba(0,0,0,0.4)] relative overflow-hidden group">
            <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-cyan-500/30 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700" />
            
            <div className="flex items-center gap-4 mb-6 relative z-10">
              <div className="w-10 h-10 rounded-xl bg-cyan-500/5 border border-cyan-500/20 flex items-center justify-center text-cyan-400 shrink-0 shadow-inner">
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </div>
              <div>
                <h1 className="text-lg font-black tracking-tight text-white/90 leading-none">Learning Plan Generator</h1>
                <p className="text-[9px] text-[#94a3b8] font-black uppercase tracking-[0.2em] mt-1.5">MoSPI AI Active</p>
              </div>
            </div>
            
            <div className="relative z-10">
              <ProfileForm onSubmit={startPipeline} isLoading={isPipelineActive} />
              <GlowingProgressBar progress={state.progress} stage={state.stage} />
            </div>
          </HoverBorderCard>

          {/* Terminal always visible for active feedback */}
          <div className="h-[250px]">
            <TerminalLogs />
          </div>
        </div>

        {/* RIGHT: Intelligence Feed */}
        <div className="xl:col-span-8 flex flex-col">
          {state.stage === 'idle' ? (
            <SystemReadiness />
          ) : (
            <IntelligenceFeed />
          )}
        </div>
      </div>

      {/* ROW 2: SYSTEM INSIGHTS */}
      <div className="space-y-12 pt-12 border-t border-white/5">
        <div className="flex flex-col gap-2">
          <h2 className="text-2xl font-black tracking-tight text-white/90 uppercase tracking-widest">Dashboard & Insights</h2>
          <p className="text-[#94a3b8] text-[10px] font-black uppercase tracking-[0.3em]">MoSPI Official Statistics Telemetry</p>
        </div>

        <div className="space-y-8">
          {/* Top Insight Row: Side-by-Side Metrics */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div id="analytics">
              <AdminAnalytics />
            </div>
            <div id="history">
              <LearnerHistory />
            </div>
          </div>
        </div>
      </div>

    </div>
  );
};

export default Operations;
