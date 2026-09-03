/**
 * Store for analytics data (learner and admin).
 */
import { create } from 'zustand';

interface AnalyticsState {
  learnerData: any;
  adminData: any;
  isLoading: boolean;
  fetchLearnerData: () => Promise<void>;
  fetchAdminData: () => Promise<void>;
}

export const useAnalyticsStore = create<AnalyticsState>((set) => ({
  learnerData: null,
  adminData: null,
  isLoading: false,

  fetchLearnerData: async () => {
    set({ isLoading: true });
    try {
      const res = await fetch('/api/analytics/learner', {
        headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` },
      });
      const data = await res.json();
      set({ learnerData: data, isLoading: false });
    } catch (e) {
      set({ isLoading: false });
    }
  },

  fetchAdminData: async () => {
    set({ isLoading: true });
    try {
      const res = await fetch('/api/analytics/admin', {
        headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` },
      });
      const data = await res.json();
      set({ adminData: data, isLoading: false });
    } catch (e) {
      set({ isLoading: false });
    }
  },
}));
