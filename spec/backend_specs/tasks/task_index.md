# task_index.md — Backend Task Registry

> **Customer Success Digital FTE — Global Backend Task Registry**
>
> This file is the **single source of truth** for all backend tasks.
> LLM must read this file once, then load individual task files as needed.

---

```slc
@block INDEX task_registry
priority: critical
intent: "Global backend task registry - all tasks visible"
scope: backend
failure_if_skipped: true

content:
  total_tasks: 44
  total_estimate_minutes: 480
  total_estimate_hours: 8
  
  phases:
    - phase: 1
      name: "Foundation & CRM"
      dir: "phases/phase-1/"
      tasks: 11
      estimate_minutes: 120
    
    - phase: 2
      name: "Agent Brain & Multi-Provider"
      dir: "phases/phase-2/"
      tasks: 13
      estimate_minutes: 150
    
    - phase: 3
      name: "Channel Integration"
      dir: "phases/phase-3/"
      tasks: 14
      estimate_minutes: 150
    
    - phase: 4
      name: "Production & Resilience"
      dir: "phases/phase-4/"
      tasks: 6
      estimate_minutes: 60
  
  all_tasks:
    # Phase 1
    - id: "1.1"
      file: "phases/phase-1/1.1_init_project.md"
      title: "Initialize FastAPI project with UV"
      status: done
      estimate_minutes: 10

    - id: "1.2"
      file: "phases/phase-1/1.2_project_structure.md"
      title: "Create project directory structure"
      status: done
      estimate_minutes: 10

    - id: "1.3"
      file: "phases/phase-1/1.3_env_config.md"
      title: "Setup environment configuration"
      status: done
      estimate_minutes: 10
    
    - id: "1.4"
      file: "phases/phase-1/1.4_docker_postgres.md"
      title: "Create Docker config for PostgreSQL"
      status: done
      estimate_minutes: 15

    - id: "1.5"
      file: "phases/phase-1/1.5_docker_kafka.md"
      title: "Create Docker config for Kafka"
      status: done
      estimate_minutes: 15
    
    - id: "1.6"
      file: "phases/phase-1/1.6_database_schema.md"
      title: "Define database schema with SQLModel"
      status: done
      estimate_minutes: 15
    
    - id: "1.7"
      file: "phases/phase-1/1.7_alembic_setup.md"
      title: "Setup Alembic migrations"
      status: done
      estimate_minutes: 10
    
    - id: "1.8"
      file: "phases/phase-1/1.8_run_migrations.md"
      title: "Run initial database migrations"
      status: done
      estimate_minutes: 10
    
    - id: "1.9"
      file: "phases/phase-1/1.9_health_endpoint.md"
      title: "Create health check endpoint"
      status: done
      estimate_minutes: 10
    
    - id: "1.10"
      file: "phases/phase-1/1.10_jwt_auth.md"
      title: "Implement JWT authentication"
      status: done
      estimate_minutes: 15
    
    - id: "1.11"
      file: "phases/phase-1/1.11_base_crud.md"
      title: "Create base CRUD utilities"
      status: done
      estimate_minutes: 10
    
    # Phase 2
    - id: "2.1"
      file: "phases/phase-2/2.1_openai_agents.md"
      title: "Integrate OpenAI Agents SDK"
      status: done
      estimate_minutes: 15
    
    - id: "2.2"
      file: "phases/phase-2/2.2_context7_mcp.md"
      title: "Integrate Context7 MCP for RAG"
      status: done
      estimate_minutes: 15
    
    - id: "2.3"
      file: "phases/phase-2/2.3_provider_fallback.md"
      title: "Implement multi-provider fallback"
      status: done
      estimate_minutes: 15
    
    - id: "2.4"
      file: "phases/phase-2/2.4_sentiment_analysis.md"
      title: "Implement sentiment analysis"
      status: done
      estimate_minutes: 10
    
    - id: "2.5"
      file: "phases/phase-2/2.5_escalation_rules.md"
      title: "Configure escalation rules"
      status: done
      estimate_minutes: 10

    - id: "2.6"
      file: "phases/phase-2/2.6_agent_respond_endpoint.md"
      title: "Create /agent/respond endpoint"
      status: done
      estimate_minutes: 15
    
    - id: "2.7"
      file: "phases/phase-2/2.7_provider_status.md"
      title: "Create /agent/providers endpoint"
      status: done
      estimate_minutes: 10

    - id: "2.8"
      file: "phases/phase-2/2.8_vector_embeddings.md"
      title: "Implement agent memory (conversation history)"
      status: done
      estimate_minutes: 15

    - id: "2.9"
      file: "phases/phase-2/2.9_memory_retrieval.md"
      title: "Implement tool selector logic"
      status: done
      estimate_minutes: 15
    
    - id: "2.10"
      file: "phases/phase-2/2.10_token_tracking.md"
      title: "Implement token usage tracking"
      status: todo
      estimate_minutes: 10
    
    - id: "2.11"
      file: "phases/phase-2/2.11_confidence_scoring.md"
      title: "Implement confidence scoring"
      status: todo
      estimate_minutes: 10
    
    - id: "2.12"
      file: "phases/phase-2/2.12_response_caching.md"
      title: "Implement response caching"
      status: todo
      estimate_minutes: 10
    
    - id: "2.13"
      file: "phases/phase-2/2.13_agent_testing.md"
      title: "Test AI agent responses"
      status: todo
      estimate_minutes: 10
    
    # Phase 3
    - id: "3.1"
      file: "phases/phase-3/3.1_kafka_producer.md"
      title: "Implement UltraMsg WhatsApp service"
      status: done
      estimate_minutes: 15

    - id: "3.2"
      file: "phases/phase-3/3.2_kafka_consumer.md"
      title: "Implement Gmail email service"
      status: done
      estimate_minutes: 15

    - id: "3.3"
      file: "phases/phase-3/3.3_gmail_api.md"
      title: "Implement WhatsApp notifications"
      status: done
      estimate_minutes: 15

    - id: "3.4"
      file: "phases/phase-3/3.4_gmail_webhook.md"
      title: "Implement webhook handlers"
      status: done
      estimate_minutes: 10
    
    - id: "3.5"
      file: "phases/phase-3/3.5_ultramsg_api.md"
      title: "Integrate UltraMsg API"
      status: done
      estimate_minutes: 15

    - id: "3.6"
      file: "phases/phase-3/3.6_ultramsg_webhook.md"
      title: "Implement UltraMsg webhook handler"
      status: done
      estimate_minutes: 10
    
    - id: "3.7"
      file: "phases/phase-3/3.7_identity_resolution.md"
      title: "Implement cross-channel identity resolution"
      status: todo
      estimate_minutes: 15
    
    - id: "3.8"
      file: "phases/phase-3/3.8_ticket_crud.md"
      title: "Implement ticket CRUD endpoints"
      status: todo
      estimate_minutes: 15
    
    - id: "3.9"
      file: "phases/phase-3/3.9_message_crud.md"
      title: "Implement message CRUD endpoints"
      status: todo
      estimate_minutes: 10
    
    - id: "3.10"
      file: "phases/phase-3/3.10_customer_crud.md"
      title: "Implement customer CRUD endpoints"
      status: todo
      estimate_minutes: 10
    
    - id: "3.11"
      file: "phases/phase-3/3.11_web_support_form.md"
      title: "Create web support form endpoint"
      status: todo
      estimate_minutes: 10
    
    - id: "3.12"
      file: "phases/phase-3/3.12_status_tracking.md"
      title: "Create ticket status tracking endpoint"
      status: todo
      estimate_minutes: 10
    
    - id: "3.13"
      file: "phases/phase-3/3.13_escalation_crud.md"
      title: "Implement escalation CRUD endpoints"
      status: todo
      estimate_minutes: 10
    
    - id: "3.14"
      file: "phases/phase-3/3.14_channel_integration_test.md"
      title: "Test channel integration end-to-end"
      status: todo
      estimate_minutes: 10
    
    # Phase 4
    - id: "4.1"
      file: "phases/phase-4/4.1_k8s_deployment.md"
      title: "Create Kubernetes deployment manifests"
      status: todo
      estimate_minutes: 15
    
    - id: "4.2"
      file: "phases/phase-4/4.2_k8s_services.md"
      title: "Create Kubernetes service definitions"
      status: todo
      estimate_minutes: 10
    
    - id: "4.3"
      file: "phases/phase-4/4.3_k8s_secrets.md"
      title: "Configure Kubernetes secrets"
      status: todo
      estimate_minutes: 10
    
    - id: "4.4"
      file: "phases/phase-4/4.4_load_testing.md"
      title: "Run load testing with Locust"
      status: todo
      estimate_minutes: 10
    
    - id: "4.5"
      file: "phases/phase-4/4.5_chaos_testing.md"
      title: "Run chaos testing"
      status: todo
      estimate_minutes: 10
    
    - id: "4.6"
      file: "phases/phase-4/4.6_uptime_verification.md"
      title: "Verify 99.9% uptime target"
      status: todo
      estimate_minutes: 5
@end
```

---

## EXECUTION RULES

1. **Read this file once** at the start of each session
2. **Load individual task files** only when executing that task
3. **Update status** to `done` immediately after task completion
4. **Do not skip tasks** — follow the order within each phase
5. **Phase gates** — Complete all tasks in phase N before starting phase N+1

---

## CURRENT EXECUTION STATE

| Metric | Value |
|--------|-------|
| Total Tasks | 44 |
| Completed | 27 |
| In Progress | 0 |
| Pending | 17 |
| Current Phase | 3 |

### Completed Tasks

**Phase 1: Foundation & CRM (11 tasks)**
- [x] 1.1 - Initialize FastAPI project with UV
- [x] 1.2 - Create project directory structure
- [x] 1.3 - Setup environment configuration
- [x] 1.4 - Create Docker config for PostgreSQL
- [x] 1.5 - Create Docker config for Kafka
- [x] 1.6 - Define database schema with SQLModel
- [x] 1.7 - Setup Alembic migrations
- [x] 1.8 - Run initial database migrations
- [x] 1.9 - Create health check endpoint
- [x] 1.10 - Implement JWT authentication
- [x] 1.11 - Create base CRUD utilities

**Phase 2: Agent Brain & Multi-Provider (9/13 tasks)**
- [x] 2.1 - Integrate OpenAI Agents SDK
- [x] 2.2 - Integrate Context7 MCP for RAG
- [x] 2.3 - Implement multi-provider fallback
- [x] 2.4 - Implement sentiment analysis
- [x] 2.5 - Configure escalation rules
- [x] 2.6 - Create /agent/respond endpoint
- [x] 2.7 - Create /agent/providers endpoint ✅
- [x] 2.8 - Implement agent memory ✅
- [x] 2.9 - Implement tool selector logic ✅

**Phase 3: Channel Integration (6/14 tasks)**
- [x] 3.1 - Implement UltraMsg WhatsApp service ✅
- [x] 3.2 - Implement Gmail email service ✅
- [x] 3.3 - Implement WhatsApp notifications ✅ NEW
- [x] 3.4 - Implement webhook handlers ✅ NEW
- [x] 3.5 - Integrate UltraMsg API ✅
- [x] 3.6 - Implement UltraMsg webhook handler ✅

### Next Task
- [ ] 2.10 - Implement token usage tracking

---

*End of task_index.md — Backend Task Registry*
