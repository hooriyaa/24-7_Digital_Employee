# CONTRACT.md — API Contract

> **Customer Success Digital FTE — Backend API Specification**
>
> This document is **authoritative** for all API endpoints, schemas, and payloads.
> Frontend must derive from this contract. No invention allowed.

---

```slc
@block INDEX api_contract_index
priority: critical
intent: "API contract router"
scope: backend
failure_if_skipped: true

read_order:
  - backend_specs/ARCH.md
  - backend_specs/PLAN.md
  - backend_specs/CONTRACT.md

content:
  short: "Complete API specification for Customer Success Digital FTE"
  version: "v1"
  base_path: "/api/v1"
@end

@block CONTRACT api_contract
priority: critical
intent: "Define all API endpoints and schemas"
scope: backend
depends_on: backend_specs/ARCH.md

content:
  api_version: "v1"
  base_url: "/api/v1"
  authentication: "JWT Bearer token"
  content_type: "application/json"
  
  endpoints:
    # ==================== HEALTH ====================
    - path: "/health"
      method: "GET"
      auth: false
      description: "Health check endpoint"
      request: null
      response:
        status: 200
        body:
          status: "string"
          timestamp: "string"
          version: "string"
    
    # ==================== CUSTOMERS ====================
    - path: "/customers"
      method: "POST"
      auth: true
      description: "Create a new customer"
      request:
        body:
          email: "string (required, unique)"
          phone: "string (optional, unique)"
          name: "string (required)"
      response:
        status: 201
        body:
          id: "UUID"
          email: "string"
          phone: "string"
          name: "string"
          created_at: "timestamp"
    
    - path: "/customers/{customer_id}"
      method: "GET"
      auth: true
      description: "Get customer by ID"
      request:
        params:
          customer_id: "UUID"
      response:
        status: 200
        body:
          id: "UUID"
          email: "string"
          phone: "string"
          name: "string"
          channels: "array of ChannelIdentity"
          created_at: "timestamp"
          updated_at: "timestamp"
    
    - path: "/customers/lookup"
      method: "GET"
      auth: true
      description: "Lookup customer by email or phone"
      request:
        query:
          identifier: "string (email or phone)"
      response:
        status: 200
        body:
          customer: "Customer object or null"
          found: "boolean"
    
    # ==================== TICKETS ====================
    - path: "/tickets"
      method: "POST"
      auth: true
      description: "Create a new ticket"
      request:
        body:
          customer_id: "UUID (required)"
          channel: "string (required: gmail|whatsapp|web)"
          subject: "string (optional)"
          content: "string (required)"
          priority: "string (optional: low|normal|high|urgent)"
      response:
        status: 201
        body:
          id: "UUID"
          customer_id: "UUID"
          status: "string"
          channel: "string"
          subject: "string"
          created_at: "timestamp"
    
    - path: "/tickets"
      method: "GET"
      auth: true
      description: "List tickets with pagination"
      request:
        query:
          page: "integer (default: 1)"
          limit: "integer (default: 20, max: 100)"
          status: "string (optional filter)"
          customer_id: "UUID (optional filter)"
      response:
        status: 200
        body:
          tickets: "array of Ticket"
          total: "integer"
          page: "integer"
          limit: "integer"
          has_more: "boolean"
    
    - path: "/tickets/{ticket_id}"
      method: "GET"
      auth: true
      description: "Get ticket by ID"
      request:
        params:
          ticket_id: "UUID"
      response:
        status: 200
        body:
          id: "UUID"
          customer_id: "UUID"
          status: "string"
          priority: "string"
          subject: "string"
          sentiment_score: "float"
          confidence_score: "float"
          assigned_to: "string"
          created_at: "timestamp"
          resolved_at: "timestamp"
          conversation: "Conversation object"
    
    - path: "/tickets/{ticket_id}"
      method: "PUT"
      auth: true
      description: "Update ticket"
      request:
        params:
          ticket_id: "UUID"
        body:
          status: "string (optional)"
          priority: "string (optional)"
          assigned_to: "string (optional)"
      response:
        status: 200
        body:
          id: "UUID"
          status: "string"
          updated_at: "timestamp"
    
    - path: "/tickets/{ticket_id}/close"
      method: "POST"
      auth: true
      description: "Close a ticket"
      request:
        params:
          ticket_id: "UUID"
      response:
        status: 200
        body:
          id: "UUID"
          status: "closed"
          resolved_at: "timestamp"
    
    # ==================== MESSAGES ====================
    - path: "/tickets/{ticket_id}/messages"
      method: "POST"
      auth: true
      description: "Add message to conversation"
      request:
        params:
          ticket_id: "UUID"
        body:
          content: "string (required)"
          sender_type: "string (required: customer|agent|system)"
          channel: "string (required)"
      response:
        status: 201
        body:
          id: "UUID"
          content: "string"
          sender_type: "string"
          created_at: "timestamp"
    
    - path: "/tickets/{ticket_id}/messages"
      method: "GET"
      auth: true
      description: "Get conversation messages"
      request:
        params:
          ticket_id: "UUID"
        query:
          limit: "integer (default: 50)"
      response:
        status: 200
        body:
          messages: "array of Message"
          total: "integer"
    
    # ==================== AI AGENT ====================
    - path: "/agent/respond"
      method: "POST"
      auth: true
      description: "Generate AI response for a ticket"
      request:
        body:
          ticket_id: "UUID (required)"
          force_provider: "string (optional: openai|gemini|qwen)"
      response:
        status: 200
        body:
          response: "string"
          provider: "string"
          confidence_score: "float"
          sentiment_score: "float"
          requires_escalation: "boolean"
          escalation_reason: "string or null"
          tokens_used: "integer"
    
    - path: "/agent/providers"
      method: "GET"
      auth: true
      description: "Get AI provider status"
      request: null
      response:
        status: 200
        body:
          providers:
            - name: "string"
              priority: "integer"
              is_active: "boolean"
              tokens_used_today: "integer"
              daily_limit: "integer"
    
    # ==================== ESCALATIONS ====================
    - path: "/escalations"
      method: "POST"
      auth: true
      description: "Create escalation"
      request:
        body:
          ticket_id: "UUID (required)"
          reason: "string (required: low_confidence|negative_sentiment|customer_request|complex_issue)"
          escalated_to: "string (optional)"
      response:
        status: 201
        body:
          id: "UUID"
          ticket_id: "UUID"
          reason: "string"
          escalated_to: "string"
          escalated_at: "timestamp"
    
    - path: "/escalations/{escalation_id}"
      method: "GET"
      auth: true
      description: "Get escalation by ID"
      request:
        params:
          escalation_id: "UUID"
      response:
        status: 200
        body:
          id: "UUID"
          ticket_id: "UUID"
          reason: "string"
          escalated_to: "string"
          escalated_at: "timestamp"
          resolved_at: "timestamp"
          resolution_notes: "string"
    
    - path: "/escalations/{escalation_id}/resolve"
      method: "POST"
      auth: true
      description: "Resolve escalation"
      request:
        params:
          escalation_id: "UUID"
        body:
          resolution_notes: "string (required)"
      response:
        status: 200
        body:
          id: "UUID"
          resolved_at: "timestamp"
          resolution_notes: "string"
    
    # ==================== WEBHOOKS ====================
    - path: "/webhooks/gmail"
      method: "POST"
      auth: false
      description: "Gmail Pub/Sub webhook endpoint"
      request:
        headers:
          X-Google-Channel-ID: "string"
          X-Google-Resource-ID: "string"
          X-Google-Resource-STATE: "string"
        body: "Gmail Pub/Sub message format"
      response:
        status: 200
        body: null
    
    - path: "/webhooks/ultramsg"
      method: "POST"
      auth: false
      description: "UltraMsg webhook endpoint"
      request:
        body:
          from: "string (phone number)"
          message: "string"
          timestamp: "integer"
      response:
        status: 200
        body: null
    
    # ==================== WEB FORM ====================
    - path: "/web/support"
      method: "POST"
      auth: false
      description: "Public web support form submission"
      request:
        body:
          name: "string (required)"
          email: "string (required)"
          subject: "string (required)"
          message: "string (required)"
      response:
        status: 201
        body:
          ticket_id: "UUID"
          status: "submitted"
          tracking_url: "string"
    
    - path: "/web/status/{ticket_id}"
      method: "GET"
      auth: false
      description: "Public ticket status check"
      request:
        params:
          ticket_id: "UUID"
      response:
        status: 200
        body:
          ticket_id: "UUID"
          status: "string"
          updated_at: "timestamp"
@end
```

---

## ERROR RESPONSES

All endpoints return errors in the following format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}
  }
}
```

### Standard Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `UNAUTHORIZED` | 401 | Missing or invalid authentication |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `VALIDATION_ERROR` | 400 | Request validation failed |
| `CONFLICT` | 409 | Resource conflict (e.g., duplicate email) |
| `RATE_LIMITED` | 429 | Rate limit exceeded |
| `INTERNAL_ERROR` | 500 | Internal server error |

---

## RATE LIMITS

| Endpoint Type | Limit |
|---------------|-------|
| Public endpoints | 10 requests/minute |
| Authenticated endpoints | 100 requests/minute |
| AI agent endpoints | 20 requests/minute |

---

## PAGINATION

All list endpoints support pagination:

```json
{
  "data": [],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "has_more": true
  }
}
```

---

*End of CONTRACT.md — Customer Success Digital FTE v1.0.0*
