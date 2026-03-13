# PLAN.md — Frontend Execution Plan

> **Customer Success Digital FTE — Frontend Phases**
>
> This document defines **high-level execution phases and milestones** for the frontend.
> Derived from backend CONTRACT.md — no API invention.

---

```slc
@block INDEX frontend_plan_index
priority: critical
intent: "Frontend plan router"
scope: frontend
failure_if_skipped: true

read_order:
  - frontend_specs/ARCH.md
  - frontend_specs/PLAN.md
  - frontend_specs/CONTRACT.md
  - frontend_specs/tasks/task_index.md

content:
  short: "Frontend execution plan with 3 phases"
@end

@block PLAN frontend_plan
priority: critical
intent: "Define frontend execution phases"
scope: frontend
depends_on: frontend_specs/ARCH.md

content:
  total_phases: 3
  total_estimate_minutes: 240
  total_estimate_hours: 4
  
  phases:
    - phase: 1
      name: "Foundation & Public Pages"
      estimate_minutes: 90
      estimate_hours: 1.5
      description: "Next.js setup, Web Support Form, Status Tracker"
      milestones:
        - "Next.js 14 project initialized"
        - "Tailwind CSS + shadcn/ui configured"
        - "Web Support Form page complete"
        - "Ticket Status page complete"
        - "API client configured"
    
    - phase: 2
      name: "Dashboard & Ticket Management"
      estimate_minutes: 100
      estimate_hours: 1.67
      description: "Authentication, Dashboard, Ticket CRUD UI"
      milestones:
        - "Authentication flow implemented"
        - "Dashboard layout with sidebar"
        - "Ticket list with filters"
        - "Ticket detail with conversation"
        - "Agent response UI working"
    
    - phase: 3
      name: "Escalations & Polish"
      estimate_minutes: 50
      estimate_hours: 0.83
      description: "Escalation management, testing, deployment"
      milestones:
        - "Escalation list and management"
        - "Customer list page"
        - "Responsive design verified"
        - "E2E tests passing"
        - "Production build deployed"
@end
```

---

## PHASE 1: Foundation & Public Pages

**Duration:** 1.5 hours (90 minutes)

### Objectives
- Initialize Next.js 14 project with App Router
- Configure Tailwind CSS and shadcn/ui component library
- Build public Web Support Form page
- Build public Ticket Status Tracker page
- Set up API client and React Query

### Milestones
| # | Milestone | Verification |
|---|-----------|--------------|
| 1 | Next.js 14 project initialized | `npm run dev` starts successfully |
| 2 | Tailwind + shadcn/ui configured | Components render with correct styles |
| 3 | Web Support Form complete | Form submits to backend API |
| 4 | Ticket Status page complete | Status fetched and displayed |
| 5 | API client configured | API calls succeed with proper auth |

---

## PHASE 2: Dashboard & Ticket Management

**Duration:** 1.67 hours (100 minutes)

### Objectives
- Implement authentication flow (login, token management)
- Create dashboard layout with navigation sidebar
- Build ticket list page with filters and pagination
- Build ticket detail page with conversation thread
- Implement agent response UI

### Milestones
| # | Milestone | Verification |
|---|-----------|--------------|
| 1 | Authentication flow implemented | Login/logout working, tokens managed |
| 2 | Dashboard layout complete | Sidebar navigation functional |
| 3 | Ticket list page complete | Tickets displayed with filters |
| 4 | Ticket detail page complete | Conversation thread visible |
| 5 | Agent response UI working | Agents can send responses |

---

## PHASE 3: Escalations & Polish

**Duration:** 0.83 hours (50 minutes)

### Objectives
- Build escalation list and management UI
- Build customer list page
- Ensure responsive design across devices
- Write and run E2E tests
- Deploy production build

### Milestones
| # | Milestone | Verification |
|---|-----------|--------------|
| 1 | Escalation management complete | Escalations listed and resolvable |
| 2 | Customer list page complete | Customers browsable |
| 3 | Responsive design verified | Works on mobile, tablet, desktop |
| 4 | E2E tests passing | Critical flows tested |
| 5 | Production deployment | Frontend accessible via HTTPS |

---

## DEPENDENCY GRAPH

```
Phase 1 (Foundation)
    │
    ├── Next.js setup
    ├── Tailwind + shadcn/ui
    └── Public pages
    │
    ▼
Phase 2 (Dashboard)
    │
    ├── Authentication
    ├── Dashboard layout
    └── Ticket management UI
    │
    ▼
Phase 3 (Polish)
    │
    ├── Escalation UI
    ├── Customer UI
    └── Testing & Deployment
```

---

## BACKEND DEPENDENCIES

Frontend implementation depends on these backend endpoints:

| Frontend Feature | Backend Endpoint |
|-----------------|------------------|
| Web Support Form | POST /web/support |
| Ticket Status | GET /web/status/{id} |
| Login | POST /auth/login |
| Ticket List | GET /tickets |
| Ticket Detail | GET /tickets/{id} |
| Send Message | POST /tickets/{id}/messages |
| Agent Response | POST /agent/respond |
| Escalations | GET/POST /escalations |
| Customers | GET /customers |

---

*End of PLAN.md — Customer Success Digital FTE v1.0.0*
