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
    <div className="space-y-6">
      {/* Hero */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl p-8 text-white">
        <h1 className="text-3xl font-bold mb-2">
          Welcome, {user?.username}! 👋
        </h1>
        <p className="text-indigo-100">
          Continue your learning journey. Track your progress, complete courses, and build your skills.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[
          { label: 'Learning Hours', value: '24h', icon: '⏱️' },
          { label: 'Quizzes Taken', value: '12', icon: '📝' },
          { label: 'Courses Enrolled', value: '5', icon: '📚' },
          { label: 'Avg Score', value: '78%', icon: '🎯' },
        ].map(stat => (
          <div key={stat.label} className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500">{stat.label}</p>
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
              </div>
              <span className="text-2xl">{stat.icon}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Skill Gaps */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h3 className="text-lg font-semibold mb-4">🔍 Skill Gaps Identified</h3>
        <div className="space-y-3">
          {['survey_design', 'sampling_methods', 'data_analysis'].map(gap => (
            <div key={gap} className="flex items-center justify-between p-3 bg-amber-50 rounded-lg">
              <span className="text-sm font-medium text-amber-800">
                {gap.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}
              </span>
              <button className="text-sm bg-indigo-600 text-white px-3 py-1 rounded-lg hover:bg-indigo-700">
                Start Learning
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
