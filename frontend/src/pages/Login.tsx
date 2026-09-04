import { useState } from 'react';
import { useAuthStore } from '../store/useAuthStore';
import { useNavigate, Link } from 'react-router-dom';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const { login, isLoading } = useAuthStore();
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg('');
    try {
      await login(username, password);
      navigate('/');
    } catch (err: any) {
      setErrorMsg(err.message || 'Login failed');
    }
  };

  const demoLogin = (e: React.MouseEvent) => {
    e.preventDefault();
    setUsername('admin');
    setPassword('admin123');
  };

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-[var(--bg)]">
      {/* Animated Background */}
      <div className="absolute inset-0 animate-aurora opacity-20 pointer-events-none"></div>
      
      {/* Floating Neural Particles */}
      {[...Array(15)].map((_, i) => (
        <div 
          key={i} 
          className="neural-particle" 
          style={{ 
            left: `${Math.random() * 100}%`, 
            top: `${Math.random() * 100}%`,
            animationDelay: `${Math.random() * 5}s`,
            animationDuration: `${5 + Math.random() * 10}s`
          }}
        ></div>
      ))}

      {/* Glassmorphism Card */}
      <div className="relative z-10 w-full max-w-md p-8 m-4 rounded-3xl glass backdrop-blur-3xl border border-white/10 shadow-2xl">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-black tracking-tighter bg-clip-text text-transparent bg-gradient-to-r from-[var(--primary)] to-[var(--accent)]">
            MoSPI Platform
          </h1>
          <p className="text-[var(--text-muted)] mt-2 font-medium tracking-wide">Enter your credentials to continue</p>
        </div>

        {errorMsg && (
          <div className="bg-red-500/10 border border-red-500/50 text-red-400 p-3 rounded-xl mb-6 text-sm text-center">
            {errorMsg}
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-6">
          <div className="space-y-2">
            <label className="text-xs uppercase tracking-wider text-[var(--text-muted)] font-semibold ml-1">Username</label>
            <input 
              className="w-full bg-white/5 border border-white/10 rounded-xl p-3.5 text-white placeholder-white/30 focus:outline-none focus:ring-2 focus:ring-[var(--primary)]/50 transition-all duration-300" 
              placeholder="e.g. admin" 
              value={username} 
              onChange={e => setUsername(e.target.value)} 
              required
            />
          </div>
          
          <div className="space-y-2">
            <label className="text-xs uppercase tracking-wider text-[var(--text-muted)] font-semibold ml-1">Password</label>
            <input 
              className="w-full bg-white/5 border border-white/10 rounded-xl p-3.5 text-white placeholder-white/30 focus:outline-none focus:ring-2 focus:ring-[var(--primary)]/50 transition-all duration-300" 
              type="password" 
              placeholder="••••••••" 
              value={password} 
              onChange={e => setPassword(e.target.value)} 
              required
            />
          </div>

          <button 
            disabled={isLoading}
            className="group relative w-full bg-gradient-to-r from-[var(--secondary)] to-[var(--accent)] text-white font-bold text-lg p-3.5 rounded-xl overflow-hidden transition-all duration-300 hover:scale-[1.02] active:scale-95 disabled:opacity-70"
          >
            <span className="relative z-10 flex items-center justify-center gap-2">
              {isLoading ? 'Authenticating...' : 'Sign In'}
            </span>
            <div className="absolute inset-0 h-full w-full bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300 ease-out"></div>
          </button>
        </form>

        <div className="mt-8 flex flex-col gap-4 text-center text-sm text-[var(--text-muted)]">
          <button 
            onClick={demoLogin}
            className="hover:text-[var(--primary)] transition-colors inline-block underline decoration-white/20 underline-offset-4"
          >
            Fill Demo Credentials
          </button>
          
          <div className="h-px w-full bg-gradient-to-r from-transparent via-white/10 to-transparent"></div>

          <p>
            Don't have an account?{' '}
            <Link to="/register" className="text-[var(--primary)] font-semibold hover:text-white transition-colors">
              Register now
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
