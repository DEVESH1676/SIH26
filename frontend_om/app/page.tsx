'use client';

import { useState, useEffect, useCallback } from 'react';
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  Cell,
} from 'recharts';
import {
  Shield,
  BookOpen,
  Brain,
  Users,
  BarChart3,
  Award,
  ChevronRight,
  Smartphone,
  QrCode,
  Download,
  CheckCircle2,
  ArrowRight,
  Zap,
  Target,
  TrendingUp,
  LogOut,
  User,
  Clock,
  Building2,
  GraduationCap,
  Loader2,
  Info,
  Menu,
  X,
  Play,
  Star,
  Globe,
} from 'lucide-react';

// ─────────────────────────── TYPES ───────────────────────────
type Screen =
  | 'LOGIN'
  | 'EMPLOYEE_DASHBOARD'
  | 'QUIZ_ACTIVE'
  | 'EVALUATING'
  | 'QUIZ_RESULTS'
  | 'ADMIN_DASHBOARD';

interface Course {
  id: string;
  title: string;
  org: string;
  duration: string;
  domain: string;
  enrolled: boolean;
}

interface Question {
  id: number;
  domain: string;
  scenario: string;
  options: string[];
  correctIndex: number;
}

// ─────────────────────────── DATA ───────────────────────────

const DOMAINS = [
  'Governance & Law',
  'Cybersecurity & Tech',
  'Managerial & Soft Skills',
  'Public Administration',
] as const;

type Domain = (typeof DOMAINS)[number];

const COURSES: Course[] = [
  {
    id: 'course-01',
    title: 'Introduction to Bharatiya Sakshya Adhiniyam, 2023',
    org: 'Karmayogi Bharat',
    duration: '15m 38s',
    domain: 'Governance & Law',
    enrolled: false,
  },
  {
    id: 'course-02',
    title: 'Introduction to Bharatiya Nagarik Suraksha Sanhita, 2023',
    org: 'Karmayogi Bharat',
    duration: '22m 15s',
    domain: 'Governance & Law',
    enrolled: false,
  },
  {
    id: 'course-03',
    title: 'Legal Framework for Lawful Interception',
    org: 'NTIPRIT',
    duration: '34m 20s',
    domain: 'Governance & Law',
    enrolled: false,
  },
  {
    id: 'course-04',
    title: 'Virtual Private Network (VPN) Overview',
    org: 'BSNL',
    duration: '41m 54s',
    domain: 'Cybersecurity & Tech',
    enrolled: false,
  },
  {
    id: 'course-05',
    title: 'Basic of Access and Core Network',
    org: 'BSNL',
    duration: '28m 42s',
    domain: 'Cybersecurity & Tech',
    enrolled: false,
  },
  {
    id: 'course-06',
    title: 'Developing Effective Soft Skills',
    org: 'CRPF',
    duration: '39m 59s',
    domain: 'Managerial & Soft Skills',
    enrolled: false,
  },
  {
    id: 'course-07',
    title: 'e-Ustad: Negotiation Skills',
    org: 'Bureau of Police Research and Development',
    duration: '45m 12s',
    domain: 'Managerial & Soft Skills',
    enrolled: false,
  },
  {
    id: 'course-08',
    title: 'Design Thinking For Excellence In Public Services',
    org: 'Brihat',
    duration: '52m 30s',
    domain: 'Public Administration',
    enrolled: false,
  },
  {
    id: 'course-09',
    title: 'Introduction to Quality Control in FCI',
    org: 'FCI',
    duration: '36m 48s',
    domain: 'Public Administration',
    enrolled: false,
  },
  {
    id: 'course-10',
    title: 'Low Carbon Development: Planning and Modelling',
    org: 'World Bank',
    duration: '1h 05m',
    domain: 'Public Administration',
    enrolled: false,
  },
];

const QUESTIONS: Question[] = [
  // ── Governance & Law (Q1–Q3) ──
  {
    id: 1,
    domain: 'Governance & Law',
    scenario:
      'Under the Bharatiya Sakshya Adhiniyam, 2023 (BSA), electronic records are given specific evidentiary treatment. A district office submits a digitally signed statistical report as evidence in a tribunal. Under BSA, what is the primary provision governing the admissibility of such electronic records?',
    options: [
      'Section 61 — Admissibility of electronic records is not specifically addressed.',
      'Section 57 — Electronic records are admissible only when accompanied by a physical printout certified by a gazetted officer.',
      'Section 63 — Electronic records are admissible as evidence if the conditions regarding reliability and digital signatures are fulfilled.',
      'Section 45 — Only electronic records stored on government servers are admissible.',
    ],
    correctIndex: 2,
  },
  {
    id: 2,
    domain: 'Governance & Law',
    scenario:
      'The Bharatiya Nagarik Suraksha Sanhita (BNSS), 2023 replaces the Code of Criminal Procedure. A statistical officer witnesses data tampering at a government office. Under BNSS, what is the correct procedure for filing a Zero FIR?',
    options: [
      'A Zero FIR can only be filed at the jurisdictional police station where the offense occurred.',
      'A Zero FIR can be filed at any police station regardless of jurisdiction, and it must be transferred to the appropriate station within 15 days.',
      'Zero FIR is not recognized under BNSS — it remains an administrative guideline only.',
      'A Zero FIR requires prior written permission from a Magistrate before being registered.',
    ],
    correctIndex: 1,
  },
  {
    id: 3,
    domain: 'Governance & Law',
    scenario:
      'A government agency intends to lawfully intercept communications as part of a national security investigation. Under the legal framework for lawful interception in India, which authority is empowered to issue an interception order?',
    options: [
      'Any senior police officer of the rank of Inspector or above can authorize interception.',
      'The Home Secretary of the Central or State Government, as specified under Section 69 of the IT Act, 2000 and Rule 419A.',
      'The concerned telecom operator can authorize interception upon receiving a written request.',
      'Only the Supreme Court of India can authorize lawful interception of communications.',
    ],
    correctIndex: 1,
  },
  // ── Cybersecurity & Tech (Q4–Q6) ──
  {
    id: 4,
    domain: 'Cybersecurity & Tech',
    scenario:
      'A statistical field office needs to securely transmit sensitive census microdata from a remote location to the central server over a public internet connection. Which approach best ensures data confidentiality and integrity during transit?',
    options: [
      'Compress the data into a password-protected ZIP file and email it to the central office.',
      'Upload the data to a public cloud storage service and share the link via encrypted email.',
      'Establish a site-to-site VPN tunnel to encrypt all traffic between the field office and the central server.',
      'Use an FTP connection to transfer the files directly to the server IP address.',
    ],
    correctIndex: 2,
  },
  {
    id: 5,
    domain: 'Cybersecurity & Tech',
    scenario:
      'A district office is setting up its network infrastructure. The network engineer needs to connect the local access network to the national backbone. In a telecom context, what is the primary role of the "Core Network" in relation to the "Access Network"?',
    options: [
      'The Core Network provides last-mile connectivity directly to end-user devices.',
      'The Core Network aggregates traffic from multiple Access Networks and routes it to the appropriate destination or internet backbone.',
      'The Core Network and Access Network are interchangeable terms for the same infrastructure.',
      'The Core Network is exclusively used for voice calls while the Access Network handles data.',
    ],
    correctIndex: 1,
  },
  {
    id: 6,
    domain: 'Cybersecurity & Tech',
    scenario:
      'A government data centre experiences a suspected ransomware attack. The IT team notices encrypted files and a ransom note on several servers. What is the most appropriate immediate response according to cybersecurity best practices?',
    options: [
      'Pay the ransom immediately to recover the encrypted data before the deadline.',
      'Isolate affected systems from the network, preserve forensic evidence, notify CERT-In, and begin restoring from verified clean backups.',
      'Format all affected servers and reinstall the operating systems to remove the malware.',
      'Shut down the entire data centre including unaffected systems to prevent further spread.',
    ],
    correctIndex: 1,
  },
  // ── Managerial & Soft Skills (Q7–Q8) ──
  {
    id: 7,
    domain: 'Managerial & Soft Skills',
    scenario:
      'You are a Deputy Director managing a cross-functional statistical survey team. A senior colleague openly challenges your methodology in a meeting, leading to visible discomfort among junior staff. What is the most effective response?',
    options: [
      'Dismiss the criticism and assert your authority as the project lead.',
      'Acknowledge their perspective calmly, propose a follow-up discussion with data, and check in privately with affected team members.',
      'Escalate the matter to your supervisor immediately after the meeting.',
      'Ignore the interruption completely and continue presenting as if nothing happened.',
    ],
    correctIndex: 1,
  },
  {
    id: 8,
    domain: 'Managerial & Soft Skills',
    scenario:
      'During a multi-stakeholder budget negotiation, the finance department insists on a 30% cut to your survey operations budget. Your field teams require at minimum 85% of the current allocation. Using principled negotiation, what is the most effective strategy?',
    options: [
      'Accept the 30% cut to maintain a positive relationship with the finance department.',
      'Refuse any budget reduction and escalate directly to the Secretary for overriding the finance department.',
      'Present objective data on the impact of cuts on data quality, propose tiered reduction scenarios, and identify shared interests such as cost-per-data-point efficiency.',
      'Suggest postponing the survey entirely until the full budget is restored next fiscal year.',
    ],
    correctIndex: 2,
  },
  // ── Public Administration (Q9–Q10) ──
  {
    id: 9,
    domain: 'Public Administration',
    scenario:
      'A government agency is tasked with redesigning the citizen grievance redressal process. Applying Design Thinking methodology, what is the correct first step?',
    options: [
      'Immediately brainstorm digital solutions based on similar platforms in other countries.',
      'Empathize — conduct field research with citizens and frontline staff to deeply understand pain points, needs, and the current experience journey.',
      'Define KPIs and service-level agreements before understanding the current process.',
      'Build a prototype portal and launch it as a pilot to collect feedback.',
    ],
    correctIndex: 1,
  },
  {
    id: 10,
    domain: 'Public Administration',
    scenario:
      'The Food Corporation of India (FCI) receives a large consignment of wheat from a procurement centre. Before the stock enters the central warehouse, a quality control officer must assess it. Under FCI\'s quality control framework, which parameter is NOT typically part of the standard quality assessment for wheat?',
    options: [
      'Moisture content percentage measured using a calibrated moisture meter.',
      'Foreign matter and damaged/shrivelled grain percentage by weight.',
      'Blockchain provenance hash of the procurement transaction ledger.',
      'Test weight (hectolitre weight) and presence of insect infestation.',
    ],
    correctIndex: 2,
  },
];

const RADAR_DATA = [
  { skill: 'Governance & Law', current: 45, benchmark: 75 },
  { skill: 'Cybersecurity & Tech', current: 60, benchmark: 80 },
  { skill: 'Soft Skills', current: 55, benchmark: 70 },
  { skill: 'Public Admin', current: 70, benchmark: 85 },
];

const ADMIN_BAR_DATA = [
  { dept: 'MoSPI', skillGap: 34, completion: 72 },
  { dept: 'NSSO', skillGap: 28, completion: 65 },
  { dept: 'CSO', skillGap: 41, completion: 58 },
  { dept: 'DES', skillGap: 22, completion: 81 },
  { dept: 'RGI', skillGap: 38, completion: 62 },
];

const NAV_LINKS = ['About Us', 'Newsroom', 'Career', 'Tenders', 'Help Centre'];

// ─────────────────────────── COMPONENT ───────────────────────────

export default function KarmaSetuApp() {
  const [screen, setScreen] = useState<Screen>('LOGIN');
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [currentQ, setCurrentQ] = useState(0);
  const [enrolledCourses, setEnrolledCourses] = useState<Set<string>>(new Set());
  const [mobileNav, setMobileNav] = useState(false);
  const [toast, setToast] = useState<string | null>(null);

  // Evaluating auto-advance
  useEffect(() => {
    if (screen === 'EVALUATING') {
      const timer = setTimeout(() => setScreen('QUIZ_RESULTS'), 3000);
      return () => clearTimeout(timer);
    }
  }, [screen]);

  // Toast auto-dismiss
  useEffect(() => {
    if (toast) {
      const t = setTimeout(() => setToast(null), 3000);
      return () => clearTimeout(t);
    }
  }, [toast]);

  const handleAnswer = useCallback(
    (questionIndex: number, optionIndex: number) => {
      setAnswers((prev) => ({ ...prev, [questionIndex]: optionIndex }));
      if (questionIndex < QUESTIONS.length - 1) {
        setTimeout(() => setCurrentQ(questionIndex + 1), 350);
      } else {
        setTimeout(() => setScreen('EVALUATING'), 400);
      }
    },
    []
  );

  const toggleEnroll = useCallback((courseId: string, courseTitle: string) => {
    setEnrolledCourses((prev) => {
      const next = new Set(prev);
      if (next.has(courseId)) {
        next.delete(courseId);
        setToast(`Unenrolled from "${courseTitle}"`);
      } else {
        next.add(courseId);
        setToast(`✓ Successfully enrolled in "${courseTitle}"`);
      }
      return next;
    });
  }, []);

  const resetQuiz = useCallback(() => {
    setAnswers({});
    setCurrentQ(0);
    setEnrolledCourses(new Set());
  }, []);

  // Compute per-domain score percentages
  const getDomainScores = useCallback((): Record<string, { correct: number; total: number; percent: number }> => {
    const scores: Record<string, { correct: number; total: number; percent: number }> = {};
    for (const domain of DOMAINS) {
      const domainQs = QUESTIONS.filter((q) => q.domain === domain);
      const correct = domainQs.filter((q, _) => {
        const qIdx = QUESTIONS.indexOf(q);
        return answers[qIdx] === q.correctIndex;
      }).length;
      scores[domain] = {
        correct,
        total: domainQs.length,
        percent: domainQs.length > 0 ? Math.round((correct / domainQs.length) * 100) : 100,
      };
    }
    return scores;
  }, [answers]);

  const getRecommendedCourses = useCallback((): Course[] => {
    const scores = getDomainScores();
    const weakDomains = DOMAINS.filter((d) => scores[d].percent < 70);
    // Return all courses whose domain scored below 70%
    return COURSES.filter((c) => weakDomains.includes(c.domain as Domain));
  }, [answers, getDomainScores]);

  // ─────────────────── SHARED NAVBAR ───────────────────
  const Navbar = ({ showLogout = false, role = '' }: { showLogout?: boolean; role?: string }) => (
    <nav className="sticky top-0 z-50 glass-strong shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <button
            onClick={() => {
              setScreen('LOGIN');
              resetQuiz();
            }}
            className="flex items-center gap-2 group cursor-pointer"
          >
            <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-blue-600 to-blue-700 flex items-center justify-center shadow-md group-hover:shadow-lg transition-shadow">
              <Zap className="w-5 h-5 text-white" />
            </div>
            <div className="flex flex-col">
              <span className="text-lg font-bold text-gradient-blue leading-tight">
                KarmaSetu
              </span>
              <span className="text-[10px] text-slate-400 leading-none tracking-wider uppercase">
                iGOT Karmayogi
              </span>
            </div>
          </button>

          {/* Desktop Nav */}
          <div className="hidden md:flex items-center gap-1">
            {!showLogout &&
              NAV_LINKS.map((link) => (
                <button
                  key={link}
                  className="px-3 py-2 text-sm font-medium text-slate-600 hover:text-blue-700 hover:bg-blue-50 rounded-lg transition-colors cursor-pointer"
                >
                  {link}
                </button>
              ))}
            {showLogout && role && (
              <span className="px-3 py-1.5 text-xs font-semibold bg-blue-50 text-blue-700 rounded-full mr-2">
                {role}
              </span>
            )}
            {showLogout && (
              <button
                onClick={() => {
                  setScreen('LOGIN');
                  resetQuiz();
                }}
                className="flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-red-600 hover:bg-red-50 rounded-lg transition-colors cursor-pointer"
              >
                <LogOut className="w-4 h-4" />
                Logout
              </button>
            )}
          </div>

          {/* Mobile hamburger */}
          <button
            className="md:hidden p-2 rounded-lg hover:bg-slate-100 transition-colors cursor-pointer"
            onClick={() => setMobileNav(!mobileNav)}
          >
            {mobileNav ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>

        {/* Mobile dropdown */}
        {mobileNav && (
          <div className="md:hidden pb-4 animate-slideDown">
            {!showLogout &&
              NAV_LINKS.map((link) => (
                <button
                  key={link}
                  className="block w-full text-left px-4 py-2.5 text-sm text-slate-600 hover:bg-blue-50 hover:text-blue-700 rounded-lg cursor-pointer"
                >
                  {link}
                </button>
              ))}
            {showLogout && (
              <button
                onClick={() => {
                  setScreen('LOGIN');
                  resetQuiz();
                  setMobileNav(false);
                }}
                className="block w-full text-left px-4 py-2.5 text-sm text-red-600 hover:bg-red-50 rounded-lg cursor-pointer"
              >
                <LogOut className="w-4 h-4 inline mr-2" />
                Logout
              </button>
            )}
          </div>
        )}
      </div>
    </nav>
  );

  // ─────────────────── LOGIN / LANDING ───────────────────
  if (screen === 'LOGIN') {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-50 via-white to-blue-50/30">
        <Navbar />

        {/* Hero */}
        <section className="relative overflow-hidden">
          {/* Decorative bg elements */}
          <div className="absolute inset-0 pointer-events-none">
            <div className="absolute top-20 left-10 w-72 h-72 bg-blue-100/40 rounded-full blur-3xl" />
            <div className="absolute bottom-10 right-10 w-96 h-96 bg-orange-100/30 rounded-full blur-3xl" />
            <div className="absolute top-40 right-1/4 w-48 h-48 bg-blue-200/20 rounded-full blur-2xl" />
          </div>

          <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-20">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              {/* Left — Text */}
              <div className="animate-slideUp">
                <div className="inline-flex items-center gap-2 px-4 py-1.5 mb-6 bg-blue-50 text-blue-700 rounded-full text-sm font-medium border border-blue-100">
                  <Shield className="w-4 h-4" />
                  Smart India Hackathon 2024
                </div>

                <h1 className="text-4xl sm:text-5xl lg:text-[3.4rem] font-extrabold leading-tight tracking-tight text-slate-900">
                  Dynamic Skill Intelligence for{' '}
                  <span className="text-gradient-blue">India&apos;s Official Statisticians</span>
                </h1>

                <p className="mt-6 text-lg text-slate-600 leading-relaxed max-w-lg">
                  KarmaSetu bridges competency gaps through AI-powered evaluation, mapping real-time
                  skill deltas to curated iGOT Karmayogi courses — empowering every government
                  official to serve better.
                </p>

                {/* CTA buttons */}
                <div className="mt-10 flex flex-col sm:flex-row gap-4">
                  <button
                    onClick={() => setScreen('EMPLOYEE_DASHBOARD')}
                    className="group flex items-center justify-center gap-2 px-8 py-4 bg-gradient-to-r from-blue-600 to-blue-700 text-white font-semibold rounded-xl shadow-lg shadow-blue-500/25 hover:shadow-xl hover:shadow-blue-500/30 hover:from-blue-700 hover:to-blue-800 transition-all duration-300 cursor-pointer"
                  >
                    <User className="w-5 h-5" />
                    Login as Employee
                    <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </button>
                  <button
                    onClick={() => setScreen('ADMIN_DASHBOARD')}
                    className="group flex items-center justify-center gap-2 px-8 py-4 bg-gradient-to-r from-orange-500 to-amber-500 text-white font-semibold rounded-xl shadow-lg shadow-orange-500/25 hover:shadow-xl hover:shadow-orange-500/30 hover:from-orange-600 hover:to-amber-600 transition-all duration-300 cursor-pointer"
                  >
                    <Shield className="w-5 h-5" />
                    Login as MDO Admin
                    <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </button>
                </div>
              </div>

              {/* Right — Hero Visual */}
              <div className="hidden lg:flex justify-center animate-fadeIn delay-300">
                <div className="relative">
                  {/* Main card */}
                  <div className="w-[400px] h-[340px] rounded-2xl bg-gradient-to-br from-blue-600 to-indigo-700 p-8 shadow-2xl shadow-blue-500/20 flex flex-col justify-between text-white">
                    <div>
                      <div className="flex items-center gap-3 mb-4">
                        <div className="w-12 h-12 rounded-xl bg-white/15 flex items-center justify-center backdrop-blur">
                          <Brain className="w-7 h-7" />
                        </div>
                        <div>
                          <p className="font-bold text-lg">AI Competency Engine</p>
                          <p className="text-blue-200 text-sm">Real-time skill mapping</p>
                        </div>
                      </div>
                      <div className="space-y-3 mt-6">
                        {['Soft Skills', 'Law & Policy', 'Technology'].map((s, i) => (
                          <div key={s} className="flex items-center gap-3">
                            <div className="flex-1 h-2.5 bg-white/15 rounded-full overflow-hidden">
                              <div
                                className="h-full bg-white/80 rounded-full animate-progress"
                                style={{
                                  width: `${[65, 48, 72][i]}%`,
                                  animationDelay: `${i * 300 + 500}ms`,
                                }}
                              />
                            </div>
                            <span className="text-sm text-blue-100 w-24 text-right">{s}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                    <div className="flex items-center gap-2 text-sm text-blue-200">
                      <TrendingUp className="w-4 h-4" />
                      <span>Mapped to 3,200+ iGOT courses</span>
                    </div>
                  </div>

                  {/* Floating badges */}
                  <div className="absolute -top-4 -right-4 px-4 py-2 bg-white rounded-xl shadow-lg animate-float delay-200">
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 bg-green-400 rounded-full" />
                      <span className="text-sm font-semibold text-slate-700">1,248 Assessed</span>
                    </div>
                  </div>
                  <div className="absolute -bottom-3 -left-4 px-4 py-2 bg-white rounded-xl shadow-lg animate-float delay-500">
                    <div className="flex items-center gap-2">
                      <Award className="w-4 h-4 text-orange-500" />
                      <span className="text-sm font-semibold text-slate-700">94% Match Rate</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Stats bar */}
        <section className="border-y border-slate-100 bg-white/60 backdrop-blur">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              {[
                { icon: Users, label: 'Officials Onboarded', value: '4.2L+' },
                { icon: BookOpen, label: 'iGOT Courses', value: '3,200+' },
                { icon: Building2, label: 'MDOs Covered', value: '850+' },
                { icon: Award, label: 'Certifications', value: '12,400+' },
              ].map(({ icon: Icon, label, value }, i) => (
                <div
                  key={label}
                  className={`flex items-center gap-4 animate-slideUp delay-${(i + 1) * 100}`}
                >
                  <div className="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center flex-shrink-0">
                    <Icon className="w-6 h-6 text-blue-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-slate-900">{value}</p>
                    <p className="text-sm text-slate-500">{label}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Feature highlights */}
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center mb-14 animate-fadeIn">
            <h2 className="text-3xl font-bold text-slate-900">
              How <span className="text-gradient-blue">KarmaSetu</span> Works
            </h2>
            <p className="mt-3 text-slate-500 max-w-2xl mx-auto">
              A three-step intelligent pipeline from assessment to upskilling
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: Target,
                color: 'from-blue-500 to-blue-600',
                shadow: 'shadow-blue-500/20',
                title: 'AI Competency Evaluation',
                desc: 'Scenario-based assessments aligned to your role & department, powered by adaptive questioning.',
              },
              {
                icon: Brain,
                color: 'from-indigo-500 to-purple-600',
                shadow: 'shadow-indigo-500/20',
                title: 'Skill Delta Mapping',
                desc: 'Our engine computes precise competency gaps across Law, Tech, Soft Skills, and Administration domains.',
              },
              {
                icon: GraduationCap,
                color: 'from-orange-500 to-amber-500',
                shadow: 'shadow-orange-500/20',
                title: 'iGOT Course Matching',
                desc: 'Personalized course recommendations from the official iGOT Karmayogi catalog — enroll in one click.',
              },
            ].map(({ icon: Icon, color, shadow, title, desc }, i) => (
              <div
                key={title}
                className={`card-hover relative p-8 rounded-2xl bg-white border border-slate-100 shadow-sm animate-slideUp delay-${(i + 1) * 200}`}
              >
                <div className="flex items-start gap-4 mb-1">
                  <div
                    className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${color} ${shadow} shadow-lg flex items-center justify-center flex-shrink-0`}
                  >
                    <Icon className="w-7 h-7 text-white" />
                  </div>
                  <div className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-sm font-bold text-slate-500 flex-shrink-0 mt-1">
                    {i + 1}
                  </div>
                </div>
                <h3 className="text-xl font-bold text-slate-900 mt-5">{title}</h3>
                <p className="mt-3 text-slate-500 leading-relaxed">{desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* ── Mobile App Download Section ── */}
        <section className="bg-gradient-to-r from-blue-700 via-blue-800 to-indigo-900 text-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              <div className="animate-slideUp">
                <div className="inline-flex items-center gap-2 px-3 py-1 bg-white/10 rounded-full text-sm mb-6">
                  <Smartphone className="w-4 h-4" />
                  Mobile Experience
                </div>
                <h2 className="text-3xl sm:text-4xl font-bold leading-tight">
                  Download iGOT Karmayogi Mobile App
                </h2>
                <p className="mt-4 text-blue-200 text-lg leading-relaxed max-w-lg">
                  Continue your lifelong learning experience anywhere anytime. Access courses,
                  track progress, and build competencies on the go.
                </p>

                {/* App store buttons */}
                <div className="flex flex-col sm:flex-row gap-4 mt-8">
                  <button className="flex items-center gap-3 px-6 py-3.5 bg-black rounded-xl hover:bg-gray-900 transition-colors group cursor-pointer">
                    <Play className="w-7 h-7 text-white" />
                    <div className="text-left">
                      <p className="text-[10px] text-gray-400 uppercase tracking-wider">
                        Get it on
                      </p>
                      <p className="text-base font-semibold text-white leading-tight">
                        Google Play
                      </p>
                    </div>
                  </button>
                  <button className="flex items-center gap-3 px-6 py-3.5 bg-black rounded-xl hover:bg-gray-900 transition-colors group cursor-pointer">
                    <Download className="w-7 h-7 text-white" />
                    <div className="text-left">
                      <p className="text-[10px] text-gray-400 uppercase tracking-wider">
                        Download on the
                      </p>
                      <p className="text-base font-semibold text-white leading-tight">App Store</p>
                    </div>
                  </button>
                </div>
              </div>

              {/* QR Codes */}
              <div className="flex justify-center lg:justify-end animate-fadeIn delay-300">
                <div className="flex gap-8">
                  {['Android', 'iOS'].map((platform) => (
                    <div key={platform} className="flex flex-col items-center gap-3">
                      <div className="w-36 h-36 bg-white rounded-2xl p-3 shadow-xl shadow-black/10">
                        {/* Mock QR code grid */}
                        <div className="w-full h-full grid grid-cols-7 grid-rows-7 gap-[2px]">
                          {Array.from({ length: 49 }).map((_, i) => {
                            const row = Math.floor(i / 7);
                            const col = i % 7;
                            const isCorner =
                              (row < 3 && col < 3) ||
                              (row < 3 && col > 3) ||
                              (row > 3 && col < 3);
                            const isFilled =
                              isCorner || (i + Math.floor(i / 3)) % 3 === 0;
                            return (
                              <div
                                key={i}
                                className={`rounded-[1px] ${isFilled ? 'bg-slate-900' : 'bg-slate-100'}`}
                              />
                            );
                          })}
                        </div>
                      </div>
                      <div className="flex items-center gap-1.5 text-sm text-blue-200">
                        <QrCode className="w-3.5 h-3.5" />
                        Scan for {platform}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="bg-slate-900 text-slate-400">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
            <div className="flex flex-col md:flex-row items-center justify-between gap-4">
              <div className="flex items-center gap-2">
                <div className="w-7 h-7 rounded-md bg-blue-600 flex items-center justify-center">
                  <Zap className="w-4 h-4 text-white" />
                </div>
                <span className="font-bold text-white">KarmaSetu</span>
                <span className="text-slate-500 text-sm ml-2">
                  © 2024 Ministry of Statistics & Programme Implementation
                </span>
              </div>
              <div className="flex items-center gap-6 text-sm">
                <span className="flex items-center gap-1.5">
                  <Globe className="w-3.5 h-3.5" />
                  igotkarmayogi.gov.in
                </span>
                <span>Privacy Policy</span>
                <span>Terms of Use</span>
              </div>
            </div>
          </div>
        </footer>
      </div>
    );
  }

  // ─────────────────── EMPLOYEE DASHBOARD ───────────────────
  if (screen === 'EMPLOYEE_DASHBOARD') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50/40">
        <Navbar showLogout role="Employee" />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Welcome */}
          <div className="animate-slideUp">
            <h1 className="text-2xl sm:text-3xl font-bold text-slate-900">
              Welcome back, <span className="text-gradient-blue">Arjun Mehta</span>
            </h1>
            <p className="text-slate-500 mt-1">
              Deputy Director, National Statistical Office · MoSPI
            </p>
          </div>

          <div className="grid lg:grid-cols-3 gap-6 mt-8">
            {/* Profile card */}
            <div className="lg:col-span-1 animate-slideUp delay-100">
              <div className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
                <div className="h-24 bg-gradient-to-r from-blue-600 to-indigo-600" />
                <div className="px-6 pb-6 -mt-10">
                  <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-blue-100 to-blue-200 border-4 border-white shadow-lg flex items-center justify-center">
                    <User className="w-10 h-10 text-blue-600" />
                  </div>
                  <h2 className="mt-3 text-xl font-bold text-slate-900">Arjun Mehta</h2>
                  <p className="text-sm text-slate-500">ID: NSO-2024-04781</p>

                  <div className="mt-5 space-y-3">
                    {[
                      { label: 'Department', value: 'MoSPI', icon: Building2 },
                      { label: 'Designation', value: 'Deputy Director', icon: Award },
                      { label: 'Service', value: 'ISS (2016 Batch)', icon: Star },
                      { label: 'Last Assessment', value: 'Never', icon: Clock },
                    ].map(({ label, value, icon: Icon }) => (
                      <div
                        key={label}
                        className="flex items-center gap-3 p-2.5 rounded-xl bg-slate-50"
                      >
                        <Icon className="w-4 h-4 text-slate-400 flex-shrink-0" />
                        <div className="flex-1 min-w-0">
                          <p className="text-xs text-slate-400">{label}</p>
                          <p className="text-sm font-medium text-slate-700 truncate">{value}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Main content */}
            <div className="lg:col-span-2 space-y-6">
              {/* Competency Radar */}
              <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 animate-slideUp delay-200">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-bold text-slate-900">Competency Profile</h3>
                    <p className="text-sm text-slate-500">
                      Baseline assessment vs. role benchmark
                    </p>
                  </div>
                  <div className="flex items-center gap-4 text-xs">
                    <div className="flex items-center gap-1.5">
                      <div className="w-3 h-3 rounded-full bg-blue-500" />
                      <span className="text-slate-500">Current</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <div className="w-3 h-3 rounded-full bg-orange-400" />
                      <span className="text-slate-500">Benchmark</span>
                    </div>
                  </div>
                </div>
                <div className="h-72">
                  <ResponsiveContainer width="100%" height="100%">
                    <RadarChart data={RADAR_DATA} cx="50%" cy="50%" outerRadius="72%">
                      <PolarGrid stroke="#e2e8f0" />
                      <PolarAngleAxis
                        dataKey="skill"
                        tick={{ fill: '#475569', fontSize: 13, fontWeight: 600 }}
                      />
                      <PolarRadiusAxis
                        angle={90}
                        domain={[0, 100]}
                        tick={{ fill: '#94a3b8', fontSize: 10 }}
                      />
                      <Radar
                        name="Current"
                        dataKey="current"
                        stroke="#3b82f6"
                        fill="#3b82f6"
                        fillOpacity={0.2}
                        strokeWidth={2}
                      />
                      <Radar
                        name="Benchmark"
                        dataKey="benchmark"
                        stroke="#f97316"
                        fill="#f97316"
                        fillOpacity={0.1}
                        strokeWidth={2}
                        strokeDasharray="5 5"
                      />
                    </RadarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* CTA */}
              <div className="animate-slideUp delay-300">
                <button
                  onClick={() => {
                    resetQuiz();
                    setScreen('QUIZ_ACTIVE');
                  }}
                  className="w-full group relative overflow-hidden rounded-2xl bg-gradient-to-r from-blue-600 via-blue-700 to-indigo-700 p-8 text-white shadow-xl shadow-blue-500/20 hover:shadow-2xl hover:shadow-blue-500/30 transition-all duration-300 cursor-pointer animate-pulseGlow"
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent animate-shimmer" />
                  <div className="relative flex items-center justify-between">
                    <div className="flex items-center gap-5">
                      <div className="w-16 h-16 rounded-2xl bg-white/15 flex items-center justify-center backdrop-blur-sm">
                        <Brain className="w-9 h-9" />
                      </div>
                      <div className="text-left">
                        <h3 className="text-2xl font-bold">Start AI Competency Evaluation</h3>
                        <p className="text-blue-200 mt-1">
                          3 scenario-based questions · ~5 min · Adaptive difficulty
                        </p>
                      </div>
                    </div>
                    <ArrowRight className="w-8 h-8 text-white/70 group-hover:translate-x-2 group-hover:text-white transition-all" />
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // ─────────────────── QUIZ ───────────────────
  if (screen === 'QUIZ_ACTIVE') {
    const q = QUESTIONS[currentQ];
    const domainColors: Record<string, string> = {
      'Governance & Law': 'from-amber-500 to-orange-600',
      'Cybersecurity & Tech': 'from-cyan-500 to-blue-600',
      'Managerial & Soft Skills': 'from-pink-500 to-rose-600',
      'Public Administration': 'from-emerald-500 to-teal-600',
    };
    const domainIcons: Record<string, typeof Users> = {
      'Governance & Law': BookOpen,
      'Cybersecurity & Tech': Shield,
      'Managerial & Soft Skills': Users,
      'Public Administration': Building2,
    };
    const DomainIcon = domainIcons[q.domain] || Brain;

    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50/40">
        <Navbar showLogout role="Assessment" />

        <div className="max-w-3xl mx-auto px-4 sm:px-6 py-8">
          {/* Progress bar */}
          <div className="mb-8 animate-fadeIn">
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm font-semibold text-slate-600">
                Question {currentQ + 1} of {QUESTIONS.length}
              </span>
              <span
                className={`px-3 py-1 text-xs font-bold rounded-full text-white bg-gradient-to-r ${domainColors[q.domain]}`}
              >
                {q.domain}
              </span>
            </div>
            <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-blue-500 to-blue-600 rounded-full transition-all duration-500 ease-out"
                style={{ width: `${((currentQ + 1) / QUESTIONS.length) * 100}%` }}
              />
            </div>
          </div>

          {/* Question card */}
          <div key={q.id} className="animate-slideUp">
            <div className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
              {/* Question header */}
              <div
                className={`p-6 bg-gradient-to-r ${domainColors[q.domain]} text-white`}
              >
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-xl bg-white/15 flex items-center justify-center flex-shrink-0 backdrop-blur">
                    <DomainIcon className="w-6 h-6" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-white/70 mb-1">
                      Scenario-Based Assessment
                    </p>
                    <p className="text-lg font-semibold leading-relaxed">{q.scenario}</p>
                  </div>
                </div>
              </div>

              {/* Options */}
              <div className="p-6 space-y-3">
                {q.options.map((option, i) => {
                  const isSelected = answers[currentQ] === i;
                  const letter = String.fromCharCode(65 + i);
                  return (
                    <button
                      key={i}
                      onClick={() => handleAnswer(currentQ, i)}
                      disabled={answers[currentQ] !== undefined}
                      className={`w-full text-left p-4 rounded-xl border-2 transition-all duration-200 group cursor-pointer ${isSelected
                          ? 'border-blue-500 bg-blue-50 shadow-md shadow-blue-500/10'
                          : 'border-slate-100 hover:border-blue-200 hover:bg-blue-50/50 hover:shadow-sm'
                        } disabled:cursor-default`}
                    >
                      <div className="flex items-start gap-3">
                        <span
                          className={`w-8 h-8 rounded-lg flex items-center justify-center text-sm font-bold flex-shrink-0 mt-0.5 transition-colors ${isSelected
                              ? 'bg-blue-600 text-white'
                              : 'bg-slate-100 text-slate-500 group-hover:bg-blue-100 group-hover:text-blue-700'
                            }`}
                        >
                          {letter}
                        </span>
                        <span
                          className={`text-sm leading-relaxed ${isSelected
                              ? 'text-blue-900 font-medium'
                              : 'text-slate-700'
                            }`}
                        >
                          {option}
                        </span>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Question dots */}
            <div className="flex items-center justify-center gap-1.5 mt-6 flex-wrap">
              {QUESTIONS.map((_, i) => (
                <div
                  key={i}
                  className={`h-2.5 rounded-full transition-all duration-300 ${i === currentQ
                      ? 'w-6 bg-blue-600'
                      : i < currentQ
                        ? 'w-2.5 bg-blue-400'
                        : 'w-2.5 bg-slate-200'
                    }`}
                />
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // ─────────────────── EVALUATING ───────────────────
  if (screen === 'EVALUATING') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50/40 flex items-center justify-center">
        <div className="text-center animate-scaleIn">
          {/* Spinner */}
          <div className="relative w-32 h-32 mx-auto mb-8">
            {/* Outer ring */}
            <div className="absolute inset-0 rounded-full border-4 border-blue-100" />
            <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-blue-600 animate-spin-slow" />
            {/* Middle ring */}
            <div className="absolute inset-3 rounded-full border-4 border-transparent border-b-indigo-500 animate-spin-slow" style={{ animationDirection: 'reverse', animationDuration: '2s' }} />
            {/* Inner icon */}
            <div className="absolute inset-0 flex items-center justify-center">
              <Brain className="w-12 h-12 text-blue-600 animate-pulse" />
            </div>
            {/* Ping */}
            <div className="absolute inset-0 rounded-full border-2 border-blue-400 animate-radar-ping" />
          </div>

          <h2 className="text-2xl font-bold text-slate-900 mb-2">
            AI Mapping Competency Delta...
          </h2>
          <p className="text-slate-500 max-w-md mx-auto">
            Analyzing your responses against role-specific benchmarks and mapping skill gaps to
            curated iGOT Karmayogi courses.
          </p>

          {/* Progress bar */}
          <div className="w-64 mx-auto mt-8">
            <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
              <div className="h-full bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full animate-progress" />
            </div>
          </div>
        </div>
      </div>
    );
  }

  // ─────────────────── QUIZ RESULTS ───────────────────
  if (screen === 'QUIZ_RESULTS') {
    const recommended = getRecommendedCourses();
    const domainScores = getDomainScores();
    const correctCount = QUESTIONS.filter(
      (q, i) => answers[i] === q.correctIndex
    ).length;
    const scorePercent = Math.round((correctCount / QUESTIONS.length) * 100);
    const weakDomainCount = DOMAINS.filter((d) => domainScores[d].percent < 70).length;

    const domainColorMap: Record<string, string> = {
      'Governance & Law': 'from-amber-500 to-orange-500',
      'Cybersecurity & Tech': 'from-cyan-500 to-blue-500',
      'Managerial & Soft Skills': 'from-pink-500 to-rose-500',
      'Public Administration': 'from-emerald-500 to-teal-500',
    };

    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50/40">
        <Navbar showLogout role="Results" />

        <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8">
          {/* Score card */}
          <div className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden animate-scaleIn">
            <div className="bg-gradient-to-r from-blue-600 to-indigo-700 p-8 text-white">
              <div className="flex flex-col sm:flex-row items-center gap-6">
                <div className="relative w-28 h-28 flex-shrink-0">
                  <svg className="w-28 h-28 transform -rotate-90" viewBox="0 0 120 120">
                    <circle
                      cx="60"
                      cy="60"
                      r="52"
                      stroke="rgba(255,255,255,0.15)"
                      strokeWidth="8"
                      fill="none"
                    />
                    <circle
                      cx="60"
                      cy="60"
                      r="52"
                      stroke="white"
                      strokeWidth="8"
                      fill="none"
                      strokeLinecap="round"
                      strokeDasharray={`${(scorePercent / 100) * 327} 327`}
                      className="transition-all duration-1000"
                    />
                  </svg>
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="text-center">
                      <span className="text-3xl font-bold">{scorePercent}%</span>
                    </div>
                  </div>
                </div>
                <div className="text-center sm:text-left">
                  <h2 className="text-2xl font-bold">Competency Assessment Complete</h2>
                  <p className="text-blue-200 mt-2">
                    You answered {correctCount} of {QUESTIONS.length} questions correctly.
                    {weakDomainCount > 0
                      ? ` We identified ${weakDomainCount} domain${weakDomainCount > 1 ? 's' : ''} below 70% proficiency and matched ${recommended.length} course${recommended.length > 1 ? 's' : ''} to bridge them.`
                      : ' Outstanding — all domains scored above 70% proficiency!'}
                  </p>
                </div>
              </div>
            </div>

            {/* Question-by-question breakdown */}
            <div className="p-6">
              <h3 className="text-sm font-bold text-slate-500 uppercase tracking-wider mb-4">
                Question Breakdown
              </h3>
              <div className="space-y-3">
                {QUESTIONS.map((q, i) => {
                  const isCorrect = answers[i] === q.correctIndex;
                  return (
                    <div
                      key={q.id}
                      className={`flex items-center gap-4 p-4 rounded-xl border animate-slideUp delay-${(i + 1) * 100} ${isCorrect
                          ? 'border-green-100 bg-green-50/50'
                          : 'border-red-100 bg-red-50/50'
                        }`}
                    >
                      <div
                        className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 ${isCorrect ? 'bg-green-100' : 'bg-red-100'
                          }`}
                      >
                        {isCorrect ? (
                          <CheckCircle2 className="w-5 h-5 text-green-600" />
                        ) : (
                          <X className="w-5 h-5 text-red-500" />
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-semibold text-slate-800">Q{i + 1}: {q.domain}</p>
                        <p className="text-xs text-slate-500 mt-0.5">
                          Your answer: Option{' '}
                          {answers[i] !== undefined
                            ? String.fromCharCode(65 + answers[i])
                            : '—'}{' '}
                          · Correct: Option {String.fromCharCode(65 + q.correctIndex)}
                        </p>
                      </div>
                      <span
                        className={`text-xs font-bold px-3 py-1 rounded-full ${isCorrect
                            ? 'bg-green-100 text-green-700'
                            : 'bg-red-100 text-red-600'
                          }`}
                      >
                        {isCorrect ? 'Correct' : 'Incorrect'}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Domain Competency Breakdown */}
          <div className="mt-8 bg-white rounded-2xl shadow-sm border border-slate-100 p-6 animate-slideUp delay-200">
            <h3 className="text-sm font-bold text-slate-500 uppercase tracking-wider mb-4">
              Domain-wise Competency Analysis
            </h3>
            <p className="text-xs text-slate-400 mb-5">
              Domains scoring below 70% are flagged for upskilling. Courses are recommended for flagged domains.
            </p>
            <div className="grid sm:grid-cols-2 gap-4">
              {DOMAINS.map((domain) => {
                const s = domainScores[domain];
                const isWeak = s.percent < 70;
                return (
                  <div
                    key={domain}
                    className={`p-4 rounded-xl border-2 transition-all ${isWeak
                        ? 'border-red-200 bg-red-50/50'
                        : 'border-green-200 bg-green-50/50'
                      }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-bold text-slate-800">{domain}</span>
                      <span
                        className={`text-xs font-bold px-2.5 py-0.5 rounded-full ${isWeak
                            ? 'bg-red-100 text-red-700'
                            : 'bg-green-100 text-green-700'
                          }`}
                      >
                        {isWeak ? '⚠ Gap Detected' : '✓ Proficient'}
                      </span>
                    </div>
                    <div className="h-2.5 bg-slate-100 rounded-full overflow-hidden mb-2">
                      <div
                        className={`h-full rounded-full transition-all duration-700 bg-gradient-to-r ${domainColorMap[domain] || 'from-blue-500 to-blue-600'}`}
                        style={{ width: `${s.percent}%` }}
                      />
                    </div>
                    <div className="flex items-center justify-between text-xs text-slate-500">
                      <span>{s.correct}/{s.total} correct</span>
                      <span className={`font-bold ${isWeak ? 'text-red-600' : 'text-green-600'}`}>
                        {s.percent}%
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Recommended courses */}
          {recommended.length > 0 && (
            <div className="mt-8 animate-slideUp delay-400">
              <div className="flex items-center gap-3 mb-5">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-orange-500 to-amber-500 flex items-center justify-center shadow-lg shadow-orange-500/20">
                  <BookOpen className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-slate-900">
                    Recommended iGOT Courses
                  </h3>
                  <p className="text-sm text-slate-500">
                    Curated to bridge your identified competency gaps
                  </p>
                </div>
              </div>

              <div className="space-y-4">
                {recommended.map((course, i) => {
                  const isEnrolled = enrolledCourses.has(course.id);
                  const domainColor: Record<string, string> = {
                    'Governance & Law': 'from-amber-500 to-orange-500',
                    'Cybersecurity & Tech': 'from-cyan-500 to-blue-500',
                    'Managerial & Soft Skills': 'from-pink-500 to-rose-500',
                    'Public Administration': 'from-emerald-500 to-teal-500',
                  };
                  return (
                    <div
                      key={course.id}
                      className={`card-hover bg-white rounded-2xl shadow-sm border border-slate-100 p-6 animate-slideUp delay-${(i + 1) * 100}`}
                    >
                      <div className="flex flex-col sm:flex-row sm:items-center gap-4">
                        <div
                          className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${domainColor[course.domain] || 'from-blue-500 to-blue-600'} flex items-center justify-center flex-shrink-0 shadow-lg`}
                        >
                          <GraduationCap className="w-7 h-7 text-white" />
                        </div>

                        <div className="flex-1 min-w-0">
                          <h4 className="text-base font-bold text-slate-900">
                            {course.title}
                          </h4>
                          <div className="flex flex-wrap items-center gap-3 mt-2 text-sm text-slate-500">
                            <span className="flex items-center gap-1">
                              <Building2 className="w-3.5 h-3.5" />
                              {course.org}
                            </span>
                            <span className="flex items-center gap-1">
                              <Clock className="w-3.5 h-3.5" />
                              {course.duration}
                            </span>
                            <span
                              className={`px-2.5 py-0.5 rounded-full text-xs font-semibold text-white bg-gradient-to-r ${domainColor[course.domain] || 'from-blue-500 to-blue-600'}`}
                            >
                              {course.domain}
                            </span>
                          </div>
                        </div>

                        <button
                          onClick={() => toggleEnroll(course.id, course.title)}
                          className={`flex items-center gap-2 px-6 py-3 rounded-xl font-semibold text-sm transition-all duration-300 flex-shrink-0 cursor-pointer ${isEnrolled
                              ? 'bg-green-50 text-green-700 border-2 border-green-200 shadow-sm shadow-green-500/10'
                              : 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg shadow-blue-500/25 hover:shadow-xl hover:from-blue-700 hover:to-blue-800'
                            }`}
                        >
                          {isEnrolled ? (
                            <>
                              <CheckCircle2 className="w-4 h-4" />
                              ✓ Enrolled
                            </>
                          ) : (
                            <>
                              <ArrowRight className="w-4 h-4" />
                              Enroll
                            </>
                          )}
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* All correct message */}
          {recommended.length === 0 && (
            <div className="mt-8 bg-gradient-to-r from-green-50 to-emerald-50 border border-green-100 rounded-2xl p-8 text-center animate-scaleIn delay-200">
              <div className="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center mx-auto mb-4">
                <Award className="w-8 h-8 text-green-600" />
              </div>
              <h3 className="text-xl font-bold text-green-800">
                Outstanding Performance!
              </h3>
              <p className="text-green-600 mt-2 max-w-md mx-auto">
                You scored above 70% in all domains. No course remediation required at this time.
              </p>
            </div>
          )}

          {/* Toast notification */}
          {toast && (
            <div className="fixed bottom-6 right-6 z-50 animate-slideUp">
              <div className="flex items-center gap-3 px-5 py-3.5 bg-slate-900 text-white rounded-xl shadow-2xl shadow-black/20 max-w-sm">
                <CheckCircle2 className="w-5 h-5 text-green-400 flex-shrink-0" />
                <p className="text-sm font-medium">{toast}</p>
              </div>
            </div>
          )}

          {/* Back to dashboard */}
          <div className="mt-8 flex justify-center animate-fadeIn delay-500">
            <button
              onClick={() => {
                resetQuiz();
                setScreen('EMPLOYEE_DASHBOARD');
              }}
              className="flex items-center gap-2 px-6 py-3 text-sm font-semibold text-blue-700 hover:bg-blue-50 rounded-xl transition-colors cursor-pointer"
            >
              <ChevronRight className="w-4 h-4 rotate-180" />
              Back to Dashboard
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ─────────────────── ADMIN DASHBOARD ───────────────────
  if (screen === 'ADMIN_DASHBOARD') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-orange-50/30">
        <Navbar showLogout role="MDO Admin" />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Header */}
          <div className="animate-slideUp">
            <h1 className="text-2xl sm:text-3xl font-bold text-slate-900">
              MDO Command Centre
            </h1>
            <p className="text-slate-500 mt-1">
              Ministry of Statistics & Programme Implementation · Real-time Analytics
            </p>
          </div>

          {/* KPI cards */}
          <div className="grid sm:grid-cols-3 gap-6 mt-8">
            {[
              {
                icon: Users,
                label: 'Officials Assessed',
                value: '1,248',
                change: '+12% this month',
                color: 'from-blue-500 to-blue-600',
                shadow: 'shadow-blue-500/20',
                bg: 'bg-blue-50',
              },
              {
                icon: TrendingUp,
                label: 'Average Competency Score',
                value: '67.3%',
                change: '+4.2% improvement',
                color: 'from-emerald-500 to-green-600',
                shadow: 'shadow-green-500/20',
                bg: 'bg-green-50',
              },
              {
                icon: BookOpen,
                label: 'Course Enrollments',
                value: '3,847',
                change: '89% completion rate',
                color: 'from-orange-500 to-amber-500',
                shadow: 'shadow-orange-500/20',
                bg: 'bg-orange-50',
              },
            ].map(({ icon: Icon, label, value, change, color, shadow, bg }, i) => (
              <div
                key={label}
                className={`card-hover bg-white rounded-2xl shadow-sm border border-slate-100 p-6 animate-slideUp delay-${(i + 1) * 100}`}
              >
                <div className="flex items-start justify-between">
                  <div
                    className={`w-12 h-12 rounded-2xl bg-gradient-to-br ${color} ${shadow} shadow-lg flex items-center justify-center`}
                  >
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  <span
                    className={`px-2.5 py-1 text-xs font-semibold rounded-full ${bg} text-slate-600`}
                  >
                    Live
                  </span>
                </div>
                <p className="mt-4 text-3xl font-bold text-slate-900">{value}</p>
                <p className="text-sm text-slate-500 mt-1">{label}</p>
                <p className="text-xs text-emerald-600 font-medium mt-2 flex items-center gap-1">
                  <TrendingUp className="w-3 h-3" />
                  {change}
                </p>
              </div>
            ))}
          </div>

          {/* Charts row */}
          <div className="grid lg:grid-cols-2 gap-6 mt-8">
            {/* Bar chart — Skill Gaps vs Completion */}
            <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 animate-slideUp delay-300">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h3 className="text-lg font-bold text-slate-900">
                    Department Skill Analysis
                  </h3>
                  <p className="text-sm text-slate-500">
                    Skill gaps vs. course completion rates
                  </p>
                </div>
                <BarChart3 className="w-5 h-5 text-slate-400" />
              </div>
              <div className="h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={ADMIN_BAR_DATA} barGap={4}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                    <XAxis
                      dataKey="dept"
                      tick={{ fill: '#64748b', fontSize: 12, fontWeight: 500 }}
                      axisLine={{ stroke: '#e2e8f0' }}
                    />
                    <YAxis
                      tick={{ fill: '#94a3b8', fontSize: 11 }}
                      axisLine={{ stroke: '#e2e8f0' }}
                    />
                    <Tooltip
                      contentStyle={{
                        borderRadius: '12px',
                        border: '1px solid #e2e8f0',
                        boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
                        fontSize: '13px',
                      }}
                    />
                    <Legend
                      wrapperStyle={{ fontSize: '12px', paddingTop: '12px' }}
                    />
                    <Bar
                      dataKey="skillGap"
                      name="Skill Gap %"
                      fill="#ef4444"
                      radius={[6, 6, 0, 0]}
                    >
                      {ADMIN_BAR_DATA.map((_, i) => (
                        <Cell
                          key={i}
                          fill={`hsl(${0 + i * 5}, 80%, ${55 + i * 3}%)`}
                        />
                      ))}
                    </Bar>
                    <Bar
                      dataKey="completion"
                      name="Course Completion %"
                      fill="#3b82f6"
                      radius={[6, 6, 0, 0]}
                    >
                      {ADMIN_BAR_DATA.map((_, i) => (
                        <Cell
                          key={i}
                          fill={`hsl(${210 + i * 8}, 75%, ${50 + i * 4}%)`}
                        />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Top Gap Areas */}
            <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 animate-slideUp delay-400">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h3 className="text-lg font-bold text-slate-900">
                    Priority Upskilling Areas
                  </h3>
                  <p className="text-sm text-slate-500">
                    Domains with the largest competency deficits
                  </p>
                </div>
                <Target className="w-5 h-5 text-slate-400" />
              </div>

              <div className="space-y-4">
                {[
                  {
                    domain: 'Bharatiya Sakshya Adhiniyam',
                    gap: 41,
                    officials: 312,
                    course: 'Introduction to BSA, 2023',
                    color: 'bg-red-500',
                    bgLight: 'bg-red-50',
                  },
                  {
                    domain: 'Cyber Security & VPN',
                    gap: 35,
                    officials: 287,
                    course: 'VPN Overview',
                    color: 'bg-orange-500',
                    bgLight: 'bg-orange-50',
                  },
                  {
                    domain: 'Interpersonal Communication',
                    gap: 28,
                    officials: 245,
                    course: 'Effective Soft Skills',
                    color: 'bg-amber-500',
                    bgLight: 'bg-amber-50',
                  },
                  {
                    domain: 'Data Privacy Compliance',
                    gap: 24,
                    officials: 198,
                    course: 'IT Act Overview',
                    color: 'bg-yellow-500',
                    bgLight: 'bg-yellow-50',
                  },
                  {
                    domain: 'Statistical Methodology',
                    gap: 19,
                    officials: 156,
                    course: 'Survey Design',
                    color: 'bg-blue-500',
                    bgLight: 'bg-blue-50',
                  },
                ].map(({ domain, gap, officials, course, color, bgLight }, i) => (
                  <div
                    key={domain}
                    className={`flex items-center gap-4 p-3.5 rounded-xl ${bgLight} animate-slideUp delay-${(i + 1) * 100}`}
                  >
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between mb-1.5">
                        <p className="text-sm font-semibold text-slate-800 truncate">
                          {domain}
                        </p>
                        <span className="text-xs font-bold text-slate-600 ml-2 flex-shrink-0">
                          {gap}% gap
                        </span>
                      </div>
                      <div className="h-2 bg-white rounded-full overflow-hidden">
                        <div
                          className={`h-full ${color} rounded-full transition-all duration-700`}
                          style={{ width: `${gap}%` }}
                        />
                      </div>
                      <div className="flex items-center justify-between mt-1.5">
                        <span className="text-xs text-slate-500">
                          {officials} officials affected
                        </span>
                        <span className="text-xs text-blue-600 font-medium">
                          → {course}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Recent assessments table */}
          <div className="mt-8 bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden animate-slideUp delay-500">
            <div className="p-6 border-b border-slate-100">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-bold text-slate-900">
                    Recent Assessments
                  </h3>
                  <p className="text-sm text-slate-500">
                    Latest competency evaluations across departments
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <Info className="w-4 h-4 text-slate-400" />
                  <span className="text-xs text-slate-400">Auto-refreshing</span>
                </div>
              </div>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="bg-slate-50">
                    <th className="text-left px-6 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                      Officer
                    </th>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                      Department
                    </th>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                      Score
                    </th>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                      Gaps Found
                    </th>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                      Status
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-50">
                  {[
                    {
                      name: 'Priya Sharma',
                      dept: 'NSSO',
                      score: 78,
                      gaps: 1,
                      status: 'Enrolled',
                    },
                    {
                      name: 'Rajesh Kumar',
                      dept: 'CSO',
                      score: 45,
                      gaps: 3,
                      status: 'Pending',
                    },
                    {
                      name: 'Anjali Desai',
                      dept: 'DES',
                      score: 92,
                      gaps: 0,
                      status: 'Cleared',
                    },
                    {
                      name: 'Vikram Singh',
                      dept: 'MoSPI',
                      score: 61,
                      gaps: 2,
                      status: 'Enrolled',
                    },
                    {
                      name: 'Meera Nair',
                      dept: 'RGI',
                      score: 53,
                      gaps: 2,
                      status: 'Pending',
                    },
                  ].map(({ name, dept, score, gaps, status }) => (
                    <tr key={name} className="hover:bg-slate-50/50 transition-colors">
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-100 to-blue-200 flex items-center justify-center">
                            <span className="text-xs font-bold text-blue-700">
                              {name
                                .split(' ')
                                .map((n) => n[0])
                                .join('')}
                            </span>
                          </div>
                          <span className="text-sm font-medium text-slate-800">
                            {name}
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-600">{dept}</td>
                      <td className="px-6 py-4">
                        <span
                          className={`text-sm font-bold ${score >= 75
                              ? 'text-green-600'
                              : score >= 50
                                ? 'text-amber-600'
                                : 'text-red-600'
                            }`}
                        >
                          {score}%
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-600">{gaps}</td>
                      <td className="px-6 py-4">
                        <span
                          className={`px-2.5 py-1 text-xs font-semibold rounded-full ${status === 'Cleared'
                              ? 'bg-green-50 text-green-700'
                              : status === 'Enrolled'
                                ? 'bg-blue-50 text-blue-700'
                                : 'bg-amber-50 text-amber-700'
                            }`}
                        >
                          {status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Fallback — should never reach
  return null;
}
