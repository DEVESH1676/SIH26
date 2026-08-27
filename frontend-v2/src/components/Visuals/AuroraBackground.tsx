import React, { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import { cn } from '../../lib/utils';

interface AuroraBackgroundProps {
  children: React.ReactNode;
  showRadialGradient?: boolean;
  className?: string;
}

export const AuroraBackground = ({
  children,
  showRadialGradient = true,
  className,
}: AuroraBackgroundProps) => {
  const containerRef = useRef(null);
  const isInView = useInView(containerRef, { amount: 0.1 });

  return (
    <div ref={containerRef} className="relative flex flex-col min-h-screen items-center justify-center bg-zinc-950 text-slate-950 transition-bg">
      <div className={cn("absolute inset-0 overflow-hidden", className)}>
        <div
          // Optimized: will-change-transform for GPU acceleration
          className={cn(
            `
            [--white-gradient:linear-gradient(to_bottom,white,white_transparent)]
            [--dark-gradient:linear-gradient(to_bottom,black,black_transparent)]
            [--aurora:repeating-linear-gradient(100deg,var(--blue-500)_10%,var(--indigo-300)_15%,var(--blue-300)_20%,var(--violet-200)_25%,var(--blue-400)_30%)]
            [background-image:var(--white-gradient),var(--aurora)]
            dark:[background-image:var(--dark-gradient),var(--aurora)]
            [background-size:300%,_200%]
            [background-position:50%_50%,50%_50%]
            filter blur-[10px] invert dark:invert-0
            after:content-[""] after:absolute after:inset-0 after:[background-image:var(--white-gradient),var(--aurora)] 
            after:dark:[background-image:var(--dark-gradient),var(--aurora)]
            after:[background-size:200%,_100%] 
            after:animate-aurora after:[background-attachment:fixed] after:mix-blend-difference
            pointer-events-none
            absolute -inset-[10px] opacity-50 will-change-transform`,
            showRadialGradient &&
              `[mask-image:radial-gradient(ellipse_at_100%_0%,black_10%,transparent_70%)]`
          )}
        ></div>
        
        {/* Animated Aurora Layers with Viewport Awareness */}
        {isInView && (
          <div className="absolute inset-0 overflow-hidden pointer-events-none">
            <motion.div
               animate={{
                 opacity: [0.3, 0.5, 0.3],
                 scale: [1, 1.1, 1],
                 rotate: [0, 5, 0],
               }}
               transition={{
                 duration: 15,
                 repeat: Infinity,
                 ease: "easeInOut"
               }}
               className="absolute top-[-20%] left-[-10%] w-[120%] h-[140%] bg-gradient-to-br from-blue-500/20 via-transparent to-purple-500/20 blur-[100px] will-change-transform"
            />
            <motion.div
               animate={{
                 opacity: [0.2, 0.4, 0.2],
                 scale: [1.1, 1, 1.1],
                 rotate: [0, -5, 0],
               }}
               transition={{
                 duration: 20,
                 repeat: Infinity,
                 ease: "easeInOut"
               }}
               className="absolute bottom-[-20%] right-[-10%] w-[120%] h-[140%] bg-gradient-to-tl from-emerald-500/10 via-transparent to-blue-500/10 blur-[100px] will-change-transform"
            />
          </div>
        )}
      </div>
      <div className="relative z-10 w-full h-full">
        {children}
      </div>
    </div>
  );
};
