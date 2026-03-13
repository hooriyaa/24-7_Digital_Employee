# SECURITY.md — Global Security Law

> **Customer Success Digital FTE — Security Rules**
>
> This document defines **security rules that apply to all code**.
> Security overrides convenience, speed, and creativity.
> LLMs must refuse to generate insecure code.

---

```slc
@block SECURITY cs_fte_security
priority: critical
intent: "Define global security laws for all code"
scope: global
depends_on: CONSTRAINTS.md

content:
  backend_rules:
    - "All API keys stored in environment variables only"
    - "JWT authentication required for all protected endpoints"
    - "Rate limiting mandatory (100 requests/minute per client)"
    - "Input validation on all endpoints using Pydantic"
    - "SQL injection prevention via SQLModel ORM only (no raw SQL)"
    - "CORS configured for specific origins only"
    - "HTTPS enforced in production"
    - "Sensitive data encrypted at rest (AES-256)"
    - "PostgreSQL credentials via secrets management"
  
  frontend_rules:
    - "No API keys exposed in client-side code"
    - "All API calls via secure HTTPS endpoints"
    - "JWT tokens stored in httpOnly cookies only"
    - "XSS prevention via React escaping (no dangerouslySetInnerHTML)"
    - "CSRF protection on all state-changing operations"
    - "Content Security Policy (CSP) headers enforced"
    - "Form validation on client and server"
  
  api_rules:
    - "Authentication required for all /api/* endpoints"
    - "Request signing for webhook verification (Gmail, UltraMsg)"
    - "Response sanitization (no internal error details)"
    - "API versioning via URL path (/api/v1/...)"
    - "Request logging without PII"
    - "Idempotency keys for write operations"
  
  data_rules:
    - "Customer PII encrypted in database"
    - "Conversation history access logged"
    - "Right to deletion implemented (GDPR)"
    - "No conversation data in logs"
    - "pgvector embeddings anonymized"
  
  infrastructure_rules:
    - "Kubernetes secrets for sensitive config"
    - "Network policies isolate services"
    - "Pod security contexts restrict privileges"
    - "Image scanning in CI/CD pipeline"
    - "Kafka SASL authentication"
@end
```

---

## BACKEND RULES

### Authentication & Authorization

| Rule | Implementation |
|------|----------------|
| API Key Storage | Environment variables only (`.env`, Kubernetes Secrets) |
| JWT Authentication | Required for all protected endpoints |
| Token Expiry | Access tokens: 15 minutes, Refresh tokens: 7 days |
| Role-Based Access | Admin, Agent, Customer roles enforced |

### Input Validation

| Rule | Implementation |
|------|----------------|
| Validation Library | Pydantic v2 for all request/response models |
| Sanitization | Strip HTML, escape special characters |
| Size Limits | Max request body: 1MB |
| Rate Limiting | 100 requests/minute per client IP |

### Database Security

| Rule | Implementation |
|------|----------------|
| ORM Only | SQLModel only — no raw SQL queries |
| Connection Pooling | PgBouncer with max 20 connections |
| Encryption | AES-256 for PII fields |
| Credentials | Via environment variables or Kubernetes Secrets |

### Network Security

| Rule | Implementation |
|------|----------------|
| CORS | Whitelist specific origins only |
| HTTPS | Enforced in production (TLS 1.3) |
| Headers | Security headers (HSTS, X-Frame-Options, etc.) |

---

## FRONTEND RULES

### Client-Side Security

| Rule | Implementation |
|------|----------------|
| API Keys | Never exposed in client-side code |
| Token Storage | httpOnly, secure cookies only |
| XSS Prevention | React auto-escaping; no `dangerouslySetInnerHTML` |
| CSRF Protection | Anti-CSRF tokens on all state-changing forms |

### Content Security

| Rule | Implementation |
|------|----------------|
| CSP Headers | Strict Content-Security-Policy |
| Subresource Integrity | SRI hashes for all external scripts |
| Form Validation | Client + server validation required |

---

## API RULES

### Endpoint Security

| Rule | Implementation |
|------|----------------|
| Authentication | Required for all `/api/*` endpoints |
| Webhook Verification | HMAC signature verification (Gmail, UltraMsg) |
| Error Handling | Generic error messages; no stack traces |
| API Versioning | URL path versioning (`/api/v1/...`) |

### Request/Response Security

| Rule | Implementation |
|------|----------------|
| Logging | No PII in logs; request IDs for tracing |
| Idempotency | Idempotency keys for POST/PUT operations |
| Response Size | Max response: 500KB |
| Pagination | Required for list endpoints (max 100 items/page) |

---

## DATA RULES

### Customer Data Protection

| Rule | Implementation |
|------|----------------|
| PII Encryption | AES-256 for name, email, phone |
| Conversation Access | All access logged with timestamp + user |
| Right to Deletion | GDPR-compliant data deletion endpoint |
| Data Retention | Auto-delete after 2 years of inactivity |

### Vector Memory Security

| Rule | Implementation |
|------|----------------|
| Embedding Anonymization | No PII in pgvector embeddings |
| Access Control | Vector queries require authentication |
| Similarity Threshold | Min cosine similarity: 0.7 for RAG retrieval |

---

## INFRASTRUCTURE RULES

### Kubernetes Security

| Rule | Implementation |
|------|----------------|
| Secrets | Kubernetes Secrets only (no ConfigMaps for sensitive data) |
| Network Policies | Services isolated; default deny all |
| Pod Security | Non-root containers; read-only root filesystem |
| Image Security | Scan images in CI/CD; block critical CVEs |

### Kafka Security

| Rule | Implementation |
|------|----------------|
| Authentication | SASL/SCRAM authentication |
| Encryption | TLS for all broker communication |
| ACLs | Topic-level access control |

---

## VIOLATION RESPONSE

If any security rule is violated, the LLM must:

1. **Stop code generation immediately**
2. **Report the violation** with specific rule reference
3. **Provide secure alternative** implementation
4. **Log the incident** in MEMORY.md

---

*End of SECURITY.md — Customer Success Digital FTE v1.0.0*
