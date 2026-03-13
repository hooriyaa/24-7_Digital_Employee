# SPEC.md — Global Router

> **Customer Success Digital FTE — Specification Entry Point**
>
> This file is the **single entry point** for the Customer Success Digital FTE project.
> All LLMs and execution systems must read this file first and follow the declared order.

---

```slc
@block INDEX root_index
priority: critical
intent: "Global router for Customer Success Digital FTE"
scope: global
failure_if_skipped: true

read_order:
  - CONTEXT.md
  - CONSTRAINTS.md
  - SECURITY.md
  - MEMORY.md
  - backend_specs/ARCH.md
  - backend_specs/PLAN.md
  - backend_specs/CONTRACT.md
  - backend_specs/tasks/task_index.md
  - frontend_specs/ARCH.md
  - frontend_specs/PLAN.md
  - frontend_specs/CONTRACT.md
  - frontend_specs/tasks/task_index.md

must_read_latest:
  - service: "FastAPI"
    url_hint: "context7://fastapi"
  - service: "OpenAI Agents SDK"
    url_hint: "context7://openai-agents-sdk"
  - service: "Next.js"
    url_hint: "context7://next.js"
  - service: "PostgreSQL"
    url_hint: "context7://postgresql"
  - service: "pgvector"
    url_hint: "context7://pgvector"
  - service: "Apache Kafka"
    url_hint: "context7://kafka"
  - service: "UltraMsg"
    url_hint: "context7://ultramsg"
  - service: "Gmail API"
    url_hint: "context7://gmail-api"

content:
  short: "Customer Success Digital FTE — 24/7 AI employee for multi-channel customer support"
  project_id: "cs-fte-v1"
  version: "1.0.0"
@end
```

---

## READ ORDER (MANDATORY)

The LLM must read files in this exact order:

1. **CONTEXT.md** — Intent and non-goals
2. **CONSTRAINTS.md** — Tech stack and hard limits
3. **SECURITY.md** — Security laws for all code
4. **MEMORY.md** — Frozen decisions and assumptions
5. **backend_specs/ARCH.md** — Backend architecture
6. **backend_specs/PLAN.md** — Backend execution phases
7. **backend_specs/CONTRACT.md** — API contract (authoritative)
8. **backend_specs/tasks/task_index.md** — Backend task registry
9. **frontend_specs/ARCH.md** — Frontend architecture
10. **frontend_specs/PLAN.md** — Frontend execution phases
11. **frontend_specs/CONTRACT.md** — Frontend contract
12. **frontend_specs/tasks/task_index.md** — Frontend task registry

---

## EXECUTION RULES

- **No code generation** before ARCH files are finalized
- **Task files are locked** after user approval via task_index.md
- **CONTRACT.md is authoritative** for API schemas
- **Violations must abort execution** and report diagnostics
- **Context7 MCP must be called** before implementing any service integration

---

## APPROVAL GATES

| Gate | Trigger | Required Sign-off |
|------|---------|-------------------|
| Gate 1 | ARCH files complete | User approval before tasks |
| Gate 2 | Phase 1 tasks complete | User approval before Phase 2 |
| Gate 3 | Phase 2 tasks complete | User approval before Phase 3 |
| Gate 4 | Phase 3 tasks complete | User approval before Phase 4 |
| Gate 5 | All phases complete | Final user acceptance |

---

## IMMUTABILITY CONSTRAINTS

- Once a task status is `done`, it cannot revert to `todo` without explicit user override
- CONTRACT.md changes require re-validation of dependent tasks
- CONTEXT.md changes trigger full architecture re-evaluation

---

## VIOLATION HANDLING

If any rule is violated, the LLM must:

1. Stop execution immediately
2. Report the violation with code and message
3. Reference the violated file and rule
4. Ask for user correction before proceeding

Silent correction is **forbidden**.

---

*End of SPEC.md — Customer Success Digital FTE v1.0.0*
