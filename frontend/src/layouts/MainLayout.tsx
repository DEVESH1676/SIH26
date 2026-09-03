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
