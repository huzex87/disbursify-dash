# Disbursify Dash
## Database Schema v1.0

### Multi-Business Financial Management Platform

---

**Document Version:** 1.0  
**Last Updated:** February 2, 2026  
**Database:** PostgreSQL 15+

---

## 1. Schema Overview

### 1.1 Entity Relationship Diagram

```
┌──────────────────┐
│      USERS       │
├──────────────────┤
│ id (PK)          │
│ email            │
│ phone            │
│ password_hash    │
│ ...              │
└────────┬─────────┘
         │
         │ owns
         ▼
┌──────────────────┐       ┌──────────────────┐
│  ORGANIZATIONS   │       │   TEAM_MEMBERS   │
├──────────────────┤       ├──────────────────┤
│ id (PK)          │◄──────│ organization_id  │
│ owner_id (FK)    │       │ user_id (FK)     │
│ name             │       │ role             │
│ subscription_tier│       │ ...              │
│ ...              │       └──────────────────┘
└────────┬─────────┘
         │
         │ contains
         ▼
┌──────────────────┐       ┌──────────────────┐
│    BUSINESSES    │       │  BANK_ACCOUNTS   │
├──────────────────┤       ├──────────────────┤
│ id (PK)          │◄──────│ business_id (FK) │
│ organization_id  │       │ provider         │
│ name             │       │ bank_name        │
│ industry         │       │ account_number   │
│ ...              │       │ ...              │
└────────┬─────────┘       └──────────────────┘
         │
         │ has
         ▼
┌──────────────────┐       ┌──────────────────┐
│   TRANSACTIONS   │       │    CATEGORIES    │
├──────────────────┤       ├──────────────────┤
│ id (PK)          │       │ id (PK)          │
│ business_id (FK) │───────│ organization_id  │
│ category         │       │ name             │
│ amount           │       │ type             │
│ ...              │       │ ...              │
└──────────────────┘       └──────────────────┘
         │
         │ has
         ▼
┌──────────────────┐
│    RECEIPTS      │
├──────────────────┤
│ id (PK)          │
│ transaction_id   │
│ file_url         │
│ ...              │
└──────────────────┘
```

---

## 2. Core Tables

### 2.1 users

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Authentication
    email VARCHAR(255) NOT NULL UNIQUE,
    email_verified BOOLEAN DEFAULT FALSE,
    email_verified_at TIMESTAMP,
    phone VARCHAR(20),
    phone_verified BOOLEAN DEFAULT FALSE,
    phone_verified_at TIMESTAMP,
    password_hash VARCHAR(255) NOT NULL,
    
    -- Profile
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    avatar_url TEXT,
    timezone VARCHAR(50) DEFAULT 'Africa/Lagos',
    locale VARCHAR(10) DEFAULT 'en-NG',
    
    -- Security
    two_factor_enabled BOOLEAN DEFAULT FALSE,
    two_factor_secret VARCHAR(255),
    last_login_at TIMESTAMP,
    last_login_ip INET,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP,
    
    -- Preferences
    preferences JSONB DEFAULT '{}',
    -- {
    --   "notifications": {
    --     "email": true,
    --     "sms": true,
    --     "push": true
    --   },
    --   "dashboard": {
    --     "default_currency": "NGN",
    --     "show_naira_only": false
    --   }
    -- }
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_users_deleted ON users(deleted_at) WHERE deleted_at IS NULL;
```

### 2.2 organizations

```sql
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    
    -- Details
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE,
    logo_url TEXT,
    
    -- Subscription
    subscription_tier VARCHAR(50) DEFAULT 'starter',
    -- 'starter' | 'growth' | 'business' | 'enterprise'
    subscription_status VARCHAR(50) DEFAULT 'active',
    -- 'trialing' | 'active' | 'past_due' | 'canceled' | 'unpaid'
    trial_ends_at TIMESTAMP,
    subscription_ends_at TIMESTAMP,
    
    -- Limits based on tier
    max_businesses INTEGER DEFAULT 5,
    max_team_members INTEGER DEFAULT 1,
    features_enabled JSONB DEFAULT '{}',
    -- {
    --   "bank_sync": false,
    --   "ai_categorization": false,
    --   "forecasting": false,
    --   "api_access": false
    -- }
    
    -- Billing
    billing_email VARCHAR(255),
    billing_address JSONB,
    paystack_customer_id VARCHAR(100),
    
    -- Settings
    settings JSONB DEFAULT '{}',
    -- {
    --   "default_currency": "NGN",
    --   "fiscal_year_start": "01-01",
    --   "date_format": "DD/MM/YYYY"
    -- }
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP
);

-- Indexes
CREATE INDEX idx_org_owner ON organizations(owner_id);
CREATE INDEX idx_org_slug ON organizations(slug);
CREATE INDEX idx_org_subscription ON organizations(subscription_status);
```

### 2.3 team_members

```sql
CREATE TABLE team_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    
    -- Invitation (before user accepts)
    invited_email VARCHAR(255),
    invited_by UUID REFERENCES users(id),
    invited_at TIMESTAMP,
    invitation_token VARCHAR(255) UNIQUE,
    invitation_expires_at TIMESTAMP,
    
    -- Role & Permissions
    role VARCHAR(50) NOT NULL DEFAULT 'viewer',
    -- 'owner' | 'admin' | 'accountant' | 'manager' | 'viewer'
    
    -- Business-level access (for 'manager' role)
    business_access UUID[] DEFAULT '{}',
    -- If empty and role is manager, no access
    -- If contains business IDs, access to those only
    
    -- Permissions override (optional granular control)
    permissions_override JSONB,
    -- {
    --   "can_add_transactions": true,
    --   "can_edit_transactions": false,
    --   "can_delete_transactions": false,
    --   "can_view_reports": true,
    --   "can_export": false,
    --   "can_manage_team": false,
    --   "can_manage_billing": false
    -- }
    
    -- Status
    status VARCHAR(50) DEFAULT 'pending',
    -- 'pending' | 'active' | 'suspended' | 'removed'
    accepted_at TIMESTAMP,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_team_org ON team_members(organization_id);
CREATE INDEX idx_team_user ON team_members(user_id);
CREATE INDEX idx_team_status ON team_members(status);
CREATE UNIQUE INDEX idx_team_unique ON team_members(organization_id, user_id) 
    WHERE user_id IS NOT NULL;
```

### 2.4 businesses

```sql
CREATE TABLE businesses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    
    -- Basic Info
    name VARCHAR(255) NOT NULL,
    short_name VARCHAR(50), -- For compact display
    description TEXT,
    
    -- Classification
    industry VARCHAR(100),
    -- 'restaurant' | 'retail' | 'transport' | 'real_estate' | 'consulting' 
    -- 'agriculture' | 'manufacturing' | 'technology' | 'healthcare' | 'other'
    business_type VARCHAR(50),
    -- 'sole_proprietorship' | 'partnership' | 'limited_liability' | 'plc'
    registration_number VARCHAR(100),
    
    -- Branding
    logo_url TEXT,
    color VARCHAR(7) DEFAULT '#6B21A8', -- Hex color for dashboard cards
    icon VARCHAR(50), -- Icon identifier
    
    -- Financial Settings
    primary_currency CHAR(3) DEFAULT 'NGN',
    fiscal_year_start DATE, -- NULL = follow org setting
    
    -- Opening Balances (for when business was added)
    opening_balance DECIMAL(15, 2) DEFAULT 0,
    opening_balance_date DATE,
    
    -- Calculated Fields (cached, updated by triggers/jobs)
    current_balance DECIMAL(15, 2) DEFAULT 0,
    balance_updated_at TIMESTAMP,
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    archived_at TIMESTAMP,
    archived_by UUID REFERENCES users(id),
    
    -- Metadata
    metadata JSONB DEFAULT '{}',
    -- {
    --   "address": {},
    --   "contact_person": "",
    --   "tax_id": ""
    -- }
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    created_by UUID REFERENCES users(id)
);

-- Indexes
CREATE INDEX idx_business_org ON businesses(organization_id);
CREATE INDEX idx_business_active ON businesses(organization_id, is_active);
CREATE INDEX idx_business_industry ON businesses(industry);
```

### 2.5 bank_accounts

```sql
CREATE TABLE bank_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    
    -- Bank Info
    bank_name VARCHAR(100) NOT NULL,
    bank_code VARCHAR(20),
    account_name VARCHAR(255),
    account_number VARCHAR(20) NOT NULL,
    account_type VARCHAR(50), -- 'current' | 'savings' | 'domiciliary'
    currency CHAR(3) DEFAULT 'NGN',
    
    -- Provider Integration
    provider VARCHAR(50), -- 'mono' | 'okra' | 'manual'
    provider_account_id VARCHAR(255), -- ID from Mono/Okra
    provider_institution_id VARCHAR(255),
    provider_access_token TEXT, -- Encrypted
    provider_refresh_token TEXT, -- Encrypted
    
    -- Sync Status
    sync_status VARCHAR(50) DEFAULT 'active',
    -- 'active' | 'paused' | 'failed' | 'disconnected'
    last_synced_at TIMESTAMP,
    last_sync_error TEXT,
    next_sync_at TIMESTAMP,
    
    -- Balance (from provider)
    current_balance DECIMAL(15, 2),
    available_balance DECIMAL(15, 2),
    balance_updated_at TIMESTAMP,
    
    -- Settings
    is_primary BOOLEAN DEFAULT FALSE, -- Primary account for this business
    auto_sync_enabled BOOLEAN DEFAULT TRUE,
    sync_frequency_minutes INTEGER DEFAULT 60,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    connected_by UUID REFERENCES users(id),
    disconnected_at TIMESTAMP,
    disconnected_by UUID REFERENCES users(id)
);

-- Indexes
CREATE INDEX idx_bank_business ON bank_accounts(business_id);
CREATE INDEX idx_bank_org ON bank_accounts(organization_id);
CREATE INDEX idx_bank_sync ON bank_accounts(sync_status, next_sync_at);
CREATE UNIQUE INDEX idx_bank_provider ON bank_accounts(provider, provider_account_id) 
    WHERE provider IS NOT NULL;
```

### 2.6 categories

```sql
CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    -- NULL organization_id = system default category
    
    -- Category Info
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Classification
    type VARCHAR(20) NOT NULL, -- 'income' | 'expense' | 'transfer'
    parent_id UUID REFERENCES categories(id), -- For subcategories
    
    -- Display
    icon VARCHAR(50),
    color VARCHAR(7),
    sort_order INTEGER DEFAULT 0,
    
    -- Flags
    is_system BOOLEAN DEFAULT FALSE, -- System categories can't be deleted
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_category_org ON categories(organization_id);
CREATE INDEX idx_category_type ON categories(type);
CREATE INDEX idx_category_parent ON categories(parent_id);
CREATE UNIQUE INDEX idx_category_slug ON categories(organization_id, slug);

-- Default Categories (inserted via migration)
-- Income: sales, services, investments, refunds, other_income
-- Expense: rent, utilities, salaries, inventory, marketing, transport, 
--          bank_charges, taxes, supplies, repairs, professional_fees, other_expense
```

### 2.7 transactions

```sql
CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE RESTRICT,
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE RESTRICT,
    
    -- Transaction Core
    transaction_date DATE NOT NULL,
    transaction_type VARCHAR(20) NOT NULL, -- 'income' | 'expense' | 'transfer'
    
    -- Amount
    amount DECIMAL(15, 2) NOT NULL CHECK (amount > 0),
    currency CHAR(3) DEFAULT 'NGN',
    exchange_rate DECIMAL(10, 6) DEFAULT 1.0, -- For foreign currency
    amount_ngn DECIMAL(15, 2), -- Converted to NGN for reporting
    
    -- Classification
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100),
    
    -- Details
    description TEXT NOT NULL,
    notes TEXT,
    reference_number VARCHAR(100),
    
    -- Payment
    payment_method VARCHAR(50), 
    -- 'cash' | 'bank_transfer' | 'pos' | 'cheque' | 'mobile_money' | 'online'
    payment_reference VARCHAR(255), -- Bank reference, cheque number, etc.
    
    -- For Transfers
    transfer_to_business_id UUID REFERENCES businesses(id),
    transfer_pair_id UUID REFERENCES transactions(id),
    -- When a transfer is created, two transactions are made (debit + credit)
    -- This links them together
    
    -- Bank Sync
    bank_account_id UUID REFERENCES bank_accounts(id),
    bank_transaction_id VARCHAR(255), -- ID from bank provider
    bank_narration TEXT, -- Original narration from bank
    
    -- Status
    status VARCHAR(50) DEFAULT 'confirmed',
    -- 'pending' | 'confirmed' | 'reconciled' | 'voided'
    is_reconciled BOOLEAN DEFAULT FALSE,
    reconciled_at TIMESTAMP,
    reconciled_by UUID REFERENCES users(id),
    
    -- AI Categorization
    ai_categorized BOOLEAN DEFAULT FALSE,
    ai_confidence DECIMAL(5, 2), -- 0.00 to 1.00
    ai_suggested_category VARCHAR(100),
    user_corrected BOOLEAN DEFAULT FALSE,
    
    -- Attachments (receipt URLs stored in separate table)
    has_receipt BOOLEAN DEFAULT FALSE,
    
    -- Audit
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    voided_at TIMESTAMP,
    voided_by UUID REFERENCES users(id),
    void_reason TEXT
);

-- Indexes (crucial for performance)
CREATE INDEX idx_txn_org_date ON transactions(organization_id, transaction_date DESC);
CREATE INDEX idx_txn_business_date ON transactions(business_id, transaction_date DESC);
CREATE INDEX idx_txn_category ON transactions(organization_id, category);
CREATE INDEX idx_txn_type_date ON transactions(organization_id, transaction_type, transaction_date);
CREATE INDEX idx_txn_status ON transactions(status);
CREATE INDEX idx_txn_bank_id ON transactions(bank_transaction_id) WHERE bank_transaction_id IS NOT NULL;
CREATE INDEX idx_txn_search ON transactions USING gin(to_tsvector('english', description || ' ' || COALESCE(notes, '')));

-- Partition by date (for large scale)
-- Consider partitioning by month or year if transactions exceed millions
```

### 2.8 receipts

```sql
CREATE TABLE receipts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id UUID NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    
    -- File Info
    file_name VARCHAR(255) NOT NULL,
    file_url TEXT NOT NULL, -- S3 URL
    file_size INTEGER, -- Bytes
    mime_type VARCHAR(100),
    
    -- Image Processing
    thumbnail_url TEXT,
    ocr_text TEXT, -- Extracted text from receipt
    ocr_processed_at TIMESTAMP,
    
    -- Metadata
    uploaded_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_receipt_txn ON receipts(transaction_id);
CREATE INDEX idx_receipt_org ON receipts(organization_id);
```

---

## 3. Alert & Notification Tables

### 3.1 alert_rules

```sql
CREATE TABLE alert_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    business_id UUID REFERENCES businesses(id) ON DELETE CASCADE,
    -- NULL business_id = applies to all businesses
    
    -- Rule Definition
    alert_type VARCHAR(50) NOT NULL,
    -- 'low_cash' | 'unusual_expense' | 'large_transaction' | 
    -- 'sync_failed' | 'daily_summary' | 'goal_achieved'
    
    name VARCHAR(255),
    description TEXT,
    
    -- Conditions (JSON format)
    conditions JSONB NOT NULL,
    -- Examples:
    -- { "threshold": 500000, "operator": "<" }                    -- low_cash
    -- { "multiplier": 2.0, "period": "day" }                      -- unusual_expense
    -- { "amount": 1000000, "direction": "out" }                   -- large_transaction
    -- { "target": 5000000, "period": "month", "type": "income" }  -- goal_achieved
    
    -- Notification Channels
    notify_email BOOLEAN DEFAULT TRUE,
    notify_sms BOOLEAN DEFAULT FALSE,
    notify_push BOOLEAN DEFAULT TRUE,
    notify_whatsapp BOOLEAN DEFAULT FALSE,
    
    -- Recipients (defaults to org owner + admins)
    recipients UUID[], -- Specific user IDs to notify
    
    -- Schedule (for recurring alerts like daily_summary)
    schedule JSONB,
    -- { "time": "18:00", "timezone": "Africa/Lagos", "days": [1,2,3,4,5] }
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    last_triggered_at TIMESTAMP,
    trigger_count INTEGER DEFAULT 0,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    created_by UUID REFERENCES users(id)
);

CREATE INDEX idx_alert_rule_org ON alert_rules(organization_id);
CREATE INDEX idx_alert_rule_type ON alert_rules(alert_type, is_active);
```

### 3.2 alerts

```sql
CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    alert_rule_id UUID REFERENCES alert_rules(id) ON DELETE SET NULL,
    business_id UUID REFERENCES businesses(id) ON DELETE CASCADE,
    
    -- Alert Details
    alert_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) DEFAULT 'medium', -- 'low' | 'medium' | 'high' | 'critical'
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    
    -- Context
    context_data JSONB,
    -- {
    --   "current_balance": 450000,
    --   "threshold": 500000,
    --   "transaction_id": "uuid",
    --   "amount": 150000
    -- }
    
    -- Links
    action_url TEXT, -- Deep link to relevant screen
    
    -- Status
    status VARCHAR(20) DEFAULT 'unread', -- 'unread' | 'read' | 'actioned' | 'dismissed'
    read_at TIMESTAMP,
    read_by UUID REFERENCES users(id),
    actioned_at TIMESTAMP,
    dismissed_at TIMESTAMP,
    dismissed_by UUID REFERENCES users(id),
    
    -- Notifications sent
    email_sent BOOLEAN DEFAULT FALSE,
    email_sent_at TIMESTAMP,
    sms_sent BOOLEAN DEFAULT FALSE,
    sms_sent_at TIMESTAMP,
    push_sent BOOLEAN DEFAULT FALSE,
    push_sent_at TIMESTAMP,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP -- Auto-cleanup old alerts
);

CREATE INDEX idx_alert_org_status ON alerts(organization_id, status, created_at DESC);
CREATE INDEX idx_alert_business ON alerts(business_id);
CREATE INDEX idx_alert_expires ON alerts(expires_at) WHERE expires_at IS NOT NULL;
```

---

## 4. Audit & Logging Tables

### 4.1 audit_logs

```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL,
    user_id UUID,
    
    -- Action
    action VARCHAR(50) NOT NULL,
    -- 'create' | 'update' | 'delete' | 'login' | 'logout' | 
    -- 'export' | 'connect' | 'disconnect' | 'invite' | 'permission_change'
    
    resource_type VARCHAR(50) NOT NULL,
    -- 'user' | 'organization' | 'business' | 'transaction' | 
    -- 'bank_account' | 'team_member' | 'report'
    resource_id UUID,
    
    -- Changes
    old_values JSONB,
    new_values JSONB,
    
    -- Context
    ip_address INET,
    user_agent TEXT,
    request_id VARCHAR(100),
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for audit queries
CREATE INDEX idx_audit_org ON audit_logs(organization_id, created_at DESC);
CREATE INDEX idx_audit_user ON audit_logs(user_id, created_at DESC);
CREATE INDEX idx_audit_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX idx_audit_action ON audit_logs(action, created_at DESC);

-- Retention: Keep for 2 years, then archive to cold storage
```

---

## 5. Integration Tables

### 5.1 sync_jobs

```sql
CREATE TABLE sync_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    bank_account_id UUID NOT NULL REFERENCES bank_accounts(id),
    
    -- Job Details
    job_type VARCHAR(50) NOT NULL, -- 'scheduled' | 'manual' | 'webhook'
    status VARCHAR(50) DEFAULT 'pending',
    -- 'pending' | 'running' | 'completed' | 'failed' | 'cancelled'
    
    -- Progress
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    
    -- Results
    transactions_fetched INTEGER DEFAULT 0,
    transactions_created INTEGER DEFAULT 0,
    transactions_updated INTEGER DEFAULT 0,
    transactions_skipped INTEGER DEFAULT 0,
    
    error_message TEXT,
    error_details JSONB,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    triggered_by UUID REFERENCES users(id)
);

CREATE INDEX idx_sync_job_bank ON sync_jobs(bank_account_id, created_at DESC);
CREATE INDEX idx_sync_job_status ON sync_jobs(status, created_at);
```

---

## 6. Row-Level Security (RLS)

```sql
-- Enable RLS on all tables
ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE businesses ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE bank_accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;

-- Create policies
-- Transactions: Users can only see transactions from their org
CREATE POLICY transactions_org_isolation ON transactions
    USING (organization_id = current_setting('app.current_org_id')::UUID);

-- Businesses: Users can only see businesses from their org
CREATE POLICY businesses_org_isolation ON businesses
    USING (organization_id = current_setting('app.current_org_id')::UUID);

-- Function to set current org context
CREATE OR REPLACE FUNCTION set_tenant_context(org_id UUID)
RETURNS VOID AS $$
BEGIN
    PERFORM set_config('app.current_org_id', org_id::TEXT, FALSE);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

---

## 7. Triggers & Functions

### 7.1 Update Business Balance

```sql
CREATE OR REPLACE FUNCTION update_business_balance()
RETURNS TRIGGER AS $$
BEGIN
    -- Recalculate business balance
    UPDATE businesses 
    SET 
        current_balance = (
            SELECT COALESCE(SUM(
                CASE 
                    WHEN transaction_type = 'income' THEN amount_ngn
                    WHEN transaction_type = 'expense' THEN -amount_ngn
                    ELSE 0
                END
            ), 0) + opening_balance
            FROM transactions 
            WHERE business_id = NEW.business_id 
            AND status = 'confirmed'
        ),
        balance_updated_at = NOW()
    WHERE id = NEW.business_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_balance
AFTER INSERT OR UPDATE OR DELETE ON transactions
FOR EACH ROW
EXECUTE FUNCTION update_business_balance();
```

### 7.2 Updated At Trigger

```sql
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to all tables with updated_at
CREATE TRIGGER set_updated_at
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER set_updated_at
BEFORE UPDATE ON organizations
FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ... repeat for other tables
```

---

## 8. Migrations Strategy

### 8.1 Migration Files

```
migrations/
├── 0001_create_extensions.sql
├── 0002_create_users.sql
├── 0003_create_organizations.sql
├── 0004_create_team_members.sql
├── 0005_create_businesses.sql
├── 0006_create_categories.sql
├── 0007_create_transactions.sql
├── 0008_create_bank_accounts.sql
├── 0009_create_receipts.sql
├── 0010_create_alerts.sql
├── 0011_create_audit_logs.sql
├── 0012_create_sync_jobs.sql
├── 0013_create_rls_policies.sql
├── 0014_create_triggers.sql
├── 0015_seed_categories.sql
└── 0016_create_indexes.sql
```

### 8.2 Required Extensions

```sql
-- 0001_create_extensions.sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- For fuzzy search
```

---

## Document Control

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Feb 2, 2026 | Initial database schema |

---

© 2026 Disbursify. All Rights Reserved.
