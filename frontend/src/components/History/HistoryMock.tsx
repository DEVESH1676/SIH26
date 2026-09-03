import React from "react";

const mockHistory = [
  { id: "T-1001", subject: "VPN connection drops", category: "Network", confidence: 0.89, status: "Resolved", date: "2 mins ago" },
  { id: "T-1002", subject: "Access denied to database", category: "Security", confidence: 0.94, status: "Auto-Resolved", date: "15 mins ago" },
  { id: "T-1003", subject: "Slow application response", category: "Infrastructure", confidence: 0.42, status: "Escalated", date: "1 hour ago" },
  { id: "T-1004", subject: "Password reset request", category: "Access", confidence: 0.98, status: "Resolved", date: "2 hours ago" },
];

const HistoryMock: React.FC = () => {
  return (
    <div className="glass rounded-3xl p-6 overflow-hidden">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold tracking-tight text-white/90">Recent Run History</h2>
        <button className="text-xs font-semibold text-cyan-400 hover:text-cyan-300 transition-colors">
          View Full Archive →
        </button>
      </div>

      <div className="space-y-4">
        {mockHistory.map((item) => (
          <div key={item.id} className="flex items-center gap-6 p-6 rounded-[2rem] bg-white/[0.03] border border-white/10 hover:bg-white/[0.05] transition-all group cursor-pointer shadow-2xl relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
            
            <div className="w-16 h-16 rounded-2xl bg-cyan-500/10 flex items-center justify-center text-cyan-400 font-mono text-base font-black border border-cyan-500/20 group-hover:scale-105 transition-transform shrink-0 relative z-10 shadow-inner">
              {item.id.split('-')[1]}
            </div>
            <div className="flex-1 min-w-0 relative z-10">
              <h4 className="text-lg font-black text-white/95 tracking-tight truncate">{item.subject}</h4>
              <div className="flex items-center gap-4 mt-2">
                <span className="text-[10px] font-black text-cyan-400 uppercase tracking-[0.2em]">{item.category}</span>
                <span className="w-1 h-1 rounded-full bg-zinc-700" />
                <span className="text-[11px] text-zinc-400 font-bold uppercase tracking-wider">{item.date}</span>
              </div>
            </div>
            <div className="text-right flex flex-col items-end gap-2 shrink-0 relative z-10">
              <span className={`text-[10px] font-black px-4 py-1.5 rounded-full border tracking-[0.2em] ${
                item.status === 'Escalated' 
                  ? 'bg-red-500/15 text-red-400 border-red-500/30' 
                  : 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30'
              }`}>
                {item.status.toUpperCase()}
              </span>
              <span className="text-[11px] font-mono font-black text-zinc-500">
                {(item.confidence * 100).toFixed(0)}% CONF
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HistoryMock;
