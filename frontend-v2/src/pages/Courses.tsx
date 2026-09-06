/**
 * Course catalog & AI Personalized Learning Pathway page.
 * Integrates live iGOT Karmayogi micro-learning courses and NSSTA TPAC training calendar.
 */
import { useEffect, useState } from 'react';
import {
  ArrowRight, BookOpen, Calendar, Check, Clock, Filter,
  Layers, RefreshCw, Search, Sparkles, Star, Users
} from 'lucide-react';
import toast from 'react-hot-toast';
import * as api from '../lib/api';

const domains = ['all', 'statistical', 'technical', 'digital_governance', 'behavioural'];
const sources = [
  { id: 'all', label: 'All Sources' },
  { id: 'igot', label: 'iGOT Karmayogi' },
  { id: 'tpac', label: 'NSSTA TPAC (Cohort/Residential)' },
];

const difficultyColor: Record<string, string> = {
  Beginner: '#16a34a',
  Intermediate: '#ca8a04',
  Advanced: '#dc2626',
};

const sourceLabel: Record<string, string> = {
  igot: 'iGOT Karmayogi (Micro-learning)',
  tpac: 'NSSTA TPAC (Institutional)',
  local: 'Internal MoSPI',
};

export default function Courses() {
  const [courses, setCourses] = useState<any[]>([]);
  const [enrolledIds, setEnrolledIds] = useState<Set<string>>(new Set());
  const [search, setSearch] = useState('');
  const [domain, setDomain] = useState('all');
  const [source, setSource] = useState('all');
  const [loading, setLoading] = useState(true);

  // AI Pathway state
  const [pathway, setPathway] = useState<any>(null);
  const [loadingPathway, setLoadingPathway] = useState(false);
  const [activeTab, setActiveTab] = useState<'catalog' | 'pathway'>('catalog');
  const [gapReport, setGapReport] = useState<string>('');

  useEffect(() => {
    loadCourses();
    loadEnrolled();
    loadPathway();
  }, []);

  const loadCourses = async () => {
    try {
      setLoading(true);
      const data = await api.getCourses();
      setCourses(data);
    } catch (e: any) {
      console.error('Error fetching courses:', e);
    } finally {
      setLoading(false);
    }
  };

  const loadEnrolled = async () => {
    try {
      const data = await api.getEnrolledCourses();
      const ids = new Set<string>(data.map((c: any) => c.id));
      setEnrolledIds(ids);
    } catch (e) {
      console.warn('Could not load enrolled courses:', e);
    }
  };

  const loadPathway = async () => {
    try {
      setLoadingPathway(true);
      const gapsData = await api.getMyGaps();
      if (gapsData?.gap_report) {
        setGapReport(gapsData.gap_report);
      }
      const plan = await api.generatePlan({
        designation: gapsData?.designation || 'Statistical Officer',
        profile_text: gapsData?.gap_report || 'Official requiring competency progression.',
        department: gapsData?.department || 'Field Operations Division (FOD)',
      });
      setPathway(plan?.pathway);
    } catch (e: any) {
      console.warn('Could not auto-generate pathway:', e);
    } finally {
      setLoadingPathway(false);
    }
  };

  const handleEnroll = async (courseId: string, courseTitle: string) => {
    try {
      await api.enrollInCourse(courseId);
      setEnrolledIds((prev) => new Set([...prev, courseId]));
      toast.success(`Enrolled in ${courseTitle}!`);
    } catch (e: any) {
      toast.error(e.message || 'Enrollment failed');
    }
  };

  const filtered = courses.filter((c) => {
    const matchSearch =
      c.title.toLowerCase().includes(search.toLowerCase()) ||
      c.description.toLowerCase().includes(search.toLowerCase()) ||
      (c.skills || []).some((s: string) => s.toLowerCase().includes(search.toLowerCase()));
    const matchDomain = domain === 'all' || c.domain === domain;
    const matchSource = source === 'all' || c.source === source;
    return matchSearch && matchDomain && matchSource;
  });

  return (
    <div className="courses-page">
      {/* Header */}
      <div className="courses-header">
        <div>
          <h1><BookOpen size={22} /> MoSPI Learning & Training Catalog</h1>
          <p>Integrated official repository of iGOT Karmayogi digital courses and NSSTA TPAC calendar workshops.</p>
        </div>
        <div style={{ display: 'flex', gap: '0.6rem', alignItems: 'center' }}>
          <button
            className={`secondary-button ${activeTab === 'pathway' ? 'active-tab' : ''}`}
            onClick={() => setActiveTab(activeTab === 'pathway' ? 'catalog' : 'pathway')}
            style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}
          >
            <Sparkles size={16} color="#e04e17" />
            {activeTab === 'pathway' ? 'Show All Courses' : 'My AI Pathway'}
          </button>
          <span className="courses-count">{filtered.length} programs</span>
        </div>
      </div>

      {/* AI Recommendation Pathway Banner */}
      {activeTab === 'pathway' && (
        <div className="ai-pathway-banner" style={{
          background: 'linear-gradient(135deg, rgba(24,102,215,0.08) 0%, rgba(224,78,23,0.08) 100%)',
          border: '1px solid var(--accent, #1866d7)',
          borderRadius: '12px',
          padding: '1.5rem',
          marginBottom: '2rem'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#1866d7', fontWeight: 600, fontSize: '0.85rem' }}>
                <Sparkles size={16} /> PERSONALIZED HYBRID RECOMMENDATION (AI/ML ENGINE)
              </div>
              <h2 style={{ fontSize: '1.3rem', margin: '0.4rem 0 0.2rem' }}>Your Calibrated Capacity Building Pathway</h2>
              {gapReport && (
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', maxWidth: '800px', margin: '0.3rem 0 0.8rem' }}>
                  <strong>Diagnostic Gap Report:</strong> {gapReport}
                </p>
              )}
            </div>
            <button
              className="soft-button"
              onClick={loadPathway}
              disabled={loadingPathway}
              style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}
            >
              <RefreshCw size={14} className={loadingPathway ? 'spin' : ''} />
              {loadingPathway ? 'Recalibrating...' : 'Refresh Pathway'}
            </button>
          </div>

          {pathway?.suggested_pathway && (
            <div style={{
              background: 'var(--card-bg, #fff)',
              padding: '1.2rem',
              borderRadius: '8px',
              margin: '1rem 0',
              border: '1px solid var(--border-color, #e2e8f0)',
              fontSize: '0.92rem',
              lineHeight: 1.6,
              whiteSpace: 'pre-line'
            }}>
              {pathway.suggested_pathway}
            </div>
          )}

          {/* Recommended Cards */}
          <div style={{ marginTop: '1.2rem' }}>
            <h3 style={{ fontSize: '1rem', marginBottom: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <Layers size={16} /> Recommended Curricula for Immediate Enrollment:
            </h3>
            <div className="courses-grid">
              {[...(pathway?.courses || []), ...(pathway?.tpac_programs || [])].map((course: any) => (
                <div className="course-card" key={course.id} style={{ borderLeft: '4px solid #1866d7' }}>
                  <div className="course-card-top">
                    <span className="course-domain">{course.domain || 'Statistical'}</span>
                    <span className="course-source">{sourceLabel[course.source] || course.source}</span>
                  </div>
                  <h3>{course.title}</h3>
                  <p>{course.description}</p>
                  {course.schedule_info && (
                    <div style={{ fontSize: '0.8rem', color: '#e04e17', fontWeight: 600, margin: '0.4rem 0', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                      <Calendar size={13} /> {course.schedule_info}
                    </div>
                  )}
                  {course.eligibility && (
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                      <Users size={12} /> Eligible: {course.eligibility}
                    </div>
                  )}
                  <div className="course-meta">
                    <span><Clock size={13} /> {course.duration_hours}h</span>
                    <span style={{ color: difficultyColor[course.difficulty] || '#ca8a04' }}>
                      <Star size={13} /> {course.difficulty}
                    </span>
                  </div>
                  <button
                    className={`course-enroll ${enrolledIds.has(course.id) ? 'enrolled' : ''}`}
                    onClick={() => handleEnroll(course.id, course.title)}
                    disabled={enrolledIds.has(course.id)}
                  >
                    {enrolledIds.has(course.id) ? (
                      <><Check size={14} /> Enrolled</>
                    ) : (
                      <>Enroll in Program <ArrowRight size={14} /></>
                    )}
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="courses-filters">
        <div className="search-wrap">
          <Search size={16} />
          <input
            type="text"
            placeholder="Search competencies, tools (Python, R, Sampling), or courses..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        {/* Source Toggle */}
        <div className="domain-filters" style={{ flexWrap: 'wrap' }}>
          {sources.map((s) => (
            <button
              key={s.id}
              className={source === s.id ? 'active' : ''}
              onClick={() => setSource(s.id)}
            >
              {s.label}
            </button>
          ))}
        </div>

        {/* Domain Filter */}
        <div className="domain-filters">
          <Filter size={14} />
          {domains.map((d) => (
            <button
              key={d}
              className={domain === d ? 'active' : ''}
              onClick={() => setDomain(d)}
            >
              {d === 'all' ? 'All Domains' : d.replace('_', ' ').replace(/\b\w/g, (c) => c.toUpperCase())}
            </button>
          ))}
        </div>
      </div>

      {/* Course Grid */}
      {loading ? (
        <div className="courses-empty">
          <RefreshCw size={36} className="spin" />
          <h3>Loading MoSPI course catalog...</h3>
        </div>
      ) : (
        <div className="courses-grid">
          {filtered.map((course) => {
            const isEnrolled = enrolledIds.has(course.id);
            const isTPAC = course.source === 'tpac';

            return (
              <div className="course-card" key={course.id}>
                <div className="course-card-top">
                  <span className="course-domain">{course.domain.replace('_', ' ')}</span>
                  <span className={`course-source ${isTPAC ? 'tpac-badge' : ''}`}>
                    {isTPAC ? '🏛️ NSSTA TPAC' : '🌐 iGOT Karmayogi'}
                  </span>
                </div>
                <h3>{course.title}</h3>
                <p>{course.description}</p>

                {course.schedule_info && (
                  <div style={{
                    fontSize: '0.8rem',
                    color: isTPAC ? '#e04e17' : '#1866d7',
                    fontWeight: 600,
                    margin: '0.4rem 0',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.3rem'
                  }}>
                    <Calendar size={13} /> {course.schedule_info}
                  </div>
                )}

                {course.eligibility && (
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                    <Users size={12} /> {course.eligibility}
                  </div>
                )}

                <div className="course-meta">
                  <span><Clock size={13} /> {course.duration_hours}h</span>
                  <span style={{ color: difficultyColor[course.difficulty] || '#ca8a04' }}>
                    <Star size={13} /> {course.difficulty}
                  </span>
                </div>

                <div className="course-skills">
                  {(course.skills || []).map((s: string) => (
                    <span key={s} className="skill-tag">{s}</span>
                  ))}
                </div>

                <button
                  className={`course-enroll ${isEnrolled ? 'enrolled' : ''}`}
                  onClick={() => handleEnroll(course.id, course.title)}
                  disabled={isEnrolled}
                >
                  {isEnrolled ? (
                    <><Check size={14} /> Enrolled</>
                  ) : (
                    <>Enroll Now <ArrowRight size={14} /></>
                  )}
                </button>
              </div>
            );
          })}
        </div>
      )}

      {!loading && filtered.length === 0 && (
        <div className="courses-empty">
          <BookOpen size={40} />
          <h3>No courses match your filter criteria</h3>
          <p>Try searching for other competencies or clear the domain filter.</p>
        </div>
      )}
    </div>
  );
}
