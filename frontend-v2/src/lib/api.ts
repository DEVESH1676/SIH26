/**
 * Centralized API client for the SIH26 FastAPI backend.
 * Handles JWT auth, token refresh, and typed API methods.
 */
import type {
  LoginResponse,
  RegisterData,
  User,
  LearnerProfileRequest,
  LearnerProfileResponse,
  QuizResponse,
  QuizAttemptRequest,
  QuizResult,
  AssistantRequest,
  AssistantResponse,
  HealthResponse,
  AdminAnalyticsResponse,
  LearningHoursResponse,
} from '../types';

const API_BASE = '/api';

// ── Token helpers ───────────────────────────────────────────
function getAccessToken(): string | null {
  return localStorage.getItem('karmasetu_access_token');
}

function getRefreshToken(): string | null {
  return localStorage.getItem('karmasetu_refresh_token');
}

export function setTokens(access: string, refresh: string) {
  localStorage.setItem('karmasetu_access_token', access);
  localStorage.setItem('karmasetu_refresh_token', refresh);
}

export function clearTokens() {
  localStorage.removeItem('karmasetu_access_token');
  localStorage.removeItem('karmasetu_refresh_token');
}

// ── Core fetch wrapper ──────────────────────────────────────
async function apiFetch<T>(
  path: string,
  options: RequestInit = {},
  skipAuth = false
): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };

  if (!skipAuth) {
    const token = getAccessToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
  }

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  // Attempt token refresh on 401
  if (res.status === 401 && !skipAuth) {
    const refreshed = await tryRefreshToken();
    if (refreshed) {
      headers['Authorization'] = `Bearer ${getAccessToken()}`;
      const retryRes = await fetch(`${API_BASE}${path}`, { ...options, headers });
      if (!retryRes.ok) {
        const err = await retryRes.json().catch(() => ({ detail: 'Request failed' }));
        console.error(`[API Error] Retry ${options.method || 'GET'} ${API_BASE}${path} [${retryRes.status}]:`, err);
        throw new Error(err.detail || `API error ${retryRes.status}`);
      }
      return retryRes.json();
    }
    clearTokens();
    window.location.href = '/login';
    throw new Error('Session expired');
  }

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Request failed' }));
    console.error(`[API Error] ${options.method || 'GET'} ${API_BASE}${path} [${res.status}]:`, err);
    throw new Error(err.detail || `API error ${res.status}`);
  }

  return res.json();
}

async function tryRefreshToken(): Promise<boolean> {
  const refreshToken = getRefreshToken();
  if (!refreshToken) return false;
  try {
    const res = await fetch(`${API_BASE}/auth/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${refreshToken}`,
      },
    });
    if (!res.ok) return false;
    const data = await res.json();
    localStorage.setItem('karmasetu_access_token', data.access_token);
    return true;
  } catch {
    return false;
  }
}

// ── Auth API ────────────────────────────────────────────────
export async function login(username: string, password: string): Promise<LoginResponse> {
  const data = await apiFetch<LoginResponse>(
    '/auth/login',
    { method: 'POST', body: JSON.stringify({ username, password }) },
    true
  );
  setTokens(data.access_token, data.refresh_token);
  return data;
}

export async function register(formData: RegisterData): Promise<{ message: string; user_id: string }> {
  return apiFetch('/auth/register', {
    method: 'POST',
    body: JSON.stringify(formData),
  }, true);
}

export async function getMe(): Promise<User> {
  return apiFetch<User>('/auth/me');
}

// ── Competency & Pipeline ───────────────────────────────────
export async function analyzeProfile(req: LearnerProfileRequest): Promise<LearnerProfileResponse> {
  return apiFetch('/analyze-profile', {
    method: 'POST',
    body: JSON.stringify(req),
  });
}

export async function generatePlan(req: LearnerProfileRequest): Promise<any> {
  return apiFetch('/pipeline/generate-plan', {
    method: 'POST',
    body: JSON.stringify(req),
  });
}

export async function streamPlan(req: LearnerProfileRequest): Promise<ReadableStream> {
  const token = getAccessToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}/pipeline/stream`, {
    method: 'POST',
    headers,
    body: JSON.stringify(req),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Stream failed' }));
    throw new Error(err.detail || `Stream error ${res.status}`);
  }
  return res.body as unknown as ReadableStream;
}

// ── Quiz ────────────────────────────────────────────────────
export async function generateQuiz(sourceText: string, numQuestions = 10, difficulty = 'intermediate'): Promise<QuizResponse> {
  return apiFetch('/quiz/generate', {
    method: 'POST',
    body: JSON.stringify({ source_text: sourceText, num_questions: numQuestions, difficulty }),
  });
}

export async function listQuizzes(): Promise<any[]> {
  return apiFetch('/quiz/list');
}

export async function getQuiz(quizId: string): Promise<QuizResponse> {
  return apiFetch(`/quiz/${quizId}`);
}

export async function submitQuizAttempt(attempt: QuizAttemptRequest): Promise<QuizResult> {
  return apiFetch('/quiz/attempt', {
    method: 'POST',
    body: JSON.stringify(attempt),
  });
}

export async function uploadQuizFile(file: File, numQuestions = 5, difficulty = 'intermediate'): Promise<QuizResponse> {
  const token = getAccessToken();
  const formData = new FormData();
  formData.append('file', file);
  formData.append('num_questions', numQuestions.toString());
  formData.append('difficulty', difficulty);

  const headers: Record<string, string> = {};
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}/quiz/upload`, {
    method: 'POST',
    headers,
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'File upload failed' }));
    throw new Error(err.detail || `Upload error ${res.status}`);
  }
  return res.json();
}

// ── Courses & Catalogs ───────────────────────────────────────
export async function getCourses(params?: { domain?: string; source?: string; search?: string }): Promise<any[]> {
  const query = new URLSearchParams();
  if (params?.domain && params.domain !== 'all') query.set('domain', params.domain);
  if (params?.source && params.source !== 'all') query.set('source', params.source);
  if (params?.search) query.set('search', params.search);
  const qStr = query.toString();
  return apiFetch(`/courses${qStr ? `?${qStr}` : ''}`);
}

export async function enrollInCourse(courseId: string): Promise<{ status: string; message: string }> {
  return apiFetch('/courses/enroll', {
    method: 'POST',
    body: JSON.stringify({ course_id: courseId }),
  });
}

export async function getEnrolledCourses(): Promise<any[]> {
  return apiFetch('/courses/enrolled');
}

export async function getMyGaps(): Promise<any> {
  return apiFetch('/competency/my-gaps');
}

// ── Analytics ───────────────────────────────────────────────
export async function getLearnerAnalytics(): Promise<any> {
  return apiFetch('/analytics/learner');
}

export async function getAdminAnalytics(): Promise<AdminAnalyticsResponse> {
  return apiFetch('/analytics/admin');
}

export async function getLearningHours(): Promise<LearningHoursResponse> {
  return apiFetch('/learning/hours');
}

// ── Virtual Assistant ───────────────────────────────────────
export async function chatWithAssistant(req: AssistantRequest): Promise<AssistantResponse> {
  return apiFetch('/assistant', {
    method: 'POST',
    body: JSON.stringify(req),
  });
}

// ── Health ──────────────────────────────────────────────────
export async function healthCheck(): Promise<HealthResponse> {
  return apiFetch('/health', {}, true);
}
