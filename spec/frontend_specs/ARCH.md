# ARCH.md — Frontend Architecture

> **Customer Success Digital FTE — Frontend System Design**
>
> This document defines the **state shape, UI flow, and rendering logic** for the frontend.
> No API invention allowed — all derived from backend CONTRACT.md.

---

```slc
@block INDEX frontend_arch_index
priority: critical
intent: "Frontend architecture router"
scope: frontend
failure_if_skipped: true

read_order:
  - frontend_specs/ARCH.md
  - frontend_specs/PLAN.md
  - frontend_specs/CONTRACT.md

content:
  short: "Frontend architecture for Customer Success Digital FTE"
@end

@block ARCH frontend_system
priority: critical
intent: "Define frontend system architecture"
scope: frontend
depends_on: [CONTEXT.md, CONSTRAINTS.md, SECURITY.md, backend_specs/CONTRACT.md]

content:
  system_name: "Customer Success Digital FTE Frontend"
  version: "1.0.0"
  
  tech_stack:
    framework: "Next.js 14+ (App Router)"
    language: "TypeScript 5+"
    styling: "Tailwind CSS + shadcn/ui"
    state_management: "React Query + Zustand"
    forms: "React Hook Form + Zod"
  
  applications:
    - name: "Web Support Form"
      type: "Public Page"
      route: "/"
      description: "Customer-facing support submission form"
    
    - name: "Ticket Status Tracker"
      type: "Public Page"
      route: "/status/[ticketId]"
      description: "Track ticket status without authentication"
    
    - name: "Agent Dashboard"
      type: "Protected App"
      route: "/dashboard/*"
      description: "Human agent interface for managing tickets"
@end

@block STATE frontend_state
priority: critical
intent: "Define frontend state management"
scope: frontend
depends_on: frontend_system

content:
  client_state:
    store: "Zustand"
    slices:
      - name: "authSlice"
        state:
          user: "User | null"
          token: "string | null"
          isAuthenticated: "boolean"
          isLoading: "boolean"
        actions:
          - "login(credentials)"
          - "logout()"
          - "refreshToken()"
      
      - name: "ticketSlice"
        state:
          tickets: "Ticket[]"
          currentTicket: "Ticket | null"
          filters: "TicketFilters"
          pagination: "PaginationState"
        actions:
          - "fetchTickets(filters)"
          - "fetchTicket(id)"
          - "updateTicket(id, updates)"
          - "closeTicket(id)"
      
      - name: "conversationSlice"
        state:
          messages: "Message[]"
          isLoading: "boolean"
          isSending: "boolean"
        actions:
          - "fetchMessages(ticketId)"
          - "sendMessage(ticketId, content)"
          - "clearConversation()"
  
  server_state:
    library: "TanStack Query (React Query)"
    queries:
      - name: "useTickets"
        endpoint: "GET /tickets"
        stale_time: "30000"
      
      - name: "useTicket"
        endpoint: "GET /tickets/{id}"
        stale_time: "10000"
      
      - name: "useMessages"
        endpoint: "GET /tickets/{id}/messages"
        stale_time: "5000"
      
      - name: "useCustomers"
        endpoint: "GET /customers"
        stale_time: "60000"
      
      - name: "useEscalations"
        endpoint: "GET /escalations"
        stale_time: "10000"
    
    mutations:
      - name: "useCreateTicket"
        endpoint: "POST /tickets"
        invalidates: ["tickets"]
      
      - name: "useUpdateTicket"
        endpoint: "PUT /tickets/{id}"
        invalidates: ["ticket", "tickets"]
      
      - name: "useSendMessage"
        endpoint: "POST /tickets/{id}/messages"
        invalidates: ["messages"]
      
      - name: "useCreateEscalation"
        endpoint: "POST /escalations"
        invalidates: ["escalations"]
@end

@block FLOW ui_flow
priority: high
intent: "Define UI navigation flow"
scope: frontend
depends_on: frontend_state

content:
  public_routes:
    - path: "/"
      page: "WebSupportForm"
      description: "Submit support request"
    
    - path: "/status/[ticketId]"
      page: "TicketStatus"
      description: "View ticket status"
  
  protected_routes:
    - path: "/dashboard"
      page: "DashboardHome"
      description: "Ticket overview and stats"
    
    - path: "/dashboard/tickets"
      page: "TicketList"
      description: "Browse all tickets"
    
    - path: "/dashboard/tickets/[ticketId]"
      page: "TicketDetail"
      description: "View and respond to ticket"
    
    - path: "/dashboard/escalations"
      page: "EscalationList"
      description: "View escalated tickets"
    
    - path: "/dashboard/customers"
      page: "CustomerList"
      description: "Browse customers"
  
  auth_routes:
    - path: "/login"
      page: "LoginPage"
      description: "Agent login"
@end

@block COMPONENTS ui_components
priority: medium
intent: "Define major UI components"
scope: frontend
depends_on: ui_flow

content:
  shared_components:
    - name: "Header"
      description: "Navigation header with logo and user menu"
    
    - name: "Sidebar"
      description: "Dashboard navigation sidebar"
    
    - name: "TicketCard"
      description: "Compact ticket preview card"
    
    - name: "StatusBadge"
      description: "Status indicator badge"
    
    - name: "PriorityBadge"
      description: "Priority level indicator"
    
    - name: "MessageBubble"
      description: "Chat message display component"
    
    - name: "MessageInput"
      description: "Message composition input"
    
    - name: "CustomerAvatar"
      description: "Customer avatar with initials"
  
  page_components:
    - name: "WebSupportForm"
      description: "Public support submission form"
      fields: ["name", "email", "subject", "message"]
    
    - name: "TicketStatus"
      description: "Public ticket status display"
    
    - name: "TicketList"
      description: "Ticket table with filters and pagination"
    
    - name: "TicketDetail"
      description: "Full ticket view with conversation thread"
    
    - name: "DashboardHome"
      description: "Dashboard with stats and recent activity"
@end

@block INTEGRATION api_integration
priority: critical
intent: "Define API integration patterns"
scope: frontend
depends_on: backend_specs/CONTRACT.md

content:
  base_url: "process.env.NEXT_PUBLIC_API_URL"
  auth_strategy: "httpOnly cookies"
  
  api_client:
    library: "fetch with custom wrapper"
    features:
      - "Automatic token refresh on 401"
      - "Request interceptors for auth headers"
      - "Response error handling"
      - "Retry logic for failed requests"
  
  endpoints:
    public:
      - "POST /web/support"
      - "GET /web/status/{ticketId}"
      - "POST /auth/login"
      - "POST /auth/refresh"
    
    protected:
      - "GET /tickets"
      - "POST /tickets"
      - "GET /tickets/{id}"
      - "PUT /tickets/{id}"
      - "POST /tickets/{id}/close"
      - "GET /tickets/{id}/messages"
      - "POST /tickets/{id}/messages"
      - "GET /customers"
      - "POST /customers"
      - "GET /customers/{id}"
      - "GET /escalations"
      - "POST /escalations"
      - "POST /escalations/{id}/resolve"
      - "POST /agent/respond"
      - "GET /agent/providers"
@end
```

---

## APPLICATION STRUCTURE

```
frontend/
├── app/
│   ├── (public)/
│   │   ├── page.tsx              # Web Support Form
│   │   └── status/
│   │       └── [ticketId]/
│   │           └── page.tsx      # Ticket Status
│   ├── (auth)/
│   │   └── login/
│   │       └── page.tsx          # Login Page
│   ├── (dashboard)/
│   │   ├── layout.tsx            # Dashboard layout with sidebar
│   │   ├── page.tsx              # Dashboard home
│   │   ├── tickets/
│   │   │   ├── page.tsx          # Ticket list
│   │   │   └── [ticketId]/
│   │   │       └── page.tsx      # Ticket detail
│   │   ├── escalations/
│   │   │   └── page.tsx          # Escalation list
│   │   └── customers/
│   │       └── page.tsx          # Customer list
│   ├── api/                      # API route proxies (optional)
│   ├── layout.tsx                # Root layout
│   └── globals.css
├── components/
│   ├── ui/                       # shadcn/ui components
│   ├── shared/                   # Shared components
│   └── features/                 # Feature-specific components
├── lib/
│   ├── api.ts                    # API client
│   ├── utils.ts                  # Utilities
│   └── validations.ts            # Zod schemas
├── hooks/                        # Custom React hooks
├── stores/                       # Zustand stores
├── queries/                      # React Query hooks
└── types/                        # TypeScript types
```

---

*End of ARCH.md — Customer Success Digital FTE v1.0.0*
