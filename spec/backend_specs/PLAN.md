# PLAN.md — Backend Execution Plan

> **Customer Success Digital FTE — Backend Phases**
>
> This document defines **high-level execution phases and milestones** for the backend.
> No implementation details. Phase structure only.

---

```slc
@block INDEX backend_plan_index
priority: critical
intent: "Backend plan router"
scope: backend
failure_if_skipped: true

read_order:
  - backend_specs/ARCH.md
  - backend_specs/PLAN.md
  - backend_specs/CONTRACT.md
  - backend_specs/tasks/task_index.md

content:
  short: "Backend execution plan with 4 phases"
@end

@block PLAN backend_plan
priority: critical
intent: "Define backend execution phases"
scope: backend
depends_on: backend_specs/ARCH.md

content:
  total_phases: 4
  total_estimate_minutes: 480
  total_estimate_hours: 8
  
  phases:
    - phase: 1
      name: "Foundation & CRM"
      estimate_minutes: 120
      estimate_hours: 2
      description: "Project setup, database schema, Docker infrastructure"
      milestones:
        - "FastAPI project initialized with UV"
        - "PostgreSQL + pgvector running in Docker"
        - "Kafka running in Docker"
        - "Database schema migrated"
        - "Environment configuration complete"
    
    - phase: 2
      name: "Agent Brain & Multi-Provider"
      estimate_minutes: 150
      estimate_hours: 2.5
      description: "AI Agent implementation with Context7 RAG and provider fallback"
      milestones:
        - "OpenAI Agents SDK integrated"
        - "Context7 MCP integration working"
        - "Multi-provider fallback (OpenAI → Gemini → Qwen)"
        - "Sentiment analysis implemented"
        - "Escalation rules configured"
    
    - phase: 3
      name: "Channel Integration"
      estimate_minutes: 150
      estimate_hours: 2.5
      description: "Gmail, WhatsApp, and Kafka ingestion"
      milestones:
        - "Gmail API webhook integrated"
        - "UltraMsg webhook integrated"
        - "Kafka producer-consumer logic working"
        - "Identity resolution across channels"
        - "Ticket CRUD operations complete"
    
    - phase: 4
      name: "Production & Resilience"
      estimate_minutes: 60
      estimate_hours: 1
      description: "Kubernetes deployment and load testing"
      milestones:
        - "Kubernetes manifests created"
        - "Load testing with 100+ concurrent messages"
        - "Chaos testing (pod failures)"
        - "99.9% uptime verified"
@end
```

---

## PHASE 1: Foundation & CRM

**Duration:** 2 hours (120 minutes)

### Objectives
- Initialize FastAPI project with UV package manager
- Set up PostgreSQL with pgvector extension
- Set up Apache Kafka for event streaming
- Design and migrate database schema
- Configure environment variables

### Milestones
| # | Milestone | Verification |
|---|-----------|--------------|
| 1 | FastAPI project initialized | `backend/main.py` runs with `uv run uvicorn` |
| 2 | PostgreSQL + pgvector running | Docker container healthy, extension enabled |
| 3 | Kafka running | Docker container healthy, topics creatable |
| 4 | Database schema migrated | All tables created with correct structure |
| 5 | Environment configuration | `.env` file with all required variables |

---

## PHASE 2: Agent Brain & Multi-Provider

**Duration:** 2.5 hours (150 minutes)

### Objectives
- Integrate OpenAI Agents SDK as primary AI provider
- Implement Context7 MCP for RAG knowledge retrieval
- Build multi-provider fallback chain (OpenAI → Gemini → Qwen)
- Implement sentiment analysis for customer messages
- Configure escalation rules and thresholds

### Milestones
| # | Milestone | Verification |
|---|-----------|--------------|
| 1 | OpenAI Agents SDK integrated | Agent responds to test prompts |
| 2 | Context7 MCP integration | Documentation fetched for test queries |
| 3 | Multi-provider fallback working | Failover tested for each provider |
| 4 | Sentiment analysis implemented | Sentiment scores returned for test messages |
| 5 | Escalation rules configured | Escalation triggered at threshold |

---

## PHASE 3: Channel Integration

**Duration:** 2.5 hours (150 minutes)

### Objectives
- Integrate Gmail API with Pub/Sub webhooks
- Integrate UltraMsg API for WhatsApp
- Implement Kafka producer-consumer for ticket ingestion
- Build identity resolution across all channels
- Complete ticket CRUD operations

### Milestones
| # | Milestone | Verification |
|---|-----------|--------------|
| 1 | Gmail API webhook integrated | Emails trigger ticket creation |
| 2 | UltraMsg webhook integrated | WhatsApp messages trigger ticket creation |
| 3 | Kafka producer-consumer working | Events published and consumed correctly |
| 4 | Identity resolution working | Same customer identified across channels |
| 5 | Ticket CRUD operations | Create, read, update, delete all functional |

---

## PHASE 4: Production & Resilience

**Duration:** 1 hour (60 minutes)

### Objectives
- Create Kubernetes deployment manifests
- Create Kubernetes service definitions
- Run load testing with Locust (100+ concurrent messages)
- Run chaos testing (pod failures)
- Verify 99.9% uptime target

### Milestones
| # | Milestone | Verification |
|---|-----------|--------------|
| 1 | Kubernetes manifests created | `kubectl apply` succeeds |
| 2 | Load testing complete | 100+ concurrent messages handled |
| 3 | Chaos testing complete | System recovers from pod failures |
| 4 | 99.9% uptime verified | Monitoring shows target met |

---

## DEPENDENCY GRAPH

```
Phase 1 (Foundation)
    │
    ├── Database schema
    ├── Docker infrastructure
    └── Environment config
    │
    ▼
Phase 2 (Agent Brain)
    │
    ├── OpenAI Agents SDK
    ├── Context7 MCP
    └── Sentiment analysis
    │
    ▼
Phase 3 (Channel Integration)
    │
    ├── Gmail API
    ├── UltraMsg API
    └── Kafka ingestion
    │
    ▼
Phase 4 (Production)
    │
    ├── Kubernetes deployment
    ├── Load testing
    └── Chaos testing
```

---

*End of PLAN.md — Customer Success Digital FTE v1.0.0*
