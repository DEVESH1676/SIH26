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
