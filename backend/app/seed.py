"""
Database Seeding Script.

Populates the database with sample data for development and testing.
Run with: uv run python -m app.seed
"""
import asyncio
import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel, select

from app.config import get_settings
from app.models.customer import Customer
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.ticket import Ticket
from app.models.knowledge_base import KnowledgeBase
from app.models.channel import Channel, ChannelIdentity


async def seed_database():
    """Seed the database with sample data."""
    
    settings = get_settings()
    
    # Convert URL for asyncpg
    db_url = settings.database_url
    if not db_url.startswith('postgresql+asyncpg://'):
        db_url = db_url.replace('postgresql://', 'postgresql+asyncpg://')
    db_url = db_url.replace('?sslmode=require', '')
    
    # Create engine
    engine = create_async_engine(
        db_url,
        connect_args={"ssl": True},
    )
    
    async with engine.begin() as conn:
        # Create tables if they don't exist
        await conn.run_sync(SQLModel.metadata.create_all)
    
    # Use async session for data operations
    from sqlmodel.ext.asyncio.session import AsyncSession
    
    async with AsyncSession(engine) as session:
        print("Seeding database...")
        
        # Check if already seeded
        result = await session.exec(select(Customer).limit(1))
        if result.first():
            print("WARNING: Database already has data. Skipping seed.")
            await engine.dispose()
            return
        
        # ==================== CHANNELS ====================
        print("  - Seeding channels...")
        channels = [
            Channel(id=1, name="gmail", description="Gmail Email", is_active=True),
            Channel(id=2, name="whatsapp", description="WhatsApp Messaging", is_active=True),
            Channel(id=3, name="web", description="Web Support Form", is_active=True),
        ]
        for channel in channels:
            session.add(channel)
        await session.flush()
        
        # ==================== KNOWLEDGE BASE (5 articles) ====================
        print("  - Seeding knowledge base articles...")
        knowledge_base_articles = [
            KnowledgeBase(
                title="How to Reset Your Password",
                content="""
To reset your password:
1. Go to the login page
2. Click 'Forgot Password'
3. Enter your email address
4. Check your email for the reset link
5. Click the link and create a new password
6. Your password must be at least 8 characters long

If you don't receive the email within 5 minutes, check your spam folder.
""",
                source="custom",
                category="Account",
                tags=["password", "reset", "account", "login"],
                is_active=True,
            ),
            KnowledgeBase(
                title="Billing and Payment Methods",
                content="""
We accept the following payment methods:
- Credit/Debit Cards (Visa, MasterCard, American Express)
- PayPal
- Bank Transfer (for enterprise plans)

Billing Cycle:
- Monthly plans are billed on the same day each month
- Annual plans are billed once per year
- Prorated charges apply for mid-cycle upgrades

To update your payment method:
1. Go to Account Settings
2. Click 'Billing'
3. Select 'Update Payment Method'
4. Enter your new payment details
""",
                source="custom",
                category="Billing",
                tags=["billing", "payment", "invoice", "subscription"],
                is_active=True,
            ),
            KnowledgeBase(
                title="Refund Policy",
                content="""
Our refund policy guidelines:

Eligible for Refund:
- Service outages lasting more than 24 hours
- Accidental duplicate charges
- Cancellation within 14 days of initial purchase

Not Eligible for Refund:
- Partial month usage
- Plan downgrades
- Usage over limits

To request a refund:
1. Contact our support team
2. Provide your account details
3. Explain the reason for refund request
4. Our team will review within 2-3 business days

Refunds are processed to the original payment method within 5-7 business days.
""",
                source="custom",
                category="Billing",
                tags=["refund", "billing", "policy", "cancellation"],
                is_active=True,
            ),
            KnowledgeBase(
                title="Account Security Best Practices",
                content="""
Protect your account with these security best practices:

Password Security:
- Use at least 8 characters
- Include uppercase, lowercase, numbers, and symbols
- Don't reuse passwords from other sites
- Change your password every 90 days

Two-Factor Authentication (2FA):
- Enable 2FA in Account Settings
- Use an authenticator app (Google Authenticator, Authy)
- Save backup codes in a secure location

Account Monitoring:
- Review login activity regularly
- Enable login notifications
- Report suspicious activity immediately

If you suspect unauthorized access:
1. Change your password immediately
2. Review recent account activity
3. Contact support to secure your account
""",
                source="custom",
                category="Security",
                tags=["security", "password", "2FA", "account"],
                is_active=True,
            ),
            KnowledgeBase(
                title="Contact Support",
                content="""
Getting help from our support team:

Support Channels:
- Email: support@example.com
- Live Chat: Available 24/7 from your dashboard
- Phone: 1-800-EXAMPLE (Business hours: 9 AM - 6 PM EST)

Response Times:
- Critical issues: Within 1 hour
- High priority: Within 4 hours
- Normal priority: Within 24 hours
- Low priority: Within 48 hours

Before contacting support, please have ready:
- Your account email address
- Description of the issue
- Steps to reproduce (if applicable)
- Any error messages you received

For faster service, use live chat for urgent issues.
""",
                source="custom",
                category="Support",
                tags=["support", "contact", "help", "service"],
                is_active=True,
            ),
        ]
        for article in knowledge_base_articles:
            session.add(article)
        await session.flush()
        
        # ==================== CUSTOMERS (3 customers) ====================
        print("  - Seeding customers...")
        customers = [
            Customer(
                id=uuid.UUID("11111111-1111-1111-1111-111111111111"),
                email="john.doe@example.com",
                phone="+1-555-0101",
                name="John Doe",
                custom_metadata={"plan": "premium", "signup_date": "2024-01-15"},
            ),
            Customer(
                id=uuid.UUID("22222222-2222-2222-2222-222222222222"),
                email="jane.smith@company.com",
                phone="+1-555-0102",
                name="Jane Smith",
                custom_metadata={"plan": "enterprise", "company": "Acme Corp"},
            ),
            Customer(
                id=uuid.UUID("33333333-3333-3333-3333-333333333333"),
                email="bob.wilson@startup.io",
                phone="+1-555-0103",
                name="Bob Wilson",
                custom_metadata={"plan": "basic", "referral": "partner"},
            ),
        ]
        for customer in customers:
            session.add(customer)
        await session.flush()
        
        # Channel identities
        channel_identities = [
            ChannelIdentity(
                customer_id=customers[0].id,
                channel_id=1,  # Gmail
                channel_identifier="john.doe@example.com",
            ),
            ChannelIdentity(
                customer_id=customers[1].id,
                channel_id=1,  # Gmail
                channel_identifier="jane.smith@company.com",
            ),
            ChannelIdentity(
                customer_id=customers[2].id,
                channel_id=3,  # Web
                channel_identifier="bob.wilson@startup.io",
            ),
        ]
        for identity in channel_identities:
            session.add(identity)
        await session.flush()
        
        # ==================== CONVERSATIONS & TICKETS (5 tickets) ====================
        print("  - Seeding tickets and conversations...")
        
        now = datetime.now(timezone.utc)
        
        tickets_data = [
            {
                "customer": customers[0],
                "status": "open",
                "priority": "high",
                "subject": "Unable to access my account",
                "sentiment_score": -0.6,
                "confidence_score": 0.85,
                "messages": [
                    ("customer", "I can't log in to my account. It keeps saying my password is wrong but I know it's correct!"),
                    ("agent", "I understand your frustration. Let me help you with that. Can you tell me what email address you're using?"),
                ],
            },
            {
                "customer": customers[1],
                "status": "in_progress",
                "priority": "normal",
                "subject": "Question about enterprise features",
                "sentiment_score": 0.3,
                "confidence_score": 0.92,
                "messages": [
                    ("customer", "Hi, I'm interested in learning more about the enterprise features. Specifically the API rate limits."),
                    ("agent", "Hello! I'd be happy to help. Our enterprise plan includes 10,000 API calls per hour. Would you like me to send you our enterprise features document?"),
                ],
            },
            {
                "customer": customers[2],
                "status": "open",
                "priority": "urgent",
                "subject": "Billing error - charged twice",
                "sentiment_score": -0.8,
                "confidence_score": 0.78,
                "messages": [
                    ("customer", "I was charged twice for my subscription this month! This is unacceptable. I want a refund immediately."),
                ],
            },
            {
                "customer": customers[0],
                "status": "resolved",
                "priority": "low",
                "subject": "How to export my data",
                "sentiment_score": 0.5,
                "confidence_score": 0.95,
                "messages": [
                    ("customer", "Is there a way to export all my data?"),
                    ("agent", "Yes! Go to Settings > Data > Export. You can download everything as a CSV or JSON file."),
                    ("customer", "Perfect, thank you!"),
                ],
            },
            {
                "customer": customers[1],
                "status": "waiting_customer",
                "priority": "normal",
                "subject": "Integration with Slack",
                "sentiment_score": 0.1,
                "confidence_score": 0.88,
                "messages": [
                    ("customer", "Do you have a Slack integration?"),
                    ("agent", "Yes, we do! I've sent you the setup guide. Let me know if you need any help configuring it."),
                ],
            },
        ]
        
        for ticket_data in tickets_data:
            # Create conversation
            conversation = Conversation(
                customer_id=ticket_data["customer"].id,
                status="active",
                message_count=len(ticket_data["messages"]),
            )
            session.add(conversation)
            await session.flush()
            
            # Create ticket (conversation relationship is via ticket.conversation_id)
            ticket = Ticket(
                customer_id=ticket_data["customer"].id,
                conversation_id=conversation.id,
                status=ticket_data["status"],
                priority=ticket_data["priority"],
                subject=ticket_data["subject"],
                sentiment_score=ticket_data["sentiment_score"],
                confidence_score=ticket_data["confidence_score"],
            )
            session.add(ticket)
            await session.flush()
            
            # Create messages
            for sender_type, content in ticket_data["messages"]:
                message = Message(
                    conversation_id=conversation.id,
                    sender_type=sender_type,
                    channel="web",
                    role="user" if sender_type == "customer" else "assistant",
                    content=content,
                )
                session.add(message)
        
        # Commit all changes
        await session.commit()
        
        print("SUCCESS: Database seeded successfully!")
        print(f"   - 3 channels")
        print(f"   - 5 knowledge base articles")
        print(f"   - 3 customers")
        print(f"   - 5 tickets with conversations")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_database())
