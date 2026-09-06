/**
 * Zustand store for analytics data (learner and admin).
 */
import { create } from 'zustand';
import * as api from '../lib/api';

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
      const data = await api.getLearnerAnalytics();
      set({ learnerData: data, isLoading: false });
    } catch {
      set({ isLoading: false });
    }
  },

  fetchAdminData: async () => {
    set({ isLoading: true });
    try {
      const data = await api.getAdminAnalytics();
      set({ adminData: data, isLoading: false });
    } catch {
      set({ isLoading: false });
    }
  },
}));
