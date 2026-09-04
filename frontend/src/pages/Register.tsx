import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

export default function Register() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    designation: '',
    department: '',
    role: 'learner'
  });
  const [errorMsg, setErrorMsg] = useState('');
  const [successMsg, setSuccessMsg] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg('');
    setSuccessMsg('');
    setIsLoading(true);
    
    try {
      const res = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Registration failed');
      
      setSuccessMsg('Registration successful! Redirecting to login...');
      setTimeout(() => navigate('/login'), 2000);
    } catch (err: any) {
      setErrorMsg(err.message || 'Registration failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-[var(--bg)] py-12">
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
            Create Account
          </h1>
          <p className="text-[var(--text-muted)] mt-2 font-medium tracking-wide">Join the MoSPI Platform</p>
        </div>

        {errorMsg && (
          <div className="bg-red-500/10 border border-red-500/50 text-red-400 p-3 rounded-xl mb-6 text-sm text-center">
            {errorMsg}
          </div>
        )}
        
        {successMsg && (
          <div className="bg-green-500/10 border border-green-500/50 text-green-400 p-3 rounded-xl mb-6 text-sm text-center">
            {successMsg}
          </div>
        )}

        <form onSubmit={handleRegister} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2 col-span-2">
              <label className="text-xs uppercase tracking-wider text-[var(--text-muted)] font-semibold ml-1">Username</label>
              <input 
                name="username"
                className="w-full bg-white/5 border border-white/10 rounded-xl p-3 text-white placeholder-white/30 focus:outline-none focus:ring-2 focus:ring-[var(--primary)]/50 transition-all duration-300" 
                placeholder="Choose a username" 
                value={formData.username} 
                onChange={handleChange} 
                required
                minLength={3}
              />
            </div>

            <div className="space-y-2 col-span-2">
              <label className="text-xs uppercase tracking-wider text-[var(--text-muted)] font-semibold ml-1">Email</label>
              <input 
                name="email"
                type="email"
                className="w-full bg-white/5 border border-white/10 rounded-xl p-3 text-white placeholder-white/30 focus:outline-none focus:ring-2 focus:ring-[var(--primary)]/50 transition-all duration-300" 
                placeholder="you@domain.com" 
                value={formData.email} 
                onChange={handleChange} 
                required
              />
            </div>
            
            <div className="space-y-2 col-span-2">
              <label className="text-xs uppercase tracking-wider text-[var(--text-muted)] font-semibold ml-1">Password</label>
              <input 
                name="password"
                type="password"
                className="w-full bg-white/5 border border-white/10 rounded-xl p-3 text-white placeholder-white/30 focus:outline-none focus:ring-2 focus:ring-[var(--primary)]/50 transition-all duration-300" 
                placeholder="Minimum 8 characters" 
                value={formData.password} 
                onChange={handleChange} 
                required
                minLength={8}
              />
            </div>

            <div className="space-y-2">
              <label className="text-xs uppercase tracking-wider text-[var(--text-muted)] font-semibold ml-1">Designation</label>
              <input 
                name="designation"
                className="w-full bg-white/5 border border-white/10 rounded-xl p-3 text-white placeholder-white/30 focus:outline-none focus:ring-2 focus:ring-[var(--primary)]/50 transition-all duration-300" 
                placeholder="e.g. Analyst" 
                value={formData.designation} 
                onChange={handleChange} 
                required
              />
            </div>

            <div className="space-y-2">
              <label className="text-xs uppercase tracking-wider text-[var(--text-muted)] font-semibold ml-1">Department</label>
              <input 
                name="department"
                className="w-full bg-white/5 border border-white/10 rounded-xl p-3 text-white placeholder-white/30 focus:outline-none focus:ring-2 focus:ring-[var(--primary)]/50 transition-all duration-300" 
                placeholder="e.g. IT" 
                value={formData.department} 
                onChange={handleChange} 
                required
              />
            </div>
          </div>

          <button 
            disabled={isLoading}
            className="group relative w-full bg-gradient-to-r from-[var(--secondary)] to-[var(--accent)] text-white font-bold text-lg p-3.5 rounded-xl overflow-hidden transition-all duration-300 hover:scale-[1.02] active:scale-95 disabled:opacity-70 mt-4"
          >
            <span className="relative z-10 flex items-center justify-center gap-2">
              {isLoading ? 'Creating Account...' : 'Register'}
            </span>
            <div className="absolute inset-0 h-full w-full bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300 ease-out"></div>
          </button>
        </form>

        <div className="mt-8 flex flex-col gap-4 text-center text-sm text-[var(--text-muted)]">
          <div className="h-px w-full bg-gradient-to-r from-transparent via-white/10 to-transparent"></div>

          <p>
            Already have an account?{' '}
            <Link to="/login" className="text-[var(--primary)] font-semibold hover:text-white transition-colors">
              Sign In
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
