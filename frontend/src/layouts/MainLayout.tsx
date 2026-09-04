/**
 * Main layout with role-aware sidebar navigation.
 */
import { useAuthStore } from '../store/useAuthStore';
import { useTranslation } from 'react-i18next';
import { Link, useLocation, Outlet } from 'react-router-dom';

const navItems = [
  { path: '/', label: 'nav.home', icon: '🏠' },
  { path: '/courses', label: 'nav.courses', icon: '📚' },
  { path: '/analytics', label: 'nav.analytics', icon: '📊' },
  { path: '/profile', label: 'nav.profile', icon: '👤' },
];

export default function MainLayout() {
  const { user, logout } = useAuthStore();
  const { t } = useTranslation();
  const location = useLocation();

  const isAdmin = user?.roles?.includes('admin');

  return (
    <div className="relative flex h-screen overflow-hidden bg-[var(--bg)] text-white">
      {/* Animated Background */}
      <div className="absolute inset-0 animate-aurora opacity-10 pointer-events-none"></div>

      {/* Sidebar */}
      <aside className="relative z-20 w-64 glass flex flex-col border-r border-white/10 shrink-0">
        <div className="p-6 border-b border-white/10">
          <h1 className="text-2xl font-black bg-clip-text text-transparent bg-gradient-to-r from-[var(--primary)] to-[var(--accent)]">
            MoSPI AI
          </h1>
          <p className="text-xs text-[var(--text-muted)] tracking-wider uppercase mt-1 font-semibold">Learning Platform</p>
        </div>
        
        <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
          {navItems.map(item => {
            const isActive = location.pathname === item.path || (item.path !== '/' && location.pathname.startsWith(item.path));
            return (
              <Link
                key={item.path}
                to={isAdmin && item.path === '/analytics' ? '/admin' : item.path}
                className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 ${
                  isActive
                    ? 'bg-gradient-to-r from-[var(--primary)]/20 to-transparent border-l-2 border-[var(--primary)] text-white'
                    : 'text-[var(--text-muted)] hover:bg-white/5 hover:text-white'
                }`}
              >
                <span className="text-xl">{item.icon}</span>
                <span className="font-medium">{t(item.label)}</span>
              </Link>
            );
          })}
          
          {isAdmin && (
            <Link to="/admin" className="flex items-center gap-3 px-4 py-3 rounded-xl bg-orange-500/10 text-orange-200 border border-orange-500/20 hover:bg-orange-500/20 transition-all mt-4">
              <span>🛡️</span><span className="font-semibold">Admin Panel</span>
            </Link>
          )}
        </nav>
        
        <div className="p-5 border-t border-white/10 bg-black/20">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-full bg-gradient-to-tr from-[var(--secondary)] to-[var(--accent)] flex items-center justify-center text-white font-bold shadow-lg">
              {user?.username?.[0]?.toUpperCase() || 'U'}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold truncate text-white">{user?.username}</p>
              <p className="text-xs text-[var(--primary)] truncate">{user?.designation}</p>
            </div>
          </div>
          <button 
            onClick={logout} 
            className="mt-4 w-full flex items-center justify-center gap-2 py-2 px-4 rounded-lg bg-red-500/10 text-red-400 border border-red-500/20 hover:bg-red-500/20 transition-all"
          >
            <span>🚪</span>
            <span className="font-medium text-sm">Logout</span>
          </button>
        </div>
      </aside>

      {/* Main content */}
      <main className="relative z-10 flex-1 flex flex-col h-screen overflow-hidden">
        <header className="glass shadow-sm px-8 py-4 flex items-center justify-between border-b border-white/10 shrink-0">
          <h2 className="text-xl font-bold text-white tracking-tight">
            {t('dashboard.welcome', { name: user?.username })}
          </h2>
          <div className="flex items-center gap-4">
            <select className="bg-black/20 border border-white/10 rounded-lg px-3 py-2 text-sm text-[var(--text-muted)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]/50">
              <option value="en">English</option>
              <option value="hi">हिंदी</option>
              <option value="bn">বাংলা</option>
            </select>
          </div>
        </header>
        <div className="flex-1 overflow-y-auto p-8 relative">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
