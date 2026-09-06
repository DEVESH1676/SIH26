/**
 * KarmaSetu — Main Application with React Router.
 * Routes: Landing, Login, Register, Onboarding, Dashboard, Courses, Quiz, Analytics, Admin.
 */
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';

// Layouts
import AppLayout from './layouts/AppLayout';

// Components
import ProtectedRoute from './components/ProtectedRoute';
import Landing from './components/Landing';
import ProfileFlow from './components/ProfileFlow';

// Pages
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Courses from './pages/Courses';
import QuizTake from './pages/QuizTake';
import Analytics from './pages/Analytics';
import AdminPanel from './pages/AdminPanel';

export default function App() {
  return (
    <BrowserRouter>
      <Toaster
        position="top-right"
        toastOptions={{
          style: {
            background: '#fff',
            color: '#102442',
            border: '1px solid #e1e6ef',
            borderRadius: '10px',
            fontSize: '13px',
            fontFamily: "'DM Sans', sans-serif",
          },
        }}
      />
      <div className="app-shell">
        <Routes>
          {/* Public routes */}
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/onboarding" element={<ProfileFlow />} />

          {/* Protected routes (require auth) */}
          <Route element={<ProtectedRoute><AppLayout /></ProtectedRoute>}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/courses" element={<Courses />} />
            <Route path="/quiz" element={<QuizTake />} />
            <Route path="/quiz/:quizId" element={<QuizTake />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/admin" element={<AdminPanel />} />
          </Route>
        </Routes>
      </div>
    </BrowserRouter>
  );
}
