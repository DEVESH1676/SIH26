import React, { useEffect, useState } from "react";
import HoverBorderCard from "../ui/HoverBorderCard";

interface HistoryRecord {
  id: number;
  ticket_id: string;
  category: string;
  confidence: number;
  resolution_steps: string;
  judge_scores: string;
  agent_action: string;
  human_override: string | null;
  outcome: string;
  created_at: string;
}

const History: React.FC = () => {
  const [history, setHistory] = useState<HistoryRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch("/api/history");
        const data = await response.json();
        setHistory(data.history || []);
      } catch (error) {
        console.error("Failed to fetch history:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  const formatTimeAgo = (dateString: string) => {
    if (!dateString) return "N/A";
    try {
      const date = new Date(dateString);
      const now = new Date();
      const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);
      
      let interval = seconds / 31536000;
      if (interval > 1) return Math.floor(interval) + " years ago";
      interval = seconds / 2592000;
      if (interval > 1) return Math.floor(interval) + " months ago";
      interval = seconds / 86400;
      if (interval > 1) return Math.floor(interval) + " days ago";
      interval = seconds / 3600;
      if (interval > 1) return Math.floor(interval) + " hours ago";
      interval = seconds / 60;
      if (interval > 1) return Math.floor(interval) + " mins ago";
      return "just now";
    } catch {
      return "N/A";
    }
  };

  if (loading) {
    return (
      <div className="glass rounded-3xl p-12 flex items-center justify-center">
        <div className="animate-pulse text-cyan-500 font-mono tracking-widest text-sm">RECONSTRUCTING TIMELINE...</div>
      </div>
    );
  }

  return (
    <HoverBorderCard className="glass rounded-3xl p-6 overflow-hidden">
      <div className="flex items-center justify-between mb-6 relative z-10">
        <h2 className="text-xl font-bold tracking-tight text-white/90">Recent Run History</h2>
        <button className="text-xs font-semibold text-cyan-400 hover:text-cyan-300 transition-colors">
          View Full Archive ({history.length}) →
        </button>
      </div>

      <div className="space-y-4 relative z-10">
        {history.length === 0 ? (
          <div className="p-12 text-center border border-white/5 rounded-[2rem] bg-white/[0.01]">
            <p className="text-zinc-500 text-sm font-bold uppercase tracking-widest">No intelligence runs detected in telemetry.</p>
          </div>
        ) : (
          history.map((item) => (
            <div key={item.id} className="flex items-center gap-6 p-6 rounded-[2rem] bg-white/[0.03] border border-white/10 hover:bg-white/[0.05] transition-all group cursor-pointer shadow-2xl relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              
              <div className="w-16 h-16 rounded-2xl bg-cyan-500/10 flex items-center justify-center text-cyan-400 font-mono text-base font-black border border-cyan-500/20 group-hover:scale-105 transition-transform shrink-0 relative z-10 shadow-inner">
                {item.ticket_id.split('-').pop()}
              </div>
              <div className="flex-1 min-w-0 relative z-10">
                <h4 className="text-lg font-black text-white/95 tracking-tight truncate">Intelligence Run {item.ticket_id}</h4>
                <div className="flex items-center gap-4 mt-2">
                  <span className="text-[10px] font-black text-cyan-400 uppercase tracking-[0.2em]">{item.category}</span>
                  <span className="w-1 h-1 rounded-full bg-zinc-700" />
                  <span className="text-[11px] text-zinc-400 font-bold uppercase tracking-wider">
                    {formatTimeAgo(item.created_at)}
                  </span>
                </div>
              </div>
              <div className="text-right flex flex-col items-end gap-2 shrink-0 relative z-10">
                <span className={`text-[10px] font-black px-4 py-1.5 rounded-full border tracking-[0.2em] ${
                  item.outcome === 'escalated' 
                    ? 'bg-red-500/15 text-red-400 border-red-500/30' 
                    : 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30'
                }`}>
                  {(item.outcome || 'resolved').toUpperCase()}
                </span>
                <span className="text-[11px] font-mono font-black text-zinc-500">
                  {(item.confidence * 100).toFixed(0)}% CONF
                </span>
              </div>
            </div>
          ))
        )}
      </div>
    </HoverBorderCard>
  );
};

export default History;
