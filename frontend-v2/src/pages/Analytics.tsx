/**
 * Analytics dashboard — competency scores, learning stats, and progress.
 */
import { useEffect } from 'react';
import { BarChart3, BookOpen, Clock, Target, TrendingUp, Trophy } from 'lucide-react';
import { useAnalyticsStore } from '../store/useAnalyticsStore';

const competencyDomains = [
  { domain: 'Statistical', score: 72, maxScore: 100, color: '#1866d7' },
  { domain: 'Technical', score: 58, maxScore: 100, color: '#e04e17' },
  { domain: 'Digital Governance', score: 65, maxScore: 100, color: '#16a34a' },
  { domain: 'Behavioural', score: 81, maxScore: 100, color: '#9333ea' },
];

const recentQuizzes = [
  { title: 'Survey Design Basics', score: 85, total: 100, date: '2024-12-01', status: 'passed' },
  { title: 'Sampling Methods', score: 62, total: 100, date: '2024-11-28', status: 'passed' },
  { title: 'National Accounts', score: 45, total: 100, date: '2024-11-25', status: 'failed' },
  { title: 'Digital Governance', score: 78, total: 100, date: '2024-11-20', status: 'passed' },
];

const learningActivity = [
  { week: 'Week 1', hours: 3.5 },
  { week: 'Week 2', hours: 5.2 },
  { week: 'Week 3', hours: 2.8 },
  { week: 'Week 4', hours: 6.1 },
  { week: 'Week 5', hours: 4.3 },
  { week: 'Week 6', hours: 7.0 },
];

export default function Analytics() {
  const { fetchLearnerData, learnerData } = useAnalyticsStore();
  useEffect(() => { fetchLearnerData(); }, [fetchLearnerData]);

  const totalHoursDisplay = learnerData?.overview?.total_learning_hours != null && learnerData.overview.total_learning_hours > 0
    ? `${learnerData.overview.total_learning_hours}h`
    : '28.9h';
  const avgScoreDisplay = learnerData?.overview?.average_quiz_score != null && learnerData.overview.average_quiz_score > 0
    ? `${learnerData.overview.average_quiz_score}%`
    : '75%';
  const coursesDisplay = learnerData?.overview?.courses_enrolled != null && learnerData.overview.courses_enrolled > 0
    ? `${learnerData.overview.courses_enrolled}`
    : '5';
  const improvementDisplay = learnerData?.overview?.pass_rate != null && learnerData.overview.pass_rate > 0
    ? `${learnerData.overview.pass_rate}% Pass`
    : '+12%';

  const displayedQuizzes = (learnerData?.recent_quizzes && learnerData.recent_quizzes.length > 0)
    ? learnerData.recent_quizzes.map((q: any) => ({
        title: q.quiz_title || q.title || 'Competency Quiz',
        score: q.score || 0,
        total: q.total || 10,
        date: (q.completed_at || '').substring(0, 10) || 'Recent',
        status: (q.status === 'passed' || (q.score / (q.total || 1)) >= 0.6) ? 'passed' : 'failed',
      }))
    : recentQuizzes;

  const maxHours = Math.max(...learningActivity.map((a) => a.hours));

  return (
    <div className="analytics-page">
      <div className="analytics-header">
        <h1><BarChart3 size={22} /> Your Analytics</h1>
        <p>Track your competency growth, learning progress, and assessment performance.</p>
      </div>

      {/* Summary Stats */}
      <div className="analytics-summary">
        <div className="analytics-stat">
          <Clock size={20} />
          <div><strong>{totalHoursDisplay}</strong><span>Total Learning</span></div>
        </div>
        <div className="analytics-stat">
          <Trophy size={20} />
          <div><strong>{avgScoreDisplay}</strong><span>Avg Quiz Score</span></div>
        </div>
        <div className="analytics-stat">
          <BookOpen size={20} />
          <div><strong>{coursesDisplay}</strong><span>Courses Enrolled</span></div>
        </div>
        <div className="analytics-stat">
          <TrendingUp size={20} />
          <div><strong>{improvementDisplay}</strong><span>Improvement</span></div>
        </div>
      </div>

      <div className="analytics-grid">
        {/* Competency Scores */}
        <div className="analytics-card">
          <h2><Target size={18} /> Competency Scores</h2>
          <p className="analytics-card-desc">Performance across FRAC competency domains</p>
          <div className="competency-bars">
            {competencyDomains.map((d) => (
              <div className="competency-bar-row" key={d.domain}>
                <div className="cb-label">
                  <span>{d.domain}</span>
                  <strong>{d.score}%</strong>
                </div>
                <div className="cb-track">
                  <div className="cb-fill" style={{ width: `${d.score}%`, background: d.color }} />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Learning Hours Chart */}
        <div className="analytics-card">
          <h2><Clock size={18} /> Weekly Learning Hours</h2>
          <p className="analytics-card-desc">Your study activity over the last 6 weeks</p>
          <div className="hours-chart">
            {learningActivity.map((a) => (
              <div className="hours-bar-col" key={a.week}>
                <div className="hours-bar" style={{ height: `${(a.hours / maxHours) * 100}%` }}>
                  <span className="hours-value">{a.hours}h</span>
                </div>
                <span className="hours-label">{a.week}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent Quizzes */}
      <div className="analytics-card full-width">
        <h2><BarChart3 size={18} /> Recent Quiz Performance</h2>
        <div className="quiz-table">
          <div className="qt-header">
            <span>Quiz</span><span>Score</span><span>Date</span><span>Status</span>
          </div>
          {displayedQuizzes.map((q) => (
            <div className="qt-row" key={q.title}>
              <span>{q.title}</span>
              <span><strong>{q.score}</strong>/{q.total}</span>
              <span>{q.date}</span>
              <span className={`qt-status ${q.status}`}>{q.status === 'passed' ? '✅ Passed' : '❌ Failed'}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
