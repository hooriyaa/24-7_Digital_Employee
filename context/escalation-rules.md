# 🚨 Escalation Rules - Customer Support

## Overview

This document defines when and how to escalate customer issues to human agents. The AI agent should handle routine inquiries autonomously but recognize situations requiring human intervention.

---

## Escalation Triggers

### 🔴 CRITICAL - Immediate Escalation (Within 5 minutes)

**Trigger Conditions:**
1. **Security Breach:** Customer reports unauthorized access, data leak, or security vulnerability
2. **Data Loss:** Customer experienced data loss or corruption
3. **Service Outage:** Complete service unavailability for enterprise customer
4. **Legal/Compliance:** Legal threats, GDPR requests, compliance issues
5. **Payment Fraud:** Unauthorized charges or payment fraud

**Action:**
- Create ticket with priority: URGENT
- Tag: security, data-loss, outage, legal, or fraud
- Notify: Security team + Engineering lead + Customer success manager
- Response time: Within 5 minutes
- Channel: Phone call + Email + Slack alert

**Example Messages:**
- "My account was hacked!"
- "All my data is gone!"
- "We're suing for breach of contract!"
- "Your service is down and we're losing money!"

---

### 🟠 HIGH - Escalate Within 30 minutes

**Trigger Conditions:**
1. **Negative Sentiment:** Customer sentiment score < -0.5 (angry/frustrated)
2. **Repeated Requests:** Customer contacted support 3+ times in 24 hours
3. **Enterprise Down:** Enterprise customer reports critical feature not working
4. **Billing Dispute:** Customer disputes charge or requests refund
5. **Explicit Request:** Customer asks for human/supervisor/manager
6. **Threat to Churn:** Customer mentions canceling or switching to competitor

**Action:**
- Create ticket with priority: HIGH
- Tag: escalation, billing, enterprise, or churn-risk
- Notify: Senior support agent + Account manager (if enterprise)
- Response time: Within 30 minutes
- Channel: Email + Phone call for enterprise

**Example Messages:**
- "This is unacceptable! I want to speak to your manager!"
- "I'm canceling my subscription if this isn't fixed!"
- "We're evaluating other solutions."
- "I've contacted you 5 times and still no resolution!"
- "Charge me back immediately!"

---

### 🟡 MEDIUM - Escalate Within 2 hours

**Trigger Conditions:**
1. **Complex Technical Issue:** Problem requires engineering investigation
2. **Feature Request:** Customer requests custom feature or integration
3. **Pricing Negotiation:** Enterprise customer wants custom pricing
4. **Third-Party Issue:** Problem with integration partner (Slack, GitHub, etc.)
5. **AI Confidence Low:** AI confidence score < 0.6 in response

**Action:**
- Create ticket with priority: MEDIUM
- Tag: technical, feature-request, pricing, or integration
- Notify: Support specialist + Product team (if feature request)
- Response time: Within 2 hours
- Channel: Email

**Example Messages:**
- "Can you build a custom integration with Salesforce?"
- "We need special pricing for 500+ users."
- "The GitHub integration isn't syncing properly."
- "This bug only happens in specific circumstances."

---

### 🟢 LOW - Escalate Within 24 hours

**Trigger Conditions:**
1. **General Inquiry:** Question AI couldn't answer from knowledge base
2. **Feedback:** Customer provides product feedback or suggestions
3. **Training Request:** Customer wants training session or demo
4. **Partnership Inquiry:** Business development or partnership opportunities

**Action:**
- Create ticket with priority: LOW
- Tag: inquiry, feedback, training, or partnership
- Notify: Appropriate team (Sales, Product, or Partnerships)
- Response time: Within 24 hours
- Channel: Email

**Example Messages:**
- "Do you have plans to add [feature]?"
- "We'd like a training session for our team."
- "I have a suggestion for improvement."
- "Can we discuss a partnership?"

---

## Sentiment Analysis Thresholds

### Sentiment Scores

| Score Range | Sentiment | Action |
|-------------|-----------|--------|
| 0.7 to 1.0 | Very Positive | Continue AI handling |
| 0.3 to 0.7 | Positive | Continue AI handling |
| -0.3 to 0.3 | Neutral | Continue AI handling |
| -0.7 to -0.3 | Negative | Monitor closely, prepare to escalate |
| -1.0 to -0.7 | Very Negative | **ESCALATE IMMEDIATELY** |

### Sentiment Escalation Rules

**Very Negative (< -0.7):**
- Keywords: "angry", "frustrated", "useless", "terrible", "worst"
- Action: Immediate human intervention
- Response: Empathetic apology + immediate action

**Negative (-0.7 to -0.3):**
- Keywords: "disappointed", "unhappy", "issue", "problem"
- Action: AI attempts resolution, flag for human review
- Response: Acknowledge concern + provide solution + follow-up

---

## Customer Tier Escalation

### Free Plan Users
- **Standard:** AI handles everything
- **Escalation:** Only for critical issues (security, data loss)
- **Response Time:** 24-48 hours

### Pro Plan Users
- **Standard:** AI handles routine, human for complex
- **Escalation:** Technical issues, billing disputes
- **Response Time:** 2-24 hours

### Enterprise Users
- **Standard:** Human agent assigned from start
- **Escalation:** Immediate for any issue
- **Response Time:** 1 hour (critical), 4 hours (normal)
- **Dedicated:** Account manager + priority support

---

## Escalation Workflow

### Step 1: Identify Escalation Need

**AI Checks:**
1. Sentiment analysis score
2. Customer tier (Free/Pro/Enterprise)
3. Issue category (technical/billing/general)
4. Keyword detection (angry, cancel, lawsuit, etc.)
5. Conversation history (repeated contacts?)
6. Confidence score in proposed solution

### Step 2: Create Escalation Ticket

**Required Information:**
- Customer name and email
- Customer tier
- Issue summary
- Sentiment score
- Conversation transcript
- Suggested priority
- Tags for routing

### Step 3: Notify Appropriate Team

**Notification Channels:**
- **Slack:** #support-escalations
- **Email:** support-lead@techflow.io
- **PagerDuty:** For critical (security/outage)
- **Phone:** For enterprise critical issues

### Step 4: Handoff to Human

**AI Message to Customer:**
```
Thank you for your patience. I'm connecting you with [Agent Name], 
our [specialist/manager], who will be happy to assist you further. 
They'll review our conversation and get back to you within 
[response time based on priority].

Your ticket number is #[ticket-id]. You can track status at 
techflow.io/support/tickets/[ticket-id].

Is there anything else I can help you with while you wait?
```

### Step 5: Follow-up

**Human Agent Responsibilities:**
1. Review conversation transcript
2. Contact customer within SLA
3. Resolve issue or escalate further
4. Update ticket with resolution
5. Tag for knowledge base if new issue

---

## Special Cases

### VIP Customers
**Criteria:**
- Enterprise customers with >100 users
- Customers paying >$500/month
- Strategic partners

**Handling:**
- Always escalate to dedicated account manager
- Response time: 30 minutes maximum
- Channel: Phone call preferred

### Media/Press Inquiries
**Keywords:** "press", "media", "journalist", "article", "interview"

**Handling:**
- Escalate to PR/Communications team immediately
- Do not provide any statements
- Tag: media-inquiry

### Competitor Mentions
**Keywords:** Competitor names (Asana, Monday, Trello, Jira, etc.)

**Handling:**
- If customer threatening to switch: Escalate to retention team
- If customer comparing features: Provide honest comparison, escalate if needed
- Tag: competitor, churn-risk

---

## Quality Assurance

### Escalation Review

**Weekly Review:**
- Review all escalations from past week
- Identify patterns (common issues, product gaps)
- Update knowledge base with new solutions
- Provide feedback to AI training

**Metrics to Track:**
- Escalation rate (target: <20%)
- Time to escalate (target: <5 min for critical)
- Resolution time after escalation
- Customer satisfaction post-escalation
- Repeat escalations per customer

### Continuous Improvement

**Monthly:**
- Analyze escalation reasons
- Update escalation rules if needed
- Train AI on new scenarios
- Update knowledge base articles

**Quarterly:**
- Review escalation thresholds
- Update customer tier policies
- Train support team on new processes

---

## Contact Information

### Support Teams

**Support Lead:**
- Name: Sarah Johnson
- Email: sarah.j@techflow.io
- Phone: 1-800-TECHFLOW ext. 1

**Enterprise Manager:**
- Name: Michael Chen
- Email: michael.c@techflow.io
- Phone: 1-800-TECHFLOW ext. 2

**Security Team:**
- Email: security@techflow.io
- Phone: 1-800-TECHFLOW ext. 9 (24/7)

**Engineering On-Call:**
- PagerDuty: techflow-support
- Slack: #eng-oncall

---

## Examples

### Example 1: Billing Dispute

**Customer:** "I was charged twice! This is ridiculous! I want my money back NOW!"

**Analysis:**
- Sentiment: -0.8 (Very Negative)
- Issue: Billing dispute
- Tier: Pro
- Trigger: Negative sentiment + billing + demand for refund

**Action:** ESCALATE IMMEDIATELY (HIGH priority)
- Tag: billing, refund, escalation
- Notify: Billing team + Support lead
- Response: Within 30 minutes

---

### Example 2: Feature Request

**Customer:** "Would be great if you could add a calendar view for tasks."

**Analysis:**
- Sentiment: 0.5 (Positive)
- Issue: Feature request
- Tier: Free
- Trigger: Feature request

**Action:** ESCALATE (LOW priority)
- Tag: feature-request, product
- Notify: Product team
- Response: Within 24 hours

---

### Example 3: Security Concern

**Customer:** "I think someone accessed my account without permission!"

**Analysis:**
- Sentiment: -0.9 (Very Negative)
- Issue: Security breach
- Tier: Pro
- Trigger: Security concern

**Action:** ESCALATE IMMEDIATELY (CRITICAL priority)
- Tag: security, urgent
- Notify: Security team + Engineering
- Response: Within 5 minutes
- Channel: Phone call

---

### Example 4: Integration Issue

**Customer:** "The Slack integration stopped working yesterday. Messages aren't coming through."

**Analysis:**
- Sentiment: -0.2 (Slightly Negative)
- Issue: Third-party integration
- Tier: Pro
- Trigger: Technical issue with integration

**Action:** ESCALATE (MEDIUM priority)
- Tag: integration, technical, slack
- Notify: Support specialist
- Response: Within 2 hours

---

## AI Response Templates

### For Immediate Escalation

```
I understand this is urgent, and I want to make sure you get the help you need right away.

I'm escalating this to our [specialist/manager] team. They'll contact you within 
[response time] at [customer email/phone].

Your ticket number is #[ticket-id]. You can track it here: [tracking URL]

Is there anything else I can help you with while you wait?
```

### For Standard Escalation

```
Thank you for providing those details. I'm going to connect you with a specialist 
who can better assist with this issue.

They'll review our conversation and get back to you within [response time].

Your ticket reference is #[ticket-id].

Is there anything else I can help you with today?
```

### For Follow-up

```
Hi [Customer Name],

I wanted to follow up on your ticket #[ticket-id]. Our team is still working on 
resolving this issue.

Current status: [status]
Expected resolution: [timeframe]

We'll update you as soon as we have more information. Please don't hesitate to 
reach out if you have any questions.

Best regards,
[Agent Name]
Customer Success Team
```
