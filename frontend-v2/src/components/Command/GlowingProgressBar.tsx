import React from "react";
import { motion } from "framer-motion";

interface GlowingProgressBarProps {
  progress: number;
  stage: string;
}

const GlowingProgressBar: React.FC<GlowingProgressBarProps> = ({ progress, stage }) => {
  return (
    <div className="space-y-3 mt-8">
      <div className="flex justify-between items-end px-1">
        <div className="flex flex-col">
          <span className="text-[10px] font-bold text-zinc-500 uppercase tracking-[0.2em]">Active Stage</span>
          <span className="text-xs font-bold text-cyan-400 uppercase tracking-widest animate-pulse">
            {stage === 'idle' ? 'Awaiting Ignition' : stage}
          </span>
        </div>
        <span className="text-xs font-mono text-zinc-500">{(progress * 100).toFixed(0)}%</span>
      </div>
      
      <div className="h-2 w-full bg-white/[0.03] border border-white/5 rounded-full overflow-hidden relative">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${progress * 100}%` }}
          transition={{ type: "spring", stiffness: 50, damping: 20 }}
          className="h-full bg-gradient-to-r from-cyan-500 to-purple-500 relative"
        >
          {/* Inner Glow */}
          <div className="absolute inset-0 shadow-[0_0_15px_rgba(34,211,238,0.5)]" />
        </motion.div>
        
        {/* Animated Scanline */}
        {progress > 0 && progress < 1 && (
          <motion.div
            animate={{ left: ["-10%", "110%"] }}
            transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
            className="absolute top-0 bottom-0 w-20 bg-gradient-to-r from-transparent via-white/20 to-transparent skew-x-12 z-20"
          />
        )}
      </div>
    </div>
  );
};

export default GlowingProgressBar;
