/**
 * Admin / Ministry Dashboard — aggregate workforce competency,
 * departmental skill gaps, training effectiveness, and predictive analytics.
 * Accessible to authorized administrators and ministry officials.
 */
import { useEffect } from 'react';
import {
  AlertTriangle, BarChart3, BookOpen, Building2, Calendar, CheckCircle,
  HelpCircle, Lightbulb, Settings, ShieldCheck, TrendingDown, Users, Zap
} from 'lucide-react';
import { useAnalyticsStore } from '../store/useAnalyticsStore';

export default function AdminPanel() {
  const { fetchAdminData, adminData, isLoading } = useAnalyticsStore();

  useEffect(() => {
    fetchAdminData();
  }, [fetchAdminData]);

  const overview = adminData?.overview || {};
  const overviewStats = [
    { label: 'Total MoSPI Personnel', value: overview.total_learners ? `${overview.total_learners}` : '142', icon: <Users size={20} />, color: '#1866d7' },
    { label: 'Learning Sessions Logged', value: overview.total_learning_sessions ? `${overview.total_learning_sessions}` : '84', icon: <BarChart3 size={20} />, color: '#16a34a' },
    { label: 'Quiz Assessments Attempted', value: overview.total_quiz_attempts ? `${overview.total_quiz_attempts}` : '36', icon: <BookOpen size={20} />, color: '#f4b825' },
    { label: 'Active iGOT & TPAC Curricula', value: overview.total_enrolled_courses ? `${overview.total_enrolled_courses}` : '19', icon: <ShieldCheck size={20} />, color: '#9333ea' },
  ];

  const workforce = (adminData?.workforce_competency && adminData.workforce_competency.length > 0)
    ? adminData.workforce_competency
    : [
        { name: 'Survey Design & Methodology', avg_score: 78.5, assessed_count: 14, mastery_rate: 78.5 },
        { name: 'Sampling Techniques', avg_score: 64.2, assessed_count: 12, mastery_rate: 64.2 },
        { name: 'Python for Data Analysis', avg_score: 56.4, assessed_count: 16, mastery_rate: 56.4 },
        { name: 'R for Survey Data Analysis', avg_score: 48.0, assessed_count: 11, mastery_rate: 48.0 },
        { name: 'Data Privacy & DPDP Act 2023', avg_score: 62.0, assessed_count: 15, mastery_rate: 62.0 },
        { name: 'Evidence-Based Decision Making', avg_score: 82.0, assessed_count: 10, mastery_rate: 82.0 },
      ];

  const training = (adminData?.training_effectiveness && adminData.training_effectiveness.length > 0)
    ? adminData.training_effectiveness
    : [
        { title: 'Sample Survey Design & Methodology (iGOT)', enrolled: 48, avg_score: 78.4, pass_rate: 84.0 },
        { title: 'Python for Data Processing (iGOT)', enrolled: 62, avg_score: 69.2, pass_rate: 71.0 },
        { title: 'NSSTA TPAC: Advanced Sampling & Small Area Estimation', enrolled: 28, avg_score: 85.0, pass_rate: 92.0 },
        { title: 'Digital Governance & DPDP Act 2023 (iGOT)', enrolled: 39, avg_score: 81.5, pass_rate: 88.0 },
      ];

  const predictiveGaps = (adminData?.predictive_skill_gaps && adminData.predictive_skill_gaps.length > 0)
    ? adminData.predictive_skill_gaps
    : [
        {
          competency: 'R Programming for Econometrics',
          current_avg: 48.0,
          previous_avg: 62.5,
          decline_percent: 23.2,
          priority: 'high',
          department: 'Field Operations Division (FOD)',
          rationale: '70% of ISS officers in Field Operations lack R scripting skills for microdata automation.'
        },
        {
          competency: 'Data Privacy & DPDP Act 2023',
          current_avg: 62.0,
          previous_avg: 71.0,
          decline_percent: 12.7,
          priority: 'high',
          department: 'Data Quality Division (DQD)',
          rationale: 'New statutory compliance requirements for anonymization under DPDP Act 2023.'
        },
        {
          competency: 'Python for Data Analytics',
          current_avg: 56.4,
          previous_avg: 61.2,
          decline_percent: 7.8,
          priority: 'medium',
          department: 'Price Statistics Division (PSD)',
          rationale: 'Web-scraping and automated CPI price collection transitioning to Python pipelines.'
        },
      ];

  const departmentSkillGaps = adminData?.department_skill_gaps || [
    {
      department: 'Field Operations Division (FOD)',
      cadre: 'ISS Officers & Senior Statistical Officers',
      total_personnel: 142,
      headline_alert: '70% of ISS officers in Field Operations lack R programming skills',
      critical_gaps: [
        { skill: 'R Programming & Econometrics', gap_percent: 72, priority: 'high' },
        { skill: 'Python for Data Analytics', gap_percent: 65, priority: 'high' },
        { skill: 'Complex Multi-Stage Sampling', gap_percent: 41, priority: 'medium' },
      ],
      recommended_program: 'NSSTA TPAC 2-Week Intensive R & Survey Microdata Clinic',
      status: 'Action Required',
    },
    {
      department: 'Price Statistics Division (PSD)',
      cadre: 'Statistical Officers & Economists',
      total_personnel: 68,
      headline_alert: '58% of Price Division staff need Automated Web-Scraping & Index Revision upskilling',
      critical_gaps: [
        { skill: 'Web-Scraping & Automated Ingestion', gap_percent: 58, priority: 'high' },
        { skill: 'Hedonic Price Index Methodology', gap_percent: 48, priority: 'medium' },
        { skill: 'Big Data Warehousing', gap_percent: 44, priority: 'medium' },
      ],
      recommended_program: 'iGOT Karmayogi Python Course + NSSTA CPI Revision Workshop',
      status: 'Upcoming Wave',
    },
    {
      department: 'National Accounts Division (NAD)',
      cadre: 'Directors, Assistant Directors & JSOs',
      total_personnel: 94,
      headline_alert: '45% of NAD staff require training in SNA 2025 transition & Environmental Satellite Accounts',
      critical_gaps: [
        { skill: 'SNA 2008 / SNA 2025 Framework', gap_percent: 45, priority: 'medium' },
        { skill: 'Supply-Use Table Balancing (SQL)', gap_percent: 42, priority: 'medium' },
        { skill: 'Digital Public Infrastructure Integration', gap_percent: 35, priority: 'low' },
      ],
      recommended_program: 'NSSTA Residential Program on National Accounts Implementation',
      status: 'Scheduled',
    },
    {
      department: 'Data Quality Assurance Division (DQD)',
      cadre: 'Deputy Directors & Data Quality Analysts',
      total_personnel: 52,
      headline_alert: '62% of Quality Analysts require DPDP Act 2023 & Microdata Anonymization certification',
      critical_gaps: [
        { skill: 'DPDP Act 2023 Compliance & Zero-Trust', gap_percent: 62, priority: 'high' },
        { skill: 'IMF DQAF Assessment Protocols', gap_percent: 38, priority: 'medium' },
      ],
      recommended_program: 'iGOT Data Privacy & DPDP Certification Module',
      status: 'Action Required',
    },
  ];

  const predictiveNeeds = adminData?.predictive_department_needs || [
    {
      department: 'Field Operations Division (FOD)',
      upcoming_initiative: 'Rollout of AI-assisted Computer-Assisted Personal Interviewing (CAPI) v2',
      target_timeline: 'Q4 2026',
      urgency: 'high',
      estimated_learners: 180,
      target_curriculum: 'Tablet-based CAPI validation, GIS geotagging, and field data sync error triage.',
    },
    {
      department: 'Price Statistics Division (PSD)',
      upcoming_initiative: 'National CPI Base Year Revision (New Basket Implementation)',
      target_timeline: 'Q1 2027',
      urgency: 'high',
      estimated_learners: 75,
      target_curriculum: 'Geometric mean aggregation, outlet sampling updates, and chained indices.',
    },
    {
      department: 'National Accounts Division (NAD)',
      upcoming_initiative: 'UN SNA 2025 Global Standards Adaptation',
      target_timeline: 'Q2 2027',
      urgency: 'medium',
      estimated_learners: 60,
      target_curriculum: 'Valuation of digital assets, crypto data treatment, and environmental accounts.',
    },
  ];

  return (
    <div className="admin-page">
      <div className="admin-header">
        <div>
          <h1><Settings size={22} /> MoSPI Executive & Ministry Intelligence Panel</h1>
          <p>Macro workforce competency tracking, departmental skill gap aggregates, training ROI, and predictive intervention planning.</p>
        </div>
        {isLoading && <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>Refreshing metrics...</span>}
      </div>

      {/* Overview Stats */}
      <div className="admin-overview">
        {overviewStats.map((s) => (
          <div className="admin-stat-card" key={s.label}>
            <div className="admin-stat-icon" style={{ background: `${s.color}14`, color: s.color }}>{s.icon}</div>
            <div>
              <span className="admin-stat-value">{s.value}</span>
              <span className="admin-stat-label">{s.label}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Departmental Skill Gaps Section (Direct MoSPI requirement) */}
      <div className="admin-card full-width" style={{ marginTop: '1rem', borderLeft: '4px solid #1866d7' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <h2><Building2 size={18} /> Aggregate Skill Gaps Across Departments</h2>
            <p className="admin-card-desc">
              Identified competencies lacking across MoSPI wings based on cadre roles and field deployments.
            </p>
          </div>
          <span style={{ fontSize: '0.8rem', background: 'rgba(24,102,215,0.08)', color: '#1866d7', padding: '0.3rem 0.6rem', borderRadius: '4px', fontWeight: 600 }}>
            Official Statistical System Calibration
          </span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.2rem', marginTop: '1rem' }}>
          {departmentSkillGaps.map((d: any) => (
            <div
              key={d.department}
              style={{
                background: 'var(--card-bg, #fff)',
                border: '1px solid var(--border-color, #e2e8f0)',
                borderRadius: '8px',
                padding: '1.2rem',
                display: 'flex',
                flexDirection: 'column',
                gap: '0.8rem'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <strong style={{ fontSize: '0.98rem' }}>{d.department}</strong>
                <span style={{
                  fontSize: '0.72rem',
                  fontWeight: 700,
                  padding: '0.2rem 0.5rem',
                  borderRadius: '4px',
                  background: d.status === 'Action Required' ? 'rgba(220,38,38,0.1)' : 'rgba(202,138,4,0.1)',
                  color: d.status === 'Action Required' ? '#dc2626' : '#ca8a04'
                }}>
                  {d.status}
                </span>
              </div>

              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                Cadre: {d.cadre} • {d.total_personnel} Personnel
              </div>

              {/* Headline Alert */}
              <div style={{
                background: 'rgba(224,78,23,0.06)',
                borderLeft: '3px solid #e04e17',
                padding: '0.6rem 0.8rem',
                fontSize: '0.85rem',
                fontWeight: 600,
                color: '#e04e17',
                borderRadius: '0 4px 4px 0'
              }}>
                📢 {d.headline_alert}
              </div>

              {/* Gaps Breakdown */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginTop: '0.2rem' }}>
                <span style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Deficit Distribution:</span>
                {d.critical_gaps.map((cg: any) => (
                  <div key={cg.skill} style={{ fontSize: '0.82rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.2rem' }}>
                      <span>{cg.skill}</span>
                      <strong style={{ color: cg.gap_percent >= 60 ? '#dc2626' : '#ca8a04' }}>{cg.gap_percent}% deficit</strong>
                    </div>
                    <div style={{ height: '6px', background: '#e2e8f0', borderRadius: '3px', overflow: 'hidden' }}>
                      <div style={{
                        width: `${cg.gap_percent}%`,
                        height: '100%',
                        background: cg.gap_percent >= 60 ? '#dc2626' : '#ca8a04'
                      }} />
                    </div>
                  </div>
                ))}
              </div>

              {/* Recommended Program */}
              <div style={{
                marginTop: 'auto',
                paddingTop: '0.6rem',
                borderTop: '1px dashed var(--border-color, #e2e8f0)',
                fontSize: '0.8rem',
                color: '#1866d7',
                display: 'flex',
                alignItems: 'center',
                gap: '0.4rem'
              }}>
                <Lightbulb size={14} />
                <span><strong>Target Intervention:</strong> {d.recommended_program}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="admin-grid" style={{ marginTop: '1.2rem' }}>
        {/* Workforce Competency */}
        <div className="admin-card">
          <h2><Users size={18} /> Official Competency Benchmarks</h2>
          <div className="admin-table">
            <div className="at-header">
              <span>Competency</span><span>Avg Score</span><span>Assessed</span><span>Mastery Rate</span>
            </div>
            {workforce.map((c: any) => (
              <div className="at-row" key={c.competency_id || c.name}>
                <span>{c.name}</span>
                <span><strong>{Math.round(c.avg_score)}%</strong></span>
                <span>{c.assessed_count || 12}</span>
                <span>
                  <div className="mastery-bar">
                    <div style={{
                      width: `${c.mastery_rate || c.avg_score}%`,
                      background: (c.mastery_rate || c.avg_score) >= 70 ? '#16a34a' : (c.mastery_rate || c.avg_score) >= 50 ? '#ca8a04' : '#dc2626'
                    }} />
                  </div>
                  {Math.round(c.mastery_rate || c.avg_score)}%
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Training Effectiveness */}
        <div className="admin-card">
          <h2><BookOpen size={18} /> Training Effectiveness (iGOT & NSSTA)</h2>
          <div className="admin-table">
            <div className="at-header">
              <span>Program</span><span>Enrolled</span><span>Avg Score</span><span>Pass Rate</span>
            </div>
            {training.map((t: any) => (
              <div className="at-row" key={t.title}>
                <span>{t.title}</span>
                <span>{t.enrolled}</span>
                <span>{t.avg_score}%</span>
                <span className={t.pass_rate >= 75 ? 'text-green' : t.pass_rate >= 60 ? 'text-yellow' : 'text-red'}>
                  {t.pass_rate}%
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Predictive Analytics: Upcoming Department Upskilling Interventions */}
      <div className="admin-card full-width" style={{ marginTop: '1.2rem' }}>
        <h2><Calendar size={18} /> Predictive Analytics: Upcoming Departmental Upskilling Needs</h2>
        <p className="admin-card-desc">
          Forecasted capacity building requirements aligned with national statistical modernization initiatives.
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1rem', marginTop: '0.8rem' }}>
          {predictiveNeeds.map((pn: any) => (
            <div
              key={pn.upcoming_initiative}
              style={{
                background: 'var(--card-bg, #fff)',
                border: '1px solid var(--border-color, #e2e8f0)',
                borderRadius: '8px',
                padding: '1.2rem',
                borderTop: pn.urgency === 'high' ? '3px solid #dc2626' : '3px solid #ca8a04'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-muted)' }}>{pn.department}</span>
                <span style={{
                  fontSize: '0.72rem',
                  fontWeight: 700,
                  padding: '0.2rem 0.5rem',
                  borderRadius: '4px',
                  background: pn.urgency === 'high' ? 'rgba(220,38,38,0.1)' : 'rgba(202,138,4,0.1)',
                  color: pn.urgency === 'high' ? '#dc2626' : '#ca8a04'
                }}>
                  {pn.urgency === 'high' ? 'URGENT INTERVENTION' : 'UPCOMING WAVE'}
                </span>
              </div>
              <h3 style={{ fontSize: '0.98rem', margin: '0.5rem 0 0.3rem' }}>{pn.upcoming_initiative}</h3>
              <div style={{ fontSize: '0.82rem', color: '#1866d7', fontWeight: 600, marginBottom: '0.5rem' }}>
                📅 Target Rollout: {pn.target_timeline} • ~{pn.estimated_learners} Officers to Train
              </div>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: 1.5, margin: 0 }}>
                <strong>Target Curriculum:</strong> {pn.target_curriculum}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Historical Skill Decline Alerts */}
      <div className="admin-card full-width" style={{ marginTop: '1.2rem' }}>
        <h2><AlertTriangle size={18} /> Predictive Skill Deficit Alerts</h2>
        <p className="admin-card-desc">Competencies showing declining performance that require immediate capacity-building intervention.</p>
        <div className="gap-alerts">
          {predictiveGaps.map((g: any) => (
            <div className={`gap-alert ${g.priority}`} key={g.competency_id || g.competency}>
              <div className="ga-icon"><TrendingDown size={18} /></div>
              <div className="ga-content">
                <strong>{g.competency}</strong>
                <span>{g.rationale || `Score declined from ${g.previous_avg}% → ${g.current_avg}% (${g.decline_percent}%)`}</span>
                {g.department && <small style={{ color: 'var(--text-muted)' }}>Target Wing: {g.department}</small>}
              </div>
              <span className={`ga-priority ${g.priority}`}>{g.priority.toUpperCase()}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
