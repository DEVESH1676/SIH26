import React, { useEffect, useState } from 'react';
import HoverBorderCard from '../ui/HoverBorderCard';

interface AnalyticsData {
  status: string;
  data: {
    total_learners: number;
    total_assessments: number;
    average_score: number;
    top_skill_gaps: { skill: string; count: number }[];
    completion_rates: { domain: string; rate: number }[];
  };
}

const AdminAnalytics: React.FC = () => {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In a real app, we would fetch from /api/admin/overview
    // For this MVP, we simulate a response
    setTimeout(() => {
      setData({
        status: "success",
        data: {
          total_learners: 124,
          total_assessments: 342,
          average_score: 82.5,
          top_skill_gaps: [
            { skill: "Data Privacy Act 2023", count: 45 },
            { skill: "Python for Big Data", count: 32 },
            { skill: "Survey Methodology", count: 28 },
          ],
          completion_rates: [
            { domain: "Domain", rate: 75 },
            { domain: "Functional", rate: 60 },
            { domain: "Behavioral", rate: 85 },
          ]
        }
      });
      setLoading(false);
    }, 1500);
  }, []);

  return (
    <HoverBorderCard className="glass p-6 rounded-2xl h-full border-white/5 relative group overflow-hidden">
      <div className="absolute top-0 right-0 p-4 opacity-10">
        <svg className="w-24 h-24 text-cyan-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
      </div>

      <div className="relative z-10 flex flex-col h-full">
        <h3 className="text-[12px] font-black uppercase tracking-widest text-zinc-400 mb-6 flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-cyan-500" />
          Workforce Analytics
        </h3>

        {loading ? (
          <div className="flex-1 flex items-center justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-500" />
          </div>
        ) : data ? (
          <div className="space-y-6">
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                <p className="text-[10px] text-zinc-400 uppercase tracking-widest font-black mb-1">Total Learners</p>
                <p className="text-2xl font-black text-white">{data.data.total_learners}</p>
              </div>
              <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                <p className="text-[10px] text-zinc-400 uppercase tracking-widest font-black mb-1">Assessments</p>
                <p className="text-2xl font-black text-white">{data.data.total_assessments}</p>
              </div>
              <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                <p className="text-[10px] text-zinc-400 uppercase tracking-widest font-black mb-1">Avg Score</p>
                <p className="text-2xl font-black text-cyan-400">{data.data.average_score}%</p>
              </div>
            </div>

            <div>
              <p className="text-[10px] text-zinc-400 uppercase tracking-widest font-black mb-3">Top Skill Gaps Detected</p>
              <div className="space-y-2">
                {data.data.top_skill_gaps.map((gap, i) => (
                  <div key={i} className="flex items-center justify-between bg-black/30 px-3 py-2 rounded-lg text-sm border border-white/5">
                    <span className="text-zinc-300 font-medium">{gap.skill}</span>
                    <span className="text-orange-400 font-black text-[11px]">{gap.count} officials</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : null}
      </div>
    </HoverBorderCard>
  );
};

export default AdminAnalytics;
