"""
Test script to verify ticket creation API.

Sends a fake ticket creation request to the API.

Usage:
    cd backend
    .venv\Scripts\activate
    python test_post.py
"""
import httpx
import json

API_URL = "http://localhost:8000/api/v1/tickets"

# Test data - NO SUBJECT, only message
test_ticket = {
    "customer_name": "Test Customer",
    "customer_email": "test@example.com",
    "customer_phone": "+1-234-567-8900",
    "message": "Hello, I need help with your product. Can you please explain the pricing plans available?",
    "channel": "web",
    "priority": "normal"
}

print("=" * 60)
print("Testing Ticket Creation API")
print("=" * 60)
print(f"\nPOST {API_URL}")
print(f"\nEXACT JSON BEING SENT:")
print(json.dumps(test_ticket, indent=2))
print("\n" + "=" * 60)

try:
    with httpx.Client() as client:
        response = client.post(API_URL, json=test_ticket, timeout=30.0)
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"\nResponse Body:")
        
        try:
            response_json = response.json()
            print(json.dumps(response_json, indent=2))
            
            if response.status_code == 201:
                print("\n" + "=" * 60)
                print("SUCCESS! Ticket created successfully!")
                print("=" * 60)
                print(f"\nTicket ID: {response_json.get('id')}")
                print(f"Customer ID: {response_json.get('customer_id')}")
                print(f"Conversation ID: {response_json.get('conversation_id')}")
                print(f"Status: {response_json.get('status')}")
                print(f"Subject: {response_json.get('subject')}")
            else:
                print("\n" + "=" * 60)
                print(f"FAILED! Status code: {response.status_code}")
                print("=" * 60)
                print(f"\nError Detail: {response_json.get('detail', 'Unknown error')}")
                
        except json.JSONDecodeError:
            print(response.text)
            
except httpx.ConnectError as e:
    print(f"\n❌ CONNECTION ERROR!")
    print("=" * 60)
    print(f"Could not connect to {API_URL}")
    print("\nMake sure the backend server is running:")
    print("  cd backend")
    print("  .venv\\Scripts\\activate")
    print("  uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    print(f"\nError: {e}")
    
except Exception as e:
    print(f"\n❌ UNEXPECTED ERROR: {type(e).__name__}")
    print("=" * 60)
    print(f"Error: {e}")
