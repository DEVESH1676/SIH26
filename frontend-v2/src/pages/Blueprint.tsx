import React, { useEffect, useState } from 'react';
import MermaidCanvas from '../components/Architecture/Mermaid';
import TermInspector, { type Term } from '../components/Architecture/TermInspector';
import { Cpu } from 'lucide-react';

const LMS_GRAPH = `
%%{init: {'flowchart': {'curve': 'basis', 'theme': 'dark'}}}%%
graph TD
    UI[Frontend: operations.tsx] -->|POST /api/pipeline/stream| Pipeline[Pipeline Controller]
    
    subgraph Core AI Layer
        Pipeline --> PA[ProfileAgent: analyze_profile]
        PA --> Ext[FRAC Competency Extractor]
        Ext --> Gaps[Skill Gap Identifier]
        
        Gaps --> Path[PathwayAgent: suggest_courses]
        Path --> RAG[RAG Engine: chroma_db]
        
        RAG --> iGOT[iGOT Catalog Matcher]
    end
    
    iGOT -->|SSE Stream| UI
    
    subgraph Assessment Engine
        Doc[Uploaded Doc] --> Parser[MediaParser]
        Parser --> QA[AssessmentAgent: QuizGenerator]
        QA -->|POST /api/assessment| UI
    end
`;

const LMS_DICTIONARY: Term[] = [
  { term: "ProfileAgent", description: "LLM agent that maps official duties to the tripartite FRAC competency model.", storage: "In-Memory", nodeId: "PA" },
  { term: "PathwayAgent", description: "Recommends learning interventions by matching skill gaps against iGOT courses.", storage: "In-Memory", nodeId: "Path" },
  { term: "AssessmentAgent", description: "Generates multiple-choice quizzes and subjective evaluations from learning material.", storage: "SQLite", nodeId: "QA" },
  { term: "ChromaDB", description: "Local vector database storing embedding vectors for semantic search over course catalog.", storage: "Disk", nodeId: "ChromaDB" },
  { term: "MediaParser", description: "Data ingestion engine capable of parsing PDF, DOCX, PPTX, and multimedia.", storage: "Disk", nodeId: "Parser" }
];

const Blueprint: React.FC = () => {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate loading for effect
    setTimeout(() => {
      setLoading(false);
    }, 800);
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

  const depGraph = `
%%{init: {'flowchart': {'curve': 'basis', 'theme': 'dark'}}}%%
graph LR
  FastAPI --> Ollama
  FastAPI --> Groq
  FastAPI --> ChromaDB
  FastAPI --> SQLite[learner_progress.db]
  React --> FastAPI
  `;

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
            MoSPI Architecture Blueprint
          </h1>
          <p className="text-xs font-bold uppercase tracking-[0.3em] text-cyan-400 mt-2">
            AI Learning Platform Topology & Data Flow
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
            <TermInspector terms={LMS_DICTIONARY} onSearch={handleSearch} />
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
              chart={LMS_GRAPH} 
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
