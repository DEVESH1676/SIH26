import React from 'react';
import { usePipeline } from '../../hooks/usePipeline';
import StageCard from './StageCard';
import type { PipelineStage } from '../../types/pipeline';

const STAGES: { id: PipelineStage; title: string }[] = [
  { id: 'profiling', title: 'Competency Analysis' },
  { id: 'identifying_gaps', title: 'Skill Gap Identification' },
  { id: 'matching_courses', title: 'iGOT Course Matching' },
  { id: 'pathway_built', title: 'Learning Pathway Construction' },
];

const IntelligenceFeed: React.FC = () => {
  const { state } = usePipeline();

  const getStatus = (stageId: PipelineStage) => {
    if (state.stage === 'idle') return 'idle';
    if (state.stage === 'complete') return 'completed';
    if (state.stage === 'error') return 'error';

    const currentIdx = STAGES.findIndex(s => s.id === state.stage);
    const stageIdx = STAGES.findIndex(s => s.id === stageId);

    if (stageIdx < currentIdx && currentIdx !== -1) return 'completed';
    if (stageIdx === currentIdx) return 'running';
    return 'idle';
  };

  const getResult = (stageId: PipelineStage) => {
    switch (stageId) {
      case 'profiling':
      case 'identifying_gaps': return state.results.profile;
      case 'matching_courses':
      case 'pathway_built': return state.results.pathway;
      default: return undefined;
    }
  };

  return (
    <div className="flex flex-col gap-4 p-4 max-w-2xl mx-auto w-full h-full overflow-y-auto no-scrollbar">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse" />
          Intelligence Pipeline
        </h2>
        <div className="px-2 py-0.5 rounded-full bg-white/5 border border-white/10">
          <span className="text-[10px] font-mono text-slate-400 uppercase tracking-widest">
            STATE: {state.stage}
          </span>
        </div>
      </div>
      
      <div className="space-y-4">
        {STAGES.map((stage, index) => (
          <StageCard
            key={stage.id}
            stage={stage.id}
            title={stage.title}
            status={getStatus(stage.id)}
            result={getResult(stage.id)}
            index={index}
          />
        ))}
      </div>

      {state.error && (
        <div className="mt-4 p-4 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm flex items-center gap-3">
          <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
          {state.error}
        </div>
      )}
    </div>
  );
};

export default IntelligenceFeed;
