# ARCH.md — Backend Architecture

> **Customer Success Digital FTE — Backend System Design**
>
> This document defines the **data models, control flow, and service boundaries** for the backend.
> No tasks. No code. Architecture only.

---

```slc
@block INDEX backend_arch_index
priority: critical
intent: "Backend architecture router"
scope: backend
failure_if_skipped: true

read_order:
  - backend_specs/ARCH.md
  - backend_specs/PLAN.md
  - backend_specs/CONTRACT.md

content:
  short: "Backend architecture for Customer Success Digital FTE"
@end

@block ARCH backend_system
priority: critical
intent: "Define backend system architecture"
scope: backend
depends_on: [CONTEXT.md, CONSTRAINTS.md, SECURITY.md]

content:
  system_name: "Customer Success Digital FTE Backend"
  version: "1.0.0"
  
  services:
    - name: "API Gateway"
      type: "FastAPI"
      responsibility: "HTTP request routing, authentication, rate limiting"
    
    - name: "Ticket Ingestion Service"
      type: "Kafka Consumer"
      responsibility: "Process incoming tickets from all channels"
    
    - name: "AI Agent Service"
      type: "OpenAI Agents SDK"
      responsibility: "Generate responses with Context7 RAG"
    
    - name: "Channel Connectors"
      type: "Webhook Handlers"
      responsibility: "Gmail API, UltraMsg webhook receivers"
    
    - name: "Memory Service"
      type: "PostgreSQL + pgvector"
      responsibility: "Store and retrieve conversation embeddings"
    
    - name: "Escalation Service"
      type: "Rule Engine"
      responsibility: "Trigger human escalation when needed"
@end

@block DATA_MODEL backend_data_model
priority: critical
intent: "Define all database entities and relationships"
scope: backend
depends_on: backend_system

content:
  entities:
    - name: "Customer"
      description: "Unified customer identity across all channels"
      fields:
        - name: "id"
          type: "UUID"
          constraints: ["PRIMARY KEY", "NOT NULL"]
        - name: "email"
          type: "VARCHAR(255)"
          constraints: ["UNIQUE", "NOT NULL"]
        - name: "phone"
          type: "VARCHAR(20)"
          constraints: ["UNIQUE", "NULL"]
        - name: "name"
          type: "VARCHAR(255)"
          constraints: ["NOT NULL"]
        - name: "created_at"
          type: "TIMESTAMP"
          constraints: ["DEFAULT NOW()"]
        - name: "updated_at"
          type: "TIMESTAMP"
          constraints: ["DEFAULT NOW()"]
    
    - name: "Channel"
      description: "Communication channel types"
      fields:
        - name: "id"
          type: "INTEGER"
          constraints: ["PRIMARY KEY"]
        - name: "name"
          type: "VARCHAR(50)"
          constraints: ["UNIQUE", "NOT NULL"]
          values: ["gmail", "whatsapp", "web"]
    
    - name: "ChannelIdentity"
      description: "Channel-specific customer identifiers"
      fields:
        - name: "id"
          type: "UUID"
          constraints: ["PRIMARY KEY"]
        - name: "customer_id"
          type: "UUID"
          constraints: ["FOREIGN KEY REFERENCES Customer(id)"]
        - name: "channel_id"
          type: "INTEGER"
          constraints: ["FOREIGN KEY REFERENCES Channel(id)"]
        - name: "channel_identifier"
          type: "VARCHAR(255)"
          constraints: ["NOT NULL"]
        - name: "metadata"
          type: "JSONB"
          constraints: ["DEFAULT '{}'"]
    
    - name: "Ticket"
      description: "Customer support ticket"
      fields:
        - name: "id"
          type: "UUID"
          constraints: ["PRIMARY KEY"]
        - name: "customer_id"
          type: "UUID"
          constraints: ["FOREIGN KEY REFERENCES Customer(id)"]
        - name: "status"
          type: "VARCHAR(50)"
          constraints: ["NOT NULL"]
          values: ["open", "in_progress", "waiting_customer", "resolved", "escalated", "closed"]
        - name: "priority"
          type: "VARCHAR(20)"
          constraints: ["DEFAULT 'normal'"]
          values: ["low", "normal", "high", "urgent"]
        - name: "subject"
          type: "VARCHAR(500)"
          constraints: ["NULL"]
        - name: "sentiment_score"
          type: "FLOAT"
          constraints: ["DEFAULT NULL"]
        - name: "confidence_score"
          type: "FLOAT"
          constraints: ["DEFAULT NULL"]
        - name: "assigned_to"
          type: "VARCHAR(255)"
          constraints: ["NULL"]
        - name: "created_at"
          type: "TIMESTAMP"
          constraints: ["DEFAULT NOW()"]
        - name: "resolved_at"
          type: "TIMESTAMP"
          constraints: ["NULL"]
    
    - name: "Conversation"
      description: "Conversation thread within a ticket"
      fields:
        - name: "id"
          type: "UUID"
          constraints: ["PRIMARY KEY"]
        - name: "ticket_id"
          type: "UUID"
          constraints: ["FOREIGN KEY REFERENCES Ticket(id)"]
        - name: "message_count"
          type: "INTEGER"
          constraints: ["DEFAULT 0"]
        - name: "created_at"
          type: "TIMESTAMP"
          constraints: ["DEFAULT NOW()"]
        - name: "updated_at"
          type: "TIMESTAMP"
          constraints: ["DEFAULT NOW()"]
    
    - name: "Message"
      description: "Individual message in a conversation"
      fields:
        - name: "id"
          type: "UUID"
          constraints: ["PRIMARY KEY"]
        - name: "conversation_id"
          type: "UUID"
          constraints: ["FOREIGN KEY REFERENCES Conversation(id)"]
        - name: "sender_type"
          type: "VARCHAR(20)"
          constraints: ["NOT NULL"]
          values: ["customer", "agent", "system"]
        - name: "content"
          type: "TEXT"
          constraints: ["NOT NULL"]
        - name: "content_embedding"
          type: "VECTOR(1536)"
          constraints: ["NULL"]
        - name: "channel"
          type: "VARCHAR(50)"
          constraints: ["NOT NULL"]
        - name: "metadata"
          type: "JSONB"
          constraints: ["DEFAULT '{}'"]
        - name: "created_at"
          type: "TIMESTAMP"
          constraints: ["DEFAULT NOW()"]
    
    - name: "AIProvider"
      description: "AI provider configuration and quota tracking"
      fields:
        - name: "id"
          type: "INTEGER"
          constraints: ["PRIMARY KEY"]
        - name: "name"
          type: "VARCHAR(50)"
          constraints: ["UNIQUE", "NOT NULL"]
          values: ["openai", "gemini", "qwen"]
        - name: "priority"
          type: "INTEGER"
          constraints: ["NOT NULL"]
          values: ["1", "2", "3"]
        - name: "is_active"
          type: "BOOLEAN"
          constraints: ["DEFAULT TRUE"]
        - name: "daily_token_limit"
          type: "INTEGER"
          constraints: ["DEFAULT 100000"]
        - name: "tokens_used_today"
          type: "INTEGER"
          constraints: ["DEFAULT 0"]
        - name: "last_reset"
          type: "DATE"
          constraints: ["DEFAULT CURRENT_DATE"]
    
    - name: "Escalation"
      description: "Human escalation records"
      fields:
        - name: "id"
          type: "UUID"
          constraints: ["PRIMARY KEY"]
        - name: "ticket_id"
          type: "UUID"
          constraints: ["FOREIGN KEY REFERENCES Ticket(id)", "UNIQUE"]
        - name: "reason"
          type: "VARCHAR(255)"
          constraints: ["NOT NULL"]
          values: ["low_confidence", "negative_sentiment", "customer_request", "complex_issue"]
        - name: "escalated_to"
          type: "VARCHAR(255)"
          constraints: ["NULL"]
        - name: "escalated_at"
          type: "TIMESTAMP"
          constraints: ["DEFAULT NOW()"]
        - name: "resolved_at"
          type: "TIMESTAMP"
          constraints: ["NULL"]
        - name: "resolution_notes"
          type: "TEXT"
          constraints: ["NULL"]
@end

@block FLOW ticket_flow
priority: high
intent: "Define ticket ingestion and response flow"
scope: backend
depends_on: backend_data_model

content:
  flow_name: "Ticket Ingestion and Response"
  steps:
    - step: 1
      name: "Channel Webhook Received"
      description: "Gmail Pub/Sub or UltraMsg webhook triggers ticket creation"
      service: "Channel Connectors"
    
    - step: 2
      name: "Identity Resolution"
      description: "Match sender to existing Customer or create new"
      service: "API Gateway"
    
    - step: 3
      name: "Ticket Created"
      description: "New Ticket record with status 'open'"
      service: "Ticket Ingestion Service"
    
    - step: 4
      name: "Kafka Event Published"
      description: "tickets.create event published to Kafka"
      service: "Ticket Ingestion Service"
    
    - step: 5
      name: "AI Agent Triggered"
      description: "AI Agent Service consumes tickets.create event"
      service: "AI Agent Service"
    
    - step: 6
      name: "Context7 RAG Query"
      description: "Query Context7 for relevant documentation"
      service: "AI Agent Service"
    
    - step: 7
      name: "Response Generated"
      description: "AI generates response with confidence score"
      service: "AI Agent Service"
    
    - step: 8
      name: "Escalation Check"
      description: "If confidence < 0.7 or sentiment negative, escalate"
      service: "Escalation Service"
    
    - step: 9
      name: "Response Sent"
      description: "Response sent via original channel"
      service: "Channel Connectors"
    
    - step: 10
      name: "Memory Stored"
      description: "Message with embedding stored in PostgreSQL"
      service: "Memory Service"
@end

@block FLOW escalation_flow
priority: high
intent: "Define human escalation flow"
scope: backend
depends_on: ticket_flow

content:
  flow_name: "Human Escalation"
  trigger_conditions:
    - "AI confidence score < 0.7"
    - "Customer sentiment score < -0.5"
    - "Customer explicitly requests human"
    - "Ticket contains pricing or billing keywords"
  
  steps:
    - step: 1
      name: "Escalation Triggered"
      description: "Escalation record created with reason"
    
    - step: 2
      name: "Ticket Status Updated"
      description: "Ticket status changed to 'escalated'"
    
    - step: 3
      name: "Notification Sent"
      description: "Email/Slack notification to human agents"
    
    - step: 4
      name: "Human Takes Over"
      description: "Human agent assigned and responds"
    
    - step: 5
      name: "Resolution Logged"
      description: "Resolution notes added, ticket closed"
@end

@block BOUNDARIES service_boundaries
priority: medium
intent: "Define service boundaries and interfaces"
scope: backend
depends_on: backend_system

content:
  boundaries:
    - service: "API Gateway"
      provides:
        - "HTTP REST API"
        - "WebSocket for real-time updates"
      consumes:
        - "PostgreSQL"
        - "Kafka"
    
    - service: "Ticket Ingestion Service"
      provides:
        - "Kafka event production"
      consumes:
        - "Channel Webhooks"
        - "PostgreSQL"
    
    - service: "AI Agent Service"
      provides:
        - "Response generation"
      consumes:
        - "Context7 MCP"
        - "AI Providers (OpenAI, Gemini, Qwen)"
        - "PostgreSQL (memory)"
    
    - service: "Channel Connectors"
      provides:
        - "Webhook endpoints"
        - "Outbound message delivery"
      consumes:
        - "Gmail API"
        - "UltraMsg API"
        - "Kafka"
    
    - service: "Memory Service"
      provides:
        - "Vector storage and retrieval"
      consumes:
        - "PostgreSQL + pgvector"
    
    - service: "Escalation Service"
      provides:
        - "Escalation triggers"
        - "Human notification"
      consumes:
        - "PostgreSQL"
        - "Email/Slack APIs"
@end
```

---

## SYSTEM OVERVIEW

```
┌─────────────────────────────────────────────────────────────────┐
│                    Customer Success Digital FTE                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │    Gmail     │    │   UltraMsg   │    │  Web Form    │      │
│  │    API       │    │     API      │    │  (Next.js)   │      │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘      │
│         │                   │                   │               │
│         └───────────────────┼───────────────────┘               │
│                             ▼                                   │
│                  ┌─────────────────────┐                        │
│                  │   API Gateway       │                        │
│                  │   (FastAPI)         │                        │
│                  └──────────┬──────────┘                        │
│                             │                                   │
│         ┌───────────────────┼───────────────────┐               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐           │
│  │   Ticket    │   │     AI      │   │  Channel    │           │
│  │  Ingestion  │   │   Agent     │   │  Connectors │           │
│  │   Service   │   │   Service   │   │             │           │
│  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘           │
│         │                 │                 │                   │
│         ▼                 ▼                 ▼                   │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐           │
│  │    Kafka    │   │  Context7   │   │  Gmail API  │           │
│  │             │   │     MCP     │   │  UltraMsg   │           │
│  └──────┬──────┘   └──────┬──────┘   └─────────────┘           │
│         │                 │                                     │
│         ▼                 ▼                                     │
│  ┌─────────────────────────────────┐                           │
│  │      Memory Service             │                           │
│  │   (PostgreSQL + pgvector)       │                           │
│  └─────────────────────────────────┘                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## KAFKA TOPICS

| Topic | Purpose | Producer | Consumer |
|-------|---------|----------|----------|
| `tickets.create` | New ticket created | Ticket Ingestion | AI Agent, Analytics |
| `tickets.update` | Ticket status changed | API Gateway | AI Agent, Escalation |
| `messages.send` | Send message to customer | AI Agent | Channel Connectors |
| `escalations.trigger` | Human escalation needed | Escalation Service | Notification Service |

---

*End of ARCH.md — Customer Success Digital FTE v1.0.0*
