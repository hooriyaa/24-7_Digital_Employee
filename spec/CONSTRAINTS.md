# CONSTRAINTS.md — Reality Anchor

> **Customer Success Digital FTE — Hard Limits**
>
> This document defines **non-negotiable constraints** that override all plans and tasks.
> LLMs must not propose solutions outside these boundaries.

---

```slc
@block CONSTRAINTS cs_fte_constraints
priority: critical
intent: "Define hard technical and operational limits"
scope: global
depends_on: CONTEXT.md

content:
  tech:
    backend:
      language: "Python 3.11+"
      framework: "FastAPI"
      package_manager: "UV"
    
    frontend:
      framework: "Next.js 14+ (App Router)"
      language: "TypeScript 5+"
      styling: "Tailwind CSS + shadcn/ui"
    
    ai_agent:
      primary: "Google Gemini API (via LiteLLM)"
      fallback_1: "OpenRouter (Qwen/DeepSeek models)"
      fallback_2: "OpenAI Agents SDK (optional)"
    
    messaging:
      whatsapp: "UltraMsg API"
      email: "Gmail API with Pub/Sub webhooks"
    
    database:
      type: "PostgreSQL 15+"
      vector_extension: "pgvector"
      orm: "SQLModel"
    
    infrastructure:
      containerization: "Docker"
      orchestration: "Kubernetes (K8s)"
      message_queue: "Apache Kafka"
    
    knowledge:
      source: "Context7 MCP"
      rag_required: true
  
  scale:
    max_concurrent_messages: 100
    target_latency_ms: 3000
    uptime_target: "99.9%"
    max_cost_per_year_usd: 1000
    max_context_window_tokens: 128000
  
  hard_rules:
    - "Context7 MCP must be called before any service implementation"
    - "All API endpoints must be defined in CONTRACT.md before coding"
    - "No code generation before ARCH files are finalized"
    - "PostgreSQL is the only database allowed"
    - "Kafka is mandatory for ticket ingestion"
    - "Multi-provider AI fallback is required (no single provider)"
    - "All conversations must be stored with pgvector embeddings"
    - "Docker containers are mandatory for all services"
    - "Kubernetes manifests required for production deployment"
@end
```

---

## TECH

### Backend

| Component | Technology | Version |
|-----------|------------|---------|
| Language | Python | 3.11+ |
| Framework | FastAPI | Latest |
| Package Manager | UV | Latest |
| ORM | SQLModel | Latest |
| Database | PostgreSQL | 15+ |
| Vector Extension | pgvector | Latest |
| Message Queue | Apache Kafka | Latest |

### Frontend

| Component | Technology | Version |
|-----------|------------|---------|
| Framework | Next.js | 14+ (App Router) |
| Language | TypeScript | 5+ |
| Styling | Tailwind CSS + shadcn/ui | Latest |

### AI Agent

| Priority | Provider | SDK |
|----------|----------|-----|
| Primary | OpenAI | Agents SDK |
| Fallback 1 | Google Gemini | Gemini API |
| Fallback 2 | Qwen | OpenRouter |

### Messaging

| Channel | Technology | Integration |
|---------|------------|-------------|
| WhatsApp | UltraMsg | Real-time API |
| Email | Gmail | API + Pub/Sub webhooks |
| Web | Next.js | Direct API submission |

### Infrastructure

| Component | Technology |
|-----------|------------|
| Containerization | Docker |
| Orchestration | Kubernetes (K8s) |
| Knowledge Source | Context7 MCP |

---

## SCALE

| Metric | Target |
|--------|--------|
| Max concurrent messages | 100 |
| Target latency | <3000ms |
| Uptime target | 99.9% |
| Max operating cost | <$1,000/year per FTE |
| Max context window | 128,000 tokens |

---

## HARD RULES

The following rules are **non-negotiable**:

1. **Context7 MCP Integration** — Must be called before implementing any service, framework, or library integration
2. **Contract-First Development** — All API endpoints must be defined in CONTRACT.md before any code is written
3. **Architecture Before Code** — No code generation before ARCH files are finalized and approved
4. **PostgreSQL Only** — No other database technology is permitted
5. **Kafka Mandatory** — Apache Kafka is required for all ticket ingestion and event streaming
6. **Multi-Provider AI** — Single AI provider is forbidden; fallback chain (OpenAI → Gemini → Qwen) is mandatory
7. **Vector Memory Required** — All conversations must be stored with pgvector embeddings for RAG
8. **Docker Containers** — All services must be containerized
9. **Kubernetes for Production** — K8s manifests are required for production deployment
10. **RAG via Context7** — All AI responses must use Context7 as the primary knowledge source

---

## FORBIDDEN TECHNOLOGIES

The following are **explicitly forbidden**:

- MySQL, MongoDB, Redis (PostgreSQL only)
- RabbitMQ, NATS (Kafka only)
- Flask, Django (FastAPI only)
- Express.js, NestJS (Next.js API routes only for frontend)
- Single-provider AI implementations
- Non-containerized production deployments

---

*End of CONSTRAINTS.md — Customer Success Digital FTE v1.0.0*
