import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User, Organization } from '../types';
import { authApi, organizationsApi } from '../services/api';

interface AuthState {
    user: User | null;
    organizations: { id: string; name: string; role: string }[];
    currentOrganizationId: string | null;
    isAuthenticated: boolean;
    isLoading: boolean;

    // Actions
    login: (email: string, password: string, rememberMe?: boolean) => Promise<void>;
    logout: () => Promise<void>;
    register: (data: { email: string; password: string; password_confirm: string; first_name?: string; last_name?: string }) => Promise<void>;
    setCurrentOrganization: (orgId: string) => void;
    fetchMe: () => Promise<void>;
    updateProfile: (data: Partial<User>) => Promise<void>;
}

export const useAuthStore = create<AuthState>()(
    persist(
        (set) => ({
            user: null,
            organizations: [],
            currentOrganizationId: null,
            isAuthenticated: false,
            isLoading: false,

            login: async (email, password, rememberMe = false) => {
                set({ isLoading: true });
                try {
                    const response = await authApi.login({ email, password, remember_me: rememberMe });
                    const { access_token, refresh_token, user, organizations, default_organization_id } = response.data.data;

                    localStorage.setItem('access_token', access_token);
                    localStorage.setItem('refresh_token', refresh_token);

                    const orgId = default_organization_id || organizations[0]?.id || null;
                    if (orgId) {
                        localStorage.setItem('current_organization_id', orgId);
                    }

                    set({
                        user,
                        organizations,
                        currentOrganizationId: orgId,
                        isAuthenticated: true,
                        isLoading: false,
                    });
                } catch (error) {
                    set({ isLoading: false });
                    throw error;
                }
            },

            logout: async () => {
                try {
                    await authApi.logout();
                } catch (error) {
                    // Ignore errors on logout
                } finally {
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('refresh_token');
                    localStorage.removeItem('current_organization_id');
                    set({
                        user: null,
                        organizations: [],
                        currentOrganizationId: null,
                        isAuthenticated: false,
                    });
                }
            },

            register: async (data) => {
                set({ isLoading: true });
                try {
                    await authApi.register(data);
                    set({ isLoading: false });
                } catch (error) {
                    set({ isLoading: false });
                    throw error;
                }
            },

            setCurrentOrganization: (orgId) => {
                localStorage.setItem('current_organization_id', orgId);
                set({ currentOrganizationId: orgId });
            },

            fetchMe: async () => {
                try {
                    const response = await authApi.me();
                    set({ user: response.data.data, isAuthenticated: true });

                    // Also fetch organizations
                    const orgsResponse = await organizationsApi.list();
                    const orgs = orgsResponse.data.data.map((org: Organization) => ({
                        id: org.id,
                        name: org.name,
                        role: 'owner', // Would come from API
                    }));
                    set({ organizations: orgs });
                } catch (error) {
                    set({ isAuthenticated: false, user: null });
                    throw error;
                }
            },

            updateProfile: async (data) => {
                const response = await authApi.updateProfile(data as any);
                set({ user: response.data.data });
            },
        }),
        {
            name: 'auth-storage',
            partialize: (state) => ({
                currentOrganizationId: state.currentOrganizationId,
            }),
        }
    )
);
