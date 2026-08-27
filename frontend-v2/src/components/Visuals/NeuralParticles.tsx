import React from 'react';
import { motion } from 'framer-motion';

const NeuralParticles: React.FC = () => {
  // Generate 8 random nodes
  const nodes = Array.from({ length: 8 }).map((_, i) => ({
    id: i,
    top: `${Math.random() * 100}%`,
    left: `${Math.random() * 100}%`,
    delay: Math.random() * 5,
    duration: 6 + Math.random() * 4
  }));

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-40">
      {/* SVG Connections */}
      <svg className="absolute inset-0 w-full h-full">
        <defs>
          <linearGradient id="neural-grad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="var(--primary)" stopOpacity="0.2" />
            <stop offset="100%" stopColor="var(--secondary)" stopOpacity="0.1" />
          </linearGradient>
        </defs>
        
        {/* Simple connecting lines between first few nodes */}
        {nodes.slice(0, 4).map((node, i) => (
          <motion.line
            key={`line-${i}`}
            x1={node.left}
            y1={node.top}
            x2={nodes[(i + 1) % nodes.length].left}
            y2={nodes[(i + 1) % nodes.length].top}
            stroke="url(#neural-grad)"
            strokeWidth="0.5"
            initial={{ pathLength: 0, opacity: 0 }}
            animate={{ pathLength: 1, opacity: 1 }}
            transition={{ 
              duration: 2, 
              repeat: Infinity, 
              repeatType: "reverse", 
              delay: node.delay 
            }}
          />
        ))}
      </svg>

      {/* Pulsing Nodes */}
      {nodes.map((node) => (
        <div
          key={node.id}
          className="neural-particle"
          style={{
            top: node.top,
            left: node.left,
            animationDelay: `${node.delay}s`,
            animationDuration: `${node.duration}s`
          }}
        />
      ))}
    </div>
  );
};

export default NeuralParticles;
