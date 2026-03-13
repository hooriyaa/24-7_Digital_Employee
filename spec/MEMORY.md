# MEMORY.md — Anti-Hallucination Anchor

> **Customer Success Digital FTE — Frozen Decisions**
>
> This document defines **frozen facts and decisions** that prevent drift, contradictions, and hallucinated changes.
> If a conflict arises, MEMORY.md always wins.

---

```slc
@block MEMORY cs_fte_memory
priority: critical
intent: "Anchor frozen decisions and assumptions"
scope: global
depends_on: [CONTEXT.md, CONSTRAINTS.md, SECURITY.md]

content:
  decisions:
    - "PostgreSQL is the single source of truth for all data"
    - "Context7 MCP is the primary knowledge source for AI responses"
    - "Multi-channel identity resolution uses email as the primary key"
    - "AI provider fallback order: Gemini (primary) → OpenRouter (Qwen/DeepSeek) → OpenAI (optional)"
    - "Kafka topics: tickets.create, tickets.update, messages.send"
    - "Human escalation triggered when confidence < 0.7 or sentiment = negative"
    - "Web form requires no authentication for submission"
    - "Conversation history retained for 2 years"
    - "D1: Centralized configuration management using Pydantic Settings v2 with validation on startup"
    - "D3: Containerization with Docker Compose - PostgreSQL 16+pgvector for local dev, Confluent Kafka KRaft mode, multi-stage Dockerfile with uv"
    - "D4: SQLModel schema design with UUID primary keys, async relationships, and pgvector Vector(1536) columns"
    - "D5: Alembic migrations with sync engine for schema changes, async URL conversion, pgvector extension auto-creation"
    - "D6: JWT authentication with bcrypt password hashing, HS256 algorithm, access/refresh token rotation"
    - "D7: Generic CRUD pattern with async sessions, singleton instances, entity-specific extensions"
    - "D8: FTEAgent architecture with OpenAI Agents SDK, function tools as skills, pgvector knowledge retrieval"
    - "D9: Context7 MCP integration via HostedMCPTool for external documentation search with caching"
    - "D10: Cost-effective provider strategy - Gemini primary (via LiteLLM), OpenRouter fallback, automatic token tracking and failover"
    - "D11: Rule-based sentiment analysis with keyword matching, escalation triggers for anger/frustration, score range -1.0 to 1.0"
    - "D12: Escalation rules - auto-escalate on low confidence (<0.7), negative sentiment (<-0.5), customer request, pricing/billing keywords"
    - "D13: Tool selection logic - automatic routing between RAG, CRM, Docs based on query intent analysis"
    - "D14: Channel integration - UltraMsg for WhatsApp, Gmail API for email, webhook-based ingestion"
    - "D15: Webhook strategy - background task processing for channel messages, auto-ticket creation from WhatsApp/Gmail"
    - "D16: API Routing Architecture - RESTful endpoints at /api/v1/{resource}, CORS enabled for localhost:3000, async session dependencies"
    - "D17: Automation & Workflows - Auto-responder for positive sentiment queries (score > 0.3) with KB confidence > 0.8, SLA monitoring with WhatsApp alerts for High priority tickets (5 min threshold), Urgent tickets (2 min threshold)"
    - "D18: Circular Dependency Resolution - Use TYPE_CHECKING for type hints, lazy imports inside methods for runtime dependencies, avoid top-level imports between app.agent and app.services.automation"
    - "D19: Ticket Context Management - Chat auto-connects to latest ticket on page load, ticket selection broadcasts via localStorage, zero-UUID placeholder validation in backend, auto-reconnect on 404"
    - "D20: Model Provider Prefixing - Gemini models use bare model name (gemini-2.0-flash) without prefix, OpenRouter models use openrouter/ prefix, LiteLLM auto-detects provider from API key"
    - "D21: Forced Provider Prefixing - Explicit gemini/ prefix required in LiteLLM model string to prevent OpenAI default fallback, GEMINI_API_KEY exported to environment for provider authentication"
    - "D22: Environment Robustness - Non-critical API keys (Gmail, UltraMsg) are Optional to prevent startup failures, .env path resolved via Path(__file__).parent.parent for reliable loading"
    - "D23: Library Version Standard - OpenAI Agents SDK uses openai_agents import (not agents), all agent imports must use from openai_agents import Agent, Runner, function_tool, HostedMCPTool, RunContextWrapper"
    - "D24: Environment Recovery - Broken venv recovery via reset_backend.ps1 script: force-delete .venv, recreate with python -m venv, ensurepip upgrade, install all dependencies including openai-agents>=0.10.0"
    - "D25: Manual Dependency Recovery - Direct pip repair: python -m pip install --upgrade pip, pip install openai-agents==0.10.2, add PYTHONPATH for local module resolution"
    - "F1: Frontend stack - Next.js 15 App Router, TypeScript, Tailwind CSS, health status monitoring"
    - "F2: UI Framework - shadcn/ui components, Slate-Grey professional theme, sidebar navigation, real-time chat interface"
    - "F3: Data Fetching Strategy - Axios client with interceptors, live data from Neon DB, refresh buttons for all tables"
  
  assumptions:
    - "Users have valid Gmail API credentials"
    - "Users have valid UltraMsg API subscription"
    - "OpenAI API key with sufficient quota available"
    - "Kubernetes cluster available for deployment"
    - "Domain with HTTPS certificate available"
    - "Neon Database connection verified and migrations applied successfully (2026-02-24)"
    - "Health endpoint (/api/v1/health) implemented with database connectivity test"
  
  do_not_change:
    - "Tech stack defined in CONSTRAINTS.md"
    - "Security rules defined in SECURITY.md"
    - "Goals and non-goals in CONTEXT.md"
    - "API contract in backend_specs/CONTRACT.md"
    - "Data model in backend_specs/ARCH.md"
@end
```

---

## DECISIONS

The following decisions are **final** and cannot be changed without explicit user approval:

| Decision | Rationale |
|----------|-----------|
| **PostgreSQL single source of truth** | Unified CRM with pgvector for RAG memory |
| **Context7 MCP primary knowledge** | Prevents AI hallucinations with real-time docs |
| **Email as identity primary key** | Common identifier across Gmail, WhatsApp, Web |
| **AI fallback: OpenAI → Gemini → Qwen** | Ensures continuity when quota exceeded |
| **Kafka topics** | `tickets.create`, `tickets.update`, `messages.send` |
| **Escalation threshold** | Confidence < 0.7 OR sentiment = negative |
| **Web form no auth** | Low-friction customer support access |
| **2-year retention** | Balance between memory and storage costs |
| **D1: Centralized Config Management** | Pydantic Settings v2 with startup validation - all mandatory keys enforced |
| **D3: Containerization Strategy** | Docker Compose: PostgreSQL 16+pgvector (local), Confluent Kafka KRaft, multi-stage Dockerfile with uv |
| **D4: Schema Design** | SQLModel with UUID primary keys, async relationships, pgvector Vector(1536) for embeddings |
| **D5: Migration Strategy** | Alembic with sync engine, async URL conversion, pgvector extension auto-creation on migrate |
| **D16: API Routing Architecture** | RESTful endpoints at /api/v1/{resource}, CORS enabled for localhost:3000, async session dependencies |
| **D17: Automation & Workflows** | Auto-responder for positive sentiment (score > 0.3) + KB confidence > 0.8; SLA monitoring with WhatsApp alerts: Urgent (2 min), High (5 min), Normal (30 min), Low (60 min) |
| **D18: Circular Dependency Resolution** | Use TYPE_CHECKING for type hints, lazy imports inside methods for runtime dependencies, avoid top-level imports between app.agent and app.services.automation |
| **D19: Ticket Context Management** | Chat auto-connects to latest ticket on page load, ticket selection broadcasts via localStorage, zero-UUID placeholder validation in backend, auto-reconnect on 404 |
| **D20: Model Provider Prefixing** | Gemini: bare model name (gemini-2.0-flash), OpenRouter: openrouter/{model}, LiteLLM auto-detects provider from API key |
| **D21: Forced Provider Prefixing** | Explicit gemini/ prefix required in LiteLLM model string to prevent OpenAI default fallback, GEMINI_API_KEY exported to environment for provider authentication |
| **D22: Environment Robustness** | Non-critical API keys (Gmail, UltraMsg) are Optional; .env path resolved via Path(__file__).parent.parent for reliable loading from any working directory |
| **D23: Library Version Standard** | OpenAI Agents SDK: use openai_agents import (not agents), pin openai-agents>=0.10.0 in pyproject.toml |
| **D24: Environment Recovery** | Broken venv recovery: reset_backend.ps1 script force-deletes .venv, recreates with python -m venv, runs ensurepip --upgrade, installs all dependencies |
| **D25: Manual Dependency Recovery** | Direct pip repair: python -m pip install --upgrade pip, pip install openai-agents==0.10.2, set PYTHONPATH for local module resolution |

---

## ASSUMPTIONS

The system assumes the following **external prerequisites**:

| Assumption | Verification Required |
|------------|----------------------|
| Valid Gmail API credentials | OAuth 2.0 setup in Google Cloud Console |
| Valid UltraMsg API subscription | Active UltraMsg account with phone number |
| OpenAI API key with quota | Billing-enabled OpenAI account |
| Kubernetes cluster available | GKE, EKS, AKS, or self-managed |
| Domain with HTTPS | TLS certificate (Let's Encrypt or commercial) |

---

## DO NOT CHANGE

The following are **immutable** unless user explicitly requests changes:

| Immutable Item | Defined In |
|----------------|------------|
| Tech stack | CONSTRAINTS.md |
| Security rules | SECURITY.md |
| Goals and non-goals | CONTEXT.md |
| API contract | backend_specs/CONTRACT.md |
| Data model | backend_specs/ARCH.md |
| Task execution order | backend_specs/tasks/task_index.md |

---

## CHANGE LOG

| Date | Change | Authorized By |
|------|--------|---------------|
| 2026-02-24 | Initial creation | User |

---

## CONFLICT RESOLUTION

If any file conflicts with MEMORY.md:

1. **MEMORY.md wins** — frozen decisions override all other files
2. **Report the conflict** — LLM must notify user of the contradiction
3. **Require explicit override** — User must approve any change to frozen decisions

---

*End of MEMORY.md — Customer Success Digital FTE v1.0.0*
