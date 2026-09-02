# Part 9 — Frontend Restructuring

## Objective
Transform the React 19 frontend from IT ticket dashboard to MoSPI learning platform with role-based dashboards, course catalog, quiz interface, file upload, analytics, multi-language support, and responsive design.

## 9.1 Update `frontend-v2/package.json`

```json
{
  "name": "mospi-learning-platform",
  "version": "2.0.0",
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "react-router-dom": "^6.28.0",
    "react-i18next": "^15.2.0",
    "i18next": "^24.0.0",
    "i18next-browser-languagedetector": "^8.0.0",
    "zustand": "^5.0.0",
    "react-hot-toast": "^2.4.0",
    "react-dropzone": "^14.3.0",
    "recharts": "^2.15.0",
    "@headlessui/react": "^2.2.0",
    "@heroicons/react": "^2.2.0",
    "axios": "^1.7.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.5.0"
  },
  "devDependencies": {
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "@vitejs/plugin-react": "^4.3.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.6.0",
    "vite": "^6.0.0",
    "vitest": "^2.0.0"
  }
}
```

## 9.2 Create `frontend-v2/src/i18n.ts` (NEW FILE)

```typescript
/**
 * Multi-language i18n configuration.
 * Supports English, Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Urdu, etc.
 */
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

const resources = {
  en: {
    translation: {
      nav: { home: 'Home', courses: 'Courses', quizzes: 'Quizzes', analytics: 'Analytics', profile: 'Profile' },
      dashboard: { welcome: 'Welcome, {{name}}', your_progress: 'Your Learning Progress', recommended: 'Recommended for You', skill_gaps: 'Skill Gaps Identified' },
      course: { title: 'Title', duration: 'Duration', difficulty: 'Difficulty', enroll: 'Enroll Now', start: 'Start Course', progress: 'Progress' },
      quiz: { take_quiz: 'Take Quiz', submit: 'Submit Answers', score: 'Score', pass: 'Pass', fail: 'Try Again', explanation: 'Explanation' },
      upload: { upload_file: 'Upload Learning Material', supported_formats: 'Supported: PDF, DOCX, PPTX, MP4, MP3', generate_quiz: 'Generate Quiz' },
      admin: { overview: 'Overview', workforce: 'Workforce Analytics', training: 'Training Effectiveness', predictive: 'Predictive Insights' },
      assistant: { type_message: 'Type your question...', response: 'Assistant Response', suggest: 'Suggestions' },
    },
  },
  hi: {
    translation: {
      nav: { home: 'होम', courses: 'कोर्सेज', quizzes: 'क्विज़', analytics: 'विश्लेषण', profile: 'प्रोफ़ाइल' },
      dashboard: { welcome: 'स्वागत है, {{name}}', your_progress: 'आपकी शिक्षा प्रगति', recommended: 'आपके लिए अनुशंसित', skill_gaps: 'कौशल अंतर पहचाने गए' },
      course: { title: 'शीर्षक', duration: 'अवधि', difficulty: 'कठिनाई', enroll: 'अभी नामांकन करें', start: 'कोर्स शुरू करें', progress: 'प्रगति' },
      quiz: { take_quiz: 'क्विज़ लें', submit: 'उत्तर जमा करें', score: 'अंक', pass: 'पार', fail: 'फिर से प्रयास करें', explanation: 'व्याख्या' },
      upload: { upload_file: 'शिक्षा सामग्री अपलोड करें', supported_formats: 'समर्थित: PDF, DOCX, PPTX, MP4, MP3', generate_quiz: 'क्विज़ उत्पन्न करें' },
      admin: { overview: 'अवलोकन', workforce: 'कार्यबल विश्लेषण', training: 'प्रशिक्षण प्रभावकारिता', predictive: 'पूर्वानुमानित अंतर्दृष्टि' },
      assistant: { type_message: 'अपना प्रश्न लिखें...', response: 'सहायक उत्तर', suggest: 'सुझाव' },
    },
  },
  // Add more languages: bn, ta, te, mr, gu, ur, pa, ml, or, etc.
} as const;

i18n.use(LanguageDetector).use(initReactI18next).init({
  resources,
  fallbackLng: 'en',
  interpolation: { escapeValue: false },
});

export default i18n;
```

## 9.3 Create `frontend-v2/src/store/useAuthStore.ts` (NEW FILE)

```typescript
/**
 * Zustand store for authentication state management.
 */
import { create } from 'zustand';

interface User {
  user_id: string;
  username: string;
  email: string;
  designation: string;
  department: string;
  roles: string[];
}

interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  refreshTokens: () => Promise<void>;
  loadProfile: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  accessToken: null,
  refreshToken: null,
  isAuthenticated: false,
  isLoading: false,

  login: async (username: string, password: string) => {
    set({ isLoading: true });
    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
      if (!res.ok) throw new Error('Invalid credentials');
      const data = await res.json();
      set({
        user: { user_id: data.user_id, username: data.username, email: '', designation: '', department: '', roles: data.roles },
        accessToken: data.access_token,
        refreshToken: data.refresh_token,
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (e: any) {
      set({ isLoading: false });
      throw e;
    }
  },

  logout: () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    set({ user: null, accessToken: null, refreshToken: null, isAuthenticated: false });
  },

  refreshTokens: async () => {
    const { refreshToken } = get();
    if (!refreshToken) return;
    try {
      const res = await fetch('/api/auth/refresh', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${refreshToken}` },
      });
      if (!res.ok) throw new Error('Refresh failed');
      const data = await res.json();
      set({ accessToken: data.access_token });
      localStorage.setItem('accessToken', data.access_token);
    } catch (e) {
      get().logout();
    }
  },

  loadProfile: async () => {
    const { accessToken } = get();
    if (!accessToken) return;
    try {
      const res = await fetch('/api/auth/me', {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      if (!res.ok) throw new Error('Failed to load profile');
      const user = await res.json();
      set({ user, isAuthenticated: true });
    } catch (e) {
      get().logout();
    }
  },
}));
```

## 9.4 Create `frontend-v2/src/store/useAnalyticsStore.ts` (NEW FILE)

```typescript
/**
 * Store for analytics data (learner and admin).
 */
import { create } from 'zustand';

interface AnalyticsState {
  learnerData: any;
  adminData: any;
  isLoading: boolean;
  fetchLearnerData: () => Promise<void>;
  fetchAdminData: () => Promise<void>;
}

export const useAnalyticsStore = create<AnalyticsState>((set) => ({
  learnerData: null,
  adminData: null,
  isLoading: false,

  fetchLearnerData: async () => {
    set({ isLoading: true });
    try {
      const res = await fetch('/api/analytics/learner', {
        headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` },
      });
      const data = await res.json();
      set({ learnerData: data, isLoading: false });
    } catch (e) {
      set({ isLoading: false });
    }
  },

  fetchAdminData: async () => {
    set({ isLoading: true });
    try {
      const res = await fetch('/api/analytics/admin', {
        headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` },
      });
      const data = await res.json();
      set({ adminData: data, isLoading: false });
    } catch (e) {
      set({ isLoading: false });
    }
  },
}));
```

## 9.5 Replace `frontend-v2/src/App.tsx`

```typescript
/**
 * Main app with route-based layout for learning platform.
 */
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import './i18n';
import { useAuthStore } from './store/useAuthStore';

// Layouts
import MainLayout from './layouts/MainLayout';

// Pages
import Dashboard from './pages/Dashboard';
import Courses from './pages/Courses';
import QuizTake from './pages/QuizTake';
import QuizResults from './pages/QuizResults';
import Analytics from './pages/Analytics';
import Profile from './pages/Profile';
import AdminPanel from './pages/AdminPanel';
import VirtualAssistant from './components/Assistant/VirtualAssistant';
import Login from './pages/Login';

// Auth guard
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuthStore();
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Toaster position="top-right" />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <MainLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Dashboard />} />
          <Route path="courses" element={<Courses />} />
          <Route path="quiz/:quizId" element={<QuizTake />} />
          <Route path="quiz/:quizId/results" element={<QuizResults />} />
          <Route path="analytics" element={<Analytics />} />
          <Route path="profile" element={<Profile />} />
          <Route path="admin/*" element={<AdminPanel />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
```

## 9.6 Replace `frontend-v2/src/layouts/MainLayout.tsx`

```typescript
/**
 * Main layout with role-aware sidebar navigation.
 */
import { useAuthStore } from '../store/useAuthStore';
import { useTranslation } from 'react-i18next';
import { Link, useLocation } from 'react-router-dom';

const navItems = [
  { path: '/', label: 'nav.home', icon: '🏠' },
  { path: '/courses', label: 'nav.courses', icon: '📚' },
  { path: '/analytics', label: 'nav.analytics', icon: '📊' },
  { path: '/profile', label: 'nav.profile', icon: '👤' },
];

export default function MainLayout({ children }: { children: React.ReactNode }) {
  const { user, logout } = useAuthStore();
  const { t } = useTranslation();
  const location = useLocation();

  const isAdmin = user?.roles?.includes('admin');
  const isTrainer = user?.roles?.includes('trainer');

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className="w-64 bg-gradient-to-b from-indigo-700 to-indigo-900 text-white flex flex-col">
        <div className="p-6 border-b border-indigo-600">
          <h1 className="text-xl font-bold">🏛️ MoSPI</h1>
          <p className="text-xs text-indigo-300 mt-1">Learning Platform</p>
        </div>
        <nav className="flex-1 p-4 space-y-1">
          {navItems.map(item => (
            <Link
              key={item.path}
              to={isAdmin && item.path === '/analytics' ? '/admin' : item.path}
              className={`flex items-center gap-3 px-4 py-2 rounded-lg transition ${
                location.pathname === item.path
                  ? 'bg-white/20 font-semibold'
                  : 'hover:bg-white/10'
              }`}
            >
              <span>{item.icon}</span>
              <span>{t(item.label)}</span>
            </Link>
          ))}
          {isAdmin && (
            <Link to="/admin" className="flex items-center gap-3 px-4 py-2 rounded-lg bg-amber-600/30 hover:bg-amber-600/40">
              <span>🛡️</span><span>Admin Panel</span>
            </Link>
          )}
        </nav>
        <div className="p-4 border-t border-indigo-600">
          <p className="text-sm">{user?.username}</p>
          <p className="text-xs text-indigo-300">{user?.designation}</p>
          <button onClick={logout} className="mt-2 text-sm text-red-300 hover:text-red-200">
            Logout
          </button>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-y-auto">
        <header className="bg-white shadow-sm px-6 py-4 flex items-center justify-between">
          <h2 className="text-xl font-semibold text-gray-800">{t('dashboard.welcome', { name: user?.username })}</h2>
          <div className="flex items-center gap-4">
            {/* Language selector */}
            <select className="border rounded px-2 py-1 text-sm">
              <option value="en">English</option>
              <option value="hi">हिंदी</option>
              <option value="bn">বাংলা</option>
            </select>
          </div>
        </header>
        <div className="p-6">{children}</div>
      </main>
    </div>
  );
}
```

## 9.7 Create `frontend-v2/src/pages/Dashboard.tsx` (NEW FILE)

```typescript
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
```

## 9.8 Create `frontend-v2/src/pages/Courses.tsx` (NEW FILE)

```typescript
/**
 * Course catalog page — displays iGOT and local courses.
 */
import { useState } from 'react';

export default function Courses() {
  const [search, setSearch] = useState('');
  const [domain, setDomain] = useState('all');

  const domains = ['all', 'statistical', 'technical', 'digital_governance', 'behavioural'];

  // Mock data — will be replaced with API call
  const courses = [
    { id: '1', title: 'Principles of Survey Design', domain: 'statistical', duration: '8 hours', difficulty: 'Beginner' },
    { id: '2', title: 'Sampling Techniques for Official Statistics', domain: 'statistical', duration: '12 hours', difficulty: 'Intermediate' },
    { id: '3', title: 'National Accounts Methodology', domain: 'statistical', duration: '16 hours', difficulty: 'Advanced' },
    { id: '4', title: 'Digital Governance Framework', domain: 'digital_governance', duration: '6 hours', difficulty: 'Beginner' },
  ];

  const filtered = courses.filter(c => {
    const matchSearch = c.title.toLowerCase().includes(search.toLowerCase());
    const matchDomain = domain === 'all' || c.domain === domain;
    return matchSearch && matchDomain;
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">📚 Course Catalog</h1>

      {/* Filters */}
      <div className="flex gap-4">
        <input
          type="text"
          placeholder="Search courses..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="flex-1 border rounded-lg px-4 py-2"
        />
        <select value={domain} onChange={e => setDomain(e.target.value)} className="border rounded-lg px-4 py-2">
          {domains.map(d => <option key={d} value={d}>{d === 'all' ? 'All Domains' : d.replace('_', ' ').replace(/\b\w/g, c => c.toUpperCase())}</option>)}
        </select>
      </div>

      {/* Course Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map(course => (
          <div key={course.id} className="bg-white rounded-xl p-5 shadow-sm border border-gray-100 hover:shadow-md transition">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-medium px-2 py-1 bg-indigo-100 text-indigo-700 rounded-full">
                {course.domain.replace('_', ' ')}
              </span>
              <span className={`text-xs font-medium px-2 py-1 rounded-full ${
                course.difficulty === 'Beginner' ? 'bg-green-100 text-green-700' :
                course.difficulty === 'Intermediate' ? 'bg-yellow-100 text-yellow-700' :
                'bg-red-100 text-red-700'
              }`}>{course.difficulty}</span>
            </div>
            <h3 className="font-semibold text-gray-900 mb-1">{course.title}</h3>
            <p className="text-sm text-gray-500 mb-4">{course.duration}</p>
            <button className="w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700">
              Enroll Now
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
```

## 9.9 Create `frontend-v2/src/components/Upload/FileUpload.tsx` (NEW FILE)

```typescript
/**
 * File upload component with drag-and-drop.
 */
import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

export default function FileUpload({ onFileSelect }: { onFileSelect: (file: File) => void }) {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles[0]) onFileSelect(acceptedFiles[0]);
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx'],
      'video/mp4': ['.mp4'],
      'audio/mpeg': ['.mp3'],
    },
  });

  return (
    <div
      {...getRootProps()}
      className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition ${
        isDragActive ? 'border-indigo-500 bg-indigo-50' : 'border-gray-300 hover:border-indigo-400'
      }`}
    >
      <input {...getInputProps()} />
      <p className="text-lg font-medium text-gray-700">
        {isDragActive ? 'Drop the file here' : 'Drag & drop a file or click to browse'}
      </p>
      <p className="text-sm text-gray-500 mt-2">
        Supported: PDF, DOCX, PPTX, MP4, MP3 (max 100MB)
      </p>
    </div>
  );
}
```

## 9.10 Create `frontend-v2/src/components/Assistant/VirtualAssistant.tsx` (NEW FILE)

```typescript
/**
 * Floating virtual assistant widget.
 */
import { useState } from 'react';

export default function VirtualAssistant() {
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [conversation, setConversation] = useState<{role: string, text: string}[]>([]);

  const handleSend = async () => {
    if (!message.trim()) return;
    setConversation(prev => [...prev, { role: 'user', text: message }]);

    const res = await fetch('/api/assistant/respond', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, language: 'en' }),
    });
    const data = await res.json();
    setConversation(prev => [...prev, { role: 'assistant', text: data.response }]);
    setMessage('');
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {open && (
        <div className="bg-white rounded-xl shadow-2xl w-96 max-h-96 flex flex-col border border-gray-200 mb-4">
          <div className="bg-indigo-600 text-white px-4 py-3 rounded-t-xl flex items-center justify-between">
            <span className="font-semibold">🤖 Learning Assistant</span>
            <button onClick={() => setOpen(false)} className="text-white hover:text-red-200">✕</button>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {conversation.map((c, i) => (
              <div key={i} className={`p-3 rounded-lg ${c.role === 'user' ? 'bg-indigo-100 ml-8' : 'bg-gray-100 mr-8'}`}>
                {c.text}
              </div>
            ))}
          </div>
          <div className="p-3 border-t">
            <div className="flex gap-2">
              <input
                value={message}
                onChange={e => setMessage(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleSend()}
                placeholder="Ask me anything..."
                className="flex-1 border rounded-lg px-3 py-2 text-sm"
              />
              <button onClick={handleSend} className="bg-indigo-600 text-white px-4 py-2 rounded-lg">Send</button>
            </div>
          </div>
        </div>
      )}
      <button
        onClick={() => setOpen(!open)}
        className="w-14 h-14 bg-indigo-600 hover:bg-indigo-700 rounded-full shadow-lg flex items-center justify-center text-white text-2xl"
      >
        {open ? '✕' : '🤖'}
      </button>
    </div>
  );
}
```

## 9.11 Replace `frontend-v2/src/components/Analytics/AnalyticsMock.tsx`

Replace with `frontend-v2/src/pages/Analytics.tsx` that fetches real data from `/api/analytics/learner`.

## 9.12 Verification Checklist

- [ ] `package.json` updated with i18n, react-dropzone, recharts
- [ ] `i18n.ts` multi-language configuration
- [ ] `useAuthStore.ts` Zustand auth store
- [ ] `useAnalyticsStore.ts` analytics data store
- [ ] `App.tsx` with route-based layout
- [ ] `MainLayout.tsx` role-aware sidebar
- [ ] `Dashboard.tsx` learner dashboard with stats
- [ ] `Courses.tsx` course catalog with filters
- [ ] `FileUpload.tsx` drag-and-drop upload
- [ ] `VirtualAssistant.tsx` floating chat widget
- [ ] `Analytics.tsx` real data analytics page
- [ ] All mock data replaced with API calls
- [ ] Responsive design works on mobile
