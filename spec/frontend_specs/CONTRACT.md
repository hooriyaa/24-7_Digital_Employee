# CONTRACT.md — Frontend Contract

> **Customer Success Digital FTE — Frontend Specification**
>
> This document defines **TypeScript types, form schemas, and UI contracts**.
> All API types derived from backend CONTRACT.md — no invention.

---

```slc
@block INDEX frontend_contract_index
priority: critical
intent: "Frontend contract router"
scope: frontend
failure_if_skipped: true

read_order:
  - frontend_specs/ARCH.md
  - frontend_specs/PLAN.md
  - frontend_specs/CONTRACT.md

content:
  short: "Frontend TypeScript types and UI contracts"
@end

@block TYPES frontend_types
priority: critical
intent: "Define TypeScript types from backend API"
scope: frontend
depends_on: backend_specs/CONTRACT.md

content:
  types:
    - name: "Customer"
      source: "backend_specs/CONTRACT.md - Customer schema"
      fields:
        id: "string"
        email: "string"
        phone: "string | null"
        name: "string"
        created_at: "string"
        updated_at: "string"
    
    - name: "Ticket"
      source: "backend_specs/CONTRACT.md - Ticket schema"
      fields:
        id: "string"
        customer_id: "string"
        status: "'open' | 'in_progress' | 'waiting_customer' | 'resolved' | 'escalated' | 'closed'"
        priority: "'low' | 'normal' | 'high' | 'urgent'"
        subject: "string | null"
        sentiment_score: "number | null"
        confidence_score: "number | null"
        assigned_to: "string | null"
        created_at: "string"
        resolved_at: "string | null"
    
    - name: "Message"
      source: "backend_specs/CONTRACT.md - Message schema"
      fields:
        id: "string"
        conversation_id: "string"
        sender_type: "'customer' | 'agent' | 'system'"
        content: "string"
        channel: "string"
        created_at: "string"
    
    - name: "Conversation"
      source: "backend_specs/CONTRACT.md - Conversation schema"
      fields:
        id: "string"
        ticket_id: "string"
        message_count: "number"
        messages: "Message[]"
    
    - name: "Escalation"
      source: "backend_specs/CONTRACT.md - Escalation schema"
      fields:
        id: "string"
        ticket_id: "string"
        reason: "string"
        escalated_to: "string | null"
        escalated_at: "string"
        resolved_at: "string | null"
        resolution_notes: "string | null"
    
    - name: "User"
      source: "Auth token payload"
      fields:
        id: "string"
        email: "string"
        role: "'admin' | 'agent'"
    
    - name: "AuthTokens"
      source: "Auth response"
      fields:
        access_token: "string"
        refresh_token: "string"
        token_type: "'bearer'"
        expires_in: "number"
@end

@block FORMS frontend_forms
priority: critical
intent: "Define form schemas with Zod validation"
scope: frontend
depends_on: frontend_types

content:
  forms:
    - name: "WebSupportForm"
      route: "/"
      validation: "Zod"
      fields:
        - name: "name"
          type: "string"
          required: true
          validation: "min(2), max(100)"
        
        - name: "email"
          type: "string"
          required: true
          validation: "email format"
        
        - name: "subject"
          type: "string"
          required: true
          validation: "min(5), max(200)"
        
        - name: "message"
          type: "string"
          required: true
          validation: "min(10), max(2000)"
      
      submission:
        endpoint: "POST /web/support"
        success_redirect: "/status/{ticket_id}"
        error_handling: "Show inline error message"
    
    - name: "LoginForm"
      route: "/login"
      validation: "Zod"
      fields:
        - name: "email"
          type: "string"
          required: true
          validation: "email format"
        
        - name: "password"
          type: "string"
          required: true
          validation: "min(8)"
      
      submission:
        endpoint: "POST /auth/login"
        success_redirect: "/dashboard"
        error_handling: "Show toast notification"
    
    - name: "TicketFilterForm"
      route: "/dashboard/tickets"
      validation: "Zod"
      fields:
        - name: "status"
          type: "string[]"
          required: false
          validation: "enum values"
        
        - name: "priority"
          type: "string[]"
          required: false
          validation: "enum values"
        
        - name: "assignee"
          type: "string"
          required: false
        
        - name: "dateFrom"
          type: "string"
          required: false
          validation: "ISO date"
        
        - name: "dateTo"
          type: "string"
          required: false
          validation: "ISO date"
    
    - name: "AgentResponseForm"
      route: "/dashboard/tickets/{ticketId}"
      validation: "Zod"
      fields:
        - name: "content"
          type: "string"
          required: true
          validation: "min(1), max(2000)"
      
      submission:
        endpoint: "POST /tickets/{ticketId}/messages"
        success_action: "Append message to conversation"
        error_handling: "Show inline error, keep draft"
    
    - name: "EscalationForm"
      route: "/dashboard/tickets/{ticketId}"
      validation: "Zod"
      fields:
        - name: "reason"
          type: "string"
          required: true
          validation: "enum: low_confidence | negative_sentiment | customer_request | complex_issue"
        
        - name: "escalated_to"
          type: "string"
          required: false
          validation: "email format"
        
        - name: "notes"
          type: "string"
          required: false
          validation: "max(500)"
      
      submission:
        endpoint: "POST /escalations"
        success_action: "Update ticket status, show confirmation"
        error_handling: "Show toast notification"
@end

@block UI ui_contracts
priority: high
intent: "Define UI component contracts"
scope: frontend
depends_on: frontend_forms

content:
  components:
    - name: "StatusBadge"
      props:
        status: "Ticket['status']"
        variant: "'default' | 'compact'"
      variants:
        open: "bg-blue-100 text-blue-800"
        in_progress: "bg-yellow-100 text-yellow-800"
        waiting_customer: "bg-orange-100 text-orange-800"
        resolved: "bg-green-100 text-green-800"
        escalated: "bg-red-100 text-red-800"
        closed: "bg-gray-100 text-gray-800"
    
    - name: "PriorityBadge"
      props:
        priority: "Ticket['priority']"
        variant: "'default' | 'compact'"
      variants:
        low: "bg-gray-100 text-gray-600"
        normal: "bg-blue-100 text-blue-600"
        high: "bg-orange-100 text-orange-600"
        urgent: "bg-red-100 text-red-600"
    
    - name: "MessageBubble"
      props:
        message: "Message"
        isOwn: "boolean"
        showAvatar: "boolean"
      layout:
        customer: "align-left, gray background"
        agent: "align-right, blue background"
        system: "centered, muted background"
    
    - name: "TicketCard"
      props:
        ticket: "Ticket"
        customer: "Customer"
        onClick: "() => void"
        showPreview: "boolean"
      content:
        - "Subject or first message preview"
        - "Status and Priority badges"
        - "Customer name"
        - "Created/updated timestamp"
    
    - name: "CustomerAvatar"
      props:
        customer: "Customer"
        size: "'sm' | 'md' | 'lg'"
        showName: "boolean"
      fallback: "Initials from name"
    
    - name: "DataTable"
      props:
        columns: "ColumnDef<T>[]"
        data: "T[]"
        pagination: "boolean"
        sorting: "boolean"
        filters: "boolean"
      features:
        - "Column sorting"
        - "Pagination controls"
        - "Row selection"
        - "Filter toolbar"
    
    - name: "ConfirmDialog"
      props:
        open: "boolean"
        onOpenChange: "(open: boolean) => void"
        title: "string"
        description: "string"
        confirmText: "string"
        cancelText: "string"
        onConfirm: "() => void"
      variants:
        default: "Standard confirm/cancel"
        destructive: "Red confirm button for dangerous actions"
@end

@block ROUTES frontend_routes
priority: critical
intent: "Define route configurations"
scope: frontend
depends_on: ui_contracts

content:
  routes:
    - path: "/"
      name: "WebSupportForm"
      access: "public"
      layout: "public"
      metadata:
        title: "Customer Support"
        description: "Submit a support request"
    
    - path: "/status/{ticketId}"
      name: "TicketStatus"
      access: "public"
      layout: "public"
      metadata:
        title: "Ticket Status"
        description: "Track your support ticket"
    
    - path: "/login"
      name: "LoginPage"
      access: "public"
      layout: "auth"
      redirect_if_auth: "/dashboard"
      metadata:
        title: "Agent Login"
    
    - path: "/dashboard"
      name: "DashboardHome"
      access: "protected"
      layout: "dashboard"
      metadata:
        title: "Dashboard"
    
    - path: "/dashboard/tickets"
      name: "TicketList"
      access: "protected"
      layout: "dashboard"
      metadata:
        title: "Tickets"
    
    - path: "/dashboard/tickets/{ticketId}"
      name: "TicketDetail"
      access: "protected"
      layout: "dashboard"
      metadata:
        title: "Ticket Details"
    
    - path: "/dashboard/escalations"
      name: "EscalationList"
      access: "protected"
      layout: "dashboard"
      metadata:
        title: "Escalations"
    
    - path: "/dashboard/customers"
      name: "CustomerList"
      access: "protected"
      layout: "dashboard"
      metadata:
        title: "Customers"
@end
```

---

## API CLIENT CONFIG

```typescript
// lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

interface ApiConfig {
  baseUrl: string;
  timeout: number;
  retries: number;
}

const config: ApiConfig = {
  baseUrl: API_BASE_URL,
  timeout: 30000,
  retries: 3,
};

// Request interceptor adds auth header
// Response handler manages 401 token refresh
// Error handler shows toast notifications
```

---

## ERROR HANDLING

| Error Type | UI Behavior |
|------------|-------------|
| 400 Validation | Show inline field errors |
| 401 Unauthorized | Redirect to login |
| 403 Forbidden | Show "Access Denied" page |
| 404 Not Found | Show "Not Found" page |
| 429 Rate Limited | Show "Too many requests" toast |
| 500 Server Error | Show "Something went wrong" toast |
| Network Error | Show "Connection error" toast |

---

*End of CONTRACT.md — Customer Success Digital FTE v1.0.0*
