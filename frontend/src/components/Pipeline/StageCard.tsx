import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, Circle, Clock, AlertCircle, Search, User, BookOpen, Target, GraduationCap } from 'lucide-react';
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
      case 'profiling': return <User className="w-5 h-5" />;
      case 'identifying_gaps': return <Target className="w-5 h-5" />;
      case 'matching_courses': return <Search className="w-5 h-5" />;
      case 'pathway_built': return <GraduationCap className="w-5 h-5" />;
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

  const renderProfiling = (data: any) => {
    const skillsDict = data.current_skills || {};
    const totalSkills = Object.values(skillsDict).reduce((acc: number, list: any) => acc + (list?.length || 0), 0);
    
    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-[10px] uppercase tracking-widest text-zinc-500 font-black">Identified Skills</span>
          <Badge className="bg-cyan-500/10 text-cyan-400 border-cyan-500/20 px-3 py-1 rounded-full text-[11px] font-black uppercase tracking-wider">
            {totalSkills} Skills Found
          </Badge>
        </div>
        <div className="space-y-3">
          {Object.entries(skillsDict).map(([domain, skills]: [string, any], idx: number) => (
            <div key={idx}>
              <span className="text-[9px] text-cyan-400/80 font-black uppercase tracking-widest block mb-1">{domain}</span>
              <div className="flex flex-wrap gap-2">
                {(skills || []).map((skill: string, i: number) => (
                  <span key={i} className="text-[10px] bg-white/5 border border-white/10 px-2 py-1 rounded text-zinc-300">
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderIdentifyingGaps = (data: any) => {
    const gapsDict = data.skill_gaps || {};
    const totalGaps = Object.values(gapsDict).reduce((acc: number, list: any) => acc + (list?.length || 0), 0);

    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-[10px] uppercase tracking-widest text-zinc-500 font-black">Skill Gaps</span>
          <Badge className="bg-orange-500/10 text-orange-400 border-orange-500/20 px-3 py-1 rounded-full text-[11px] font-black uppercase tracking-wider">
            {totalGaps} Gaps Detected
          </Badge>
        </div>
        <div className="space-y-3">
          {Object.entries(gapsDict).map(([domain, gaps]: [string, any], idx: number) => (
            <div key={idx}>
              <span className="text-[9px] text-orange-400/80 font-black uppercase tracking-widest block mb-1">{domain}</span>
              <div className="flex flex-wrap gap-2">
                {(gaps || []).map((gap: string, i: number) => (
                  <span key={i} className="text-[10px] bg-orange-500/5 border border-orange-500/20 px-2 py-1 rounded text-orange-300">
                    {gap}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
        <div className="bg-white/[0.02] border border-white/5 rounded-xl p-4 mt-2">
          <p className="text-[11px] text-zinc-300 leading-relaxed font-medium">
            {data.analysis_summary || 'Analyzing profile data...'}
          </p>
        </div>
      </div>
    );
  };

  const renderMatchingCourses = (data: any) => (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <span className="text-[10px] uppercase tracking-widest text-zinc-500 font-black">iGOT Course Catalog</span>
        <span className="text-[10px] font-black text-cyan-400 bg-cyan-400/10 px-2 py-0.5 rounded uppercase">
          {data.courses?.length || 0} Matches Found
        </span>
      </div>
      <div className="space-y-3">
        {(data.courses || []).slice(0, 3).map((course: any, i: number) => (
          <div key={i} className="bg-black/40 border border-white/5 rounded-xl p-3 relative group">
            <h4 className="text-[12px] font-bold text-white mb-1">{course.course_name}</h4>
            <div className="flex gap-2 text-[9px] uppercase font-bold tracking-wider mb-2">
              <span className="text-zinc-500">{course.domain}</span>
              <span className="text-cyan-600">•</span>
              <span className="text-cyan-500">{course.course_id}</span>
            </div>
            <p className="text-[10px] text-zinc-400 line-clamp-2">
              {course.description}
            </p>
          </div>
        ))}
      </div>
    </div>
  );

  const renderPathwayBuilt = (data: any) => (
    <div className="space-y-4">
      <span className="text-[10px] uppercase tracking-widest text-zinc-500 font-black">Suggested Learning Pathway</span>
      <div className="bg-blue-500/5 border border-blue-500/20 rounded-xl p-4">
        <p className="text-[12px] text-blue-200 leading-relaxed">
          {data.suggested_pathway || 'Building pathway...'}
        </p>
      </div>
      
      <div className="pt-2">
        <button className="w-full py-3 bg-white/10 hover:bg-white/20 border border-white/10 rounded-lg text-[11px] font-black uppercase tracking-widest text-white transition-all flex items-center justify-center gap-2">
          <BookOpen className="w-4 h-4" />
          Generate Assessment Quiz
        </button>
      </div>
    </div>
  );


  const renderContent = () => {
    if (!result) return null;
    
    switch (stage) {
      case 'profiling': return renderProfiling(result);
      case 'identifying_gaps': return renderIdentifyingGaps(result);
      case 'matching_courses': return renderMatchingCourses(result);
      case 'pathway_built': return renderPathwayBuilt(result);
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
                AI Analysis Active
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
