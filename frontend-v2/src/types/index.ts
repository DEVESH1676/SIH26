// ── User & Auth ─────────────────────────────────────────────
export interface User {
  user_id: string;
  username: string;
  email: string;
  designation: string;
  department: string;
  roles: string[];
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user_id: string;
  roles: string[];
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  designation: string;
  department: string;
  role?: string;
}

// ── Competency & Profile ────────────────────────────────────
export interface CompetencySummary {
  domain: string;
  level: string;
  score: number;
  strengths: string[];
  gaps: string[];
}

export interface LearnerProfileRequest {
  designation: string;
  profile_text: string;
  department?: string;
  education?: string;
  experience_years?: number;
  previous_trainings?: string[];
}

export interface LearnerProfileResponse {
  current_skills: Array<{ id: string; name: string; level: string }>;
  skill_gaps: Array<{ id: string; name: string; priority: string; domain?: string; reason?: string }>;
  competency_summary: Record<string, any>;
  analysis_summary: string;
  gap_report?: string;
}

// ── Courses ─────────────────────────────────────────────────
export interface CourseResponse {
  id: string;
  title: string;
  description: string;
  domain: string;
  duration_hours: number;
  difficulty: string;
  skills: string[];
  tags: string[];
  source: string;
}

export interface CourseRecommendation {
  courses: CourseResponse[];
  tpac_programmes: any[];
  estimated_hours: number;
  recommended_sequence: any[];
  source: string;
}

// ── Quiz ────────────────────────────────────────────────────
export interface QuizQuestion {
  id: string;
  question: string;
  options: string[];
  correct_answer: number;
  explanation: string;
  difficulty: string;
  category: string;
}

export interface QuizResponse {
  quiz_id: string;
  quiz_title: string;
  questions: QuizQuestion[];
  source: string;
}

export interface QuizAttemptRequest {
  quiz_id: string;
  answers: Record<string, number>;
  time_taken_seconds: number;
}

export interface QuizResult {
  score: number;
  total: number;
  percentage: number;
  passed: boolean;
  results: any[];
}

// ── Analytics ───────────────────────────────────────────────
export interface AdminOverview {
  total_learners: number;
  total_learning_sessions: number;
  total_quiz_attempts: number;
  total_enrolled_courses: number;
}

export interface WorkforceCompetency {
  competency_id: string;
  competency_name: string;
  avg_score: number;
  assessed_count: number;
  mastery_rate: number;
}

export interface TrainingEffectiveness {
  title: string;
  enrolled: number;
  avg_score: number;
  pass_rate: number;
}

export interface PredictiveGap {
  competency_id: string;
  current_avg: number;
  previous_avg: number;
  decline_percent: number;
  priority: string;
}

export interface AdminAnalyticsResponse {
  overview: AdminOverview;
  workforce_competency: WorkforceCompetency[];
  training_effectiveness: TrainingEffectiveness[];
  predictive_skill_gaps: PredictiveGap[];
}

// ── Virtual Assistant ───────────────────────────────────────
export interface AssistantRequest {
  message: string;
  language?: string;
  user_context?: Record<string, any>;
}

export interface AssistantResponse {
  response: string;
  suggested_actions: Array<{ label: string; action: string }>;
  related_resources: Array<{ title: string; url: string; type: string }>;
  intent: string;
}

// ── Learning Progress ───────────────────────────────────────
export interface LearningSession {
  session_id: string;
  activity_type: string;
  resource_id: string;
  resource_type: string;
  duration_seconds: number;
  started_at: string;
  completed_at: string;
}

export interface LearningHoursResponse {
  total_sessions: number;
  total_hours: number;
  average_session_minutes: number;
  first_session: string | null;
  last_session: string | null;
}

// ── Health ──────────────────────────────────────────────────
export interface HealthResponse {
  status: string;
  database: string;
  version: string;
}

// ── Profile (KarmaSetu onboarding) ──────────────────────────
export type SkillLevel = 'Beginner' | 'Intermediate' | 'Advanced';
export type ProfileStep = 1 | 2 | 3 | 4;

export interface OnboardingProfile {
  name: string;
  officerId: string;
  department: string;
  organization: string;
  designation: string;
  role: string;
  years: string;
  qualification: string;
  field: string;
  certifications: string[];
  expertise: string[];
  levels: Record<string, SkillLevel>;
  focus: string[];
  format: string;
  time: string;
}
