import React from "react";
import PillNavbar from "../components/Navigation/PillNavbar";
import { AuroraBackground } from "../components/Visuals/AuroraBackground";

interface MainLayoutProps {
  children: React.ReactNode;
  onViewChange?: (view: "operations" | "architecture") => void;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children, onViewChange }) => {
  return (
    <AuroraBackground className="z-0">
      <div className="min-h-screen text-white font-sans selection:bg-cyan-500/30 overflow-x-hidden text-balance w-full">
        <PillNavbar onViewChange={onViewChange} />

        <main className="relative z-10 pt-32 pb-20 px-6 max-w-[1700px] mx-auto">
          {children}
        </main>

        {/* Footer Branding */}
        <footer className="relative z-10 py-16 px-8 border-t border-white/5 bg-black/40 mt-24">
          <div className="max-w-[1700px] mx-auto flex flex-col md:flex-row justify-between items-center gap-8 text-pretty">
            <div className="flex items-center gap-4 opacity-80 transition-all cursor-default">
              <div className="w-10 h-10 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center shadow-2xl">
                <span className="text-[12px] font-black text-white">M</span>
              </div>
              <span className="text-[11px] font-black tracking-[0.5em] uppercase text-white">MoSPI AI Learning Platform</span>
            </div>
            <div className="flex gap-12 text-[11px] font-black text-zinc-500 uppercase tracking-widest">
              <a href="#" className="hover:text-cyan-400 transition-colors duration-300">Documentation</a>
              <a href="#" className="hover:text-cyan-400 transition-colors duration-300">API Status</a>
              <a href="#" className="hover:text-cyan-400 transition-colors duration-300">Security Audit</a>
            </div>
          </div>
          <div className="max-w-[1700px] mx-auto mt-12 pt-8 border-t border-white/[0.02] flex justify-center">
            <p className="text-[10px] font-bold text-zinc-700 uppercase tracking-[0.4em]">© 2026 MoSPI CAPACITY BUILDING</p>
          </div>
        </footer>
      </div>
    </AuroraBackground>
  );
};

export default MainLayout;
