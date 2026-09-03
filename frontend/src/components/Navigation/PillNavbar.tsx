import React, { useState, useEffect, useMemo } from "react";
import { motion } from "framer-motion";
import { cn } from "../../lib/utils";

const sections = [
  { id: "classify", label: "Competency Assessment" },
  { id: "analytics", label: "Workforce Analytics" },
  { id: "history", label: "Learner History" },
  { id: "blueprint", label: "Architecture Blueprint" },
];

interface PillNavbarProps {
  onViewChange?: (view: "operations" | "architecture") => void;
}

const PillNavbar: React.FC<PillNavbarProps> = ({ onViewChange }) => {
  const [activeSection, setActiveSection] = useState("classify");
  const [isScrolled, setIsScrolled] = useState(false);

  const observerEntries = useMemo(() => sections.map(s => ({ id: s.id })), []);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
      
      if (activeSection === "blueprint") return;

      const offset = window.innerHeight * 0.45; // Increased offset for better detection

      let current = activeSection;

      // Find the section currently in view by checking from bottom to top
      for (let i = sections.length - 1; i >= 0; i--) {
        const entry = sections[i];
        if (entry.id === "blueprint") continue;
        const el = document.getElementById(entry.id);
        if (!el) continue;
        
        const rect = el.getBoundingClientRect();
        if (rect.top <= offset) {
          current = entry.id;
          break;
        }
      }

      if (current && current !== activeSection) setActiveSection(current);
    };

    window.addEventListener("scroll", handleScroll, { passive: true });
    handleScroll();
    return () => window.removeEventListener("scroll", handleScroll);
  }, [activeSection, observerEntries]);

  const handleNavClick = (sectionId: string, e: React.MouseEvent) => {
    e.preventDefault();
    if (sectionId === "blueprint") {
      onViewChange?.("architecture");
    } else {
      onViewChange?.("operations");
      setTimeout(() => {
        const el = document.getElementById(sectionId);
        if (el) {
          const offset = 120; // Account for navbar height
          const bodyRect = document.body.getBoundingClientRect().top;
          const elementRect = el.getBoundingClientRect().top;
          const elementPosition = elementRect - bodyRect;
          const offsetPosition = elementPosition - offset;

          window.scrollTo({
            top: offsetPosition,
            behavior: "smooth"
          });
        }
      }, 50);
    }
    setActiveSection(sectionId);
  };

  return (
    <header
      className={cn(
        "fixed z-[100] transition-all duration-500 ease-in-out",
        "inset-x-0 top-0 border-b border-white/10 bg-black/50 backdrop-blur-2xl backdrop-saturate-150 md:border-none md:bg-transparent md:backdrop-filter-none",
        "md:inset-x-auto md:left-1/2 md:-translate-x-1/2 md:w-auto md:max-w-[95%] xl:max-w-7xl",
        isScrolled ? "md:top-4" : "md:top-8"
      )}
    >
      <div
        className={cn(
          "flex items-center justify-between px-4 lg:px-6 transition-all duration-500 ease-in-out",
          "md:rounded-full md:border",
          isScrolled
            ? "py-2 md:bg-white/[0.05] md:backdrop-blur-2xl md:backdrop-saturate-[1.8] md:shadow-2xl md:shadow-black/50 md:border-white/20"
            : "py-3 md:bg-transparent md:backdrop-blur-none md:shadow-none md:border-transparent"
        )}
      >
        {/* LOGO (Animated) */}
        <motion.a
          href="#classify"
          initial={{ letterSpacing: "0.2em" }}
          whileHover={{
            letterSpacing: "0.3em",
            textShadow: "0 0 20px rgba(34,211,238, 0.5)"
          }}
          transition={{ duration: 0.3 }}
          onClick={(e) => handleNavClick("classify", e)}
          className="font-black text-[11px] tracking-[0.2em] uppercase md:ml-4 md:mr-6 whitespace-nowrap cursor-pointer text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500"
        >
          MoSPI AI
        </motion.a>

        {/* DESKTOP NAV (Framer Motion Pill) */}
        <nav className="hidden md:flex items-center gap-1 p-1">
          {sections.map((section) => (
            <a
              key={section.id}
              href={`#${section.id}`}
              onClick={(e) => handleNavClick(section.id, e)}
              className={cn(
                "relative group px-4 lg:px-6 py-2 text-[10px] uppercase tracking-[0.15em] font-black transition-colors duration-300 rounded-full cursor-pointer",
                activeSection === section.id
                  ? "text-white"
                  : "text-zinc-500 hover:text-zinc-200"
              )}
            >
              {activeSection === section.id && (
                <motion.div
                  layoutId="navbar-pill"
                  className="absolute inset-0 bg-gradient-to-r from-cyan-500/20 to-blue-500/20 rounded-full -z-10 shadow-[0_0_20px_rgba(34,211,238,0.3),inset_0_0_12px_rgba(34,211,238,0.2)] border border-cyan-500/30"
                  transition={{ type: "spring", stiffness: 300, damping: 30 }}
                />
              )}
              <motion.span
                initial={{ letterSpacing: "0.15em" }}
                animate={{ letterSpacing: activeSection === section.id ? "0.25em" : "0.15em" }}
                transition={{ duration: 0.3, ease: "easeOut" }}
                className="inline-block whitespace-nowrap"
              >
                {section.label}
              </motion.span>
            </a>
          ))}
        </nav>

        {/* ACTIONS (Right) */}
        <div className="ml-2 pl-5 pr-4 border-l border-white/10 hidden lg:flex items-center gap-3">
          <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse shadow-[0_0_8px_rgba(16,185,129,0.5)]" />
          <span className="text-[9px] font-black text-zinc-500 uppercase tracking-widest">System Ready</span>
        </div>

      </div>
    </header>
  );
};

export default PillNavbar;
