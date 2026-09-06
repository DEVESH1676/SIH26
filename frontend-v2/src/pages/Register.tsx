/**
 * Registration page — wired to POST /api/auth/register.
 * Matches KarmaSetu's portal design.
 */
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import {
  ArrowLeft, ArrowRight, LockKeyhole, Mail, Network, ShieldCheck, UserRound, Building2,
} from 'lucide-react';
import { useAuthStore } from '../store/useAuthStore';
import { Brand } from '../components/Landing';

export default function Register() {
  const navigate = useNavigate();
  const { register, isLoading, error, clearError } = useAuthStore();
  const [form, setForm] = useState({
    username: '', email: '', password: '', designation: '', department: '',
  });

  const update = (key: string, value: string) => setForm((f) => ({ ...f, [key]: value }));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();
    try {
      await register(form);
      toast.success('Account created! Redirecting to login...');
      setTimeout(() => navigate('/login'), 1500);
    } catch {
      // error in store
    }
  };

  return (
    <div className="portal-page">
      <header className="portal-header">
        <Brand />
        <button className="return-home" onClick={() => navigate('/')}><ArrowLeft size={16} /> Return to Home</button>
      </header>

      <div className="login-wrap">
        <div className="login-card fade-up" style={{ maxWidth: 500 }}>
          <div className="brand brand-compact" style={{ justifyContent: 'center' }}>
            <span className="brand-mark"><Network size={17} /></span>
            <span><strong>KarmaSetu</strong></span>
          </div>
          <h1>Create Your Account</h1>
          <p className="login-subtitle">Join the National Capacity Bridge platform</p>

          {error && (
            <div style={{ background: '#fff0f0', border: '1px solid #ffc4c4', color: '#c62828', borderRadius: 8, padding: '10px 14px', marginBottom: 18, fontSize: 12, textAlign: 'center' }}>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <label>Username
              <div className="input-wrap">
                <UserRound size={17} />
                <input placeholder="Choose a username (min 3 chars)" value={form.username} onChange={(e) => update('username', e.target.value)} required minLength={3} />
              </div>
            </label>

            <label>Official Email
              <div className="input-wrap">
                <Mail size={17} />
                <input type="email" placeholder="name@gov.in" value={form.email} onChange={(e) => update('email', e.target.value)} required />
              </div>
            </label>

            <label>Password
              <div className="input-wrap">
                <LockKeyhole size={17} />
                <input type="password" placeholder="Minimum 8 characters" value={form.password} onChange={(e) => update('password', e.target.value)} required minLength={8} />
              </div>
            </label>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
              <label>Designation
                <div className="input-wrap">
                  <ShieldCheck size={17} />
                  <input placeholder="e.g. Statistical Officer" value={form.designation} onChange={(e) => update('designation', e.target.value)} required />
                </div>
              </label>
              <label>Department
                <div className="input-wrap">
                  <Building2 size={17} />
                  <input placeholder="e.g. MoSPI" value={form.department} onChange={(e) => update('department', e.target.value)} required />
                </div>
              </label>
            </div>

            <button type="submit" className="primary-button full" disabled={isLoading} style={{ marginTop: 16 }}>
              {isLoading ? 'Creating Account...' : 'Register'} <ArrowRight size={17} />
            </button>
          </form>

          <div className="login-help">
            Already have an account? <Link to="/login" style={{ color: '#125fc1', fontWeight: 700 }}>Sign In</Link>
          </div>
        </div>
      </div>

      <footer className="portal-footer">
        <span><ShieldCheck size={14} /> MeitY & NIC Certified • 256-bit TLS</span>
        <span>© 2024 Digital India / SIH-2024</span>
      </footer>
    </div>
  );
}
