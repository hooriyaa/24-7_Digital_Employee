# Field Mapping Documentation

## Frontend → Backend → Database Flow

### 1. Frontend (components/new-ticket-form.tsx)

**Form Fields:**
```typescript
formData = {
  customer_name: string,      // "John Doe"
  customer_email: string,     // "john@example.com"
  customer_phone: string,     // "+1-234-567-8900"
  subject: string,            // "Pricing question"
  message: string,            // "Hello, I need help with pricing..."
  channel: string,            // "web"
  priority: string            // "normal"
}
```

**POST Request Body (exactly as sent):**
```json
{
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "customer_phone": "+1-234-567-8900",
  "subject": "Pricing question",
  "message": "Hello, I need help with pricing. What plans are available?",
  "channel": "web",
  "priority": "normal"
}
```

---

### 2. Backend (app/api/routes_tickets.py)

**Request Schema (app/schemas/agent.py):**
```python
class AgentRequest(BaseModel):
    customer_name: Optional[str]
    customer_email: Optional[str]
    customer_phone: Optional[str]
    subject: Optional[str]           # ← Ticket subject
    message: Optional[str]           # ← Message content
    channel: Optional[str]
    priority: Optional[str]
```

**Field Mapping in create_ticket endpoint:**

| Request Field | Goes To | Database Table | Column |
|--------------|---------|----------------|--------|
| `customer_email` | Customer | `customers` | `email` |
| `customer_name` | Customer | `customers` | `name` |
| `customer_phone` | Customer | `customers` | `phone` |
| `subject` | **Ticket** | `tickets` | `subject` |
| `message` | **Message** | `messages` | `content` |
| `channel` | Conversation | `conversations` | `channel` |
| `priority` | Ticket | `tickets` | `priority` |

---

### 3. Database Schema

**customers table:**
```sql
CREATE TABLE customers (
    id UUID PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    ...
);
```

**conversations table:**
```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY,
    customer_id UUID REFERENCES customers(id),
    channel VARCHAR(50),
    status VARCHAR(50),
    ...
);
```

**tickets table:**
```sql
CREATE TABLE tickets (
    id UUID PRIMARY KEY,
    customer_id UUID REFERENCES customers(id),
    conversation_id UUID REFERENCES conversations(id),
    subject VARCHAR(500),        -- ← request.subject goes here
    priority VARCHAR(20),
    status VARCHAR(50),
    ...
);
```

**messages table:**
```sql
CREATE TABLE messages (
    id UUID PRIMARY KEY,
    conversation_id UUID REFERENCES conversations(id),
    content TEXT NOT NULL,       -- ← request.message goes here
    sender_type VARCHAR(20),
    role VARCHAR(50),
    ...
);
```

---

## Verification Steps

### Test with curl:
```bash
curl -X POST http://localhost:8000/api/v1/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Test User",
    "customer_email": "test@example.com",
    "subject": "My Subject",
    "message": "My Message Content",
    "channel": "web",
    "priority": "normal"
  }'
```

### Expected Backend Logs:
```
🎫 CREATE TICKET REQUEST: ...
📋 Request fields:
   - subject: My Subject
   - message: My Message Content
   - customer_email: test@example.com
   - customer_name: Test User
📝 Ticket subject: My Subject
✅ Ticket created: <uuid>
📋 Ticket.subject stored as: My Subject
💬 Creating message with content: My Message Content...
✅ Message created: <uuid>
📋 Message.content stored as: My Message Content
```

### Verify in Database:
```sql
-- Check ticket subject
SELECT id, subject FROM tickets ORDER BY created_at DESC LIMIT 1;

-- Check message content
SELECT m.id, m.content, m.conversation_id
FROM messages m
ORDER BY m.created_at DESC
LIMIT 1;
```

**Expected Result:**
- `tickets.subject` = "My Subject" ✅
- `messages.content` = "My Message Content" ✅

---

## Common Issues

### Issue: Subject and Message are the same
**Cause**: Frontend sending same value for both fields
**Fix**: Check formData in new-ticket-form.tsx line 75-82

### Issue: Message is null in database
**Cause**: `request.message` is empty or not sent
**Fix**: Verify frontend form has `message` field and it's not empty

### Issue: Subject shows "New Support Request"
**Cause**: `request.subject` is null/undefined
**Fix**: Check frontend form has `subject` field populated

---

## Files Modified

1. **backend/app/api/routes_tickets.py** - Added detailed logging for field mapping
2. **backend/test_post.py** - Shows exact JSON being sent
3. **frontend/components/new-ticket-form.tsx** - Already correct (no changes needed)
4. **frontend/lib/api.ts** - Already correct (no changes needed)
