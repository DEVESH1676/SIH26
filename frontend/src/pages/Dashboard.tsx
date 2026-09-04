/**
 * Learner dashboard — replaces the old IT ticket dashboard.
 */
import { useEffect } from 'react';
import { useAuthStore } from '../store/useAuthStore';
import { useAnalyticsStore } from '../store/useAnalyticsStore';
import { useTranslation } from 'react-i18next';
import VirtualAssistant from '../components/Assistant/VirtualAssistant';

export default function Dashboard() {
  const { user } = useAuthStore();
  const { fetchLearnerData } = useAnalyticsStore();
  const { t } = useTranslation();

  useEffect(() => { fetchLearnerData(); }, [fetchLearnerData]);

  return (
    <div className="space-y-8 animate-in fade-in duration-500 relative z-10">
      {/* Hero */}
      <div className="relative overflow-hidden rounded-3xl glass p-10 border border-white/10 shadow-2xl">
        <div className="absolute top-0 right-0 p-12 opacity-30 pointer-events-none">
          <div className="w-64 h-64 bg-[var(--primary)] rounded-full blur-[100px]"></div>
        </div>
        
        <div className="relative z-10">
          <h1 className="text-4xl font-black mb-3 bg-clip-text text-transparent bg-gradient-to-r from-white to-white/70">
            Welcome back, {user?.username}! 👋
          </h1>
          <p className="text-[var(--text-muted)] text-lg max-w-2xl font-medium tracking-wide">
            Your learning journey continues. Dive back into your courses, conquer skill gaps, and level up your competency profile.
          </p>
          
          <button className="mt-8 bg-white/10 hover:bg-white/20 text-white border border-white/20 px-6 py-3 rounded-xl font-semibold transition-all duration-300 backdrop-blur-md">
            Resume Last Course
          </button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {[
          { label: 'Learning Hours', value: '24h', icon: '⏱️', glow: 'from-blue-500 to-cyan-500' },
          { label: 'Quizzes Taken', value: '12', icon: '📝', glow: 'from-purple-500 to-pink-500' },
          { label: 'Courses Enrolled', value: '5', icon: '📚', glow: 'from-green-500 to-emerald-500' },
          { label: 'Avg Score', value: '78%', icon: '🎯', glow: 'from-orange-500 to-yellow-500' },
        ].map(stat => (
          <div key={stat.label} className="relative group rounded-2xl glass p-6 border border-white/10 hover:border-white/20 transition-all duration-300 overflow-hidden">
            <div className={`absolute -right-4 -top-4 w-24 h-24 bg-gradient-to-br ${stat.glow} rounded-full blur-[40px] opacity-20 group-hover:opacity-40 transition-opacity`}></div>
            
            <div className="relative z-10 flex flex-col gap-2">
              <span className="text-3xl mb-2">{stat.icon}</span>
              <p className="text-sm font-semibold tracking-wider uppercase text-[var(--text-muted)]">{stat.label}</p>
              <p className="text-3xl font-black text-white">{stat.value}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Skill Gaps */}
      <div className="rounded-3xl glass p-8 border border-white/10">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-xl font-black text-white flex items-center gap-2">
              <span>🎯</span> Skill Gaps Identified
            </h3>
            <p className="text-sm text-[var(--text-muted)] mt-1">Focus on these areas to improve your FRAC competency score.</p>
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {['survey_design', 'sampling_methods', 'data_analysis'].map(gap => (
            <div key={gap} className="flex flex-col justify-between p-5 bg-white/5 border border-white/10 rounded-2xl hover:bg-white/10 transition-colors group">
              <div className="flex items-start justify-between mb-4">
                <span className="text-lg font-bold text-white capitalize">
                  {gap.replace(/_/g, ' ')}
                </span>
                <span className="bg-red-500/20 text-red-400 text-xs px-2 py-1 rounded-md font-bold border border-red-500/20">Action Required</span>
              </div>
              
              <button className="w-full text-sm font-bold bg-[var(--primary)]/10 text-[var(--primary)] border border-[var(--primary)]/20 px-4 py-2.5 rounded-xl group-hover:bg-[var(--primary)] group-hover:text-black transition-all">
                View Recommendations
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Virtual Assistant */}
      <VirtualAssistant />
    </div>
  );
}
