import React, { useState } from 'react';
import { Search } from 'lucide-react';

export interface Term {
  term: string;
  description: string;
  nodeId?: string;
  storage: string;
}

interface TermInspectorProps {
  terms: Term[];
  onSearch: (termId: string | null) => void;
}

const TermInspector: React.FC<TermInspectorProps> = ({ terms, onSearch }) => {
  const [query, setQuery] = useState('');

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    
    // Find the closest matching term nodeId, or null if empty
    if (!value.trim()) {
      onSearch(null);
      return;
    }
    
    const matchedTerm = terms.find(t => 
      t.term.toLowerCase().includes(value.toLowerCase()) || 
      t.description.toLowerCase().includes(value.toLowerCase())
    );
    
    onSearch(matchedTerm?.nodeId || null);
  };

  const filteredTerms = terms.filter(t => 
    t.term.toLowerCase().includes(query.toLowerCase()) || 
    t.description.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="flex flex-col h-full space-y-4">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-cyan-500" />
        <input
          type="text"
          placeholder="Search glossary..."
          value={query}
          onChange={handleSearch}
          className="w-full bg-white/5 border border-white/10 rounded-xl pl-10 pr-4 py-3 text-sm text-white placeholder:text-zinc-500 focus:outline-none focus:border-cyan-500/50 transition-all"
        />
      </div>

      <div className="flex-1 overflow-y-auto no-scrollbar space-y-3 pr-2">
        {filteredTerms.map((term, i) => (
          <div 
            key={i} 
            className="glass bg-white/[0.02] border border-white/5 p-4 rounded-xl hover:border-cyan-500/30 transition-colors group cursor-pointer"
            onClick={() => {
              setQuery(term.term);
              onSearch(term.nodeId || null);
            }}
          >
            <div className="flex justify-between items-start mb-2">
              <h4 className="text-cyan-400 font-black text-sm uppercase tracking-wide">{term.term}</h4>
              {term.nodeId && (
                <span className="text-[9px] bg-white/10 text-zinc-300 px-2 py-0.5 rounded-full font-mono">
                  NODE: {term.nodeId}
                </span>
              )}
            </div>
            <p className="text-zinc-300 text-[11px] mb-3 leading-relaxed">
              {term.description}
            </p>
            <div className="flex items-center gap-2">
              <span className="text-[9px] uppercase font-bold text-zinc-500">Storage Location</span>
              <span className="text-[10px] text-emerald-400 bg-emerald-400/10 px-2 py-0.5 rounded font-mono border border-emerald-400/20">
                {term.storage}
              </span>
            </div>
          </div>
        ))}
        {filteredTerms.length === 0 && (
          <div className="text-center p-8 text-zinc-500 text-sm">
            No terms found matching "{query}"
          </div>
        )}
      </div>
    </div>
  );
};

export default TermInspector;
