/**
 * Login page — wired to POST /api/auth/login via the auth store.
 * Matches KarmaSetu's existing portal design.
 */
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  ArrowLeft, ArrowRight, Eye, EyeOff, Landmark,
  LockKeyhole, Network, ShieldCheck, UserRound,
} from 'lucide-react';
import { useAuthStore } from '../store/useAuthStore';
import { Brand } from '../components/Landing';

function PortalHeader({ onBack }: { onBack: () => void }) {
  return (
    <header className="portal-header">
      <Brand />
      <button className="return-home" onClick={onBack}><ArrowLeft size={16} /> Return to Home</button>
    </header>
  );
}

function PortalFooter() {
  return (
    <footer className="portal-footer">
      <span><ShieldCheck size={14} /> MeitY & NIC Certified • 256-bit TLS</span>
      <span>Helpdesk &nbsp; • &nbsp; Data Security Policy &nbsp; • &nbsp; © 2024 Digital India / SIH-2024</span>
    </footer>
  );
}

export default function Login() {
  const navigate = useNavigate();
  const { login, isLoading, error, clearError } = useAuthStore();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();
    try {
      await login(username, password);
      navigate('/dashboard');
    } catch {
      // error is set in store
    }
  };

  const demoLogin = () => {
    setUsername('admin');
    setPassword('admin123');
  };

  return (
    <div className="portal-page">
      <PortalHeader onBack={() => navigate('/')} />

      <div className="login-wrap">
        <div className="login-card fade-up">
          <div className="brand brand-compact" style={{ justifyContent: 'center' }}>
            <span className="brand-mark"><Network size={17} /></span>
            <span><strong>KarmaSetu</strong></span>
          </div>
          <h1>Welcome to KarmaSetu</h1>
          <p className="login-subtitle">Select your portal to continue</p>

          <div className="portal-toggle">
            <button className="selected"><UserRound size={18} /> Officer / Employee</button>
            <button><Landmark size={18} /> MDO / Department Admin</button>
          </div>

          {error && (
            <div style={{ background: '#fff0f0', border: '1px solid #ffc4c4', color: '#c62828', borderRadius: 8, padding: '10px 14px', marginBottom: 18, fontSize: 12, textAlign: 'center' }}>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <label>Official Email / Karmayogi ID
              <div className="input-wrap">
                <UserRound size={17} />
                <input placeholder="name@gov.in or CADRE-ID" value={username} onChange={(e) => setUsername(e.target.value)} required />
              </div>
            </label>

            <div className="label-row">
              <label>Password</label>
              <button type="button" className="text-button" onClick={demoLogin}>Demo Credentials</button>
            </div>
            <div className="input-wrap">
              <LockKeyhole size={17} />
              <input type={showPassword ? 'text' : 'password'} placeholder="••••••••••••" value={password} onChange={(e) => setPassword(e.target.value)} required />
              <button type="button" className="input-action" onClick={() => setShowPassword(!showPassword)} aria-label="Show password">
                {showPassword ? <EyeOff size={17} /> : <Eye size={17} />}
              </button>
            </div>

            <label className="remember"><input type="checkbox" /> Remember credentials</label>

            <button type="submit" className="primary-button full" disabled={isLoading}>
              {isLoading ? 'Signing In...' : 'Sign In to Portal'} <ArrowRight size={17} />
            </button>
          </form>

          <div className="login-help">
            Don't have an account? <Link to="/register" style={{ color: '#125fc1', fontWeight: 700 }}>Register now</Link>
            <br /><br />
            Need assistance? Contact Nodal Officer or call <strong>1800–111–555</strong>
          </div>
        </div>
      </div>

      <PortalFooter />
    </div>
  );
}
