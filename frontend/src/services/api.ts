import axios, { type AxiosError, type AxiosInstance, type InternalAxiosRequestConfig } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance
const api: AxiosInstance = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor - add auth token
api.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
        const token = localStorage.getItem('access_token');
        if (token && config.headers) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        // Add organization context if selected
        const orgId = localStorage.getItem('current_organization_id');
        if (orgId && config.params) {
            config.params.organization_id = orgId;
        }

        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor - handle token refresh
api.interceptors.response.use(
    (response) => response,
    async (error: AxiosError) => {
        const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

        // If 401 and not already retrying
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const refreshToken = localStorage.getItem('refresh_token');
                if (!refreshToken) {
                    throw new Error('No refresh token');
                }

                const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
                    refresh: refreshToken,
                });

                const { access } = response.data;
                localStorage.setItem('access_token', access);

                if (originalRequest.headers) {
                    originalRequest.headers.Authorization = `Bearer ${access}`;
                }

                return api(originalRequest);
            } catch (refreshError) {
                // Refresh failed - clear tokens and redirect to login
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('current_organization_id');
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

export default api;

// Auth API
export const authApi = {
    register: (data: { email: string; password: string; password_confirm: string; first_name?: string; last_name?: string; phone?: string }) =>
        api.post('/auth/register', data),

    login: (data: { email: string; password: string; remember_me?: boolean }) =>
        api.post('/auth/login', data),

    logout: () => {
        const refreshToken = localStorage.getItem('refresh_token');
        return api.post('/auth/logout', { refresh_token: refreshToken });
    },

    refresh: (refreshToken: string) =>
        api.post('/auth/refresh', { refresh: refreshToken }),

    me: () => api.get('/auth/me'),

    updateProfile: (data: Partial<{ first_name: string; last_name: string; phone: string; avatar_url: string }>) =>
        api.patch('/auth/me', data),

    changePassword: (data: { old_password: string; new_password: string }) =>
        api.post('/auth/password/change', data),

    sendOtp: (data: { phone?: string; email?: string; otp_type: string }) =>
        api.post('/auth/otp/send', data),

    verifyOtp: (data: { phone?: string; email?: string; code: string }) =>
        api.post('/auth/otp/verify', data),
};

// Organizations API
export const organizationsApi = {
    list: () => api.get('/organizations/'),

    get: (id: string) => api.get(`/organizations/${id}/`),

    create: (data: { name: string; logo_url?: string }) =>
        api.post('/organizations/', data),

    update: (id: string, data: Partial<{ name: string; logo_url: string }>) =>
        api.patch(`/organizations/${id}/`, data),

    getTeam: (orgId: string) => api.get(`/organizations/${orgId}/team/`),

    inviteTeamMember: (orgId: string, data: { email: string; role: string; business_access?: string[] }) =>
        api.post(`/organizations/${orgId}/team/`, data),

    removeTeamMember: (orgId: string, memberId: string) =>
        api.delete(`/organizations/${orgId}/team/${memberId}/`),
};

// Businesses API
export const businessesApi = {
    list: (organizationId?: string) =>
        api.get('/businesses/', { params: { organization_id: organizationId } }),

    get: (id: string) => api.get(`/businesses/${id}/`),

    create: (data: {
        organization_id: string;
        name: string;
        short_name?: string;
        description?: string;
        industry?: string;
        color?: string;
        opening_balance?: number;
    }) => api.post('/businesses/', data),

    update: (id: string, data: Partial<{
        name: string;
        short_name: string;
        description: string;
        industry: string;
        color: string;
    }>) => api.patch(`/businesses/${id}/`, data),

    archive: (id: string) => api.post(`/businesses/${id}/archive/`),

    getBankAccounts: (businessId: string) =>
        api.get(`/businesses/${businessId}/bank_accounts/`),

    connectBankAccount: (businessId: string, data: {
        provider: string;
        access_code?: string;
        bank_name?: string;
        account_number?: string;
        account_name?: string;
    }) => api.post(`/businesses/${businessId}/bank_accounts/`, data),

    recalculateBalance: (id: string) =>
        api.post(`/businesses/${id}/recalculate_balance/`),
};

// Transactions API
export const transactionsApi = {
    list: (params?: {
        organization_id?: string;
        business?: string;
        transaction_type?: string;
        category?: string;
        status?: string;
        date_from?: string;
        date_to?: string;
        min_amount?: number;
        max_amount?: number;
        search?: string;
        page?: number;
    }) => api.get('/transactions/', { params }),

    get: (id: string) => api.get(`/transactions/${id}/`),

    create: (data: {
        business: string;
        transaction_date: string;
        transaction_type: 'income' | 'expense';
        amount: number;
        currency?: string;
        category: string;
        description: string;
        notes?: string;
        payment_method?: string;
        reference_number?: string;
        tags?: string[];
    }) => api.post('/transactions/', data),

    update: (id: string, data: Partial<{
        transaction_date: string;
        transaction_type: string;
        amount: number;
        category: string;
        description: string;
        notes: string;
        payment_method: string;
        tags: string[];
    }>) => api.patch(`/transactions/${id}/`, data),

    void: (id: string, reason?: string) =>
        api.post(`/transactions/${id}/void/`, { reason }),
};

// Categories API
export const categoriesApi = {
    list: (organizationId?: string) =>
        api.get('/categories/', { params: { organization_id: organizationId } }),
};
