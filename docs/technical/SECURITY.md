# Disbursify Dash - Security Architecture

## Overview

Security is paramount for Disbursify Dash. We handle sensitive financial data for thousands of businesses, making robust security non-negotiable.

---

## 1. Authentication & Authorization

### 1.1 Password Security
- **Hashing**: Argon2id (memory-hard, resistant to GPU attacks)
- **Minimum Requirements**: 8+ chars, mixed case, number, special char
- **Breach Detection**: Check against HaveIBeenPwned API

### 1.2 Token Management
- **Access Tokens**: JWT, RS256, 15-minute expiry
- **Refresh Tokens**: Opaque, 7-day expiry (30 with "remember me")
- **Token Rotation**: Refresh token rotated on each use

### 1.3 Multi-Factor Authentication
- TOTP-based (Google Authenticator, Authy)
- SMS OTP for phone verification
- Recovery codes for backup

### 1.4 Session Security
- Device fingerprinting
- Concurrent session limits (5 devices)
- Suspicious login alerts

---

## 2. Data Protection

### 2.1 Encryption in Transit
- TLS 1.3 enforced (HSTS enabled)
- Certificate pinning for mobile apps
- Perfect Forward Secrecy

### 2.2 Encryption at Rest
- Database: AWS RDS encryption (AES-256)
- S3: Server-side encryption (SSE-S3)
- Sensitive fields: Application-level encryption (bank tokens)

### 2.3 Field-Level Encryption
Fields encrypted at application layer:
- Bank account tokens
- API keys
- 2FA secrets

---

## 3. Multi-Tenancy Isolation

### 3.1 Row-Level Security (RLS)
```sql
-- All queries scoped to organization
CREATE POLICY org_isolation ON transactions
USING (organization_id = current_setting('app.current_org_id')::UUID);
```

### 3.2 Application Layer
- Organization context set on every request
- Cross-tenant queries impossible by design
- Audit logging for all data access

---

## 4. API Security

### 4.1 Rate Limiting
| Tier | Requests/min |
|------|--------------|
| Starter | 120 |
| Growth | 300 |
| Business | 600 |

### 4.2 Input Validation
- Schema validation on all endpoints
- SQL injection prevention (parameterized queries)
- XSS prevention (output encoding)

### 4.3 CORS Policy
- Whitelist of allowed origins
- Credentials only from trusted domains

---

## 5. Compliance

### 5.1 NDPR (Nigerian Data Protection Regulation)
- Data residency in Africa (AWS Africa / EU regions)
- User consent management
- Right to erasure implementation
- Data Processing Agreement available

### 5.2 PCI DSS Considerations
- No card data stored directly
- Paystack handles payment processing
- Tokenization for bank connections

---

## 6. Incident Response

### 6.1 Monitoring
- Real-time anomaly detection
- Failed login monitoring
- Data exfiltration alerts

### 6.2 Response Plan
1. Detect & contain
2. Assess impact
3. Notify affected users (within 72 hours)
4. Remediate
5. Post-mortem

---

## 7. Security Practices

- Regular penetration testing
- Dependency vulnerability scanning (Snyk)
- Security code reviews
- Bug bounty program (planned)

---

© 2026 Disbursify. All Rights Reserved.
