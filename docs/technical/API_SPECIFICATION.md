# Disbursify Dash - API Specification v1.0

**Base URL:** `https://api.disbursify.com/v1`  
**Last Updated:** February 2, 2026

## Authentication

### Register
```http
POST /auth/register
Body: { "email", "password", "phone", "first_name", "last_name" }
Response: { user, verification_required }
```

### Login
```http
POST /auth/login
Body: { "email", "password", "remember_me" }
Response: { access_token, refresh_token, user, organizations }
```

### Refresh Token
```http
POST /auth/refresh
Body: { "refresh_token" }
```

## Businesses

### List Businesses
```http
GET /businesses
Headers: Authorization, X-Organization-Id
Query: is_active, industry, sort, order
```

### Create Business
```http
POST /businesses
Body: { name, industry, business_type, primary_currency, opening_balance }
```

### Get Business Summary
```http
GET /businesses/{id}/summary
Query: period, start_date, end_date
```

## Transactions

### List Transactions
```http
GET /transactions
Query: business_id, type, category, start_date, end_date, search, page, per_page
```

### Create Transaction
```http
POST /transactions
Body: { business_id, transaction_date, type, amount, category, description, payment_method }
```

### Upload Receipt
```http
POST /transactions/{id}/receipts
Content-Type: multipart/form-data
```

## Reports

### Profit & Loss
```http
GET /reports/profit-loss
Query: business_id, start_date, end_date, group_by
```

### Cash Flow
```http
GET /reports/cash-flow
Query: business_id, start_date, end_date
```

### Export Report
```http
POST /reports/export
Body: { report_type, format, business_id, start_date, end_date }
```

## Dashboard

### Main Dashboard
```http
GET /dashboard
Response: { total_cash, today, businesses[], alerts[], recent_transactions[] }
```

## Bank Accounts

### Connect Bank
```http
POST /bank-accounts/connect
Body: { business_id, provider }
Response: { connect_url, session_id }
```

### Trigger Sync
```http
POST /bank-accounts/{id}/sync
```

## Error Codes

| Code | Description |
|------|-------------|
| 400  | Validation error |
| 401  | Unauthorized |
| 403  | Forbidden |
| 404  | Not found |
| 429  | Rate limited |
| 500  | Server error |

## Rate Limits

| Tier | Requests/min |
|------|--------------|
| Starter | 120 |
| Growth | 300 |
| Business | 600 |

---
© 2026 Disbursify. All Rights Reserved.
