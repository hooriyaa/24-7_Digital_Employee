# SLC — Universal Project Structure Rule

> **Purpose**
> This document defines the **universal, project-agnostic SLC structure** that an LLM must follow to initiate, plan, and execute any software project using **Spec‑Driven Development**.
>
> This file is the **root behavioral contract** between humans and LLMs.
>
> If this file is present, the LLM must **strictly obey it**. If it is missing or violated, execution must abort.

---

## 1. Core Philosophy (Non‑Negotiable)

SLC enforces the following truths:

1. **Specs come before code**
2. **Intent freezes before execution**
3. **Tasks are immutable once approved**
4. **Memory overrides creativity**
5. **Security overrides convenience**
6. **Frontend and backend derive from the same source of truth**

LLMs must not invent structure, APIs, models, or behavior outside what is explicitly defined.

---

## 2. Mandatory Root Structure

Every SLC‑compliant project MUST follow this root structure:

```
spec/
├── SPEC.md
├── CONTEXT.md
├── CONSTRAINTS.md
├── SECURITY.md
├── MEMORY.md
│
├── backend_specs/
│   ├── ARCH.md
│   ├── PLAN.md
│   ├── CONTRACT.md
│   └── tasks/
│       ├── task_index.md      # Hot: Global task registry & router
│       └── phases/
│           ├── phase-1/       # Individual task files
│           ├── phase-2/
│           └── phase-N/
│
├── frontend_specs/
│   ├── ARCH.md
│   ├── PLAN.md
│   ├── CONTRACT.md
│   └── tasks/
│       ├── task_index.md
│       └── phases/
│           ├── phase-1/
│           └── phase-2/
```

Any deviation must be explicitly approved by the user and recorded in `MEMORY.md`.

---

## 3. SPEC.md — Global Router (Entry Point)

### Responsibilities

`SPEC.md` is the **single entry point**. The LLM must read this file first.

It must define:
- Mandatory read order
- Execution rules
- Immutability constraints
- Approval gates

### Required Sections

```md
## READ ORDER (MANDATORY)
1. CONTEXT.md
2. CONSTRAINTS.md
3. SECURITY.md
4. MEMORY.md
5. backend/ARCH.md
6. frontend/ARCH.md

## EXECUTION RULES
- No code generation before ARCH files are finalized
- TASKS.md files are locked after user approval
- CONTRACT.md is authoritative
- Violations must abort execution
```

LLMs must not skip or reorder these steps.

---

## 4. CONTEXT.md — Intent Freezer

### Purpose

Defines **why the system exists** and **what it is not**.

### Rules

- Immutable unless user explicitly changes it
- No technical implementation details

### Required Sections

```md
## GOAL
<single clear objective>

## NON‑GOALS
- <explicit exclusions>
```

LLMs must reject features that violate NON‑GOALS.

---

## 5. CONSTRAINTS.md — Reality Anchor

### Purpose

Defines **hard limits**. These override all plans and tasks.

### Required Sections

```md
## TECH
- Language
- Frameworks

## SCALE
- Expected usage limits

## HARD RULES
- Non‑negotiable constraints
```

LLMs must not propose solutions outside these constraints.

---

## 6. SECURITY.md — Global Security Law

### Purpose

Defines security rules that apply to **all code**.

### Rules

- This file overrides convenience, speed, and creativity
- Violations must be explicitly reported

### Required Sections

```md
## BACKEND RULES
- <security principles>

## FRONTEND RULES
- <client‑side rules>

## API RULES
- <contract enforcement>
```

LLMs must refuse to generate insecure code.

---

## 7. MEMORY.md — Anti‑Hallucination Anchor

### Purpose

Defines **frozen facts and decisions**.

This file exists to prevent:
- Drift
- Contradictions
- Hallucinated changes

### Required Sections

```md
## DECISIONS
- <final decisions>

## ASSUMPTIONS
- <explicit assumptions>

## DO NOT CHANGE
- <immutable facts>
```

If a conflict arises, MEMORY.md always wins.

---

## 8. Backend Rules (Authoritative)

### backend/ARCH.md

Defines:
- Data models
- Control flow
- Boundaries

No tasks. No code.

---

### backend/PLAN.md

Defines:
- High‑level execution phases
- No implementation details

---

### backend_specs/tasks/ — Individual Task File System

**Purpose**: Maximum granularity and context efficiency with individual task files.

**Problem**: Even phase-based files require loading entire phase context when only one task is needed.

**Solution**: Individual task files with global index for routing.

---

#### Directory Structure

```
tasks/
├── task_index.md              # HOT: Global registry + SINGLE SOURCE OF TRUTH for status
└── phases/
    ├── phase-1/
    │   ├── 1.1_init_project.md    # Task definition only (no status)
    │   ├── 1.2_project_structure.md
    │   └── ...
    ├── phase-2/
    ├── phase-3/
    ├── phase-4/
    └── phase-5/
```

---

#### tasks/task_index.md (HOT)

**Authority**: Global task registry — lists ALL tasks at once.

**Key Rule**: Tasks are NOT locked. All visible from start.

**Responsibilities**:
- List ALL tasks across ALL phases with status
- Track current execution position
- Route to individual task files
- NO iteration needed — full visibility

**Required Structure**:

```slc
@block INDEX task_registry
priority: critical
intent: "Global task registry - all tasks visible"
scope: global
failure_if_skipped: true

content:
  total_tasks: 55
  total_estimate: 810
  
  phases:
    - phase: 1
      name: "Foundation"
      dir: "phases/phase-1/"
      tasks: 11
      estimate: 120
      
    - phase: 2
      name: "Core Entities"
      dir: "phases/phase-2/"
      tasks: 16
      estimate: 240

  all_tasks:
    # Phase 1
    - id: "1.1"
      file: "phases/phase-1/1.1_init_project.md"
      status: todo
    - id: "1.2"
      file: "phases/phase-1/1.2_project_structure.md"
      status: todo
    # ... all tasks listed
@end
```

**Execution Rule**: LLM reads `task_index.md` once, sees all tasks, loads only the individual task file needed.

---

#### phases/phase-N/X.X_task_name.md (WARM)

**Purpose**: Single task in isolated file.

**Benefits**:
- Load only ~1-2KB per task execution
- No parsing overhead
- Clean git history per task
- Easy status updates

**Required Structure**:

```slc
@block TASK 1.1_init_project
priority: critical
intent: "Initialize FastAPI project with UV package manager"
scope: phase-1
depends_on: none
estimate: 10
status: todo

content:
  - Create project directory: backend/
  - Initialize with: uv init
  - Create pyproject.toml with dependencies
  
acceptance_criteria:
  - pyproject.toml exists with all dependencies
  - UV package manager working
@end
```

**File Naming**: `{phase}.{task_number}_{snake_case_name}.md`

---

#### phases/phase-N/_summary.md

**Purpose**: Phase overview and progress tracking.

**Required Structure**:

```slc
@block PHASE phase_1_summary
priority: high
intent: "Phase 1 overview and progress"
scope: phase-1

content:
  name: "Foundation"
  description: "Project setup, database, authentication"
  total_tasks: 11
  estimate: 120
  completed: 0
  
  task_order:
    - 1.1_init_project
    - 1.2_project_structure
    - 1.3_env_config
    # ... all tasks in order
@end
```

---

#### Memory Tier Strategy

| Tier | Files | Load Frequency | Size Target |
|------|-------|----------------|-------------|
| **HOT** | task_index.md | Once per session | <8KB |
| **WARM** | Individual task files | Per execution | <2KB each |

**Context Window Optimization**:
- Load task_index.md once (~8KB for 55 tasks)
- Load individual task file (~1-2KB)
- **Total per task: ~2KB** vs 64KB = **97% reduction**

---

#### Migration from Legacy TASKS.md

**If TASKS.md exists**:
1. Read TASKS.md
2. Create phases/ directory structure
3. Extract each `@block TASK` to individual file
4. Generate task_index.md with all tasks
5. Create _summary.md per phase
6. Delete legacy TASKS.md
7. Update SPEC.md to point to task_index.md

---

### backend_specs/CONTRACT.md

Defines:
- API schemas
- Endpoints
- Payload shapes

This file is **authoritative** for frontend.

---

## 9. Frontend Rules (Derived)

Frontend MUST derive from backend `CONTRACT.md`.

### frontend_specs/ARCH.md

Defines:
- State shape
- UI flow
- Rendering logic

No API invention allowed.

---

### frontend_specs/PLAN.md & tasks/

Same rules as backend, but:
- Tasks must align with backend contracts
- Any mismatch must be reported
- Uses same phase‑based task structure

---

## 10. Execution Protocol (LLM Behavior)

LLM must follow this loop:

1. Read SPEC.md
2. Read files in declared order
3. Validate MEMORY + SECURITY
4. Finalize ARCH files
5. Generate task files (phase‑by‑phase)
7. Create task_index.md
8. Ask for user approval
9. Lock task_index
10. **Execute tasks via router**:
    - Read task_index.md
    - Load only current phase file
    - Execute next task
    - Update task_index.md status
    - If phase complete, move to archive
    - Unlock next phase

Skipping steps is forbidden.

---

### Task Execution Loop (Detailed)

```
while (tasks_remaining):
  1. Read task_index.md
  2. Get current_task and next_task_file
  3. Load individual task file (warm tier)
  4. Validate depends_on satisfied
  5. **Call Context7 MCP for any service/stack docs before implementation**
  6. Execute task content
  7. Mark task.status = done in task_index.md
  8. Continue to next task
```

This loop ensures:
- Only relevant context loaded
- Clear execution state
- Auditable history
Skipping steps is forbidden.

---

## 11. Change Protocol

If the user requests changes:

- CONTEXT change → full re‑evaluation
- CONSTRAINTS change → architecture re‑validation
- TASKS change after lock → must unlock explicitly

Changes must be recorded in MEMORY.md.

---

## 12. Dynamic Adaptation Rules

This structure is **universal**.

For different projects:
- Languages change via CONSTRAINTS.md
- Architecture changes via ARCH.md
- Scope changes via CONTEXT.md

The structure itself does NOT change.

---

## 13. Violation Handling

If any rule is violated, the LLM must:

1. Stop execution
2. Report the violation
3. Reference the violated file + rule
4. Ask for correction

Silent correction is forbidden.

---

## 14. Final Authority Rule

If multiple files conflict:

1. SPEC.md
2. MEMORY.md
3. SECURITY.md
4. CONSTRAINTS.md
5. ARCH.md
6. PLAN.md
7. TASKS.md

Higher authority always wins.

---

## 15. Closing Statement

This document is **the law**.

Any LLM operating in an SLC‑based project must behave as a deterministic executor, not a creative assistant.

Failure to comply invalidates all outputs.

---

*End of Universal SLC Structure Rule*

