import React from 'react';
import { motion, useMotionValue, useSpring, useMotionTemplate } from 'framer-motion';
import type { HTMLMotionProps } from 'framer-motion';
import { cn } from '../../lib/utils';

interface HoverBorderCardProps extends HTMLMotionProps<"div"> {
  children: React.ReactNode;
}

export const HoverBorderCard = React.forwardRef<HTMLDivElement, HoverBorderCardProps>(
  ({ children, className, onMouseMove, ...props }, ref) => {
    const mouseX = useMotionValue(0);
    const mouseY = useMotionValue(0);

    const springConfig = { damping: 25, stiffness: 300 };
    const smoothX = useSpring(mouseX, springConfig);
    const smoothY = useSpring(mouseY, springConfig);

    const glowBackground = useMotionTemplate`radial-gradient(300px circle at ${smoothX}px ${smoothY}px, var(--primary), transparent 70%)`;

    const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
      const { left, top } = e.currentTarget.getBoundingClientRect();
      mouseX.set(e.clientX - left);
      mouseY.set(e.clientY - top);
      if (onMouseMove) onMouseMove(e);
    };

    return (
      <motion.div
        ref={ref}
        onMouseMove={handleMouseMove}
        className={cn("relative group overflow-hidden", className)}
        {...props}
      >
        {/* Magnetic Border Glow Overlay */}
        <div className="border-flow-container opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-0">
          <motion.div
            className="absolute inset-0"
            style={{ background: glowBackground }}
          />
        </div>

        {/* Content */}
        {children}
      </motion.div>
    );
  }
);

HoverBorderCard.displayName = "HoverBorderCard";
export default HoverBorderCard;
