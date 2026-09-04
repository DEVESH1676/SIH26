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
import Register from './pages/Register';

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
        <Route path="/register" element={<Register />} />
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
