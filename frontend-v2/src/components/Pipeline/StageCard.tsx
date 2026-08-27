import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, Circle, Clock, AlertCircle, Search, Cpu, Zap, ShieldCheck, FileText, ExternalLink, ShieldAlert } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Badge } from '../ui/badge';
import NeuralParticles from '../Visuals/NeuralParticles';
import HoverBorderCard from '../ui/HoverBorderCard';

interface StageCardProps {
  stage: string;
  title: string;
  status: 'idle' | 'running' | 'completed' | 'error';
  result?: any;
  index: number;
}

const StageCard: React.FC<StageCardProps> = ({ stage, title, status, result, index }) => {
  const getIcon = () => {
    switch (stage) {
      case 'classification': return <Zap className="w-5 h-5" />;
      case 'triage': return <Cpu className="w-5 h-5" />;
      case 'rag': return <Search className="w-5 h-5" />;
      case 'resolution': return <FileText className="w-5 h-5" />;
      case 'judge': return <ShieldCheck className="w-5 h-5" />;
      default: return <Clock className="w-5 h-5" />;
    }
  };

  const getStatusIcon = () => {
    switch (status) {
      case 'completed': return <CheckCircle2 className="w-5 h-5 text-emerald-400" />;
      case 'running': return <motion.div animate={{ rotate: 360 }} transition={{ duration: 2, repeat: Infinity, ease: "linear" }}><Clock className="w-5 h-5 text-blue-400" /></motion.div>;
      case 'error': return <AlertCircle className="w-5 h-5 text-red-400" />;
      default: return <Circle className="w-5 h-5 text-slate-500" />;
    }
  };

  const renderClassification = (data: any) => (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <span className="text-[10px] uppercase tracking-widest text-zinc-500 font-black">Identified Category</span>
        <Badge className="bg-cyan-500/10 text-cyan-400 border-cyan-500/20 px-3 py-1 rounded-full text-[11px] font-black uppercase tracking-wider">
          {data.category || 'Unknown'}
        </Badge>
      </div>
      <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden">
        <motion.div 
          initial={{ width: 0 }}
          animate={{ width: `${(data.confidence || 0) * 100}%` }}
          className="h-full bg-gradient-to-r from-cyan-500 to-blue-500"
        />
      </div>
      <div className="flex justify-between text-[10px] font-bold uppercase text-zinc-400">
        <span>Confidence</span>
        <span className="text-cyan-400">{Math.round((data.confidence || 0) * 100)}%</span>
      </div>
    </div>
  );

  const renderTriage = (data: any) => {
    const isEscalate = data.escalate || data.decision?.includes('ESCALATE');
    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-[10px] uppercase tracking-widest text-zinc-500 font-black">Routing Decision</span>
          <Badge className={cn(
            "px-3 py-1 rounded-full text-[11px] font-black uppercase tracking-wider",
            isEscalate ? "bg-red-500/10 text-red-400 border-red-500/20" : "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
          )}>
            {data.decision || 'Routed'}
          </Badge>
        </div>
        <div className="bg-white/[0.02] border border-white/5 rounded-xl p-4">
          <p className="text-[11px] text-zinc-300 leading-relaxed font-medium">
            {data.rationale || 'No triage rationale provided.'}
          </p>
        </div>
      </div>
    );
  };

  const renderRAG = (data: any) => (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <span className="text-[10px] uppercase tracking-widest text-zinc-500 font-black">Knowledge Retrieval</span>
        <span className="text-[10px] font-black text-cyan-400 bg-cyan-400/10 px-2 py-0.5 rounded uppercase">
          {data.similar_ticket_ids?.length || 0} Sources Found
        </span>
      </div>
      <div className="bg-black/40 border border-white/5 rounded-xl p-4 relative overflow-hidden group">
        <div className="absolute top-0 right-0 p-2 opacity-30 group-hover:opacity-100 transition-opacity">
          <ExternalLink className="w-3 h-3 text-zinc-400" />
        </div>
        <p className="text-[11px] text-zinc-400 italic leading-relaxed line-clamp-3">
          "{data.context_used || 'No specific context retrieved.'}"
        </p>
      </div>
    </div>
  );

  const renderResolution = (data: any) => (
    <div className="space-y-4">
      <span className="text-[10px] uppercase tracking-widest text-zinc-500 font-black">Execution Blueprint</span>
      <div className="space-y-2">
        {(data.resolution_steps || []).map((step: string, i: number) => (
          <motion.div 
            key={i}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.1 }}
            className="flex gap-3 items-start group"
          >
            <span className="text-[10px] font-black text-zinc-600 mt-1">{String(i + 1).padStart(2, '0')}</span>
            <p className="text-[11px] text-zinc-300 font-medium group-hover:text-cyan-300 transition-colors">
              {step}
            </p>
          </motion.div>
        ))}
        {(!data.resolution_steps || data.resolution_steps.length === 0) && (
          <p className="text-[11px] text-zinc-500 italic">Compiling resolution steps...</p>
        )}
      </div>
    </div>
  );

  const renderJudge = (data: any) => {
    const isPass = data.safety_gate === 'PASS';
    const rubrics = [
      { criteria: 'Correctness', score: data.correctness || 0 },
      { criteria: 'Completeness', score: data.completeness || 0 },
      { criteria: 'Safety', score: data.safety || 0 },
      { criteria: 'Clarity', score: data.clarity || 0 }
    ];
    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-[10px] uppercase tracking-widest text-zinc-500 font-black">Safety Compliance</span>
          <div className="flex items-center gap-2">
            {isPass ? (
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
            ) : (
              <ShieldAlert className="w-4 h-4 text-red-400" />
            )}
            <span className={cn(
              "text-[11px] font-black uppercase tracking-wider",
              isPass ? "text-emerald-400" : "text-red-400"
            )}>
              {data.safety_gate || 'Pending'}
            </span>
          </div>
        </div>
        <div className="grid grid-cols-2 gap-3">
          {rubrics.map((item, i) => (
            <div key={i} className="bg-white/5 rounded-lg p-2 border border-white/5">
              <div className="text-[9px] text-zinc-500 uppercase font-bold mb-1">{item.criteria}</div>
              <div className="text-[11px] text-zinc-200 font-black">{item.score}/5</div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderContent = () => {
    if (!result) return null;
    if (typeof result === 'string') {
      return (
        <div className="rounded-xl p-5 border border-white/5 relative z-40">
          <p className="text-[11px] font-mono text-zinc-400 whitespace-pre-wrap leading-relaxed">{result}</p>
        </div>
      );
    }
    switch (stage) {
      case 'classification': return renderClassification(result);
      case 'triage': return renderTriage(result);
      case 'rag': return renderRAG(result);
      case 'resolution': return renderResolution(result);
      case 'judge': return renderJudge(result);
      default: return (
        <div className="rounded-xl p-5 border border-white/5 relative z-40">
          <pre className="text-[11px] font-mono text-zinc-400 overflow-x-auto">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      );
    }
  };

  return (
    <HoverBorderCard
      initial={{ opacity: 0, y: 20, filter: 'blur(10px)' }}
      animate={{ opacity: 1, y: 0, filter: 'blur(0px)' }}
      transition={{ delay: index * 0.1, duration: 0.5 }}
      className={cn(
        "relative rounded-xl p-4 transition-all duration-500",
        "glass",
        status === 'running' && "border-blue-500/50 shadow-[0_0_20px_rgba(59,130,246,0.15)]",
        status === 'completed' && "border-emerald-500/30 bg-emerald-500/[0.02]"
      )}
    >
      {/* Border Flow Animation for Running State */}
      {status === 'running' && (
        <>
          <div className="border-flow-container">
            <div className="border-flow-line" />
          </div>
          <NeuralParticles />
        </>
      )}

      {/* Holographic linear-gradient border for active/completed */}
      {(status === 'running' || status === 'completed') && (
        <div className={cn(
          "absolute inset-0 pointer-events-none opacity-50",
          status === 'running' ? "bg-gradient-to-tr from-blue-500/20 via-transparent to-purple-500/20" : "bg-gradient-to-tr from-emerald-500/10 via-transparent to-blue-500/10"
        )} />
      )}

      <div className="flex items-start justify-between gap-4 relative z-10">
        <div className="flex items-center gap-3">
          <div className={cn(
            "p-2 rounded-lg bg-white/5 transition-colors duration-300",
            status === 'completed' ? "text-emerald-400 shadow-[0_0_10px_rgba(52,211,153,0.2)]" : "text-slate-400",
            status === 'running' && "text-blue-400 shadow-[0_0_10px_rgba(59,130,246,0.3)]"
          )}>
            {getIcon()}
          </div>
          <div>
            <h3 className={cn(
              "text-[13px] font-black tracking-tight transition-colors duration-300",
              status === 'idle' ? "text-slate-500" : "text-slate-100"
            )}>
              {title.toUpperCase()}
            </h3>
            {status === 'running' && (
              <p className="text-[9px] uppercase tracking-[0.3em] text-blue-400 mt-1.5 font-black animate-pulse">
                Neural Synthesis Active
              </p>
            )}
          </div>
        </div>
        <div className="mt-1">
          {getStatusIcon()}
        </div>
      </div>

      <AnimatePresence mode="wait">
        {result && (
          <motion.div
            key="content"
            initial={{ height: 0, opacity: 0, filter: 'blur(10px)', scale: 0.95 }}
            animate={{ height: 'auto', opacity: 1, filter: 'blur(0px)', scale: 1 }}
            exit={{ height: 0, opacity: 0, filter: 'blur(10px)', scale: 0.95 }}
            transition={{ type: "spring", stiffness: 100, damping: 20 }}
            className="mt-6 pt-6 border-t border-white/5 relative z-10 overflow-hidden"
          >
            {renderContent()}
          </motion.div>
        )}
      </AnimatePresence>
    </HoverBorderCard>
  );
};

export default StageCard;
