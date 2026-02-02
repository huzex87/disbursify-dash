// API Types

export interface User {
    id: string;
    email: string;
    phone: string | null;
    first_name: string;
    last_name: string;
    full_name: string;
    avatar_url: string | null;
    timezone: string;
    locale: string;
    email_verified: boolean;
    phone_verified: boolean;
    two_factor_enabled: boolean;
    date_joined: string;
    last_login_at: string | null;
}

export interface Organization {
    id: string;
    name: string;
    slug: string | null;
    logo_url: string | null;
    subscription_tier: 'starter' | 'growth' | 'business' | 'enterprise';
    subscription_status: 'trialing' | 'active' | 'past_due' | 'canceled' | 'unpaid';
    trial_ends_at: string | null;
    subscription_ends_at: string | null;
    max_businesses: number;
    max_team_members: number;
    features_enabled: Record<string, boolean>;
    business_count: number;
    member_count: number;
    tier_limits: {
        businesses: number;
        team_members: number;
        bank_sync: boolean;
    };
    created_at: string;
    updated_at: string;
}

export interface Business {
    id: string;
    name: string;
    short_name: string | null;
    description: string | null;
    industry: string;
    business_type: string | null;
    registration_number: string | null;
    logo_url: string | null;
    color: string;
    icon: string | null;
    primary_currency: string;
    fiscal_year_start: string | null;
    opening_balance: number;
    opening_balance_date: string | null;
    current_balance: number;
    balance_updated_at: string | null;
    is_active: boolean;
    transaction_count: number;
    created_at: string;
    updated_at: string;
}

export interface Transaction {
    id: string;
    business: string;
    business_name: string;
    business_color?: string;
    transaction_date: string;
    transaction_type: 'income' | 'expense' | 'transfer';
    amount: number;
    currency: string;
    exchange_rate: number;
    amount_ngn: number;
    category: string;
    subcategory: string | null;
    description: string;
    notes: string | null;
    reference_number: string | null;
    payment_method: string | null;
    payment_reference: string | null;
    status: 'pending' | 'confirmed' | 'reconciled' | 'voided';
    is_reconciled: boolean;
    tags: string[];
    has_receipt: boolean;
    receipts: Receipt[];
    ai_categorized: boolean;
    ai_confidence: number | null;
    ai_suggested_category: string | null;
    created_by_name: string | null;
    created_at: string;
    updated_at: string;
}

export interface Receipt {
    id: string;
    file_name: string;
    file_url: string;
    file_size: number | null;
    mime_type: string | null;
    thumbnail_url: string | null;
    created_at: string;
}

export interface Category {
    id: string;
    name: string;
    slug: string;
    description: string | null;
    category_type: 'income' | 'expense' | 'transfer';
    icon: string | null;
    color: string | null;
    sort_order: number;
    is_system: boolean;
    is_active: boolean;
    subcategories: Category[];
}

export interface Alert {
    id: string;
    alert_type: string;
    severity: 'low' | 'medium' | 'high' | 'critical';
    title: string;
    message: string;
    status: 'unread' | 'read' | 'actioned' | 'dismissed';
    action_url: string | null;
    created_at: string;
}

export interface TeamMember {
    id: string;
    user: User | null;
    invited_email: string | null;
    role: 'owner' | 'admin' | 'accountant' | 'manager' | 'viewer';
    status: 'pending' | 'active' | 'suspended' | 'removed';
    business_access: string[];
    invited_at: string | null;
    accepted_at: string | null;
    created_at: string;
}

// API Response types
export interface ApiResponse<T> {
    success: boolean;
    data: T;
    error?: {
        code: string;
        message: string;
        details?: { field: string; message: string }[];
    };
}

export interface PaginatedResponse<T> {
    results: T[];
    count: number;
    next: string | null;
    previous: string | null;
}

export interface LoginResponse {
    access_token: string;
    refresh_token: string;
    token_type: string;
    expires_in: number;
    user: User;
    organizations: { id: string; name: string; role: string }[];
    default_organization_id: string | null;
}

export interface TransactionSummary {
    total_income: number;
    total_expense: number;
    net: number;
    count: number;
}

export interface BusinessSummary {
    count: number;
    total_balance: number;
    currency: string;
}
