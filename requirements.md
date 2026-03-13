# 🏭 Project Requirements: Customer Success Digital FTE Factory

## 1. Executive Summary
This project aims to build a **Digital Full-Time Equivalent (FTE)**—a 24/7 autonomous AI employee. The system will handle customer inquiries across Email, WhatsApp, and Web, using the latest AI standards and a custom PostgreSQL-based CRM.

## 2. Intelligence Strategy: The Context7 Advantage
To ensure high accuracy and zero hallucination, the agent uses **Context7** as its primary knowledge source.
* **Real-time Docs:** Fetching latest snippets for `OpenAI Agents SDK`, `FastAPI`, `Next.js`, and `UltraMsg`.
* **RAG Flow:** The agent will first query Context7 for technical documentation before generating any response.
* **Up-to-date Coding:** Using Context7 to write modern, bug-free code for the implementation phase.

## 3. Tech Stack (The Specialist Body)
* **Frontend:** React/Next.js (For the mandatory Web Support Form).
* **Backend:** FastAPI (Python) for high-performance API endpoints.
* **AI Agent:** OpenAI Agents SDK (Primary) with fallback to Gemini/OpenRouter (Qwen).
* **Messaging:** UltraMsg API for WhatsApp integration.
* **CRM/Database:** PostgreSQL with `pgvector` for long-term memory.
* **Reliability:** Apache Kafka for ticket ingestion and event streaming.
* **Infrastructure:** Docker containers and Kubernetes (K8s) for 24/7 uptime.

## 4. Multi-Channel Architecture
| Channel | Technology | Integration Logic |
| :--- | :--- | :--- |
| **Gmail** | Gmail API | Webhook/Pub-Sub to trigger ticket creation from emails. |
| **WhatsApp** | UltraMsg | Real-time chat handling with concise, casual formatting. |
| **Web Form** | Next.js Component | Direct API submission into the Kafka ingestion queue. |

## 5. Development Strategy (Step-by-Step)

### Phase 1: Foundation & CRM (Hours 1-8)
* **Database:** Design PostgreSQL schema (Customers, Conversations, Tickets, Messages).
* **Context:** Connect Context7 to pull latest SDK documentation.
* **Infra:** Setup Docker Compose for local development (Postgres + Kafka).

### Phase 2: Agent Brain & Multi-Provider (Hours 9-24)
* **Agent Factory:** Create a Custom Class that switches providers (OpenAI ↔ Gemini) based on quota.
* **Skills:** Implement Knowledge Retrieval (using Context7) and Sentiment Analysis.
* **Escalation:** Define rules for Human-in-the-loop (e.g., pricing or angry users).

### Phase 3: Channel Integration & Web UI (Hours 25-40)
* **Intake Handlers:** Build webhooks for UltraMsg and Gmail.
* **Frontend:** Build the "Web Support Form" React component with status tracking.
* **Kafka:** Implement the producer-consumer logic for unified ingestion.

### Phase 4: Production & Resilience (Hours 41-48)
* **Deployment:** Write Kubernetes manifests (Deployments, Services, HPA).
* **Load Testing:** Run Locust to simulate 100+ concurrent customer messages.
* **Chaos Testing:** Verify 99.9% uptime by simulating pod failures.

## 6. Business Value & KPIs
* **Target Cost:** Operating at <$1,000/year per FTE.
* **Response Speed:** < 3 seconds average latency.
* **Continuity:** 100% identification of the same customer across all 3 channels.