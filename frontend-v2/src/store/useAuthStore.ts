/**
 * Zustand store for authentication state management.
 * Handles login, logout, token persistence, and profile loading.
 */
import { create } from 'zustand';
import type { User } from '../types';
import * as api from '../lib/api';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (username: string, password: string) => Promise<void>;
  register: (data: { username: string; email: string; password: string; designation: string; department: string }) => Promise<void>;
  logout: () => void;
  loadProfile: () => Promise<void>;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  isAuthenticated: !!localStorage.getItem('karmasetu_access_token'),
  isLoading: false,
  error: null,

  login: async (username: string, password: string) => {
    set({ isLoading: true, error: null });
    try {
      const data = await api.login(username, password);
      set({
        user: {
          user_id: data.user_id,
          username,
          email: '',
          designation: '',
          department: '',
          roles: data.roles,
        },
        isAuthenticated: true,
        isLoading: false,
      });
      // Load full profile in background
      get().loadProfile();
    } catch (e: any) {
      set({ isLoading: false, error: e.message || 'Login failed' });
      throw e;
    }
  },

  register: async (data) => {
    set({ isLoading: true, error: null });
    try {
      await api.register({ ...data, role: 'learner' });
      set({ isLoading: false });
    } catch (e: any) {
      set({ isLoading: false, error: e.message || 'Registration failed' });
      throw e;
    }
  },

  logout: () => {
    api.clearTokens();
    set({ user: null, isAuthenticated: false, error: null });
  },

  loadProfile: async () => {
    try {
      const user = await api.getMe();
      set({ user, isAuthenticated: true });
    } catch {
      api.clearTokens();
      set({ user: null, isAuthenticated: false });
    }
  },

  clearError: () => set({ error: null }),
}));
