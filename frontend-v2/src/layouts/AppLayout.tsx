/**
 * App layout shell for authenticated pages — sidebar navigation + top bar.
 * Follows KarmaSetu's light theme with DM Sans / Manrope typography.
 */
import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import {
  BarChart3, BookOpen, GraduationCap, LayoutDashboard,
  LogOut, Network, Settings, ShieldCheck, UserRound,
} from 'lucide-react';
import { useAuthStore } from '../store/useAuthStore';

const navItems = [
  { to: '/dashboard', icon: <LayoutDashboard size={18} />, label: 'Dashboard' },
  { to: '/courses', icon: <BookOpen size={18} />, label: 'Courses' },
  { to: '/analytics', icon: <BarChart3 size={18} />, label: 'Analytics' },
];

const adminItems = [
  { to: '/admin', icon: <Settings size={18} />, label: 'Admin Panel' },
];

export default function AppLayout() {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  const isAdmin = user?.roles?.includes('admin');

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="app-layout">
      {/* ── Sidebar ─────────────────────────────────────── */}
      <aside className="app-sidebar">
        <div className="sidebar-brand">
          <span className="brand-mark"><Network size={18} /></span>
          <span><strong>KarmaSetu</strong></span>
        </div>

        <nav className="sidebar-nav">
          <div className="nav-group">
            <span className="nav-label">MAIN</span>
            {navItems.map((item) => (
              <NavLink key={item.to} to={item.to} className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                {item.icon}
                <span>{item.label}</span>
              </NavLink>
            ))}
          </div>

          {isAdmin && (
            <div className="nav-group">
              <span className="nav-label">ADMIN</span>
              {adminItems.map((item) => (
                <NavLink key={item.to} to={item.to} className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                  {item.icon}
                  <span>{item.label}</span>
                </NavLink>
              ))}
            </div>
          )}
        </nav>

        <div className="sidebar-footer">
          <div className="sidebar-user">
            <span className="sidebar-avatar"><UserRound size={14} /></span>
            <div>
              <strong>{user?.username || 'User'}</strong>
              <small>{user?.roles?.[0] || 'learner'}</small>
            </div>
          </div>
          <button className="sidebar-logout" onClick={handleLogout} title="Logout">
            <LogOut size={16} />
          </button>
        </div>
      </aside>

      {/* ── Main Content ────────────────────────────────── */}
      <div className="app-content">
        <header className="app-topbar">
          <div className="topbar-left">
            <GraduationCap size={18} className="topbar-icon" />
            <span>AI Skill Intelligence Platform</span>
          </div>
          <div className="topbar-right">
            <span className="topbar-badge">
              <ShieldCheck size={13} />
              {user?.designation || 'Officer'}
            </span>
            <span className="topbar-dept">{user?.department || 'MoSPI'}</span>
          </div>
        </header>
        <main className="app-main">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
