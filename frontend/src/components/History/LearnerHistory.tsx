import React from 'react';
import HoverBorderCard from '../ui/HoverBorderCard';
import { BookOpen, CheckCircle } from 'lucide-react';

const mockHistory = [
  {
    id: 1,
    type: 'course',
    title: 'Data Privacy in Statistical Systems',
    date: '2026-09-01',
    status: 'completed',
    score: null
  },
  {
    id: 2,
    type: 'quiz',
    title: 'National Accounts Basics Quiz',
    date: '2026-08-28',
    status: 'passed',
    score: 92
  },
  {
    id: 3,
    type: 'course',
    title: 'Python for Data Analysis',
    date: '2026-08-15',
    status: 'in_progress',
    score: null
  }
];

const LearnerHistory: React.FC = () => {
  return (
    <HoverBorderCard className="glass p-6 rounded-2xl h-full border-white/5 relative group overflow-hidden">
      <div className="absolute top-0 right-0 p-4 opacity-10">
        <svg className="w-24 h-24 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>

      <div className="relative z-10 flex flex-col h-full">
        <h3 className="text-[12px] font-black uppercase tracking-widest text-zinc-400 mb-6 flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-blue-500" />
          Learner History
        </h3>

        <div className="space-y-4">
          {mockHistory.map((item) => (
            <div key={item.id} className="flex items-center gap-4 bg-white/5 p-4 rounded-xl border border-white/10 hover:bg-white/10 transition-colors">
              <div className="p-2 rounded-lg bg-black/40">
                {item.type === 'course' ? (
                  <BookOpen className="w-5 h-5 text-cyan-400" />
                ) : (
                  <CheckCircle className="w-5 h-5 text-emerald-400" />
                )}
              </div>
              
              <div className="flex-1">
                <h4 className="text-[13px] font-bold text-white">{item.title}</h4>
                <div className="flex items-center gap-2 mt-1">
                  <span className="text-[10px] text-zinc-500 font-medium">{item.date}</span>
                  <span className="text-[10px] text-zinc-600">•</span>
                  <span className={`text-[10px] uppercase font-black tracking-wider ${
                    item.status === 'completed' || item.status === 'passed' ? 'text-emerald-400' : 'text-blue-400'
                  }`}>
                    {item.status.replace('_', ' ')}
                  </span>
                </div>
              </div>

              {item.score && (
                <div className="text-right">
                  <span className="text-xl font-black text-white">{item.score}</span>
                  <span className="text-[10px] text-zinc-500 font-bold ml-1">%</span>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </HoverBorderCard>
  );
};

export default LearnerHistory;
