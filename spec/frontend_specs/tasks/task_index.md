# task_index.md — Frontend Task Registry

> **Customer Success Digital FTE — Global Frontend Task Registry**
>
> This file is the **single source of truth** for all frontend tasks.
> LLM must read this file once, then load individual task files as needed.

---

```slc
@block INDEX task_registry
priority: critical
intent: "Global frontend task registry - all tasks visible"
scope: frontend
failure_if_skipped: true

content:
  total_tasks: 30
  total_estimate_minutes: 240
  total_estimate_hours: 4
  
  phases:
    - phase: 1
      name: "Foundation & Public Pages"
      dir: "phases/phase-1/"
      tasks: 10
      estimate_minutes: 90
    
    - phase: 2
      name: "Dashboard & Ticket Management"
      dir: "phases/phase-2/"
      tasks: 14
      estimate_minutes: 100
    
    - phase: 3
      name: "Escalations & Polish"
      dir: "phases/phase-3/"
      tasks: 6
      estimate_minutes: 50
  
  all_tasks:
    # Phase 1
    - id: "1.1"
      file: "phases/phase-1/1.1_init_nextjs.md"
      title: "Initialize Next.js 14 project"
      status: done
      estimate_minutes: 10
    
    - id: "1.2"
      file: "phases/phase-1/1.2_tailwind_shadcn.md"
      title: "Configure Tailwind CSS and shadcn/ui"
      status: done
      estimate_minutes: 10

    - id: "1.3"
      file: "phases/phase-1/1.3_project_structure.md"
      title: "Create frontend directory structure"
      status: done
      estimate_minutes: 5

    - id: "1.4"
      file: "phases/phase-1/1.4_api_client.md"
      title: "Implement chat interface and sidebar"
      status: done
      estimate_minutes: 15
    
    - id: "1.5"
      file: "phases/phase-1/1.5_react_query.md"
      title: "Setup API client with Axios"
      status: done
      estimate_minutes: 10

    - id: "1.6"
      file: "phases/phase-1/1.6_zustand_store.md"
      title: "Implement Tickets table with live data"
      status: done
      estimate_minutes: 15

    - id: "1.7"
      file: "phases/phase-1/1.7_types_types.md"
      title: "Implement Customers table with live data"
      status: done
      estimate_minutes: 15

    - id: "1.8"
      file: "phases/phase-1/1.8_web_support_form.md"
      title: "Implement Knowledge Base grid"
      status: done
      estimate_minutes: 15
    
    - id: "1.9"
      file: "phases/phase-1/1.9_ticket_status_page.md"
      title: "Build Ticket Status page"
      status: todo
      estimate_minutes: 10
    
    - id: "1.10"
      file: "phases/phase-1/1.11_public_layout.md"
      title: "Create public page layout"
      status: todo
      estimate_minutes: 10
    
    # Phase 2
    - id: "2.1"
      file: "phases/phase-2/2.1_auth_store.md"
      title: "Implement authentication store"
      status: todo
      estimate_minutes: 10
    
    - id: "2.2"
      file: "phases/phase-2/2.2_login_page.md"
      title: "Build Login page"
      status: todo
      estimate_minutes: 10
    
    - id: "2.3"
      file: "phases/phase-2/2.3_auth_guards.md"
      title: "Implement auth guards and redirects"
      status: todo
      estimate_minutes: 10
    
    - id: "2.4"
      file: "phases/phase-2/2.4_dashboard_layout.md"
      title: "Create dashboard layout with sidebar"
      status: todo
      estimate_minutes: 10
    
    - id: "2.5"
      file: "phases/phase-2/2.5_dashboard_home.md"
      title: "Build Dashboard home page"
      status: todo
      estimate_minutes: 5
    
    - id: "2.6"
      file: "phases/phase-2/2.6_ticket_list.md"
      title: "Build Ticket List page"
      status: todo
      estimate_minutes: 10
    
    - id: "2.7"
      file: "phases/phase-2/2.7_ticket_filters.md"
      title: "Implement ticket filters and search"
      status: todo
      estimate_minutes: 10
    
    - id: "2.8"
      file: "phases/phase-2/2.8_ticket_detail.md"
      title: "Build Ticket Detail page"
      status: todo
      estimate_minutes: 10
    
    - id: "2.9"
      file: "phases/phase-2/2.9_conversation_thread.md"
      title: "Build conversation thread component"
      status: todo
      estimate_minutes: 10
    
    - id: "2.10"
      file: "phases/phase-2/2.11_agent_response.md"
      title: "Implement agent response form"
      status: todo
      estimate_minutes: 10
    
    - id: "2.11"
      file: "phases/phase-2/2.12_ai_response.md"
      title: "Integrate AI response generation UI"
      status: todo
      estimate_minutes: 10
    
    - id: "2.12"
      file: "phases/phase-2/2.13_ticket_actions.md"
      title: "Implement ticket actions (close, assign)"
      status: todo
      estimate_minutes: 5
    
    - id: "2.13"
      file: "phases/phase-2/2.14_toast_notifications.md"
      title: "Setup toast notifications"
      status: todo
      estimate_minutes: 5
    
    - id: "2.14"
      file: "phases/phase-2/2.15_loading_states.md"
      title: "Implement loading states and skeletons"
      status: todo
      estimate_minutes: 5
    
    # Phase 3
    - id: "3.1"
      file: "phases/phase-3/3.1_escalation_list.md"
      title: "Build Escalation List page"
      status: todo
      estimate_minutes: 10
    
    - id: "3.2"
      file: "phases/phase-3/3.2_escalation_actions.md"
      title: "Implement escalation actions"
      status: todo
      estimate_minutes: 10
    
    - id: "3.3"
      file: "phases/phase-3/3.3_customer_list.md"
      title: "Build Customer List page"
      status: todo
      estimate_minutes: 10
    
    - id: "3.4"
      file: "phases/phase-3/3.4_responsive_design.md"
      title: "Verify responsive design"
      status: todo
      estimate_minutes: 10
    
    - id: "3.5"
      file: "phases/phase-3/3.5_e2e_tests.md"
      title: "Write E2E tests"
      status: todo
      estimate_minutes: 5
    
    - id: "3.6"
      file: "phases/phase-3/3.6_production_build.md"
      title: "Build and deploy production"
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
| Total Tasks | 30 |
| Completed | 8 |
| In Progress | 0 |
| Pending | 22 |
| Current Phase | 1 |

### Completed Tasks

**Phase 1: Foundation (8/10 tasks)**
- [x] 1.1 - Initialize Next.js 14 project
- [x] 1.2 - Configure Tailwind CSS and shadcn/ui ✅
- [x] 1.3 - Create frontend directory structure ✅
- [x] 1.4 - Implement chat interface and sidebar ✅
- [x] 1.5 - Setup API client with Axios ✅ NEW
- [x] 1.6 - Implement Tickets table with live data ✅ NEW
- [x] 1.7 - Implement Customers table with live data ✅ NEW
- [x] 1.8 - Implement Knowledge Base grid ✅ NEW

### Next Task
- [ ] 1.9 - Build Ticket Status page

---

*End of task_index.md — Frontend Task Registry*
