"""
Test WhatsApp Polling Service
"""
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def test_polling():
    """Test polling once."""
    from app.services.whatsapp_polling import whatsapp_polling_service
    
    print("\n📱 Testing WhatsApp Polling Service...\n")
    
    # Test get_received_messages
    messages = await whatsapp_polling_service.get_received_messages(limit=10)
    
    print(f"\n📦 Found {len(messages)} messages\n")
    
    if messages:
        for msg in messages:
            print(f"📨 Message: {msg}")
    else:
        print("⚠️  No messages found\n")
        print("💡 Possible reasons:")
        print("   1. No WhatsApp messages received yet")
        print("   2. Internet connection issue")
        print("   3. UltraMsg API credentials incorrect")
        print("   4. UltraMsg API is down")
    
    print("\n✅ Test completed\n")

if __name__ == "__main__":
    asyncio.run(test_polling())
