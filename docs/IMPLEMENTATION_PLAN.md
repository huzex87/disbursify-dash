# Disbursify Flow
## Implementation Plan v1.0

### Multi-Business Financial Management Platform
**Development Roadmap & Technical Implementation Guide**

---

**Document Version:** 1.0  
**Last Updated:** February 2, 2026  
**Prepared By:** Disbursify Engineering Team

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Development Phases](#2-development-phases)
3. [Phase 1: MVP Foundation](#3-phase-1-mvp-foundation)
4. [Phase 2: Bank Integration](#4-phase-2-bank-integration)
5. [Phase 3: Intelligence Layer](#5-phase-3-intelligence-layer)
6. [Phase 4: Mobile & Expansion](#6-phase-4-mobile--expansion)
7. [Technical Architecture](#7-technical-architecture)
8. [Database Design](#8-database-design)
9. [API Specification](#9-api-specification)
10. [Security Implementation](#10-security-implementation)
11. [DevOps & Infrastructure](#11-devops--infrastructure)
12. [Testing Strategy](#12-testing-strategy)
13. [Team & Resources](#13-team--resources)

---

## 1. Project Overview

### 1.1 Product Summary

**Disbursify Flow** is a multi-business financial management SaaS platform enabling Nigerian entrepreneurs to manage finances across multiple business entities from a single, intelligent dashboard.

### 1.2 Core Objectives

| Objective | Success Metric |
|-----------|----------------|
| Unified visibility | See all business finances in <30 seconds |
| Multi-entity support | Manage 2-20+ businesses per account |
| Real-time insights | Dashboard updates within 15 minutes of transactions |
| Mobile-first | 80% of features accessible on mobile |
| Offline capable | Core features work without internet |
| Nigerian localization | Naira + local bank integrations |

### 1.3 Technology Stack Summary

```
┌───────────────────────────────────────────────────────────────┐
│                    TECHNOLOGY STACK                            │
├───────────────────────────────────────────────────────────────┤
│                                                                │
│  FRONTEND                    BACKEND                           │
│  ────────                    ───────                           │
│  • React 18 + TypeScript     • Python 3.11+                   │
│  • Tailwind CSS              • Django 4.2 + DRF               │
│  • Zustand (state)           • Celery (async tasks)           │
│  • Workbox (PWA)             • Redis (cache/queue)            │
│  • React Native (mobile)     • PostgreSQL 15                  │
│                                                                │
│  INFRASTRUCTURE              INTEGRATIONS                      │
│  ──────────────              ────────────                      │
│  • AWS (Lagos region)        • Mono/Okra (banking)            │
│  • Docker + ECS              • Paystack (payments)            │
│  • CloudFlare (CDN)          • Twilio/Africa's Talking        │
│  • GitHub Actions (CI/CD)    • SendGrid (email)               │
│  • Sentry (monitoring)       • OpenAI API (AI features)       │
│                                                                │
└───────────────────────────────────────────────────────────────┘
```

---

## 2. Development Phases

### 2.1 Phase Timeline Overview

```
2026
├── Q1 (Months 1-3): PHASE 1 - MVP FOUNDATION
│   ├── Month 1: Core backend + authentication
│   ├── Month 2: Dashboard + transaction management
│   └── Month 3: Reports + PWA + beta launch
│
├── Q2 (Months 4-6): PHASE 2 - BANK INTEGRATION
│   ├── Month 4: Mono/Okra integration
│   ├── Month 5: Auto-sync + categorization
│   └── Month 6: Alerts + team features
│
├── Q3 (Months 7-9): PHASE 3 - INTELLIGENCE
│   ├── Month 7: AI categorization
│   ├── Month 8: Cash flow forecasting
│   └── Month 9: Anomaly detection + insights
│
└── Q4 (Months 10-12): PHASE 4 - MOBILE & SCALE
    ├── Month 10: React Native apps
    ├── Month 11: WhatsApp integration
    └── Month 12: Ghana expansion prep
```

### 2.2 Resource Allocation by Phase

| Phase | Duration | Team Size | Key Deliverables |
|-------|----------|-----------|------------------|
| Phase 1 | 12 weeks | 2-3 | MVP, 50 beta users |
| Phase 2 | 12 weeks | 3-4 | Bank sync, 200 users |
| Phase 3 | 12 weeks | 4-5 | AI features, 500 users |
| Phase 4 | 12 weeks | 5-6 | Mobile apps, 800 users |

---

## 3. Phase 1: MVP Foundation

**Timeline:** Weeks 1-12  
**Goal:** Launch functional MVP with core features to 50 beta users

### 3.1 Month 1: Core Backend & Authentication (Weeks 1-4)

#### Week 1: Project Setup

| Task | Hours | Owner |
|------|-------|-------|
| Initialize Django project with DRF | 8 | Backend |
| PostgreSQL database setup (AWS RDS) | 4 | DevOps |
| Configure environment management (.env) | 2 | Backend |
| Set up Git repository + branching strategy | 2 | Backend |
| Configure CI/CD pipeline (GitHub Actions) | 8 | DevOps |
| Set up development, staging, production environments | 8 | DevOps |
| Initialize React project with TypeScript | 8 | Frontend |
| Configure Tailwind CSS + design system | 8 | Frontend |

**Deliverables:**
- [ ] Django project skeleton deployed to staging
- [ ] React project with base routing
- [ ] CI/CD pipeline running tests on PR

#### Week 2: User Authentication

| Task | Hours | Owner |
|------|-------|-------|
| User model with custom fields | 6 | Backend |
| Registration endpoint + email verification | 8 | Backend |
| Login/logout with JWT (access + refresh tokens) | 8 | Backend |
| Password reset flow | 6 | Backend |
| Phone verification (OTP via Twilio) | 8 | Backend |
| Auth middleware + permission classes | 8 | Backend |
| Login/Register UI components | 16 | Frontend |
| Auth state management (Zustand) | 8 | Frontend |

**Deliverables:**
- [ ] Users can register with email
- [ ] Users can log in and receive JWT tokens
- [ ] Password reset via email works
- [ ] Frontend auth flow complete

#### Week 3: Organization & Business Core

| Task | Hours | Owner |
|------|-------|-------|
| Organization model (multi-tenant) | 8 | Backend |
| Business model with industry types | 8 | Backend |
| Multi-tenancy middleware (org isolation) | 12 | Backend |
| Business CRUD API endpoints | 8 | Backend |
| Row-level security implementation | 8 | Backend |
| Team member invitation system | 10 | Backend |
| Business setup wizard UI | 16 | Frontend |
| Business listing + cards | 12 | Frontend |

**Deliverables:**
- [ ] Users can create organization
- [ ] Users can add multiple businesses
- [ ] Data isolation verified between orgs

#### Week 4: Account Structure

| Task | Hours | Owner |
|------|-------|-------|
| Chart of Accounts model | 8 | Backend |
| Default account templates per industry | 6 | Backend |
| Bank account model (manual tracking) | 8 | Backend |
| Account API endpoints | 8 | Backend |
| Account management UI | 12 | Frontend |
| Settings pages | 10 | Frontend |
| Testing + bug fixes | 16 | All |

**Deliverables:**
- [ ] Chart of accounts per business
- [ ] Bank accounts can be added manually
- [ ] Full authentication + business setup flow

### 3.2 Month 2: Dashboard & Transactions (Weeks 5-8)

#### Week 5: Transaction System

| Task | Hours | Owner |
|------|-------|-------|
| Transaction model (comprehensive) | 10 | Backend |
| Transaction CRUD endpoints | 12 | Backend |
| Transaction filtering (date, type, category) | 8 | Backend |
| Pagination + sorting | 6 | Backend |
| Transaction entry form UI | 16 | Frontend |
| Transaction list with filters | 14 | Frontend |
| Mobile-responsive tables | 6 | Frontend |

**Transaction Model Structure:**
```python
class Transaction(models.Model):
    id = models.UUIDField(primary_key=True)
    organization = models.ForeignKey(Organization)
    business = models.ForeignKey(Business)
    transaction_date = models.DateField()
    transaction_type = models.CharField()  # income/expense/transfer
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(default='NGN')
    category = models.CharField()
    subcategory = models.CharField(null=True)
    description = models.TextField()
    payment_method = models.CharField()  # cash/transfer/pos/cheque
    reference_number = models.CharField(null=True)
    receipt_url = models.URLField(null=True)
    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### Week 6: Dashboard Core

| Task | Hours | Owner |
|------|-------|-------|
| Dashboard aggregation endpoints | 16 | Backend |
| Cash position calculation (real-time) | 8 | Backend |
| Performance caching (Redis) | 8 | Backend |
| Dashboard layout + components | 20 | Frontend |
| Real-time cash position cards | 12 | Frontend |
| Recent transactions widget | 8 | Frontend |

**Deliverables:**
- [ ] Main dashboard showing all businesses
- [ ] Total cash position calculated
- [ ] Business cards with health indicators

#### Week 7: Business Detail Views

| Task | Hours | Owner |
|------|-------|-------|
| Business detail endpoints | 10 | Backend |
| Transaction summary by period | 8 | Backend |
| Category breakdown analytics | 8 | Backend |
| Business detail page UI | 16 | Frontend |
| Income vs expense charts | 12 | Frontend |
| Category pie charts | 8 | Frontend |
| Trend line charts | 10 | Frontend |

#### Week 8: Data Entry + Polish

| Task | Hours | Owner |
|------|-------|-------|
| Bulk transaction import (CSV) | 12 | Backend |
| Duplicate detection | 6 | Backend |
| Quick expense entry (mobile-optimized) | 10 | Frontend |
| Receipt photo upload | 12 | Full-stack |
| UI/UX polish + animations | 16 | Frontend |
| Performance optimization | 10 | All |

### 3.3 Month 3: Reports & Beta Launch (Weeks 9-12)

#### Week 9: Basic Reports

| Task | Hours | Owner |
|------|-------|-------|
| Profit & Loss report endpoint | 12 | Backend |
| Cash flow report | 10 | Backend |
| Report date range filtering | 6 | Backend |
| PDF export (reportlab) | 8 | Backend |
| Report viewer UI | 16 | Frontend |
| Print/export functionality | 8 | Frontend |

#### Week 10: PWA Implementation

| Task | Hours | Owner |
|------|-------|-------|
| Service Worker setup (Workbox) | 12 | Frontend |
| Offline caching strategy | 10 | Frontend |
| IndexedDB for local data | 12 | Frontend |
| Background sync for offline transactions | 12 | Frontend |
| App manifest + icons | 4 | Frontend |
| Push notification setup | 10 | Full-stack |

**Offline Capability Requirements:**
- View dashboard (cached data)
- Add transactions offline (queue for sync)
- View recent transactions
- Sync when connection restored

#### Week 11: Beta Preparation

| Task | Hours | Owner |
|------|-------|-------|
| User onboarding flow | 12 | Full-stack |
| In-app help/tooltips | 8 | Frontend |
| Error boundary + fallbacks | 8 | Frontend |
| Feedback collection widget | 6 | Frontend |
| Analytics integration (Mixpanel) | 8 | Full-stack |
| Security audit | 16 | Backend |
| Load testing (100 concurrent users) | 8 | DevOps |

#### Week 12: Beta Launch

| Task | Hours | Owner |
|------|-------|-------|
| Production deployment | 12 | DevOps |
| Monitoring + alerts setup | 8 | DevOps |
| Beta user onboarding (20 users) | 20 | All |
| Bug triage + hotfixes | 20 | All |
| Documentation | 10 | All |

### 3.4 Phase 1 Deliverables Checklist

**Core Features:**
- [ ] User registration + authentication
- [ ] Multi-business management (CRUD)
- [ ] Transaction recording (income/expense)
- [ ] Dashboard with cash positions
- [ ] Basic financial reports (P&L, cash flow)
- [ ] CSV import for transactions
- [ ] Receipt photo uploads

**Technical:**
- [ ] PWA with offline support
- [ ] Mobile-responsive design
- [ ] <3 second page load
- [ ] 99.5% uptime
- [ ] Automated testing (>70% coverage)
- [ ] CI/CD pipeline

**Business:**
- [ ] 20 active beta users
- [ ] NPS >30
- [ ] <10 critical bugs

---

## 4. Phase 2: Bank Integration

**Timeline:** Weeks 13-24  
**Goal:** Automated bank transaction sync for Nigerian banks

### 4.1 Month 4: Mono/Okra Integration (Weeks 13-16)

#### Week 13-14: Mono Integration

| Task | Hours | Owner |
|------|-------|-------|
| Mono API client implementation | 16 | Backend |
| OAuth flow for bank linking | 12 | Backend |
| Account details retrieval | 8 | Backend |
| Transaction fetch + storage | 16 | Backend |
| Bank connection UI flow | 20 | Frontend |
| Connection status dashboard | 8 | Frontend |

**Mono API Integration:**
```python
class MonoService:
    BASE_URL = "https://api.withmono.com/v1"
    
    def exchange_code(self, code: str) -> dict:
        """Exchange auth code for account access"""
        response = requests.post(
            f"{self.BASE_URL}/account/auth",
            json={"code": code},
            headers={"mono-sec-key": settings.MONO_SECRET_KEY}
        )
        return response.json()
    
    def get_transactions(self, account_id: str, 
                         start: date, end: date) -> list:
        """Fetch transactions for date range"""
        # Implementation
        pass
    
    def sync_transactions(self, bank_account: BankAccount):
        """Sync and store new transactions"""
        # Implementation with duplicate detection
        pass
```

#### Week 15-16: Okra Integration (Backup Provider)

| Task | Hours | Owner |
|------|-------|-------|
| Okra API client | 12 | Backend |
| Provider abstraction layer | 10 | Backend |
| Fallback logic (Mono → Okra) | 8 | Backend |
| Multiple provider UI handling | 10 | Frontend |
| Testing + error handling | 16 | All |

### 4.2 Month 5: Auto-Sync & Categorization (Weeks 17-20)

#### Week 17-18: Background Sync

| Task | Hours | Owner |
|------|-------|-------|
| Celery worker setup | 8 | Backend |
| Scheduled sync jobs (hourly) | 12 | Backend |
| Webhook handlers for real-time | 16 | Backend |
| Sync status tracking | 8 | Backend |
| Last synced indicators UI | 8 | Frontend |
| Manual sync trigger button | 4 | Frontend |

#### Week 19-20: Transaction Categorization

| Task | Hours | Owner |
|------|-------|-------|
| Basic keyword categorization | 12 | Backend |
| User-defined rules engine | 16 | Backend |
| Category suggestion endpoint | 8 | Backend |
| Category management UI | 12 | Frontend |
| Transaction editing (recategorize) | 10 | Frontend |
| Bulk categorization | 10 | Frontend |

**Categorization Logic:**
```python
class TransactionCategorizer:
    def categorize(self, transaction: dict) -> str:
        narration = transaction['narration'].lower()
        
        # Rule-based categorization
        if any(w in narration for w in ['salary', 'wages']):
            return 'salaries'
        if any(w in narration for w in ['rent', 'lease']):
            return 'rent'
        if any(w in narration for w in ['fuel', 'diesel']):
            return 'fuel'
        # ... more rules
        
        # User-defined rules
        for rule in self.get_user_rules():
            if rule.matches(transaction):
                return rule.category
        
        return 'uncategorized'
```

### 4.3 Month 6: Alerts & Team Features (Weeks 21-24)

#### Week 21-22: Alert System

| Task | Hours | Owner |
|------|-------|-------|
| Alert model + types | 8 | Backend |
| Alert trigger engine | 16 | Backend |
| Email notification (SendGrid) | 8 | Backend |
| SMS notification (Twilio) | 8 | Backend |
| Push notification (FCM) | 10 | Backend |
| Alert preferences UI | 12 | Frontend |
| Notification center UI | 10 | Frontend |

**Alert Types:**
```python
class AlertType(Enum):
    LOW_CASH = "low_cash"         # Balance below threshold
    UNUSUAL_EXPENSE = "unusual"    # Transaction > 2x daily average
    LARGE_TRANSACTION = "large"    # Transaction > defined amount
    SYNC_FAILED = "sync_failed"    # Bank sync issue
    DAILY_SUMMARY = "daily"        # End of day recap
    GOAL_ACHIEVED = "goal"         # Target reached
```

#### Week 23-24: Team Features

| Task | Hours | Owner |
|------|-------|-------|
| Role-based permissions model | 12 | Backend |
| Invitation flow | 10 | Backend |
| Activity logging | 8 | Backend |
| Team management UI | 14 | Frontend |
| Permission settings UI | 10 | Frontend |
| Audit trail viewer | 8 | Frontend |

**Permission Levels:**
- **Owner**: Full access, billing, delete org
- **Admin**: All features except billing/delete
- **Accountant**: View all, edit transactions
- **Manager**: View assigned businesses only
- **Viewer**: Read-only access

### 4.4 Phase 2 Deliverables Checklist

- [ ] Mono bank integration (30+ banks)
- [ ] Okra as backup provider
- [ ] Automated hourly sync
- [ ] Transaction categorization (keyword + rules)
- [ ] Alert system (email, SMS, push)
- [ ] Team member management
- [ ] Role-based permissions
- [ ] Activity audit log
- [ ] 200+ active users

---

## 5. Phase 3: Intelligence Layer

**Timeline:** Weeks 25-36  
**Goal:** AI-powered insights and predictions

### 5.1 Month 7: AI Categorization (Weeks 25-28)

| Task | Hours | Owner |
|------|-------|-------|
| Training data preparation | 16 | ML Engineer |
| OpenAI integration for categorization | 12 | Backend |
| ML model fine-tuning | 24 | ML Engineer |
| Confidence scoring | 8 | Backend |
| User feedback loop | 10 | Full-stack |
| A/B testing framework | 12 | Backend |

**AI Categorization Architecture:**
```python
class AICategorizationService:
    def categorize_transaction(self, transaction: dict) -> dict:
        # First: Check user-defined rules
        rule_match = self.check_rules(transaction)
        if rule_match:
            return {"category": rule_match, "confidence": 1.0}
        
        # Second: ML model prediction
        features = self.extract_features(transaction)
        prediction = self.model.predict(features)
        
        if prediction['confidence'] > 0.85:
            return prediction
        
        # Third: OpenAI API for complex cases
        return self.openai_categorize(transaction)
```

### 5.2 Month 8: Cash Flow Forecasting (Weeks 29-32)

| Task | Hours | Owner |
|------|-------|-------|
| Historical pattern analysis | 16 | Backend |
| Time-series forecasting model | 24 | ML Engineer |
| Forecast API endpoints | 10 | Backend |
| Scenario modeling (best/worst) | 12 | Backend |
| Forecast visualization UI | 20 | Frontend |
| What-if calculator | 16 | Frontend |

### 5.3 Month 9: Anomaly Detection (Weeks 33-36)

| Task | Hours | Owner |
|------|-------|-------|
| Anomaly detection model | 20 | ML Engineer |
| Real-time anomaly scoring | 12 | Backend |
| Alert integration | 8 | Backend |
| Insight generation | 16 | Backend |
| Anomaly dashboard | 16 | Frontend |
| Insight cards + recommendations | 12 | Frontend |

### 5.4 Phase 3 Deliverables

- [ ] AI categorization (95%+ accuracy)
- [ ] 30/60/90 day cash flow forecast
- [ ] Anomaly detection + alerts
- [ ] Business health scoring
- [ ] Actionable insights dashboard
- [ ] 500+ active users

---

## 6. Phase 4: Mobile & Expansion

**Timeline:** Weeks 37-48  
**Goal:** Native mobile apps and Ghana market entry

### 6.1 Month 10: React Native Apps (Weeks 37-40)

| Task | Hours | Owner |
|------|-------|-------|
| React Native project setup | 8 | Mobile |
| Navigation + routing | 12 | Mobile |
| Authentication flow | 16 | Mobile |
| Dashboard screen | 20 | Mobile |
| Transaction entry | 16 | Mobile |
| Offline sync (WatermelonDB) | 24 | Mobile |
| Push notifications | 10 | Mobile |
| Biometric authentication | 8 | Mobile |

### 6.2 Month 11: WhatsApp & Beyond (Weeks 41-44)

| Task | Hours | Owner |
|------|-------|-------|
| WhatsApp Business API setup | 16 | Backend |
| Conversational flows | 20 | Backend |
| Balance check commands | 8 | Backend |
| Expense submission via chat | 12 | Backend |
| Daily summary messages | 8 | Backend |
| App Store / Play Store prep | 16 | All |

### 6.3 Month 12: Ghana Expansion (Weeks 45-48)

| Task | Hours | Owner |
|------|-------|-------|
| Ghana banking APIs research | 12 | Backend |
| Multi-currency enhancement | 16 | Backend |
| Localization (GHS support) | 10 | Full-stack |
| Ghana-specific compliance | 8 | Legal |
| Marketing landing pages | 12 | Frontend |
| Beta launch in Ghana | 20 | All |

### 6.4 Phase 4 Deliverables

- [ ] iOS app in App Store
- [ ] Android app in Play Store
- [ ] WhatsApp bot for quick access
- [ ] Ghana market entry (50 users)
- [ ] 800+ total active users

---

## 7. Technical Architecture

### 7.1 System Components

```
                                 LOAD BALANCER
                                      │
                     ┌────────────────┼────────────────┐
                     │                │                │
                     ▼                ▼                ▼
              ┌───────────┐    ┌───────────┐    ┌───────────┐
              │  API Pod  │    │  API Pod  │    │  API Pod  │
              │  (Django) │    │  (Django) │    │  (Django) │
              └─────┬─────┘    └─────┬─────┘    └─────┬─────┘
                    │                │                │
                    └────────────────┼────────────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
                    ▼                ▼                ▼
             ┌───────────┐    ┌───────────┐    ┌───────────┐
             │ PostgreSQL│    │   Redis   │    │    S3     │
             │   (RDS)   │    │(ElastiC.) │    │ (Storage) │
             └───────────┘    └───────────┘    └───────────┘
                                     │
                                     ▼
             ┌───────────┐    ┌───────────┐    ┌───────────┐
             │  Celery   │    │  Celery   │    │  Celery   │
             │  Worker   │    │  Worker   │    │   Beat    │
             └───────────┘    └───────────┘    └───────────┘
```

### 7.2 Directory Structure

```
disbursify-flow/
├── backend/
│   ├── config/                    # Django settings
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   ├── production.py
│   │   │   └── test.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   ├── apps/
│   │   ├── accounts/              # User & auth
│   │   ├── organizations/         # Multi-tenancy
│   │   ├── businesses/            # Business entities
│   │   ├── transactions/          # Financial records
│   │   ├── integrations/          # Bank APIs
│   │   ├── analytics/             # Reports & insights
│   │   ├── notifications/         # Alerts
│   │   └── ai/                    # ML features
│   │
│   ├── utils/                     # Shared utilities
│   ├── tests/                     # Test suites
│   ├── manage.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/            # React components
│   │   │   ├── common/            # Buttons, inputs, etc.
│   │   │   ├── dashboard/         # Dashboard widgets
│   │   │   ├── transactions/      # Transaction UI
│   │   │   ├── reports/           # Report viewers
│   │   │   └── settings/          # Settings pages
│   │   │
│   │   ├── pages/                 # Route pages
│   │   ├── hooks/                 # Custom hooks
│   │   ├── store/                 # Zustand stores
│   │   ├── services/              # API clients
│   │   ├── utils/                 # Helpers
│   │   ├── App.tsx
│   │   └── main.tsx
│   │
│   ├── public/
│   ├── package.json
│   └── Dockerfile
│
├── mobile/
│   ├── src/
│   │   ├── screens/
│   │   ├── components/
│   │   ├── navigation/
│   │   ├── store/
│   │   └── services/
│   │
│   ├── ios/
│   ├── android/
│   └── package.json
│
├── infrastructure/
│   ├── terraform/                 # IaC
│   ├── docker-compose.yml         # Local dev
│   └── k8s/                       # Kubernetes (future)
│
├── docs/
│   ├── api/                       # API documentation
│   ├── architecture/              # Design docs
│   └── guides/                    # Developer guides
│
└── scripts/
    ├── setup.sh                   # Dev setup
    ├── deploy.sh                  # Deployment
    └── seed_data.py               # Test data
```

---

## 8. Database Design

### 8.1 Core Schema

```sql
-- Organizations (tenant root)
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    owner_id UUID NOT NULL,
    subscription_tier VARCHAR(50) DEFAULT 'starter',
    subscription_status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    settings JSONB DEFAULT '{}'
);

-- Businesses (entities within org)
CREATE TABLE businesses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    business_type VARCHAR(50),
    registration_number VARCHAR(100),
    primary_currency VARCHAR(3) DEFAULT 'NGN',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'
);

-- Chart of Accounts
CREATE TABLE accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    business_id UUID NOT NULL REFERENCES businesses(id),
    account_type VARCHAR(50) NOT NULL,
    account_name VARCHAR(255) NOT NULL,
    currency VARCHAR(3) DEFAULT 'NGN',
    current_balance DECIMAL(15,2) DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);

-- Transactions
CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    business_id UUID NOT NULL REFERENCES businesses(id),
    transaction_date DATE NOT NULL,
    transaction_type VARCHAR(50) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'NGN',
    category VARCHAR(100),
    description TEXT,
    payment_method VARCHAR(50),
    reference_number VARCHAR(100),
    receipt_url TEXT,
    bank_transaction_id VARCHAR(255),
    is_reconciled BOOLEAN DEFAULT FALSE,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Bank Accounts (connected)
CREATE TABLE bank_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    business_id UUID NOT NULL REFERENCES businesses(id),
    bank_name VARCHAR(100),
    account_number VARCHAR(20),
    provider VARCHAR(50),  -- mono, okra, manual
    provider_account_id VARCHAR(255),
    last_synced_at TIMESTAMP,
    sync_status VARCHAR(50) DEFAULT 'active',
    current_balance DECIMAL(15,2)
);

-- Indexes for performance
CREATE INDEX idx_txn_org_date ON transactions(organization_id, transaction_date);
CREATE INDEX idx_txn_business ON transactions(business_id, transaction_date);
CREATE INDEX idx_txn_category ON transactions(category);
```

### 8.2 Entity Relationship Diagram

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│    Users     │       │Organizations │       │  Businesses  │
├──────────────┤       ├──────────────┤       ├──────────────┤
│ id           │──────►│ id           │◄──────│ id           │
│ email        │       │ owner_id     │       │ org_id       │
│ password     │       │ name         │       │ name         │
│ ...          │       │ subscription │       │ industry     │
└──────────────┘       └──────────────┘       └──────┬───────┘
                                                      │
                       ┌──────────────────────────────┼──────────────┐
                       │                              │              │
                       ▼                              ▼              ▼
              ┌──────────────┐              ┌──────────────┐  ┌──────────────┐
              │ Transactions │              │   Accounts   │  │ BankAccounts │
              ├──────────────┤              ├──────────────┤  ├──────────────┤
              │ id           │              │ id           │  │ id           │
              │ business_id  │              │ business_id  │  │ business_id  │
              │ amount       │              │ account_name │  │ bank_name    │
              │ category     │              │ balance      │  │ provider     │
              │ ...          │              │ ...          │  │ ...          │
              └──────────────┘              └──────────────┘  └──────────────┘
```

---

## 9. API Specification

### 9.1 API Overview

**Base URL:** `https://api.disbursifyflow.com/v1`

**Authentication:** Bearer token (JWT)

### 9.2 Core Endpoints

#### Authentication
```
POST   /auth/register           # Create account
POST   /auth/login              # Get tokens
POST   /auth/refresh            # Refresh access token
POST   /auth/logout             # Invalidate tokens
POST   /auth/password/reset     # Request reset
POST   /auth/password/confirm   # Confirm reset
```

#### Organizations
```
GET    /organizations/me        # Get current org
PATCH  /organizations/me        # Update org settings
GET    /organizations/me/subscription
POST   /organizations/me/team/invite
```

#### Businesses
```
GET    /businesses              # List all businesses
POST   /businesses              # Create business
GET    /businesses/{id}         # Get business details
PATCH  /businesses/{id}         # Update business
DELETE /businesses/{id}         # Delete business
GET    /businesses/{id}/stats   # Business statistics
```

#### Transactions
```
GET    /businesses/{id}/transactions
POST   /businesses/{id}/transactions
GET    /transactions/{id}
PATCH  /transactions/{id}
DELETE /transactions/{id}
POST   /transactions/bulk-import
```

#### Reports
```
GET    /businesses/{id}/reports/profit-loss
GET    /businesses/{id}/reports/cash-flow
GET    /businesses/{id}/reports/balance-sheet
GET    /organizations/dashboard
GET    /organizations/consolidated
```

#### Bank Integration
```
GET    /businesses/{id}/bank-accounts
POST   /businesses/{id}/bank-accounts/connect
POST   /bank-accounts/{id}/sync
DELETE /bank-accounts/{id}/disconnect
```

### 9.3 Request/Response Examples

**Create Transaction:**
```json
// POST /businesses/{id}/transactions
// Request
{
  "transaction_date": "2026-02-01",
  "transaction_type": "expense",
  "amount": 250000.00,
  "category": "rent",
  "description": "January office rent",
  "payment_method": "bank_transfer",
  "reference_number": "TRF-12345"
}

// Response
{
  "id": "txn_abc123",
  "business_id": "biz_xyz789",
  "transaction_date": "2026-02-01",
  "transaction_type": "expense",
  "amount": 250000.00,
  "currency": "NGN",
  "category": "rent",
  "description": "January office rent",
  "payment_method": "bank_transfer",
  "reference_number": "TRF-12345",
  "created_at": "2026-02-01T10:30:00Z",
  "created_by": "user_def456"
}
```

**Dashboard Response:**
```json
// GET /organizations/dashboard
{
  "total_cash_position": {
    "NGN": 47250000.00,
    "USD": 12500.00
  },
  "today_summary": {
    "income": 1840000.00,
    "expenses": 920000.00,
    "net": 920000.00
  },
  "businesses": [
    {
      "id": "biz_001",
      "name": "Mama's Kitchen",
      "balance": 12500000.00,
      "change_percent": 15.2,
      "health": "healthy"
    },
    // ... more businesses
  ],
  "alerts": [
    {
      "type": "low_cash",
      "business_id": "biz_003",
      "message": "Cash will run out in 5 days"
    }
  ]
}
```

---

## 10. Security Implementation

### 10.1 Authentication Security

| Measure | Implementation |
|---------|----------------|
| Password hashing | Argon2 (Django default) |
| JWT expiry | Access: 15 min, Refresh: 7 days |
| Token storage | HttpOnly cookies (web), secure storage (mobile) |
| 2FA | TOTP via pyotp, enforced for admins |
| Rate limiting | 100 req/min per user, 1000/min per IP |

### 10.2 Data Security

| Layer | Protection |
|-------|------------|
| Transport | TLS 1.3 enforced |
| At rest | AES-256 encryption (RDS) |
| PII fields | Field-level encryption |
| Backups | Encrypted, 30-day retention |
| Audit logs | Immutable, 2-year retention |

### 10.3 Multi-Tenancy Security

```python
# Middleware ensuring tenant isolation
class TenantMiddleware:
    def __call__(self, request):
        if request.user.is_authenticated:
            org = request.user.organization
            # Set PostgreSQL session variable for RLS
            connection.cursor().execute(
                "SET app.current_org_id = %s", [str(org.id)]
            )
        return self.get_response(request)

# Row-Level Security policy
"""
CREATE POLICY org_isolation ON transactions
    USING (organization_id = current_setting('app.current_org_id')::UUID);
"""
```

### 10.4 Compliance

| Regulation | Compliance Measures |
|------------|---------------------|
| NDPR | Data mapping, consent management, DPO appointment |
| PCI DSS | No card storage, Paystack handles payments |
| SOC 2 | Targeted for Year 2 |

---

## 11. DevOps & Infrastructure

### 11.1 Environment Strategy

| Environment | Purpose | Infrastructure |
|-------------|---------|----------------|
| Local | Development | Docker Compose |
| Staging | Testing, QA | AWS (minimal) |
| Production | Live users | AWS (scaled) |

### 11.2 CI/CD Pipeline

```yaml
# .github/workflows/main.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run backend tests
        run: |
          cd backend
          pip install -r requirements.txt
          pytest --cov=apps/

      - name: Run frontend tests
        run: |
          cd frontend
          npm ci
          npm run test

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          # Build and push Docker images
          # Deploy to AWS ECS
```

### 11.3 Monitoring & Alerting

| Tool | Purpose |
|------|---------|
| Sentry | Error tracking, performance |
| CloudWatch | Infrastructure metrics |
| PagerDuty | On-call alerting |
| Mixpanel | Product analytics |

---

## 12. Testing Strategy

### 12.1 Testing Pyramid

```
                    ▲
                   /│\
                  / │ \        E2E Tests (10%)
                 /  │  \       • Critical user flows
                /   │   \      • Cross-browser testing
               ───────────
              /     │     \    Integration Tests (30%)
             /      │      \   • API endpoints
            /       │       \  • Database operations
           ─────────────────
          /         │         \  Unit Tests (60%)
         /          │          \ • Business logic
        /           │           \• Utilities
       ───────────────────────────
```

### 12.2 Coverage Targets

| Component | Target | Critical Paths |
|-----------|--------|----------------|
| Backend | 80% | Auth, transactions, reports |
| Frontend | 70% | Dashboard, forms |
| E2E | Critical flows | Signup → Add business → Add transaction |

### 12.3 Test Data Strategy

- Factories for test data generation (Factory Boy)
- Seed scripts for demo environments
- Anonymized production data for staging

---

## 13. Team & Resources

### 13.1 Team Structure

**Phase 1 (MVP):**
- 1 Founder/Product Lead
- 1 Senior Full-Stack Developer
- 1 Junior Developer (or contractor)

**Phase 2 (Scale):**
- 1 Founder/CEO
- 1 Tech Lead
- 2 Backend Developers
- 1 Frontend Developer
- 1 Product Designer
- 1 Customer Success

**Phase 3+ (Growth):**
- Add: ML Engineer, Mobile Developer, DevOps, Sales

### 13.2 Key Hires Timeline

| Role | When | Priority |
|------|------|----------|
| Senior Full-Stack | Month 1 | P0 |
| Junior Developer | Month 2 | P1 |
| Product Designer | Month 4 | P1 |
| Customer Success | Month 5 | P1 |
| DevOps Engineer | Month 8 | P2 |
| Mobile Developer | Month 9 | P2 |

### 13.3 Development Velocity Assumptions

- Sprint length: 2 weeks
- Story points per sprint: 40-50 (team of 3)
- Velocity ramp-up: 3 sprints to full speed
- Buffer for bugs/tech debt: 20% of capacity

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Feb 2, 2026 | Engineering Team | Initial release |

---

*This implementation plan is a living document and will be updated as the project evolves.*

© 2026 Disbursify. All Rights Reserved.
