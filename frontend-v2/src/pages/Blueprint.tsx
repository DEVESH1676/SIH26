import React, { useEffect, useState } from 'react';
import MermaidCanvas from '../components/Architecture/Mermaid';
import TermInspector, { type Term } from '../components/Architecture/TermInspector';
import { Cpu } from 'lucide-react';

interface BlueprintData {
  execution_flow: string;
  dictionary: Term[];
  dependencies: { from: string; to: string; type: string }[];
}

const Blueprint: React.FC = () => {
  const [data, setData] = useState<BlueprintData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBlueprint = async () => {
      try {
        const res = await fetch('/api/blueprint');
        if (!res.ok) throw new Error('Failed to fetch blueprint data');
        const json = await res.json();
        setData(json);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchBlueprint();
  }, []);

  const handleSearch = (nodeId: string | null) => {
    // We search the container for both Mermaid graphs
    const nodes = document.querySelectorAll('.node');
    
    if (!nodeId) {
      // Reset all
      nodes.forEach(node => {
        (node as HTMLElement).style.opacity = '1';
        (node as HTMLElement).style.filter = 'none';
        (node as HTMLElement).style.transition = 'all 0.3s ease';
        
        // Custom styling cleanup
        const rect = node.querySelector('rect, polygon, circle');
        if (rect) {
          (rect as HTMLElement).style.strokeWidth = '';
          (rect as HTMLElement).style.stroke = '';
        }
      });
      return;
    }

    nodes.forEach(node => {
      const el = node as HTMLElement;
      // Mermaid nodes have ids like "flowchart-step1-something"
      // or the node ID is stored in the id attribute
      // The text inside the node can also be checked, or we can check if id includes nodeId
      
      const isMatch = el.id.includes(nodeId) || el.getAttribute('id')?.includes(nodeId);
      
      el.style.transition = 'all 0.3s ease';
      
      if (isMatch) {
        el.style.opacity = '1';
        el.style.filter = 'drop-shadow(0 0 8px rgba(34,211,238,0.8))';
        const rect = el.querySelector('rect, polygon, circle');
        if (rect) {
          (rect as HTMLElement).style.strokeWidth = '3px';
          (rect as HTMLElement).style.stroke = '#22d3ee';
        }
      } else {
        el.style.opacity = '0.3';
        el.style.filter = 'blur(1px)';
        const rect = el.querySelector('rect, polygon, circle');
        if (rect) {
          (rect as HTMLElement).style.strokeWidth = '';
          (rect as HTMLElement).style.stroke = '';
        }
      }
    });
  };

  if (loading) {
    return (
      <div className="min-h-[70vh] flex items-center justify-center">
        <div className="animate-pulse text-cyan-500 font-mono tracking-widest text-sm">LOADING ARCHITECTURE...</div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-[70vh] flex items-center justify-center">
        <div className="text-red-400 font-mono text-sm border border-red-500/20 bg-red-500/10 p-4 rounded-xl">
          ERROR: {error || 'Failed to load blueprint'}
        </div>
      </div>
    );
  }

  // Generate a simple mermaid string for dependencies if not provided by backend as mermaid
  const depGraph = data.dependencies 
    ? "%%{init: {'flowchart': {'curve': 'basis'}}}%%\ngraph TD\n  Pipeline[\"api/routes/pipeline.py\"]\n" + data.dependencies.map((d, i) => `  Pipeline -->|${d.type}| Node${i}[\"${d.to}\"]`).join("\n")
    : "graph TD\n  A[No Dependencies Found]";

  return (
    <div className="w-full flex flex-col gap-8 pb-12">
      {/* Header */}
      <div className="glass rounded-2xl p-8 border-white/10 shadow-[0_20px_50px_rgba(0,0,0,0.4)] flex items-center gap-6 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/10 to-transparent pointer-events-none" />
        <div className="w-16 h-16 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 shadow-[0_0_15px_rgba(34,211,238,0.2)]">
          <Cpu className="w-8 h-8" />
        </div>
        <div>
          <h1 className="text-3xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-white to-white/60">
            Nexus Architecture Blueprint
          </h1>
          <p className="text-xs font-bold uppercase tracking-[0.3em] text-cyan-400 mt-2">
            System Topology & Data Flow Orchestration
          </p>
        </div>
      </div>

      {/* Main Dual-Pane Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left: Term Inspector */}
        <div className="lg:col-span-4 h-[800px] lg:sticky lg:top-32">
          <div className="h-full glass rounded-2xl border border-white/10 p-6 flex flex-col">
            <h2 className="text-sm font-black uppercase tracking-widest text-zinc-400 mb-6 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-cyan-500 animate-pulse" />
              Term Inspector
            </h2>
            <TermInspector terms={data.dictionary} onSearch={handleSearch} />
          </div>
        </div>

        {/* Right: Mermaid Canvases */}
        <div className="lg:col-span-8 space-y-8">
          
          {/* Primary Flow */}
          <div className="glass rounded-2xl border border-white/10 p-6">
            <h2 className="text-sm font-black uppercase tracking-widest text-zinc-400 mb-6 flex items-center gap-2">
              Execution Flow
            </h2>
            <MermaidCanvas 
              id="execution-flow-chart"
              chart={data.execution_flow} 
              className="bg-black/20 border-white/5" 
            />
          </div>

          {/* Secondary Graph */}
          <div className="glass rounded-2xl border border-white/10 p-6">
            <h2 className="text-sm font-black uppercase tracking-widest text-zinc-400 mb-6 flex items-center gap-2">
              Dependency Graph
            </h2>
            <MermaidCanvas 
              id="dependency-graph-chart"
              chart={depGraph} 
              className="bg-black/20 border-white/5 overflow-x-auto" 
            />
          </div>

        </div>
      </div>
    </div>
  );
};

export default Blueprint;
