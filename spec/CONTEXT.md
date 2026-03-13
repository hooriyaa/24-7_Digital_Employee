# CONTEXT.md — Intent Freezer

> **Customer Success Digital FTE — Why This System Exists**
>
> This document defines the **immutable intent** and **explicit exclusions** for the project.
> LLMs must reject any feature or behavior that violates these declarations.

---

```slc
@block INTENT cs_fte_intent
priority: critical
intent: "Define why the Customer Success Digital FTE exists"
scope: global
depends_on: none

content:
  purpose: "Build a 24/7 autonomous AI employee that handles customer inquiries across Email, WhatsApp, and Web channels"
  
  goals:
    - "Provide instant customer support responses (<3 seconds latency)"
    - "Unify customer identity across all 3 channels (Gmail, WhatsApp, Web)"
    - "Operate continuously with 99.9% uptime"
    - "Maintain conversation memory using PostgreSQL + pgvector"
    - "Use Context7 for real-time documentation and zero hallucination"
    - "Support multi-provider AI fallback (OpenAI → Gemini → Qwen)"
    - "Enable human-in-the-loop escalation for complex cases"
    - "Keep operating costs under $1,000/year per FTE"
  
  non_goals:
    - "Replace human agents entirely (escalation is required)"
    - "Handle voice calls or voice-based support"
    - "Support social media channels (Twitter, Facebook, Instagram)"
    - "Build a mobile application"
    - "Provide analytics dashboards for business intelligence"
    - "Integrate with third-party CRMs (Salesforce, HubSpot, Zendesk)"
    - "Support languages other than English in v1.0"
    - "Handle payment processing or financial transactions"
    - "Provide marketing automation or sales outreach"
@end
```

---

## GOAL

Build a **Digital Full-Time Equivalent (FTE)** — a 24/7 autonomous AI employee that:

1. **Handles customer inquiries** across Email (Gmail), WhatsApp (UltraMsg), and Web (Next.js form)
2. **Responds in under 3 seconds** average latency
3. **Maintains 99.9% uptime** via Kubernetes orchestration
4. **Remembers all conversations** using PostgreSQL with pgvector for long-term memory
5. **Uses Context7** as the primary knowledge source to prevent hallucinations
6. **Falls back between AI providers** (OpenAI → Gemini → Qwen) based on quota and availability
7. **Escalates to humans** when confidence is low or sentiment is negative
8. **Operates at under $1,000/year** per FTE instance

---

## NON-GOALS

The following are **explicitly excluded** from this project:

| Exclusion | Rationale |
|-----------|-----------|
| **Full human replacement** | Escalation to human agents is a core requirement |
| **Voice call support** | Out of scope for v1.0; text-only channels |
| **Social media integration** | Twitter, Facebook, Instagram not supported |
| **Mobile application** | Web-only interface for customer interactions |
| **BI analytics dashboards** | Focus on support, not business intelligence |
| **Third-party CRM integration** | Custom PostgreSQL CRM is the system of record |
| **Multi-language support** | English-only for v1.0 |
| **Payment processing** | No financial transactions handled |
| **Marketing automation** | Pure customer success focus |

---

## SUCCESS CRITERIA

The system is considered successful when:

- [ ] **100% customer identification** across all 3 channels
- [ ] **<3 seconds average response latency** under load
- [ ] **99.9% uptime** during production operation
- [ ] **Zero hallucinated responses** (Context7 RAG enforced)
- [ ] **<$1,000/year operating cost** per FTE instance
- [ ] **Seamless human escalation** when confidence < threshold

---

*End of CONTEXT.md — Customer Success Digital FTE v1.0.0*
