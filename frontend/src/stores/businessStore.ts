import { create } from 'zustand';
import type { Business, BusinessSummary } from '../types';
import { businessesApi } from '../services/api';

interface BusinessState {
    businesses: Business[];
    currentBusiness: Business | null;
    summary: BusinessSummary | null;
    isLoading: boolean;
    error: string | null;

    // Actions
    fetchBusinesses: (organizationId?: string) => Promise<void>;
    fetchBusiness: (id: string) => Promise<void>;
    createBusiness: (data: {
        organization_id: string;
        name: string;
        industry?: string;
        color?: string;
        opening_balance?: number;
    }) => Promise<Business>;
    updateBusiness: (id: string, data: Partial<Business>) => Promise<void>;
    archiveBusiness: (id: string) => Promise<void>;
    setCurrentBusiness: (business: Business | null) => void;
}

export const useBusinessStore = create<BusinessState>((set) => ({
    businesses: [],
    currentBusiness: null,
    summary: null,
    isLoading: false,
    error: null,

    fetchBusinesses: async (organizationId) => {
        set({ isLoading: true, error: null });
        try {
            const response = await businessesApi.list(organizationId);
            const { businesses, summary } = response.data.data;
            set({ businesses, summary, isLoading: false });
        } catch (error: any) {
            set({
                error: error.response?.data?.error?.message || 'Failed to fetch businesses',
                isLoading: false
            });
        }
    },

    fetchBusiness: async (id) => {
        set({ isLoading: true, error: null });
        try {
            const response = await businessesApi.get(id);
            set({ currentBusiness: response.data.data, isLoading: false });
        } catch (error: any) {
            set({
                error: error.response?.data?.error?.message || 'Failed to fetch business',
                isLoading: false
            });
        }
    },

    createBusiness: async (data) => {
        set({ isLoading: true, error: null });
        try {
            const response = await businessesApi.create(data);
            const business = response.data.data;
            set(state => ({
                businesses: [...state.businesses, business],
                isLoading: false,
            }));
            return business;
        } catch (error: any) {
            set({
                error: error.response?.data?.error?.message || 'Failed to create business',
                isLoading: false
            });
            throw error;
        }
    },

    updateBusiness: async (id, data) => {
        set({ isLoading: true, error: null });
        try {
            const response = await businessesApi.update(id, data as any);
            const updated = response.data.data;
            set(state => ({
                businesses: state.businesses.map(b => b.id === id ? updated : b),
                currentBusiness: state.currentBusiness?.id === id ? updated : state.currentBusiness,
                isLoading: false,
            }));
        } catch (error: any) {
            set({
                error: error.response?.data?.error?.message || 'Failed to update business',
                isLoading: false
            });
            throw error;
        }
    },

    archiveBusiness: async (id) => {
        try {
            await businessesApi.archive(id);
            set(state => ({
                businesses: state.businesses.filter(b => b.id !== id),
                currentBusiness: state.currentBusiness?.id === id ? null : state.currentBusiness,
            }));
        } catch (error: any) {
            set({ error: error.response?.data?.error?.message || 'Failed to archive business' });
            throw error;
        }
    },

    setCurrentBusiness: (business) => {
        set({ currentBusiness: business });
    },
}));
