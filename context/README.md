# 📚 Context Files - Knowledge Base for AI Agent

## Overview

This folder contains all the context and knowledge base files that power the Customer Success FTE (Digital FTE) AI agent. These files provide the AI with information about the company, products, policies, and customer interaction patterns.

---

## 📁 File Structure

```
context/
├── company-profile.md      # Company information, mission, values, products
├── product-docs.md         # Detailed product documentation, features, pricing
├── escalation-rules.md     # When and how to escalate to human agents
├── brand-voice.md          # Communication guidelines and tone
└── sample-tickets.json     # Example customer inquiries for training
```

---

## 📄 File Descriptions

### 1. **company-profile.md**

**Purpose:** Provides the AI with company background and context.

**Contains:**
- Company overview (name, industry, size)
- Mission statement and core values
- Product lineup and target audiences
- Contact information
- Recent company news

**AI Uses This For:**
- Answering "Tell me about your company" questions
- Understanding company positioning
- Providing accurate company information
- Representing brand values in responses

---

### 2. **product-docs.md**

**Purpose:** Comprehensive product knowledge for customer support.

**Contains:**
- Getting started guides
- Feature descriptions
- Pricing plans (Free, Pro, Enterprise)
- Integration documentation
- Troubleshooting guides
- FAQs

**AI Uses This For:**
- Answering product questions
- Providing how-to guidance
- Explaining features and pricing
- Troubleshooting common issues
- Comparing plans

---

### 3. **escalation-rules.md**

**Purpose:** Defines when AI should escalate to human agents.

**Contains:**
- Escalation triggers (Critical, High, Medium, Low)
- Sentiment analysis thresholds
- Customer tier handling
- Escalation workflows
- Contact information for teams
- Response time SLAs

**AI Uses This For:**
- Deciding when to escalate
- Determining escalation priority
- Routing to appropriate team
- Setting customer expectations
- Handling sensitive situations

---

### 4. **brand-voice.md**

**Purpose:** Communication guidelines for consistent brand representation.

**Contains:**
- Brand attributes (Friendly, Clear, Empathetic, etc.)
- Tone by channel (email, chat, phone, social)
- Response templates
- Words to use vs. avoid
- Emoji guidelines
- Handling difficult situations

**AI Uses This For:**
- Maintaining consistent tone
- Writing customer responses
- Adapting to different channels
- Handling angry customers
- Professional communication

---

### 5. **sample-tickets.json**

**Purpose:** Training data and examples for AI learning.

**Contains:**
- 25+ real-world customer inquiries
- Multi-channel examples (email, WhatsApp, web form)
- Sentiment scores
- Priority levels
- Expected escalation decisions
- Expected responses

**AI Uses This For:**
- Learning response patterns
- Understanding sentiment
- Practicing escalation decisions
- Training on edge cases
- Improving response quality

---

## 🚀 How to Use These Files

### For AI Agent Training

1. **Load Context into Knowledge Base:**
   ```bash
   # Script to load markdown files into vector database
   python scripts/load_knowledge_base.py context/
   ```

2. **Index for Semantic Search:**
   - Files are converted to embeddings
   - Stored in PostgreSQL with pgvector
   - AI searches using vector similarity

3. **Query During Conversations:**
   ```python
   # AI searches knowledge base
   results = await search_knowledge_base(query="Pro plan pricing")
   # Returns relevant sections from product-docs.md
   ```

---

### For Human Support Agents

1. **Reference During Escalations:**
   - Check escalation-rules.md for priority
   - Use brand-voice.md for response templates
   - Consult product-docs.md for accurate info

2. **Training New Hires:**
   - company-profile.md → Company orientation
   - product-docs.md → Product training
   - brand-voice.md → Communication training
   - sample-tickets.json → Scenario practice

---

## 📊 Knowledge Base Architecture

### Data Flow

```
┌─────────────────┐
│ Context Files   │
│ (.md, .json)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Load & Parse    │
│ (Python Script) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Generate        │
│ Embeddings      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ PostgreSQL      │
│ + pgvector      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ AI Agent        │
│ Semantic Search │
└─────────────────┘
```

---

## 🔧 Maintenance

### Updating Content

**When to Update:**
- Product features change
- Pricing updates
- New integrations added
- Company news/announcements
- New escalation scenarios discovered

**How to Update:**
1. Edit relevant markdown file
2. Re-run knowledge base load script
3. Test AI responses with sample queries
4. Monitor customer interactions for accuracy

### Quality Assurance

**Weekly Checks:**
- Review AI responses for accuracy
- Check if knowledge base has latest info
- Update sample-tickets.json with new scenarios
- Verify escalation rules are current

**Monthly Reviews:**
- Full content audit
- Remove outdated information
- Add new product features
- Update pricing if changed

---

## 📈 Best Practices

### Writing for AI Consumption

1. **Use Clear Headings:**
   ```markdown
   ## Pricing Plans
   ### Free Plan
   ### Pro Plan
   ### Enterprise Plan
   ```

2. **Structure Information:**
   ```markdown
   **Feature:** Time Tracking
   **Available On:** Pro, Enterprise
   **How To:** Click timer icon on any task
   ```

3. **Include Examples:**
   ```markdown
   **Example Response:**
   "The Pro plan costs $29/month and includes unlimited projects, 
   time tracking, and 100GB storage."
   ```

4. **Use Tables for Comparisons:**
   ```markdown
   | Feature | Free | Pro | Enterprise |
   |---------|------|-----|------------|
   | Projects | 3 | Unlimited | Unlimited |
   ```

---

## 🎯 Context for Different Scenarios

### Scenario 1: Pricing Question

**Customer:** "What's the Pro plan pricing?"

**AI Searches:**
- product-docs.md → Pricing Plans section
- Returns: "$29/month per team"

**AI Response:**
"The Pro plan costs $29/month per team and includes unlimited projects, 
advanced task management, time tracking, 100GB storage, and email support."

---

### Scenario 2: Escalation Decision

**Customer:** "I'm canceling! Your competitor is cheaper!"

**AI Analyzes:**
- Sentiment: -0.5 (Negative)
- Keywords: "canceling", "competitor"
- escalation-rules.md → Churn risk → HIGH priority

**AI Action:**
- Escalate to retention team
- Offer retention discount
- Connect with specialist

---

### Scenario 3: How-To Question

**Customer:** "How do I export my data?"

**AI Searches:**
- product-docs.md → Export section
- Returns: Step-by-step instructions

**AI Response:**
"To export your data:
1. Go to Settings → Export
2. Choose format (CSV, JSON, PDF)
3. Select date range
4. Click 'Export'

You'll receive an email when the export is ready!"

---

## 🔐 Security & Access

### Who Can Edit

**Context Files:**
- Product team → product-docs.md
- Marketing → company-profile.md, brand-voice.md
- Support lead → escalation-rules.md
- All team members → Can suggest updates

**Sample Tickets:**
- Support team → Add new scenarios
- AI trainers → Update training data

### Version Control

- All files in Git repository
- Changes require PR review
- Monthly audit of all changes
- Rollback capability if needed

---

## 📚 Additional Resources

### Related Documentation

- `/specs/customer-success-fte-spec.md` - Full agent specification
- `/backend/app/agent/` - AI agent implementation
- `/backend/app/services/automation/auto_responder.py` - Auto-response logic

### External References

- [Agent Maturity Model](https://agentfactory.panaversity.org/docs/General-Agents-Foundations/agent-factory-paradigm/the-2025-inflection-point#the-agent-maturity-model)
- [OpenAI Agents SDK](https://platform.openai.com/docs/agents)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

## ✅ Checklist: Adding New Context

When adding new information to knowledge base:

- [ ] Information is accurate and up-to-date
- [ ] Clear headings and structure
- [ ] Includes examples where relevant
- [ ] Tone matches brand-voice.md
- [ ] Escalation rules updated if needed
- [ ] Sample tickets updated with new scenarios
- [ ] Run knowledge base load script
- [ ] Test AI responses
- [ ] Document changes in changelog

---

## 🎓 Training Exercises

### Exercise 1: Context Lookup

**Query:** "Do you offer discounts for nonprofits?"

**Expected AI Action:**
1. Search product-docs.md → Pricing section
2. Find: "50% off for nonprofits"
3. Respond with accurate info

**Test Command:**
```bash
python test_knowledge_base.py --query "nonprofit discount"
```

---

### Exercise 2: Escalation Decision

**Scenario:** Customer says "I want to speak to your manager!"

**Expected AI Action:**
1. Analyze sentiment: -0.7 (Very Negative)
2. Check escalation-rules.md → Explicit request for human
3. Escalate with HIGH priority
4. Use appropriate response template

---

### Exercise 3: Brand Voice

**Task:** Rewrite this response in TechFlow brand voice:

**Original:** "Per policy, refunds unavailable after 30 days."

**Better:** "I understand you'd like a refund. Our 30-day window has passed, 
but let me see what options we have..."

---

## 📞 Support

For questions about context files or knowledge base:

- **Technical Issues:** #support-engineering Slack channel
- **Content Updates:** #support-content Slack channel
- **AI Training:** #support-ai-training Slack channel

**Contact:**
- Support Lead: support-lead@techflow.io
- AI Team: ai-team@techflow.io

---

**Last Updated:** March 2026  
**Version:** 1.0  
**Maintained By:** Customer Success & AI Teams
